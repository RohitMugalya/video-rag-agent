import gradio as gr

from core.session import (
    fixed_video_ids,
    resolve_video_path,
    save_uploaded_video,
    session_video_ids,
)
from core.video_io import VIDEO_EXTENSIONS


def _gallery_items(video_ids, session_id=None):
    items = []
    for video_id in video_ids:
        try:
            path = resolve_video_path(video_id, session_id)
            items.append((path, video_id))
        except FileNotFoundError:
            continue
    return items


def render_library_tab():
    gr.Markdown("### Video Library", elem_classes=["library-heading"])

    with gr.Column(elem_classes=["library-panel"]):
        gr.Markdown("**Pre-loaded sample videos**", elem_classes=["library-section-title"])
        sample_gallery = gr.Gallery(
            value=_gallery_items(fixed_video_ids()),
            columns=3,
            object_fit="cover",
            height=360,
            show_label=True,
            elem_classes=["library-gallery"],
        )

        gr.Markdown("**Your uploaded videos (this session only)**", elem_classes=["library-section-title"])
        session_gallery = gr.Gallery(
            value=[],
            columns=3,
            object_fit="cover",
            height=360,
            show_label=True,
            elem_classes=["library-gallery"],
        )

        upload_status = gr.Markdown(
            "Upload one or more videos to build your session library.",
            elem_classes=["library-helper"],
        )
        uploader = gr.Files(
            label="Upload more videos",
            file_types=list(VIDEO_EXTENSIONS),
            file_count="multiple",
            elem_classes=["library-upload"],
        )

        def _on_upload(files, request: gr.Request):
            if files:
                for file_path in files:
                    save_uploaded_video(file_path, request.session_hash)
                message = f"Added {len(files)} video(s) to your session."
            else:
                message = "No new videos were uploaded."
            updated_items = _gallery_items(session_video_ids(request.session_hash), request.session_hash)
            return updated_items, message

        uploader.upload(_on_upload, inputs=uploader, outputs=[session_gallery, upload_status])

    return sample_gallery, session_gallery
