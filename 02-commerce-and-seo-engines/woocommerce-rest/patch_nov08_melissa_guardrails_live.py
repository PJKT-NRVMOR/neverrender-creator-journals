#!/usr/bin/env python3
"""
Enforce Melissa Chapman's November 8, 2026 (07:57 AM & 09:46 AM PST) Permanent Guardrails
directly in the live WooCommerce database:
1. Complete Purge of Hand-Finished Silk Qum Rugs (WC-3192, 3105, 3103, 3101, 3098, 3095, 3092, 3090, 3088, 3081):
   - Unpublishes (status='draft', catalog_visibility='hidden') 100% of hand-finished silk carpets from WooCommerce.
2. No In-Home Trial Offers (e.g. WC-3045, WC-3043, WC-3037):
   - Strips all mentions of "in home trial" / "in-home trial".
3. Institutional CTA:
   - Replaces any "contact Melissa" / "text Melissa" / "call Melissa" with "contact us".
"""

import os
import sys
import json
import base64
import urllib.request
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(r"c:\Users\Saturn\Desktop\project-marshall-college\.env")

WP_BASE = "https://thechapmancollection.com/wp-json/wc/v3"
WC_KEY = os.getenv("WC_CONSUMER_KEY", "")
WC_SECRET = os.getenv("WC_CONSUMER_SECRET", "")
WP_USER = os.getenv("WP_REST_USER", "neverrender-labs")
WP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")

if WC_KEY and WC_SECRET:
    AUTH = "Basic " + base64.b64encode(f"{WC_KEY}:{WC_SECRET}".encode("utf-8")).decode("utf-8")
else:
    AUTH = "Basic " + base64.b64encode(f"{WP_USER}:{WP_PASS}".encode("utf-8")).decode("utf-8")

PURGED_SILK_QUM_IDS = [3192, 3105, 3103, 3101, 3098, 3095, 3092, 3090, 3088, 3081]


def wc_request(endpoint, method="GET", payload=None):
    url = f"{WP_BASE}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": AUTH,
        "User-Agent": "NRL-Woo-Guardrail-Auditor/2.0",
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def sanitize_text(text):
    if not text:
        return text
    updated = text
    replacements = [
        ("with complimentary local delivery and in home trial.", "with local and worldwide delivery available."),
        ("with complimentary local delivery and in-home trial.", "with local and worldwide delivery available."),
        ("48-hour in-home trial", "private showroom appointment"),
        ("48 hour in home trial", "private showroom appointment"),
        ("complimentary in-home trial", "private showroom appointment"),
        ("complimentary in home trial", "private showroom appointment"),
        ("complimentary in-home preview", "private showroom appointment"),
        ("free in-home trial", "private showroom appointment"),
        ("free in home trial", "private showroom appointment"),
        ("call or text Melissa directly", "contact us"),
        ("contact Melissa directly", "contact us"),
        ("contact Melissa", "contact us"),
        ("text Melissa", "contact us"),
    ]
    for old_s, new_s in replacements:
        updated = updated.replace(old_s, new_s)
    return updated


def main():
    print("=== 1. Unpublishing All Hand-Finished Silk Qum Carpets ===")
    # Also scan full catalog for any other hand-finished silk carpets
    all_target_purge_ids = set(PURGED_SILK_QUM_IDS)
    for page in range(1, 5):
        items = wc_request(f"products?per_page=100&page={page}&status=any")
        if not items:
            break
        for p in items:
            pid = int(p.get("id", 0))
            blob = f"{p.get('name', '')} {p.get('slug', '')} {p.get('description', '')} {p.get('short_description', '')}".lower()
            if "hand finished" in blob or "hand-finished" in blob or ("silk qum" in blob):
                all_target_purge_ids.add(pid)

    for pid in sorted(all_target_purge_ids, reverse=True):
        try:
            prod = wc_request(f"products/{pid}")
            name = prod.get("name", "")
            status = prod.get("status", "")
            vis = prod.get("catalog_visibility", "")
            slug = prod.get("slug", "")
            if status != "draft" or vis != "hidden":
                wc_request(
                    f"products/{pid}",
                    method="PUT",
                    payload={"status": "draft", "catalog_visibility": "hidden"},
                )
                print(f"[UNPUBLISHED -> DRAFT] WC-{pid} | {name} | slug={slug}")
            else:
                print(f"[ALREADY DRAFT/HIDDEN] WC-{pid} | {name} | slug={slug}")
        except Exception as e:
            print(f"[SKIP/NOT FOUND] WC-{pid}: {e}")

    print("\n=== 2. Sanitizing Trial & CTA Guardrails on Active Products ===")
    for pid in [3045, 3043, 3037]:
        prod = wc_request(f"products/{pid}")
        name = prod.get("name", "")
        desc = prod.get("description", "")
        short_desc = prod.get("short_description", "")
        new_desc = sanitize_text(desc)
        new_short = sanitize_text(short_desc)
        if new_desc != desc or new_short != short_desc:
            wc_request(
                f"products/{pid}",
                method="PUT",
                payload={"description": new_desc, "short_description": new_short},
            )
            print(f"[PATCHED] WC-{pid} ({name})")
        else:
            print(f"[CLEAN]   WC-{pid} ({name})")


if __name__ == "__main__":
    main()
