#!/usr/bin/env python3
"""Original procedural animation of waves that rise, break, crash into whitewater and wash up a beach.

Nothing here is derived from any existing artwork: the scene (sky, headlands, sea, foam, sand) is drawn
from code, so the output is our own work. It is a stylized painterly look, not photorealism.

Waves are crest trains travelling toward the viewer. Each crest swells and steepens, throws a foam lip,
breaks into expanding whitewater, then collapses into a swash that runs up the sand. Breaking progresses
along the crest line, and spray droplets arc off each break. All motion is periodic in the loop length,
so the clip repeats seamlessly.

usage: procedural_waves.py --out waves_loop.mp4 [--seconds 30] [--seed 1] [--palette dusk|day]
         [--width 1280] [--workers 4] [--frames N]   (--frames N renders only N frames, for testing)
"""
import argparse
import multiprocessing as mp
import subprocess
import sys

import numpy as np

TAU = 2 * np.pi
P = {}  # per-run parameters shared with worker processes (set before forking)


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def make_tile(n, seed, beta):
    rng = np.random.default_rng(seed)
    fx = np.fft.fftfreq(n)
    f2 = fx[:, None] ** 2 + fx[None, :] ** 2
    f2[0, 0] = 1.0
    spec = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / f2 ** (beta / 2)
    spec[0, 0] = 0
    t = np.fft.ifft2(spec).real
    t = (t - t.mean()) / (t.std() * 4) + 0.5
    return np.clip(t, 0, 1).astype(np.float32)


def tsample(tile, x, y):
    n = tile.shape[0]
    x0, y0 = np.floor(x).astype(np.int32), np.floor(y).astype(np.int32)
    fx, fy = (x - x0).astype(np.float32), (y - y0).astype(np.float32)
    x0 %= n
    y0 %= n
    x1, y1 = (x0 + 1) % n, (y0 + 1) % n
    return (tile[y0, x0] * (1 - fx) + tile[y0, x1] * fx) * (1 - fy) + (tile[y1, x0] * (1 - fx) + tile[y1, x1] * fx) * fy


def box_blur(img, r):
    if r <= 0:
        return img
    out = img
    for axis in (0, 1):
        c = np.cumsum(np.pad(out, [(r + 1, r) if i == axis else (0, 0) for i in range(out.ndim)], mode="edge"), axis=axis)
        n = 2 * r + 1
        sl_hi = [slice(None)] * out.ndim
        sl_lo = [slice(None)] * out.ndim
        sl_hi[axis] = slice(n, None)
        sl_lo[axis] = slice(0, -n)
        out = (c[tuple(sl_hi)] - c[tuple(sl_lo)]) / n
    return out


PALETTES = {
    "dusk": dict(sky_top=(0.30, 0.36, 0.52), sky_hor=(0.88, 0.74, 0.72), far=(0.50, 0.52, 0.66), near=(0.07, 0.27, 0.36), shallow=(0.26, 0.58, 0.58), glint=(1.0, 0.86, 0.82),
                 dark=(0.03, 0.15, 0.24), turq=(0.17, 0.60, 0.64), refl=(0.58, 0.58, 0.72), foam=(0.97, 0.93, 0.92),
                 foam_sh=(0.66, 0.70, 0.82), sand=(0.55, 0.44, 0.38), wet=(0.30, 0.26, 0.30), hill1=(0.36, 0.38, 0.52),
                 hill2=(0.50, 0.50, 0.64)),
    "day": dict(sky_top=(0.55, 0.68, 0.82), sky_hor=(0.86, 0.90, 0.94), far=(0.52, 0.66, 0.76), near=(0.08, 0.40, 0.46), shallow=(0.40, 0.78, 0.72), glint=(1.0, 1.0, 0.95),
                dark=(0.04, 0.22, 0.30), turq=(0.20, 0.72, 0.72), refl=(0.66, 0.74, 0.84), foam=(0.98, 0.98, 0.98),
                foam_sh=(0.70, 0.80, 0.90), sand=(0.76, 0.66, 0.50), wet=(0.46, 0.40, 0.36), hill1=(0.42, 0.52, 0.56),
                hill2=(0.56, 0.64, 0.70)),
}


def setup(a):
    W = a.width
    H = W * 9 // 16
    pal = {k: np.array(v, dtype=np.float32) for k, v in PALETTES[a.palette].items()}
    rng = np.random.default_rng(a.seed)
    P.update(W=W, H=H, pal=pal, T=a.seconds, TRAV=a.seconds / 2.0, NC=4, seed=a.seed,
             noise_a=make_tile(512, a.seed + 1, 2.2), noise_b=make_tile(512, a.seed + 2, 1.5),
             noise_c=make_tile(256, a.seed + 3, 2.6),
             lat=[(rng.uniform(0, TAU), rng.uniform(0, TAU), rng.uniform(1.0, 1.8), rng.uniform(2.6, 3.6)) for _ in range(4)],
             YH=0.36, YS=0.86, C=0.5)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    P["xs"], P["ys"] = xs, ys
    P["u"] = xs / W
    P["yf"] = ys / H
    # sky and headlands (static except clouds)
    yf, u = P["yf"], P["u"]
    t = np.clip(yf / P["YH"], 0, 1)[..., None]
    P["sky0"] = pal["sky_top"] * (1 - t ** 0.8) + pal["sky_hor"] * t ** 0.8
    ridge = 0.012 * (tsample(P["noise_c"], P["xs"] * 0.35, np.zeros_like(xs)) - 0.5)
    hill_a = 0.115 * np.exp(-((u - 0.24) / 0.17) ** 2) + 0.035 * np.exp(-((u - 0.43) / 0.07) ** 2)
    hill_b = 0.045 * np.exp(-((u - 0.82) / 0.13) ** 2)
    P["hill_a_top"] = P["YH"] - hill_a + ridge
    P["hill_b_top"] = P["YH"] - hill_b + ridge * 0.6
    P["canvas"] = (1.0 + 0.035 * (tsample(P["noise_c"], xs * 1.7, ys * 1.7) - 0.5) +
                   0.02 * np.sin(xs * 1.9) * np.sin(ys * 1.9))[..., None].astype(np.float32)
    P["vig"] = (1.0 - 0.22 * (((u - 0.5) * 1.1) ** 2 + ((yf - 0.5) * 1.1) ** 2) ** 1.0)[..., None].astype(np.float32)


def crest_state(k, t):
    """Progress p in [0,1) of crest k along its journey, varying along the crest line (peeling break)."""
    u = P["u"]
    a1, a2, f1, f2 = P["lat"][k]
    lat = 0.03 * np.sin(TAU * f1 * u + a1) + 0.02 * np.sin(TAU * f2 * u + a2) + 0.10 * (u - 0.5)
    p = (t / P["TRAV"] + k / P["NC"] + lat) % 1.0
    return p


def wave_fields(d, t, detail):
    """Height, slope, and foam for sea points at world distance d. Returns dict of arrays."""
    D_FAR, D_SHORE = 1.0 / P["C"], 1.0 / (1 + P["C"])
    h = np.zeros_like(d)
    slope = np.zeros_like(d)
    foam = np.zeros_like(d)
    soft = np.zeros_like(d)
    face = np.zeros_like(d)
    swash = np.zeros_like(d)
    pb = 0.60
    for k in range(P["NC"]):
        p = crest_state(k, t)
        dc = D_FAR - p * (D_FAR - D_SHORE * 0.97)
        wob = 0.055 * (tsample(P["noise_c"], P["u"] * 420.0 + k * 53.0, p * 256.0 + k * 31.0) - 0.5)
        delta = d - dc + wob
        grow = smooth(0.02, 0.55, p)
        collapse = (1.0 - 0.72 * smooth(pb, pb + 0.22, p)) * (1.0 - smooth(0.80, 0.97, p))
        var = 0.55 + 0.9 * tsample(P["noise_c"], P["u"] * 150.0 + k * 91.0, p * 128.0)
        A = 0.075 * grow * collapse * var
        steep = smooth(0.22, pb, p)
        sg = 0.062
        sf = sg * (1.0 - 0.58 * steep)
        sb = sg * (1.0 + 0.9 * steep)
        side = np.where(delta < 0, sf, sb)
        g = np.exp(-(delta / side) ** 2)
        hk = A * g
        h += hk
        slope += hk * (-2 * delta / side ** 2)
        face = np.maximum(face, g * grow)
        if detail:
            ax = P["u"] * 520.0 / dc + k * 137.0
            ay = delta * 700.0 + k * 61.0
            nz = tsample(P["noise_a"], ax, ay)
            nz2 = tsample(P["noise_b"], ax * 1.9 + 31, ay * 1.9 + 17)
            lip_w = smooth(pb - 0.22, pb + 0.02, p)
            lip = lip_w * smooth(0.62, 0.95, g + 0.30 * (nz - 0.5)) * (1.0 - smooth(0.12, 0.30, p - pb))
            ap = np.clip((p - pb) / (1 - pb), 0.0, 1.0)
            Lw = 0.05 + 0.34 * ap ** 0.8
            geo = smooth(-Lw, -0.55 * Lw, delta) * (1.0 - smooth(0.02, 0.22, delta)) * smooth(pb, pb + 0.04, p)
            thr = 0.28 + 0.46 * ap
            nz3 = tsample(P["noise_c"], ax * 3.1 + 7, ay * 2.7 + 5)
            lace = smooth(thr - 0.07, thr + 0.07, 0.45 * nz + 0.35 * nz2 + 0.20 * nz3)
            ww = geo * lace * (1.0 - smooth(0.80, 0.99, p)) * (1.0 - 0.25 * ap)
            foam = np.maximum(foam, np.maximum(lip, ww))
            soft = np.maximum(soft, geo * (1.0 - smooth(0.82, 0.99, p)) * (0.30 + 0.25 * ap))
        q = np.where(p < 0.5, p + 1.0, p)
        swash += smooth(0.90, 0.99, q) * (1.0 - smooth(1.02, 1.22, q))
    return h, slope, foam, face, swash, soft


def render_frame(i):
    W, H, pal = P["W"], P["H"], P["pal"]
    n = P["nframes"]
    t = P["T"] * i / n
    YH, YS = P["YH"], P["YS"]
    D_FAR, D_SHORE = 1.0 / P["C"], 1.0 / (1 + P["C"])
    yf, u, xs = P["yf"], P["u"], P["xs"]

    # --- sky with drifting clouds (one tile width per loop => seamless)
    shift = (i / n) * 512.0
    cl = tsample(P["noise_a"], xs * 0.55 + shift, P["ys"] * 0.9 + 40)
    sky = P["sky0"] + (0.13 * (cl - 0.5) * (1.0 - np.clip(yf / YH, 0, 1) ** 2))[..., None] * np.array([1.0, 0.95, 1.0], dtype=np.float32)
    # --- headlands
    ha = smooth(-0.004, 0.004, yf - P["hill_a_top"])
    hb = smooth(-0.003, 0.003, yf - P["hill_b_top"])
    haze = smooth(P["hill_a_top"] - 0.02, P["hill_a_top"] + 0.07, yf)[..., None]
    col_b = pal["hill2"] * (1 - 0.25 * haze) + pal["sky_hor"] * 0.25 * haze
    col_a = pal["hill1"] * (1 - 0.35 * haze) + pal["sky_hor"] * 0.35 * haze
    sky = sky * (1 - hb[..., None]) + col_b * hb[..., None]
    sky = sky * (1 - ha[..., None]) + col_a * ha[..., None]
    mist = np.exp(-(((yf - YH) / 0.03) ** 2))[..., None] * 0.22
    sky = sky * (1 - mist) + pal["sky_hor"] * mist

    # --- sea: two-step inverse of the vertical displacement caused by wave height
    yg = P["ys"].copy()
    for _ in range(2):
        yn = np.clip((yg / H - YH) / (YS - YH), 0.0, 1.6)
        d = 1.0 / (yn + P["C"])
        h, *_ = wave_fields(d, t, False)
        yg = P["ys"] + h * (1.25 * H) / d
    yn = np.clip((yg / H - YH) / (YS - YH), 0.0, 1.6)
    d = 1.0 / (yn + P["C"])
    h, slope, foam, face, swash, soft = wave_fields(d, t, True)

    depth = np.clip((D_FAR - d) / (D_FAR - D_SHORE), 0, 1.2)[..., None]
    dm = np.clip(depth[..., 0], 0, 1)
    shal = smooth(0.78, 1.05, depth[..., 0])[..., None]
    base = pal["far"] * (1 - dm[..., None]) + pal["near"] * dm[..., None]
    base = base * (1 - shal) + pal["shallow"] * shal * (0.85 + 0.3 * (tsample(P["noise_b"], xs * 0.4, yg * 0.7) - 0.5))[..., None]
    shift = (t / P["TRAV"]) * (D_FAR - D_SHORE) * 192.0
    rip = tsample(P["noise_c"], xs * 0.55, d * 192.0 + shift) - 0.5
    rip2 = tsample(P["noise_b"], xs * 0.9 + 100, d * 384.0 + 2 * shift) - 0.5
    nl = np.clip(slope * 1.8 + 0.35 * rip, -1, 1)
    hn = np.clip(face * 1.1 + 0.25 * rip2, 0, 1.2)
    wf = (smooth(0.02, 0.35, nl) * (0.25 + 0.75 * np.clip(depth[..., 0], 0, 1)))[..., None]
    wb = (smooth(0.02, 0.45, -nl) * 0.6)[..., None]
    front = pal["dark"] * (1 - smooth(0.35, 0.98, hn)[..., None]) + pal["turq"] * smooth(0.35, 0.98, hn)[..., None]
    sea = base * (1 - wf * 0.95) + front * wf * 0.95
    sea = sea * (1 - wb) + pal["refl"] * wb
    streak = tsample(P["noise_c"], xs * 0.12 + 9, P["ys"] * 2.8)
    sea = sea * (1.0 + 0.22 * (streak - 0.5))[..., None]
    shade = (0.58 + 0.42 * tsample(P["noise_a"], xs * 0.9, yg * 1.5 + 2 * shift))[..., None]
    foamcol = pal["foam"] * shade + pal["foam_sh"] * (1 - shade) * 0.9
    sea = sea * (1 - soft[..., None]) + (pal["shallow"] * 0.5 + foamcol * 0.5) * soft[..., None]
    fa = np.clip(foam * 1.15, 0, 1)[..., None]
    sea = sea * (1 - fa) + foamcol * fa
    gl = (smooth(0.84, 0.97, tsample(P["noise_b"], xs * 1.6 + 7, d * 520.0 + 3 * shift)) *
          smooth(0.42, 0.68, tsample(P["noise_a"], xs * 0.45 + 200, d * 150.0 + shift)) *
          smooth(0.0, 0.5, -nl + 0.2) * (1 - fa[..., 0]))
    sea = sea + pal["glint"] * (0.35 * gl * (0.3 + 0.7 * (1 - dm)))[..., None]

    # --- shoreline and sand
    sw = (swash / max(1, 1) * 0.045) * (0.6 + 0.4 * np.sin(TAU * (u * 2.3) + 1.0))
    ysw = YS + sw
    sandt = np.clip((yf - ysw) / (1.0 - YS), 0, 1)[..., None]
    wetness = np.exp(-np.clip(yf - ysw, 0, None) / 0.035)[..., None]
    sand = pal["sand"] * (1 - 0.15 * sandt) * (1 - wetness) + pal["wet"] * wetness
    sand = sand + pal["refl"] * 0.18 * wetness * smooth(0.0, 0.03, yf - ysw)[..., None]
    edge = np.exp(-(((yf - ysw) / 0.006) ** 2))
    lacy = smooth(0.35, 0.75, tsample(P["noise_b"], xs * 1.3 + 5 * i * 0, yg * 2.0 + 90))
    sea_w = smooth(-0.003, 0.003, ysw - yf)[..., None]
    land = sand * (1 - (edge * lacy)[..., None]) + foamcol * (edge * lacy)[..., None]
    water = sea * sea_w + land * (1 - sea_w)

    # --- compose: sky above the visible sea
    visible_sea = smooth(YH - 0.004, YH + 0.004, yg / H)[..., None]
    out = sky * (1 - visible_sea) + water * visible_sea

    # --- spray: droplets arcing off each break
    spray = np.zeros((H, W), dtype=np.float32)
    rng = np.random.default_rng(P["seed"] * 1000 + 7)
    pb = 0.60
    for k in range(P["NC"]):
        for c in range(14):                       # 14 break points spread along the crest line
            uc = (c + rng.uniform(0.1, 0.9)) / 14.0
            a1, a2, f1, f2 = P["lat"][k]
            lat = 0.03 * np.sin(TAU * f1 * uc + a1) + 0.02 * np.sin(TAU * f2 * uc + a2) + 0.10 * (uc - 0.5)
            p = (t / P["TRAV"] + k / P["NC"] + lat) % 1.0
            age = (p - pb) * P["TRAV"]            # seconds since this point broke
            dcn = D_FAR - pb * (D_FAR - D_SHORE * 0.97)
            ycn = (1.0 / dcn - P["C"]) * (YS - YH) + YH
            for j in range(9):
                vx, vy = rng.uniform(-0.05, 0.05), rng.uniform(0.18, 0.42)
                delay = rng.uniform(0.0, 0.5)
                a = age - delay
                if a < 0 or a > 1.6:
                    continue
                size = max(1, int(round(W / 640.0 * (1 + 1.6 * rng.random()))))
                px = int((uc + vx * a) * W)
                py = int((ycn - (vy * a - 0.55 * a * a) * 0.25 - 0.04 * (1 - np.exp(-a * 3))) * H)
                if 0 <= px < W - 2 and 0 <= py < H - 2:
                    spray[py:py + size, px:px + size] = np.maximum(spray[py:py + size, px:px + size], 0.95 * (1 - a / 1.6))
    out = out * (1 - spray[..., None] * 0.9) + pal["foam"] * spray[..., None] * 0.9

    # --- painterly finish: soft blur, canvas texture, vignette
    out = 0.40 * out + 0.60 * box_blur(out, 1)
    out = out * P["canvas"] * P["vig"]
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=int, default=30)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--palette", choices=sorted(PALETTES), default="dusk")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--frames", type=int, help="render only this many frames (testing)")
    ap.add_argument("--frame-at", type=float, help="write one PNG frame at this time (s) to --out and exit")
    a = ap.parse_args()
    if a.seconds % 2:
        sys.exit("--seconds must be even (crest period divides the loop)")
    setup(a)
    P["nframes"] = a.seconds * a.fps
    if a.frame_at is not None:
        from PIL import Image
        i = int(a.frame_at * a.fps)
        raw = render_frame(i)
        Image.frombytes("RGB", (P["W"], P["H"]), raw).save(a.out)
        print(f"wrote {a.out} (t={a.frame_at}s)")
        return
    total = a.frames or P["nframes"]
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{P['W']}x{P['H']}", "-r", str(a.fps), "-i", "-",
           "-vf", "scale=1920:1080:flags=lanczos,format=yuv420p",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-movflags", "+faststart", a.out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with mp.get_context("fork").Pool(a.workers) as pool:
        for n, frame in enumerate(pool.imap(render_frame, range(total), chunksize=2)):
            proc.stdin.write(frame)
            if n % 100 == 0:
                print(f"frame {n}/{total}", flush=True)
    proc.stdin.close()
    if proc.wait():
        sys.exit("ffmpeg failed")
    print(f"wrote {a.out} ({a.seconds}s loop at {a.fps} fps)")


if __name__ == "__main__":
    main()
