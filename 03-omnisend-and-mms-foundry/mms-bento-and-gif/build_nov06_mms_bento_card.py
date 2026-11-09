"""
Build the November 6, 2026 Chaphavian 5-Swatch MMS Bento Card (1080x1350 4:5 Portrait,
<450 KB carrier-safe JPEG) and 1200x630 OpenGraph Link Preview Banner for
The Chapman Collection's Scandinavian Gustavian circular (zero prices displayed).
"""
import os
from PIL import Image, ImageDraw, ImageFont

DST_DIRS = [
    r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-11-04-scandinavian-gustavian-gallery\cuts",
    r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\2026-11-04-scandinavian-gustavian-gallery\cuts",
]

# Enshrined 5-Swatch Chaphavian Palette
ALABASTER = (247, 245, 242)  # #F7F5F2 (60% Primary plaster & linen canvas)
PUTTY = (217, 211, 204)      # #D9D3CC (60% Carved limestone & millwork)
SLATE = (138, 143, 151)      # #8A8F97 (30% Wainscoting & study paneling)
ROSE = (179, 90, 94)         # #B35A5E (10% Alcove warmth & textile accent)
IRON = (43, 47, 51)          # #2B2F33 (10% Steel window grids & deep ink)


def load_font(names, size):
    for name in names:
        p = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


f_reg = lambda sz: load_font(["gara.ttf", "georgia.ttf", "times.ttf"], sz)
f_bold = lambda sz: load_font(["garabd.ttf", "georgiab.ttf", "timesbd.ttf"], sz)
f_ital = lambda sz: load_font(["garait.ttf", "georgiai.ttf", "timesi.ttf"], sz)


def paste_centered(canvas, img_path, box, bg_color=ALABASTER):
    x1, y1, x2, y2 = box
    bw, bh = x2 - x1, y2 - y1
    if not os.path.exists(img_path):
        return
    im = Image.open(img_path)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, bg_color)
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    im.thumbnail((bw, bh), Image.Resampling.LANCZOS)
    px = x1 + (bw - im.width) // 2
    py = y1 + (bh - im.height) // 2
    canvas.paste(im, (px, py))


def draw_centered_text(draw, y, text, font, fill, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def build_mms_bento_2x3(cuts_dir: str) -> Image.Image:
    W, H = 1080, 1350
    card = Image.new("RGB", (W, H), PUTTY)
    draw = ImageDraw.Draw(card)

    pad = 26
    # Inner Alabaster gallery canvas with Iron top/bottom bars and Slate side borders
    draw.rectangle([pad, pad, W - pad, H - pad], fill=ALABASTER, outline=SLATE, width=2)
    draw.rectangle([pad, pad, W - pad, pad + 8], fill=IRON)
    draw.rectangle([pad, pad + 8, W - pad, pad + 11], fill=ROSE)
    draw.rectangle([pad, H - pad - 8, W - pad, H - pad], fill=IRON)

    crest_path = os.path.join(cuts_dir, "tcc-crest.png")
    if os.path.exists(crest_path):
        crest = Image.open(crest_path).convert("RGBA")
        crest.thumbnail((84, 84), Image.Resampling.LANCZOS)
        card.paste(crest, ((W - crest.width) // 2, 50), mask=crest.split()[-1])

    draw_centered_text(draw, 142, "THE CHAPMAN COLLECTION", f_reg(31), IRON, W)
    draw_centered_text(
        draw,
        182,
        "PERSIAN CARPETS   |   FINE FURNITURE   |   ARTWORKS   |   ACCESSORIES",
        f_bold(14),
        SLATE,
        W,
    )
    draw.line([(84, 210), (W - 84, 210)], fill=PUTTY, width=2)
    draw_centered_text(draw, 220, "Timeless Character and Fine Craftsmanship", f_ital(36), ROSE, W)
    draw_centered_text(draw, 264, "A curated selection from our Rancho Santa Fe showroom", f_reg(20), IRON, W)
    draw.line([(W // 2 - 36, 296), (W // 2 + 36, 296)], fill=ROSE, width=3)

    # 2x3 Bento Grid (6 pieces, zero prices, dimensions & provenance sub-kicker)
    items_bento = [
        (
            "tcc-f7f5f2-02-english-gothic-hallstand.jpg",
            "1892 Gothic Oak Hall Stand",
            "FRENCH OAK · 117\" H X 83\" W",
        ),
        (
            "tcc-f7f5f2-10-christ-before-pilate-rembrandt.jpg",
            "Christ Before Pilate",
            "AFTER REMBRANDT · 35\" X 30.5\"",
        ),
        (
            "tcc-f7f5f2-11-french-napoleon-iii-cabinet-front.jpg",
            "Napoleon III Display Cabinet",
            "MOTHER-OF-PEARL · 45.5\" X 48\"",
        ),
        (
            "tcc-f7f5f2-12-sevres-porcelain-plate-shadowbox.jpg",
            "Hand-Painted Sèvres Plate",
            "SHADOW BOX · 21\" H X 21\" W",
        ),
        (
            "tcc-f7f5f2-13-renaissance-revival-writing-desk.jpg",
            "Renaissance Revival Desk",
            "CIRCA 1890 · 56\" H X 58\" W",
        ),
        (
            "tcc-f7f5f2-07-silk-qum-runner-closeup.jpg",
            "Persian 10' Silk Qum Runner",
            "HAND FINISHED SILK · 10'0\" X 3'3\"",
        ),
    ]

    grid_left = 58
    grid_top = 314
    col_w = 306
    row_h = 418
    gap_x = 23
    gap_y = 20

    for idx, (img_name, title_txt, sub_txt) in enumerate(items_bento):
        r = idx // 3
        c = idx % 3
        cx1 = grid_left + c * (col_w + gap_x)
        cy1 = grid_top + r * (row_h + gap_y)
        cx2 = cx1 + col_w
        cy2 = cy1 + row_h

        draw.rectangle([cx1, cy1, cx2, cy2], fill=ALABASTER, outline=PUTTY, width=2)
        paste_centered(card, os.path.join(cuts_dir, img_name), (cx1 + 12, cy1 + 12, cx2 - 12, cy2 - 78))

        sub_font = f_bold(13)
        ttl_font = f_ital(21)

        sb_box = draw.textbbox((0, 0), sub_txt, font=sub_font)
        sw = sb_box[2] - sb_box[0]
        draw.text((cx1 + (col_w - sw) // 2, cy2 - 64), sub_txt, font=sub_font, fill=SLATE)

        tb_box = draw.textbbox((0, 0), title_txt, font=ttl_font)
        tw = tb_box[2] - tb_box[0]
        draw.text((cx1 + (col_w - tw) // 2, cy2 - 40), title_txt, font=ttl_font, fill=IRON)

    # Bottom Ghost-to-Iron CTA Bar
    btn_w, btn_h = 620, 54
    btn_x1 = (W - btn_w) // 2
    btn_y1 = 1192
    draw.rectangle([btn_x1, btn_y1, btn_x1 + btn_w, btn_y1 + btn_h], fill=IRON, outline=IRON, width=2)
    draw_centered_text(draw, btn_y1 + 14, "TAP LINK BELOW TO EXPLORE THE COLLECTION", f_reg(20), ALABASTER, W)
    draw_centered_text(
        draw,
        1268,
        "6014 La Granada, Rancho Santa Fe   |   (858) 349-2638   |   Open Seven Days",
        f_bold(17),
        SLATE,
        W,
    )
    return card


def build_mms_bento_1over6(cuts_dir: str) -> Image.Image:
    """7-Tile 1-Over-6 Bento Card matching the exact 7 items in the circular."""
    W, H = 1080, 1350
    card = Image.new("RGB", (W, H), PUTTY)
    draw = ImageDraw.Draw(card)

    pad = 26
    draw.rectangle([pad, pad, W - pad, H - pad], fill=ALABASTER, outline=SLATE, width=2)
    draw.rectangle([pad, pad, W - pad, pad + 8], fill=IRON)
    draw.rectangle([pad, pad + 8, W - pad, pad + 11], fill=ROSE)
    draw.rectangle([pad, H - pad - 8, W - pad, H - pad], fill=IRON)

    crest_path = os.path.join(cuts_dir, "tcc-crest.png")
    if os.path.exists(crest_path):
        crest = Image.open(crest_path).convert("RGBA")
        crest.thumbnail((72, 72), Image.Resampling.LANCZOS)
        card.paste(crest, ((W - crest.width) // 2, 46), mask=crest.split()[-1])

    draw_centered_text(draw, 124, "THE CHAPMAN COLLECTION", f_reg(29), IRON, W)
    draw_centered_text(draw, 160, "Timeless Character and Fine Craftsmanship", f_ital(33), ROSE, W)
    draw.line([(W // 2 - 34, 202), (W // 2 + 34, 202)], fill=ROSE, width=2)

    # Top Feature Row: Full-Width Split Banner for Item 1 (1892 Gothic Revival Oak Hall Stand)
    hx1, hy1, hx2, hy2 = 58, 218, W - 58, 466
    draw.rectangle([hx1, hy1, hx2, hy2], fill=ALABASTER, outline=PUTTY, width=2)
    paste_centered(
        card,
        os.path.join(cuts_dir, "tcc-f7f5f2-02-english-gothic-hallstand.jpg"),
        (hx1 + 28, hy1 + 8, hx1 + 324, hy2 - 8),
    )
    draw.text((hx1 + 344, hy1 + 50), "FRENCH GOTHIC REVIVAL OAK  ·  DATED 1892  ·  117\" H X 83\" W", font=f_bold(14), fill=SLATE)
    draw.text((hx1 + 344, hy1 + 80), "Monumental Gothic Revival Oak Hall Stand", font=f_ital(29), fill=IRON)
    draw.text((hx1 + 344, hy1 + 124), "Standing 9 feet 9 inches tall in carved French oak with", font=f_reg(19), fill=IRON)
    draw.text((hx1 + 344, hy1 + 150), "pierced Gothic tracery, linenfold panels, tall inset mirror", font=f_reg(19), fill=IRON)
    draw.text((hx1 + 344, hy1 + 176), "and an upholstered lift-seat bench.", font=f_reg(19), fill=IRON)

    # 6-Item 3x2 Grid Below (Items 2-7)
    items_6 = [
        ("tcc-f7f5f2-10-christ-before-pilate-rembrandt.jpg", "Christ Before Pilate", "AFTER REMBRANDT · 35\" X 30.5\""),
        ("tcc-f7f5f2-11-french-napoleon-iii-cabinet-front.jpg", "Napoleon III Cabinet", "MOTHER-OF-PEARL · 45.5\" X 48\""),
        ("tcc-f7f5f2-12-sevres-porcelain-plate-shadowbox.jpg", "Hand-Painted Sèvres Plate", "SHADOW BOX · 21\" H X 21\" W"),
        ("tcc-f7f5f2-13-renaissance-revival-writing-desk.jpg", "Renaissance Writing Desk", "CIRCA 1890 · 56\" H X 58\" W"),
        ("tcc-f7f5f2-05-french-empire-pedestals.jpg", "French Empire Pedestals", "GREEN MARBLE AND GILT · 54.5\" H"),
        ("tcc-f7f5f2-07-silk-qum-runner-closeup.jpg", "10' Silk Qum Runner", "MIDNIGHT BLUE · 10'0\" X 3'3\""),
    ]

    grid_left = 58
    grid_top = 484
    col_w = 306
    row_h = 334
    gap_x = 23
    gap_y = 18

    for idx, (img_name, title_txt, sub_txt) in enumerate(items_6):
        r = idx // 3
        c = idx % 3
        cx1 = grid_left + c * (col_w + gap_x)
        cy1 = grid_top + r * (row_h + gap_y)
        cx2 = cx1 + col_w
        cy2 = cy1 + row_h

        draw.rectangle([cx1, cy1, cx2, cy2], fill=ALABASTER, outline=PUTTY, width=2)
        paste_centered(card, os.path.join(cuts_dir, img_name), (cx1 + 10, cy1 + 10, cx2 - 10, cy2 - 68))

        sub_font = f_bold(12)
        ttl_font = f_ital(20)

        sb_box = draw.textbbox((0, 0), sub_txt, font=sub_font)
        sw = sb_box[2] - sb_box[0]
        draw.text((cx1 + (col_w - sw) // 2, cy2 - 56), sub_txt, font=sub_font, fill=SLATE)

        tb_box = draw.textbbox((0, 0), title_txt, font=ttl_font)
        tw = tb_box[2] - tb_box[0]
        draw.text((cx1 + (col_w - tw) // 2, cy2 - 34), title_txt, font=ttl_font, fill=IRON)

    btn_w, btn_h = 620, 52
    btn_x1 = (W - btn_w) // 2
    btn_y1 = 1194
    draw.rectangle([btn_x1, btn_y1, btn_x1 + btn_w, btn_y1 + btn_h], fill=IRON, outline=IRON, width=2)
    draw_centered_text(draw, btn_y1 + 13, "TAP LINK BELOW TO EXPLORE THE COLLECTION", f_reg(20), ALABASTER, W)
    draw_centered_text(
        draw,
        1268,
        "6014 La Granada, Rancho Santa Fe   |   (858) 349-2638   |   Open Seven Days",
        f_bold(17),
        SLATE,
        W,
    )
    return card


def main():
    card_2x3 = build_mms_bento_2x3(DST_DIRS[0])
    card_1over6 = build_mms_bento_1over6(DST_DIRS[0])

    for d in DST_DIRS:
        os.makedirs(d, exist_ok=True)
        p1 = os.path.join(d, "tcc-nov06-mms-bento-card.jpg")
        p2 = os.path.join(d, "tcc-nov06-mms-bento-1over6.jpg")
        card_2x3.save(p1, "JPEG", quality=90, optimize=True)
        card_1over6.save(p2, "JPEG", quality=90, optimize=True)
        print(f"Saved: {p1} ({os.path.getsize(p1)} bytes)")
        print(f"Saved: {p2} ({os.path.getsize(p2)} bytes)")


if __name__ == "__main__":
    main()
