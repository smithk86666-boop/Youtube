#!/usr/bin/env python3
"""Validate channel.yaml and backlog.yaml for every channel. Requires pyyaml."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHANNEL_STATUS = {"planning", "launching", "active", "paused", "retired"}
VIDEO_STATUS = {"idea", "scripted", "produced", "scheduled", "published", "retired"}
DISCLOSURE = {"not_required", "required", "undecided"}
GATED = {"scheduled", "published"}
COMPLIANCE_KEYS = [
    "original_script", "no_health_claims", "voice_licensed", "voice_disclosure_decided",
    "music_licensed", "visuals_licensed", "not_made_for_kids", "audio_levels_checked",
    "metadata_honest", "variation_check",
]


def check_channel(path, errors):
    data = yaml.safe_load((path / "channel.yaml").read_text())
    if data.get("slug") != path.name:
        errors.append(f"{path.name}: slug does not match folder name")
    if data.get("status") not in CHANNEL_STATUS:
        errors.append(f"{path.name}: invalid channel status {data.get('status')!r}")
    for key in ("name", "niche", "format", "voice", "monetization"):
        if key not in data:
            errors.append(f"{path.name}: channel.yaml missing {key}")


def check_backlog(path, errors):
    data = yaml.safe_load((path / "backlog.yaml").read_text()) or {}
    seen = set()
    for video in data.get("videos") or []:
        vid = video.get("id")
        where = f"{path.name}/{vid}"
        if not vid or vid in seen:
            errors.append(f"{where}: missing or duplicate id")
        seen.add(vid)
        status = video.get("status")
        if status not in VIDEO_STATUS:
            errors.append(f"{where}: invalid status {status!r}")
        if not video.get("title"):
            errors.append(f"{where}: missing title")
        if status in {"scripted", "produced", "scheduled", "published"}:
            if not (path / video.get("script", f"scripts/{vid}.md")).exists():
                errors.append(f"{where}: script file missing")
        if status in GATED:
            if video.get("ai_disclosure") not in DISCLOSURE - {"undecided"}:
                errors.append(f"{where}: ai_disclosure undecided")
            comp = video.get("compliance") or {}
            failed = [k for k in COMPLIANCE_KEYS if comp.get(k) is not True]
            if failed:
                errors.append(f"{where}: compliance not passed: {', '.join(failed)}")


def main():
    errors = []
    channels = sorted(p for p in (ROOT / "channels").iterdir() if p.is_dir())
    for path in channels:
        for name, fn in (("channel.yaml", check_channel), ("backlog.yaml", check_backlog)):
            if not (path / name).exists():
                errors.append(f"{path.name}: missing {name}")
            else:
                fn(path, errors)
    for e in errors:
        print("ERROR", e)
    print(f"{len(channels)} channel(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
