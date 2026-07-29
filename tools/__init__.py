from tools.describe_visual_attribute import describe_visual_attribute
from tools.motion_search import motion_search
from tools.ocr_read import ocr_read
from tools.transcript_search import transcript_search
from tools.verify_visual_claim import verify_visual_claim
from tools.visual_frame_search import visual_frame_search
from tools.zero_shot_classify import zero_shot_classify

ALL_TOOLS = [
    visual_frame_search,
    ocr_read,
    motion_search,
    transcript_search,
    zero_shot_classify,
    verify_visual_claim,
    describe_visual_attribute,
]
