import gradio as gr


LOCAL_MODELS_TABLE = """
| Tool | Model | Size | Accuracy | Notes |
|---|---|---|---|---|
| `transcript_search` | Whisper `base` (via faster-whisper) | 74M params | WER 5.0% / 12.4% (LibriSpeech test-clean / test-other) | Matching is literal keyword overlap against the transcript, not semantic search. |
| `visual_frame_search`, `zero_shot_classify` | SigLIP2 (`google/siglip2-base-patch16-224`) | ~375MB checkpoint (~92M-param vision tower + text tower) | Top-1 70.79% / Top-5 93.27% (ImageNet zero-shot) | One shared model powers both static-appearance search and label scoring. |
| `motion_search` | ViCLIP-L-14 (`OpenGVLab/ViCLIP-L-14-hf`) | 0.4B params | 75.7% top-1 (zero-shot action recognition, Kinetics-400) | Published research benchmark from the InternVid paper — not independently re-verified on this project's videos. |
| `ocr_read` | EasyOCR (CRAFT detector + English recognizer) | ~98MB (83MB detector + 15MB recognizer) | No single published figure | OCR accuracy swings heavily with text size, lighting, and camera angle — independent comparisons place EasyOCR as a solid lightweight option, generally a step behind larger VLM-based OCR on difficult real-world images. |
"""

AGENT_MODELS_TABLE = """
| Role | Model | Size | Benchmark | Notes |
|---|---|---|---|---|
| Agent orchestrator (plans and calls tools) | `openai/gpt-oss-120b` | 116.8B total params, 5.1B active per token (MoE) | MMLU 90%, GPQA Diamond 80.1% | Swappable from the sidebar; this is the default. |
| Vision-language model (`verify_visual_claim`, `describe_visual_attribute`) | `qwen/qwen3.6-27b` | 27B params (dense, multimodal) | ~84.5% MMLU (community-measured; no official first-party figure published) | Also swappable from the sidebar; this is the default. |
"""


def render_model_info_tab():
    gr.Markdown("### Model Information")
    gr.Markdown(
        "Every model this project relies on, mapped to the tool it powers. "
        "Accuracy figures are published results from each model's own paper, model card, "
        "or an independent community evaluation — none of these were re-measured against "
        "this project's own video library."
    )

    gr.Markdown("**Per-tool local models** (run directly on this Space)")
    gr.Markdown(LOCAL_MODELS_TABLE)

    gr.Markdown("**Agent & reasoning models** (called via API)")
    gr.Markdown(AGENT_MODELS_TABLE)

    gr.Markdown(
        "_Note: this project runs entirely on free-tier infrastructure — Hugging Face "
        "ZeroGPU for the local models above, and free-tier inference APIs for the agent "
        "and vision-language models. Speed, availability, and rate limits are all subject "
        "to those free-tier constraints rather than the models' own ceiling._"
    )
