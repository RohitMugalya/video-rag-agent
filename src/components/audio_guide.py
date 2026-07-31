import os

import gradio as gr

AUDIO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "assets",
    "audios",
    "project_guide.mp3",
)


def render_audio_guide():
    with gr.Row(equal_height=True):
        with gr.Column(scale=2):
            gr.Markdown(
                "### New here? Press play\n"
                "Play this quick 1-minute walkthrough to get started instantly."
            )
        with gr.Column(scale=1):
            if os.path.exists(AUDIO_PATH):
                gr.Audio(value=AUDIO_PATH, label="Project guide", interactive=False, show_download_button=False)
            else:
                gr.Markdown("_Guide audio not added yet — drop a file at `assets/audios/project_guide.mp3`_")
