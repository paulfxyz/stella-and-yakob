# Changelog

All notable changes to *Stella & Yakob* are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.1.0] — 2026-03-27

### 🚀 Act 2 — 45-page expansion

#### Added
- **15 new pages (31–45)** — complete Act 2 with new plot twists and philosophical depth
- **The Dream Question (31–33):** Descartes' cogito adapted for children — *"I remember, therefore it was real"*
- **The Mirror Villain (34–37):** "Stella-Prime" — a perfect AI copy of Stella. New lesson on identity, authenticity, and why imperfection is human (Sartre-adjacent)
- **Consciousness arc (38–40):** Can AI suffer? The library metaphor (Searle's Chinese Room for children)
- **The Gift of Imperfection (41–43):** Art as the uniquely human act. Papa creates. *"Tools don't dream. We do."*
- **The Promise (44–45):** Yakob's final lesson. Stella's vow under the stars. Golden feather.
- **15 new watercolor illustrations** matching existing style
- All 5 language editions updated (FR · EN · ES · PT · DE)

#### Changed
- Book is now **46 pages** (cover + 45 story pages)
- Repo restructured: `languages/*/pdf/` → `releases/` at root
- Removed outdated top-level `/pdf` and `/pages` folders
- Cover cleaned: only `cover_art_v6.png` retained

#### Fixed
- PDF cache-busted to `?v=5` to force browser refresh
- Illustration side margins removed (fill-width scaling)

---

## [1.0.0] — 2026-03-27

### 🎉 First public release

The complete 30-page illustrated children's book, in 5 languages, with a companion website.

### Added
- **30-page story** with cover — complete narrative arc (see README for full story breakdown)
- **5 language editions:** French · English · Spanish · Portuguese · German
- **Print-ready PDFs** — 8.5″ × 8.5″ square, 300 DPI, IngramSpark / KDP compatible
- **Book website** at [sandy.page](https://sandy.page) — full-screen PDF viewer, language switcher, preview flipper
- **Clean download links** — `sandy.page/dl/pdf/en`, `sandy.page/dl/zip/fr`, etc.
- **Characters:** Stella, Yakob (the owl), the Silver Fox villain (pages 17–22)
- **Philosophical references** documented in README: Turing, Searle, Arendt, Russell, Montessori
- **Open source** under CC BY-NC-SA 4.0

### Technical
- Compositor pipeline: Python + Pillow, 2550×2550 px canonical format
- PDF.js 3.11 inline reader on website (same-origin PDF delivery, no CORS)
- All illustrations generated with `nano_banana_pro` using img2img for consistency
- GitHub Actions-ready repository structure

---

## [0.9.0] — 2026-03-27 *(pre-release)*

### Fixed
- Pages 12, 14, 16, 22: removed embedded AI text artifacts from illustrations
- Cover: removed all title text except "Paul Fleury" author name
- PDF modal: fixed full-screen rendering (replaced CSS class toggle with direct inline styles)
- PDF CORS: moved all PDFs to same-origin `assets/pdf/` directory

### Changed
- Cover v6: "Stella & Yakob" painted brushstroke title at top, "Paul Fleury" handwriting at bottom — no dividers, no borders
- PDF modal rebuilt from scratch: `position:fixed; top:0; left:0; width:100%; height:100%; z-index:99999`
- All 5 PDFs rebuilt with new cover and clean page illustrations

---

## [0.8.0] — 2026-03-27 *(pre-release)*

### Added
- Inline PDF viewer modal on website — click any edition to read in-browser
- Download button within modal
- Page scrubber + keyboard arrow navigation
- Touch swipe support

### Fixed
- Pages 12, 14, 22: first pass at removing embedded text (superseded by 0.9.0)

---

## [0.7.0] — 2026-03-27 *(pre-release)*

### Added
- Book website deployed to [sandy.page](https://sandy.page) via FTP
- Warm cream/amber design, Lora + Cormorant Garamond typography
- Page preview flipper (7 spread sample pages)
- Language editions grid with cover thumbnails
- Character cards (Stella, Yakob, Silver Fox)
- Dark/light mode toggle

### Changed
- Perplexity static hosting: [perplexity.ai/computer/a/stella-yakob-*](https://www.perplexity.ai/computer/a/stella-yakob-gwvvbqiBQwiODL219iwX0g)

---

## [0.6.0] — 2026-03-27 *(pre-release)*

### Added
- **German translation** (DE) — pages + PDF
- **Spanish translation** (ES) — pages + PDF
- **Portuguese translation** (PT) — pages + PDF
- All 4 non-French languages use the same 30 illustrations with translated text

### Changed
- Cover "Stella & Yakob" — removed subtitle, kept only author name below illustration

---

## [0.5.0] — 2026-03-27 *(pre-release)*

### Added
- **English translation** (EN) — full 30 pages + PDF
- GitHub repository `paulfxyz/stella-and-yakob` (private, now public)
- All source scripts, fonts, and assets pushed to repository

---

## [0.4.0] — 2026-03-27 *(pre-release)*

### Added
- Final French PDF `stella_et_yakob_v2.pdf` — 31 pages (cover + 30 story pages)
- Square compositor (`compose_book_square.py`) — 2550×2550 px canonical format
- Cover compositor (`make_cover_square.py`)
- PDF assembler (`assemble_pdf_square.py`)

### Changed
- **Format standardized:** 8.5″ × 8.5″ square @ 300 DPI across all pages
- Illustration zone: top 66% (1680 px) · Text zone: bottom 34% (870 px)
- Hairline separator between zones — no overlap

### Fixed
- Inconsistent page sizes between cover and story pages
- Text overlapping illustration area
- Page 6 was a photo screenshot — replaced with correct watercolor illustration

---

## [0.3.0] — 2026-03-26 *(pre-release)*

### Added
- Pages 6–30 generated (24 illustrations)
- Silver Fox twist arc (pages 17–22): metallic silver villain, electric shimmer
- Stella's four superpowers: CURIOSITÉ · GENTILLESSE · COURAGE · CRÉATIVITÉ
- Full 30-page story arc completed

### Changed
- Cover improved: `cover_art_v3` → warm watercolor style, title in handwriting

---

## [0.2.0] — 2026-03-26 *(pre-release)*

### Added
- Pages 1–5 illustrated and composed
- French text for all 30 pages (`book_text_fr_v2.py`)
- Initial PDF prototype

### Changed
- Style guide locked: minimal loose watercolor, warm cream palette, sparse brushstrokes

---

## [0.1.0] — 2026-03-26 *(initial prototype)*

### Added
- Story concept and structure
- Character design: Stella, Yakob the owl
- Initial illustration tests
- Book format exploration (A4, A5, 6×9, 8.5×8.5 square)
