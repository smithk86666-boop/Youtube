#!/usr/bin/env python3
"""Build upload metadata (title, description, chapters, sources) for a video.

usage: package.py <channel> <id> [--duration-sec N] [--wpm 125]

Chapters come from the script's `## ` headings. Timestamps are estimated from word counts
and, if --duration-sec (the real narration length) is given, scaled to it. Estimates drift;
check them against the audio before publishing. Output: output/<channel>/<id>/metadata.md
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scriptlib import NARR_END, NARR_START, ROOT, find_video, read_channel, words  # noqa: E402

DISCLAIMER = ("This video is for relaxation and entertainment. It is not medical advice and does not "
              "treat or cure any condition. If you have trouble sleeping or worry about your health, "
              "speak with a qualified professional.")


def fmt(sec):
    sec = int(sec)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def chapters(text, wpm, duration):
    if NARR_START in text and NARR_END in text:
        text = text.split(NARR_START, 1)[1].split(NARR_END, 1)[0]
    sections, title, buf = [], "Introduction", []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*)", line)
        if m:
            sections.append((title, len(words(" ".join(buf)))))
            title, buf = m.group(1).strip(), []
        elif not line.lstrip().startswith(("#", "<!--")):
            buf.append(line)
    sections.append((title, len(words(" ".join(buf)))))
    sections = [(t, n) for t, n in sections if n > 0]
    total_words = sum(n for _, n in sections)
    scale = (duration / (total_words / wpm * 60)) if duration else 1.0
    out, t = [], 0.0
    for title, n in sections:
        out.append((t, title))
        t += n / wpm * 60 * scale
    return out


def topic_sentence(topic):
    topic = topic.strip()
    return (topic[:1].upper() + topic[1:] + ".") if topic else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel")
    ap.add_argument("id")
    ap.add_argument("--duration-sec", type=float)
    ap.add_argument("--wpm", type=int, default=125)
    a = ap.parse_args()

    video = find_video(a.channel, a.id)
    chan = read_channel(a.channel)
    script = (ROOT / "channels" / a.channel / video.get("script", f"scripts/{a.id}.md")).read_text()
    ch = chapters(script, a.wpm, a.duration_sec)
    lines = [f"# {video['title']}", "", f"Title length: {len(video['title'])} characters"
             + (" (consider shortening below 70)" if len(video["title"]) > 70 else ""), "",
             "## Description", "",
             f"{topic_sentence(video.get('topic', ''))} A calm, slowly paced narration for winding down. "
             "Everything described is drawn from historical research; sources are listed below.", ""]
    if len(ch) >= 3:
        lines += ["Chapters (estimated, verify against the audio):"] + [f"{fmt(t)} {title}" for t, title in ch] + [""]
    if video.get("sources"):
        lines += ["Sources and further reading:"] + [f"- {s}" for s in video["sources"]] + [""]
    lines += [DISCLAIMER, ""]
    if video.get("ai_disclosure") == "required":
        lines += ["Narration uses a synthetic voice.", ""]
    lines += ["## Studio settings checklist", "",
              "- Audience: not made for kids",
              f"- Altered or synthetic content toggle: {video.get('ai_disclosure', 'undecided')}",
              "- Playlist: " + str(video.get("series", "")),
              "- Mid-roll: per current test assignment in docs/experiments/",
              "- Thumbnail: uploaded; title matches content",
              f"- Channel: {chan['name']} (working name)", ""]
    out = ROOT / "output" / a.channel / a.id
    out.mkdir(parents=True, exist_ok=True)
    (out / "metadata.md").write_text("\n".join(lines))
    print(f"wrote {out / 'metadata.md'}")


if __name__ == "__main__":
    main()
