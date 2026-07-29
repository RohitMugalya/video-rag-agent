import os
import string
import subprocess

from langchain_core.tools import tool

from core.models import load_whisper
from core.prompt_loader import load_prompt
from core.session import library_video_ids, resolve_video_path


def _transcript_search(query: str, top_k: int = 5) -> list:
    model = load_whisper()
    all_results = []
    for video_id in library_video_ids():
        path = resolve_video_path(video_id)
        audio_path = f"{path}.wav"
        if not os.path.exists(audio_path):
            subprocess.run(["ffmpeg", "-y", "-i", path, "-ar", "16000", "-ac", "1", audio_path], capture_output=True)
        segments, _ = model.transcribe(audio_path)
        for seg in segments:
            all_results.append(
                {"video_id": video_id, "start_ts": seg.start, "end_ts": seg.end, "transcript_text": seg.text}
            )

    query_words = set(query.lower().translate(str.maketrans("", "", string.punctuation)).split())
    scored = []
    for r in all_results:
        clean_text = r["transcript_text"].lower().translate(str.maketrans("", "", string.punctuation))
        score = len(query_words & set(clean_text.split())) / len(query_words) if query_words else 0
        scored.append({**r, "score": score})
    scored.sort(key=lambda r: -r["score"])

    if not scored or all(r["score"] == 0 for r in scored):
        return [{"note": "no relevant speech found in any video in the library"}]
    return [r for r in scored if r["score"] > 0][:top_k]


transcript_search = tool(_transcript_search, description=load_prompt("transcript_search.md"))
