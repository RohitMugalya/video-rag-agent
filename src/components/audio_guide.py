import os

import gradio as gr

AUDIO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "assets",
    "audios",
    "project_guide.mp3",
)


def render_audio_guide():
    gr.Markdown(
        "### New here? Press play\n"
        "A short walkthrough of this project and how to use the interface, in my own voice."
    )
    if os.path.exists(AUDIO_PATH):
        gr.Audio(value=AUDIO_PATH, label="Project guide", interactive=False)
    else:
        gr.Markdown("_Guide audio not added yet — drop a file at `assets/audios/project_guide.mp3`_")
