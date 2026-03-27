#!/usr/bin/env python3
"""
Compose all 30 pages of Stella & Yakob v2 in 8.5x8.5" square format @ 300 DPI.
= 2550 x 2550 px

Layout:
- Full page: 2550 x 2550 px, cream background
- Illustration zone: top 1680 px (66%) — centered, no bleed into text
- Thin decorative rule: a single hairline at y=1680 (very subtle)
- Text zone: bottom 870 px — centered text, generous leading
- No overlap between illustration and text whatsoever

Typography:
- Font: Lora Italic, 72pt (= 96 px at 300dpi / scaled for 2550px canvas)
- Leading: 38px extra
- Text centered horizontally, anchored at top of text zone + 60px margin
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

# ── Constants ──────────────────────────────────────────────────────────────────
PX           = 2550          # 8.5" × 300 DPI
BG           = (251, 249, 244)        # warm cream
INK          = (42, 30, 18)           # warm dark brown, full opacity
MUTED        = (100, 90, 75)          # for lighter elements

ILL_ZONE_H   = 1680          # illustration occupies top 1680px (65.9%)
TEXT_ZONE_Y  = ILL_ZONE_H    # text starts here
TEXT_ZONE_H  = PX - ILL_ZONE_H       # = 870 px

FONT_SIZE    = 78            # comfortable reading size for children's book
FONT_PATH    = "/home/user/workspace/Lora-Italic.ttf"
LINE_EXTRA   = 32            # extra leading

OUT_DIR      = "/home/user/workspace/book_pages_square"
ILL_DIR      = "/home/user/workspace"

os.makedirs(OUT_DIR, exist_ok=True)

# ── Font ───────────────────────────────────────────────────────────────────────
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

def lh():
    bb = font.getbbox("Ag")
    return (bb[3] - bb[1]) + LINE_EXTRA

LH = lh()

# ── Fit illustration into ILL_ZONE (centered, letterboxed, no crop) ────────────
def paste_illustration(page_rgba, ill_path):
    """
    Load illustration, fit inside ILL_ZONE_H × PX (centered, maintain aspect).
    No fade — clean separation at ILL_ZONE_H line.
    """
    ill = Image.open(ill_path).convert("RGBA")
    iw, ih = ill.size

    # Scale to fill ILL_ZONE — fill width, crop if slightly over height
    scale = max(PX / iw, ILL_ZONE_H / ih)
    # But don't exceed more than 15% crop on either axis
    scale_fit = min(PX / iw, ILL_ZONE_H / ih)
    if scale / scale_fit > 1.15:
        scale = scale_fit * 1.10
    nw = int(iw * scale)
    nh = int(ih * scale)
    ill = ill.resize((nw, nh), Image.LANCZOS)

    # Center both horizontally and vertically in ill zone
    x = (PX - nw) // 2
    y = max(0, (ILL_ZONE_H - nh) // 2)  # vertically centered

    # Crop if taller than zone
    if nh > ILL_ZONE_H:
        # Crop from top to fit, keeping bottom
        crop_top = nh - ILL_ZONE_H
        ill = ill.crop((0, crop_top, nw, nh))
        nh = ILL_ZONE_H
        y = 0

    page_rgba.paste(ill, (x, y), ill)

# ── Draw centered text block ───────────────────────────────────────────────────
def draw_text_centered(draw, lines):
    """Draw lines of text, centered horizontally, in text zone."""
    # Calculate total block height to vertically center it
    visible = [l for l in lines if l != ""]
    gaps    = lines.count("")

    total_h = len(visible) * LH + gaps * (LH // 2)

    # Start y: center the block in the text zone
    margin_top = (TEXT_ZONE_H - total_h) // 2
    y = TEXT_ZONE_Y + max(margin_top, 55)  # at least 55px padding from separator

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
        [(pad, ILL_ZONE_H + 18), (PX - pad, ILL_ZONE_H + 18)],
        fill=(195, 182, 162, 180),
        width=2
    )

# ── Import page text ──────────────────────────────────────────────────────────
sys.path.insert(0, "/home/user/workspace")
from book_text_fr_v2 import PAGES

# ── Compose ───────────────────────────────────────────────────────────────────
for page_num, lines in PAGES:
    ill_path = os.path.join(ILL_DIR, f"v2_p{page_num:02d}.png")
    if not os.path.exists(ill_path):
        print(f"  SKIP p{page_num:02d} — illustration not found")
        continue

    # Blank cream page
    page = Image.new("RGBA", (PX, PX), BG + (255,))

    # Illustration
    paste_illustration(page, ill_path)

    # Draw elements
    draw = ImageDraw.Draw(page)
    draw_separator(draw)
    draw_text_centered(draw, lines)

    out_path = os.path.join(OUT_DIR, f"page_{page_num:02d}.png")
    page.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"  ✓ page {page_num:02d}")

print("\nDone.")
