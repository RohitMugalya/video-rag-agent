Searches spoken dialogue across every video currently in the library, matching your query against what was actually said in each video's transcribed audio.

**Arguments**
- `query` (string): the word or phrase you're listening for. Matching is based on literal word overlap with the transcript, not semantic meaning — so prefer specific words likely to have actually been spoken ("budget", "password", "deadline") over a vague paraphrase of the topic. If a first attempt returns nothing, try a more literal or differently-worded query before concluding it wasn't said.
- `top_k` (integer, default 5): maximum number of matches to return.

**Returns**: a list of matches ranked by relevance, each with `video_id`, `start_ts`, `end_ts`, `transcript_text` (the actual transcribed segment), and a match `score`. If nothing relevant is found in any video, you'll get back a single-item list containing only a `note` field saying so — check for that before treating the result as a real match.

**Use when**: the query is about something someone said out loud — quotes, spoken numbers, names, topics discussed, questions asked in dialogue.

**Don't use when**: the information is shown as on-screen text rather than spoken (use `ocr_read` after locating the frame instead) or is about what's visually happening rather than what was said.

**Example call**: `transcript_search(query="wifi password")`
