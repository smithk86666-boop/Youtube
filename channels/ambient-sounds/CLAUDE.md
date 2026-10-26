# Still Weather (ambient-sounds): channel rules

Inherits the root `CLAUDE.md`. Working name only. This channel is the cheap-to-produce arm of the format experiment in `docs/experiments/2026-q4-format-test.md`.

## The main risk
Ambient and loop channels are reported to have some of the highest rejection rates for repetitive/inauthentic content. A rain video and a rain-plus-fireplace video from the same source look like one template. Sources are third-party marketing blogs, so confidence is medium, but the mitigation is cheap, so we follow it from day one.

## Do
- Make every video genuinely distinct: a different location, recording session, time of day, and visual. "Distinct" means a viewer could tell two videos apart without reading the title.
- Prefer our own field recordings. Keep proof: raw files, a photo or short clip of the recording setup, date and place in the backlog entry.
- If using a library, use a paid license with commercial rights. Free previews are not licensed.
- Use an original or properly licensed still photo/video per video. Never reuse the same loop or image across videos.
- Put the duration and the sound in the title, since viewers search that way ("8 Hours of Heavy Rain on a Tin Roof").
- Fade in and out; keep levels steady with no sudden peaks.
- Use the standard disclaimer in descriptions. No health claims.

## Don't
- Don't publish the same audio with a different title or length.
- Don't stack several sounds into a pile of near-identical mixes.
- Don't add a music bed unless its license is recorded.
- Don't mark videos as made for kids.

## Open tests
1. Length: 3 vs 8 vs 10 hours.
2. Mid-roll: off vs automatic.
3. Visual: still photo vs slow real footage.
4. Title style: sound-first vs sleep-outcome-first.

## Workflow
1. Pick the top `idea` from `backlog.yaml`.
2. Record or license the audio; save the source in `licenses.audio` and proof of origin in `assets/`.
3. Build the video; status `produced`.
4. Fill `compliance:`; run `python3 tools/validate.py`.
5. Upload through Studio; status `scheduled`, then `published`. Record `results:` after 7 and 28 days.
