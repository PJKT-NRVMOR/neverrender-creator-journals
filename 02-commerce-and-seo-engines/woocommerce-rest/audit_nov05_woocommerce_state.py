#!/usr/bin/env python3
"""
Audit the current live, draft, private, and trashed WooCommerce products on
thechapmancollection.com as of Thursday, November 5, 2026:
1. Identify which items Melissa deleted or moved to draft/trash last night.
2. Check exact status/pricing of:
   - WC-3177 (Mother-of-Pearl and Bone Inlaid Chest on Stand - SOLD in showroom)
   - Pablo Picasso, "Seated Woman in Red Hat" (to be repriced to $2,800 Reg / $1,950 Sale)
   - WC-3311 (Hand Carved Marble Lady with Floral Wreath and Bird - $9,800)
   - Tea sets / Porcelain sets on the website (for swapping Colleen's consignment set WC-3191)
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
        "User-Agent": "NRL-WooCommerce-Auditor/1.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all_by_status(status="any"):
    all_items = []
    page = 1
    while True:
        url = f"{WP_BASE}/wc/v3/products?status={status}&per_page=100&page={page}"
        batch = api_request(url)
        if not batch:
            break
        all_items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return all_items


def main():
    active_items = fetch_all_by_status("any")
    trash_items = fetch_all_by_status("trash")

    by_status = {}
    for p in active_items + trash_items:
        st = p.get("status", "unknown")
        by_status.setdefault(st, []).append(p)

    print("=== WOOCOMMERCE STATUS SUMMARY (2026-11-05) ===")
    for st, items in sorted(by_status.items()):
        print(f"  {st}: {len(items)} items")

    # Compare against previous local snapshot if available
    prev_path = r"c:\Users\Saturn\Desktop\project-marshall-college\woocommerce_live_products_full.json"
    if os.path.exists(prev_path):
        with open(prev_path, "r", encoding="utf-8") as f:
            prev_items = json.load(f)
        prev_map = {p["id"]: p for p in prev_items}
        curr_map = {p["id"]: p for p in active_items}

        missing_or_trashed = []
        for pid, old_p in prev_map.items():
            if pid not in curr_map:
                missing_or_trashed.append((pid, old_p.get("name"), "DELETED/TRASHED"))
            elif curr_map[pid].get("status") != old_p.get("status"):
                missing_or_trashed.append(
                    (pid, old_p.get("name"), f"{old_p.get('status')} -> {curr_map[pid].get('status')}")
                )

        print("\n=== DIFF VS PREVIOUS SNAPSHOT ===")
        for pid, name, change in missing_or_trashed:
            print(f"  [WC-{pid}] {name}: {change}")

    print("\n=== NON-PUBLISH ITEMS (DRAFT / PENDING / PRIVATE / TRASH) ===")
    for st in ("draft", "pending", "private", "trash"):
        for p in by_status.get(st, []):
            print(
                f"  [{st.upper()}] WC-{p['id']} | {p['name']} | Reg: ${p.get('regular_price')} | Sale: ${p.get('sale_price')} | Stock: {p.get('stock_status')}"
            )

    print("\n=== KEY TARGET ITEMS CHECK ===")
    keywords = ["mother-of-pearl", "chest", "picasso", "marble lady", "tea", "porcelain", "limoges", "sevres", "spode", "china"]
    for p in active_items + trash_items:
        name_l = p["name"].lower()
        if any(k in name_l for k in keywords) or p["id"] in (3177, 3311, 3191):
            print(
                f"  WC-{p['id']} [{p['status']}] | {p['name']} | Reg: ${p.get('regular_price')} | Sale: ${p.get('sale_price')} | Stock: {p.get('stock_status')} | CatalogVis: {p.get('catalog_visibility')}"
            )


if __name__ == "__main__":
    main()
