import os
"""
Translate Stella & Yakob into Danish, Swedish, Norwegian (Bokmål), and Polish
using OpenRouter API with GPT-4o for initial translation and Claude 3.5 Sonnet for refinement.
"""

import json
import requests
import time
import concurrent.futures

API_KEY = os.environ.get('OPENROUTER_API_KEY', '')
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://paulfleury.com",
    "X-Title": "Stella & Yakob Translation"
}

# Source English text
import sys
sys.path.insert(0, '/home/user/workspace')
from book_text_en_v3 import PAGES as ENGLISH_PAGES

LANGUAGE_CONFIGS = {
    "da": {
        "name": "Danish",
        "instructions": """You are translating a children's book from English to Danish.
Language: Modern standard Danish (rigsdansk). Warm, accessible children's book register. Natural contractions and flow.
Story context:
- Stella: small girl, dark bob hair, pale blue dress, rosy cheeks
- Yakob: large natural owl, warm brown feathers, amber eyes — NO glasses
- Silver Fox: sleek metallic silver villain (pages 17-22)
- Act 2 (pages 31-45): The Dream Question (Descartes), The Mirror Villain (Stella-Prime), Consciousness (library metaphor = Searle), The Gift of Imperfection, The Promise
- Tone: poetic, tender, sparse — minimal watercolour aesthetic in the language too
Keep character names: Stella, Yakob, Silver Fox (= Sølvræven)
Return ONLY a valid Python PAGES list with the exact same structure as the input.""",
        "refine_instructions": "You are a native Danish speaker and children's book editor. Refine this translation so it sounds warm, modern, and completely natural — the way a parent would read aloud to a child aged 5–10. Fix any awkward phrasing, stiff word choices, or overly literal translations. Return ONLY the corrected Python PAGES list.",
        "output_file": "book_text_da_v3.py"
    },
    "sv": {
        "name": "Swedish",
        "instructions": """You are translating a children's book from English to Swedish.
Language: Modern standard Swedish (rikssvenska). Warm and playful, appropriate for age 5–10.
Story context:
- Stella: small girl, dark bob hair, pale blue dress, rosy cheeks
- Yakob: large natural owl, warm brown feathers, amber eyes — NO glasses
- Silver Fox: sleek metallic silver villain (pages 17-22)
- Act 2 (pages 31-45): The Dream Question (Descartes), The Mirror Villain (Stella-Prime), Consciousness (library metaphor = Searle), The Gift of Imperfection, The Promise
- Tone: poetic, tender, sparse — minimal watercolour aesthetic in the language too
Keep character names: Stella, Yakob, Silver Fox (= Silverräven)
Return ONLY a valid Python PAGES list with the exact same structure as the input.""",
        "refine_instructions": "You are a native Swedish speaker and children's book editor. Refine this translation so it sounds warm, modern, and completely natural — the way a parent would read aloud to a child aged 5–10. Fix any awkward phrasing, stiff word choices, or overly literal translations. Return ONLY the corrected Python PAGES list.",
        "output_file": "book_text_sv_v3.py"
    },
    "no": {
        "name": "Norwegian (Bokmål)",
        "instructions": """You are translating a children's book from English to Norwegian Bokmål.
Language: Modern, accessible Norwegian Bokmål. Warm. NOT Nynorsk.
Story context:
- Stella: small girl, dark bob hair, pale blue dress, rosy cheeks
- Yakob: large natural owl, warm brown feathers, amber eyes — NO glasses
- Silver Fox: sleek metallic silver villain (pages 17-22)
- Act 2 (pages 31-45): The Dream Question (Descartes), The Mirror Villain (Stella-Prime), Consciousness (library metaphor = Searle), The Gift of Imperfection, The Promise
- Tone: poetic, tender, sparse — minimal watercolour aesthetic in the language too
Keep character names: Stella, Yakob, Silver Fox (= Sølvreven)
Return ONLY a valid Python PAGES list with the exact same structure as the input.""",
        "refine_instructions": "You are a native Norwegian Bokmål speaker and children's book editor. Refine this translation so it sounds warm, modern, and completely natural — the way a parent would read aloud to a child aged 5–10. Fix any awkward phrasing, stiff word choices, or overly literal translations. Return ONLY the corrected Python PAGES list.",
        "output_file": "book_text_no_v3.py"
    },
    "pl": {
        "name": "Polish",
        "instructions": """You are translating a children's book from English to Polish.
Language: Współczesna polska. Warm, modern children's register.
Story context:
- Stella: small girl, dark bob hair, pale blue dress, rosy cheeks — stays Stella in Polish
- Yakob: large natural owl, warm brown feathers, amber eyes — NO glasses — becomes Jakub (natural Polish form)
- Silver Fox: sleek metallic silver villain (pages 17-22) — becomes Srebrny Lis
- Act 2 (pages 31-45): The Dream Question (Descartes), The Mirror Villain (Stella-Prime), Consciousness (library metaphor = Searle), The Gift of Imperfection, The Promise
- Tone: poetic, tender, sparse — minimal watercolour aesthetic in the language too
Character names: Stella stays Stella, Yakob becomes Jakub (use consistently), Silver Fox = Srebrny Lis
Return ONLY a valid Python PAGES list with the exact same structure as the input.""",
        "refine_instructions": "You are a native Polish speaker and children's book editor. Refine this translation so it sounds warm, modern, and completely natural — the way a parent would read aloud to a child aged 5–10. Fix any awkward phrasing, stiff word choices, or overly literal translations. Stella stays Stella, Yakob becomes Jakub throughout. Return ONLY the corrected Python PAGES list.",
        "output_file": "book_text_pl_v3.py"
    }
}

def call_api(model, messages, max_retries=3):
    """Call OpenRouter API with retry logic."""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                BASE_URL,
                headers=HEADERS,
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 8000,
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise

def pages_to_python_string(pages):
    """Convert PAGES list to Python string representation."""
    lines = ["PAGES = ["]
    for page_num, page_lines in pages:
        lines.append(f"    ({page_num}, [")
        for line in page_lines:
            escaped = line.replace('\\', '\\\\').replace('"', '\\"')
            lines.append(f'        "{escaped}",')
        lines.append("    ]),")
    lines.append("]")
    return "\n".join(lines)

def extract_pages_from_response(response_text):
    """Extract and parse the PAGES list from model response."""
    # Try to find the PAGES = [ ... ] block
    text = response_text.strip()
    
    # Remove markdown code blocks if present
    if "```python" in text:
        start = text.find("```python") + 9
        end = text.find("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        text = text[start:end].strip()
    
    # Find PAGES = [
    if "PAGES = [" in text:
        start = text.find("PAGES = [")
        text = text[start:]
    elif "PAGES=[" in text:
        start = text.find("PAGES=[")
        text = text[start:].replace("PAGES=[", "PAGES = [")
    
    return text

def build_translation_prompt(lang_code, config):
    """Build the prompt for translating all 45 pages."""
    pages_str = pages_to_python_string(ENGLISH_PAGES)
    
    prompt = f"""{config['instructions']}

Translate ALL 45 pages of this children's book from English to {config['name']}.
Maintain the exact Python PAGES list structure. Each page must keep its page number.
Output ONLY the Python PAGES list, nothing else.

Here is the English source:

{pages_str}"""
    
    return prompt

def translate_language(lang_code):
    """Full translation pipeline for one language."""
    config = LANGUAGE_CONFIGS[lang_code]
    print(f"\n{'='*60}")
    print(f"Starting {config['name']} ({lang_code}) translation...")
    print(f"{'='*60}")
    
    # Step 1: Initial translation with GPT-4o
    print(f"[{lang_code}] Step 1: GPT-4o initial translation...")
    prompt = build_translation_prompt(lang_code, config)
    
    messages_step1 = [
        {"role": "user", "content": prompt}
    ]
    
    raw_translation = call_api("openai/gpt-4o", messages_step1)
    print(f"[{lang_code}] Got initial translation ({len(raw_translation)} chars)")
    
    # Save intermediate result
    with open(f"/home/user/workspace/book_text_{lang_code}_v3_draft1.txt", "w", encoding="utf-8") as f:
        f.write(raw_translation)
    
    # Step 2: Refinement with Claude 3.5 Sonnet
    print(f"[{lang_code}] Step 2: Claude 3.5 Sonnet refinement...")
    
    extracted_draft = extract_pages_from_response(raw_translation)
    
    messages_step2 = [
        {"role": "user", "content": f"{config['refine_instructions']}\n\nHere is the {config['name']} translation to refine:\n\n{extracted_draft}"}
    ]
    
    refined_translation = call_api("anthropic/claude-3.5-sonnet", messages_step2)
    print(f"[{lang_code}] Got refined translation ({len(refined_translation)} chars)")
    
    # Save intermediate result
    with open(f"/home/user/workspace/book_text_{lang_code}_v3_draft2.txt", "w", encoding="utf-8") as f:
        f.write(refined_translation)
    
    # Extract and save final version
    final_text = extract_pages_from_response(refined_translation)
    
    # Write the final Python file
    output_path = f"/home/user/workspace/{config['output_file']}"
    file_content = f'''"""
Stella & Yakob — Version 3 (45 pages)
{config['name']} translation
"""

{final_text}
'''
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    
    print(f"[{lang_code}] Saved to {output_path}")
    
    # Verify
    try:
        exec_globals = {}
        exec(open(output_path).read(), exec_globals)
        pages = exec_globals.get("PAGES", [])
        if len(pages) == 45:
            print(f"[{lang_code}] VERIFIED: {len(pages)} pages ✓")
        else:
            print(f"[{lang_code}] WARNING: Expected 45 pages, got {len(pages)}")
    except Exception as e:
        print(f"[{lang_code}] ERROR verifying: {e}")
    
    return lang_code, output_path

def main():
    print("Starting parallel translation of Stella & Yakob...")
    print(f"Source: {len(ENGLISH_PAGES)} pages")
    
    languages = ["da", "sv", "no", "pl"]
    
    # Run all 4 languages in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(translate_language, lang): lang for lang in languages}
        results = []
        for future in concurrent.futures.as_completed(futures):
            lang = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"\nCompleted: {result[0]} -> {result[1]}")
            except Exception as e:
                print(f"\nFAILED {lang}: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "="*60)
    print("All translations complete!")
    print("="*60)
    for lang, path in sorted(results):
        print(f"  {lang}: {path}")

if __name__ == "__main__":
    main()
