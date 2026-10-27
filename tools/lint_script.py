#!/usr/bin/env python3
"""Lint a narration script before voice generation.

Checks length, health claims, tone, sentence shape, and near-duplicate text
against other scripts in the same folder (templating guard).

usage: lint_script.py <script.md> [--wpm 125] [--target-min N] [--max-similarity 0.08]
Exit code 1 if any ERROR is found.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scriptlib import sentences, split_script, words  # noqa: E402

HEALTH = [
    r"\bcures?\s+(for\s+)?(your\s+)?(insomnia|anxiety|stress|depression|sleeplessness)",
    r"\b(treats?|treating|heals?|fix(es)?)\s+(your\s+)?(insomnia|anxiety|depression|sleeplessness)",
    r"\bclinically\s+proven\b", r"\bguaranteed?\b.{0,40}\bsleep",
    r"\binsomnia\s+(cure|treatment|remedy)",
    r"\bfall\s+asleep\s+(in|within)\s+\d+", r"\b(replace|instead\s+of)\s+(your\s+)?(medication|therapy|doctor)",
    r"\bhelps?\s+(you\s+)?(overcome|beat|cure)\s+(insomnia|anxiety)",
]
TENSION = ["suddenly", "scream", "screamed", "blood", "murder", "terrified", "horror",
           "shocking", "unbelievable", "you won't believe", "chilling", "slaughter", "gruesome"]


def shingles(text, n=6):
    w = [x.lower() for x in words(text)]
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--wpm", type=int, default=125)
    ap.add_argument("--target-min", type=float)
    ap.add_argument("--max-similarity", type=float, default=0.08)
    args = ap.parse_args()

    path = Path(args.script)
    text = path.read_text()
    narration, fixed = split_script(text)
    all_words = words(narration) + words(fixed)
    n = len(all_words)
    minutes = n / args.wpm
    errors, warns = [], []

    print(f"{path.name}: {n} words, about {minutes:.0f} min at {args.wpm} wpm")
    if args.target_min:
        lo, hi = args.target_min * 0.9, args.target_min * 1.1
        if not lo <= minutes <= hi:
            errors.append(f"length {minutes:.0f} min is outside 10% of target {args.target_min:.0f} min")

    for pat in HEALTH:
        for m in re.finditer(pat, narration, re.I):
            errors.append(f"health claim pattern {pat!r}: ...{narration[max(0, m.start() - 30):m.end() + 30].strip()}...")
    low = narration.lower()
    for t in TENSION:
        c = low.count(t)
        if c:
            warns.append(f"tension word {t!r} x{c}")
    if narration.count("!"):
        warns.append(f"{narration.count('!')} exclamation marks")
    shouting = [w for w in words(narration) if len(w) >= 4 and w.isupper()]
    if shouting:
        warns.append(f"all-caps words: {', '.join(sorted(set(shouting))[:6])}")

    sents = sentences(narration)
    if sents:
        lens = [len(words(s)) for s in sents]
        avg = sum(lens) / len(lens)
        short = sum(1 for x in lens if x < 6) / len(lens)
        print(f"sentences: {len(sents)}, average {avg:.1f} words, {short:.0%} under 6 words, longest {max(lens)}")
        if avg < 12:
            warns.append("average sentence is short; sleep narration reads better with medium and long sentences")
        if short > 0.20:
            warns.append("more than 20% punchy short sentences")
        if max(lens) > 60:
            warns.append("a sentence over 60 words; may be hard to narrate")
        openers = {}
        for s in sents:
            k = " ".join(words(s)[:2]).lower()
            openers[k] = openers.get(k, 0) + 1
        top = sorted(openers.items(), key=lambda kv: -kv[1])[:1]
        if top and top[0][1] / len(sents) > 0.08 and top[0][0]:
            warns.append(f"repetitive sentence opener {top[0][0]!r} in {top[0][1] / len(sents):.0%} of sentences")

    mine = shingles(narration)
    for other in sorted(path.parent.glob("*.md")):
        if other.resolve() == path.resolve() or other.name.startswith("_"):
            continue
        theirs = shingles(split_script(other.read_text())[0])
        if not mine or not theirs:
            continue
        sim = len(mine & theirs) / len(mine | theirs)
        if sim > args.max_similarity:
            errors.append(f"text overlap with {other.name}: {sim:.1%} (limit {args.max_similarity:.0%})")

    if "not medical advice" not in text.lower() and "disclaimer" not in text.lower():
        warns.append("no disclaimer text found in the script file (it must be in the description)")

    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
