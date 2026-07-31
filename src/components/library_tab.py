import os

import gradio as gr

from core.session import fixed_video_ids, save_uploaded_video, session_video_ids
from core.video_io import VIDEO_EXTENSIONS


def _resolve_video_path(base_dir, video_id):
    for ext in VIDEO_EXTENSIONS:
        video_path = os.path.join(base_dir, f"{video_id}{ext}")
        if os.path.exists(video_path):
            return video_path
    return None


def _build_video_grid(video_ids, base_dir):
    if not video_ids:
        return "<div style='color:#6b7280;'>No videos yet.</div>"

    items = []
    for video_id in video_ids:
        video_path = _resolve_video_path(base_dir, video_id)
        if video_path is None:
            continue
        items.append(
            f"<div style='border:1px solid #d1d5db;border-radius:8px;padding:8px;background:#fff;'>"
            f"<video controls preload='metadata' style='width:100%;max-height:220px;border-radius:6px;'><source src='{video_path}'></video>"
            f"<div style='margin-top:6px;font-weight:600;'>{video_id}</div>"
            f"</div>"
        )

    if not items:
        return "<div style='color:#6b7280;'>No videos yet.</div>"

    return (
        "<div style='display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;'>"
        + "".join(items)
        + "</div>"
    )


def _render_sample_videos():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "videos")
    return _build_video_grid(fixed_video_ids(), base_dir)


def _render_session_videos(session_id):
    upload_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "video_rag_sessions", session_id)
    if not os.path.isdir(upload_dir):
        return "<div style='color:#6b7280;'>No videos yet.</div>"
    return _build_video_grid(session_video_ids(session_id), upload_dir)


def _on_upload(file, request: gr.Request):
    if file is not None:
        save_uploaded_video(file, request.session_hash)
    return _render_session_videos(request.session_hash)


def render_library_tab():
    gr.Markdown("### Video Library")

    gr.Markdown("**Pre-loaded sample videos**")
    gr.HTML(value=_render_sample_videos())

    gr.Markdown("**Your uploaded videos (this session only)**")
    session_videos = gr.HTML(value="<div style='color:#6b7280;'>No videos yet.</div>")

    uploader = gr.File(label="Add a video to your session", file_types=list(VIDEO_EXTENSIONS))
    uploader.upload(_on_upload, inputs=uploader, outputs=session_videos)
