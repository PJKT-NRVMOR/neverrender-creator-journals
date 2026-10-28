import os
import json
import base64
import urllib.request

WP_USER = "neverrender-labs"
WP_APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode()).decode()

SRC_DIR = r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\WEBSITE_MEDIA\tcc-oct23"

FILES = [
    ("crest.png", "tcc-oct23-crest.png", "image/png"),
    ("carpet-1-medallion.jpg", "tcc-oct23-carpet-1-medallion.jpg", "image/jpeg"),
    ("carpet-2-teal-silk.jpg", "tcc-oct23-carpet-2-teal-silk.jpg", "image/jpeg"),
    ("furn-1-french-desk.jpg", "tcc-oct23-furn-1-french-desk.jpg", "image/jpeg"),
    ("furn-2-french-commode.jpg", "tcc-oct23-furn-2-french-commode.jpg", "image/jpeg"),
    ("art-1-venice-oil.jpg", "tcc-oct23-art-1-venice-oil.jpg", "image/jpeg"),
    ("art-2-matisse-litho.jpg", "tcc-oct23-art-2-matisse-litho.jpg", "image/jpeg"),
    ("acc-1-grandfather-clock.jpg", "tcc-oct23-acc-1-grandfather-clock.jpg", "image/jpeg"),
    ("acc-2-vienna-urns.jpg", "tcc-oct23-acc-2-vienna-urns.jpg", "image/jpeg"),
    ("acc-3-dragon-vases.jpg", "tcc-oct23-acc-3-dragon-vases.jpg", "image/jpeg"),
    ("award-ranch-and-coast-2026.jpg", "tcc-oct23-award-ranch-and-coast-2026.jpg", "image/jpeg"),
]

uploaded_urls = {}

for local_name, wp_filename, mime in FILES:
    path = os.path.join(SRC_DIR, local_name)
    with open(path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(
        "https://thechapmancollection.com/wp-json/wp/v2/media",
        data=data,
        method="POST",
        headers={
            "Authorization": AUTH_HEADER,
            "Content-Type": mime,
            "Content-Disposition": f'attachment; filename="{wp_filename}"',
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        url = res_json.get("source_url")
        uploaded_urls[local_name] = url
        print(f"{local_name} -> {url}")

out_json = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\scratch\wp_uploaded_urls.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(uploaded_urls, f, indent=2)
print("Saved mapping to", out_json)
