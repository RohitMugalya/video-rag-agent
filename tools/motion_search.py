import spaces
import torch
from langchain_core.tools import tool

from core.models import load_viclip, run_with_gpu_fallback
from core.prompt_loader import load_prompt
from core.session import library_video_ids, resolve_video_path
from core.video_io import frames2tensor, get_raw_frames

DISTRACTOR_ACTIONS = ["a person standing still", "an empty scene with no activity", "a static parked scene"]


@spaces.GPU(duration=120)
def _motion_search_gpu(query: str, top_k: int = 5) -> dict:
    clip, tokenizer, device = load_viclip()
    candidates = [query] + [d for d in DISTRACTOR_ACTIONS if d != query]
    text_feat_d = {}
    text_feats = [clip.get_text_features(t, tokenizer, text_feat_d) for t in candidates]
    text_feats_tensor = torch.cat(text_feats, 0)

    all_clusters = []
    for video_id in library_video_ids():
        path = resolve_video_path(video_id)
        frames, fps = get_raw_frames(path)
        if not frames or not fps:
            continue
        duration = len(frames) / fps
        window_sec, stride_sec = 3.0, 1.5
        window_scores = []
        t = 0.0
        while t < duration:
            start_idx, end_idx = int(t * fps), int((t + window_sec) * fps)
            window_frames = frames[start_idx:end_idx]
            if len(window_frames) >= 8:
                frames_tensor = frames2tensor(window_frames).to(device)
                vid_feat = clip.get_vid_features(frames_tensor)
                probs, idxs = clip.get_predict_label(vid_feat, text_feats_tensor, top=len(candidates))
                probs_np = probs.cpu().numpy()[0]
                idxs_np = idxs.cpu().numpy()[0]
                score_map = {candidates[i]: p for i, p in zip(idxs_np, probs_np)}
                window_scores.append((t, min(t + window_sec, duration), float(score_map.get(query, 0.0))))
            t += stride_sec

        clusters, threshold = [], 0.15
        for start, end, score in window_scores:
            if score < threshold:
                continue
            if clusters and start - clusters[-1]["end_ts"] <= stride_sec + 0.5:
                clusters[-1]["end_ts"] = end
                if score > clusters[-1]["score"]:
                    clusters[-1]["score"] = score
            else:
                clusters.append(
                    {
                        "video_id": video_id,
                        "start_ts": round(start, 1),
                        "end_ts": round(end, 1),
                        "action_label": query,
                        "score": score,
                    }
                )
        all_clusters.extend(clusters)

    all_clusters.sort(key=lambda c: -c["score"])
    if not all_clusters:
        return {"results": [{"action_label": query, "note": "no matching motion found in any video in the library"}], "ran_on_cpu": False}
    return {"results": all_clusters[:top_k], "ran_on_cpu": False}


def _motion_search_cpu(query: str, top_k: int = 5) -> dict:
    clip, tokenizer, device = load_viclip()
    clip = clip.to("cpu")
    try:
        candidates = [query] + [d for d in DISTRACTOR_ACTIONS if d != query]
        text_feat_d = {}
        text_feats = [clip.get_text_features(t, tokenizer, text_feat_d) for t in candidates]
        text_feats_tensor = torch.cat(text_feats, 0)

        all_clusters = []
        for video_id in library_video_ids():
            path = resolve_video_path(video_id)
            frames, fps = get_raw_frames(path)
            if not frames or not fps:
                continue
            duration = len(frames) / fps
            window_sec, stride_sec = 3.0, 1.5
            window_scores = []
            t = 0.0
            while t < duration:
                start_idx, end_idx = int(t * fps), int((t + window_sec) * fps)
                window_frames = frames[start_idx:end_idx]
                if len(window_frames) >= 8:
                    frames_tensor = frames2tensor(window_frames).to("cpu")
                    vid_feat = clip.get_vid_features(frames_tensor)
                    probs, idxs = clip.get_predict_label(vid_feat, text_feats_tensor, top=len(candidates))
                    probs_np = probs.cpu().numpy()[0]
                    idxs_np = idxs.cpu().numpy()[0]
                    score_map = {candidates[i]: p for i, p in zip(idxs_np, probs_np)}
                    window_scores.append((t, min(t + window_sec, duration), float(score_map.get(query, 0.0))))
                t += stride_sec

            clusters, threshold = [], 0.15
            for start, end, score in window_scores:
                if score < threshold:
                    continue
                if clusters and start - clusters[-1]["end_ts"] <= stride_sec + 0.5:
                    clusters[-1]["end_ts"] = end
                    if score > clusters[-1]["score"]:
                        clusters[-1]["score"] = score
                else:
                    clusters.append(
                        {
                            "video_id": video_id,
                            "start_ts": round(start, 1),
                            "end_ts": round(end, 1),
                            "action_label": query,
                            "score": score,
                        }
                    )
            all_clusters.extend(clusters)

        all_clusters.sort(key=lambda c: -c["score"])
        if not all_clusters:
            return {"results": [{"action_label": query, "note": "no matching motion found in any video in the library"}], "ran_on_cpu": True}
        return {"results": all_clusters[:top_k], "ran_on_cpu": True}
    finally:
        clip.to(device)


def _motion_search(query: str, top_k: int = 5) -> dict:
    result, used_cpu_fallback = run_with_gpu_fallback(
        lambda: _motion_search_gpu(query, top_k),
        lambda: _motion_search_cpu(query, top_k),
    )
    result["ran_on_cpu"] = used_cpu_fallback or result.get("ran_on_cpu", False)
    return result


motion_search = tool(_motion_search, description=load_prompt("motion_search.md"))
