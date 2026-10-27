"""Shared helpers for reading channel scripts and backlog entries."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

NARR_START = "<!-- narration:start -->"
NARR_END = "<!-- narration:end -->"
FIXED_START = "<!-- fixed:start -->"
FIXED_END = "<!-- fixed:end -->"


def read_backlog(channel):
    path = ROOT / "channels" / channel / "backlog.yaml"
    return yaml.safe_load(path.read_text()).get("videos") or []


def find_video(channel, vid):
    for v in read_backlog(channel):
        if v.get("id") == vid:
            return v
    raise SystemExit(f"video {vid} not found in channels/{channel}/backlog.yaml")


def read_channel(channel):
    return yaml.safe_load((ROOT / "channels" / channel / "channel.yaml").read_text())


def split_script(text):
    """Return (narration, fixed) text. Narration excludes markdown headings and
    HTML comments; fixed holds text inside fixed markers (shared intro/outro)."""
    if NARR_START in text and NARR_END in text:
        text = text.split(NARR_START, 1)[1].split(NARR_END, 1)[0]
    fixed_parts = re.findall(re.escape(FIXED_START) + r"(.*?)" + re.escape(FIXED_END), text, re.S)
    body = re.sub(re.escape(FIXED_START) + r".*?" + re.escape(FIXED_END), "", text, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    lines = [ln for ln in body.splitlines() if not ln.lstrip().startswith("#")]
    narration = "\n".join(lines).strip()
    fixed = "\n".join(fixed_parts).strip()
    return narration, fixed


def full_narration(text):
    """Narration including the fixed intro/outro, in script order, headings removed."""
    if NARR_START in text and NARR_END in text:
        text = text.split(NARR_START, 1)[1].split(NARR_END, 1)[0]
    text = text.replace(FIXED_START, "").replace(FIXED_END, "")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
    return "\n".join(lines).strip()


def words(text):
    return re.findall(r"[A-Za-z0-9'’-]+", text)


def sentences(text):
    flat = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p for p in parts if p.strip()]
