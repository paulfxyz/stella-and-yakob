#!/usr/bin/env python3
"""
Cover for Stella & Yakob — square 8.5x8.5" @ 300 DPI = 2550x2550 px
Layout: illustration top ~62%, title zone bottom ~38%
"""
from PIL import Image, ImageDraw, ImageFont

PX    = 2550
BG    = (251, 249, 244)
INK   = (38, 28, 20)
MUTED = (110, 96, 78)

# Illustration zone height (top portion)
ILL_H = int(PX * 0.62)   # ~1581px

# Load cover art
art = Image.open("/home/user/workspace/cover_art_v3.png").convert("RGBA")
aw, ah = art.size

# Scale to fill ILL_H height, centered
scale = min(PX / aw, ILL_H / ah)
nw = int(aw * scale)
nh = int(ah * scale)
art = art.resize((nw, nh), Image.LANCZOS)

page = Image.new("RGBA", (PX, PX), BG + (255,))
x = (PX - nw) // 2
y = ILL_H - nh   # bottom-align in illustration zone
page.paste(art, (x, y), art)

draw = ImageDraw.Draw(page)

# Subtle separator
pad = int(PX * 0.18)
draw.line([(pad, ILL_H + 12), (PX - pad, ILL_H + 12)], fill=(195, 182, 162, 160), width=2)

# Fonts
font_title    = ImageFont.truetype("/home/user/workspace/Lora-Bold.ttf", 148)
font_subtitle = ImageFont.truetype("/home/user/workspace/Lora-Italic.ttf", 72)
font_author   = ImageFont.truetype("/home/user/workspace/Lora-Italic.ttf", 58)

def draw_centered(text, font, y, color):
    bb = font.getbbox(text)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    x  = (PX - tw) // 2
    draw.text((x, y), text, font=font, fill=color)
    return y + th + 22

y = ILL_H + 60
y = draw_centered("Stella & Yakob", font_title, y, INK)
y += 10
y = draw_centered("Une histoire formidable", font_subtitle, y, MUTED)
y += 38

# thin rule
rule_w = int(PX * 0.28)
rx = (PX - rule_w) // 2
draw.line([(rx, y), (rx + rule_w, y)], fill=(170, 155, 130, 140), width=2)
y += 32

draw_centered("Paul Fleury", font_author, y, MUTED)

out = "/home/user/workspace/cover_square.png"
page.convert("RGB").save(out, "PNG", dpi=(300, 300))
print(f"Cover saved: {out}")
