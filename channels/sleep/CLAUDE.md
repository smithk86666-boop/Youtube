# Quiet Hours (sleep): channel rules

Inherits the root `CLAUDE.md`. One channel, several series. Working name only.

## Positioning
The accurate, human-edited alternative in a field crowded with inaccurate AI-made "boring history" videos. Same calm experience, but the facts are right, the sources are listed, and no two videos are templated copies. Evidence: `docs/research/2026-10-top-performers.md`.

## Series
| Series | Role | Format |
|---|---|---|
| `quiet-history` | core, launch first | Narrated calm history, 60-120 min, gentle bed under the voice |
| `still-weather` | probe (after 8 core videos) | One real place, one sound, 3+ hours, provenance proof |
| `gentle-stories` | probe (after 8 core videos) | Original calm fiction, no tension, no climax |

Each series gets its own playlist and its own results rows, so we can compare series inside one channel.

## Voice and tone (quiet-history)
- Warm, slow, low-stimulation. Second person is fine ("imagine the lane in the dark").
- Medium and long sentences. Avoid short punchy statements, exclamation marks, and rhetorical shocks.
- No climax, no cliffhanger, no mystery, no violence in detail, no politics.
- About 120-130 spoken words per minute. A 60-minute video is roughly 7,500 words; 90 minutes roughly 11,000.
- Honest about uncertainty: use "historians think", "sources suggest" where scholars disagree.

## Title formula
`<Specific, honest hook> | Calm History for Sleep`. Sentence case, under 70 characters where possible, no all-caps shouting, and no copying a competitor's prefix. The hook can promise an experience ("A Winter Night in a Medieval English Village"), never a medical outcome.

## Do
- Write every script fresh from several sources. A fixed intro and outro under 30 seconds each are the only shared text, and are wrapped in `<!-- fixed:start -->` / `<!-- fixed:end -->` markers.
- Run `python3 tools/lint_script.py channels/sleep/scripts/<id>.md` before voice generation.
- Fill `sources` in the backlog entry. List them in the description.
- Use `assets/lexicon.txt` for pronunciation and spot-listen to the narration every ~10 minutes of audio.
- Keep period-correct facts; where we do not know, say so.
- Fade in at the start and out at the end. Target about -24 LUFS.
- Keep a corrections log in the video's backlog entry if an error is reported.

## Don't
- Don't claim the video treats insomnia or any condition.
- Don't read aloud or lightly reword another source.
- Don't reuse structures video to video (same section order and same stock phrases throughout). Vary openings and how the night unfolds.
- Don't pad to reach a length. Don't mark videos as made for kids.
- Don't delete low performers. Unlist only if a video breaks policy.

## Tests (record in `docs/experiments/2026-q4-series-test.md`)
1. Length 60 / 90 / 120 minutes.
2. Mid-roll off vs automatic.
3. Title style, honest-hook vs question.
4. Series probes after video 8.

## Workflow
Use the skills in `.claude/skills/`: `sleep-script-writer`, `fact-check-script`, `compliance-gate`, `video-package`, `weekly-review`, `niche-sampling`. Pipeline commands are in the root `CLAUDE.md`.
