---
name: produce-video
description: Turn a fact-checked script into upload-ready files (narration, bed, thumbnail, rendered MP4, metadata) with the repo tools. Use when a backlog entry is scripted and fact_check is done.
---

# Produce a video

Run from the repo root. Outputs go to `output/sleep/<id>/` (gitignored).

## Preconditions
- `status: scripted`, `fact_check: done`, `python3 tools/lint_script.py ...` passes.
- Voice plan with commercial rights, and `ELEVENLABS_API_KEY` set in the environment (never commit it). `voice.voice_id` set in `channels/sleep/channel.yaml`. If these are missing, stop and report; only the owner can supply them.

## Steps
1. Plan: `python3 tools/tts.py plan sleep <id>` (no cost). Check chunk count and length.
2. Voice test: `python3 tools/tts.py run sleep <id> --limit 1`, then listen and check pronunciation. Add fixes to `channels/sleep/assets/lexicon.txt`.
3. Full synthesis: `python3 tools/tts.py run sleep <id>` (resumable).
4. Glitch check: `python3 tools/tts.py check sleep <id>`. Re-generate flagged chunks (delete the file and re-run). Listen to each flagged chunk.
5. Join: `python3 tools/tts.py join sleep <id>`.
6. Bed: `python3 tools/make_bed.py --kind rain|wind --minutes <narration minutes + 2> --seed <id as int> --out output/sleep/<id>/bed.m4a`. Use a different seed and kind from the previous three videos.
7. Art: source a period-accurate image that we are allowed to use (own, public domain with source recorded, or licensed). Then `python3 tools/make_thumbnail.py --text "<short hook>" --art <image> --seed <n> --out output/sleep/<id>/thumb.jpg --still output/sleep/<id>/still.jpg`. Without art the tool draws a generic night sky; acceptable for a pilot, weaker for accuracy.
8. Render: `python3 tools/render_video.py --narration output/sleep/<id>/narration.wav --bed output/sleep/<id>/bed.m4a --image output/sleep/<id>/still.jpg --out output/sleep/<id>/video.mp4`. Confirm about -24 LUFS.
9. Metadata: `python3 tools/package.py sleep <id> --duration-sec <real narration seconds>`. Check chapter times against the audio.
10. Update the backlog: `status: produced`, record `licenses`, then run `compliance-gate`.

## Notes
- `tts.py run` is untested against the live service; keep the first run small.
- Upload is manual in Studio until the API project is audited (see `docs/automation-roadmap.md`).
- The generated bed is a quiet layer under the voice. Do not publish bed-only videos made from it.
