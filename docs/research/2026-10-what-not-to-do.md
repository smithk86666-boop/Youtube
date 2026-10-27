# What the bottom 90% get wrong (researched 2026-10-26)

No source gave a verified failure rate. A "90% never reach 1,000 subscribers" figure and a "97% fail" headline were found with no methodology, so we do not use them. The list below combines creator-advice sources, YouTube's help pages, and reporting on AI sleep channels. Confidence is medium unless noted.

| Mistake | Evidence | What we do instead |
|---|---|---|
| Templated, mass-produced videos | YouTube policy text; 404 Media on AI history channels | One distinct topic and structure per video; recurring intro/outro only; `tools/lint_script.py` blocks near-duplicate scripts |
| Reading others' material aloud | YouTube "reused content" text | Write original scripts from several sources; keep a source list; never paste from Wikipedia |
| Inaccurate content | Historian quoted in 404 Media | Fact-check pass, sources listed in the description, corrections log |
| Glitchy or mispronounced narration | "FEEEEEE" glitch at 1h15m; forum anecdote on mispronunciation | Pronunciation lexicon, chunk-boundary checks, spot-listen every ~10 minutes |
| Loud or abrupt audio | Common sense plus sleep context; no source on sleepers specifically | Loudness target around -24 LUFS, fade in and out, no stings |
| Inconsistent uploads | Creator-advice sources | Fixed weekly rhythm in `calendar.md` |
| No clear niche or audience | Creator-advice sources | One audience, one promise, series inside it |
| Impatience, unrealistic expectations | vidIQ: creators expect fast results, then find 1,000 subs and 4,000 hours hard after 6-12 months | 90-day plan with checkpoints; judge by leading indicators (CTR, retention), not income |
| Deleting underperforming videos | vidIQ: deleting a video removes its views and watch time, which hurts monetization progress | Retire by unlisting only if a video breaks policy; never delete for low views |
| No monetization plan beyond ads | Creator-advice sources; small ambient channels earn little | Affiliate and product plan in `strategy.md` |
| Appealing a rejection without preparing | YouTube help: appeal within 21 days; first reapply wait 30 days, later 90; appeals are judged on the channel as it stands | Keep the evidence trail; fix named issues before reapplying; prefer fix-and-reapply for a first rejection if the cause is clear |
| Copying a competitor's brand wording | Reasoned: confuses viewers, invites reports and trademark trouble | Own name, own title formula |
| Chasing views with misleading titles | Common platform guidance | Honest metadata (`compliance.metadata_honest`) |

## Sleep-specific hazards to test, not assume

- Mid-roll ads may wake listeners; no source tested this. Run the on/off test.
- Sleep viewers tolerate repetition; the algorithm and reviewers may not. Variation lives in topics and visuals, not in the voice.
- Very long videos (3+ hours) are the norm among imitators. Length is a test, not a rule.

## Sources

- https://support.google.com/youtube/answer/1311392
- https://support.google.com/youtube/answer/9235730
- https://news.slashdot.org/story/25/09/03/2028206/ai-generated-boring-history-videos-are-flooding-youtube-drowning-out-real-history
- https://vidiq.com/blog/post/13-mistakes-new-youtubers-make/
- https://www.sirency.com/blog/youtube-monetization-rejected
