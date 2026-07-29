import cv2
from langchain_core.tools import tool

from core.models import load_ocr
from core.prompt_loader import load_prompt
from core.session import resolve_video_path


def _ocr_read(video_id: str, timestamp: float) -> list:
    reader = load_ocr()
    path = resolve_video_path(video_id)
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = total_frames / fps if fps else 0
    safe_ts = min(max(timestamp, 0), max(duration - 0.15, 0))
    cap.set(cv2.CAP_PROP_POS_MSEC, safe_ts * 1000)
    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None or frame.size == 0:
        return [{"video_id": video_id, "timestamp": timestamp, "extracted_text": "no text detected", "bbox": None}]

    results = reader.readtext(frame)
    frame_area = frame.shape[0] * frame.shape[1]
    filtered = []
    for bbox, text, conf in results:
        xs = [p[0] for p in bbox]
        ys = [p[1] for p in bbox]
        area = (max(xs) - min(xs)) * (max(ys) - min(ys))
        if area / frame_area > 0.01:
            filtered.append({"video_id": video_id, "timestamp": timestamp, "extracted_text": text, "bbox": bbox})

    if not filtered:
        return [{"video_id": video_id, "timestamp": timestamp, "extracted_text": "no text detected", "bbox": None}]
    return filtered


ocr_read = tool(_ocr_read, description=load_prompt("ocr_read.md"))
