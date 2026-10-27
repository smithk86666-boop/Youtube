---
name: niche-sampling
description: Sample real YouTube search results for target queries to measure demand, competition, quality, and gaps for the sleep channel. Use before choosing topics, when re-validating the niche, or when a series underperforms.
---

# Niche sampling

Purpose: replace guesses with observed data. This repo has no YouTube API key, so sampling uses WebSearch and WebFetch against public pages (video pages, channel aggregator pages such as vidIQ, Social Blade, OutlierKit). Expect partial data and say what is missing.

## Steps
1. List 15 queries from `channels/sleep/strategy.md` plus any new idea (era, region, activity, "no music", duration terms).
2. For each query, find the top results that WebSearch surfaces and open the most relevant 5 video or channel pages. Record: title, channel, views, age, length, subscribers, upload cadence, whether visuals look accurate, whether narration is human or synthetic (only if stated), and any visible comment complaints about accuracy or audio.
3. Mark each result as measured (read from a page) or estimated (from an aggregator or AI-written analysis). Never blend them.
4. Summarize in a table, then answer:
   - Which queries have high views with weak competitors (inaccurate, glitchy, templated)?
   - Which eras or regions are underserved?
   - What lengths dominate?
   - What do comments praise or complain about?
5. Write the findings to `docs/research/<YYYY-MM>-sampling-<topic>.md` with sources and a confidence note. Propose backlog changes and edit `backlog.yaml` only for ideas backed by the data.

## Rules
- Do not copy competitor titles or thumbnails; learn the pattern, write our own.
- If a number cannot be verified, label it unverified.
