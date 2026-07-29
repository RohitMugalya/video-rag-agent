from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from core.context import get_vlm_preference
from core.prompt_loader import load_prompt
from core.session import resolve_video_path
from core.video_io import frame_to_base64, get_frame
from core.vlm_chain import call_vlm


def _describe_visual_attribute(video_id: str, timestamp: float, question: str) -> dict:
    path = resolve_video_path(video_id)
    image = get_frame(path, timestamp)
    if image is None:
        return {
            "video_id": video_id,
            "timestamp": timestamp,
            "question": question,
            "response": "no frame available at this timestamp",
        }

    b64 = frame_to_base64(image)
    message = HumanMessage(
        content=[
            {"type": "text", "text": question + " Answer concisely based only on what is visible."},
            {"type": "image_url", "image_url": f"data:image/png;base64,{b64}"},
        ]
    )

    preferred_provider, preferred_model = get_vlm_preference()
    response, answered_by, attempts = call_vlm([message], preferred_provider, preferred_model)

    return {
        "video_id": video_id,
        "timestamp": timestamp,
        "question": question,
        "response": response.content,
        "answered_by": answered_by,
        "fallback_attempts": attempts,
    }


describe_visual_attribute = tool(_describe_visual_attribute, description=load_prompt("describe_visual_attribute.md"))
