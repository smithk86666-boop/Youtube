#!/usr/bin/env python3
"""Narration synthesis: chunk a script, apply the pronunciation lexicon, call a
TTS provider, check chunks for glitches, and join them.

Commands
  plan   <channel> <id>                  show the chunk plan; no network, no cost
  run    <channel> <id> [--voice ID]     synthesize (needs ELEVENLABS_API_KEY)
  check  <channel> <id>                  flag chunks whose seconds-per-word is off
  join   <channel> <id>                  concatenate chunks into narration.wav

Status: `plan`, `check`, and `join` are tested locally. `run` calls the provider's
HTTP API and has NOT been tested against the live service (no key available when
written). Run it on one short chunk first and listen before a full video.
Use a paid plan with commercial rights; record plan and date in the backlog entry.
Outputs go to output/<channel>/<id>/ (gitignored).
"""
import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scriptlib import ROOT, find_video, full_narration, read_channel, words  # noqa: E402

MAX_CHARS = 2800


def out_dir(channel, vid):
    d = ROOT / "output" / channel / vid
    (d / "chunks").mkdir(parents=True, exist_ok=True)
    return d


def load_lexicon(channel):
    lex = {}
    path = ROOT / "channels" / channel / "assets" / "lexicon.txt"
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip() and not line.startswith("#") and "\t" in line:
                a, b = line.split("\t", 1)
                lex[a.strip()] = b.strip()
    return lex


def apply_lexicon(text, lex):
    for a, b in lex.items():
        text = re.sub(rf"\b{re.escape(a)}\b", b, text)
    return text


def chunk_text(text, max_chars=MAX_CHARS):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(p) > max_chars:  # split a long paragraph on sentence ends
            sents = re.split(r"(?<=[.!?])\s+", p)
        else:
            sents = [p]
        for s in sents:
            if cur and len(cur) + len(s) + 2 > max_chars:
                chunks.append(cur)
                cur = ""
            cur = f"{cur}\n\n{s}" if cur else s
    if cur:
        chunks.append(cur)
    return chunks


def get_chunks(channel, vid):
    video = find_video(channel, vid)
    script = ROOT / "channels" / channel / video.get("script", f"scripts/{vid}.md")
    text = apply_lexicon(full_narration(script.read_text()), load_lexicon(channel))
    return chunk_text(text)


def cmd_plan(a):
    chunks = get_chunks(a.channel, a.id)
    total = sum(len(c) for c in chunks)
    w = sum(len(words(c)) for c in chunks)
    print(f"{len(chunks)} chunks, {total} characters, {w} words, about {w / 125:.0f} min at 125 wpm")
    print(f"largest chunk {max(len(c) for c in chunks)} chars (limit {MAX_CHARS})")


def synth_elevenlabs(text, voice, prev_text, next_text, key):
    body = {"text": text, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.7, "similarity_boost": 0.75, "style": 0.0}}
    if prev_text:
        body["previous_text"] = prev_text[-500:]
    if next_text:
        body["next_text"] = next_text[:500]
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(2 ** (attempt + 1))
                continue
            raise SystemExit(f"provider error {e.code}: {e.read()[:200]!r}")
    raise SystemExit("provider failed")


def cmd_run(a):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("set ELEVENLABS_API_KEY (never commit it)")
    voice = a.voice or read_channel(a.channel)["voice"].get("voice_id")
    if not voice:
        sys.exit("no voice id: pass --voice or set voice.voice_id in channel.yaml")
    chunks = get_chunks(a.channel, a.id)
    d = out_dir(a.channel, a.id)
    limit = a.limit or len(chunks)
    for i, c in enumerate(chunks[:limit]):
        f = d / "chunks" / f"{i:04d}.mp3"
        if f.exists() and f.stat().st_size > 0:
            continue  # resumable
        audio = synth_elevenlabs(c, voice, chunks[i - 1] if i else "", chunks[i + 1] if i + 1 < len(chunks) else "", key)
        f.write_bytes(audio)
        print(f"chunk {i + 1}/{len(chunks)} ok ({len(audio) // 1024} KB)")


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def cmd_check(a):
    chunks = get_chunks(a.channel, a.id)
    d = out_dir(a.channel, a.id)
    rows = []
    for i, c in enumerate(chunks):
        f = d / "chunks" / f"{i:04d}.mp3"
        if not f.exists():
            print(f"MISSING chunk {i}")
            continue
        rows.append((i, duration(f) / max(1, len(words(c)))))
    if not rows:
        sys.exit("no chunks found")
    med = statistics.median(r for _, r in rows)
    bad = [(i, r) for i, r in rows if r < med * 0.8 or r > med * 1.25]
    print(f"{len(rows)}/{len(chunks)} chunks, median {med:.3f} s/word (~{60 / med:.0f} wpm)")
    for i, r in bad:
        kind = "too fast: dropped text?" if r < med else "too slow: repeats/glitch?"
        print(f"FLAG chunk {i}: {r:.3f} s/word, {kind}. Listen to {d / 'chunks' / f'{i:04d}.mp3'}")
    print("OK" if not bad and len(rows) == len(chunks) else "REVIEW")
    return 1 if bad or len(rows) != len(chunks) else 0


def cmd_join(a):
    d = out_dir(a.channel, a.id)
    files = sorted((d / "chunks").glob("*.mp3"))
    if not files:
        sys.exit("no chunks")
    listing = d / "chunks.txt"
    listing.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    out = d / "narration.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-ar", "44100", "-ac", "2", str(out)], check=True)
    print(f"wrote {out} ({duration(out) / 60:.1f} min)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("plan", cmd_plan), ("run", cmd_run), ("check", cmd_check), ("join", cmd_join)):
        p = sub.add_parser(name)
        p.add_argument("channel")
        p.add_argument("id")
        if name == "run":
            p.add_argument("--voice")
            p.add_argument("--limit", type=int, help="only synthesize the first N chunks (test run)")
        p.set_defaults(fn=fn)
    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
