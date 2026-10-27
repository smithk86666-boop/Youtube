---
name: fact-check-script
description: Verify every factual claim in a sleep-channel script against independent sources, soften or fix what cannot be verified, and record a report. Use after a script is drafted and before it can be scheduled.
---

# Fact-check a script

Accuracy is the channel's main edge over the flood of inaccurate AI history videos. Do not skip claims because they sound familiar.

## Steps
1. Open `channels/sleep/scripts/<id>.md` and its numbered fact-check list. Add any claim that is in the narration but missing from the list (dates, numbers, names, "was common", "always", causes, etymologies, customs).
2. For each claim, search with WebSearch and WebFetch for two independent sources, at least one scholarly or institutional (museum, university, heritage body, reputable reference). Record the URL and what it says.
3. Classify each claim:
   - `verified`: two independent sources agree.
   - `hedged`: sources conflict or evidence is thin. The script must say so ("historians think...", "we do not know..."). Edit the script to match.
   - `removed`: could not be verified. Delete or rewrite the sentence.
   - `atmosphere`: not a historical claim (weather, sounds). Check it is not stated as fact about the past.
4. Check for anachronism: objects, foods, words, and customs must fit the stated place and decade. Check proverbs and quotations are real and dated, or remove them.
5. Write the report to `channels/sleep/factchecks/<id>.md`: a table of claim, verdict, sources, and the edit made. Note any claim you could not check.
6. Re-run `python3 tools/lint_script.py` after edits.
7. In `backlog.yaml` set `fact_check: done` only if no claim is left unclassified and every `verified` claim has two sources in the report. Otherwise leave `pending` and say what blocks it.
8. State plainly in the report that this was done by an AI search pass, and that a human spot-check of the highest-risk claims is still recommended.

## Do not
- Do not mark `done` on the strength of your own memory.
- Do not cite a source you did not open.
- Do not keep a claim because it makes the script nicer.
