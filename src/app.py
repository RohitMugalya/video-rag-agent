import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

import gradio as gr

from core.models import warm_up_models
from src.components.audio_guide import render_audio_guide
from src.components.chat_tab import chat_respond, render_chat_components, retry_response
from src.components.library_tab import render_library_tab
from src.components.sidebar import render_sidebar
from src.components.trace_tab import render_trace_tab_components

print("Warming up models before serving traffic...")
warm_up_models()
print("All models ready.")

with gr.Blocks(title="Video-RAG Agent") as demo:
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
