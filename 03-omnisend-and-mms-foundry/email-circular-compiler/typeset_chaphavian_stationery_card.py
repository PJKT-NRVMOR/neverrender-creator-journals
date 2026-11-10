#!/usr/bin/env python3
"""
NeverRender Labs // Universal Chaphavian Letterpress Stationery Press (Force-Multiplier)
----------------------------------------------------------------------------------------
Auto-detects the Alabaster stationery plaque, #B35A5E rose divider rule, and bottom
imprint line on ANY blank Chaphavian 5:4 salon plate (1152x928, 1382x1114, or 2K+),
scales 4x-supersampled Garamond letterpress typography proportionally to the detected
card width, and preserves embedded XMP / sRGB metadata chunks.

Built-in --preset profiles:
  - welcome-18h       : +18-Hour New Subscriber Salon Welcome (zero Oxford commas)
  - post-click-72h    : +72-Hour Post-Click Showroom Touchpoint (zero 'today' / Oxford commas)
  - cart-concierge    : Private Hold, Shipping Quote & Showroom Concierge Note
  - vip-first-look    : Inner-Circle Collector Early Arrival Preview
  - holiday-gratitude : Seasonal & Year-End Rancho Santa Fe Collector Note

Zero Secrets / Zero Client PII (Tree 1 Open-Source Studio Toolkit Standard).
"""

import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin


PRESET_COPY: dict[str, list[str]] = {
    "welcome-18h": [
        "We are delighted to welcome you to our private collector list.",
        "Each week we share newly arrived European antiques, fine art",
        "and authentic handmade Persian carpets chosen for",
        "homes of warmth and timeless character.",
        "Whenever you are in the Village, please stop in and visit",
        "our Rancho Santa Fe showroom.",
    ],
    "post-click-72h": [
        "Every antique, painting and handmade Persian carpet in our",
        "collection is chosen to bring lasting warmth, history and",
        "character into a home. If a special piece caught your eye,",
        "we would be delighted to share natural light photographs,",
        "provenance details or welcome you into our",
        "Rancho Santa Fe showroom.",
    ],
    "cart-concierge": [
        "Each piece in our Rancho Santa Fe gallery is one of a kind.",
        "If you would like exact room measurements, natural daylight",
        "video or a white-glove local or worldwide shipping quote",
        "before completing your acquisition, please reply anytime",
        "or contact our showroom directly.",
    ],
    "vip-first-look": [
        "Before our newest European antiques, fine art and",
        "authentic Persian carpets reach the public gallery,",
        "we are pleased to share an early preview with",
        "friends of our Rancho Santa Fe showroom.",
        "Contact us anytime for private details or shipping quotes.",
    ],
    "holiday-gratitude": [
        "Warmest wishes for a joyful holiday season from",
        "our Rancho Santa Fe gallery to your home.",
        "Thank you for sharing our appreciation for fine antiques,",
        "enduring craftsmanship and timeless beauty throughout",
        "the year. We look forward to welcoming you soon.",
    ],
}


def load_serif_font(size_px: int) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\GARA.TTF",
        r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\BASKVILL.TTF",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size_px)
    return ImageFont.load_default()


def auto_detect_card_geometry(im_rgb: Image.Image) -> dict[str, float]:
    """
    Auto-detects the bright Alabaster stationery plaque, the #B35A5E divider rule,
    and the bottom imprint line on any resolution blank Chaphavian salon plate.
    """
    arr = np.array(im_rgb.convert("RGB"))
    h, w, _ = arr.shape

    # Locate bright stationery plaque in lower half of image
    lower_start = int(h * 0.45)
    sub = arr[lower_start:, :, :]
    white_mask = (sub[:, :, 0] > 236) & (sub[:, :, 1] > 234) & (sub[:, :, 2] > 228)
    row_counts = white_mask.sum(axis=1)
    active_rows = np.where(row_counts > w * 0.22)[0]
    if len(active_rows) < 20:
        # Fallback proportional defaults (based on 1152x928 centered card)
        scale_y = h / 928.0
        return {
            "center_x": w / 2.0,
            "card_width": 432.0 * (w / 1152.0),
            "rule_bottom_y": 690.0 * scale_y,
            "footer_top_y": 828.0 * scale_y,
        }

    y0 = int(active_rows[0]) + lower_start
    y1 = int(active_rows[-1]) + lower_start
    col_means = white_mask[active_rows[0] : active_rows[-1], :].mean(axis=0)
    active_cols = np.where(col_means > 0.72)[0]
    x0 = int(active_cols[0])
    x1 = int(active_cols[-1])
    card_width = float(x1 - x0)
    center_x = (x0 + x1) / 2.0

    # Locate #B35A5E rose horizontal rule inside upper half of card
    pad_x = max(16, int(card_width * 0.08))
    pad_y_top = max(14, int((y1 - y0) * 0.12))
    pad_y_mid = int((y1 - y0) * 0.58)
    rule_band = arr[y0 + pad_y_top : y0 + pad_y_mid, x0 + pad_x : x1 - pad_x]
    red_mask = (rule_band[:, :, 0].astype(int) - rule_band[:, :, 1].astype(int)) > 42
    ry, rx = np.where(red_mask)
    if len(ry) > 0:
        rule_bottom_y = float(ry.max() + y0 + pad_y_top)
        center_x = float((rx.min() + rx.max()) / 2.0 + x0 + pad_x)
    else:
        rule_bottom_y = float(y0 + (y1 - y0) * 0.34)

    # Locate top of bottom imprint text ("THE CHAPMAN COLLECTION...")
    foot_y0 = int(y1 - (y1 - y0) * 0.26)
    foot_y1 = int(y1 - (y1 - y0) * 0.07)
    foot_band = arr[foot_y0:foot_y1, x0 + pad_x : x1 - pad_x]
    dark_foot = np.where(foot_band[:, :, 0] < 195)[0]
    if len(dark_foot) > 0:
        footer_top_y = float(dark_foot.min() + foot_y0)
    else:
        footer_top_y = float(y1 - (y1 - y0) * 0.14)

    return {
        "center_x": center_x,
        "card_width": card_width,
        "rule_bottom_y": rule_bottom_y,
        "footer_top_y": footer_top_y,
    }


def typeset_stationery_plate(
    blank_png_path: Path,
    output_png_path: Path,
    lines: list[str],
    center_x: float | None = None,
    rule_bottom_y: float | None = None,
    footer_top_y: float | None = None,
    font_size_ref: float = 13.4,
    line_height_ref: float = 18.0,
    ink_rgb: tuple[int, int, int] = (20, 22, 24),
    ink_opacity: float = 1.0,
    letterpress_gain: float = 0.42,
) -> tuple[Path, dict[str, float]]:
    src_img = Image.open(blank_png_path)
    orig_info = dict(src_img.info)
    geom = auto_detect_card_geometry(src_img)

    cx = center_x if center_x is not None else geom["center_x"]
    r_bot = rule_bottom_y if rule_bottom_y is not None else geom["rule_bottom_y"]
    f_top = footer_top_y if footer_top_y is not None else geom["footer_top_y"]

    # Scale typography proportionally to detected open vertical band & card width
    # Reference card (1152x928 master) has card_width ~ 420px and band height ~ 138px
    width_ratio = geom["card_width"] / 420.0
    band_ratio = (f_top - r_bot) / 138.0
    typo_scale = min(width_ratio, band_ratio * 1.04)

    font_size_1x = font_size_ref * typo_scale
    line_height_1x = line_height_ref * typo_scale

    base = src_img.convert("RGBA")
    w, h = base.size

    # 4x supersampling for crisp letterpress edges at email display scale
    scale = 4
    overlay_hi = Image.new("RGBA", (w * scale, h * scale), (0, 0, 0, 0))
    draw_hi = ImageDraw.Draw(overlay_hi)
    font_hi = load_serif_font(int(round(font_size_1x * scale)))

    n_lines = len(lines)
    step_hi = line_height_1x * scale
    first_bbox = draw_hi.textbbox((0, 0), lines[0], font=font_hi)
    last_bbox = draw_hi.textbbox((0, 0), lines[-1], font=font_hi)
    cap_top = first_bbox[1]
    last_bottom = last_bbox[3]
    total_block_hi = (n_lines - 1) * step_hi + (last_bottom - cap_top)

    band_mid_hi = ((r_bot + f_top) / 2.0 - 1.5 * typo_scale) * scale
    start_y_hi = band_mid_hi - (total_block_hi / 2.0) - cap_top
    cx_hi = cx * scale

    alpha = int(round(255 * ink_opacity))
    gain_alpha = int(round(255 * letterpress_gain))
    fill_rgba = (ink_rgb[0], ink_rgb[1], ink_rgb[2], alpha)
    gain_rgba = (ink_rgb[0], ink_rgb[1], ink_rgb[2], gain_alpha)

    for idx, line in enumerate(lines):
        ly = start_y_hi + idx * step_hi
        bbox = draw_hi.textbbox((0, 0), line, font=font_hi)
        lw = bbox[2] - bbox[0]
        lx = cx_hi - (lw / 2.0) - bbox[0]
        if gain_alpha > 0:
            draw_hi.text((lx - 1, ly), line, font=font_hi, fill=gain_rgba)
            draw_hi.text((lx + 1, ly), line, font=font_hi, fill=gain_rgba)
        draw_hi.text((lx, ly), line, font=font_hi, fill=fill_rgba)

    overlay_1x = overlay_hi.resize((w, h), resample=Image.Resampling.LANCZOS)
    composited = Image.alpha_composite(base, overlay_1x).convert("RGB")
    output_png_path.parent.mkdir(parents=True, exist_ok=True)

    pnginfo = PngImagePlugin.PngInfo()
    xmp_val = orig_info.get("XML:com.adobe.xmp") or orig_info.get("xmp")
    if isinstance(xmp_val, str) and xmp_val:
        pnginfo.add_itxt("XML:com.adobe.xmp", xmp_val)
    icc = orig_info.get("icc_profile")
    save_kwargs = {"format": "PNG", "optimize": True, "pnginfo": pnginfo}
    if icc:
        save_kwargs["icc_profile"] = icc

    composited.save(output_png_path, **save_kwargs)
    geom["font_size_1x"] = round(font_size_1x, 2)
    geom["line_height_1x"] = round(line_height_1x, 2)
    return output_png_path, geom


def main() -> None:
    parser = argparse.ArgumentParser(description="Typeset letterpress copy onto any blank Chaphavian stationery PNG.")
    parser.add_argument("--input", required=True, help="Path to blank stationery PNG")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument(
        "--preset",
        choices=list(PRESET_COPY.keys()),
        default="post-click-72h",
        help="Built-in Chaphavian concierge copy preset",
    )
    parser.add_argument("--text", help="Optional custom newline-separated lines (overrides --preset)")
    parser.add_argument("--font-size", type=float, default=13.4, help="Reference 1x font size in px (default: 13.4)")
    parser.add_argument("--line-height", type=float, default=18.0, help="Reference 1x line height in px (default: 18.0)")
    args = parser.parse_args()

    lines = [ln.strip() for ln in args.text.splitlines() if ln.strip()] if args.text else PRESET_COPY[args.preset]
    out, geom = typeset_stationery_plate(
        blank_png_path=Path(args.input),
        output_png_path=Path(args.output),
        lines=lines,
        font_size_ref=args.font_size,
        line_height_ref=args.line_height,
    )
    print(f"[OK] Typeset {len(lines)} lines ({args.preset}) -> {out} | geom={geom}")


if __name__ == "__main__":
    main()
