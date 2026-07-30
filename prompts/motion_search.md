Searches motion and actions over time across every video currently in the library, using a natural-language description of what is happening rather than what something looks like at rest.

**Arguments**
- `query` (string): a description of the action or movement itself — e.g. "a person running", "a car turning left", "someone opening a door". Describe the motion, not just the object.
- `top_k` (integer, default 5): maximum number of instance clusters to return.

**Returns**: a ranked list of instance clusters, each with `video_id`, `start_ts`, `end_ts`, `action_label`, and a match `score`. Each cluster is a distinct occurrence of that action — the same action happening at two unrelated points in a video (or in different videos) comes back as separate clusters, not merged into one.

**Use when**: the query is about what someone or something is *doing* over a span of time — running, falling, opening, throwing, turning, walking away, and similar. This is typically a first-hop locator tool: use it to find *where* an action happens, then, if the query also asks about an attribute of that moment (who's doing it, what they're wearing, what color the object is), follow up with a frame-level tool (`zero_shot_classify`, `verify_visual_claim`, or `describe_visual_attribute`) at the returned `action_label`'s peak or midpoint timestamp.

**Don't use when**: the query is about static visual appearance rather than movement (use `visual_frame_search` instead — "a red car" is appearance, "a car turning" is motion). Also don't use this for reading on-screen text or spoken content; those belong to `ocr_read` and `transcript_search` respectively.

**Example call**: `motion_search(query="a person running", top_k=5)`

**Note**: if the query implies more than one occurrence of the same action might matter ("every time someone opens the door"), treat every returned cluster as a distinct instance and address all of them relevant to the query — don't stop at the first result.
