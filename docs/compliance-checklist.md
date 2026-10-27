# Pre-publish compliance checklist

Every video records these in its `backlog.yaml` entry under `compliance:`. The validator refuses `scheduled` or `published` until every item is `true` or `n/a`, `fact_check` is `done`, `sources` is non-empty, and `ai_disclosure` is `required` or `not_required`. Re-verify the rules against YouTube's Help Center periodically; see `docs/research/2026-10-launch-risks.md`.

| Key | Check |
|---|---|
| `original_script` | Written for this video from several sources, not a reworded copy; `tools/lint_script.py` overlap check passes. |
| `no_health_claims` | No claim to treat, cure, or replace care for any condition; disclaimer is in the description. |
| `voice_licensed` | Voice provider plan includes commercial use; plan and date recorded in `licenses.voice`. |
| `voice_disclosure_decided` | Decided whether the synthetic-content toggle applies (convincingly human voice means yes). Result in `ai_disclosure`. |
| `music_licensed` | Music or bed source and license recorded in `licenses.music`. Our generated bed counts as own work. |
| `visuals_licensed` | Images own, public domain with a recorded source, or licensed. Recorded in `licenses.visuals`; period-accurate. |
| `not_made_for_kids` | Audience set to adults; setting confirmed in Studio. |
| `audio_levels_checked` | Loudness about -24 LUFS, no sudden peaks, fade-out at the end, spot-listened. |
| `metadata_honest` | Title and thumbnail match the content. No outcome promises. |
| `variation_check` | Topic, structure, opening, and visual differ meaningfully from the previous three uploads. |

Outside the `compliance:` block, also required: `fact_check: done` with a report in `channels/<slug>/factchecks/<id>.md`.
