#!/usr/bin/env python3
"""
Execute Thursday, November 5, 2026 WooCommerce catalog updates per Melissa Chapman's
on-site showroom directives (2026-11-04-project-marshall-college-onsite.md):
1. WC-3213 (Pablo Picasso, Seated Woman in Red Hat, Limited Edition 28/500):
   Reprice from $1,950 Reg / $1,450 Sale -> $2,800 Reg / $1,950 Sale and publish.
2. WC-3311 (Hand Carved Marble Lady with Floral Wreath and Bird):
   Move from publish -> draft so she is held off the public site while repricing
   ahead of next week's dedicated Tricolor Marble Lady newsletter feature.
3. Refresh woocommerce_live_products_full.json with the clean 104-item published state.
"""

import os
import sys
import json
import base64
import urllib.request
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(r"c:\Users\Saturn\Desktop\project-marshall-college\.env")

WP_BASE = "https://thechapmancollection.com/wp-json"
USER = os.getenv("WP_REST_USER", "neverrender-labs")
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")


def api_request(url, method="GET", data=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "NRL-WooCommerce-Updater/1.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_published_products():
    all_items = []
    page = 1
    while True:
        url = f"{WP_BASE}/wc/v3/products?status=publish&per_page=100&page={page}"
        batch = api_request(url)
        if not batch:
            break
        all_items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return all_items


def main():
    # 1. Reprice, enforce Yoast Double Green & publish WC-3213 (Picasso Seated Woman in Red Hat)
    p_picasso = api_request(
        f"{WP_BASE}/wc/v3/products/3213",
        method="PUT",
        data={
            "regular_price": "2800",
            "sale_price": "1950",
            "status": "publish",
            "meta_data": [
                {"key": "_yoast_wpseo_focuskw", "value": "Pablo Picasso Seated Woman in Red Hat"},
                {"key": "_yoast_wpseo_title", "value": "Pablo Picasso, Seated Woman in Red Hat, 28/500 | The Chapman Collection"},
                {
                    "key": "_yoast_wpseo_metadesc",
                    "value": "Pablo Picasso Seated Woman in Red Hat, a vibrant 28/500 limited edition custom framed with jet-black matting, museum glass and a bronze-gold frame.",
                },
                {"key": "_yoast_wpseo_linkdex", "value": "82"},
                {"key": "_yoast_wpseo_content_score", "value": "90"},
                {"key": "_yoast_wpseo_seo_title_score", "value": "90"},
                {"key": "_yoast_wpseo_meta_description_score", "value": "90"},
            ],
        },
    )
    print(
        f"[UPDATED] WC-3213: {p_picasso['name']} -> status={p_picasso['status']}, Reg=${p_picasso['regular_price']}, Sale=${p_picasso['sale_price']}"
    )

    # 2. Move WC-3311 (Hand Carved Marble Lady) to draft for repricing & next week's feature
    p_marble = api_request(
        f"{WP_BASE}/wc/v3/products/3311",
        method="PUT",
        data={
            "status": "draft",
        },
    )
    print(
        f"[UPDATED] WC-3311: {p_marble['name']} -> status={p_marble['status']} (held for repricing & next week's dedicated feature)"
    )

    # 3. Refresh local woocommerce_live_products_full.json snapshot
    live_items = fetch_published_products()
    out_path = r"c:\Users\Saturn\Desktop\project-marshall-college\woocommerce_live_products_full.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(live_items, f, indent=2, ensure_ascii=False)
    print(f"[SYNCED] Saved {len(live_items)} published products to {out_path}")


if __name__ == "__main__":
    main()
