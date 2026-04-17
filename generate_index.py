import json
import os

def generate_index():
    with open('data/bible.json', 'r') as f:
        bible_data = json.load(f)

    # Base styling and layout
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bible Index | Rooted Daily</title>
    <meta name="description" content="Browse every book and chapter of the Bible. Rooted Daily provides a clean, fast way to read Scripture online.">
    
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-HSEJQQEFLJ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-HSEJQQEFLJ');
    </script>

    <link rel="icon" type="image/png" href="rooted-icon.png">
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0a0e12;
            --accent-green: #4a735d;
            --text-primary: #f0f4f8;
            --text-secondary: #94a3b8;
            --border: rgba(255,255,255,0.1);
        }
        body { 
            font-family: 'Inter', sans-serif; 
            background: var(--bg-dark); 
            color: var(--text-primary);
            margin: 0; padding: 0;
            line-height: 1.6;
        }
        header { padding: 2rem; max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-family: 'Crimson Text', serif; font-size: 1.8rem; font-weight: 700; color: var(--accent-green); text-decoration: none; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        h1 { font-family: 'Crimson Text', serif; font-size: 3rem; margin-bottom: 2rem; text-align: center; }
        .book-section { margin-bottom: 4rem; }
        .book-title { font-family: 'Crimson Text', serif; font-size: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1rem; color: var(--accent-green); }
        .chapter-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(60px, 1fr)); gap: 0.75rem; }
        .chapter-link {
            display: flex; align-items: center; justify-content: center;
            background: rgba(255,255,255,0.05);
            border: 1px solid var(--border);
            padding: 0.75rem;
            color: var(--text-primary);
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.2s;
            font-weight: 600;
        }
        .chapter-link:hover { background: var(--accent-green); transform: translateY(-2px); border-color: transparent; }
        footer { padding: 4rem 2rem; text-align: center; border-top: 1px solid var(--border); color: var(--text-secondary); margin-top: 4rem; }
        .btn-back { color: var(--text-secondary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <header>
        <a href="index.html" class="logo">Rooted</a>
        <a href="index.html" style="color: white; text-decoration: none; font-weight: 600;">Home</a>
    </header>

    <div class="container">
        <h1>Bible Library</h1>
        <p style="text-align: center; color: var(--text-secondary); margin-bottom: 4rem; max-width: 600px; margin-left: auto; margin-right: auto;">
            Explore every chapter of the Bible. Select a book to see all available chapters.
        </p>
    """

    book_names = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth",
        "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
        "Job", "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
        "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
        "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
        "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians",
        "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter",
        "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
    ]

    for i, book in enumerate(bible_data['books']):
        name = book_names[i]
        slug = name.lower().replace(" ", "-")
        num_chapters = len(book['chapters'])
        
        html += f'<div class="book-section" id="{slug}">\n'
        html += f'    <div class="book-title">{name}</div>\n'
        html += '    <div class="chapter-grid">\n'
        
        for c in range(1, num_chapters + 1):
            html += f'        <a href="verses/{slug}-{c}.html" class="chapter-link">{c}</a>\n'
            
        html += '    </div>\n'
        html += '</div>\n'

    html += """
    </div>
    <footer>
        <p>&copy; 2026 Rooted Daily. All Bible content is indexed for reach.</p>
        <div style="margin-top: 1rem;">
            <a href="index.html" style="color: var(--accent-green); text-decoration: none;">Home</a> | 
            <a href="bible.html" style="color: var(--accent-green); text-decoration: none;">Web Reader</a>
        </div>
    </footer>
</body>
</html>
"""

    with open('bible-index.html', 'w') as f:
        f.write(html)
    print("Generated bible-index.html")

if __name__ == "__main__":
    generate_index()
