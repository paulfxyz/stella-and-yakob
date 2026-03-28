"""
Translate Stella & Yakob into Nepali (नेपाली) using OpenRouter API.
GPT-4o initial translation → Claude 3.5 Sonnet refinement.
"""

import os
import json
import requests
import time
import sys

API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://paulfleury.com",
    "X-Title": "Stella & Yakob Translation"
}

sys.path.insert(0, '/home/user/workspace')
from book_text_en_v3 import PAGES as ENGLISH_PAGES

INSTRUCTIONS_GPT = """You are translating a children's book from English to Nepali (नेपाली).
Language: Standard Nepali (खस भाषा). Warm, accessible children's book register. Natural, flowing prose.
Story context:
- Stella: small girl, dark bob hair, pale blue dress, rosy cheeks — stays "स्टेला" in Nepali
- Yakob: large natural owl, warm brown feathers, amber eyes — NO glasses — stays "याकोब" in Nepali
- Silver Fox: sleek metallic silver fox — "चाँदीको सियार" in Nepali
- Act 2 (pages 31-45): The Dream Question (Descartes), The Mirror Villain (Stella-Prime), Consciousness (Searle library metaphor), The Gift of Imperfection, The Promise
- Tone: poetic, tender, sparse — minimal watercolour aesthetic in the language too
- Use Devanagari script throughout. Natural Nepali, not over-formal.
Return ONLY a valid Python PAGES list with the exact same structure as the input."""

INSTRUCTIONS_CLAUDE = """You are a native Nepali speaker and children's book editor.
Refine this Nepali translation so it sounds warm, modern, and completely natural —
the way a parent would read aloud to a child aged 5–10.
Fix any awkward phrasing, stiff word choices, or overly literal translations.
Stella stays "स्टेला", Yakob stays "याकोब", Silver Fox stays "चाँदीको सियार".
Return ONLY the corrected Python PAGES list."""

def pages_to_str(pages):
    lines = ["PAGES = ["]
    for num, page_lines in pages:
        lines.append(f"    ({num}, [")
        for line in page_lines:
            escaped = line.replace('\\', '\\\\').replace('"', '\\"')
            lines.append(f'        "{escaped}",')
        lines.append("    ]),")
    lines.append("]")
    return "\n".join(lines)

def call_api(model, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            r = requests.post(
                BASE_URL, headers=HEADERS,
                json={"model": model, "messages": messages,
                      "temperature": 0.3, "max_tokens": 8000},
                timeout=180
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(8 * (attempt + 1))
            else:
                raise

def extract_pages(text):
    text = text.strip()
    for fence in ["```python", "```"]:
        if fence in text:
            start = text.find(fence) + len(fence)
            end = text.find("```", start)
            text = text[start:end].strip()
            break
    if "PAGES = [" in text:
        text = text[text.find("PAGES = ["):]
    elif "PAGES=[" in text:
        text = text[text.find("PAGES=["):].replace("PAGES=[", "PAGES = [")
    return text

def main():
    pages_str = pages_to_str(ENGLISH_PAGES)

    # Step 1: GPT-4o initial translation
    print("Step 1: GPT-4o initial translation...")
    prompt = f"""{INSTRUCTIONS_GPT}

Translate ALL 45 pages from English to Nepali.
Maintain the exact Python PAGES list structure. Each page must keep its page number.
Output ONLY the Python PAGES list.

{pages_str}"""

    raw = call_api("openai/gpt-4o", [{"role": "user", "content": prompt}])
    print(f"  Got {len(raw)} chars")

    with open("/home/user/workspace/book_text_ne_draft1.txt", "w", encoding="utf-8") as f:
        f.write(raw)

    # Step 2: Claude 3.5 Sonnet refinement
    print("Step 2: Claude 3.5 Sonnet refinement...")
    draft = extract_pages(raw)
    refined = call_api(
        "anthropic/claude-3.5-sonnet",
        [{"role": "user", "content": f"{INSTRUCTIONS_CLAUDE}\n\nHere is the Nepali translation to refine:\n\n{draft}"}]
    )
    print(f"  Got {len(refined)} chars")

    with open("/home/user/workspace/book_text_ne_draft2.txt", "w", encoding="utf-8") as f:
        f.write(refined)

    # Save final
    final = extract_pages(refined)
    output = f'''"""
Stella & Yakob — Version 3 (45 pages)
Nepali (नेपाली) translation
"""

{final}
'''
    out_path = "/home/user/workspace/book_text_ne_v3.py"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Saved → {out_path}")

    # Verify
    try:
        g = {}
        exec(open(out_path).read(), g)
        pages = g.get("PAGES", [])
        print(f"VERIFIED: {len(pages)} pages {'✓' if len(pages)==45 else '⚠ expected 45'}")
        print(f"Sample page 1: {pages[0][1][:2]}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
