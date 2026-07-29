from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from core.context import get_vlm_preference
from core.prompt_loader import load_prompt
from core.session import resolve_video_path
from core.video_io import frame_to_base64, get_frame
from core.vlm_chain import call_vlm


def _verify_visual_claim(video_id: str, timestamp: float, claim: str) -> dict:
    path = resolve_video_path(video_id)
    image = get_frame(path, timestamp)
    if image is None:
        return {
            "video_id": video_id,
            "timestamp": timestamp,
            "claim": claim,
            "response": "no frame available at this timestamp",
        }

    b64 = frame_to_base64(image)
    prompt = f"Look at this image carefully. Claim: '{claim}'. Is this claim true? Answer YES or NO first, then briefly explain why."
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"data:image/png;base64,{b64}"},
        ]
    )

    preferred_provider, preferred_model = get_vlm_preference()
    response, answered_by, attempts = call_vlm([message], preferred_provider, preferred_model)

    return {
        "video_id": video_id,
        "timestamp": timestamp,
        "claim": claim,
        "response": response.content,
        "answered_by": answered_by,
        "fallback_attempts": attempts,
    }


verify_visual_claim = tool(_verify_visual_claim, description=load_prompt("verify_visual_claim.md"))
