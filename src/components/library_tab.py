import gradio as gr

from core.session import fixed_video_ids, save_uploaded_video, session_video_ids
from core.video_io import VIDEO_EXTENSIONS


def _format_ids(ids):
    return ", ".join(ids) if ids else "_None yet._"


def _on_upload(file, request: gr.Request):
    if file is not None:
        save_uploaded_video(file, request.session_hash)
    return _format_ids(session_video_ids(request.session_hash))


def render_library_tab():
    gr.Markdown("### Video Library")

    gr.Markdown("**Pre-loaded sample videos**")
    gr.Markdown(_format_ids(fixed_video_ids()))

    gr.Markdown("**Your uploaded videos (this session only)**")
    session_list = gr.Markdown("_None yet._")

    uploader = gr.File(label="Add a video to your session", file_types=list(VIDEO_EXTENSIONS))
    uploader.upload(_on_upload, inputs=uploader, outputs=session_list)
