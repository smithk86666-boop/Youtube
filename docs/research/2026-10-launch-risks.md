# Launch risks and unknowns (researched 2026-10-26)

Source quality: almost everything below comes from third-party blogs and tool vendors, not YouTube's own pages. Confidence is marked per item. Re-verify against YouTube Help Center and Google API docs before acting on anything marked medium or low.

## 1. Automated uploads can be locked to private (high impact, medium confidence)

- API projects created after July 2020 that have not passed Google's compliance audit have `videos.insert` uploads forced to private, even if `privacyStatus` is `public`. The call succeeds and the creator is emailed later.
- Quota is a separate system from the audit. Staying under quota does not lift the lock. The audit can take weeks.
- Quota cost of `videos.insert` is reported inconsistently (1,600 units, 100 units, or 1 unit in a separate 100/day bucket). Check the quota table and your project's quota page.
- **Decision:** upload manually through Studio at first. File the audit request early if automation is still the goal. See `docs/automation-roadmap.md`.

## 2. Monetization thresholds are rising (high impact, medium confidence)

- Today: 1,000 subscribers plus 4,000 public watch hours (12 months) or 10M Shorts views (90 days). An early-access tier at 500 subscribers plus 3,000 hours unlocks memberships and similar features but not ad revenue.
- Several sources report Tier 2 rising on 2027-02-01 to 8,000 watch hours or 20M Shorts views for new applicants. This is reported by third parties only.
- Reviews reportedly take about a month.
- **Implication:** speed to the first 4,000 hours matters. Long-form sleep content helps, but only if retention holds.

## 3. Inauthentic-content enforcement (high impact, medium confidence)

- The test is reported as origin and originality, not voice type. AI narration over an original script is described as acceptable by vendor sources; templated, mass-produced, near-identical videos are the risk pattern.
- One source claims enforcement is channel-level, pulling monetization from all videos on a pattern detected across recent uploads. Unconfirmed by YouTube documentation in these results.
- **Mitigation:** distinct scripts, varied topics and visuals, real editorial value, modest upload cadence, no bulk-generation bursts.

## 4. AI disclosure label (medium impact, medium confidence)

- The Studio "altered or synthetic content" toggle applies to realistic content a viewer could mistake for real, including a synthetic voice imitating a real person.
- Sources disagree on generic text-to-speech. NBC and AIR Media-Tech say a clearly synthetic narrator that impersonates no one does not need a label; others list synthetic narration as an example.
- **Rule:** if the voice sounds convincingly human, disclose. Record the decision per video. YouTube can add the label itself, and repeated non-disclosure can bring penalties.

## 5. Voice licensing (medium impact, medium confidence)

- ElevenLabs free tier: reported as non-commercial with attribution required. Paid tiers reported to include commercial rights.
- Alternatives named by a vendor blog: OpenAI TTS, Deepgram Aura, Cartesia. That blog is a competitor.
- **Rule:** use a paid plan with commercial rights, save the plan and terms snapshot date in the backlog entry, and never clone a real person's voice without written consent.

## 6. Music licensing and Content ID (medium impact, low-medium confidence)

- Suno free tracks reported as non-commercial; paid tiers reported to include commercial rights. A paid license does not stop Content ID false claims, and the legal status of AI-generated music ownership is unsettled. Suno terms reportedly changed around 2026-09-03 (unverified).
- Epidemic Sound licensing was not covered by the search. Unknown.
- **Rule:** keep ambient beds simple, record license receipts, and expect to dispute claims. Prefer narration-led videos where music is a quiet bed, so a claim has less to hit.

## 7. Mid-roll ads on sleep content (medium impact, low confidence)

- Since 2025-05-12, YouTube places automatic mid-rolls at natural breaks. Creators can opt out at some revenue cost.
- No source addressed ads waking sleeping viewers, or very long videos. This needs our own testing.
- **Test plan:** on the first 10 videos, compare no-mid-roll against automatic mid-roll on retention and RPM before standardizing. One anecdote reports retention falling from 55% to 28% after padding for mid-rolls.

## 8. Health and wellness claims (medium impact, low confidence on sleep specifics)

- YouTube's medical misinformation policy covers treatment and prevention claims. Its examples are cancer, vaccines, and similar; nothing found specific to sleep or meditation.
- **Rule:** no claims of treating insomnia or any condition. Standard disclaimer in every description.

## 9. Business basics (low-medium impact, medium confidence)

- AdSense income is generally treated as self-employment income. Expect quarterly estimated tax payments, a W-9 for sponsors, and possibly a single-member LLC. Not tax or legal advice; confirm with an accountant.
- Baseline YPP requirements include 2-Step Verification and no active strikes.
- Not researched: running several channels under one Google account versus separate accounts, and any cross-channel penalty risk. Treat as unknown. Default to a separate Google account and brand channel per channel until verified.

## 10. Still unresearched

- Real search demand and competition inside the chosen sub-niche (needs VidIQ/TubeBuddy/YouTube search sampling).
- Thumbnail and title CTR norms for sleep content.
- Copyright status of images and video loops (use own or properly licensed art).
- Non-ad revenue: affiliate programs for sleep products, sponsorship minimums.
- Audience safety: sleep content played for children, and YouTube's "made for kids" setting (default to not made for kids, adult audience, and confirm).
