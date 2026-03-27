#!/usr/bin/env python3
"""Assemble final 31-page square PDF: cover + 30 story pages."""
from PIL import Image
import os

COVER_PATH = "/home/user/workspace/cover_square.png"
PAGES_DIR  = "/home/user/workspace/book_pages_square"
OUT_PDF    = "/home/user/workspace/stella_et_yakob_v2.pdf"

pages = []

# Cover
c = Image.open(COVER_PATH).convert("RGB")
pages.append(c)
print(f"Cover: {c.size}")

# Story pages
for i in range(1, 31):
    p = os.path.join(PAGES_DIR, f"page_{i:02d}.png")
    img = Image.open(p).convert("RGB")
    pages.append(img)
    print(f"  Page {i:02d}: {img.size}")

print(f"\nTotal: {len(pages)} pages")

pages[0].save(
    OUT_PDF,
    save_all=True,
    append_images=pages[1:],
    resolution=300,
    quality=92,
)
size_mb = os.path.getsize(OUT_PDF) / 1_000_000
print(f"\n✓ PDF: {OUT_PDF} ({size_mb:.1f} MB)")
