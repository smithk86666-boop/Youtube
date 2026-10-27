#!/usr/bin/env python3
"""Turn a still painting or photo of water into a seamless looping 1080p background clip.

The motion is a gentle 2.5D effect, not generated imagery: rolling wave displacement that grows
toward the viewer, a slow side-to-side surge, faint haze shimmer in the sky, glints on bright foam,
and a very slow push-in. Every motion period divides the loop length, so the clip repeats seamlessly.

usage: animate_painting.py --image art.png --out bg_loop.mp4 [--seconds 30] [--fps 24]
         [--horizon 0.32] [--crop-y 100] [--strength 1.0]

--horizon  fraction of image height where the water begins (motion is masked above it)
--crop-y   top of the 16:9 crop in source pixels (the crop takes the full width)
Only use art you own or have the rights to use; record it in the backlog entry (docs/art-sourcing.md).
"""
import argparse
import subprocess
import sys

import numpy as np
from PIL import Image


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def sample(img, xs, ys):
    h, w, _ = img.shape
    xs = np.clip(xs, 0, w - 1.001)
    ys = np.clip(ys, 0, h - 1.001)
    x0, y0 = xs.astype(np.int32), ys.astype(np.int32)
    fx, fy = (xs - x0)[..., None], (ys - y0)[..., None]
    a, b = img[y0, x0], img[y0, x0 + 1]
    c, d = img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=int, default=30)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--horizon", type=float, default=0.32)
    ap.add_argument("--crop-y", type=int, default=0)
    ap.add_argument("--strength", type=float, default=1.0)
    a = ap.parse_args()

    img = np.asarray(Image.open(a.image).convert("RGB"), dtype=np.float32) / 255.0
    H, W, _ = img.shape
    ch = int(round(W * 9 / 16))
    if a.crop_y + ch > H:
        sys.exit(f"crop of {ch}px from y={a.crop_y} exceeds image height {H}")
    T, fps, s = a.seconds, a.fps, a.strength
    if T % 30 and T % 10:
        sys.exit("--seconds should be a multiple of 10 so the wave periods divide the loop")

    yy, xx = np.mgrid[a.crop_y:a.crop_y + ch, 0:W].astype(np.float32)
    hz = a.horizon * H
    water = smoothstep((yy - hz) / (0.08 * H))
    depth = np.clip((yy - hz) / (H - hz), 0, 1) ** 1.2          # nearer water moves more
    sky = 1.0 - water
    cx, cy = W / 2, a.crop_y + ch / 2

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{ch}", "-r", str(fps), "-i", "-",
           "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-movflags", "+faststart", a.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    n = T * fps
    for i in range(n):
        t = i / n                                    # 0..1 over the loop
        tau = 2 * np.pi
        zoom = 1.0 + 0.012 * (1 - np.cos(tau * t)) / 2
        sx = cx + (xx - cx) / zoom
        sy = cy + (yy - cy) / zoom
        k_wave = T / 10                              # 10 s travelling wave
        k_surge = T / 6                              # 6 s side-to-side surge
        dy = water * s * (1.0 + 5.5 * depth) * np.sin(tau * k_wave * t - (yy - hz) / 46.0 + 0.7 * np.sin(xx / 120.0))
        dx = water * s * (0.6 + 3.2 * depth) * np.sin(tau * k_surge * t + (yy - hz) / 70.0 + xx / 260.0)
        dx = dx + sky * s * 1.1 * np.sin(tau * t + yy / 90.0)           # faint haze shimmer
        frame = sample(img, sx + dx, sy + dy)
        lum = frame @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
        foam = smoothstep((lum - 0.62) / 0.25)
        glint = 1.0 + 0.05 * s * water * foam * np.sin(tau * (T / 5) * t + xx / 55.0 - yy / 35.0)
        frame = np.clip(frame * glint[..., None], 0, 1)
        proc.stdin.write((frame * 255 + 0.5).astype(np.uint8).tobytes())
    proc.stdin.close()
    if proc.wait():
        sys.exit("ffmpeg failed")
    print(f"wrote {a.out} ({T}s loop, {fps} fps, 1920x1080)")


if __name__ == "__main__":
    main()
