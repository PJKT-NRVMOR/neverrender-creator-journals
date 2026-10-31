"""
NRL WooCommerce EXIF-Safe Batch Publisher & Yoast Double-Green Engine
====================================================================
Client-agnostic utility for uploading EXIF-transposed product photography
to WordPress Media Library and publishing WooCommerce products with
complete Yoast SEO metadata and zero em-dash / en-dash sanitization.
"""

import os
import json
import base64
import urllib.request
import urllib.parse
from PIL import Image, ImageOps


def sanitize_text(t: str) -> str:
    if not t:
        return ""
    return (
        t.replace("\u2014", " - ")
        .replace("\u2013", "-")
        .replace("—", " - ")
        .replace("–", "-")
        .replace("&mdash;", " - ")
        .replace("&ndash;", "-")
    )


def normalize_exif_jpeg(src_path: str, dst_path: str, quality: int = 95) -> tuple[int, int]:
    im = Image.open(src_path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.save(dst_path, "JPEG", quality=quality)
    return im.size


class WooCommerceBatchPublisher:
    def __init__(self, wp_base_url: str, username: str, app_password: str):
        self.wp_base = wp_base_url.rstrip("/")
        auth_token = base64.b64encode(f"{username}:{app_password}".encode("utf-8")).decode("utf-8")
        self.auth_header = f"Basic {auth_token}"
        self.tag_cache = {}

    def request(self, endpoint: str, method: str = "GET", data=None, content_type: str = "application/json", extra_headers=None):
        url = f"{self.wp_base}{endpoint}" if endpoint.startswith("/") else endpoint
        headers = {
            "Authorization": self.auth_header,
            "User-Agent": "NRL-WooCommerce-Publisher/1.0",
        }
        if content_type:
            headers["Content-Type"] = content_type
        if extra_headers:
            headers.update(extra_headers)
        body = None
        if data is not None:
            body = data if isinstance(data, (bytes, bytearray)) else json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=body, method=method, headers=headers)
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def upload_media(self, local_path: str, seo_filename: str, title: str, alt_text: str) -> tuple[int, str]:
        with open(local_path, "rb") as f:
            img_bytes = f.read()
        res = self.request(
            "/wp/v2/media",
            method="POST",
            data=img_bytes,
            content_type="image/jpeg",
            extra_headers={"Content-Disposition": f'attachment; filename="{seo_filename}"'},
        )
        media_id = res["id"]
        clean_title = sanitize_text(title)
        clean_alt = sanitize_text(alt_text)
        self.request(
            f"/wp/v2/media/{media_id}",
            method="POST",
            data={"title": clean_title, "alt_text": clean_alt, "caption": clean_alt},
        )
        return media_id, res.get("source_url", "")
