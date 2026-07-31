import os

import gradio as gr

from core.session import fixed_video_ids, get_session_upload_dir, save_uploaded_video, session_video_ids
from core.video_io import VIDEO_EXTENSIONS

ASSETS_VIDEO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "videos")


def _resolve_video_path(base_dir, video_id):
    for ext in VIDEO_EXTENSIONS:
        video_path = os.path.join(base_dir, f"{video_id}{ext}")
        if os.path.exists(video_path):
            return video_path
    return None


def _library_gallery(video_ids, base_dir):
    return [
        _resolve_video_path(base_dir, video_id)
        for video_id in video_ids
        if _resolve_video_path(base_dir, video_id) is not None
    ]


def _on_upload(file, request: gr.Request):
    if file is not None:
        save_uploaded_video(file, request.session_hash)
    upload_dir = get_session_upload_dir(request.session_hash)
    return gr.Gallery.update(value=_library_gallery(session_video_ids(request.session_hash), upload_dir), columns=2, object_fit="cover")


def render_library_tab():
    gr.Markdown("### Video Library")

    gr.Markdown("**Pre-loaded sample videos**")
    sample_gallery = gr.Gallery(
        value=_library_gallery(fixed_video_ids(), ASSETS_VIDEO_DIR),
        columns=2,
        object_fit="cover",
    )

    gr.Markdown("**Your uploaded videos (this session only)**")
    session_gallery = gr.Gallery(columns=2, object_fit="cover")

    uploader = gr.File(label="Add a video to your session", file_types=list(VIDEO_EXTENSIONS))
    uploader.upload(_on_upload, inputs=uploader, outputs=session_gallery)
