"""
Living Legacy Study Bible — Insight Generator
Calls the Gemini API to generate study notes for all verses that
have a footnote placeholder with empty content, then saves them
back to data/bible.json.

Usage:
    python3 generate_insights.py AIzaSyCy1uMfymGUfwecaXssdLPgJ3MxmhzTRxM

The script saves progress every 20 verses so it can be safely
interrupted (Ctrl+C) and re-run without losing work.
"""

import json
import sys
import time
import urllib.request
import urllib.error

# ── CONFIG ────────────────────────────────────────────────────────────────
DATA_FILE  = "data/bible.json"
API_KEY    = sys.argv[1] if len(sys.argv) > 1 else ""
MODEL      = "gemini-2.5-flash"
SAVE_EVERY = 20          # save bible.json every N generated insights
RATE_DELAY = 0.5         # seconds between API calls (stay well under quota)
# ──────────────────────────────────────────────────────────────────────────

if not API_KEY:
    print("ERROR: pass your Gemini API key as the first argument.")
    sys.exit(1)

BOOK_NAMES = [
    "Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth",
    "1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra",
    "Nehemiah","Esther","Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon",
    "Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos",
    "Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah",
    "Malachi","Matthew","Mark","Luke","John","Acts","Romans","1 Corinthians",
    "2 Corinthians","Galatians","Ephesians","Philippians","Colossians",
    "1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon",
    "Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"
]

def call_gemini(prompt):
    url = (
        f"https://generativelanguage.googleapis.com/v1/models/"
        f"{MODEL}:generateContent?key={API_KEY}"
    )
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 250}
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"\n  !! HTTP {e.code} from Gemini API:")
        print(f"  {err[:500]}")
        return None
    except Exception as e:
        print(f"\n  !! Exception: {type(e).__name__}: {e}")
        return None

def build_prompt(book, chapter, verse_num, verse_text):
    return (
        f"You are writing a study note for the Living Legacy Study Bible — "
        f"a heritage-style annotated Bible designed to pass wisdom across generations.\n\n"
        f"Write a concise, warm, and scholarly study note for {book} {chapter}:{verse_num}:\n"
        f"\"{verse_text}\"\n\n"
        f"Your note should:\n"
        f"- Illuminate the original Hebrew or Greek word meaning when relevant\n"
        f"- Provide brief historical or cultural context\n"
        f"- Offer a practical insight for daily life\n"
        f"Keep it to 2-4 sentences. Write in a warm, pastoral tone. "
        f"Do not use bullet points. Output only the study note text, nothing else."
    )

def main():
    print(f"Loading {DATA_FILE}...")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    generated = 0
    skipped   = 0
    total     = 0

    # Count total empty footnotes
    for book in data["books"]:
        if "footnotes" not in book:
            continue
        for chap_fns in book["footnotes"].values():
            for fns in chap_fns.values():
                for fn in fns:
                    if not (fn.get("content") or "").strip():
                        total += 1

    print(f"Found {total} empty footnotes to fill.\n")

    for bi, book in enumerate(data["books"]):
        if "footnotes" not in book:
            continue

        book_name = BOOK_NAMES[bi]
        chapters  = book["chapters"]

        for chap_str, verse_fns in sorted(book["footnotes"].items(), key=lambda x: int(x[0])):
            chap_num = int(chap_str)
            chap_verses = chapters[chap_num - 1] if (chap_num - 1) < len(chapters) else []

            for v_str, fns in sorted(verse_fns.items(), key=lambda x: int(x[0])):
                v_num   = int(v_str)
                v_text  = chap_verses[v_num - 1] if (v_num - 1) < len(chap_verses) else ""

                for fn in fns:
                    existing = (fn.get("content") or "").strip()
                    if existing:
                        skipped += 1
                        continue

                    ref = f"{book_name} {chap_num}:{v_num}"
                    print(f"[{generated+skipped+1}/{total+skipped}] Generating {ref}...", end=" ", flush=True)

                    prompt  = build_prompt(book_name, chap_num, v_num, v_text)
                    insight = call_gemini(prompt)

                    if insight:
                        fn["content"] = insight
                        fn["author"]  = "Living Legacy Study Bible"
                        generated += 1
                        print(f"✓  ({len(insight)} chars)")
                    else:
                        print("✗ skipped (API error)")

                    time.sleep(RATE_DELAY)

                    if generated % SAVE_EVERY == 0 and generated > 0:
                        print(f"  → Saving progress ({generated} generated)...")
                        with open(DATA_FILE, "w", encoding="utf-8") as f:
                            json.dump(data, f, separators=(",", ":"))
                        print("  → Saved.\n")

    print(f"\nAll done! Generated {generated} insights, skipped {skipped} (already had content).")
    print("Saving final bible.json...")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"✅ Saved. Run 'python3 generate_pages.py YOUR_KEY' to rebuild the site.")

if __name__ == "__main__":
    main()
