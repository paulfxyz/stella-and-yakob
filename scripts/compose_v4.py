#!/usr/bin/env python3
"""
compose_v4.py — Definitive compositor for Stella & Yakob v5.0
==============================================================
Format : 8.5 × 8.5 in  @  300 DPI  =  2550 × 2550 px
Layout :
  ┌──────────────────────────────────┐
  │  [margin_top px of cream]        │
  │  Illustration  (fit inside zone) │
  │  [gap between ill + text]        │
  │  Thin separator line             │
  │  [gap]                           │
  │  Text block  (centred)           │
  │  [padding_bottom px of cream]    │
  └──────────────────────────────────┘

Key improvements over v3:
  • New watercolour illustrations (new_p{N:02d}.png) — falls back to v2_
  • Explicit MARGIN_TOP so illustration never touches the top edge
  • GAP_BELOW_ILL separates illustration from separator line
  • Text zone starts further down → clear breathing room
  • Single font size (FONT_SIZE) + per-language overrides
  • Lora Regular for non-italic lines (line starts with normal text)
  • Lora Italic for poetic/dialogue lines (line starts with " or —)
  • RTL support for ar / he
  • Script-specific fonts for ar, he, zh, ja, hi, ne

Usage:
    python3 compose_v4.py <lang_code>  [--new-only]
    python3 compose_v4.py en
    python3 compose_v4.py ar
"""

import sys, os
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) < 2:
    print("Usage: compose_v4.py <lang_code>")
    sys.exit(1)

LANG = sys.argv[1].lower()

# ── Canvas ─────────────────────────────────────────────────────────────────────
PX              = 2550                   # square page side
BG              = (251, 249, 244)        # warm cream
INK             = (42, 30, 18)          # near-black warm

# ── Layout constants (all in pixels @ 300 DPI) ────────────────────────────────
MARGIN_TOP      = 60                    # cream above illustration
MARGIN_SIDE     = 80                    # illustration horizontal inset
GAP_BELOW_ILL   = 48                    # space between illustration bottom and separator
SEP_THICKNESS   = 2                     # separator line weight
GAP_ABOVE_TEXT  = 40                    # space between separator and first text line
PADDING_BOTTOM  = 60                    # cream below text block

# Derived: illustration fits within this zone
ILL_MAX_W       = PX - 2 * MARGIN_SIDE
ILL_MAX_H       = 1800                  # max illustration height (leaves ~690px for text)

# ── Font configuration ─────────────────────────────────────────────────────────
WS = "/home/user/workspace"

FONT_CONFIGS = {
    # lang : (regular_path, italic_path, size, rtl)
    "default" : (f"{WS}/Lora.ttf",              f"{WS}/Lora-Italic.ttf",        68, False),
    "ar"      : (f"{WS}/fonts_extra/Amiri-Regular.ttf",
                 f"{WS}/fonts_extra/Amiri-Regular.ttf",  76, True),
    "he"      : ("/usr/share/fonts/truetype/noto/NotoSerifHebrew-Regular.ttf",
                 "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Regular.ttf", 74, True),
    "zh"      : ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",
                 "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",     70, False),
    "ja"      : ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",
                 "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",     70, False),
    "hi"      : (f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",
                 f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",                70, False),
    "ne"      : (f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",
                 f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",                70, False),
}

def get_font_cfg(lang):
    return FONT_CONFIGS.get(lang, FONT_CONFIGS["default"])

reg_path, ital_path, FONT_SIZE, RTL = get_font_cfg(LANG)

# Load fonts — fall back gracefully
def load_font(path, size):
    try:
        # NotoSerifCJK needs index=0
        if path.endswith(".otc"):
            return ImageFont.truetype(path, size, index=0)
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"  ⚠ font load failed ({path}): {e} — using default")
        return ImageFont.truetype(f"{WS}/Lora-Italic.ttf", size)

font_reg  = load_font(reg_path,  FONT_SIZE)
font_ital = load_font(ital_path, FONT_SIZE)

# Line height
_bb = font_reg.getbbox("Ag")
LINE_H = (_bb[3] - _bb[1]) + 26      # 26 px inter-line breathing room
HALF_BREAK = LINE_H // 2             # blank line height

# ── Paths ──────────────────────────────────────────────────────────────────────
ILL_DIR_NEW = WS                      # new_p{N:02d}.png lives here
ILL_DIR_OLD = f"{WS}/stella-and-yakob-repo/illustrations"
OUT_DIR     = f"{WS}/book_pages_{LANG}_v4"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load page text ─────────────────────────────────────────────────────────────
sys.path.insert(0, WS)
mod   = __import__(f"book_text_{LANG}_v3")
PAGES = mod.PAGES
print(f"Loaded {len(PAGES)} pages for '{LANG}'")

# ── Illustration loader ────────────────────────────────────────────────────────
# Canonical illustration dimensions (landscape, all new illustrations)
ILL_CANONICAL_W = 1536
ILL_CANONICAL_H = 1024

def load_illustration(page_num):
    """Try new_p{N}.png first, fall back to v2_p{N}.png.
    Always normalises to landscape orientation."""
    new_path = os.path.join(ILL_DIR_NEW, f"new_p{page_num:02d}.png")
    old_path = os.path.join(ILL_DIR_OLD, f"v2_p{page_num:02d}.png")
    for path in (new_path, old_path):
        if os.path.exists(path):
            img = Image.open(path).convert("RGBA")
            iw, ih = img.size
            # If portrait or square, rotate/pad to landscape
            if ih > iw:
                # Rotate 90° to make it landscape
                img = img.rotate(-90, expand=True)
                print(f"    [normalised p{page_num:02d}: rotated portrait {iw}x{ih} → {img.size}]")
            elif ih == iw:
                # Square: letterbox into 3:2 landscape canvas
                canvas = Image.new("RGBA", (ILL_CANONICAL_W, ILL_CANONICAL_H), (251, 249, 244, 255))
                scale = ILL_CANONICAL_H / ih
                nw, nh = int(iw * scale), int(ih * scale)
                img = img.resize((nw, nh), Image.LANCZOS)
                x = (ILL_CANONICAL_W - nw) // 2
                canvas.paste(img, (x, 0), img)
                img = canvas
                print(f"    [normalised p{page_num:02d}: letterboxed square {iw}x{ih} → 1536x1024]")
            return img, path
    print(f"  WARNING: no illustration for page {page_num}")
    return None, None

def fit_illustration(ill_img):
    """Scale illustration to fit inside ILL_MAX_W × ILL_MAX_H, preserving AR."""
    iw, ih = ill_img.size
    scale = min(ILL_MAX_W / iw, ILL_MAX_H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    return ill_img.resize((nw, nh), Image.LANCZOS), nw, nh

# ── Decide if a line should be italic ─────────────────────────────────────────
def line_font(line):
    """Heuristic: lines starting with quotes or dashes are italic/dialogue."""
    stripped = line.strip()
    if stripped.startswith(('"', '\u201c', '\u201d', '\u2018', '\u2019',
                             '—', '-', '«', '»')):
        return font_ital
    return font_reg

# ── Draw text block ────────────────────────────────────────────────────────────
def draw_text(draw, lines, text_zone_y):
    """Vertically centre the text block within the remaining space."""
    SIDE_PAD = 120   # horizontal inset for text (looks better than full width)

    # Measure total height
    total_h = 0
    for ln in lines:
        total_h += HALF_BREAK if ln == "" else LINE_H
    total_h -= (LINE_H - HALF_BREAK)  # last line doesn't get trailing gap

    available = PX - text_zone_y - PADDING_BOTTOM
    y = text_zone_y + max((available - total_h) // 2, GAP_ABOVE_TEXT)

    for ln in lines:
        if ln == "":
            y += HALF_BREAK
            continue
        fnt = line_font(ln)
        if RTL:
            # Right-to-left: right-align within safe margin
            bb  = fnt.getbbox(ln)
            tw  = bb[2] - bb[0]
            x   = PX - SIDE_PAD - tw
        else:
            bb  = fnt.getbbox(ln)
            tw  = bb[2] - bb[0]
            x   = (PX - tw) // 2
        draw.text((x, y), ln, font=fnt, fill=INK)
        y += LINE_H

# ── Separator ─────────────────────────────────────────────────────────────────
def draw_separator(draw, y):
    pad = int(PX * 0.18)
    draw.line([(pad, y), (PX - pad, y)],
              fill=(195, 182, 162), width=SEP_THICKNESS)

# ── Compose all pages ─────────────────────────────────────────────────────────
for page_num, lines in PAGES:
    page = Image.new("RGBA", (PX, PX), BG + (255,))

    # 1. Paste illustration
    ill_img, ill_src = load_illustration(page_num)
    ill_bottom = MARGIN_TOP   # fallback if no illustration
    if ill_img:
        ill_fit, nw, nh = fit_illustration(ill_img)
        # Centre horizontally; start at MARGIN_TOP vertically
        x = (PX - nw) // 2
        y = MARGIN_TOP
        page.paste(ill_fit, (x, y), ill_fit)
        ill_bottom = MARGIN_TOP + nh
        src_tag = "NEW" if "new_p" in str(ill_src) else "old"
    else:
        src_tag = "MISSING"

    draw = ImageDraw.Draw(page)

    # 2. Separator line below illustration
    sep_y = ill_bottom + GAP_BELOW_ILL
    draw_separator(draw, sep_y)

    # 3. Text block
    text_zone_y = sep_y + SEP_THICKNESS + GAP_ABOVE_TEXT
    draw_text(draw, lines, text_zone_y)

    # 4. Save
    out_path = os.path.join(OUT_DIR, f"page_{page_num:02d}.png")
    page.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    print(f"  ✓ p{page_num:02d} [{src_tag}]  ill_h={ill_bottom - MARGIN_TOP}  sep_y={sep_y}")

print(f"\n✓ Done. {len(PAGES)} pages → {OUT_DIR}/")
