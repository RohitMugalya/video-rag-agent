Scores one frame from a known video and timestamp against a list of candidate labels you supply, returning a similarity score for each label.

**Arguments**
- `video_id` (string): must come from a prior tool result in this conversation (e.g. a cluster returned by `visual_frame_search` or `motion_search`) or from context already established with the user. Never invent or guess this value.
- `timestamp` (float): a single instant, in seconds, to classify. Always exactly one float — never a list of timestamps. If you have several instances to check, call this tool once per instance rather than trying to cover them all in one call.
- `labels` (list of strings): the candidate labels to score, e.g. `["red", "blue", "green", "black", "white"]` for a color question, or `["male", "female"]` for a gender-presentation question. Keep the label set short, mutually exclusive where possible, and directly answerable from a single frame.
- `is_range_end` (float, optional): if the instance you're checking spans a time range rather than a single instant, pass the range's end here alongside `timestamp` as its start — the tool will score the midpoint. Omit it for a single-instant check.

**Returns**: a flat dict with `video_id` plus one key per label mapped to its score, e.g. `{"video_id": "clip_11", "red": 0.02, "white": 0.87, "black": 0.05}` — the labels themselves become top-level keys alongside `video_id`, not a nested list.

**Use when**: the query needs an attribute that reduces cleanly to a short label set (color, category, type) for an instance you've already located with another tool.

**Don't use when**: you don't yet know which instance you're asking about (locate it first with `visual_frame_search` or `motion_search`), or the question doesn't reduce to a short label list — for open-ended or compound questions, use `describe_visual_attribute` or `verify_visual_claim` instead.

**Example call**: `zero_shot_classify(video_id="clip_11", timestamp=14.6, labels=["white van", "red van", "blue van", "black van"])`
