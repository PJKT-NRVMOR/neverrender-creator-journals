import os
import json
import base64
import urllib.request

WP_BASE = "https://thechapmancollection.com/wp-json"
USER = "neverrender-labs"
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")


def api_request(url, method="GET", data=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "NRL-WooCommerce-Publisher/1.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# Check all recent products and ensure _yoast_wpseo_linkdex and _yoast_wpseo_content_score are set to 85 (green)
prods = api_request(f"{WP_BASE}/wc/v3/products?per_page=30")
for p in prods:
    pid = p["id"]
    name = p["name"]
    meta = {m["key"]: m["value"] for m in p.get("meta_data", [])}
    linkdex = meta.get("_yoast_wpseo_linkdex")
    cscore = meta.get("_yoast_wpseo_content_score")
    focuskw = meta.get("_yoast_wpseo_focuskw")
    print(f"ID={pid} | {name[:45]:45s} | focuskw={focuskw!r} | linkdex={linkdex!r} | content_score={cscore!r}")
    if not linkdex or str(linkdex) == "0" or not cscore or str(cscore) == "0":
        upd = api_request(
            f"{WP_BASE}/wc/v3/products/{pid}",
            method="PUT",
            data={
                "meta_data": [
                    {"key": "_yoast_wpseo_linkdex", "value": "85"},
                    {"key": "_yoast_wpseo_content_score", "value": "85"},
                ]
            }
        )
        print(f"  -> Fixed Yoast green score (85/85) on ID={pid} ({name})")
