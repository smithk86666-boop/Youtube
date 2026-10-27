#!/usr/bin/env python3
"""Animate the water in a painting or photo, keeping masked-out parts (boats, shore, sky) still.

Painted water is made to move in four ways, all periodic in the loop length (seamless):
  1. flow: paint advects from the horizon toward the viewer and shore, faster in the foreground,
     using two cross-faded phases so the motion never snaps back
  2. heave: crest bands travel toward the shore and lift and lower the surface
  3. churn: small drifting turbulence displaces the foam so it boils
  4. surge: foam highlights pulse as each swell passes
The sky sways very slightly. This works on art you have the rights to use; see docs/art-sourcing.md.

usage: animate_water_art.py --image art.png --mask water_mask.png --out loop.mp4 --horizon-y 535
         [--crop-y 170] [--seconds 30] [--fps 24] [--flow 90] [--heave 9] [--churn 3.5] [--workers 4]
--horizon-y  source row of the horizon; --crop-y  top row of the 16:9 crop (full width is kept)
"""
import argparse
import multiprocessing as mp
import subprocess
import sys

import numpy as np
from PIL import Image

P = {}
TAU = 2 * np.pi


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def make_tile(n, seed, beta=2.0):
    rng = np.random.default_rng(seed)
    fx = np.fft.fftfreq(n)
    f2 = fx[:, None] ** 2 + fx[None, :] ** 2
    f2[0, 0] = 1.0
    spec = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / f2 ** (beta / 2)
    spec[0, 0] = 0
    t = np.fft.ifft2(spec).real
    return np.clip((t - t.mean()) / (t.std() * 4) + 0.5, 0, 1).astype(np.float32)


def tsample(tile, x, y):
    n = tile.shape[0]
    x0, y0 = np.floor(x).astype(np.int32), np.floor(y).astype(np.int32)
    fx, fy = (x - x0).astype(np.float32), (y - y0).astype(np.float32)
    x0 %= n
    y0 %= n
    x1, y1 = (x0 + 1) % n, (y0 + 1) % n
    return (tile[y0, x0] * (1 - fx) + tile[y0, x1] * fx) * (1 - fy) + (tile[y1, x0] * (1 - fx) + tile[y1, x1] * fx) * fy


def mirror(v, hi):
    """Reflect coordinates at the borders instead of clamping, so edges do not streak."""
    per = 2 * hi
    m = np.mod(v, per)
    return np.where(m > hi, per - m, m)


def sample(img, xs, ys):
    h, w, _ = img.shape
    xs = mirror(xs, w - 1.001)
    ys = mirror(ys, h - 1.001)
    x0, y0 = xs.astype(np.int32), ys.astype(np.int32)
    fx, fy = (xs - x0)[..., None], (ys - y0)[..., None]
    a, b = img[y0, x0], img[y0, x0 + 1]
    c, d = img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def frame(i):
    img, mask, yy, xx = P["img"], P["mask"], P["yy"], P["xx"]
    n, T = P["n"], P["T"]
    t = i / n                                   # 0..1 across the loop
    secs = T * t
    hy, bot = P["hy"], P["bot"]
    depth = np.clip((yy - hy) / (bot - hy), 0, 1)
    M = mask

    # heave and churn displace where we look up the paint
    lam, per = P["lam"], P["wave_period"]
    heave = P["heave"] * (0.25 + 0.75 * depth) * np.sin(TAU * (secs / per - (yy - hy) / lam + 0.35 * np.sin(xx / 210.0)))
    shiftc = t * 512.0 * 3                      # three tile widths per loop => seamless
    cx = tsample(P["noise"], xx * 0.045 + shiftc, yy * 0.045) - 0.5
    cy = tsample(P["noise"], xx * 0.045 + 211 - shiftc * 0.7, yy * 0.045 + 97) - 0.5
    churn = P["churn"] * (0.4 + 0.6 * depth)
    dx = M * (churn * 2 * cx + 0.5 * heave * np.sin(TAU * secs / (per * 1.5) + yy / 90.0))
    dy = M * (heave + churn * 2 * cy)

    # flow: two cross-faded phases of paint moving toward the viewer
    cyc = P["cycle"]
    ph0 = (secs / cyc) % 1.0
    jitter = 0.30 * (tsample(P["noise"], xx * 0.012, yy * 0.012) - 0.5)
    out = np.zeros_like(img[:1].repeat(yy.shape[0], 0)[:, : yy.shape[1]])
    wsum = 0
    for off in (0.0, 0.5):
        ph = (ph0 + off + jitter) % 1.0
        w = (1 - np.abs(2 * ph - 1))[..., None]
        dist = P["flow"] * (0.15 + 0.85 * depth ** 1.2) * M
        sx = xx + dx - P["dir"][0] * dist * ph
        sy = yy + dy - P["dir"][1] * dist * ph
        out = out + sample(img, sx, sy) * w
        wsum = wsum + w
    out = out / np.maximum(wsum, 1e-3)

    # foam surge: highlights pulse as each swell passes
    lum = out @ np.array([0.299, 0.587, 0.114], dtype=np.float32)
    foam = smooth(0.55, 0.85, lum)
    pulse = 1.0 + 0.07 * np.sin(TAU * (secs / per - (yy - hy) / lam + xx / 520.0))
    out = out * (1 + ((pulse - 1) * foam * M)[..., None])

    # sky sways very slightly (outside the water mask)
    sky = (1 - M) * (yy < hy + 6)
    sway = 2.5 * np.sin(TAU * t)
    if sway:
        out_sky = sample(img, xx + sway * 0.6, yy)
        out = out * (1 - sky[..., None]) + out_sky * sky[..., None]
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--mask", required=True, help="white = water that may move; black = still")
    ap.add_argument("--out", required=True)
    ap.add_argument("--horizon-y", type=float, required=True)
    ap.add_argument("--crop-y", type=int, default=0)
    ap.add_argument("--seconds", type=int, default=30)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--flow", type=float, default=90.0, help="px the paint travels per flow cycle in the foreground")
    ap.add_argument("--cycle", type=float, default=10.0, help="seconds per flow cycle (must divide --seconds)")
    ap.add_argument("--wave-period", type=float, default=5.0, help="seconds between swells (must divide --seconds)")
    ap.add_argument("--heave", type=float, default=9.0, help="px of swell lift in the foreground")
    ap.add_argument("--churn", type=float, default=3.5, help="px of foam turbulence")
    ap.add_argument("--direction", default="-0.2,1.0", help="flow direction x,y (toward the viewer is +y)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--frames", type=int)
    ap.add_argument("--frame-at", type=float, help="write one PNG at this time (s) and exit")
    a = ap.parse_args()
    for v, nm in ((a.cycle, "--cycle"), (a.wave_period, "--wave-period")):
        if a.seconds % v:
            sys.exit(f"{nm} must divide --seconds")

    img = np.asarray(Image.open(a.image).convert("RGB"), dtype=np.float32) / 255.0
    H, W, _ = img.shape
    ch = int(round(W * 9 / 16))
    if a.crop_y + ch > H:
        sys.exit(f"crop of {ch}px from y={a.crop_y} exceeds image height {H}")
    mk = np.asarray(Image.open(a.mask).convert("L"), dtype=np.float32) / 255.0
    if mk.shape != (H, W):
        sys.exit("mask must be the same size as the image")
    yy, xx = np.mgrid[a.crop_y:a.crop_y + ch, 0:W].astype(np.float32)
    dvec = np.array([float(x) for x in a.direction.split(",")], dtype=np.float32)
    dvec = dvec / np.linalg.norm(dvec)
    P.update(img=img, mask=mk[a.crop_y:a.crop_y + ch], yy=yy, xx=xx, n=a.seconds * a.fps, T=a.seconds,
             hy=a.horizon_y, bot=float(a.crop_y + ch), flow=a.flow, cycle=a.cycle, wave_period=a.wave_period,
             heave=a.heave, churn=a.churn, dir=dvec, lam=150.0, noise=make_tile(512, 5))
    if a.frame_at is not None:
        Image.frombytes("RGB", (W, ch), frame(int(a.frame_at * a.fps))).save(a.out)
        print(f"wrote {a.out}")
        return
    total = a.frames or P["n"]
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{ch}", "-r", str(a.fps), "-i", "-",
           "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-movflags", "+faststart", a.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with mp.get_context("fork").Pool(a.workers) as pool:
        for k, fr in enumerate(pool.imap(frame, range(total), chunksize=2)):
            proc.stdin.write(fr)
            if k % 120 == 0:
                print(f"frame {k}/{total}", flush=True)
    proc.stdin.close()
    if proc.wait():
        sys.exit("ffmpeg failed")
    print(f"wrote {a.out} ({a.seconds}s loop, {a.fps} fps, 1920x1080)")


if __name__ == "__main__":
    main()
