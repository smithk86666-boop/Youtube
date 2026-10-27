# Experiment: series and format tests inside one channel

One channel (`sleep`), several series. We learn which format earns the most watch hours per unit of effort and which retains viewers, without splitting effort across channels.

## Why one channel
Decision by the owner: all of it is sleep content, so one audience and one brand. Tradeoff noted: YouTube recommendations learn from viewing patterns, and a very different format can muddy them. Mitigations: separate playlists per series, consistent branding and voice, titles that name the series, and probes only after the core series has traction.

## Arms (series)
| Series | When | Format | Cost to make |
|---|---|---|---|
| `quiet-history` | videos 001-010 first | Narrated calm history, 60-120 min | Script, fact-check, voice plan, render |
| `still-weather` | after 8 core videos, 2 videos | One real place and sound, 3+ hours, provenance proof | Recording or paid license, art |
| `gentle-stories` | after 8 core videos, 2 videos | Original calm fiction, 60 min | Script, voice plan, render |

## Within-series tests (core series)
1. **Length:** 60, 90, 120 minutes across videos 001-010, topics matched as closely as possible.
2. **Mid-roll:** off vs automatic, assigned alternately.
3. **Title style:** honest hook vs question form.
4. **Visual:** generated night sky vs period-accurate art.

## Metrics
Record in each backlog entry `results:` at 7 and 28 days: views, watch hours, average view duration percent, impressions CTR. After monetization: RPM. Also log production hours and any out-of-pocket cost per video, and any policy events.

## Decision rules (fixed now, applied at the 28-day read)
1. Primary: median 28-day watch hours per video divided by production hours plus cost, per series.
2. A probe series replaces core effort only if its ratio is at least 2x the core series over at least 2 videos. Otherwise it stays a probe or stops.
3. Length: choose the length with the best average view duration percent without a drop in watch hours per video.
4. Mid-roll: keep it on only if RPM gain outweighs any measurable drop in average view duration percent. Sleep audiences may be woken by ads; watch the comments.
5. Stop or fix a series that gets a strike, a limited-ads notice for repetitive or inauthentic content, or a YPP rejection citing it.
6. No revenue forecast until real RPM exists.

Sample sizes are small. Treat results as direction. Re-run with more videos before drawing firm conclusions.

## Earlier plan
An earlier draft ran two channels (narrated vs ambient). The ambient format was kept as the `still-weather` series because of its repetitive-content risk (see `docs/research/2026-10-ambient-sounds.md`).
