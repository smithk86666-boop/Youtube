# Automation roadmap

Principle: automate one stage at a time, each runnable on a single backlog entry, with a human review point until the stage has proven reliable. Do not automate upload until the compliance gate is trusted.

| Stage | Description | Status | Notes |
|---|---|---|---|
| 0 | Manual end to end for the first 5-10 videos | next | Learn what works before encoding more |
| 1 | Idea and backlog generation | skill ready | `niche-sampling` plus `sleep-script-writer`; dedup against existing titles |
| 2 | Script drafting | skill ready, 1 script written | `sleep-script-writer`; `tools/lint_script.py` blocks near-duplicates and health claims |
| 3 | Fact-check | skill ready, 1 report done | `fact-check-script`; AI search pass, human spot-check recommended |
| 4 | Narration synthesis | tool written, **live call untested** | `tools/tts.py` plan/check/join tested; `run` needs a paid key and a first small test |
| 5 | Bed and video render | tools tested locally | `make_bed.py`, `render_video.py`; checked output near -24 LUFS; not auditioned by ear |
| 6 | Thumbnail and metadata | tools tested locally | `make_thumbnail.py`, `package.py`; chapter times are estimates until checked against audio |
| 7 | Compliance gate | skill ready, validator enforces | `tools/validate.py` blocks scheduling until every item is recorded |
| 8 | Upload | **blocked** | See API risk below. Manual in Studio |
| 9 | Analytics feedback | planned | Manual paste into `weekly-review` now; API later |

## API risk (blocker for stage 8)

- API projects created after July 2020 that have not passed Google's compliance audit have `videos.insert` uploads forced to private, regardless of the requested privacy status. The audit takes weeks and is separate from quota. Quota cost of `videos.insert` is reported inconsistently across sources; check the quota table and your project's quota page.
- Plan: file the audit request once the manual process is stable (about video 10) and the use case is clear (one owner uploading their own channel). Keep uploading manually meanwhile.
- Alternative: an upload tool that has already passed the audit.

## Design constraints for the pipeline

- Idempotent per backlog id; reruns overwrite only that id's outputs.
- Never publish automatically early on; the last step stays "schedule", a human confirms.
- Rate-limit and vary output; bursts of near-identical uploads are the pattern most associated with enforcement.
- Credentials via environment variables, never in git.
- Log every automated decision (model, prompt version, provider plan) in the backlog entry.
