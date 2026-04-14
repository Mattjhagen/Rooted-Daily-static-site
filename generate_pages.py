#!/usr/bin/env python3
"""
Rooted Daily - Static Bible Chapter Page Generator
Generates one SEO-optimized HTML page per Bible chapter.
Run from: /Users/matt/Rooted_Daily_Android/Rooted-Daily-static-site/
"""
import json, os, re

SITE_URL = "https://app.vibecodes.space"
OUTPUT_DIR = "verses"  # pages go into /verses/ folder

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

BOOK_AUTHORS = {
    "Genesis": "Moses", "Exodus": "Moses", "Leviticus": "Moses", "Numbers": "Moses",
    "Deuteronomy": "Moses", "Joshua": "Joshua", "Judges": "Samuel", "Ruth": "Samuel",
    "1 Samuel": "Samuel", "2 Samuel": "Samuel", "1 Kings": "Jeremiah", "2 Kings": "Jeremiah",
    "Psalms": "David", "Proverbs": "Solomon", "Ecclesiastes": "Solomon",
    "Song of Solomon": "Solomon", "Isaiah": "Isaiah", "Jeremiah": "Jeremiah",
    "Matthew": "Matthew", "Mark": "Mark", "Luke": "Luke", "John": "John",
    "Acts": "Luke", "Romans": "Paul", "1 Corinthians": "Paul", "2 Corinthians": "Paul",
    "Galatians": "Paul", "Ephesians": "Paul", "Philippians": "Paul", "Colossians": "Paul",
    "Hebrews": "Paul", "James": "James", "1 Peter": "Peter", "2 Peter": "Peter",
    "1 John": "John", "Revelation": "John"
}

def slugify(book, chapter):
    s = book.lower().replace(" ", "-")
    return f"{s}-{chapter}"

def build_page(book_name, chap_idx, verses, prev_slug, next_slug, total_chapters):
    chap_num = chap_idx + 1
    slug = slugify(book_name, chap_num)
    author = BOOK_AUTHORS.get(book_name, "Scripture")
    ref = f"{book_name} {chap_num}"

    # Build verse text for preview (first  verse, truncated)
    first_verse = verses[0][:160] if verses else ""
    last_verse_num = len(verses)

    # JSON-LD structured data for every verse
    verse_schema_list = []
    for i, v in enumerate(verses):
        verse_schema_list.append({
            "@type": "CreativeWork",
            "name": f"{book_name} {chap_num}:{i+1}",
            "text": v,
            "position": i + 1
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{ref} - Read, Listen & Reflect | Rooted Daily",
        "description": f"Read {ref} with audio narration, verse highlighting, and personal reflection. {first_verse}",
        "url": f"{SITE_URL}/verses/{slug}.html",
        "publisher": {
            "@type": "Organization",
            "name": "Rooted Daily",
            "url": SITE_URL
        },
        "mainEntity": {
            "@type": "Book",
            "name": "Holy Bible",
            "bookEdition": "WEB",
            "hasPart": {
                "@type": "Chapter",
                "name": ref,
                "position": chap_num,
                "author": {"@type": "Person", "name": author},
                "hasPart": verse_schema_list
            }
        }
    }

    # Build visible verse HTML (key for Google indexing)
    verses_html = ""
    for i, v in enumerate(verses):
        vnum = i + 1
        verses_html += f'''
        <p class="verse" id="v{vnum}">
            <span class="vnum">{vnum}</span>
            <span class="vtext">{v}</span>
        </p>'''

    prev_link = f'<a class="nav-arrow" href="{prev_slug}.html">&#8592;</a>' if prev_slug else '<span class="nav-arrow disabled">&#8592;</span>'
    next_link = f'<a class="nav-arrow" href="{next_slug}.html">&#8594;</a>' if next_slug else '<span class="nav-arrow disabled">&#8594;</span>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ref} - Read, Listen &amp; Reflect | Rooted Daily</title>
    <meta name="description" content="Read {ref} ({last_verse_num} verses) with neural audio narration, personal highlighting, and reflection journal. {first_verse[:100]}...">
    <link rel="canonical" href="{SITE_URL}/verses/{slug}.html">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9L915C1DE8"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9L915C1DE8');</script>

    <meta property="og:type" content="article">
    <meta property="og:title" content="{ref} | Rooted Daily">
    <meta property="og:description" content="{first_verse[:150]}">
    <meta property="og:url" content="{SITE_URL}/verses/{slug}.html">
    <meta property="og:image" content="{SITE_URL}/hero-bg.png">
    <meta property="twitter:card" content="summary_large_image">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

    <script type="application/ld+json">{json.dumps(schema, indent=2)}</script>

    <style>
        :root {{
            --bg: #111827; --bg-card: #1a2332; --bg-nav: #1e2d3d;
            --text: #f0f4f8; --text-muted: #6b7f96;
            --accent: #4a735d; --border: rgba(255,255,255,0.08);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Crimson Text', serif; background: var(--bg); color: var(--text); line-height: 1.9; }}
        header {{
            background: var(--bg-nav); border-bottom: 1px solid var(--border);
            padding: 1rem 1.5rem; display: flex; align-items: center;
            justify-content: space-between; position: sticky; top: 0; z-index: 100;
        }}
        .logo {{ font-size: 1.5rem; font-weight: 700; color: var(--accent); text-decoration: none; }}
        .open-reader {{
            background: var(--accent); color: white; border: none;
            padding: 0.6rem 1.25rem; border-radius: 20px;
            font-family: 'Inter', sans-serif; font-weight: 700;
            font-size: 0.85rem; cursor: pointer; text-decoration: none;
            display: inline-flex; align-items: center; gap: 0.4rem;
            transition: all 0.2s;
        }}
        .open-reader:hover {{ transform: translateY(-1px); box-shadow: 0 4px 15px rgba(74,115,93,0.4); }}
        .chapter-header {{
            text-align: center;
            padding: 3rem 1.5rem 2rem;
            border-bottom: 1px solid var(--border);
        }}
        .book-label {{
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem; font-weight: 700;
            letter-spacing: 0.15em; text-transform: uppercase;
            color: var(--accent); margin-bottom: 0.5rem;
        }}
        h1 {{ font-size: 3rem; font-weight: 600; margin-bottom: 0.5rem; }}
        .verse-count {{ font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text-muted); }}
        main {{ max-width: 680px; margin: 0 auto; padding: 2rem 1.5rem 6rem; }}
        .verse {{ margin-bottom: 1.25rem; padding: 0.5rem 0.75rem; border-radius: 6px; transition: background 0.2s; }}
        .verse:hover {{ background: rgba(74,115,93,0.08); }}
        .vnum {{ font-family: 'Inter', sans-serif; font-size: 0.65rem; font-weight: 800; color: var(--accent); vertical-align: super; margin-right: 0.3rem; opacity: 0.7; }}
        .vtext {{ font-size: 1.25rem; }}
        .chapter-nav {{
            position: fixed; bottom: 0; left: 0; right: 0;
            background: linear-gradient(to top, var(--bg) 60%, transparent);
            padding: 1.5rem;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .nav-arrow {{
            background: var(--bg-card); border: 1px solid var(--border);
            color: var(--text); padding: 0.75rem 1.5rem; border-radius: 50px;
            text-decoration: none; font-family: 'Inter', sans-serif; font-weight: 700;
            transition: all 0.2s;
        }}
        .nav-arrow:hover {{ background: var(--accent); border-color: var(--accent); color: white; }}
        .nav-arrow.disabled {{ opacity: 0.3; cursor: default; pointer-events: none; }}
        .cta-box {{
            background: var(--bg-card); border: 1px solid var(--border);
            border-radius: 20px; padding: 1.5rem; margin: 2rem 0;
            text-align: center;
        }}
        .cta-box h3 {{ font-size: 1.4rem; margin-bottom: 0.5rem; }}
        .cta-box p {{ font-family: 'Inter', sans-serif; font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem; }}
        footer {{
            text-align: center; padding: 2rem;
            font-family: 'Inter', sans-serif; font-size: 0.8rem;
            color: var(--text-muted); border-top: 1px solid var(--border);
        }}
        footer a {{ color: var(--accent); text-decoration: none; }}
    </style>
</head>
<body>

<header>
    <a class="logo" href="../index.html">Rooted</a>
    <a class="open-reader" href="../bible.html?book={book_name.replace(' ', '+')}&chapter={chap_num}">
        &#9654; Listen &amp; Reflect
    </a>
</header>

<div class="chapter-header">
    <div class="book-label">{book_name.upper()}</div>
    <h1>{ref}</h1>
    <p class="verse-count">{last_verse_num} verses &mdash; World English Bible</p>
</div>

<main>
    <article itemscope itemtype="https://schema.org/Book">
        {verses_html}
    </article>

    <div class="cta-box">
        <h3>Listen to {ref}</h3>
        <p>Open the full reader for neural audio narration, personal highlighting, and reflection journal.</p>
        <a class="open-reader" href="../bible.html?book={book_name.replace(' ', '+')}&chapter={chap_num}" style="display:inline-flex;">
            &#9654; Open Reader
        </a>
    </div>
</main>

<div class="chapter-nav">
    {prev_link}
    <a class="nav-arrow" href="../bible.html?book={book_name.replace(' ', '+')}&chapter={chap_num}" style="background:var(--accent);border-color:var(--accent);">
        &#9654; Listen
    </a>
    {next_link}
</div>

<footer>
    <p>&copy; 2026 <a href="../index.html">Rooted Daily</a> &middot; <a href="../terms.html">Terms</a> &middot; <a href="../privacy.html">Privacy</a> &middot; <a href="../sitemap.xml">Sitemap</a></p>
</footer>

</body>
</html>'''


def main():
    print("Loading bible.json...")
    with open("data/bible.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build a flat list of all (book, chap_idx) for prev/next links
    all_chapters = []
    for bi, book in enumerate(data["books"]):
        for ci in range(len(book["chapters"])):
            all_chapters.append((bi, ci))

    sitemap_urls = []
    total = 0

    for idx, (bi, ci) in enumerate(all_chapters):
        book_name = BOOK_NAMES[bi]
        verses = data["books"][bi]["chapters"][ci]
        chap_num = ci + 1
        slug = slugify(book_name, chap_num)

        # Prev/next slugs
        prev_slug = None
        if idx > 0:
            pb, pc = all_chapters[idx - 1]
            prev_slug = f"../{OUTPUT_DIR}/{slugify(BOOK_NAMES[pb], pc + 1)}"
        next_slug = None
        if idx < len(all_chapters) - 1:
            nb, nc = all_chapters[idx + 1]
            next_slug = f"../{OUTPUT_DIR}/{slugify(BOOK_NAMES[nb], nc + 1)}"

        total_chaps = len(data["books"][bi]["chapters"])
        html = build_page(book_name, ci, verses, prev_slug, next_slug, total_chaps)

        filepath = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        sitemap_urls.append(f"{SITE_URL}/{OUTPUT_DIR}/{slug}.html")
        total += 1
        if total % 100 == 0:
            print(f"  Generated {total} pages...")

    # Update sitemap.xml
    print("Writing sitemap.xml...")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        # Core pages
        for page in ["", "/bible.html", "/terms.html", "/privacy.html"]:
            f.write(f'  <url><loc>{SITE_URL}{page}</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n')

        # All generated chapter pages
        for url in sitemap_urls:
            f.write(f'  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>\n')

        f.write('</urlset>\n')

    print(f"\n✅ Done! Generated {total} chapter pages in /{OUTPUT_DIR}/")
    print(f"✅ Updated sitemap.xml with {total + 4} total URLs")
    print(f"\nNext step: git add . && git commit -m 'Add {total} static Bible chapter pages for SEO' && git push origin main")


if __name__ == "__main__":
    main()
