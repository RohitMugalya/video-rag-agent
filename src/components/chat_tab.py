import gradio as gr
from langchain_core.callbacks import BaseCallbackHandler

from core.context import set_session_id, set_vlm_preference
from src.agent import build_agent


class TraceCollector(BaseCallbackHandler):
    def __init__(self):
        self.events = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.events.append({"tool": serialized.get("name", "unknown"), "input": input_str, "output": None})

    def on_tool_end(self, output, **kwargs):
        if self.events:
            self.events[-1]["output"] = str(output)

    def on_tool_error(self, error, **kwargs):
        if self.events:
            self.events[-1]["output"] = f"ERROR: {error}"


def _format_turn_trace(query, events):
    if not events:
        body = "_No tool calls this turn._"
    else:
        parts = []
        for e in events:
            parts.append(f"**{e['tool']}**\n\nInput: `{e['input']}`\n\nOutput: `{e['output']}`")
        body = "\n\n---\n\n".join(parts)
    return f"#### \"{query}\"\n\n{body}"


def render_chat_components():
    gr.Markdown("### Chat with the Video-RAG Agent")
    chatbot = gr.Chatbot(type="messages", height=500)
    msg = gr.Textbox(placeholder="Ask something about the videos in your library...", label="Your question")
    return chatbot, msg


def chat_respond(message, history, llm_provider, llm_model, vlm_provider, vlm_model, trace_text, request: gr.Request):
    set_session_id(request.session_hash)
    set_vlm_preference(vlm_provider, vlm_model)

    collector = TraceCollector()
    agent = build_agent(llm_provider, llm_model)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"callbacks": [collector]},
    )
    answer = result["messages"][-1].content

    history = (history or []) + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer},
    ]
    new_turn = _format_turn_trace(message, collector.events)
    updated_trace = f"{new_turn}\n\n===\n\n{trace_text}" if trace_text else new_turn

    return history, "", updated_trace
