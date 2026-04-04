## [4.5.0] — 2026-04-04

### ✨ v4.5 — QR Page Redesign + sandy.page/book

#### QR Page (Page 49) — Fully Redesigned
- QR code now points to **sandy.page/book** (was sandy.page)
- Warm amber QR code on cream background (`qr_book.png`)
- Stella & Yakob character illustrations flank the QR code at bottom
- Amber URL text: `sandy.page/book`
- Tagline: *"Read, download & share — free for everyone"*
- Thin separator line above characters

#### Dedication Page (Page 2) — Improved
- Balloon watercolour art scaled to 42% of page width (much larger, more prominent)
- Separator line between art and quote
- Better vertical spacing

#### Infrastructure
- `.htaccess`: `/book` redirect → sandy.page/ (all devices)
- PDF cache buster bumped to `?v=12`
- 49 pages per PDF (unchanged structure)

---

## [4.4.0] — 2026-04-04

### ✨ v4.4 — Dedication Page, THE END, QR Page + Text Audit

#### New Pages (49 total: was 46)
- **Page 2 — Dedication:** Saint-Exupéry quote *« On ne voit bien qu'avec le cœur. L'essentiel est invisible pour les yeux. »* — translated into all 18 languages. Accompanied by a tiny minimal watercolour: a boy on a hilltop, a single red balloon drifting upward into cream paper sky.
- **Page 48 — THE END** (translated: FIN, ENDE, KONIEC, etc.)
- **Page 49 — QR Code:** sandy.page rounded QR code + URL — invites readers to download all editions

#### Text Audit (compose_v44.py)
- Uniform font size: 68pt for ALL story page lines (no size drift between pages)
- Strict italic rule: only dialogue/quoted speech lines (starting with `"`, `«`, `—`) use Lora Italic; all narration uses Lora Regular
- Fixed-height LINE_H calculated once from font_reg bounding box — no per-font variation
- RTL (Arabic, Hebrew): right-aligned in safe margins, same size as LTR

#### Assets
- `dedication_art.png` — new minimal watercolour (GPT-Image-1.5, img2img from p07)
- `qr_sandy.png` — rounded QR code for sandy.page
- `quote_translations.json` — Saint-Exupéry quote in 18 languages

---

# Changelog

All notable changes to *Stella & Yakob* are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [4.3.0] — 2026-04-04

### 🎨 v4.3 — New Illustrations (v5 watercolour set) + Preview Redesign

#### Illustrations — Complete v5 Watercolour Set
- All 45 story illustrations regenerated in a coherent minimal loose watercolour style
- Style reference: page 7 used as img2img anchor across all generations
- Every illustration: 1536×1024 px, consistent separator at y=1701 on all composed pages
- New compositor (compose_v4.py): proper margins, gap, separator line, italic text detection

#### Website
- "Inside the Book" flipper section redesigned with 10 new showcase pages (p3, p4, p7, p15, p17, p23, p25, p33, p39, p45)
- Preview images updated to show new watercolour illustrations
- PDF cache busted (?v=10) so readers see new illustrations immediately

#### PDFs
- All 18 language PDFs fully recomposed with v5 illustrations
- Cover page now letterboxed correctly — title and author name fully visible
- All pages: identical illustration height, separator position, text layout

---

## [5.0.0] — 2026-04-04

### 🎨 v5.0 — Complete Illustration Overhaul + New Compositor

#### Illustrations — Brand New Watercolour Set (all 45 pages)
- All 45 story illustrations regenerated from scratch using GPT-Image-1.5 (OpenAI)
- Style reference: page 7 (the book's most minimal, most poetic illustration) used as img2img anchor for every single generation
- Consistent visual language throughout: wet-on-wet loose watercolour, warm cream paper, intimate small figures, generous negative space, amber-gold palette
- Previous illustrations had major inconsistencies (some pages dark/moody, others light; varying styles suggesting different artists)
- New set: every page reads as the same artist, same hand, same day in the studio

#### New Compositor (compose_v4.py)
- Rebuilt from scratch with proper layout constants
- MARGIN_TOP: 60px cream above illustration — illustration never touches edge
- GAP_BELOW_ILL: 48px breathing room between illustration and separator
- Separator line: elegant 2px amber-cream rule
- GAP_ABOVE_TEXT: 40px before first text line
- Font system: Lora Regular for narrative, Lora Italic for dialogue/poetic lines
- Per-language font overrides: Amiri (Arabic), NotoSerifHebrew (Hebrew), NotoSerifCJK (Chinese/Japanese), TiroDevanagari (Hindi, Nepali)
- Fallback logic: uses new_p{N}.png first, falls back to v2_p{N}.png — zero crashes
- All 18 languages composed identically

#### Technical
- Image generation: GPT-Image-1.5 via Perplexity Computer API (img2img mode, 4:3 landscape, 2400×1792 → scaled to 2550×2550 in compositor)
- Rate limit mitigation: batches of 5–8 images with sleep intervals between bursts
- All 45 × 18 = 810 page compositions completed
- All 18 PDFs rebuilt at 300 DPI, 8.5″ square

---

## [4.2.0] — 2026-03-28

### 🇳🇵 v4.3 — Nepali (नेपाली) Edition

#### New Language
- **Nepali (नेपाली):** full 45-page GPT-4o + Claude 3.5 refinement translation
- Font: Noto Serif Devanagari (same script as Hindi)
- Character names: स्टेला (Stella), याकोब (Yakob), चाँदीको सियार (Silver Fox)
- Download: `sandy.page/dl/pdf/ne` · `sandy.page/dl/zip/ne`
- **Total: 18 languages — FR · EN · ES · PT · DE · AR · HE · ZH · JA · HI · RU · TR · WO · DA · SV · NO · PL · NE**

#### Security
- Removed hardcoded OpenRouter API key from all scripts
- API key now loaded from `OPENROUTER_API_KEY` environment variable
- Added `.gitignore` (blocks `.env` files) and `.env.example` template

---

## [4.1.0] — 2026-03-28

### 🌍 v4.3 — 4 new languages (DA/SV/NO/PL) + Disney landing page redesign

#### New Languages (17 total)
- **Danish (Dansk):** full 45-page GPT-4o + Claude refinement translation, composed pages, PDF, ZIP
- **Swedish (Svenska):** full 45-page translation, composed pages, PDF, ZIP
- **Norwegian Bokmål (Norsk):** full 45-page translation (Bokmål, not Nynorsk), composed pages, PDF, ZIP
- **Polish (Polski):** full 45-page translation, composed pages, PDF, ZIP — Yakob → Jakub (native Polish form)
- **Total: FR · EN · ES · PT · DE · AR · HE · ZH · JA · HI · RU · TR · WO · DA · SV · NO · PL**
- New download shortcuts: `sandy.page/dl/pdf/{da,sv,no,pl}` + zip variants

#### Website — Disney-Level Redesign
- Cinematic hero section with animated floating character cutouts (Stella, Yakob, Silver Fox)
- Parallax starfield, glowing orbs, scroll-triggered story panels
- Character showcase cards with personality descriptions
- All 17 languages in dropdown switcher with flags
- Edition cards for all 17 languages
- RTL fix: AR/HE text displayed RTL but left-aligned in dropdown list

#### Technical
- Universal compositor: `compose_lang_v3.py` — 2550×2550 px, all languages
- Translation pipeline: `translate_book.py` — GPT-4o + Claude 3.5 Sonnet (parallel 4×)
- `.htaccess` now covers all 17 language shortcuts
- Character PNG cutouts: `assets/char_stella.png`, `char_yakob.png`, `char_fox.png`

---

## [4.0.0] — 2026-03-27

### 🚀 v4 — 13 languages, RTL support, clean illustrations

#### Languages
- **8 new languages:** Arabic (RTL), Hebrew (RTL), Chinese, Japanese, Hindi, Russian, Turkish, Wolof
- **13 total:** FR · EN · ES · PT · DE · AR · HE · ZH · JA · HI · RU · TR · WO
- Translation pipeline: GPT-4o → Claude 3.5 Sonnet refinement (Mistral Large for Wolof)
- All 13 languages: 46-page PDFs, download shortlinks, inline PDF reader

#### Illustrations
- **Page 12 fixed** — user-provided clean illustration (no "stella" label)
- Applied across all 13 language editions

#### Technical
- RTL support: Arabic & Hebrew — `arabic-reshaper` + `python-bidi` + CSS `direction: rtl`
- Font stack: Amiri (Arabic), Noto Serif Hebrew, Noto Serif CJK, Noto Serif Devanagari
- Website: 13-language i18n, language detection (OS browser + cookie persistence)
- PDFs served from sandy.page (no CORS) — website deploy is 3.2MB
- Catch-all redirect: unknown `/dl/*` paths → `sandy.page/`
- README: 9 philosophical references, full AI toolchain, 10 bottlenecks + solutions

#### Download shortcuts
All 26 shortlinks live: `sandy.page/dl/pdf/{lang}` and `sandy.page/dl/zip/{lang}`
for all 13 languages.

---

## [3.0.0] — 2026-03-27

### 🚀 v3 — Full 45-page edition, multi-model pipeline, open source release

#### Story
- **45 story pages** (up from 30) — complete Act 2 added
- Act 2 new scenes: The Dream Question, Mirror Villain (Stella-Prime), Consciousness arc, Gift of Imperfection, The Promise
- New philosophical references: Descartes (cogito), Sartre (existence/essence), expanded Searle, Arendt, Montessori
- 15 new watercolor illustrations (pages 31–45)

#### Production
- Illustration zone fixed: 1904px (fill-width, zero cropping, zero side margins)
- Page compositor updated: 72pt body text, 646px text zone
- All 5 language editions rebuilt: 46 pages each (~48 MB per PDF)
- PDF cache-busted to `?v=6`

#### Repository
- Restructured: `languages/*/pdf/` → `releases/`  
- Removed outdated top-level `/pdf` and `/pages` folders
- Cover cleaned: v6 only retained
- README massively expanded: all 8 philosophical references, full AI toolchain, 10 technical bottlenecks

#### Attribution
- "Created with Perplexity Computer" → **"Made with ❤️ + AI"** everywhere
- AI toolchain documented: Perplexity Computer, Claude, GPT-4o, Gemini, Mistral, OpenRouter
- Illustration process clarified: hand-sketched by Paul Fleury, AI-refined

#### Website
- v3 branding throughout (EN/FR/ES/PT/DE)
- Language switcher: 5 languages, flag + code button
- PDF viewer: full-screen modal, PDF.js 3.11, same-origin delivery

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
