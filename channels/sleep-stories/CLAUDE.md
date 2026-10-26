# Quiet Hours (sleep-stories): channel rules

Inherits the root `CLAUDE.md`. Working name only; confirm handle availability before branding.

## Voice and tone
- Slow, warm, low-stimulation. Second person is fine ("imagine the harbor at dawn"); avoid drama, cliffhangers, and surprises.
- Sentences short to medium. Concrete, sensory detail. Gentle repetition is good.
- Topics are calm and factual: history, geography, nature, everyday science, old trades. Nothing frightening, violent, or politically charged.
- Pacing: roughly 110-130 spoken words per minute, so a 150-minute video needs about 16,500-19,500 words, usually delivered across several linked "chapters."

## Do
- Write a fresh script for every video. A fixed intro of under 30 seconds is the only shared text.
- Fade audio out at the end and never end on a loud sound.
- Keep the first 60 seconds low-friction: no long channel promotion, no loud music sting.
- Put the disclaimer from `templates/video/script.md` in every description.
- Record the voice, music, and visual license for every video in `backlog.yaml`.

## Don't
- Don't claim the video treats insomnia, anxiety, or any condition.
- Don't bulk-generate scripts and publish them unreviewed.
- Don't pad length to reach mid-roll eligibility. Test lengths on purpose instead.
- Don't use a cloned or celebrity-like voice.
- Don't mark videos as made for kids.

## Open tests (record results in `docs/research/` when done)
1. Length: 60 vs 150 vs 480 minutes, compare average view duration percent and RPM.
2. Mid-roll: off vs automatic.
3. Thumbnail style: dark minimal vs illustrated.
4. Title pattern: "boring" framing vs "for sleep" framing, check which gets clicked.

## Workflow
1. Pick the top `idea` from `backlog.yaml`.
2. Write `scripts/<id>.md` from `templates/video/script.md`; status `scripted`.
3. Generate narration, add a quiet bed, render with a looping visual; status `produced`.
4. Fill `licenses:` and `compliance:`; run `python3 tools/validate.py`.
5. Upload through Studio (API uploads are locked until audit); status `scheduled`, then `published`.
6. After 7 days, record `results:` in the backlog entry.
