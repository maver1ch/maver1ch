"""Generate GitHub profile banner PNG (1280x280) — brand-aligned with portfolio.

Run with the venv that has Pillow:
    ~/.claude/skills/.venv/bin/python3 scripts/build-banner.py

Outputs to assets/banner.png. Re-run after editing copy.
"""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BANNER_W = 1280
BANNER_H = 280
PAD_X = 90

BG_LIGHT = "#f8fafc"
ACCENT_PRIMARY = "#2563eb"
ACCENT_SECONDARY = "#0ea5e9"
ACCENT_TERTIARY = "#06b6d4"
TEXT_PRIMARY = "#0f172a"
TEXT_SECONDARY = "#475569"
TEXT_TERTIARY = "#94a3b8"

FONT_REG = "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"

OUT_PATH = "assets/banner.png"


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def gradient_bar(width: int, height: int, stops: list[str]) -> Image.Image:
    bar = Image.new("RGB", (width, height))
    pixels = bar.load()
    rgb = [hex_to_rgb(s) for s in stops]
    segments = len(rgb) - 1
    seg_w = width / segments
    for x in range(width):
        seg = min(int(x / seg_w), segments - 1)
        t = (x - seg * seg_w) / seg_w
        c1, c2 = rgb[seg], rgb[seg + 1]
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        for y in range(height):
            pixels[x, y] = (r, g, b)
    return bar


def main() -> None:
    img = Image.new("RGB", (BANNER_W, BANNER_H), BG_LIGHT)

    # Top brand bar
    bar = gradient_bar(BANNER_W, 6, [ACCENT_PRIMARY, ACCENT_SECONDARY, ACCENT_TERTIARY])
    img.paste(bar, (0, 0))

    # Soft accent orb on the right side
    orb_layer = Image.new("RGB", (BANNER_W, BANNER_H), BG_LIGHT)
    orb_draw = ImageDraw.Draw(orb_layer)
    cx, cy, r = int(BANNER_W * 0.85), int(BANNER_H * 0.55), 280
    orb_draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(199, 226, 255))
    orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(140))
    img = Image.blend(img, orb_layer, 0.55)

    # Secondary subtle accent in upper-left to keep balance
    orb2_layer = Image.new("RGB", (BANNER_W, BANNER_H), BG_LIGHT)
    orb2_draw = ImageDraw.Draw(orb2_layer)
    orb2_draw.ellipse([(-160, -140), (220, 220)], fill=(220, 232, 255))
    orb2_layer = orb2_layer.filter(ImageFilter.GaussianBlur(110))
    img = Image.blend(img, orb2_layer, 0.40)

    draw = ImageDraw.Draw(img)

    font_eyebrow = ImageFont.truetype(FONT_BOLD, 22)
    font_name = ImageFont.truetype(FONT_BOLD, 72)
    font_tagline = ImageFont.truetype(FONT_REG, 28)
    font_meta = ImageFont.truetype(FONT_BOLD, 18)

    # Eyebrow
    draw.text((PAD_X, 70), "AI FULL-STACK ENGINEER", fill=ACCENT_PRIMARY, font=font_eyebrow)

    # Name
    draw.text((PAD_X, 105), "Phuc Dam", fill=TEXT_PRIMARY, font=font_name)

    # Tagline
    draw.text(
        (PAD_X, 200),
        "Production Conversational AI  ·  RAG  ·  Multi-Agent  ·  Enterprise AWS",
        fill=TEXT_SECONDARY,
        font=font_tagline,
    )

    # Right-side meta chips (stacked) — small enterprise positioning signal
    chips = [
        ("FORTUNE 500 CLIENTS", ACCENT_PRIMARY, (228, 240, 255)),
        ("HANOI  ·  REMOTE", TEXT_SECONDARY, (235, 240, 248)),
    ]
    cx_anchor = BANNER_W - PAD_X
    cy_anchor = 90
    for text, fg, bg in chips:
        tw = draw.textlength(text, font=font_meta)
        pad_x, pad_y = 18, 10
        x1 = cx_anchor - tw - pad_x * 2
        y1 = cy_anchor
        x2 = cx_anchor
        y2 = y1 + 38
        draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=999, fill=bg)
        draw.text((x1 + pad_x, y1 + pad_y - 2), text, fill=fg, font=font_meta)
        cy_anchor += 50

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH, "PNG", optimize=True)
    print(f"wrote {OUT_PATH}  ({os.path.getsize(OUT_PATH) // 1024} KB)")


if __name__ == "__main__":
    main()
