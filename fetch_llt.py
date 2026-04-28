import urllib.request
import zipfile
import json
import os
import shutil

REPO_URL = "https://github.com/Mattjhagen/Living-Legacy-Translation/archive/refs/heads/main.zip"
ZIP_PATH = "llt_main.zip"
EXTRACT_DIR = "llt_main_extract"
DATA_FILE = "data/bible.json"

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

def run():
    print("Downloading zip...")
    urllib.request.urlretrieve(REPO_URL, ZIP_PATH)
    
    print("Extracting zip...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
        
    llt_json_dir = os.path.join(EXTRACT_DIR, "Living-Legacy-Translation-main", "json", "llt")
    
    print("Loading existing bible.json...")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        bible_data = json.load(f)
        
    print("Merging footnotes...")
    footnote_count = 0
    
    # Initialize footnotes dictionary for each book
    for book in bible_data.get("books", []):
        book["footnotes"] = {}

    for book_dir in os.listdir(llt_json_dir):
        book_path = os.path.join(llt_json_dir, book_dir)
        if not os.path.isdir(book_path):
            continue
            
        for chap_file in os.listdir(book_path):
            if not chap_file.endswith('.json'):
                continue
                
            chap_path = os.path.join(book_path, chap_file)
            with open(chap_path, 'r', encoding='utf-8') as f:
                chap_data = json.load(f)
                
            book_name = chap_data.get("book")
            chap_num = str(chap_data.get("chapter"))
            footnotes = chap_data.get("footnotes", [])
            
            if not footnotes:
                continue
                
            # Find the book index to update the corresponding book in bible_data
            try:
                bi = BOOK_NAMES.index(book_name)
            except ValueError:
                print(f"Book {book_name} not found in BOOK_NAMES")
                continue
                
            if bi >= len(bible_data["books"]):
                print(f"Book index {bi} out of bounds for bible_data")
                continue
                
            target_book = bible_data["books"][bi]
            if chap_num not in target_book["footnotes"]:
                target_book["footnotes"][chap_num] = {}
                
            for fn in footnotes:
                v_num = str(fn["verse"])
                if v_num not in target_book["footnotes"][chap_num]:
                    target_book["footnotes"][chap_num][v_num] = []
                target_book["footnotes"][chap_num][v_num].append(fn)
                footnote_count += 1
                
    print(f"Merged {footnote_count} footnotes into data/bible.json.")
    
    print("Saving bible.json...")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(bible_data, f, separators=(',', ':'))
        
    print("Cleaning up...")
    os.remove(ZIP_PATH)
    shutil.rmtree(EXTRACT_DIR)
    
    print("Done! You can now run generate_pages.py")

if __name__ == "__main__":
    run()
