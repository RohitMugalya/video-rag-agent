import gradio as gr

from core.providers import LLM_PROVIDERS, VLM_PROVIDERS
from core.session import clear_session_uploads


def _update_llm_models(provider):
    models = LLM_PROVIDERS[provider]["models"]
    return gr.update(choices=models, value=models[0])


def _update_vlm_models(provider):
    models = VLM_PROVIDERS[provider]["models"]
    return gr.update(choices=models, value=models[0])


def _clear_uploads(request: gr.Request):
    clear_session_uploads(request.session_hash)
    return "Session uploads cleared."


def render_sidebar():
    gr.Markdown("### Configuration")

    gr.Markdown("**Agent LLM**")
    default_llm_provider = "Groq"
    llm_provider = gr.Dropdown(choices=list(LLM_PROVIDERS.keys()), value=default_llm_provider, label="Provider")
    llm_model = gr.Dropdown(
        choices=LLM_PROVIDERS[default_llm_provider]["models"],
        value=LLM_PROVIDERS[default_llm_provider]["models"][0],
        label="Model",
    )
    llm_provider.change(_update_llm_models, inputs=llm_provider, outputs=llm_model)

    gr.Markdown("**VLM (visual verification)**")
    default_vlm_provider = "Groq"
    vlm_provider = gr.Dropdown(choices=list(VLM_PROVIDERS.keys()), value=default_vlm_provider, label="Provider")
    vlm_model = gr.Dropdown(
        choices=VLM_PROVIDERS[default_vlm_provider]["models"],
        value=VLM_PROVIDERS[default_vlm_provider]["models"][0],
        label="Model",
    )
    vlm_provider.change(_update_vlm_models, inputs=vlm_provider, outputs=vlm_model)
    gr.Markdown(
        "_If this model fails mid-query, the agent automatically tries the next available "
        "VLM and logs the attempt in the Tool Trace tab._"
    )

    gr.Markdown("**Session**")
    clear_btn = gr.Button("Clear my uploaded videos")
    clear_status = gr.Markdown("")
    clear_btn.click(_clear_uploads, inputs=None, outputs=clear_status)

    return llm_provider, llm_model, vlm_provider, vlm_model
