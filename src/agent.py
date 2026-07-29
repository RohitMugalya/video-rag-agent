from langchain.agents import create_agent

from core.prompt_loader import load_prompt
from core.providers import build_llm
from tools import ALL_TOOLS


def build_agent(llm_provider, llm_model):
    llm = build_llm(llm_provider, llm_model)
    system_prompt = load_prompt("system_prompt.md")
    return create_agent(model=llm, tools=ALL_TOOLS, system_prompt=system_prompt)
