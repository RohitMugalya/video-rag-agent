import os
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
VIDEO_DIR = ASSETS_DIR / "videos"
AUDIO_DIR = ASSETS_DIR / "audios"


def fetch_demo_assets():
    manifest = [
        ("car-detection.mp4", "https://raw.githubusercontent.com/RohitMugalya/video-rag-agent/main/assets/videos/car-detection.mp4"),
        ("office_conversation.mp4", "https://raw.githubusercontent.com/RohitMugalya/video-rag-agent/main/assets/videos/office_conversation.mp4"),
        ("person-bicycle-car-detection.mp4", "https://raw.githubusercontent.com/RohitMugalya/video-rag-agent/main/assets/videos/person-bicycle-car-detection.mp4"),
        ("shop_banner.mp4", "https://raw.githubusercontent.com/RohitMugalya/video-rag-agent/main/assets/videos/shop_banner.mp4"),
        ("project_guide.mp3", "https://raw.githubusercontent.com/RohitMugalya/video-rag-agent/main/assets/audios/project_guide.mp3"),
    ]

    for filename, raw_url in manifest:
        if filename == ".gitkeep":
            continue

        target_dir = AUDIO_DIR if filename.endswith(".mp3") else VIDEO_DIR
        target_path = target_dir / filename
        if target_path.exists():
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        with requests.get(raw_url, stream=True, timeout=60) as response:
            response.raise_for_status()
            with open(target_path, "wb") as handle:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        handle.write(chunk)
