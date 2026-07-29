import os
import shutil
import tempfile

from core.context import get_session_id
from core.video_io import VIDEO_EXTENSIONS

ASSETS_VIDEO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "videos")


def _video_id_from_filename(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def get_session_upload_dir(session_id=None):
    session_id = session_id or get_session_id()
    session_dir = os.path.join(tempfile.gettempdir(), "video_rag_sessions", session_id)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


def fixed_video_ids():
    if not os.path.isdir(ASSETS_VIDEO_DIR):
        return []
    return sorted(
        _video_id_from_filename(f)
        for f in os.listdir(ASSETS_VIDEO_DIR)
        if f.lower().endswith(VIDEO_EXTENSIONS)
    )


def session_video_ids(session_id=None):
    upload_dir = get_session_upload_dir(session_id)
    return sorted(
        _video_id_from_filename(f)
        for f in os.listdir(upload_dir)
        if f.lower().endswith(VIDEO_EXTENSIONS)
    )


def library_video_ids(session_id=None):
    return fixed_video_ids() + session_video_ids(session_id)


def resolve_video_path(video_id, session_id=None):
    for ext in VIDEO_EXTENSIONS:
        fixed_path = os.path.join(ASSETS_VIDEO_DIR, f"{video_id}{ext}")
        if os.path.exists(fixed_path):
            return fixed_path
    upload_dir = get_session_upload_dir(session_id)
    for ext in VIDEO_EXTENSIONS:
        session_path = os.path.join(upload_dir, f"{video_id}{ext}")
        if os.path.exists(session_path):
            return session_path
    raise FileNotFoundError(f"No video file found for video_id: {video_id}")


def save_uploaded_video(uploaded_filepath, session_id=None):
    upload_dir = get_session_upload_dir(session_id)
    filename = os.path.basename(uploaded_filepath)
    dest_path = os.path.join(upload_dir, filename)
    shutil.copyfile(uploaded_filepath, dest_path)
    return _video_id_from_filename(filename)


def clear_session_uploads(session_id=None):
    upload_dir = get_session_upload_dir(session_id)
    shutil.rmtree(upload_dir, ignore_errors=True)
    os.makedirs(upload_dir, exist_ok=True)
