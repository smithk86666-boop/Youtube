# Automation roadmap

Principle: automate one stage at a time, each runnable on a single backlog entry, with a human review point until the stage has proven reliable. Do not automate upload until the compliance gate is automated and trusted.

| Stage | Description | Status | Notes |
|---|---|---|---|
| 0 | Manual end to end for the first 5-10 videos | planned | Learn what works before encoding it. |
| 1 | Idea and backlog generation | planned | Output: entries in `backlog.yaml`. Dedup against existing titles. |
| 2 | Script drafting from a brief | planned | Claude drafts to `scripts/<id>.md`; human edits. Must follow channel voice rules. |
| 3 | Narration synthesis | planned | Paid TTS with commercial license. Record license in backlog entry. |
| 4 | Video render | planned | Voice + quiet music bed + looping visual via ffmpeg. Loudness normalization. |
| 5 | Compliance gate | planned | Script-level checks (health-claim phrases, similarity to prior scripts), license fields present. |
| 6 | Upload | blocked | See API risk below. Manual via Studio until resolved. |
| 7 | Analytics feedback | planned | Pull retention, RPM, CTR into `channels/<slug>/analytics/`; feed back into topic choice. |

## API risk (blocker for stage 6)

- Unaudited API projects have uploads forced to private. The audit takes weeks, requires a compliant use case, and is separate from quota.
- Action: when the first channel has a handful of videos and a working manual process, apply for the API compliance audit. In parallel, keep uploading manually.
- Alternative: an upload tool that has already passed the audit, at the cost of fees and a third-party dependency.

## Design constraints for the pipeline

- Idempotent per backlog id: rerunning a stage overwrites that id's outputs only.
- Never publish automatically in the early phase; the last step stays "schedule", a human confirms.
- Rate-limit and add variation: bursts of near-identical uploads are the pattern most associated with enforcement.
- Credentials via environment variables or a gitignored `secrets/` directory.
- Log every automated decision (model, prompt version, provider plan) into the backlog entry.
