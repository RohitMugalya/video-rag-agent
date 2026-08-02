import torch
from langchain_core.tools import tool

from core.models import load_siglip, run_with_gpu_fallback
from core.prompt_loader import load_prompt
from core.session import library_video_ids, resolve_video_path
from core.video_io import extract_frames


def _visual_frame_search_gpu(query: str, top_k: int = 5) -> dict:
    model, processor, device = load_siglip()
    text_inputs = processor(
        text=[f"a video of {query}"], padding="max_length", truncation=True, max_length=64, return_tensors="pt"
    ).to(device)
    with torch.no_grad():
        text_out = model.get_text_features(**text_inputs)
        text_emb = text_out / text_out.norm(dim=-1, keepdim=True)

    all_clusters = []
    for video_id in library_video_ids():
        path = resolve_video_path(video_id)
        frames = extract_frames(path)
        if not frames:
            continue
        timestamps = [t for t, _ in frames]
        images = [f for _, f in frames]
        image_inputs = processor(images=images, return_tensors="pt").to(device)
        with torch.no_grad():
            image_out = model.get_image_features(**image_inputs)
            image_emb = image_out / image_out.norm(dim=-1, keepdim=True)
        logit_scale = model.logit_scale.exp()
        logit_bias = model.logit_bias
        scores = torch.sigmoid((image_emb @ text_emb.T * logit_scale + logit_bias)).squeeze(-1).detach().cpu().numpy()

        scored = sorted(zip(timestamps, scores.tolist()), key=lambda x: x[0])
        clusters, threshold = [], 0.3
        for t, s in scored:
            if s < threshold:
                continue
            if clusters and t - clusters[-1]["end_ts"] <= 2.0:
                clusters[-1]["end_ts"] = t
                if s > clusters[-1]["score"]:
                    clusters[-1]["peak_timestamp"] = t
                    clusters[-1]["score"] = s
            else:
                clusters.append(
                    {"video_id": video_id, "start_ts": t, "end_ts": t, "peak_timestamp": t, "score": s}
                )
        all_clusters.extend(clusters)

    all_clusters.sort(key=lambda c: -c["score"])
    if not all_clusters:
        return {"results": [{"note": "no matching visual content found in any video in the library"}], "ran_on_cpu": False}
    return {"results": all_clusters[:top_k], "ran_on_cpu": False}


def _visual_frame_search_cpu(query: str, top_k: int = 5) -> dict:
    model, processor, device = load_siglip()
    model = model.to("cpu")
    try:
        text_inputs = processor(
            text=[f"a video of {query}"], padding="max_length", truncation=True, max_length=64, return_tensors="pt"
        ).to("cpu")
        with torch.no_grad():
            text_out = model.get_text_features(**text_inputs)
            text_emb = text_out / text_out.norm(dim=-1, keepdim=True)

        all_clusters = []
        for video_id in library_video_ids():
            path = resolve_video_path(video_id)
            frames = extract_frames(path)
            if not frames:
                continue
            timestamps = [t for t, _ in frames]
            images = [f for _, f in frames]
            image_inputs = processor(images=images, return_tensors="pt").to("cpu")
            with torch.no_grad():
                image_out = model.get_image_features(**image_inputs)
                image_emb = image_out / image_out.norm(dim=-1, keepdim=True)
            logit_scale = model.logit_scale.exp()
            logit_bias = model.logit_bias
            scores = torch.sigmoid((image_emb @ text_emb.T * logit_scale + logit_bias)).squeeze(-1).detach().cpu().numpy()

            scored = sorted(zip(timestamps, scores.tolist()), key=lambda x: x[0])
            clusters, threshold = [], 0.3
            for t, s in scored:
                if s < threshold:
                    continue
                if clusters and t - clusters[-1]["end_ts"] <= 2.0:
                    clusters[-1]["end_ts"] = t
                    if s > clusters[-1]["score"]:
                        clusters[-1]["peak_timestamp"] = t
                        clusters[-1]["score"] = s
                else:
                    clusters.append(
                        {"video_id": video_id, "start_ts": t, "end_ts": t, "peak_timestamp": t, "score": s}
                    )
            all_clusters.extend(clusters)

        all_clusters.sort(key=lambda c: -c["score"])
        if not all_clusters:
            return {"results": [{"note": "no matching visual content found in any video in the library"}], "ran_on_cpu": True}
        return {"results": all_clusters[:top_k], "ran_on_cpu": True}
    finally:
        model.to(device)


def _visual_frame_search(query: str, top_k: int = 5) -> dict:
    result, used_cpu_fallback = run_with_gpu_fallback(
        lambda: _visual_frame_search_gpu(query, top_k),
        lambda: _visual_frame_search_cpu(query, top_k),
    )
    result["ran_on_cpu"] = used_cpu_fallback or result.get("ran_on_cpu", False)
    if result.get("ran_on_cpu"):
        result["note"] = "GPU is currently unavailable, so this search ran on CPU."
    return result


visual_frame_search = tool(_visual_frame_search, description=load_prompt("visual_frame_search.md"))
