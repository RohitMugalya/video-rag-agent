Reads on-screen text at one specific instant in one specific video — signs, banners, captions, labels, subtitles baked into the frame, or any other legible text visible at that moment.

**Arguments**
- `video_id` (string): must come from a prior tool result in this conversation (e.g. a cluster returned by `visual_frame_search`) or from context already established with the user. Never invent or guess this value.
- `timestamp` (float): the single instant, in seconds, to read text from. Must come from a prior tool result or an instant the user explicitly gave you — never a guessed or rounded value.

**Returns**: a list of `{extracted_text, bbox}` entries for everything legible in that one frame. It can return more than one text region from a single timestamp (e.g. two separate labels visible at once), but it only ever looks at that one instant — it does not search across time on its own.

**Use when**: you already know which video and which moment to look at, and the query needs the literal text shown there — reading a sign, a banner, a caption, a price tag, a name badge, and similar.

**Don't use when**: you don't yet know where or when the text of interest appears — in that case, call `visual_frame_search` first (e.g. with a query like "a sign" or "a banner") to locate candidate timestamps, then call this tool at each one. Also don't use this for spoken content — that's `transcript_search`.

**Example call** (after a prior search already returned `video_id="clip_07"`, `peak_timestamp=22.4`): `ocr_read(video_id="clip_07", timestamp=22.4)`

**Important**: text of interest often appears at more than one point in a video (a sign shown early and again later, or two different signs at two different moments). If the query implies "any text" or "all signage" rather than one specific instant, don't call this tool once and assume that's everything — first locate every distinct timestamp cluster with `visual_frame_search`, then call this tool once per cluster's `peak_timestamp`, and report every instance found. Stopping after the first hit is a common mistake — don't make it.
