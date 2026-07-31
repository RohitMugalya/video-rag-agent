import gradio as gr

from core.session import (
    fixed_video_ids,
    get_session_upload_dir,
    resolve_video_path,
    save_uploaded_video,
    session_video_ids,
)
from core.video_io import VIDEO_EXTENSIONS


def _gallery_paths(video_ids, session_id=None):
    paths = []
    for video_id in video_ids:
        try:
            paths.append(resolve_video_path(video_id, session_id))
        except FileNotFoundError:
            continue
    return paths


def render_library_tab():
    gr.Markdown("### Video Library")

    gr.Markdown("**Pre-loaded sample videos**")
    sample_gallery = gr.Gallery(
        value=_gallery_paths(fixed_video_ids()),
        columns=2,
        object_fit="cover",
        height=320,
    )

    gr.Markdown("**Your uploaded videos (this session only)**")
    session_gallery = gr.Gallery(
        columns=2,
        object_fit="cover",
        height=320,
    )

    uploader = gr.File(label="Add a video to your session", file_types=list(VIDEO_EXTENSIONS))

    def _on_upload(file, request: gr.Request):
        if file is not None:
            save_uploaded_video(file, request.session_hash)
        return _gallery_paths(session_video_ids(request.session_hash), request.session_hash)

    uploader.upload(_on_upload, inputs=uploader, outputs=session_gallery)

    return sample_gallery, session_gallery
