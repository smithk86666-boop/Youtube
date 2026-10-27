---
name: weekly-review
description: Review the sleep channel's results, update backlog results, evaluate tests and series, and plan next week. Use weekly, or when the user shares YouTube Studio numbers.
---

# Weekly review

## Inputs
YouTube Studio numbers pasted by the user or exported to CSV: per video views, watch time (hours), average view duration (and percent), impressions, impressions CTR, and once monetized, RPM and estimated revenue. If none are provided, say so and review process metrics only (videos shipped vs plan, compliance state).

## Steps
1. Record each video's numbers in `channels/sleep/backlog.yaml` under `results:` (7-day and 28-day when available). Do not invent numbers.
2. Compute per series: median views, median average view duration percent, median CTR, total watch hours, and watch hours per production hour if effort was logged.
3. Compare to `kpis` in `channel.yaml`. Note trends, not single-video noise. With under 10 videos, label conclusions as weak.
4. Update `docs/experiments/2026-q4-series-test.md` with the test results so far (length, mid-roll, title style, series). Apply its decision rule; do not change the rule after seeing the data.
5. Check monetization progress: subscribers and public watch hours against the thresholds in force. Re-verify the thresholds against YouTube's help page, since a rise was reported for 2027-02-01.
6. Check policy health: any claims, limited ads, strikes, or review messages. Anything negative goes at the top of the report.
7. Plan next week: pick backlog entries, adjust topics toward what retained viewers, flag videos to retire (unlist only if a policy problem; never delete for low views).
8. Write the review to `docs/reviews/<YYYY-MM-DD>.md` (three short sections: what happened, what we learned, what we do next) and commit.

## Rules
- No revenue forecasts until real RPM exists.
- Retention and CTR guide decisions; do not chase views with misleading titles.
