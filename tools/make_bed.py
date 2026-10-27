#!/usr/bin/env python3
"""Generate a quiet ambient bed (rain, wind, or waves) with ffmpeg.

The output is our own work (synthesized noise), so it carries no third-party
license or Content ID risk. It is a bed under narration, not a standalone video:
ambient-only uploads of synthetic noise would look templated.

usage: make_bed.py --kind rain|wind|waves --minutes 65 --seed 7 --out bed.m4a
Each seed changes noise, modulation periods, and phases, so beds differ per video.
"""
import argparse
import random
import subprocess
import sys


def graph(kind, seed, dur):
    rnd = random.Random(seed)
    p1, p2 = rnd.uniform(23, 41), rnd.uniform(47, 89)
    ph1, ph2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
    sr = 44100
    n = lambda color, s: f"anoisesrc=c={color}:r={sr}:seed={s}:d={dur}"
    if kind == "rain":
        # two decorrelated channels; mid-band wash plus faint high-band patter
        def side(s):
            return (f"{n('pink', s)},highpass=f=250,lowpass=f=6500,"
                    f"volume='0.55*(0.85+0.15*sin(2*PI*t/{p1:.2f}+{ph1:.2f}))':eval=frame[w{s}];"
                    f"{n('white', s + 100)},highpass=f=3500,lowpass=f=9000,"
                    f"volume='0.05*(0.6+0.4*sin(2*PI*t/{p2:.2f}+{ph2:.2f}))':eval=frame[h{s}];"
                    f"[w{s}][h{s}]amix=inputs=2:normalize=0[m{s}]")
    elif kind == "wind":
        def side(s):
            return (f"{n('brown', s)},highpass=f=50,lowpass=f=650,"
                    f"volume='0.9*(0.25+0.75*pow(0.5+0.5*sin(2*PI*t/{p1:.2f}+{ph1:.2f}),1.5))*"
                    f"(0.7+0.3*sin(2*PI*t/{p2:.2f}+{ph2:.2f}))':eval=frame[m{s}]")
    elif kind == "waves":
        period = rnd.uniform(8.5, 12.5)

        def side(s):
            return (f"{n('brown', s)},highpass=f=40,lowpass=f=1100,"
                    f"volume='0.95*(0.12+0.88*pow(abs(sin(PI*t/{period:.2f}+{ph1:.2f})),2))':eval=frame[m{s}]")
    else:
        raise SystemExit("kind must be rain, wind, or waves")
    s1, s2 = seed * 2 + 1, seed * 2 + 2
    return f"{side(s1)};{side(s2)};[m{s1}][m{s2}]amerge=inputs=2,aformat=channel_layouts=stereo[out]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True)
    ap.add_argument("--minutes", type=float, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    dur = int(a.minutes * 60)
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-filter_complex",
           graph(a.kind, a.seed, dur), "-map", "[out]", "-c:a", "aac", "-b:a", "128k", a.out]
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit("ffmpeg failed")
    print(f"wrote {a.out} ({a.kind}, seed {a.seed}, {dur}s)")


if __name__ == "__main__":
    main()
