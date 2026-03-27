#!/usr/bin/env python3
"""
Compose 45 pages of Stella & Yakob in a given language.
Format: 8.5×8.5" square @ 300 DPI = 2550×2550 px
Illustrations from: /home/user/workspace/stella-and-yakob-repo/illustrations/v2_p{N:02d}.png

Usage: python3 compose_lang_v3.py <lang_code>
  e.g. python3 compose_lang_v3.py pl
"""

import sys, os
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) < 2:
    print("Usage: compose_lang_v3.py <lang_code>")
    sys.exit(1)

LANG = sys.argv[1].lower()

# ── Constants ──────────────────────────────────────────────────────────────────
PX           = 2550          # 8.5" × 300 DPI
BG           = (251, 249, 244)
INK          = (42, 30, 18)

ILL_ZONE_H   = 1904          # illustration occupies top 1904px (74.7%)
TEXT_ZONE_Y  = ILL_ZONE_H
TEXT_ZONE_H  = PX - ILL_ZONE_H  # = 646 px

FONT_PATH    = "/home/user/workspace/Lora-Italic.ttf"
FONT_SIZE    = 72
LINE_EXTRA   = 28

ILL_DIR      = "/home/user/workspace/stella-and-yakob-repo/illustrations"
OUT_DIR      = f"/home/user/workspace/book_pages_{LANG}"

os.makedirs(OUT_DIR, exist_ok=True)

# ── Font ───────────────────────────────────────────────────────────────────────
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
bb_ref = font.getbbox("Ag")
LH = (bb_ref[3] - bb_ref[1]) + LINE_EXTRA

# ── Load page text ─────────────────────────────────────────────────────────────
sys.path.insert(0, "/home/user/workspace")
mod = __import__(f"book_text_{LANG}_v3")
PAGES = mod.PAGES
print(f"Loaded {len(PAGES)} pages for language '{LANG}'")

# ── Illustration loader ────────────────────────────────────────────────────────
def paste_illustration(page_rgba, page_num):
    """
    Load v2_p{N}.png, scale to fill ILL_ZONE_H × PX, paste into page.
    Cycles if page_num > 45 (shouldn't happen).
    """
    ill_path = os.path.join(ILL_DIR, f"v2_p{page_num:02d}.png")
    if not os.path.exists(ill_path):
        # Try cyclic fallback using available range 01-45
        alt_num = ((page_num - 1) % 45) + 1
        ill_path = os.path.join(ILL_DIR, f"v2_p{alt_num:02d}.png")
        if not os.path.exists(ill_path):
            print(f"  WARNING: No illustration for page {page_num}, skipping illustration")
            return

    ill = Image.open(ill_path).convert("RGBA")
    iw, ih = ill.size

    # Scale to fill ILL_ZONE — fill width, crop if slightly over height
    scale = max(PX / iw, ILL_ZONE_H / ih)
    scale_fit = min(PX / iw, ILL_ZONE_H / ih)
    if scale / scale_fit > 1.15:
        scale = scale_fit * 1.10

    nw = int(iw * scale)
    nh = int(ih * scale)
    ill = ill.resize((nw, nh), Image.LANCZOS)

    x = (PX - nw) // 2
    y = max(0, (ILL_ZONE_H - nh) // 2)

    if nh > ILL_ZONE_H:
        crop_top = nh - ILL_ZONE_H
        ill = ill.crop((0, crop_top, nw, nh))
        nh = ILL_ZONE_H
        y = 0

    page_rgba.paste(ill, (x, y), ill)

# ── Draw centered text block ───────────────────────────────────────────────────
def draw_text_centered(draw, lines):
    """Draw lines of text, centered horizontally, in text zone."""
    visible = [l for l in lines if l != ""]
    gaps    = lines.count("")

    total_h = len(visible) * LH + gaps * (LH // 2)

    margin_top = (TEXT_ZONE_H - total_h) // 2
    y = TEXT_ZONE_Y + max(margin_top, 40)

    for line in lines:
        if line == "":
            y += LH // 2
            continue
        bb = font.getbbox(line)
        tw = bb[2] - bb[0]
        x = (PX - tw) // 2
        draw.text((x, y), line, font=font, fill=INK)
        y += LH

# ── Thin separator line ────────────────────────────────────────────────────────
def draw_separator(draw):
    pad = int(PX * 0.15)
    draw.line(
        [(pad, ILL_ZONE_H + 15), (PX - pad, ILL_ZONE_H + 15)],
        fill=(195, 182, 162, 180),
        width=2
    )

# ── Compose each page ──────────────────────────────────────────────────────────
for page_num, lines in PAGES:
    page = Image.new("RGBA", (PX, PX), BG + (255,))
    paste_illustration(page, page_num)
    draw = ImageDraw.Draw(page)
    draw_separator(draw)
    draw_text_centered(draw, lines)

    out_path = os.path.join(OUT_DIR, f"page_{page_num:02d}.png")
    page.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"  ✓ page {page_num:02d}")

print(f"\nDone. {len(PAGES)} pages → {OUT_DIR}/")
