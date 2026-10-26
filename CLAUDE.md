# CLAUDE.md

Workspace for building and running faceless YouTube channels. Goal: maximize watch time and ad/affiliate revenue, with the production pipeline automated over time. Each channel is an experiment; shared tooling and lessons live at the root.

## Layout

```
CLAUDE.md                 this file (root rules; channel folders add their own)
docs/
  research/               dated research notes, each with sources and confidence
  compliance-checklist.md pre-publish gate every video must pass
  automation-roadmap.md   staged plan from manual to automated
templates/
  channel/                scaffold copied by tools/new_channel.py
  video/                  brief + script templates
tools/
  new_channel.py          scaffold channels/<slug>/ from templates/channel
  validate.py             schema checks for channel.yaml and backlog.yaml (run before committing)
channels/<slug>/
  CLAUDE.md               channel-specific voice, rules, workflow
  channel.yaml            machine-readable config (single source of truth)
  strategy.md             positioning, audience, monetization plan
  backlog.yaml            video pipeline: idea -> scripted -> produced -> scheduled -> published
  calendar.md             publishing plan
  scripts/                one file per video, named by backlog id
  assets/                 small reference assets only (large media is gitignored)
```

## Branches

- `main`: shared tooling, templates, docs.
- `channel/<slug>`: work specific to one channel (scripts, backlog, experiments).
- This repo was bootstrapped on `claude/pensive-ptolemy-njefer`; treat that branch as the initial scaffold plus the first channel (`sleep-stories`).

## Working rules

1. **Machine-readable first.** Anything the automation will consume lives in YAML (`channel.yaml`, `backlog.yaml`). Markdown is for humans. Keep the two consistent; `tools/validate.py` checks the YAML.
2. **No fabricated data.** Revenue, RPM, and competition figures from blogs are estimates. Record the source and a confidence level in `docs/research/`. If you could not verify a claim, say so.
3. **Compliance gate.** No video moves to `scheduled` until every item in `docs/compliance-checklist.md` is recorded in its backlog entry (`compliance:` block).
4. **Original scripts only.** Do not reuse text across videos beyond a short fixed intro/outro. Templated, near-identical uploads risk YouTube's inauthentic-content enforcement, which sources say can apply at the channel level.
5. **Licenses are receipts.** For every voice and music asset, record provider, plan tier, and license reference in the backlog entry. Free tiers of TTS and AI-music tools generally exclude commercial use.
6. **No secrets in git.** OAuth client secrets, tokens, API keys, and `.env` files are gitignored. Never paste them into docs or commits.
7. **No health promises.** Sleep and meditation content must not claim to treat, cure, or replace care for insomnia, anxiety, or any condition. Use the standard disclaimer from `templates/video/script.md`.
8. **Don't pad.** Lengthen a video only if retention data supports it. Padding to reach mid-roll length has been reported to cut retention sharply.
9. **Uploads are manual until the API project is audited.** See `docs/automation-roadmap.md`.

## Commands

```
python3 tools/new_channel.py <slug> "<Display Name>"   # scaffold a channel
python3 tools/validate.py                               # validate all channels (needs pyyaml)
```

## Conventions

- Slugs: lowercase kebab-case. Video ids: `<NNN>` zero-padded, unique per channel (`001`, `002`).
- Backlog statuses: `idea`, `scripted`, `produced`, `scheduled`, `published`, `retired`.
- Dates: ISO 8601. Today's research baseline is October 2026; policy facts go stale, so re-verify against YouTube's own Help Center before relying on them.
- Commit messages: imperative, scoped by channel when relevant (`sleep-stories: add scripts 001-003`).

## Automation direction

The end state is a pipeline that reads `backlog.yaml`, drafts scripts, synthesizes narration, renders video, runs the compliance gate, uploads, and writes analytics back into the repo. Build each stage so it can run on one backlog entry and be reviewed by a human. Stage plan and open risks are in `docs/automation-roadmap.md`.
