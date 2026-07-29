import spaces
import torch
from langchain_core.tools import tool

from core.models import load_siglip
from core.prompt_loader import load_prompt
from core.session import resolve_video_path
from core.video_io import extract_frames


@spaces.GPU(duration=30)
def _zero_shot_classify(video_id: str, timestamp: float, labels: list, is_range_end: float = None) -> dict:
    model, processor = load_siglip()
    target_ts = timestamp if is_range_end is None else (timestamp + is_range_end) / 2
    path = resolve_video_path(video_id)
    frames = extract_frames(path)
    closest = min(frames, key=lambda f: abs(f[0] - target_ts))
    image = closest[1]

    text_inputs = processor(text=labels, padding="max_length", truncation=True, max_length=64, return_tensors="pt")
    image_inputs = processor(images=[image], return_tensors="pt")
    with torch.no_grad():
        text_out = model.get_text_features(**text_inputs)
        image_out = model.get_image_features(**image_inputs)
        text_emb = text_out / text_out.norm(dim=-1, keepdim=True)
        image_emb = image_out / image_out.norm(dim=-1, keepdim=True)
        scores = (image_emb @ text_emb.T).squeeze(0).tolist()

    return {"video_id": video_id, **dict(zip(labels, scores))}


zero_shot_classify = tool(_zero_shot_classify, description=load_prompt("zero_shot_classify.md"))
