# Experiment: narrated sleep content vs ambient sounds

Question: which format earns more watch hours, and eventually revenue, per unit of effort?

## Arms

| | A: `sleep-stories` | B: `ambient-sounds` |
|---|---|---|
| Format | Narrated calm history/science, ~150 min | Real-location rain/wind/wave sound, ~480 min |
| Production | Script + licensed voice + render | Recording or licensed audio + photo/footage + render |
| Cost to make | Higher (writing, voice plan) | Lower |
| Main risk | Inauthentic-content flag if scripts are templated; AI disclosure | Repetitive-content flag; library licensing |

Separate channels and separate Google accounts, so one format's problems cannot affect the other and the audience signal stays clean. Mixing formats on one channel muddies recommendations.

## Controls

- Same start date, same cadence (2 per week), same number of videos (10 each in the first 5 weeks).
- Same upload window, same title-and-thumbnail effort level.
- Every video follows its channel's compliance gate.

## Metrics (record in each backlog entry's `results:`)

- 7-day and 28-day views, watch hours, average view duration percent
- Impressions click-through rate
- RPM once monetized (not available before YPP)
- Production effort in hours and out-of-pocket cost per video
- Policy events: claims, limited ads, strikes, YPP review outcome

## Decision rule (apply at the 28-day read of video 10)

1. Primary: median 28-day watch hours per video, divided by production hours plus cost. Compare the arms.
2. If one arm is at least about 2x the other, scale it and pause the other. If not, continue both for one more cycle and re-read.
3. Overrides, regardless of the ratio: stop an arm that gets a strike or a YPP rejection for repetitive/inauthentic content until the cause is fixed.
4. Do not extrapolate revenue until at least one arm is monetized and real RPM exists.

No numeric thresholds beyond the 2x ratio are set yet. We have no baseline. Add them after the first five videos exist.

## Known tradeoffs

- Splitting effort across two new channels delays either one reaching the YPP watch-hour threshold. The reported rise to 8,000 hours on 2027-02-01 (unverified) makes that delay costlier. If the date is confirmed and we are far from threshold, consider running arms in sequence, ambient first because it is cheaper to produce.
- 10 videos per arm is small. Treat the result as direction, not proof. Topic and thumbnail differences add noise.
- Other formats can be added as new arms (guided meditation, fiction stories) using the same template.
