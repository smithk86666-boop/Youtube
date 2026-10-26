# Pre-publish compliance checklist

Every video records these in its `backlog.yaml` entry under `compliance:`. A video cannot move to `scheduled` until all are `true` (or `n/a` with a note). Re-verify the rules against YouTube's Help Center periodically; see `docs/research/2026-10-launch-risks.md`.

| Key | Check |
|---|---|
| `original_script` | Script is written for this video, not a reworded copy of another video or source. |
| `no_health_claims` | No claim to treat, cure, or replace care for any condition. Disclaimer is in the description. |
| `voice_licensed` | Voice provider plan includes commercial use; plan and date recorded in `licenses.voice`. |
| `voice_disclosure_decided` | Decided whether the synthetic-content toggle applies (realistic, human-sounding voice means yes). Result in `ai_disclosure`. |
| `music_licensed` | Music source and license recorded in `licenses.music`; no unlicensed tracks. |
| `visuals_licensed` | Images and loops are own, generated with commercial rights, or licensed. Recorded in `licenses.visuals`. |
| `not_made_for_kids` | Audience set to adults; setting confirmed in Studio. |
| `audio_levels_checked` | Loudness consistent, no sudden peaks at the start or end, fade-out at the end. |
| `metadata_honest` | Title and thumbnail match the content. No misleading claims. |
| `variation_check` | Topic, structure, or visuals differ meaningfully from the previous three uploads. |
