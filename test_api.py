import urllib.request, urllib.error, json, sys

API_KEY = sys.argv[1] if len(sys.argv) > 1 else ""

COMBOS = [
    ("v1", "gemini-2.5-flash"),
    ("v1", "gemini-2.5-pro"),
    ("v1", "gemini-2.0-flash"),
    ("v1", "gemini-2.0-flash-lite"),
    ("v1beta", "gemini-2.5-flash"),
    ("v1beta", "gemini-2.5-flash-preview-05-20"),
    ("v1beta", "gemini-2.0-flash-001"),
    ("v1beta", "gemini-1.0-pro"),
]

body = json.dumps({"contents":[{"parts":[{"text":"Say hello in one sentence."}]}]}).encode()

for api_ver, model in COMBOS:
    url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{model}:generateContent?key={API_KEY}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read())
            text = d["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ WORKS: [{api_ver}] {model}")
            print(f"   Response: {text[:80]}")
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f"✗ [{api_ver}] {model}: HTTP {e.code} - {err['error']['message'][:90]}")
    except Exception as e:
        print(f"✗ [{api_ver}] {model}: {type(e).__name__}: {str(e)[:80]}")
