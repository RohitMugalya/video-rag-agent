Asks a vision-language model an open-ended question about a known frame, at a video and timestamp you already know, and returns a free-text answer.

**Arguments**
- `video_id` (string): must come from a prior tool result in this conversation or from context already established with the user. Never invent or guess this value.
- `timestamp` (float): a single instant, in seconds, to describe. Must come from a prior tool result or an instant the user explicitly gave you.
- `question` (string): an open-ended question about that frame with no fixed set of possible answers — e.g. "what is the person holding?", "describe the background", "what is written on their shirt?".

**Returns**: a dict with `video_id`, `timestamp`, `question`, `response` (the model's free-text answer), `answered_by` (which provider/model actually answered), and `fallback_attempts` (any providers tried before that one succeeded). If no frame exists at that timestamp, `response` will say so instead of a real answer — check for that before treating it as a confirmed description.

**Use when**: the question has no natural fixed label set to score against — descriptive, "what/how" style questions about a located instance.

**Don't use when**: the answer reduces to a short label set (color, category) — use `zero_shot_classify` first, since it's cheaper and more precise. Also don't use this to locate *where* something is in the first place — it only describes a frame you've already pinpointed with a search tool; use `visual_frame_search` or `motion_search` for locating.

**Example call**: `describe_visual_attribute(video_id="clip_09", timestamp=31.0, question="What is the person wearing?")`
