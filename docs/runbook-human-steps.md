# Runbook: steps only the owner can do

Everything else (research, scripts, fact-checks, tools, planning) is done in the repo. These items need a person, an account, or a payment. Order matters; the first four unblock publishing.

## 1. Create the channel (about 20 minutes)
- [ ] Create a dedicated Google account for the channel and turn on 2-Step Verification (required for monetization).
- [ ] Create the YouTube channel (brand channel). Pick the final name and handle. Check availability first. "Quiet Hours" is a working name.
- [ ] Paste the About text from `channels/sleep/assets/channel-about.md` (choose the voice-disclosure variant that matches your voice choice).
- [ ] In Studio, Settings, Upload defaults: audience "No, it's not made for kids"; add the description boilerplate from `templates/video/script.md`; language English.
- [ ] Create playlists: "Quiet History", later "Still Weather" and "Gentle Stories".

## 2. Choose and pay for a voice (about 30 minutes)
- [ ] Pick a provider with a paid plan that includes commercial use. The tool supports ElevenLabs. Save the plan name, the date, and a copy or link of the commercial-use terms in the backlog entry (`licenses.voice`).
- [ ] Audition three calm, low-pitched voices on a paragraph from `scripts/001.md`. Choose one and keep it for the whole channel.
- [ ] Put the voice id in `channels/sleep/channel.yaml` (`voice.voice_id`). Never commit the API key; set `ELEVENLABS_API_KEY` in the environment.
- [ ] Do not clone a real person's voice without written permission.
- [ ] Decide whether the narration sounds convincingly human. If it does, set `ai_disclosure: required` (the Studio "altered or synthetic content" toggle) and use the About variant that says so.

## 3. Produce video 001
Ask Claude to run the `produce-video` skill, or follow it by hand. You listen to the first chunk, then the flagged chunks, then spot-check the full file every ten minutes or so.
- [ ] Listen to the narration and approve pronunciation.
- [ ] Listen to the bed under the voice; it should be barely noticeable. Adjust `--bed-db` if not.
- [ ] Skim `channels/sleep/factchecks/001.md` and the items it marks hedged.

## 3b. Preview before anything is public
- [ ] Rough cut locally: the pipeline can render the real script with a free local voice for timing and feel only. It is not the voice you would publish, and its commercial-use terms were not checked. The first preview (6.9 min of 001) was made this way.
- [ ] Final check in Studio: upload with visibility Private (only you can watch), review the processed video and sound on your phone and a speaker, check the Content ID and copyright status, then switch to Scheduled or Public. Uploads can stay Private for as long as you like.

## 4. Upload in Studio
- [ ] Upload `video.mp4`, the thumbnail, and the text from `output/sleep/<id>/metadata.md`.
- [ ] Confirm not made for kids, set the AI toggle as decided, choose the playlist, set the mid-roll option for the test, and schedule.
- [ ] Check for Content ID claims after processing.
- [ ] Record the URL and publish date in the backlog entry.

## 5. Weekly
- [ ] Paste Studio numbers (views, watch hours, average view duration percent, impressions CTR, subscribers, any policy notices) into a Claude session and run `weekly-review`.

## 6. When close to the monetization threshold
- [ ] Re-check the thresholds on YouTube's help page (a rise to 8,000 hours was reported for 2027-02-01; unverified).
- [ ] Link AdSense, apply for YPP, keep the evidence trail (scripts, fact-checks, source lists, commit history are in this repo).
- [ ] If rejected, read the email, fix the named issue, and use the waiting periods: appeal within 21 days, or reapply after 30 days (first rejection) or 90 days (later).

## 7. Optional, later
- [ ] API audit request to enable automated uploads (see `docs/automation-roadmap.md`).
- [ ] An accountant for self-employment tax and a W-9 for sponsors.
- [ ] A microphone and field recorder if you want original `still-weather` recordings.
