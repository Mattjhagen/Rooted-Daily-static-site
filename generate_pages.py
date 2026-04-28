#!/usr/bin/env python3
"""
Rooted Daily - Static Bible Chapter Page Generator with AI Explanations
Generates SEO-optimized HTML pages with static book context + live Gemini AI integration.
"""
import json, os, re, sys

SITE_URL = "https://rootedapp.space"
OUTPUT_DIR = "verses"

# Pass your Gemini API key as a command-line argument:
# python3 generate_pages.py YOUR_API_KEY_HERE
API_KEY = sys.argv[1] if len(sys.argv) > 1 else ""


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

BOOK_INTROS = {
    "Genesis": ("The Beginning of Everything", "Genesis is the foundational book of the Bible, recording the creation of the world, the fall of humanity, and God's covenant with Abraham, Isaac, and Jacob. It answers the deepest question: where did everything come from, and why does it matter?", "creation, covenant, fall, redemption, faith, promise"),
    "Exodus": ("Freedom from Bondage", "Exodus chronicles God's dramatic rescue of Israel from Egyptian slavery through Moses, the giving of the Ten Commandments, and the establishment of the tabernacle — a powerful picture of liberation and divine law.", "freedom, law, covenant, Moses, Passover, salvation"),
    "Leviticus": ("Holiness and Worship", "Leviticus details God's instructions for worship, sacrifice, and holy living for Israel. Though technical, it reveals how seriously God takes holiness and how completely He has made a way for sinners to approach Him.", "holiness, sacrifice, atonement, worship, purity"),
    "Numbers": ("Journey Through the Wilderness", "Numbers records Israel's forty years of wandering, their failures of faith, and God's persistent faithfulness. It is a story of human rebelliousness and divine patience across a generation.", "faith, wilderness, obedience, perseverance, trust"),
    "Deuteronomy": ("Remember and Obey", "Deuteronomy is Moses' final address to Israel before they enter the Promised Land — a passionate call to remember what God has done and to choose covenant obedience over self-reliance.", "obedience, covenant, memory, love, commandments"),
    "Joshua": ("Courage and Conquest", "Joshua records Israel's entry into and conquest of the Promised Land under Joshua's leadership. It is a testament to God's faithfulness in keeping every promise He made to Abraham.", "faith, courage, promise, obedience, victory"),
    "Judges": ("Cycles of Rebellion and Grace", "Judges tells the tragic cycles of Israel's unfaithfulness, oppression by enemies, crying out to God, and deliverance by judges — a mirror of the human heart's tendency to drift from God.", "repentance, rescue, cycles, grace, leadership"),
    "Ruth": ("Loyalty and Redemption", "Ruth is a beautiful short story of a Moabite woman's radical loyalty to her mother-in-law and her God — ultimately leading to her marriage to Boaz, a picture of Christ as our kinsman-redeemer.", "loyalty, redemption, grace, love, faithfulness"),
    "1 Samuel": ("The Rise of the Kingdom", "1 Samuel covers the transition from judges to kings, focusing on Samuel, Saul's tragic rise and fall, and the emergence of David — the man after God's own heart.", "leadership, obedience, humility, kingship, anointing"),
    "2 Samuel": ("David's Reign", "2 Samuel records the height of David's reign, including his great victories, his devastating sin with Bathsheba, and the painful consequences — showing that even great leaders need God's grace.", "grace, consequence, leadership, repentance, covenant"),
    "1 Kings": ("Glory and Division", "1 Kings moves from the pinnacle of Solomon's reign and the glorious temple to the tragic division of the kingdom — a cautionary tale about the seductive power of compromise.", "wisdom, idolatry, division, obedience, prophecy"),
    "2 Kings": ("The Fall of Nations", "2 Kings records the decline and eventual exile of both the Northern and Southern kingdoms, showing that persistent unfaithfulness to God has real consequences — even for His chosen people.", "judgment, exile, faithfulness, prophecy, consequences"),
    "1 Chronicles": ("The Legacy of David", "1 Chronicles retells Israel's history with a focus on the Davidic covenant and proper worship, encouraging a post-exile community to embrace their identity as God's covenant people.", "worship, covenant, identity, heritage, restoration"),
    "2 Chronicles": ("Temple and Revival", "2 Chronicles traces the history of Judah's kings, emphasizing how faithfulness to God brings blessing and how revival is always possible when people humble themselves and pray.", "revival, worship, prayer, repentance, blessing"),
    "Ezra": ("Return and Restoration", "Ezra records the return of Jewish exiles from Babylon and their struggles to rebuild the temple and recommit to God's law — a picture of restoration after discipline.", "restoration, worship, obedience, revival, identity"),
    "Nehemiah": ("Rebuilding with Purpose", "Nehemiah is the inspiring account of rebuilding Jerusalem's walls against fierce opposition — a model of prayer-driven leadership, perseverance, and community revival.", "leadership, prayer, perseverance, community, rebuilding"),
    "Esther": ("Hidden Providence", "Esther tells the story of a Jewish queen who risked her life to save her people from genocide — revealing how God orchestrates events even when His name is never mentioned.", "courage, providence, purpose, identity, deliverance"),
    "Job": ("Suffering and Sovereignty", "Job wrestles with the hardest question of human experience: why do the righteous suffer? God's answer doesn't explain the pain but reveals Himself — and that changes everything.", "suffering, faith, sovereignty, trust, prayer"),
    "Psalms": ("The Prayer Book of Israel", "Psalms is the most beloved book of the Bible — 150 songs covering the full range of human emotion, from ecstatic praise to desperate lament, all directed toward the living God.", "worship, prayer, praise, lament, trust, hope"),
    "Proverbs": ("Wisdom for Everyday Life", "Proverbs is God's practical wisdom for daily living — covering relationships, work, money, speech, and integrity. The foundation of all wisdom is a reverent relationship with God.", "wisdom, integrity, discipline, relationships, speech"),
    "Ecclesiastes": ("The Meaning of Life", "Ecclesiastes is Solomon's raw philosophical exploration of life under the sun. After searching everywhere for meaning, his conclusion is powerful: fear God and keep His commandments.", "meaning, purpose, vanity, wisdom, eternity"),
    "Song of Solomon": ("Sacred Love", "Song of Solomon is a celebration of romantic love between a husband and wife — affirming that human love is a gift from God and a picture of His passionate love for His people.", "love, beauty, intimacy, relationship, devotion"),
    "Isaiah": ("The Messianic Prophet", "Isaiah contains some of the most breathtaking prophecies in the Bible, including the Suffering Servant passages that describe Jesus' death with stunning accuracy written 700 years before the cross.", "prophecy, redemption, comfort, Messiah, holiness"),
    "Jeremiah": ("The Weeping Prophet", "Jeremiah faithfully proclaimed judgment to a nation that refused to listen, while simultaneously announcing the coming New Covenant — written on the hearts of God's people.", "faithfulness, judgment, hope, covenant, perseverance"),
    "Lamentations": ("Grief and Hope", "Lamentations is five poems of raw grief over the destruction of Jerusalem. Even in its darkest lines, one declaration shines through: 'Great is Thy faithfulness.'", "grief, mourning, hope, faithfulness, restoration"),
    "Ezekiel": ("Visions of God's Glory", "Ezekiel is filled with dramatic visions, including the famous valley of dry bones — a picture of Israel's spiritual resurrection and God's plan to put His Spirit within His people.", "vision, glory, restoration, Spirit, prophecy"),
    "Daniel": ("Faithful Under Pressure", "Daniel's story of unwavering faith in Babylon — from the fiery furnace to the lions' den — shows that God rules all kingdoms and protects those who trust Him against enormous pressure.", "faithfulness, sovereignty, courage, prayer, prophecy"),
    "Hosea": ("God's Relentless Love", "Hosea's tragic marriage to an unfaithful wife becomes a living parable of God's heartbroken love for unfaithful Israel — and His incredible commitment to redeem her anyway.", "love, faithfulness, redemption, covenant, mercy"),
    "Joel": ("The Day of the Lord", "Joel calls Israel to repentance in the face of devastating natural disaster, promising that God will pour out His Spirit on all people — a prophecy quoted by Peter at Pentecost.", "repentance, restoration, Spirit, prophecy, Pentecost"),
    "Amos": ("Justice must Roll Down", "Amos was a simple shepherd called to confront the social injustice and religious hypocrisy of prosperous Israel. His famous call: 'let justice roll down like waters.'", "justice, repentance, social justice, prophecy, humility"),
    "Obadiah": ("Pride Before the Fall", "Obadiah is the shortest book in the Old Testament, delivering God's judgment on Edom's pride and violence against Israel — a warning that treating God's people with contempt has consequences.", "pride, judgment, justice, covenant, consequences"),
    "Jonah": ("Running from God", "Jonah tries to run from God's call, only to be swallowed by a great fish and redirected — discovering that God's compassion extends to the nations he least expected, and least wanted.", "grace, obedience, compassion, mercy, calling"),
    "Micah": ("Justice, Mercy, and Humility", "Micah confronts corruption and injustice while announcing hope through a future Messiah born in Bethlehem. His call remains as relevant as ever: do justice, love mercy, walk humbly with God.", "justice, mercy, humility, prophecy, Messiah"),
    "Nahum": ("God's Judgment on Violence", "Nahum announces the fall of Nineveh, the capital of the brutal Assyrian empire — declaring that God's patience with oppression is not unlimited and His justice will prevail.", "justice, judgment, sovereignty, comfort, power"),
    "Habakkuk": ("Faith in the Dark", "Habakkuk dares to question God about suffering and injustice, and receives one of the most profound answers in all Scripture: 'the righteous shall live by faith.'", "faith, doubt, trust, sovereignty, prayer"),
    "Zephaniah": ("Judgment and Restoration", "Zephaniah warns of the coming Day of the Lord but ends with one of the most tender passages in Scripture: God rejoicing over His people with singing.", "judgment, restoration, joy, hope, repentance"),
    "Haggai": ("Put God First", "Haggai confronts a community more focused on their own houses than God's house — with a simple, powerful message: put God first and watch your priorities align.", "priorities, worship, obedience, restoration, faithfulness"),
    "Zechariah": ("Visions of the Coming King", "Zechariah is filled with Messianic prophecies — including Jesus' triumphal entry on a donkey and the thirty pieces of silver — making it one of the richest prophetic books.", "Messiah, vision, hope, prophecy, restoration"),
    "Malachi": ("The God Who Never Changes", "Malachi, the last Old Testament prophet, confronts a lukewarm Israel while declaring 'I the Lord do not change' — closing with the promise of a messenger who will prepare the way.", "faithfulness, repentance, covenant, preparation, hope"),
    "Matthew": ("The King Has Come", "Matthew presents Jesus as the promised Messiah-King, tracing His genealogy to Abraham and David. Written for a Jewish audience, it shows how Jesus fulfills every strand of the Old Testament story.", "Messiah, kingdom, fulfillment, prophecy, discipleship"),
    "Mark": ("Action and Power", "Mark is the shortest and fastest-paced Gospel — packed with miracles, conflict, and the dramatic events of Jesus' final week. It presents Jesus as the Servant who came to give His life as a ransom for many.", "action, power, service, sacrifice, discipleship"),
    "Luke": ("Savior of All People", "Luke, written by a physician, is the most comprehensive Gospel. It uniquely emphasizes Jesus' concern for the poor, women, outcasts, and Gentiles — the Savior for all humanity.", "compassion, grace, inclusion, salvation, prayer"),
    "John": ("The Word Became Flesh", "John's Gospel is the most theological, presenting Jesus as the eternal Son of God. Built around seven miracles and seven 'I AM' statements, it was written so that you might believe and have life.", "belief, eternal life, love, identity, Word"),
    "Acts": ("The Church Unleashed", "Acts records the explosive birth of the Church as the Holy Spirit empowered ordinary believers in Jerusalem to spread the gospel to the ends of the earth — and it's not finished yet.", "Holy Spirit, mission, church, power, witness"),
    "Romans": ("The Gospel Explained", "Romans is Paul's most comprehensive theological letter — a systematic explanation of how sinful humanity is made right with a holy God through faith in Jesus Christ alone.", "gospel, grace, faith, righteousness, salvation"),
    "1 Corinthians": ("A Church in Need of Grace", "1 Corinthians addresses a chaotic, divided church struggling with sexual immorality, lawsuits, spiritual gifts, and resurrection. Paul calls them back to the cross as the foundation of everything.", "unity, grace, love, church, resurrection"),
    "2 Corinthians": ("Strength in Weakness", "2 Corinthians is Paul's most personal letter — defending his ministry, sharing his sufferings, and revealing the paradox at the heart of the Christian life: power is perfected in weakness.", "suffering, grace, ministry, weakness, comfort"),
    "Galatians": ("Freedom in Christ", "Galatians is Paul's fiercest letter, confronting the deadly error of adding rules to the gospel. His declaration: 'It is for freedom that Christ has set us free' remains a battle cry for every generation.", "grace, freedom, faith, gospel, law"),
    "Ephesians": ("Seated with Christ", "Ephesians reveals the astonishing spiritual blessings of believers in Christ — united as one body, called to walk in love, and equipped with armor to stand against spiritual forces.", "identity, unity, grace, spiritual warfare, love"),
    "Philippians": ("Joy in Every Circumstance", "Written from prison, Philippians is Paul's most joyful letter — teaching that contentment is possible in any situation because of the surpassing worth of knowing Christ Jesus.", "joy, contentment, humility, peace, unity"),
    "Colossians": ("Christ is Supreme", "Colossians exalts Jesus as supreme over all creation, all rulers, all philosophy, and all religion. The answer to every false teaching is always a bigger, clearer vision of who Christ really is.", "supremacy, identity, Christ, completeness, freedom"),
    "1 Thessalonians": ("Living While Waiting", "1 Thessalonians encourages a young church to live holy, loving lives while eagerly awaiting the return of Jesus — confident that those who have died in Christ will rise first.", "hope, holiness, return, encouragement, community"),
    "2 Thessalonians": ("Stand Firm", "2 Thessalonians clarifies misunderstandings about Christ's return and encourages believers to stand firm against deception and idleness while waiting with confident, working faith.", "perseverance, truth, discernment, hope, diligence"),
    "1 Timothy": ("Leading Well", "1 Timothy is Paul's pastoral handbook for young Timothy — covering church leadership, prayer, sound doctrine, and how to handle difficult people with truth and grace.", "leadership, doctrine, church, integrity, prayer"),
    "2 Timothy": ("Finish Strong", "Written from Paul's final imprisonment before his execution, 2 Timothy is a charge to the next generation: guard the gospel, endure hardship, and finish strong in a world drifting from truth.", "perseverance, courage, gospel, legacy, faithfulness"),
    "Titus": ("Grace Transforms Behavior", "Titus instructs a church leader on Crete — an island known for immorality — that God's grace is not just a belief to hold but a power that trains us to live differently.", "grace, character, leadership, sound doctrine, integrity"),
    "Philemon": ("Radical Forgiveness", "Philemon is Paul's short but powerful personal appeal for the forgiveness and restoration of a runaway slave, Onesimus — a real-life demonstration of the gospel's transforming power.", "forgiveness, reconciliation, grace, brotherhood, mercy"),
    "Hebrews": ("Jesus is Better", "Hebrews was written to Jewish believers tempted to abandon Christianity — making the comprehensive case that Jesus is greater than angels, Moses, the Levitical priesthood, and every old covenant institution.", "supremacy, faith, perseverance, covenant, priesthood"),
    "James": ("Faith that Works", "James is the New Testament's book of practical wisdom — insisting that genuine faith always produces visible, tangible fruit in how we treat people, use our words, and spend our money.", "faith, works, wisdom, speech, integrity"),
    "1 Peter": ("Hope in Suffering", "1 Peter was written to persecuted Christians scattered across the empire, calling them to maintain their identity as God's holy people and to see their suffering as a path to glory — just as Jesus did.", "suffering, hope, identity, holiness, submission"),
    "2 Peter": ("Guard the Truth", "2 Peter warns against the danger of false teachers who twist Scripture and exploit believers. Peter's antidote: grow in the knowledge of Christ and remember the sure word of prophecy.", "discernment, truth, growth, judgment, knowledge"),
    "1 John": ("Love One Another", "1 John tests the reality of Christian profession by three measures: doctrine (what you believe about Jesus), righteousness (how you live), and love (how you treat fellow believers).", "love, assurance, truth, fellowship, light"),
    "2 John": ("Walk in Truth and Love", "This brief letter urges believers to walk in the truth of Jesus Christ as fully human and divine, and to refuse hospitality to those who deny it — because truth and love are not opposites.", "truth, love, discernment, protection, doctrine"),
    "3 John": ("Support Those Who Go", "3 John commends Gaius for his generous support of traveling missionaries, rebukes a power-hungry church leader, and praises faithful Demetrius — a snapshot of the early church's mission network.", "hospitality, faithfulness, truth, mission, community"),
    "Jude": ("Contend for the Faith", "Jude is a fierce warning against false teachers who have 'crept in unnoticed,' calling believers to contend earnestly for the faith once delivered to the saints.", "discernment, truth, judgment, mercy, contend"),
    "Revelation": ("The Victory of the Lamb", "Revelation is God's dramatic final word — a vision of history's destination. Despite its vivid imagery of tribulation, its core message is clear: the Lamb who was slain is Lord of all, and He wins.", "victory, hope, worship, judgment, eternity")
}

def slugify(book, chapter):
    return f"{book.lower().replace(' ', '-')}-{chapter}"

def build_page(book_name, chap_idx, verses, prev_slug, next_slug, total_chapters, footnotes=None):
    if footnotes is None: footnotes = {}
    chap_num = chap_idx + 1
    slug = slugify(book_name, chap_num)
    title_tag, book_intro, keywords = BOOK_INTROS.get(book_name, ("Scripture", f"{book_name} is part of the Holy Bible.", "Bible, scripture, faith"))
    ref = f"{book_name} {chap_num}"
    first_verse = verses[0][:160] if verses else ""
    last_verse_num = len(verses)

    # JSON-LD schema with every verse
    verse_parts = [{"@type":"CreativeWork","name":f"{book_name} {chap_num}:{i+1}","text":v,"position":i+1} for i,v in enumerate(verses)]
    schema = {
        "@context":"https://schema.org","@type":"WebPage",
        "name":f"{ref} - Read, Listen & Reflect | Rooted Daily",
        "description":f"Read {ref} with audio narration. {first_verse[:120]}",
        "url":f"{SITE_URL}/verses/{slug}.html",
        "keywords":keywords,
        "publisher":{"@type":"Organization","name":"Rooted Daily","url":SITE_URL},
        "mainEntity":{
            "@type":"Book","name":"Holy Bible","bookEdition":"WEB",
            "hasPart":{
                "@type":"Chapter","name":ref,"position":chap_num,
                "hasPart":verse_parts
            }
        }
    }

    # Visible verse HTML
    verses_html_parts = []
    for i, v in enumerate(verses):
        v_num = str(i + 1)
        sup_tag = ""
        if v_num in footnotes:
            has_content = any(
                (fn.get("content") or fn.get("text") or fn.get("note") or fn.get("body") or "").strip()
                for fn in footnotes[v_num]
            )
            if has_content:
                sup_tag = f'<a href="#fn-{chap_num}-{v_num}" onclick="openFnSheet(event, \'fn-{chap_num}-{v_num}\')" style="text-decoration:none;"><sup class="fn-marker" style="color:var(--accent);margin-left:2px;cursor:pointer;" title="See footnotes below">*</sup></a>'
        verses_html_parts.append(f'<p class="verse" id="v{i+1}"><sup class="vnum">{i+1}</sup><span class="vtext">{v}{sup_tag}</span></p>')
    verses_html = "\n".join(verses_html_parts)


    footnotes_html = ""
    fn_items_html = ""
    for v_num, fns in sorted(footnotes.items(), key=lambda x: int(x[0])):
        for fn in fns:
            content = fn.get("content") or fn.get("text") or fn.get("note") or fn.get("body") or ""
            if not content.strip():
                continue
            fn_items_html += f'<div class="fn-item" id="fn-{chap_num}-{v_num}" style="background:var(--bg-card);padding:1rem;border-radius:8px;border-left:3px solid var(--accent);"><strong style="color:var(--accent);font-family:\'Inter\',sans-serif;font-size:0.85rem;">{book_name} {chap_num}:{v_num}</strong><p style="font-size:0.95rem;color:var(--text-muted);margin-top:0.4rem;">{content}</p></div>'

    if fn_items_html:
        footnotes_html = f'<div class="footnotes-section" style="margin-top:2rem;padding-top:2rem;border-top:1px solid var(--border);"><h3>📖 Living Legacy Study Bible</h3><div class="footnotes-list" style="display:flex;flex-direction:column;gap:1rem;margin-top:1rem;">{fn_items_html}</div></div>'

    prev_link = f'<a class="nav-pill" href="{prev_slug}.html">&#8592; Prev</a>' if prev_slug else '<span class="nav-pill disabled">&#8592; Prev</span>'
    next_link = f'<a class="nav-pill" href="{next_slug}.html">Next &#8594;</a>' if next_slug else '<span class="nav-pill disabled">Next &#8594;</span>'
    reader_link = f"../bible.html?book={book_name.replace(' ', '+')}&chapter={chap_num}"

    # Chapter navigation within book (Show all chapters for maximum crawlability)
    chap_nav = "".join(
        f'<a class="chap-dot {"active" if i == chap_idx else ""}" href="{slugify(book_name, i+1)}.html">{i+1}</a>'
        for i in range(total_chapters)
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{ref} - {title_tag} | Rooted Daily</title>
    <meta name="description" content="Read {ref} ({last_verse_num} verses) with neural audio narration and AI reflection. {first_verse[:110]}...">
    <meta name="keywords" content="{book_name}, {ref}, {keywords}, Bible verse, scripture, audio Bible, Rooted Daily">
    <link rel="canonical" href="{SITE_URL}/verses/{slug}.html">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-HSEJQQEFLJ"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-HSEJQQEFLJ');
    </script>

    <meta property="og:type" content="article">
    <meta property="og:title" content="{ref} — {title_tag} | Rooted Daily">
    <meta property="og:description" content="{first_verse[:150]}">
    <meta property="og:url" content="{SITE_URL}/verses/{slug}.html">
    <meta property="og:image" content="{SITE_URL}/hero-bg.png">
    <meta property="twitter:card" content="summary_large_image">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script type="application/ld+json">{json.dumps(schema)}</script>

    <style>
        :root {{
            --bg:#111827;--bg-card:#1a2332;--bg-nav:#1e2d3d;
            --text:#f0f4f8;--text-muted:#6b7f96;
            --accent:#4a735d;--accent-glow:rgba(74,115,93,0.3);
            --border:rgba(255,255,255,0.08);
        }}
        html{{scroll-behavior:smooth;}}
        *{{margin:0;padding:0;box-sizing:border-box;}}
        body{{font-family:'Crimson Text',serif;background:var(--bg);color:var(--text);line-height:1.9;}}
        a{{color:inherit;text-decoration:none;}}

        /* HEADER */
        header{{
            background:var(--bg-nav);border-bottom:1px solid var(--border);
            padding:0 1.5rem;height:60px;
            display:flex;align-items:center;justify-content:space-between;
            position:sticky;top:0;z-index:100;backdrop-filter:blur(10px);
        }}
        .logo{{font-size:1.5rem;font-weight:700;color:var(--accent);}}
        .listen-btn{{
            background:var(--accent);color:white;border:none;
            padding:0.55rem 1.2rem;border-radius:20px;
            font-family:'Inter',sans-serif;font-weight:700;font-size:0.85rem;
            cursor:pointer;display:inline-flex;align-items:center;gap:0.4rem;
            transition:all 0.2s;
        }}
        .listen-btn:hover{{transform:translateY(-1px);box-shadow:0 4px 15px var(--accent-glow);}}

        /* HERO */
        .hero{{
            text-align:center;padding:3rem 1.5rem 2rem;
            border-bottom:1px solid var(--border);
        }}
        .book-label{{
            font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;
            letter-spacing:0.15em;text-transform:uppercase;
            color:var(--accent);margin-bottom:0.5rem;
        }}
        h1{{font-size:clamp(2rem,5vw,3rem);font-weight:600;margin-bottom:0.5rem;}}
        .meta{{font-family:'Inter',sans-serif;font-size:0.85rem;color:var(--text-muted);margin-bottom:1.5rem;}}

        /* CHAPTER DOT NAV */
        .chap-nav{{display:flex;flex-wrap:wrap;justify-content:center;gap:0.4rem;margin-top:1rem;}}
        .chap-dot{{
            width:32px;height:32px;border-radius:50%;
            background:var(--bg-card);border:1px solid var(--border);
            display:inline-flex;align-items:center;justify-content:center;
            font-family:'Inter',sans-serif;font-size:0.75rem;font-weight:600;
            color:var(--text-muted);transition:all 0.2s;
        }}
        .chap-dot:hover,.chap-dot.active{{background:var(--accent);color:white;border-color:var(--accent);}}

        /* BOOK INTRO */
        .book-intro{{
            background:var(--bg-card);border:1px solid var(--border);
            border-left:3px solid var(--accent);
            border-radius:0 16px 16px 0;
            padding:1.25rem 1.5rem;margin:2rem 0;
        }}
        .book-intro h3{{font-family:'Inter',sans-serif;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--accent);margin-bottom:0.5rem;}}
        .book-intro p{{font-size:1.1rem;color:var(--text-muted);line-height:1.7;}}
        .keywords{{margin-top:0.75rem;display:flex;flex-wrap:wrap;gap:0.4rem;}}
        .kw{{
            background:var(--accent-glow);border:1px solid var(--accent);
            color:var(--accent);border-radius:20px;
            padding:0.2rem 0.75rem;
            font-family:'Inter',sans-serif;font-size:0.75rem;font-weight:600;
        }}

        /* VERSES */
        main{{max-width:680px;margin:0 auto;padding:2rem 1.5rem 8rem;}}
        .verse{{
            margin-bottom:1.1rem;padding:0.6rem 0.75rem;
            border-radius:6px;cursor:pointer;transition:background 0.2s;
        }}
        .verse:hover{{background:rgba(74,115,93,0.08);}}
        .vnum{{
            font-family:'Inter',sans-serif;font-size:0.6rem;font-weight:800;
            color:var(--accent);vertical-align:super;margin-right:0.3rem;opacity:0.7;
        }}
        .vtext{{font-size:1.2rem;}}

        /* AI SECTION */
        .ai-section{{
            background:var(--bg-card);border:1px solid var(--border);
            border-radius:20px;padding:1.75rem;margin:2.5rem 0;
        }}
        .ai-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;}}
        .ai-header h3{{
            font-family:'Inter',sans-serif;font-size:0.75rem;font-weight:700;
            letter-spacing:0.1em;text-transform:uppercase;color:var(--accent);
        }}
        .ai-btn{{
            background:var(--accent);color:white;border:none;
            padding:0.55rem 1.25rem;border-radius:20px;
            font-family:'Inter',sans-serif;font-weight:700;font-size:0.82rem;
            cursor:pointer;display:flex;align-items:center;gap:0.4rem;
            transition:all 0.2s;
        }}
        .ai-btn:hover{{transform:translateY(-1px);box-shadow:0 4px 15px var(--accent-glow);}}
        .ai-btn:disabled{{opacity:0.6;transform:none;cursor:default;}}
        .ai-response{{
            font-size:1.1rem;line-height:1.85;color:var(--text-muted);
            display:none;margin-top:1rem;
            border-top:1px solid var(--border);padding-top:1rem;
        }}
        .ai-response.visible{{display:block;}}
        .ai-prompt-form{{display:none;margin-top:1rem;}}
        .ai-prompt-form.visible{{display:flex;gap:0.5rem;}}
        .ai-input{{
            flex:1;padding:0.7rem 1rem;
            background:var(--bg);border:1px solid var(--border);
            border-radius:12px;color:var(--text);
            font-family:'Inter',sans-serif;font-size:0.9rem;
        }}
        .ai-input:focus{{outline:none;border-color:var(--accent);}}
        .api-setup{{
            font-family:'Inter',sans-serif;font-size:0.85rem;color:var(--text-muted);
            margin-top:0.75rem;display:none;
        }}
        .api-setup.visible{{display:block;}}
        .api-setup input{{
            width:100%;margin-top:0.5rem;padding:0.65rem 1rem;
            background:var(--bg);border:1px solid var(--border);
            border-radius:10px;color:var(--text);
            font-family:'Inter',sans-serif;font-size:0.85rem;
        }}
        .api-setup input:focus{{outline:none;border-color:var(--accent);}}

        /* BOTTOM NAV */
        .bottom-nav{{
            position:fixed;bottom:0;left:0;right:0;
            background:linear-gradient(to top,var(--bg) 70%,transparent);
            padding:1.25rem 1.5rem 1.5rem;
            display:flex;align-items:center;justify-content:space-between;
            z-index:50;
        }}
        .nav-pill{{
            background:var(--bg-card);border:1px solid var(--border);
            padding:0.65rem 1.3rem;border-radius:20px;
            font-family:'Inter',sans-serif;font-weight:600;font-size:0.9rem;
            color:var(--text);transition:all 0.2s;
        }}
        .nav-pill:hover{{background:var(--accent);border-color:var(--accent);color:white;}}
        .nav-pill.disabled{{opacity:0.3;pointer-events:none;}}

        /* FOOTER */
        footer{{
            text-align:center;padding:2rem 1.5rem;
            font-family:'Inter',sans-serif;font-size:0.8rem;color:var(--text-muted);
            border-top:1px solid var(--border);
        }}
        footer a{{color:var(--accent);}}

        @media(max-width:600px){{
            h1{{font-size:2rem;}}
            main{{padding:1.5rem 1rem 8rem;}}
        }}

        /* FOOTNOTE BOTTOM SHEET */
        .fn-sheet {{
            position: fixed; bottom: -100%; left: 0; right: 0;
            background: rgba(30, 45, 61, 0.97); backdrop-filter: blur(16px);
            border-top: 1px solid var(--border); border-radius: 24px 24px 0 0;
            padding: 0.75rem 1.5rem 2.5rem; z-index: 1000;
            transition: bottom 0.32s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 -4px 30px rgba(0,0,0,0.5);
            pointer-events: none;
        }}
        .fn-sheet.open {{ bottom: 0; pointer-events: all; }}
        .fn-sheet-handle {{
            width: 36px; height: 4px; background: var(--border);
            border-radius: 2px; margin: 0 auto 1rem;
        }}
        .fn-sheet-close {{
            position: absolute; top: 1rem; right: 1.5rem;
            background: transparent; border: none; color: var(--text-muted);
            font-size: 1.1rem; cursor: pointer;
        }}
        .fn-sheet-inner {{
            max-height: 45vh; overflow-y: auto; padding-bottom: 1rem;
        }}
    </style>
</head>
<body>

<header>
    <a class="logo" href="../index.html">Rooted</a>
    <div style="display:flex;gap:1.5rem;align-items:center;">
        <a href="../bible-index.html" style="font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:700;color:var(--text-muted);text-decoration:none;">Library Index</a>
        <a class="listen-btn" href="{reader_link}">&#9654; Listen &amp; Reflect</a>
    </div>
</header>

<div class="hero">
    <div class="book-label">{book_name.upper()} &mdash; CHAPTER {chap_num} OF {total_chapters}</div>
    <h1>{ref}</h1>
    <p class="meta">{last_verse_num} verses &middot; World English Bible &middot; Audio + AI Reflection available</p>
    <div class="chap-nav">{chap_nav}</div>
</div>

<main>

    <div class="book-intro">
        <h3>About {book_name}</h3>
        <p>{book_intro}</p>
        <div class="keywords">
            {"".join(f'<span class="kw">{k.strip()}</span>' for k in keywords.split(","))}
        </div>
    </div>

    <article>
        {verses_html}
    </article>
    
    {footnotes_html}

    <!-- AI EXPLANATION SECTION -->
    <div class="ai-section">
        <div class="ai-header">
            <h3>&#10024; AI Reflection Guide</h3>
            <button class="ai-btn" id="explainBtn" onclick="generateExplanation()">
                Explain This Chapter
            </button>
        </div>
        <p style="font-family:'Inter',sans-serif;font-size:0.9rem;color:var(--text-muted);">
            Get an instant AI-powered explanation of {ref} — including key themes, historical context, and how to apply it to your life today.
        </p>
        <div class="api-setup" id="apiSetup">
            <strong>Enter your free Gemini API key to unlock AI explanations:</strong><br>
            <small>Get yours free at <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:var(--accent);">aistudio.google.com</a></small>
            <input type="password" id="apiKeyInput" placeholder="Paste your Gemini API key here..." oninput="saveKey(this.value)">
        </div>
        <div class="ai-prompt-form" id="promptForm">
            <input class="ai-input" id="customPrompt" placeholder="e.g. Apply this to dealing with anxiety...">
            <button class="ai-btn" onclick="askCustom()">Ask</button>
        </div>
        <div class="ai-response" id="aiResponse"></div>
    </div>

</main>

<div class="bottom-nav">
    {prev_link}
    <a class="nav-pill" href="{reader_link}" style="background:var(--accent);border-color:var(--accent);color:white;">
        &#9654; Full Reader
    </a>
    {next_link}
</div>

<footer>
    <p>&copy; 2026 <a href="../index.html">Rooted Daily</a> &middot; <a href="../terms.html">Terms</a> &middot; <a href="../privacy.html">Privacy</a> &middot; <a href="../sitemap.xml">Sitemap</a></p>
</footer>

<div id="fn-sheet" class="fn-sheet">
    <div class="fn-sheet-handle"></div>
    <button class="fn-sheet-close" onclick="closeFnSheet()">✕</button>
    <div id="fn-sheet-body" style="margin-top:0.5rem; max-height:40vh; overflow-y:auto; padding-bottom:2rem;"></div>
</div>

<script>
    function openFnSheet(e, id) {{
        e.preventDefault();
        const content = document.getElementById(id).innerHTML;
        document.getElementById('fn-sheet-body').innerHTML = content;
        document.getElementById('fn-sheet').classList.add('open');
    }}
    function closeFnSheet() {{
        document.getElementById('fn-sheet').classList.remove('open');
    }}

    const BOOK = "{book_name}";
    const CHAPTER = {chap_num};
    const REF = "{ref}";
    const GEMINI_KEY = "{API_KEY}";

    async function generateExplanation(prompt) {{
        if (!GEMINI_KEY) {{
            document.getElementById('aiResponse').innerHTML = '⚠️ AI explanations are not yet configured. Check back soon!';
            document.getElementById('aiResponse').classList.add('visible');
            return;
        }}
        const btn = document.getElementById('explainBtn');
        btn.textContent = 'Thinking...';
        btn.disabled = true;

        const userPrompt = prompt || `Explain {ref} from the Bible in a warm, accessible way. Cover:
1. What is happening in this chapter (context in 1-2 sentences)
2. The key spiritual insight or lesson (2-3 sentences)
3. How someone can apply this to their life today (2-3 sentences)
Keep the tone warm, grounded, and non-denominational. Begin with the chapter reference.`;

        try {{
            const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${{GEMINI_KEY}}`, {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    contents: [{{parts: [{{text: userPrompt}}]}}],
                    generationConfig: {{temperature: 0.7, maxOutputTokens: 600}}
                }})
            }});
            const data = await res.json();
            if (data.error) throw new Error(data.error.message);
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response received.';
            const el = document.getElementById('aiResponse');
            el.innerHTML = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>').replace(/\\n/g, '<br>');
            el.classList.add('visible');
            document.getElementById('promptForm').classList.add('visible');
            btn.textContent = '&#10024; Refresh';
            btn.disabled = false;
        }} catch(e) {{
            document.getElementById('aiResponse').innerHTML = '⚠️ ' + e.message;
            document.getElementById('aiResponse').classList.add('visible');
            btn.textContent = 'Try Again';
            btn.disabled = false;
        }}
    }}

    function askCustom() {{
        const q = document.getElementById('customPrompt').value.trim();
        if (!q) return;
        generateExplanation(`Regarding {ref}: ${{q}}. Please give a thoughtful, grounded, scripture-rooted answer in 3-4 sentences.`);
        document.getElementById('customPrompt').value = '';
    }}
</script>
</body>
</html>'''


def main():
    print("Loading bible.json...")
    with open("data/bible.json","r",encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_chapters = [(bi, ci) for bi, book in enumerate(data["books"]) for ci in range(len(book["chapters"]))]

    sitemap_urls = []
    total = 0

    for idx, (bi, ci) in enumerate(all_chapters):
        book_name = BOOK_NAMES[bi]
        verses = data["books"][bi]["chapters"][ci]
        chap_num = ci + 1
        slug = slugify(book_name, chap_num)

        prev_slug = f"../{OUTPUT_DIR}/{slugify(BOOK_NAMES[all_chapters[idx-1][0]], all_chapters[idx-1][1]+1)}" if idx > 0 else None
        next_slug = f"../{OUTPUT_DIR}/{slugify(BOOK_NAMES[all_chapters[idx+1][0]], all_chapters[idx+1][1]+1)}" if idx < len(all_chapters)-1 else None
        total_chaps = len(data["books"][bi]["chapters"])

        footnotes = data["books"][bi].get("footnotes", {}).get(str(chap_num), {})

        html = build_page(book_name, ci, verses, prev_slug, next_slug, total_chaps, footnotes)
        with open(os.path.join(OUTPUT_DIR, f"{slug}.html"),"w",encoding="utf-8") as f:
            f.write(html)

        sitemap_urls.append(f"{SITE_URL}/{OUTPUT_DIR}/{slug}.html")
        total += 1
        if total % 100 == 0:
            print(f"  {total} pages...")

    print("Writing sitemap.xml...")
    with open("sitemap.xml","w",encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for page in ["","bible.html","bible-index.html","terms.html","privacy.html"]:
            f.write(f'  <url><loc>{SITE_URL}/{page}</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n')
        for url in sitemap_urls:
            f.write(f'  <url><loc>{url}</loc><changefreq>monthly</changefreq><priority>0.9</priority></url>\n')
        f.write('</urlset>')

    print(f"\n✅ {total} pages generated in /{OUTPUT_DIR}/")
    print("✅ sitemap.xml updated")

if __name__ == "__main__":
    main()
