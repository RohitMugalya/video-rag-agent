import os

from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_openai import ChatOpenAI

LLM_PROVIDERS = {
    "Groq": {
        "models": ["openai/gpt-oss-120b", "qwen/qwen3.6-27b"],
        "build": lambda model: ChatGroq(model=model, temperature=0),
    },
    "NVIDIA": {
        "models": ["nvidia/llama-3.3-nemotron-super-49b-v1.5"],
        "build": lambda model: ChatNVIDIA(model=model, temperature=0),
    },
    "OpenRouter": {
        "models": ["qwen/qwen3-coder:free"],
        "build": lambda model: ChatOpenAI(
            model=model,
            temperature=0,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        ),
    },
}

VLM_PROVIDERS = {
    "Groq": {
        "models": ["qwen/qwen3.6-27b"],
        "build": lambda model: ChatGroq(model=model, temperature=0),
    },
    "NVIDIA": {
        "models": ["nvidia/cosmos3-nano-reasoner", "google/paligemma"],
        "build": lambda model: ChatNVIDIA(model=model, temperature=0),
    },
    "OpenRouter": {
        "models": ["google/gemma-4-31b-it:free", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"],
        "build": lambda model: ChatOpenAI(
            model=model,
            temperature=0,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        ),
    },
}


def build_llm(provider, model):
    return LLM_PROVIDERS[provider]["build"](model)


def build_vlm(provider, model):
    return VLM_PROVIDERS[provider]["build"](model)


def vlm_fallback_order(preferred_provider, preferred_model):
    ordered = [(preferred_provider, preferred_model)]
    for provider, config in VLM_PROVIDERS.items():
        for model in config["models"]:
            if (provider, model) != (preferred_provider, preferred_model):
                ordered.append((provider, model))
    return ordered
