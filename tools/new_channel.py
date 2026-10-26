#!/usr/bin/env python3
"""Scaffold channels/<slug>/ from templates/channel."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "channel"


def main(argv):
    if len(argv) != 3:
        print('usage: new_channel.py <slug> "<Display Name>"')
        return 2
    slug, name = argv[1], argv[2]
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        print("slug must be lowercase kebab-case")
        return 2
    dest = ROOT / "channels" / slug
    if dest.exists():
        print(f"{dest} already exists")
        return 1
    (dest / "scripts").mkdir(parents=True)
    (dest / "assets").mkdir()
    for src in TEMPLATE.iterdir():
        text = src.read_text().replace("{{slug}}", slug).replace("{{name}}", name)
        (dest / src.name).write_text(text)
    print(f"created {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
