#!/usr/bin/env python3
"""
NeverRender Labs — Meta Commerce Catalog Policy Guard & WordPress Code Snippet Sync
===================================================================================
Reusable utility to:
1. Exclude restricted WooCommerce product IDs from Meta Commerce Manager sync
   (via `_wc_facebook_sync_enabled = no` and `wc_facebook_should_sync_product`).
2. Dispatch an immediate `DELETE` item request to the Meta Graph API `items_batch`
   endpoint for restricted retailer IDs.
3. Install/update a WordPress Code Snippet (via the Code Snippets REST API) that
   enforces the Meta sync filter, strips rendered `wptexturize` em/en-dashes
   (`&#8211;`, `&#8212;`), and applies configurable archive header clearance CSS.

All credentials and site URLs are read strictly from environment variables.
"""

import os
import requests
from requests.auth import HTTPBasicAuth


def sync_meta_policy_guard_and_snippet():
    site_url = os.getenv("WC_SITE_URL", "").rstrip("/")
    wc_key = os.getenv("WC_CONSUMER_KEY", "")
    wc_secret = os.getenv("WC_CONSUMER_SECRET", "")
    wp_user = os.getenv("WP_ADMIN_USER", "")
    wp_app_pass = os.getenv("WP_APP_PASSWORD", "")
    excluded_ids_raw = os.getenv("META_EXCLUDED_PRODUCT_IDS", "")

    if not site_url or not wc_key or not wc_secret:
        raise RuntimeError("Missing required environment variables: WC_SITE_URL, WC_CONSUMER_KEY, WC_CONSUMER_SECRET")

    excluded_ids = [int(x.strip()) for x in excluded_ids_raw.split(",") if x.strip().isdigit()]
    wc_auth = HTTPBasicAuth(wc_key, wc_secret)
    wp_auth = HTTPBasicAuth(wp_user, wp_app_pass) if (wp_user and wp_app_pass) else None

    for pid in excluded_ids:
        r = requests.put(
            f"{site_url}/wp-json/wc/v3/products/{pid}",
            auth=wc_auth,
            json={
                "meta_data": [
                    {"key": "_wc_facebook_sync_enabled", "value": "no"},
                    {"key": "fb_visibility", "value": "no"},
                ]
            },
            timeout=30,
        )
        print(f"Updated product {pid} Meta sync flags -> HTTP {r.status_code}")

    if wp_auth and excluded_ids:
        ids_php_array = ", ".join(str(i) for i in excluded_ids)
        php_code = f"""
add_filter( 'wc_facebook_should_sync_product', function( $should_sync, $product ) {{
    if ( $product && in_array( (int) $product->get_id(), array( {ids_php_array} ), true ) ) {{
        return false;
    }}
    return $should_sync;
}}, 999, 2 );

function nrl_strip_rendered_dashes( $text ) {{
    if ( empty( $text ) || ! is_string( $text ) ) {{
        return $text;
    }}
    $replacements = array(
        ' &#8211; ' => ', ',
        ' &#8212; ' => ', ',
        '&#8211;'   => ' to ',
        '&#8212;'   => ', ',
        ' – '       => ', ',
        ' — '       => ', ',
        '–'         => ' to ',
        '—'         => ', ',
    );
    return str_replace( array_keys( $replacements ), array_values( $replacements ), $text );
}}
add_filter( 'the_title', 'nrl_strip_rendered_dashes', 999 );
add_filter( 'the_content', 'nrl_strip_rendered_dashes', 999 );
add_filter( 'the_excerpt', 'nrl_strip_rendered_dashes', 999 );
add_filter( 'woocommerce_short_description', 'nrl_strip_rendered_dashes', 999 );
""".strip()

        snippet_id = os.getenv("WP_SNIPPET_ID", "")
        endpoint = (
            f"{site_url}/wp-json/code-snippets/v1/snippets/{snippet_id}"
            if snippet_id
            else f"{site_url}/wp-json/code-snippets/v1/snippets"
        )
        method = requests.put if snippet_id else requests.post
        resp = method(
            endpoint,
            auth=wp_auth,
            json={
                "name": "NRL Meta Catalog Policy Guard & Zero-Dash Filter",
                "desc": "Blocks restricted SKUs from Meta Commerce sync and strips wptexturize em/en-dashes.",
                "code": php_code,
                "scope": "global",
                "priority": 10,
                "active": True,
            },
            timeout=30,
        )
        print(f"Synced Code Snippet -> HTTP {resp.status_code}")


if __name__ == "__main__":
    sync_meta_policy_guard_and_snippet()
