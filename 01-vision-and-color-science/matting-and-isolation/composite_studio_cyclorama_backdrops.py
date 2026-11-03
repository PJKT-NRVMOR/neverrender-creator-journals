#!/usr/bin/env python3
"""
Reusable NeverRender Labs Studio Cyclorama Compositor (`composite_studio_cyclorama_backdrops.py`).
Replaces neutral studio/Photoroom grey backgrounds on antique furniture and decorative objects
with bespoke textured cyclorama plates (Parchment Linen, Gustavian Ivory Cove, Silver-Slate Linen)
while preserving original floor contact shadows and 100% of subject chroma.
"""

import os
import sys
import numpy as np
from PIL import Image, ImageFilter


def crop_center_aspect(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    w, h = img.size
    target_aspect = target_w / float(target_h)
    src_aspect = w / float(h)
    if src_aspect > target_aspect:
        new_w = int(h * target_aspect)
        left = (w - new_w) // 2
        cropped = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_aspect)
        top = (h - new_h) // 2
        cropped = img.crop((0, top, w, top + new_h))
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)


def composite_piece_onto_backdrop(piece_rgb: Image.Image, bg_rgb: Image.Image) -> Image.Image:
    w, h = piece_rgb.size
    bg_sq = crop_center_aspect(bg_rgb, w, h)

    arr = np.asarray(piece_rgb, dtype=np.float32)
    bg_arr = np.asarray(bg_sq, dtype=np.float32)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    lum = 0.299 * r + 0.587 * g + 0.114 * b

    neutral_w = np.clip((18.0 - chroma) / 12.0, 0.0, 1.0)
    lum_w = np.clip((lum - 50.0) / 32.0, 0.0, 1.0)
    raw_mask = neutral_w * lum_w

    mask_img = Image.fromarray((raw_mask * 255.0).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=1.2))
    bg_mask = np.asarray(mask_img, dtype=np.float32) / 255.0

    smooth_piece = piece_rgb.filter(ImageFilter.GaussianBlur(radius=8))
    s_arr = np.asarray(smooth_piece, dtype=np.float32)
    s_lum = 0.299 * s_arr[:, :, 0] + 0.587 * s_arr[:, :, 1] + 0.114 * s_arr[:, :, 2]
    shadow_mult = 0.86 + (np.clip(s_lum - 55.0, 0.0, 155.0) / 155.0) * 0.17

    shaded_bg = np.clip(bg_arr * shadow_mult[:, :, None], 0.0, 255.0)
    out = arr * (1.0 - bg_mask[:, :, None]) + shaded_bg * bg_mask[:, :, None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python composite_studio_cyclorama_backdrops.py <subject_img> <backdrop_img> <output_img>")
        sys.exit(1)
    subj = Image.open(sys.argv[1]).convert("RGB")
    bg = Image.open(sys.argv[2]).convert("RGB")
    res = composite_piece_onto_backdrop(subj, bg)
    res.save(sys.argv[3], format="JPEG", quality=94)
