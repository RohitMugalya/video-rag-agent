Searches static visual appearance across every video currently in the library, using a natural-language description of what something looks like.

**Arguments**
- `query` (string): a description of the visual appearance you're looking for — an object, person, scene, color, or on-screen element ("a red car", "a person in a blue shirt", "a storefront sign"). Describe appearance, not action; for movement, use `motion_search` instead.
- `top_k` (integer, default 5): maximum number of instance clusters to return.

**Returns**: a list of instance clusters sorted by relevance, each with `video_id`, `start_ts`, `end_ts`, `peak_timestamp`, and a match `score`. Each cluster is a distinct occurrence — the same thing appearing at two unrelated points in a video, or in different videos, comes back as separate clusters, not merged into one. If nothing relevant is found in any video, you'll get back a single-item list containing only a `note` field saying so — check for that before treating the result as a real match.

**Use when**: locating *where* an object, person, scene, or visual detail appears. This is usually your first hop for compositional queries: find the candidate instance(s) here, then use a frame-level tool (`zero_shot_classify`, `ocr_read`, `verify_visual_claim`, or `describe_visual_attribute`) with the returned `video_id` and `peak_timestamp` to resolve whatever the query asks about that instance.

**Don't use when**: the query is about motion or action (use `motion_search`) or about reading exact on-screen text once you already know the timestamp (use `ocr_read` directly instead of re-searching).

**Example call**: `visual_frame_search(query="a red car")`

**Note**: if the query implies more than one instance might matter ("every red car", "any banners"), treat every returned cluster as independent evidence and resolve each one relevant to the query — don't stop at the first result.
