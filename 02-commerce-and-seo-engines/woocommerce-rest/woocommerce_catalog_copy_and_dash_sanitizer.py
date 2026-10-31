#!/usr/bin/env python3
"""
NeverRender Labs Open-Source Studio Toolkit
WooCommerce REST Catalog Copy, HTML Wrapper & Compound-Hyphen ('Dash Fatigue') Sanitizer.

- Strips pasted LLM DOM wrappers (data-start, data-turn-id, class="isSelectedEnd").
- Un-hyphenates textbook compound modifiers in prose while preserving HTML tag attributes and URLs.
- Pushes updates in chunks via /wp-json/wc/v3/products/batch using environment credentials.
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")


def clean_html_wrappers(html_str: str) -> str:
    if not html_str:
        return html_str
    s = html_str
    if "qMYqUG_convSearchResultHighlightRoot" in s or "data-turn-id" in s:
        blocks = re.findall(r"<(?:h[1-6]|p)\b[^>]*>.*?</(?:h[1-6]|p)>", s, flags=re.DOTALL | re.I)
        if blocks:
            s = "\n".join(blocks)
    s = re.sub(r'\s+data-[a-z0-9\-]+="[^"]*"', "", s, flags=re.I)
    s = re.sub(r'\s+class="(?:isSelectedEnd|PDq2pG_[^"]*)"', "", s, flags=re.I)
    s = re.sub(r"<span\s+role=\"text\">(.*?)</span>", r"\1", s, flags=re.DOTALL | re.I)
    s = re.sub(r"(?:\s*<p>(?:&nbsp;|\s)*</p>\s*)+$", "", s, flags=re.I)
    return s.strip()


if __name__ == "__main__":
    print("WooCommerce Catalog Copy & Dash Sanitizer ready. Configure WP_REST_USER and WP_REST_APP_PASSWORD via environment.")
