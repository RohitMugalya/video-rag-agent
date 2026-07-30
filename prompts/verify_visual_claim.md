Asks a vision-language model to confirm or deny one specific, stated claim about a known frame, at a video and timestamp you already know.

**Arguments**
- `video_id` (string): must come from a prior tool result in this conversation or from context already established with the user. Never invent or guess this value.
- `timestamp` (float): a single instant, in seconds, to check the claim against. Must come from a prior tool result or an instant the user explicitly gave you.
- `claim` (string): a specific, checkable statement about that frame, phrased so a yes/no answer makes sense — e.g. "the shelf is fully stocked", "two people are shaking hands", "the door is open". Phrase it as a claim to verify, not a question.

**Returns**: a dict with `video_id`, `timestamp`, `claim`, `response` (the model's yes/no judgment plus a brief explanation, as free text), `answered_by` (which provider/model actually answered), and `fallback_attempts` (any providers tried before that one succeeded). If no frame exists at that timestamp, `response` will say so instead of a real judgment — check for that before treating it as a confirmed answer.

**Use when**: verifying a specific claim you already suspect is true or false — especially open-ended or compound claims that don't reduce cleanly to a short label list, or as a stronger confirmation step after a low-confidence `zero_shot_classify` result.

**Use `zero_shot_classify` instead when**: the question naturally reduces to choosing among a small set of labels (a color, a category) — that tool is cheaper and more precise for that shape of question. Reserve this tool for genuine claim verification, not as a way to "guess" an answer by testing several candidate claims one at a time — if you're discovering an open-ended attribute rather than confirming a specific claim, use `describe_visual_attribute` instead.

**Example call**: `verify_visual_claim(video_id="clip_02", timestamp=5.1, claim="the sign says the shop is open")`
