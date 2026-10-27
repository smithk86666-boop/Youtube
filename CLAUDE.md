# CLAUDE.md

Workspace for building and running a faceless YouTube sleep channel (and, later, others). Goal: get monetized, then maximize watch time and ad/affiliate revenue, with the production pipeline automated over time. Shared tooling and lessons live at the root; each channel is a folder.

## Layout

```
CLAUDE.md                 this file (root rules; channel folders add their own)
.claude/skills/           workflow skills (see Skills below)
docs/
  research/               dated research notes, each with sources and confidence
  experiments/            tests with arms, metrics, and fixed decision rules
  reviews/                weekly review notes
  compliance-checklist.md pre-publish gate every video must pass ("n/a" allowed with a reason)
  automation-roadmap.md   staged plan from manual to automated
  runbook-human-steps.md  the steps only the owner can do (accounts, payment, upload)
  art-sourcing.md         where images may come from and how to record them
templates/                channel and video scaffolds
tools/                    pipeline and validation scripts (see Commands)
channels/<slug>/
  CLAUDE.md               channel voice, rules, workflow
  channel.yaml            machine-readable config and series (single source of truth)
  strategy.md             positioning, audience, monetization plan
  backlog.yaml            video pipeline: idea -> scripted -> produced -> scheduled -> published
  calendar.md             publishing plan
  scripts/                one file per video, named by backlog id
  factchecks/             claim-by-claim reports, one per video
  assets/                 small reference assets (lexicon, channel text)
output/                   generated audio and video (gitignored)
```

Current channel: `channels/sleep` ("Quiet Hours", working name), series `quiet-history` (core), `still-weather` and `gentle-stories` (probes).

## Branches

- `main`: shared tooling, templates, docs.
- `channel/<slug>`: work specific to one channel, if more channels are added.
- This repo was bootstrapped on `claude/pensive-ptolemy-njefer`: scaffold, tools, skills, and the first channel.

## Working rules

1. **Machine-readable first.** Anything the automation consumes lives in YAML. Markdown is for humans. `tools/validate.py` checks the YAML.
2. **No fabricated data.** Figures from blogs are estimates. Record the source and a confidence level in `docs/research/`. If you could not verify a claim, say so. Never invent quotations, proverbs, or statistics in scripts.
3. **Compliance gate.** No video moves to `scheduled` until `docs/compliance-checklist.md` is recorded in its backlog entry, `fact_check` is `done`, sources are listed, and `ai_disclosure` is decided. Never set a check to `true` without verifying it.
4. **Original scripts only.** Write from several sources in our own words. Do not read aloud or lightly reword a source. Reuse nothing beyond the short fixed intro and outro (marked with `<!-- fixed:start -->`). YouTube's policy text allows recurring intros and outros and disallows templated, minimally varied, or mass-produced content.
5. **Accuracy is the edge.** The niche is flooded with inaccurate AI history videos. Every factual claim is fact-checked against sources; where evidence is thin the script says so.
6. **Licenses are receipts.** For every voice, music, and image asset record provider, plan or source, and date in the backlog entry. Free tiers of TTS and AI-music tools generally exclude commercial use.
7. **No secrets in git.** API keys, OAuth tokens, and `.env` files are gitignored. Never paste them into docs or commits.
8. **No health promises.** No claim to treat, cure, or replace care for insomnia, anxiety, or any condition. Use the standard disclaimer.
9. **Don't pad, don't delete.** Lengthen only if retention supports it. Never delete low performers (it removes watch time); unlist only for policy problems.
10. **Uploads are manual until the API project is audited** (unaudited projects force uploads private). See `docs/automation-roadmap.md`.
11. **Say what is untested.** `tools/tts.py run` has not been run against the live provider. Record such gaps in the relevant doc or commit message.

## Commands

```
python3 tools/validate.py                                   # validate all channels and the gate (needs pyyaml)
python3 tools/new_channel.py <slug> "<Display Name>"        # scaffold another channel
python3 tools/lint_script.py channels/sleep/scripts/001.md --target-min 60
python3 tools/tts.py plan|run|check|join sleep 001          # narration (run needs ELEVENLABS_API_KEY)
python3 tools/make_bed.py --kind rain|wind|waves --minutes 62 --seed 1 --out bed.m4a
python3 tools/make_thumbnail.py --text "..." --out thumb.jpg --still still.jpg [--art image.jpg]
python3 tools/render_video.py --narration n.wav --bed bed.m4a --image still.jpg --out video.mp4
python3 tools/package.py sleep 001 --duration-sec 3550      # title, description, chapters, sources
```

Requires ffmpeg, Python 3, pyyaml, Pillow.

## Skills (`.claude/skills/`)

- `niche-sampling`: sample real YouTube demand and competitors before choosing topics.
- `sleep-script-writer`: research and write an original calm script from a backlog entry.
- `fact-check-script`: verify every claim against sources and record a report.
- `produce-video`: narration, bed, art, render, and metadata with the tools.
- `compliance-gate`: run the checklist honestly and run the validator.
- `weekly-review`: record results, apply the experiment rules, plan next week.

Normal flow for a video: `sleep-script-writer` -> `fact-check-script` -> `produce-video` -> `compliance-gate` -> manual upload (`docs/runbook-human-steps.md`) -> `weekly-review`.

## Conventions

- Slugs: lowercase kebab-case. Video ids: `<NNN>` zero-padded, unique per channel.
- Backlog statuses: `idea`, `scripted`, `produced`, `scheduled`, `published`, `retired`.
- Dates ISO 8601. Research baseline is October 2026; policy facts go stale, so re-verify against YouTube's own Help Center before relying on them.
- Commit messages: imperative, scoped by channel when relevant (`sleep: add script 002`).

## Automation direction

End state: a pipeline that reads `backlog.yaml`, drafts scripts, fact-checks, synthesizes narration, renders video, runs the compliance gate, uploads, and writes analytics back to the repo. Each stage already runs on one backlog entry and can be reviewed by a human. Stage status and the blocking API-audit risk are in `docs/automation-roadmap.md`.
