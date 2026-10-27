#!/usr/bin/env python3
"""Make a dark, minimal 1280x720 thumbnail (and a matching 1920x1080 video still).

usage: make_thumbnail.py --text "A Winter Night in a Medieval Village" --sub "Calm History for Sleep"
         --out thumb.jpg [--art period_art.jpg] [--seed 1] [--still still.jpg]

With --art (period-accurate, properly licensed or own image) the art is darkened and used as the
background. Without it, a gradient sky with stars is drawn. Vary --seed per video. Keep artwork
accurate for the era; anachronistic visuals are a known complaint about AI history channels.
"""
import argparse
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def sky(w, h, seed):
    rnd = random.Random(seed)
    top = (rnd.randint(8, 18), rnd.randint(12, 24), rnd.randint(30, 52))
    bot = (rnd.randint(2, 8), rnd.randint(2, 8), rnd.randint(8, 16))
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    d = ImageDraw.Draw(img)
    for _ in range(int(w * h / 4500)):
        x, y = rnd.randrange(w), rnd.randrange(int(h * 0.7))
        b = rnd.randint(90, 200)
        r = rnd.choice([1, 1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 15)))
    mx, my, mr = int(w * rnd.uniform(0.72, 0.88)), int(h * rnd.uniform(0.15, 0.3)), int(h * 0.07)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(222, 222, 205))
    d.ellipse([mx - mr + int(mr * 0.45), my - mr - 4, mx + mr + int(mr * 0.45), my + mr - 4], fill=(10, 14, 28))
    return img.filter(ImageFilter.GaussianBlur(0.6))


def background(w, h, art, seed):
    if not art:
        return sky(w, h, seed)
    img = Image.open(art).convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    img = img.crop((left, top, left + w, top + h))
    img = ImageEnhance.Brightness(img).enhance(0.45)
    return ImageEnhance.Color(img).enhance(0.8)


def draw_text(img, text, sub):
    w, h = img.size
    d = ImageDraw.Draw(img)
    size = int(h * 0.105)
    font = ImageFont.truetype(FONT_BOLD, size)
    lines = textwrap.wrap(text, width=18)[:3]
    while any(d.textlength(ln, font=font) > w * 0.84 for ln in lines) and size > 24:
        size -= 3
        font = ImageFont.truetype(FONT_BOLD, size)
    y = int(h * 0.42)
    for ln in lines:
        d.text((int(w * 0.07) + 2, y + 2), ln, font=font, fill=(0, 0, 0))
        d.text((int(w * 0.07), y), ln, font=font, fill=(236, 232, 220))
        y += int(size * 1.2)
    sfont = ImageFont.truetype(FONT_REG, int(h * 0.045))
    d.text((int(w * 0.07), y + int(h * 0.03)), sub, font=sfont, fill=(160, 170, 190))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--sub", default="Calm History for Sleep")
    ap.add_argument("--out", required=True)
    ap.add_argument("--art")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--still", help="also write a 1920x1080 text-free still for the video itself")
    a = ap.parse_args()

    thumb = background(1280, 720, a.art, a.seed)
    draw_text(thumb, a.text, a.sub)
    thumb.save(a.out, quality=88)
    size_kb = Path(a.out).stat().st_size // 1024
    print(f"wrote {a.out} ({size_kb} KB)")
    if a.still:
        background(1920, 1080, a.art, a.seed).save(a.still, quality=88)
        print(f"wrote {a.still}")


if __name__ == "__main__":
    main()
