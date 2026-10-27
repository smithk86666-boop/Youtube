---
name: compliance-gate
description: Run the pre-publish compliance checklist for a sleep-channel video and record honest results in backlog.yaml. Use before moving any video to scheduled or published.
---

# Compliance gate

Source of truth: `docs/compliance-checklist.md`. The validator (`python3 tools/validate.py`) refuses `scheduled` or `published` until every item is `true` or `n/a`, `fact_check` is `done`, sources are listed, and `ai_disclosure` is decided.

## Steps
For video `<id>`, check each item with evidence, not assumption, and write the `compliance:` block in `channels/sleep/backlog.yaml`.

| Key | How to verify |
|---|---|
| `original_script` | `lint_script.py` passes the overlap check; script was written from several sources; no pasted passages |
| `no_health_claims` | `lint_script.py` has no health ERRORs; title, description, and thumbnail make no treatment promise; disclaimer is in the description |
| `voice_licensed` | `licenses.voice` names provider, plan, and date; plan allows commercial use |
| `voice_disclosure_decided` | `ai_disclosure` set to `required` if the voice is convincingly human, otherwise `not_required`; write a one-line reason |
| `music_licensed` | `licenses.music` filled: our generated bed (own work) or a recorded license |
| `visuals_licensed` | `licenses.visuals` filled: own art, public domain with source, or licensed; image is period-accurate for the topic |
| `not_made_for_kids` | Studio setting confirmed (record in the video notes) |
| `audio_levels_checked` | Render reports about -24 LUFS; spot-listen at start, middle, end; no peaks at the fade |
| `metadata_honest` | Title and thumbnail match the content; no outcome promises |
| `variation_check` | Compare with the last three videos: topic, structure, opening, visual all differ |

## Rules
- Never set an item `true` to pass the validator. If something cannot be verified from here (for example the Studio kids setting), leave it `false` and list it as a human step.
- Set `n/a` only with a reason in a comment.
- Finish by running `python3 tools/validate.py` and reporting the result verbatim.
