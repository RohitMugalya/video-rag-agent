import gradio as gr


def render_trace_tab_components():
    gr.Markdown("### Tool Call Trace")
    gr.Markdown(
        "Shows the tool calls the agent made for each of your messages (newest turn on top), "
        "including tool input/output and any VLM fallback attempts if a provider failed mid-call."
    )
    trace_output = gr.Markdown("_No tool calls yet this session._")
    return trace_output
