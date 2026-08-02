import gradio as gr


LOCAL_MODELS = [
    {
        "tool": "transcript_search",
        "model": "Whisper base (faster-whisper)",
        "size": "74M params",
        "accuracy": "WER 5.0% / 12.4% (LibriSpeech)",
        "notes": "Matching is literal keyword overlap against the transcript, not semantic search.",
    },
    {
        "tool": "visual_frame_search, zero_shot_classify",
        "model": "SigLIP2 (google/siglip2-base-patch16-224)",
        "size": "~375MB checkpoint",
        "accuracy": "Top-1 70.79% / Top-5 93.27% (ImageNet zero-shot)",
        "notes": "One shared model powers both static-appearance search and label scoring.",
    },
    {
        "tool": "motion_search",
        "model": "ViCLIP-L-14 (OpenGVLab/ViCLIP-L-14-hf)",
        "size": "0.4B params",
        "accuracy": "75.7% top-1 (zero-shot action recognition, Kinetics-400)",
        "notes": "Published benchmark from the InternVid paper; not independently re-verified on this project’s videos.",
    },
    {
        "tool": "ocr_read",
        "model": "EasyOCR (CRAFT + English recognizer)",
        "size": "~98MB total",
        "accuracy": "No single published figure",
        "notes": "Accuracy depends heavily on text size, lighting, and camera angle.",
    },
]

AGENT_MODELS = [
    {
        "role": "Agent orchestrator",
        "model": "openai/gpt-oss-120b",
        "size": "116.8B total params",
        "benchmark": "MMLU 90%, GPQA Diamond 80.1%",
        "notes": "Swappable from the sidebar; this is the default.",
    },
    {
        "role": "Vision-language model",
        "model": "qwen/qwen3.6-27b",
        "size": "27B params",
        "benchmark": "~84.5% MMLU (community-measured)",
        "notes": "Used for verify_visual_claim and describe_visual_attribute; also swappable from the sidebar.",
    },
]


def _render_model_cards(models, title):
    with gr.Column():
        gr.Markdown(f"**{title}**")
        for model in models:
            with gr.Group():
                gr.Markdown(f"### {model['tool'] if 'tool' in model else model['role']}")
                gr.Markdown(
                    f"**Model:** {model['model']}  \n"
                    f"**Size:** {model['size']}  \n"
                    f"**Accuracy / Benchmark:** {model['accuracy'] if 'accuracy' in model else model['benchmark']}  \n"
                    f"**Notes:** {model['notes']}"
                )


def render_model_info_tab():
    gr.Markdown("### Model Information")
    gr.Markdown(
        "Every model this project relies on, mapped to the tool it powers. "
        "Accuracy figures are published results from each model's own paper, model card, "
        "or an independent community evaluation — none of these were re-measured against "
        "this project's own video library."
    )

    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            _render_model_cards(LOCAL_MODELS, "Per-tool local models (run directly on this Space)")
        with gr.Column(scale=1):
            _render_model_cards(AGENT_MODELS, "Agent & reasoning models (called via API)")

    gr.Markdown(
        "_Note: this project runs entirely on free-tier infrastructure — Hugging Face "
        "ZeroGPU for the local models above, and free-tier inference APIs for the agent "
        "and vision-language models. Speed, availability, and rate limits are all subject "
        "to those free-tier constraints rather than the models' own ceiling._"
    )
