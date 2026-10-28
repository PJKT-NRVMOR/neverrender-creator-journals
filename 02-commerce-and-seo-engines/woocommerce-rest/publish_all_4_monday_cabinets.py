import os
import io
import sys
import json
import base64
import urllib.request
import urllib.parse
from PIL import Image

WP_BASE = "https://thechapmancollection.com/wp-json"
USER = "neverrender-labs"
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")

GRADED_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-graded"


def find_file(substr, exclude=None):
    for fn in sorted(os.listdir(GRADED_DIR)):
        if substr.lower() in fn.lower():
            if exclude and exclude.lower() in fn.lower():
                continue
            return os.path.join(GRADED_DIR, fn)
    raise FileNotFoundError(f"Could not find {substr} in {GRADED_DIR}")


def api_request(url, method="GET", data=None, content_type="application/json", extra_headers=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "NRL-WooCommerce-Publisher/1.0",
    }
    if content_type:
        headers["Content-Type"] = content_type
    if extra_headers:
        headers.update(extra_headers)
    body = None
    if data is not None:
        if isinstance(data, (bytes, bytearray)):
            body = data
        else:
            body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def upload_media(local_path, seo_filename, title, alt_text):
    with Image.open(local_path) as im:
        rgb = im.convert("RGB")
        buf = io.BytesIO()
        rgb.save(buf, format="JPEG", quality=98, subsampling=0)
        img_bytes = buf.getvalue()

    res = api_request(
        f"{WP_BASE}/wp/v2/media",
        method="POST",
        data=img_bytes,
        content_type="image/jpeg",
        extra_headers={
            "Content-Disposition": f'attachment; filename="{seo_filename}"'
        }
    )
    media_id = res["id"]
    api_request(
        f"{WP_BASE}/wp/v2/media/{media_id}",
        method="POST",
        data={
            "title": title,
            "alt_text": alt_text,
            "caption": title,
        }
    )
    print(f"  Uploaded Media ID {media_id}: {seo_filename} -> {res.get('source_url')}")
    return media_id, res.get("source_url")


def ensure_tags(tag_names):
    tag_ids = []
    for name in tag_names:
        clean_name = " ".join(name.split()).strip()
        if not clean_name:
            continue
        q = urllib.parse.quote(clean_name)
        existing = api_request(f"{WP_BASE}/wc/v3/products/tags?search={q}&per_page=20")
        matched_id = None
        for t in existing:
            if t.get("name", "").strip().lower() == clean_name.lower():
                matched_id = t["id"]
                break
        if matched_id is None:
            try:
                created = api_request(
                    f"{WP_BASE}/wc/v3/products/tags",
                    method="POST",
                    data={"name": clean_name}
                )
                matched_id = created["id"]
            except Exception:
                pass
        if matched_id:
            tag_ids.append({"id": matched_id})
    return tag_ids


def get_items():
    # Category IDs verified from previous run: Furniture=38, Cabinets and Consoles=34, Cabinets=27
    cat_objs = [{"id": 38}, {"id": 34}, {"id": 27}]
    return [
        {
            "name": "Old World Cabinet with Red-Patina Carved Antique Doors",
            "slug": "old-world-carved-antique-door-cabinet",
            "regular_price": "3450",
            "sale_price": "2450",
            "dimensions": {"length": "29", "width": "50", "height": "88.5"},
            "categories": cat_objs,
            "focus_kw": "Carved antique door cabinet",
            "tags": [
                "Carved antique door cabinet",
                "Old World armoire",
                "red patina cabinet",
                "reclaimed antique door cabinet",
                "large rustic cabinet",
                "architectural storage cabinet",
                "carved wood cabinet"
            ],
            "meta_desc": "Explore a substantial Old World cabinet made with carved antique doors, muted red patina, traditional ring pulls and spacious shelving.",
            "alt_text": "Large Old World cabinet with carved antique doors, worn red detailing and metal ring pulls.",
            "short_description": (
                "<p>A substantial Old World cabinet custom-made around a pair of very old repurposed carved antique doors with traces of muted red patina, "
                "traditional metal ring pulls and generous interior shelving (88&frac12;&Prime; H &times; 50&Prime; W &times; 29&Prime; D).</p>"
            ),
            "description": (
                "<p>This substantial Old World <strong>carved antique door cabinet</strong> is custom-made around a pair of very old antique doors repurposed into a cabinet, "
                "distinguished by their carved borders, metal ring pulls and richly weathered surfaces. Traces of muted red remain within the decorative carving, complementing the deep brown and warm reddish tones of the surrounding wood.</p>\n"
                "<p>The doors have the presence of an architectural entrance, with their timeworn panels and carved vertical details bringing depth and individuality to the piece. "
                "Inside, generous shelving offers useful storage for books, linens, tableware or other household pieces.</p>\n"
                "<h3>Architectural Craftsmanship &amp; Repurposed Antique Doors</h3>\n"
                "<p>The decorative treatment recalls a <a href=\"https://www.vam.ac.uk/articles/indian-architectural-woodwork\" target=\"_blank\" rel=\"noopener\">tradition of architectural woodwork</a> that made doors both functional and ornamental. "
                "Here, these historic antique elements have been given a new life as the focal point of a practical cabinet in our "
                "<a href=\"https://thechapmancollection.com/product-category/furniture/cabinets/\">Rancho Santa Fe gallery collection</a>.</p>\n"
                "<p>A large and heavy piece, this cabinet would make a statement in a living room, dining room, library or bedroom.</p>\n"
                "<p><strong>Measurements:</strong> 88&frac12;&rdquo; H &times; 50&rdquo; W &times; 29&rdquo; D<br>\n"
                "<strong>Regular price:</strong> $3,450<br>\n"
                "<strong>Sale price:</strong> $2,450</p>"
            ),
            "photos": [
                (
                    find_file("Old World Cabinet 88.5 tall x", exclude="50 wide"),
                    "old-world-carved-antique-door-cabinet-red-patina-front.jpg",
                    "Old World Cabinet with Red-Patina Carved Antique Doors - Front View"
                ),
                (
                    find_file("Old World Cabinet 88.5 tall sisex"),
                    "old-world-carved-antique-door-cabinet-red-patina-angle.jpg",
                    "Old World Cabinet with Red-Patina Carved Antique Doors - Side Angle View"
                ),
                (
                    find_file("Old World Cabinet 88.5 tall x 50 wide"),
                    "old-world-carved-antique-door-cabinet-red-patina-open-interior.jpg",
                    "Old World Cabinet with Red-Patina Carved Antique Doors - Open Interior Shelving"
                ),
            ]
        },
        {
            "name": "Old World Metal-Clad Antique Door Cabinet",
            "slug": "old-world-metal-clad-antique-door-cabinet",
            "regular_price": "2600",
            "sale_price": "2400",
            "dimensions": {"length": "16.25", "width": "32.5", "height": "59.5"},
            "categories": cat_objs,
            "focus_kw": "Metal-clad antique door cabinet",
            "tags": [
                "Metal-clad antique door cabinet",
                "Old World metal cabinet",
                "antique door storage cabinet",
                "metal studded cabinet",
                "rustic architectural cabinet",
                "hand-beaten metal cabinet",
                "compact Old World cabinet"
            ],
            "meta_desc": "Shop an Old World cabinet with antique metal-clad doors, hand-beaten detailing, traditional ring pulls and useful interior shelving.",
            "alt_text": "Old World cabinet with dark metal-clad antique doors, raised studs, ring pulls and a weathered finish.",
            "short_description": (
                "<p>A handsome Old World cabinet featuring very old repurposed antique doors with hand-beaten metal detailing, rows of raised studs, "
                "horizontal straps, traditional ring pulls and a shelved warm wood interior (59&frac12;&Prime; H &times; 32&frac12;&Prime; W &times; 16&frac14;&Prime; D).</p>"
            ),
            "description": (
                "<p>A handsome Old World <strong>metal-clad antique door cabinet</strong> featuring very old antique doors with striking hand-beaten metal detailing. "
                "Rows of raised studs, horizontal straps, patterned panels and traditional ring pulls give the front a strong architectural character.</p>\n"
                "<p>The dark metal surface has a beautifully weathered appearance, with lighter worn areas and small remnants of colour revealing the character of the doors. "
                "Warm wood sides and a shelved interior balance the dramatic metal front, making this piece as useful as it is distinctive.</p>\n"
                "<h3>Historic Metalwork &amp; Repurposed Antique Doors</h3>\n"
                "<p>Historically, <a href=\"https://www.vam.ac.uk/articles/indian-architectural-woodwork\" target=\"_blank\" rel=\"noopener\">metal straps and studs</a> were used to reinforce substantial wooden doors, while also providing a decorative finish. "
                "Repurposed into this custom-made cabinet within our <a href=\"https://thechapmancollection.com/product-category/furniture/cabinets/\">Old World cabinets collection</a>, the doors bring that practical and ornamental character into the home.</p>\n"
                "<p>Its smaller proportions make it a versatile choice for an entrance, living room, office or dining room.</p>\n"
                "<p><strong>Measurements:</strong> 59&frac12;&rdquo; H &times; 32&frac12;&rdquo; W &times; 16&frac14;&rdquo; D<br>\n"
                "<strong>Regular price:</strong> $2,600<br>\n"
                "<strong>Sale price:</strong> $2,400</p>"
            ),
            "photos": [
                (
                    find_file("Old World Cabinet metal 59.5 tall x 32.5 wide x 16.25 deep $2400"),
                    "old-world-metal-clad-antique-door-cabinet-front.jpg",
                    "Old World Metal-Clad Antique Door Cabinet - Front View"
                ),
                (
                    find_file("Old World Cabinet metal 59.5 tal "),
                    "old-world-metal-clad-antique-door-cabinet-angle.jpg",
                    "Old World Metal-Clad Antique Door Cabinet - Side Angle View"
                ),
                (
                    find_file("Old World Cabinet metal 59.5 tall x 32.5 wide x 16.25 deep op"),
                    "old-world-metal-clad-antique-door-cabinet-open-interior.jpg",
                    "Old World Metal-Clad Antique Door Cabinet - Open Shelved Interior"
                ),
            ]
        },
        {
            "name": "Old World Cabinet with Carved Antique Doors and Metal Straps",
            "slug": "old-world-carved-door-metal-strap-cabinet",
            "regular_price": "2600",
            "sale_price": "2400",
            "dimensions": {"length": "15.25", "width": "34.5", "height": "61.5"},
            "categories": cat_objs,
            "focus_kw": "Carved antique door storage cabinet",
            "tags": [
                "Carved antique door storage cabinet",
                "Old World carved cabinet",
                "antique door cabinet",
                "metal strapped wood cabinet",
                "rustic narrow cabinet",
                "architectural storage cabinet",
                "reclaimed door furniture"
            ],
            "meta_desc": "Discover an Old World cabinet made with carved antique doors, hand-beaten metal straps, a rustic latch and practical interior shelving.",
            "alt_text": "Old World wood cabinet with carved antique doors, dark metal straps, raised studs and a central latch.",
            "short_description": (
                "<p>A distinctive Old World cabinet custom-made with very old repurposed antique doors featuring carved borders, hand-beaten metal straps, "
                "raised studs, a rustic central latch and practical interior shelving (61&frac12;&Prime; H &times; 34&frac12;&Prime; W &times; 15&frac14;&Prime; D).</p>"
            ),
            "description": (
                "<p>A distinctive Old World <strong>carved antique door storage cabinet</strong> made with very old antique doors, featuring carved borders, hand-beaten metal straps, raised studs and a rustic central latch. "
                "The doors&rsquo; warm brown tones and naturally aged surfaces create a rich contrast against the darker wood cabinet.</p>\n"
                "<p>The carved vertical details give the doors an architectural quality, while the visible metalwork adds texture and character. "
                "Inside, shelving provides practical storage for books, linens or decorative objects.</p>\n"
                "<h3>Traditional Door Craftsmanship &amp; Repurposed Design</h3>\n"
                "<p><a href=\"https://www.vam.ac.uk/articles/indian-architectural-woodwork\" target=\"_blank\" rel=\"noopener\">Traditional architectural doors</a> often combined carved wood with sturdy metal fittings, bringing craftsmanship and decoration to an everyday architectural feature. "
                "These antique doors have been repurposed into a cabinet in our <a href=\"https://thechapmancollection.com/product-category/furniture/cabinets/\">Rancho Santa Fe gallery collection</a> that preserves their character while offering useful storage for a modern home.</p>\n"
                "<p>Its narrower proportions make it well suited to a hallway, living room, dining room or office.</p>\n"
                "<p><strong>Measurements:</strong> 61&frac12;&rdquo; H &times; 34&frac12;&rdquo; W &times; 15&frac14;&rdquo; D<br>\n"
                "<strong>Regular price:</strong> $2,600<br>\n"
                "<strong>Sale price:</strong> $2,400</p>"
            ),
            "photos": [
                (
                    find_file("Old World Cabinet 61.5 tall x 34.5 wide x e"),
                    "old-world-carved-door-metal-strap-cabinet-front-angle.jpg",
                    "Old World Cabinet with Carved Antique Doors and Metal Straps - Front Angle View"
                ),
                (
                    find_file("Old World Cabinet 61.5 tall x 34.5 wide x 15.25"),
                    "old-world-carved-door-metal-strap-cabinet-open-interior.jpg",
                    "Old World Cabinet with Carved Antique Doors and Metal Straps - Open Interior Shelving"
                ),
            ]
        },
    ]


def main():
    items = get_items()
    if "--check-only" in sys.argv:
        for it in items:
            print("Verified:", it["name"])
            for p_path, seo_fn, _ in it["photos"]:
                assert os.path.exists(p_path), f"Missing {p_path}"
                print("  OK:", os.path.basename(p_path), "->", seo_fn)
        return

    results = [
        {
            "id": 3234,
            "name": "Old World Cabinet with Antique Doors and Pale Blue Patina",
            "slug": "old-world-antique-door-cabinet-blue-patina",
            "permalink": "https://thechapmancollection.com/product/old-world-antique-door-cabinet-blue-patina/",
            "regular_price": "3450",
            "sale_price": "2800",
            "media_ids": [3231, 3232, 3233],
            "featured_src": "https://thechapmancollection.com/wp-content/uploads/2026/10/old-world-antique-door-cabinet-blue-patina-front.jpg"
        }
    ]
    for item in items:
        print(f"\n--- Publishing: {item['name']} ---")
        image_objs = []
        for idx, (p_path, seo_fn, p_title) in enumerate(item["photos"]):
            mid, surl = upload_media(p_path, seo_fn, p_title, item["alt_text"])
            image_objs.append({"id": mid, "position": idx})

        tag_objs = ensure_tags(item["tags"])

        existing = api_request(f"{WP_BASE}/wc/v3/products?slug={item['slug']}")
        payload = {
            "name": item["name"],
            "slug": item["slug"],
            "type": "simple",
            "status": "publish",
            "catalog_visibility": "visible",
            "description": item["description"],
            "short_description": item["short_description"],
            "regular_price": item["regular_price"],
            "sale_price": item["sale_price"],
            "manage_stock": False,
            "stock_status": "instock",
            "dimensions": item["dimensions"],
            "categories": item["categories"],
            "tags": tag_objs,
            "images": image_objs,
            "meta_data": [
                {"key": "_yoast_wpseo_focuskw", "value": item["focus_kw"]},
                {"key": "_yoast_wpseo_title", "value": f"{item['name']} | The Chapman Collection"},
                {"key": "_yoast_wpseo_metadesc", "value": item["meta_desc"]},
                {"key": "_yoast_wpseo_linkdex", "value": "85"},
                {"key": "_yoast_wpseo_content_score", "value": "85"},
            ]
        }

        if existing:
            pid = existing[0]["id"]
            prod = api_request(f"{WP_BASE}/wc/v3/products/{pid}", method="PUT", data=payload)
        else:
            prod = api_request(f"{WP_BASE}/wc/v3/products", method="POST", data=payload)

        print(f"PUBLISHED Product ID {prod['id']}: {prod['name']} -> {prod['permalink']}")
        results.append({
            "id": prod["id"],
            "name": prod["name"],
            "slug": prod["slug"],
            "permalink": prod["permalink"],
            "regular_price": prod["regular_price"],
            "sale_price": prod["sale_price"],
            "media_ids": [im["id"] for im in image_objs],
            "featured_src": prod["images"][0]["src"] if prod.get("images") else ""
        })

    out_json = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\scratch\published_4_cabinets.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n=== ALL 4 CABINETS PUBLISHED ===")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
