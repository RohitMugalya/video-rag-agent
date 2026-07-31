import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

import gradio as gr

from core.assets_fetch import fetch_demo_assets
from core.models import warm_up_models
from src.components.audio_guide import render_audio_guide
from src.components.chat_tab import chat_respond, render_chat_components, retry_response
from src.components.library_tab import render_library_tab
from src.components.sidebar import render_sidebar
from src.components.trace_tab import render_trace_tab_components

print("Fetching demo assets before serving traffic...")
fetch_demo_assets()
print("Warming up models before serving traffic...")
warm_up_models()
print("All models ready.")

with gr.Blocks(
    title="Video-RAG Agent",
    css="""
    body { background: linear-gradient(135deg, #07111f 0%, #111c2f 100%); }
    .gradio-container { max-width: 1600px !important; }
    .library-panel {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .library-heading {
        margin-bottom: 8px;
    }
    .library-section-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .library-gallery {
        border-radius: 16px;
        overflow: hidden;
    }
    .library-gallery .gallery-item {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.12);
    }
    .library-upload {
        border: 1px dashed rgba(255,255,255,0.24);
        border-radius: 14px;
        padding: 8px;
        background: rgba(255,255,255,0.04);
    }
    .library-helper {
        color: #c7d2fe;
        font-size: 0.95rem;
        margin-top: 6px;
    }
    .audio-guide-wrapper .gradio-audio {
        max-width: 100%;
        overflow: hidden;
    }
    .audio-guide-wrapper .gradio-audio .wrap {
        overflow: hidden !important;
    }
    """,
) as demo:
    gr.Markdown("# Video-RAG Agent")
    render_audio_guide()

    with gr.Row():
        with gr.Column(scale=1):
            llm_provider, llm_model, vlm_provider, vlm_model = render_sidebar()

        with gr.Column(scale=3):
            with gr.Tabs():
                with gr.Tab("Chat"):
                    chatbot, msg, retry_button, retry_state = render_chat_components()
                with gr.Tab("Tool Trace"):
                    trace_output = render_trace_tab_components()
                with gr.Tab("Video Library"):
                    render_library_tab()

    msg.submit(
        chat_respond,
        inputs=[msg, chatbot, llm_provider, llm_model, vlm_provider, vlm_model, trace_output],
        outputs=[chatbot, msg, trace_output, retry_state, retry_button],
    )

    retry_button.click(
        retry_response,
        inputs=[chatbot, retry_state, llm_provider, llm_model, vlm_provider, vlm_model, trace_output],
        outputs=[chatbot, msg, trace_output, retry_state, retry_button],
    )

if __name__ == "__main__":
    demo.launch()
