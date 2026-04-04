#!/usr/bin/env python3
"""
compose_v44.py — Compositor for Stella & Yakob v4.5
=====================================================
Page order per PDF:
  Page 1 : Cover (letterboxed)
  Page 2 : Dedication / Saint-Exupéry quote  (with tiny balloon art)
  Pages 3–47 : 45 story pages
  Page 48 : THE END
  Page 49 : QR code + sandy.page

Format : 2550 × 2550 px  @  300 DPI  (8.5″ × 8.5″ square)

Layout for story pages:
  ┌──────────────────────────────┐
  │  MARGIN_TOP (60px cream)     │
  │  Illustration  (fit inside)  │
  │  GAP_BELOW_ILL (48px)        │
  │  ─── separator (2px) ───     │
  │  GAP_ABOVE_TEXT (40px)       │
  │  Text block  (centred)       │
  │  PADDING_BOTTOM (60px)       │
  └──────────────────────────────┘

Text rules:
  • ALL lines use FONT_SIZE = 68pt (uniform, no size variation)
  • Lora Regular  → narrative lines
  • Lora Italic   → dialogue lines (start with " « — –)
  • LINE_H is fixed — no per-font variation
  • RTL languages (ar, he): right-aligned text
"""

import sys, os, json
from PIL import Image, ImageDraw, ImageFont

if len(sys.argv) < 2:
    print("Usage: compose_v44.py <lang_code>")
    sys.exit(1)

LANG = sys.argv[1].lower()

# ── Canvas ─────────────────────────────────────────────────────────────────────
PX            = 2550
BG            = (251, 249, 244)
INK           = (42, 30, 18)
MUTED_INK     = (100, 85, 68)     # for attribution / secondary text

# ── Layout ─────────────────────────────────────────────────────────────────────
MARGIN_TOP    = 60
MARGIN_SIDE   = 80
ILL_MAX_W     = PX - 2 * MARGIN_SIDE
ILL_MAX_H     = 1800
GAP_BELOW_ILL = 48
SEP_THICK     = 2
GAP_ABOVE_TEXT= 40
PADDING_BOT   = 60
TEXT_SIDE_PAD = 140    # horizontal inset for text

# ── Fonts ──────────────────────────────────────────────────────────────────────
WS = "/home/user/workspace"

FONT_SIZE     = 68   # ALL story pages — uniform, no variation
QUOTE_SIZE    = 72   # Slightly larger for the dedication quote
QUOTE_ATTR_SZ = 58   # Attribution line
END_SIZE      = 120  # "THE END"
URL_SIZE      = 60   # sandy.page URL

FONT_CONFIGS = {
    "default": (f"{WS}/Lora.ttf",              f"{WS}/Lora-Italic.ttf",        False),
    "ar":      (f"{WS}/fonts_extra/Amiri-Regular.ttf",
                f"{WS}/fonts_extra/Amiri-Regular.ttf",                          True),
    "he":      ("/usr/share/fonts/truetype/noto/NotoSerifHebrew-Regular.ttf",
                "/usr/share/fonts/truetype/noto/NotoSerifHebrew-Regular.ttf",   True),
    "zh":      ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",
                "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",      False),
    "ja":      ("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",
                "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.otc",      False),
    "hi":      (f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",
                f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",                 False),
    "ne":      (f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",
                f"{WS}/fonts_extra/TiroDevanagari-Regular.ttf",                 False),
}

def _load(path, size):
    try:
        if path.endswith(".otc"):
            return ImageFont.truetype(path, size, index=0)
        return ImageFont.truetype(path, size)
    except Exception as e:
        print(f"  ⚠ font fallback ({path}): {e}")
        return ImageFont.truetype(f"{WS}/Lora-Italic.ttf", size)

reg_path, ital_path, RTL = FONT_CONFIGS.get(LANG, FONT_CONFIGS["default"])
font_reg   = _load(reg_path,  FONT_SIZE)
font_ital  = _load(ital_path, FONT_SIZE)

# IMPORTANT: Use same bbox for both fonts to keep LINE_H uniform
_bb = font_reg.getbbox("Ag")
_H  = _bb[3] - _bb[1]
LINE_H     = _H + 26    # fixed for ALL lines
HALF_BREAK = LINE_H // 2

# Dedicated fonts for special pages
font_quote      = _load(ital_path, QUOTE_SIZE)
font_quote_attr = _load(reg_path,  QUOTE_ATTR_SZ)
font_end        = _load(ital_path, END_SIZE)
font_url        = _load(reg_path,  URL_SIZE)

# ── Paths ──────────────────────────────────────────────────────────────────────
ILL_NEW = WS
ILL_OLD = f"{WS}/stella-and-yakob-repo/illustrations"
OUT_DIR = f"{WS}/book_pages_{LANG}_v45"
os.makedirs(OUT_DIR, exist_ok=True)

# ── Story text ─────────────────────────────────────────────────────────────────
sys.path.insert(0, WS)
mod   = __import__(f"book_text_{LANG}_v3")
PAGES = mod.PAGES

# ── Saint-Exupéry quote ────────────────────────────────────────────────────────
with open(f"{WS}/quote_translations.json", encoding="utf-8") as f:
    QUOTES = json.load(f)

ATTRIBUTION = "— Antoine de Saint-Exupéry"

# THE END translations
THE_END = {
    "fr": "FIN", "en": "THE END", "es": "FIN", "pt": "FIM",
    "de": "ENDE", "ar": "النهاية", "he": "סוֹף", "zh": "结束",
    "ja": "おわり", "hi": "समाप्त", "ru": "КОНЕЦ", "tr": "SON",
    "wo": "TUGËL", "da": "SLUT", "sv": "SLUT", "no": "SLUTT",
    "pl": "KONIEC", "ne": "अन्त",
}

# ── Illustration loader ────────────────────────────────────────────────────────
def load_illustration(page_num):
    new_p = os.path.join(ILL_NEW, f"new_p{page_num:02d}.png")
    old_p = os.path.join(ILL_OLD, f"v2_p{page_num:02d}.png")
    for path in (new_p, old_p):
        if os.path.exists(path):
            img = Image.open(path).convert("RGBA")
            iw, ih = img.size
            if ih > iw:   # portrait → rotate to landscape
                img = img.rotate(-90, expand=True)
            elif ih == iw:  # square → letterbox in 3:2 canvas
                canvas = Image.new("RGBA", (1536, 1024), BG + (255,))
                s = 1024 / ih
                nw, nh = int(iw*s), int(ih*s)
                img = img.resize((nw, nh), Image.LANCZOS)
                canvas.paste(img, ((1536-nw)//2, 0), img)
                img = canvas
            return img, path
    return None, None

def fit_ill(ill):
    iw, ih = ill.size
    scale  = min(ILL_MAX_W / iw, ILL_MAX_H / ih)
    nw, nh = int(iw*scale), int(ih*scale)
    return ill.resize((nw, nh), Image.LANCZOS), nw, nh

# ── Text helpers ───────────────────────────────────────────────────────────────
def pick_font(line):
    """Uniform font size. Italic only for dialogue/quote lines."""
    s = line.strip()
    if s.startswith(('"', '\u201c', '\u201d', '\u2018', '\u2019', '«', '»', '—', '–')):
        return font_ital
    if '," said' in line or '," asked' in line or '," whispered' in line:
        return font_ital
    return font_reg

def text_width(fnt, line):
    bb = fnt.getbbox(line)
    return bb[2] - bb[0]

def draw_centred_block(draw, lines, zone_y):
    """Draw text block vertically centred in remaining space below zone_y."""
    # Measure total block height
    total_h = 0
    for ln in lines:
        total_h += HALF_BREAK if ln == "" else LINE_H
    if lines and lines[-1] == "":
        total_h -= HALF_BREAK

    avail   = PX - zone_y - PADDING_BOT
    y = zone_y + max((avail - total_h) // 2, GAP_ABOVE_TEXT)

    for ln in lines:
        if ln == "":
            y += HALF_BREAK
            continue
        fnt = pick_font(ln)
        tw  = text_width(fnt, ln)
        if RTL:
            x = PX - TEXT_SIDE_PAD - tw
        else:
            x = (PX - tw) // 2
        draw.text((x, y), ln, font=fnt, fill=INK)
        y += LINE_H

def draw_separator(draw, y):
    pad = int(PX * 0.18)
    draw.line([(pad, y), (PX - pad, y)], fill=(195, 182, 162), width=SEP_THICK)

def blank_page():
    return Image.new("RGB", (PX, PX), BG)

# ── PAGE 1 : Cover ─────────────────────────────────────────────────────────────
def make_cover():
    cover_src = f"{WS}/stella-and-yakob-repo/languages/en/cover/cover_en.png"
    cover = Image.open(cover_src).convert("RGB")
    cw, ch = cover.size
    scale  = min(PX/cw, PX/ch)
    nw, nh = int(cw*scale), int(ch*scale)
    cr     = cover.resize((nw, nh), Image.LANCZOS)
    pg     = blank_page()
    pg.paste(cr, ((PX-nw)//2, (PX-nh)//2))
    return pg

# ── PAGE 2 : Dedication ────────────────────────────────────────────────────────
def make_dedication():
    pg   = blank_page()
    draw = ImageDraw.Draw(pg)

    quote = QUOTES.get(LANG, QUOTES["en"])

    # Art — scale to 42% of page width (much larger than before)
    art_src = f"{WS}/dedication_art.png"
    if os.path.exists(art_src):
        art = Image.open(art_src).convert("RGBA")
        aw, ah = art.size
        target_w = int(PX * 0.42)
        art_scale = target_w / aw
        nw, nh = int(aw * art_scale), int(ah * art_scale)
        art_r = art.resize((nw, nh), Image.LANCZOS)
        x = (PX - nw) // 2
        y_top = 80
        pg.paste(art_r, (x, y_top), art_r)
        text_start_y = y_top + nh + 60
    else:
        text_start_y = PX // 2 - 200

    # Thin separator
    sep_pad = int(PX * 0.22)
    draw.line([(sep_pad, text_start_y), (PX - sep_pad, text_start_y)],
              fill=(195, 182, 162), width=2)
    text_start_y += 52

    # Quote — wrap at ~38 chars
    import textwrap
    wrapped = textwrap.fill(quote, width=38)
    quote_lines = wrapped.split("\n")

    q_bb = font_quote.getbbox("Ag")
    q_line_h = (q_bb[3] - q_bb[1]) + 22
    attr_bb  = font_quote_attr.getbbox("Ag")

    y = text_start_y
    for line in quote_lines:
        bb = font_quote.getbbox(line)
        tw = bb[2] - bb[0]
        x  = (PX - tw) // 2
        draw.text((x, y), line, font=font_quote, fill=INK)
        y += q_line_h

    y += 40
    attr_tw = font_quote_attr.getbbox(ATTRIBUTION)[2] - font_quote_attr.getbbox(ATTRIBUTION)[0]
    draw.text(((PX - attr_tw)//2, y), ATTRIBUTION, font=font_quote_attr, fill=MUTED_INK)

    return pg

# ── PAGE 48 : THE END ──────────────────────────────────────────────────────────
def make_the_end():
    pg   = blank_page()
    draw = ImageDraw.Draw(pg)
    text = THE_END.get(LANG, "THE END")
    tw   = font_end.getbbox(text)[2] - font_end.getbbox(text)[0]
    th   = font_end.getbbox(text)[3] - font_end.getbbox(text)[1]
    draw.text(((PX-tw)//2, (PX-th)//2), text, font=font_end, fill=INK)
    return pg

# ── PAGE 49 : QR code + Stella & Yakob ────────────────────────────────────────
def make_qr_page():
    pg   = blank_page()
    draw = ImageDraw.Draw(pg)

    # QR code (warm amber-on-cream, pointing to sandy.page/book)
    qr_src = f"{WS}/qr_book.png"
    if not os.path.exists(qr_src):
        qr_src = f"{WS}/qr_sandy.png"  # fallback

    qr_size = 820
    if os.path.exists(qr_src):
        qr = Image.open(qr_src).convert("RGBA")
        qr_r = qr.resize((qr_size, qr_size), Image.LANCZOS)
        x_qr = (PX - qr_size) // 2
        y_qr = 260
        pg.paste(qr_r, (x_qr, y_qr), qr_r)
        url_y = y_qr + qr_size + 60
    else:
        url_y = PX // 2

    # URL — sandy.page/book (larger font)
    font_url_lg = _load(reg_path, 80)
    url = "sandy.page/book"
    tw  = font_url_lg.getbbox(url)[2] - font_url_lg.getbbox(url)[0]
    draw.text(((PX - tw)//2, url_y), url, font=font_url_lg, fill=(181, 122, 26))

    # Stella (left) and Yakob (right) as character cutouts
    stella_src = f"{WS}/stella-website-deploy/assets/char_stella.png"
    yakob_src  = f"{WS}/stella-website-deploy/assets/char_yakob.png"

    char_h = 700
    y_char_bottom = PX - 120

    if os.path.exists(stella_src):
        stella = Image.open(stella_src).convert("RGBA")
        sw, sh = stella.size
        s = char_h / sh
        stella_r = stella.resize((int(sw*s), char_h), Image.LANCZOS)
        x_s = 110
        y_s = y_char_bottom - char_h
        pg.paste(stella_r, (x_s, y_s), stella_r)

    if os.path.exists(yakob_src):
        yakob = Image.open(yakob_src).convert("RGBA")
        yw, yh = yakob.size
        s = char_h / yh
        yakob_r = yakob.resize((int(yw*s), char_h), Image.LANCZOS)
        x_y = PX - 110 - yakob_r.width
        y_y = y_char_bottom - char_h
        pg.paste(yakob_r, (x_y, y_y), yakob_r)

    # Thin separator between characters
    sep_y = y_char_bottom - char_h - 30
    draw.line([(300, sep_y), (PX - 300, sep_y)], fill=(195, 182, 162), width=2)

    return pg

# ── COMPOSE ALL PAGES ──────────────────────────────────────────────────────────
pages_out = []

# Cover
pages_out.append(make_cover())
print("  ✓ cover")

# Dedication
pages_out.append(make_dedication())
print("  ✓ dedication (Saint-Exupéry quote)")

# 45 story pages
for page_num, lines in PAGES:
    pg   = Image.new("RGBA", (PX, PX), BG + (255,))
    ill, src = load_illustration(page_num)
    if ill:
        ill_fit, nw, nh = fit_ill(ill)
        x = (PX - nw) // 2
        pg.paste(ill_fit, (x, MARGIN_TOP), ill_fit)
        sep_y = MARGIN_TOP + nh + GAP_BELOW_ILL
    else:
        sep_y = MARGIN_TOP + GAP_BELOW_ILL

    draw = ImageDraw.Draw(pg)
    draw_separator(draw, sep_y)
    text_zone_y = sep_y + SEP_THICK + GAP_ABOVE_TEXT
    draw_centred_block(draw, lines, text_zone_y)

    out_path = os.path.join(OUT_DIR, f"page_{page_num:02d}.png")
    pg.convert("RGB").save(out_path, "PNG", dpi=(300, 300))
    src_tag = "NEW" if "new_p" in str(src) else "old"
    pages_out.append(Image.open(out_path))
    print(f"  ✓ p{page_num:02d} [{src_tag}]")

# The End
pages_out.append(make_the_end())
print("  ✓ THE END")

# QR
pages_out.append(make_qr_page())
print("  ✓ QR / sandy.page")

# ── SAVE PDF ──────────────────────────────────────────────────────────────────
pdf_names = {
    "fr": "stella_et_yakob_fr",
    "en": "stella_and_yakob_en",
    "es": "stella_and_yakob_es",
    "pt": "stella_and_yakob_pt",
    "de": "stella_and_yakob_de",
    "ar": "stella_and_yakob_ar",
    "he": "stella_and_yakob_he",
    "zh": "stella_and_yakob_zh",
    "ja": "stella_and_yakob_ja",
    "hi": "stella_and_yakob_hi",
    "ru": "stella_and_yakob_ru",
    "tr": "stella_and_yakob_tr",
    "wo": "stella_and_yakob_wo",
    "da": "stella_and_yakob_da",
    "sv": "stella_and_yakob_sv",
    "no": "stella_and_yakob_no",
    "pl": "stella_and_yakob_pl",
    "ne": "stella_and_yakob_ne",
}

fname   = pdf_names.get(LANG, f"stella_and_yakob_{LANG}")
out_pdf = os.path.join(WS, f"{fname}_v45.pdf")

rgb_pages = [p.convert("RGB") for p in pages_out]
rgb_pages[0].save(
    out_pdf,
    save_all=True,
    append_images=rgb_pages[1:],
    resolution=300,
    quality=92,
)
size_mb = os.path.getsize(out_pdf) / 1e6
print(f"\n✓ {out_pdf}")
print(f"  {len(rgb_pages)} pages · {size_mb:.1f} MB")
