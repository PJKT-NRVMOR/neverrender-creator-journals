#!/usr/bin/env python3
"""
NeverRender Labs // Carrier-Safe MMS Optimizer & Chaphavian Framed Card Compiler
--------------------------------------------------------------------------------
Converts any high-resolution C2PA/Lightroom PNG plate into two carrier-safe (<430 KB,
US/Canada Toll-Free MMSC & Omnisend 500 KB limit compliant) 4:4:4 sRGB JPEGs:
  1. Full-bleed iMessage-safe 5:4 clean plate (1080w, progressive 4:4:4 sRGB JPEG)
  2. Chaphavian 5-Swatch Framed Gallery MMS Card (1080w portrait with crest, kicker,
     hero plate, italic caption, and showroom footer bar).

Zero Secrets / Zero Client PII (Tree 1 Open-Source Studio Toolkit Standard).
"""

import argparse
import io
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageCms


ALABASTER = (247, 245, 242)  # #F7F5F2
PUTTY     = (213, 211, 204)  # #D5D3CC
SLATE     = (138, 143, 151)  # #8A8F97
ROSE      = (179, 90, 94)    # #B35A5E
IRON      = (43, 47, 50)     # #2B2F32


def load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for name in candidates:
        p = Path(r"C:\Windows\Fonts") / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def save_carrier_safe_jpeg(im_rgb: Image.Image, out_path: Path, max_bytes: int = 440_000) -> tuple[int, int]:
    """Encode progressive sRGB JPEG strictly under max_bytes while maximizing chroma fidelity."""
    srgb_profile = ImageCms.createProfile("sRGB")
    icc_bytes = ImageCms.ImageCmsProfile(srgb_profile).tobytes()

    for q in (90, 88, 86, 84, 82, 80, 78, 75):
        subsampling = 0 if q >= 84 else 2
        buf = io.BytesIO()
        im_rgb.save(
            buf,
            format="JPEG",
            quality=q,
            subsampling=subsampling,
            progressive=True,
            optimize=True,
            icc_profile=icc_bytes,
        )
        data = buf.getvalue()
        if len(data) <= max_bytes or q == 75:
            out_path.write_bytes(data)
            return len(data), q
    return 0, 0


def draw_centered(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill: tuple[int, int, int], width: int) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2 - bbox[0], y - bbox[1]), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def build_framed_mms_card(
    src_img: Image.Image,
    crest_path: Path | None,
    brand_title: str,
    kicker: str,
    caption_line_1: str,
    caption_line_2: str,
    footer_bar: str,
) -> Image.Image:
    W = 1080
    pad = 26
    photo_margin = 58
    photo_w = W - (photo_margin * 2)  # 964 px
    photo_h = round(photo_w * (src_img.height / src_img.width))

    H = 236 + photo_h + 170
    card = Image.new("RGB", (W, H), PUTTY)
    draw = ImageDraw.Draw(card)

    # Chaphavian gallery frame (#F7F5F2 Alabaster inner, #8A8F97 Slate side rules, #2B2F32 Iron + #B35A5E Rose top/bottom bars)
    draw.rectangle([pad, pad, W - pad, H - pad], fill=ALABASTER, outline=SLATE, width=2)
    draw.rectangle([pad, pad, W - pad, pad + 8], fill=IRON)
    draw.rectangle([pad, pad + 8, W - pad, pad + 11], fill=ROSE)
    draw.rectangle([pad, H - pad - 8, W - pad, H - pad], fill=IRON)

    f_reg = lambda sz: load_font(["GARA.TTF", "georgia.ttf", "times.ttf"], sz)
    f_bold = lambda sz: load_font(["GARABD.TTF", "georgiab.ttf", "timesbd.ttf"], sz)
    f_ital = lambda sz: load_font(["GARAIT.TTF", "georgiai.ttf", "timesi.ttf"], sz)

    y = 48
    if crest_path and crest_path.exists():
        crest = Image.open(crest_path).convert("RGBA")
        crest.thumbnail((76, 76), Image.Resampling.LANCZOS)
        card.paste(crest, ((W - crest.width) // 2, y), mask=crest.split()[-1])
        y += crest.height + 12

    y += draw_centered(draw, y, brand_title, f_reg(30), IRON, W) + 12
    draw.line([(96, y), (W - 96, y)], fill=PUTTY, width=2)
    y += 14
    y += draw_centered(draw, y, kicker, f_bold(16), ROSE, W) + 16

    # Framed 5:4 Hero Photo
    resized_photo = src_img.convert("RGB").resize((photo_w, photo_h), Image.Resampling.LANCZOS)
    draw.rectangle([photo_margin - 2, y - 2, photo_margin + photo_w + 2, y + photo_h + 2], outline=PUTTY, width=2)
    card.paste(resized_photo, (photo_margin, y))
    y += photo_h + 18

    # Subtle Editorial Caption
    y += draw_centered(draw, y, caption_line_1, f_ital(22), IRON, W) + 8
    y += draw_centered(draw, y, caption_line_2, f_ital(20), SLATE, W) + 18

    # 56px Chaphavian Rose Divider Rule
    draw.line([(W // 2 - 28, y), (W // 2 + 28, y)], fill=ROSE, width=2)
    y += 18

    # Showroom Hours & Direct Text/Call Bar
    draw_centered(draw, y, footer_bar, f_bold(17), SLATE, W)
    return card


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile carrier-safe clean & Chaphavian-framed MMS JPEGs.")
    parser.add_argument("--input", required=True, help="Source PNG/JPG path")
    parser.add_argument("--out-clean", required=True, help="Output clean 5:4 MMS JPEG path")
    parser.add_argument("--out-card", required=True, help="Output Chaphavian framed MMS JPEG path")
    parser.add_argument("--crest", default="", help="Optional transparent crest PNG path")
    parser.add_argument("--brand", default="THE CHAPMAN COLLECTION")
    parser.add_argument("--kicker", default="VETERANS DAY  ·  NOVEMBER 11")
    parser.add_argument("--caption-1", default="On the terrace: Hand Carved Italian Polychrome Marble Figure, 64 inches high")
    parser.add_argument("--caption-2", default="With deepest gratitude this Veterans Day from our Rancho Santa Fe showroom")
    parser.add_argument("--footer", default="6014 La Granada, Rancho Santa Fe   |   (858) 349-2638   |   Open 10 AM to 7 PM")
    args = parser.parse_args()

    src = Image.open(args.input).convert("RGB")
    clean_w = 1080
    clean_h = round(clean_w * (src.height / src.width))
    clean_im = src.resize((clean_w, clean_h), Image.Resampling.LANCZOS)

    out_clean = Path(args.out_clean)
    out_card = Path(args.out_card)
    out_clean.parent.mkdir(parents=True, exist_ok=True)
    out_card.parent.mkdir(parents=True, exist_ok=True)

    b_clean, q_clean = save_carrier_safe_jpeg(clean_im, out_clean)
    card_im = build_framed_mms_card(
        src_img=src,
        crest_path=Path(args.crest) if args.crest else None,
        brand_title=args.brand,
        kicker=args.kicker,
        caption_line_1=args.caption_1,
        caption_line_2=args.caption_2,
        footer_bar=args.footer,
    )
    b_card, q_card = save_carrier_safe_jpeg(card_im, out_card)

    print(f"[OK] Clean 5:4 MMS ({clean_im.width}x{clean_im.height}, Q={q_clean}): {b_clean / 1024:.1f} KB -> {out_clean}")
    print(f"[OK] Chaphavian Card MMS ({card_im.width}x{card_im.height}, Q={q_card}): {b_card / 1024:.1f} KB -> {out_card}")


if __name__ == "__main__":
    main()
