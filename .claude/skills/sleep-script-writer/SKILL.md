---
name: sleep-script-writer
description: Write an original, accurate, calm narration script for a Quiet Hours sleep video from a backlog entry. Use when asked to script, draft, or write a video in channels/sleep (quiet-history or gentle-stories series).
---

# Write a sleep script

Goal: a script a narrator can read slowly for the target length that is original, factually careful, and never tense. Read `channels/sleep/CLAUDE.md` first; its rules win.

## Inputs
- A backlog entry in `channels/sleep/backlog.yaml` (id, title, topic, target length, series).
- `channels/sleep/scripts/001.md` as the style and structure reference. Do not copy its section order or phrasing.

## Steps
1. **Research.** Use WebSearch and WebFetch to gather at least 4 independent sources (books, museum or heritage sites, academic summaries). Prefer scholarly or institutional pages over blogs. Write the sources into the backlog entry's `sources:` list. Never paste text from a source; take facts and restate them in your own words.
2. **Plan variation.** Check the last three scripts' section lists. Choose a different shape for this video: a different way to open (not always dusk), a different arc (a journey, a single day, a season, a building walked through room by room), and different section count. The goal is that two videos are not interchangeable.
3. **Outline.** 8-10 `## ` sections, each 700-1,100 words, plus the fixed intro and outro. Compute the target: minutes x 125 words.
4. **Write** to `channels/sleep/scripts/<id>.md` using this layout: title heading, a short metadata list, `<!-- narration:start -->`, the fixed intro wrapped in `<!-- fixed:start -->` / `<!-- fixed:end -->`, sections, the fixed outro, `<!-- narration:end -->`, then the description boilerplate and a numbered fact-check list of every factual claim.
5. **Style.** Second person, slow, medium and long sentences, concrete sensory detail, gentle transitions, no exclamation marks, no cliffhangers, no violence in detail, no politics, no modern jokes. Say "historians think" or "we do not know" where evidence is thin; never invent quotations, proverbs, or statistics. Atmosphere (weather, sounds) is fine but keep it out of the historical claims list or label it as atmosphere.
6. **Lint.** Run `python3 tools/lint_script.py channels/sleep/scripts/<id>.md --target-min <N>`. Fix every ERROR. Fix WARNs unless there is a reason. Check text overlap with earlier scripts.
7. **Update the backlog:** `status: scripted`, `script: scripts/<id>.md`, `sources`, `fact_check: pending`.
8. Hand off to `fact-check-script`.

## Quality bar
- Every concrete claim could be defended with a source.
- No sentence that sounds like a documentary hook ("You won't believe...").
- Reads aloud smoothly; names and unusual words are added to `channels/sleep/assets/lexicon.txt`.
- Length within 10% of target.
