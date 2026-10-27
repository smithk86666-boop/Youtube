#!/usr/bin/env python3
"""Mix narration with a bed under it and render an MP4 with a still image.

usage: render_video.py --narration narration.wav --bed bed.m4a (--image art.jpg | --video loop.mp4) --out video.mp4
         [--bed-db -22] [--lufs -24] [--fade-in 4] [--fade-out 30] [--tail 30]

The bed sits well below the voice, the narration is leveled, the mix ends with a long
fade and a quiet tail, and the final loudness lands near -24 LUFS so it is gentle.
"""
import argparse
import subprocess
import sys


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", required=True)
    ap.add_argument("--bed", required=True)
    ap.add_argument("--image", help="still image background")
    ap.add_argument("--video", help="seamless looping background clip (see animate_painting.py)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--bed-db", type=float, default=-22.0, help="bed level relative to leveled narration")
    ap.add_argument("--lufs", type=float, default=-24.0)
    ap.add_argument("--fade-in", type=float, default=4.0)
    ap.add_argument("--fade-out", type=float, default=30.0)
    ap.add_argument("--tail", type=float, default=30.0, help="seconds of bed-only audio after the voice")
    ap.add_argument("--fps", type=int, default=5, help="frame rate for still images")
    a = ap.parse_args()
    if bool(a.image) == bool(a.video):
        sys.exit("give exactly one of --image or --video")

    nd, bd = duration(a.narration), duration(a.bed)
    total = nd + a.tail
    if bd < total:
        sys.exit(f"bed is {bd:.0f}s but the video needs {total:.0f}s; generate a longer bed")
    fade_start = max(0.0, total - a.fade_out)
    graph = (
        f"[0:a]aformat=channel_layouts=stereo,loudnorm=I=-20:TP=-3:LRA=7,apad=pad_dur={a.tail}[v];"
        f"[1:a]aformat=channel_layouts=stereo,atrim=0:{total:.2f},volume={a.bed_db}dB[b];"
        f"[v][b]amix=inputs=2:duration=longest:normalize=0,"
        f"afade=t=in:st=0:d={a.fade_in},afade=t=out:st={fade_start:.2f}:d={a.fade_out},"
        f"loudnorm=I={a.lufs}:TP=-3:LRA=9,atrim=0:{total:.2f}[a]"
    )
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats",
           "-i", a.narration, "-i", a.bed,
           *(["-loop", "1", "-framerate", str(a.fps), "-i", a.image] if a.image
             else ["-stream_loop", "-1", "-i", a.video]),
           "-filter_complex", graph,
           "-map", "2:v", "-map", "[a]",
           "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p",
           "-c:v", "libx264", *(["-tune", "stillimage", "-crf", "30"] if a.image else ["-crf", "26"]),
           "-preset", "veryfast", "-r", str(a.fps if a.image else 24),
           "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-t", f"{total:.2f}", "-movflags", "+faststart", a.out]
    if subprocess.run(cmd).returncode:
        sys.exit("ffmpeg failed")
    print(f"wrote {a.out} ({total / 60:.1f} min)")


if __name__ == "__main__":
    main()
