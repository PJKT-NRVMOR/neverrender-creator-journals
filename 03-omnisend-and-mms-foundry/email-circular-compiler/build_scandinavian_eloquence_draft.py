#!/usr/bin/env python3
"""
Build The Chapman Collection — Scandinavian / Eloquence ("Gustavian Chic!") Newsletter Draft
Using Matthew Wyatt's 7 Hand-Crafted 1x1 `#F7F5F2` Photoshop Hero Cutouts (`F7F5F2-heros`)
and his 5-Swatch Scandinavian Palette:
  - #2B2F33 : Deep Nordic Charcoal Slate (Primary Ink, Editorial Headers, CTA Buttons)
  - #B35A5E : Swedish Falun Muted Terracotta Rose (Sale Price, Kicker, Divider Rules)
  - #8A8F97 : Cool Pewter / Mora Lead-Grey (Dimensions, Provenance Subheads, Strikethrough Price)
  - #D9D3CC : Gustavian Putty / Chalk Stone (Outer Frame, Card Hairlines, Divider Rules)
  - #F7F5F2 : Bleached Nordic Alabaster / Linen White (Inner 600px Gallery Canvas — matches 1x1 cutouts 100%!)
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

HEROS_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\inspo-gustavian-eloquence-2026-11-02\pmc-custom-backdrops-preview\F7F5F2-heros"
PREV_CUTS_DIR = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-10-27-autumn-warmth-and-old-world-peculiars\cuts"

DRAFT_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-11-04-scandinavian-gustavian-gallery"
DRAFT_CUTS = os.path.join(DRAFT_DIR, "cuts")

NRL_DRAFT_DIR = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-11-04-scandinavian-gustavian-gallery"
NRL_CUTS = os.path.join(NRL_DRAFT_DIR, "cuts")

ARTIFACT_DIR = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2"

for d in (DRAFT_DIR, DRAFT_CUTS, NRL_DRAFT_DIR, NRL_CUTS):
    os.makedirs(d, exist_ok=True)

# 5-Swatch Scandinavian Palette (RGB tuples)
C_CHARCOAL  = (43, 47, 51)     # #2B2F33
C_FALUN     = (179, 90, 94)    # #B35A5E
C_PEWTER    = (138, 143, 151)  # #8A8F97
C_PUTTY     = (217, 211, 204)  # #D9D3CC
C_ALABASTER = (247, 245, 242)  # #F7F5F2


def load_font(size: int, italic: bool = False, bold: bool = False):
    candidates = []
    if bold and italic:
        candidates = ["C:/Windows/Fonts/GARAIT.TTF", "C:/Windows/Fonts/georgiaz.ttf", "C:/Windows/Fonts/timesbi.ttf"]
    elif italic:
        candidates = ["C:/Windows/Fonts/GARAIT.TTF", "C:/Windows/Fonts/georgiai.ttf", "C:/Windows/Fonts/timesi.ttf"]
    elif bold:
        candidates = ["C:/Windows/Fonts/GARABD.TTF", "C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/timesbd.ttf"]
    else:
        candidates = ["C:/Windows/Fonts/GARA.TTF", "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/times.ttf"]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def open_on_f7f5f2(path: str, size: int = 800, inner_scale: float = 1.0) -> Image.Image:
    """
    Open one of Matthew's 1x1 F7F5F2 hero PNGs, composite any alpha transparency
    directly onto exact #F7F5F2 (247, 245, 242), and resize cleanly with LANCZOS.
    If inner_scale < 1.0, pads the cutout on #F7F5F2 so bulky case pieces match
    the breathing room of chairs and pedestals.
    """
    im = Image.open(path)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (*C_ALABASTER, 255))
        comp = Image.alpha_composite(bg, rgba).convert("RGB")
    else:
        comp = im.convert("RGB")
    if inner_scale < 0.999:
        target_sz = int(round(size * inner_scale))
        scaled = comp.resize((target_sz, target_sz), Image.Resampling.LANCZOS)
        padded = Image.new("RGB", (size, size), C_ALABASTER)
        offset = (size - target_sz) // 2
        padded.paste(scaled, (offset, offset))
        return padded
    if comp.size != (size, size):
        comp = comp.resize((size, size), Image.Resampling.LANCZOS)
    return comp


def build_seamless_hero_slide(base_img: Image.Image, slide_idx: int, total_slides: int) -> Image.Image:
    """
    Build a seamless 600x600 #F7F5F2 Eloquence-style hero GIF frame with JUST the 1x1 #F7F5F2
    furniture cutout floating on the #F7F5F2 canvas (zero text descriptors).
    """
    canvas_w, canvas_h = 600, 600
    canvas = Image.new("RGB", (canvas_w, canvas_h), C_ALABASTER)
    draw = ImageDraw.Draw(canvas)

    # Outer 1px #D9D3CC gallery frame
    draw.rectangle([8, 8, canvas_w - 9, canvas_h - 9], outline=C_PUTTY, width=1)

    # Paste 560x560 1x1 hero cutout seamlessly onto #F7F5F2
    img_sz = 560
    resized = base_img.resize((img_sz, img_sz), Image.Resampling.LANCZOS)
    canvas.paste(resized, ((canvas_w - img_sz) // 2, (canvas_h - img_sz) // 2))

    return canvas


def build_mms_hero_slide(
    base_img: Image.Image,
    subtitle: str,
    title: str,
    cta_text: str,
    slide_idx: int,
    total_slides: int,
) -> Image.Image:
    """
    Build a 600x710 #F7F5F2 MMS broadcast GIF frame with the 1x1 #F7F5F2 cutout
    PLUS the provenance subtitle, italic Garamond item title, CTA text, and indicator dots.
    """
    canvas_w, canvas_h = 600, 710
    canvas = Image.new("RGB", (canvas_w, canvas_h), C_ALABASTER)
    draw = ImageDraw.Draw(canvas)

    # Outer 1px #D9D3CC gallery frame
    draw.rectangle([8, 8, canvas_w - 9, canvas_h - 9], outline=C_PUTTY, width=1)

    # Paste 530x530 1x1 hero cutout seamlessly onto #F7F5F2
    img_sz = 530
    resized = base_img.resize((img_sz, img_sz), Image.Resampling.LANCZOS)
    canvas.paste(resized, ((canvas_w - img_sz) // 2, 18))

    # Thin #D9D3CC divider rule below image
    draw.line([48, 560, canvas_w - 48, 560], fill=C_PUTTY, width=1)

    f_sub = load_font(12, bold=True)
    f_title = load_font(22, italic=True)
    f_cta = load_font(13, bold=True)

    bb_sub = draw.textbbox((0, 0), subtitle, font=f_sub)
    draw.text(((canvas_w - (bb_sub[2] - bb_sub[0])) // 2, 574), subtitle, fill=C_PEWTER, font=f_sub)

    bb_t = draw.textbbox((0, 0), title, font=f_title)
    draw.text(((canvas_w - (bb_t[2] - bb_t[0])) // 2, 596), title, fill=C_CHARCOAL, font=f_title)

    bb_p = draw.textbbox((0, 0), cta_text, font=f_cta)
    draw.text(((canvas_w - (bb_p[2] - bb_p[0])) // 2, 632), cta_text, fill=C_FALUN, font=f_cta)

    dot_r = 4
    dot_gap = 18
    total_w = (total_slides - 1) * dot_gap
    start_x = (canvas_w - total_w) // 2
    dot_y = 674
    for i in range(total_slides):
        cx = start_x + i * dot_gap
        fill_c = C_FALUN if i == slide_idx else C_PUTTY
        draw.ellipse([cx - dot_r, dot_y - dot_r, cx + dot_r, dot_y + dot_r], fill=fill_c)

    return canvas


def main():
    # Copy crest to both cuts folders
    crest_src = os.path.join(PREV_CUTS_DIR, "tcc-oct23-crest.png")
    for dst_dir in (DRAFT_CUTS, NRL_CUTS):
        shutil.copy2(crest_src, os.path.join(dst_dir, "tcc-crest.png"))

    # Matthew's 9 hand-crafted #F7F5F2 1x1 heroes (Price-free + "SELECT THIS PIECE" CTA)
    hero_specs = [
        (
            "tcc-f7f5f2-01-spanish-knights-cabinet.jpg",
            os.path.join(HEROS_DIR, "spanish-knights-cabinet-slate-curved-F7F5F2.png"),
            "SPANISH CARVED WALNUT  |  83.75\" H x 79.5\" W x 25.75\" D",
            "Antique Spanish Carved Cabinet with Knights",
            "SELECT THIS PIECE ->",
            True,   # Include in rotating 600px Hero GIF
            0.86,   # Scale slightly so it matches Chair & Pedestals breathing room in 4by grid
        ),
        (
            "tcc-f7f5f2-02-english-gothic-hallstand.jpg",
            os.path.join(HEROS_DIR, "English Tall Gothic Hallstand 117 tall x 83 wide x 16 deep $12,800-F7F5F2.png"),
            "MONUMENTAL ENGLISH OAK  |  117\" H x 83\" W x 16\" D",
            "Antique English Tall Gothic Hallstand",
            "SELECT THIS PIECE ->",
            True,
            1.0,
        ),
        (
            "tcc-f7f5f2-03-boulle-marquetry-credenza.jpg",
            os.path.join(HEROS_DIR, "boulle-marquetry-credenza-slate-curved-F7F5F2.png"),
            "FRENCH NAPOLEON III STYLE  |  EBONIZED AND FLORAL MARQUETRY",
            "Antique Boulle and Floral Marquetry Credenza",
            "SELECT THIS PIECE ->",
            True,
            0.82,   # Shrink Credenza slightly per Matthew's directive so it aligns cleanly over Chair & Pedestals
        ),
        (
            "tcc-f7f5f2-04-dutch-marquetry-armchair.jpg",
            os.path.join(HEROS_DIR, "antique-dutch-floral-marquetry-armchair-1700s-2-F7F5F2.png"),
            "CIRCA EARLY TO MID 1700S  |  45\" H x 24\" W x 19\" D",
            "Antique Dutch Floral Marquetry Armchair",
            "SELECT THIS PIECE ->",
            True,
            1.0,
        ),
        (
            "tcc-f7f5f2-05-french-empire-pedestals.jpg",
            os.path.join(HEROS_DIR, "pair-of-french-empire-style-green-marble-pedestals-hero-F7F5F2.png"),
            "GREEN MARBLE AND GILT MOUNTS  |  54.5\" H x 13.75\" W EACH",
            "Pair of French Empire Style Marble Pedestals",
            "SELECT THIS PIECE ->",
            True,
            1.0,
        ),
        (
            "tcc-f7f5f2-06-silk-qum-warm-red-carpet.jpg",
            os.path.join(HEROS_DIR, "ChatGPT-Image-Oct-16-2026-03_25_47-AM-nrl-graded-F7F5F2.png"),
            "HAND FINISHED SILK QUM  |  9'10\" x 6'5\"",
            "Persian Silk Qum Carpet in Warm Red and Ivory",
            "SELECT THIS PIECE ->",
            False,
            1.0,
        ),
        (
            "tcc-f7f5f2-07-silk-qum-runner-closeup.jpg",
            os.path.join(HEROS_DIR, "Silk Runner 10 foot long $24500 to $1850 close up-F7F5F2.png"),
            "LUMINOUS SILK WEAVE DETAIL  |  10' x 3'3\" RUNNER",
            "Persian Silk Qum Runner Medallion Detail",
            "SELECT THIS PIECE ->",
            False,
            1.0,
        ),
        (
            "tcc-f7f5f2-08-limoges-tea-service.jpg",
            os.path.join(HEROS_DIR, "18-piece-porcelain-limoges-style-tea-service-cobalt-blue-gold-detail-nr-F7F5F2.png"),
            "COBALT BLUE AND GILT PORCELAIN  |  18-PIECE SERVICE",
            "18-Piece Limoges Style Tea Service",
            "SELECT THIS PIECE ->",
            False,
            1.0,
        ),
        (
            "tcc-f7f5f2-09-joan-miro-gold-of-azure.jpg",
            os.path.join(HEROS_DIR, "joan-miro-the-gold-of-the-azure-1979-framed-scaled-F7F5F2.png"),
            "1979 FRANCE  |  21.75\" H x 19.25\" W CUSTOM FRAME",
            "Joan Miro, The Gold of the Azure",
            "SELECT THIS PIECE ->",
            False,
            1.0,
        ),
    ]

    loaded = []
    gif_candidates = []
    for out_name, src_path, sub_txt, title_txt, cta_txt, in_gif, sc in hero_specs:
        im = open_on_f7f5f2(src_path, 800, inner_scale=sc)
        for dst_dir in (DRAFT_CUTS, NRL_CUTS):
            im.save(os.path.join(dst_dir, out_name), format="JPEG", quality=94)
        loaded.append((out_name, im, sub_txt, title_txt, cta_txt))
        if in_gif:
            gif_candidates.append((im, sub_txt, title_txt, cta_txt))

    # Build 5-frame 600x710 animated MMS Hero GIF WITH descriptors (saved specifically for MMS broadcast)
    mms_frames = []
    for idx, (im, sub_txt, title_txt, cta_txt) in enumerate(gif_candidates):
        mms_slide = build_mms_hero_slide(im, sub_txt, title_txt, cta_txt, idx, len(gif_candidates))
        mms_frames.append(mms_slide.quantize(colors=256, method=Image.Quantize.MEDIANCUT))

    for mms_name in ("tcc-nov04-scandinavian-mms-hero.gif", "tcc-nov04-scandinavian-hero.gif"):
        for dst_dir in (DRAFT_CUTS, NRL_CUTS, ARTIFACT_DIR):
            mms_path = os.path.join(dst_dir, mms_name)
            mms_frames[0].save(
                mms_path,
                save_all=True,
                append_images=mms_frames[1:],
                duration=2100,
                loop=0,
                optimize=True,
            )
    print("Saved 5-frame MMS Hero GIF (with descriptions):", os.path.join(DRAFT_CUTS, "tcc-nov04-scandinavian-mms-hero.gif"))

    # Also keep pure 600x600 photo GIF on disk
    hero_frames = []
    for idx, (im, sub_txt, title_txt, price_txt) in enumerate(gif_candidates):
        slide = build_seamless_hero_slide(im, idx, len(gif_candidates))
        hero_frames.append(slide.quantize(colors=256, method=Image.Quantize.MEDIANCUT))

    for dst_dir in (DRAFT_CUTS, NRL_CUTS, ARTIFACT_DIR):
        gif_path = os.path.join(dst_dir, "tcc-nov04-scandinavian-hero-pure.gif")
        hero_frames[0].save(
            gif_path,
            save_all=True,
            append_images=hero_frames[1:],
            duration=2100,
            loop=0,
            optimize=True,
        )

    # Build OG share banner (1200x630) featuring the Gothic Hallstand, Spanish Cabinet, and Dutch Chair
    og_w, og_h = 1200, 630
    og = Image.new("RGB", (og_w, og_h), C_PUTTY)
    og_draw = ImageDraw.Draw(og)
    og_draw.rectangle([24, 24, og_w - 25, og_h - 25], fill=C_ALABASTER, outline=C_CHARCOAL, width=2)
    for i, pick_idx in enumerate([0, 1, 3]):
        thumb = loaded[pick_idx][1].resize((340, 340), Image.Resampling.LANCZOS)
        x = 60 + i * (340 + 30)
        og.paste(thumb, (x, 190))
    f_og_k = load_font(15, bold=True)
    f_og_t = load_font(36, italic=True)
    og_draw.text((66, 66), "THE CHAPMAN COLLECTION  |  RANCHO SANTA FE", fill=C_FALUN, font=f_og_k)
    og_draw.text((66, 104), "Timeless Character and Fine Craftsmanship", fill=C_CHARCOAL, font=f_og_t)
    og_draw.line([66, 162, 1134, 162], fill=C_PUTTY, width=2)
    for dst_dir in (DRAFT_CUTS, NRL_CUTS):
        og.save(os.path.join(dst_dir, "tcc-nov04-og-banner.jpg"), format="JPEG", quality=92)

    # Build full-length visual proof sheet of the newsletter showing all 9 F7F5F2 heroes
    proof_w, proof_h = 680, 2580
    proof = Image.new("RGB", (proof_w, proof_h), C_PUTTY)
    p_draw = ImageDraw.Draw(proof)
    p_draw.rectangle([40, 28, 640, proof_h - 28], fill=C_ALABASTER, outline=C_PEWTER, width=1)
    p_draw.rectangle([40, 28, 640, 33], fill=C_CHARCOAL)
    p_draw.rectangle([40, 34, 640, 36], fill=C_FALUN)

    crest_im = Image.open(crest_src).convert("RGBA")
    cw = 68
    ch = int(crest_im.height * (cw / float(crest_im.width)))
    crest_r = crest_im.resize((cw, ch), Image.Resampling.LANCZOS)
    proof.paste(crest_r, ((proof_w - cw) // 2, 52), crest_r)

    f_h1 = load_font(23, bold=False)
    f_nav = load_font(10, bold=True)
    f_red_big = load_font(22, italic=True)
    f_italic_small = load_font(14, italic=False)

    t_brand = "THE CHAPMAN COLLECTION"
    bb = p_draw.textbbox((0, 0), t_brand, font=f_h1)
    p_draw.text(((proof_w - (bb[2] - bb[0])) // 2, 52 + ch + 10), t_brand, fill=C_CHARCOAL, font=f_h1)

    t_nav = "PERSIAN CARPETS   |   FINE FURNITURE   |   ARTWORKS   |   ACCESSORIES"
    bb = p_draw.textbbox((0, 0), t_nav, font=f_nav)
    p_draw.text(((proof_w - (bb[2] - bb[0])) // 2, 52 + ch + 42), t_nav, fill=C_PEWTER, font=f_nav)
    p_draw.line([76, 52 + ch + 64, 604, 52 + ch + 64], fill=C_PUTTY, width=1)

    # Editorial Header directly under the Crest Masthead (matching Autumn Warmth & Old World Charm):
    # Fancy Garamond Italic "Timeless Character and Fine Craftsmanship" + Upright "A curated selection..." + Red Dash
    ey = 52 + ch + 78
    t_kicker = "Timeless Character and Fine Craftsmanship"
    bb = p_draw.textbbox((0, 0), t_kicker, font=f_red_big)
    p_draw.text(((proof_w - (bb[2] - bb[0])) // 2, ey), t_kicker, fill=C_FALUN, font=f_red_big)

    t_head = "A curated selection from our Rancho Santa Fe showroom"
    bb = p_draw.textbbox((0, 0), t_head, font=f_italic_small)
    p_draw.text(((proof_w - (bb[2] - bb[0])) // 2, ey + 28), t_head, fill=C_CHARCOAL, font=f_italic_small)
    p_draw.line([316, ey + 52, 364, ey + 52], fill=C_FALUN, width=2)

    # Paste Hero Carousel Card (Slide 1: English Tall Gothic Hallstand with < / > click-advance arrows & dots)
    hy = ey + 78
    p_draw.rectangle([72, hy, 608, hy + 540], fill=C_ALABASTER, outline=C_PUTTY, width=1)
    hall_hero_im = loaded[1][1].resize((380, 380), Image.Resampling.LANCZOS)
    proof.paste(hall_hero_im, ((proof_w - 380) // 2, hy + 10))
    # Draw < and > click-advance buttons on the proof
    for ax_x, arrow_ch in ((86, "<"), (562, ">")):
        p_draw.rectangle([ax_x, hy + 184, ax_x + 32, hy + 216], fill=C_ALABASTER, outline=C_PUTTY, width=1)
        p_draw.text((ax_x + 11, hy + 192), arrow_ch, fill=C_CHARCOAL, font=f_nav)
    # Draw 5 carousel dots
    for di in range(5):
        dcx = (proof_w - 64) // 2 + di * 16
        d_col = C_FALUN if di == 0 else C_PUTTY
        p_draw.ellipse([dcx - 4, hy + 400 - 4, dcx + 4, hy + 400 + 4], fill=d_col)
    f_hc_k = load_font(10, bold=True)
    f_hc_t = load_font(20, italic=True)
    tk_hero = "MONUMENTAL ENGLISH OAK   |   117\" H x 83\" W x 16\" D"
    bb = p_draw.textbbox((0, 0), tk_hero, font=f_hc_k)
    p_draw.text(((proof_w - (bb[2] - bb[0])) // 2, hy + 414), tk_hero, fill=C_PEWTER, font=f_hc_k)
    tt_hero = "Antique English Tall Gothic Hallstand"
    bb = p_draw.textbbox((0, 0), tt_hero, font=f_hc_t)
    p_draw.text(((proof_w - (bb[2] - bb[0])) // 2, hy + 432), tt_hero, fill=C_CHARCOAL, font=f_hc_t)
    f_btn_hero = load_font(10, bold=True)
    p_draw.rectangle([(proof_w - 176) // 2, hy + 492, (proof_w + 176) // 2, hy + 522], fill=C_ALABASTER, outline=C_CHARCOAL, width=1)
    bb_bh = p_draw.textbbox((0, 0), "SELECT THIS PIECE", font=f_btn_hero)
    p_draw.text(((proof_w - (bb_bh[2] - bb_bh[0])) // 2, hy + 501), "SELECT THIS PIECE", fill=C_CHARCOAL, font=f_btn_hero)

    # 4 rows x 2 columns grid in proof showing all remaining 8 pieces seamlessly on #F7F5F2 with ghost-outline "SELECT THIS PIECE" buttons
    grid_indices = [0, 2, 3, 4, 5, 6, 7, 8]
    cy = hy + 560
    f_ct = load_font(12, bold=True)
    f_btn = load_font(10, bold=True)
    f_cs = load_font(9, bold=False)
    for idx_pos, g_idx in enumerate(grid_indices):
        row = idx_pos // 2
        col = idx_pos % 2
        _, pim, psub, ptitle, _ = loaded[g_idx]
        card_w, card_h = 258, 326
        cx = 72 + col * (258 + 20)
        ry = cy + row * (card_h + 18)
        p_draw.rectangle([cx, ry, cx + card_w, ry + card_h], fill=C_ALABASTER, outline=C_PUTTY, width=1)
        th = pim.resize((234, 234), Image.Resampling.LANCZOS)
        proof.paste(th, (cx + 12, ry + 8))
        short_title = (
            ptitle.replace("Antique Spanish Carved Cabinet with Knights", "Spanish Carved Knights Cabinet")
            .replace("Antique Boulle and Floral Marquetry Credenza", "Boulle and Floral Marquetry Credenza")
            .replace("Antique Dutch Floral Marquetry Armchair", "1700s Dutch Marquetry Armchair")
            .replace("Pair of French Empire Style Marble Pedestals", "Pair of French Empire Pedestals")
            .replace("Persian Silk Qum Carpet in Warm Red and Ivory", "Silk Qum Carpet in Warm Red")
            .replace("Persian Silk Qum Runner Medallion Detail", "10' Persian Silk Qum Runner")
            .replace("18-Piece Limoges Style Tea Service", "18-Pc Limoges Style Tea Service")
            .replace("Joan Miro, The Gold of the Azure", "Joan Miro, The Gold of the Azure")
        )
        bb_st = p_draw.textbbox((0, 0), short_title, font=f_ct)
        p_draw.text((cx + (card_w - (bb_st[2] - bb_st[0])) // 2, ry + 248), short_title, fill=C_CHARCOAL, font=f_ct)
        sub_short = psub.split("|")[0].strip()
        bb_ss = p_draw.textbbox((0, 0), sub_short, font=f_cs)
        p_draw.text((cx + (card_w - (bb_ss[2] - bb_ss[0])) // 2, ry + 267), sub_short, fill=C_PEWTER, font=f_cs)
        # Draw inverted ghost-outline "SELECT THIS PIECE" button (#F7F5F2 fill, 1px #2B2F33 border & text)
        btn_w, btn_h = 164, 26
        bx = cx + (card_w - btn_w) // 2
        by_btn = ry + 288
        p_draw.rectangle([bx, by_btn, bx + btn_w, by_btn + btn_h], fill=C_ALABASTER, outline=C_CHARCOAL, width=1)
        btn_label = "SELECT THIS PIECE"
        bb_bl = p_draw.textbbox((0, 0), btn_label, font=f_btn)
        p_draw.text((bx + (btn_w - (bb_bl[2] - bb_bl[0])) // 2, by_btn + 7), btn_label, fill=C_CHARCOAL, font=f_btn)

    proof_path = os.path.join(ARTIFACT_DIR, "tcc-nov04-scandinavian-newsletter-proof.jpg")
    proof.save(proof_path, format="JPEG", quality=93)
    print("Saved updated visual proof:", proof_path)

    # Also build a dedicated close-up proof of the newly smoothed Hero English Tall Gothic Hallstand card (including the new header above it)
    hh_w, hh_h = 680, 830
    hh_im = Image.new("RGB", (hh_w, hh_h), C_PUTTY)
    hh_draw = ImageDraw.Draw(hh_im)
    hh_draw.rectangle([40, 20, 640, hh_h - 20], fill=C_ALABASTER, outline=C_PEWTER, width=1)

    t_kicker_hh = "Timeless Character and Fine Craftsmanship"
    bb = hh_draw.textbbox((0, 0), t_kicker_hh, font=f_red_big)
    hh_draw.text(((hh_w - (bb[2] - bb[0])) // 2, 42), t_kicker_hh, fill=C_FALUN, font=f_red_big)
    t_sub_hh = "A curated selection from our Rancho Santa Fe showroom"
    bb = hh_draw.textbbox((0, 0), t_sub_hh, font=f_italic_small)
    hh_draw.text(((hh_w - (bb[2] - bb[0])) // 2, 70), t_sub_hh, fill=C_CHARCOAL, font=f_italic_small)
    hh_draw.line([316, 96, 364, 96], fill=C_FALUN, width=2)

    hh_draw.rectangle([68, 126, 612, hh_h - 40], fill=C_ALABASTER, outline=C_PUTTY, width=1)
    hall_thumb = loaded[1][1].resize((456, 456), Image.Resampling.LANCZOS)
    hh_im.paste(hall_thumb, ((hh_w - 456) // 2, 134))
    # Draw < and > click-advance arrows and 5 carousel dots on the Hero Hallstand close-up proof
    for ax_x, arrow_ch in ((82, "<"), (562, ">")):
        hh_draw.rectangle([ax_x, 344, ax_x + 36, 380], fill=C_ALABASTER, outline=C_PUTTY, width=1)
        hh_draw.text((ax_x + 13, 354), arrow_ch, fill=C_CHARCOAL, font=f_nav)
    for di in range(5):
        dcx = (hh_w - 72) // 2 + di * 18
        d_col = C_FALUN if di == 0 else C_PUTTY
        hh_draw.ellipse([dcx - 4, 602 - 4, dcx + 4, 602 + 4], fill=d_col)
    f_hh_k = load_font(11, bold=True)
    f_hh_t = load_font(22, italic=True)
    f_hh_b = load_font(14, italic=False)
    tk = "MONUMENTAL ENGLISH OAK   |   117\" H x 83\" W x 16\" D"
    bb = hh_draw.textbbox((0, 0), tk, font=f_hh_k)
    hh_draw.text(((hh_w - (bb[2] - bb[0])) // 2, 618), tk, fill=C_PEWTER, font=f_hh_k)
    tt = "Antique English Tall Gothic Hallstand"
    bb = hh_draw.textbbox((0, 0), tt, font=f_hh_t)
    hh_draw.text(((hh_w - (bb[2] - bb[0])) // 2, 642), tt, fill=C_CHARCOAL, font=f_hh_t)
    for li, ltxt in enumerate([
        "Rising nearly ten feet in warm carved oak with pierced Gothic tracery,",
        "spire finials, wrought iron coat hooks, a central beveled mirror and an integrated hall bench."
    ]):
        bb = hh_draw.textbbox((0, 0), ltxt, font=f_hh_b)
        hh_draw.text(((hh_w - (bb[2] - bb[0])) // 2, 676 + li * 20), ltxt, fill=C_CHARCOAL, font=f_hh_b)
    btn_w, btn_h = 200, 34
    bx = (hh_w - btn_w) // 2
    by_btn = 728
    hh_draw.rectangle([bx, by_btn, bx + btn_w, by_btn + btn_h], fill=C_ALABASTER, outline=C_CHARCOAL, width=1)
    f_hh_btn = load_font(11, bold=True)
    bb_bl = hh_draw.textbbox((0, 0), "SELECT THIS PIECE", font=f_hh_btn)
    hh_draw.text((bx + (btn_w - (bb_bl[2] - bb_bl[0])) // 2, by_btn + 10), "SELECT THIS PIECE", fill=C_CHARCOAL, font=f_hh_btn)
    hh_proof_path = os.path.join(ARTIFACT_DIR, "tcc-nov04-scandinavian-hero-hallstand-proof.jpg")
    hh_im.save(hh_proof_path, format="JPEG", quality=95)
    print("Saved Hero Hallstand close-up proof:", hh_proof_path)

    # Also build a dedicated close-up proof of the first `4by` (2x2) Furniture/Marquetry/Pedestals grid
    four_w, four_h = 680, 920
    four_im = Image.new("RGB", (four_w, four_h), C_PUTTY)
    f_draw = ImageDraw.Draw(four_im)
    f_draw.rectangle([40, 20, 640, four_h - 20], fill=C_ALABASTER, outline=C_PEWTER, width=1)

    t_sec_k = "CONTINENTAL CRAFTSMANSHIP"
    bb = f_draw.textbbox((0, 0), t_sec_k, font=f_nav)
    f_draw.text(((four_w - (bb[2] - bb[0])) // 2, 44), t_sec_k, fill=C_FALUN, font=f_nav)

    f_sec_h = load_font(23, italic=True)
    t_sec_h = "Statement Furniture, 18th Century Marquetry and Marble"
    bb = f_draw.textbbox((0, 0), t_sec_h, font=f_sec_h)
    f_draw.text(((four_w - (bb[2] - bb[0])) // 2, 66), t_sec_h, fill=C_CHARCOAL, font=f_sec_h)

    four_cards = [
        (0, "SPANISH RENAISSANCE  |  83.75\" H", ["Spanish Carved Cabinet", "with Figural Knights"], ["Sculpted warm walnut with figural", "knight caryatids, pierced crestwork", "and deep relief panels."]),
        (2, "FRENCH NAPOLEON III  |  EBONIZED", ["Boulle and Floral Inlay", "Marquetry Credenza"], ["Ebonized serpentine display credenza", "with curved glass vitrines, gilt mounts", "and shaded floral inlay."]),
        (3, "CIRCA MID 1700S  |  45\" H X 24\" W", ["Antique Dutch Floral", "Marquetry Armchair"], ["Shaped vase splat, scrolling arms", "and cabriole legs inlaid with", "botanical and bird marquetry."]),
        (4, "GREEN MARBLE AND GILT  |  54.5\" H", ["Pair of French Empire", "Green Marble Pedestals"], ["Tapered green veined marble columns", "adorned with classical gilt metal", "swags and moldings."]),
    ]
    f_card_k = load_font(9, bold=True)
    f_card_t = load_font(15, italic=True)
    f_card_b = load_font(12, italic=False)
    for pos, (c_idx, ck, ct_lines, cb_lines) in enumerate(four_cards):
        r = pos // 2
        c = pos % 2
        card_w, card_h = 262, 396
        cx = 70 + c * (card_w + 16)
        ry = 104 + r * (card_h + 16)
        f_draw.rectangle([cx, ry, cx + card_w, ry + card_h], fill=C_ALABASTER, outline=C_PUTTY, width=1)
        th = loaded[c_idx][1].resize((230, 230), Image.Resampling.LANCZOS)
        four_im.paste(th, (cx + 16, ry + 10))
        bb_k = f_draw.textbbox((0, 0), ck, font=f_card_k)
        f_draw.text((cx + (card_w - (bb_k[2] - bb_k[0])) // 2, ry + 246), ck, fill=C_PEWTER, font=f_card_k)
        for ti, ttxt in enumerate(ct_lines):
            bb_t = f_draw.textbbox((0, 0), ttxt, font=f_card_t)
            f_draw.text((cx + (card_w - (bb_t[2] - bb_t[0])) // 2, ry + 262 + ti * 18), ttxt, fill=C_CHARCOAL, font=f_card_t)
        for li, ltxt in enumerate(cb_lines):
            bb_l = f_draw.textbbox((0, 0), ltxt, font=f_card_b)
            f_draw.text((cx + (card_w - (bb_l[2] - bb_l[0])) // 2, ry + 302 + li * 16), ltxt, fill=C_CHARCOAL, font=f_card_b)
        btn_w, btn_h = 168, 28
        bx = cx + (card_w - btn_w) // 2
        by_btn = ry + 356
        f_draw.rectangle([bx, by_btn, bx + btn_w, by_btn + btn_h], fill=C_ALABASTER, outline=C_CHARCOAL, width=1)
        btn_label = "SELECT THIS PIECE"
        bb_bl = f_draw.textbbox((0, 0), btn_label, font=f_btn)
        f_draw.text((bx + (btn_w - (bb_bl[2] - bb_bl[0])) // 2, by_btn + 8), btn_label, fill=C_CHARCOAL, font=f_btn)

    four_proof_path = os.path.join(ARTIFACT_DIR, "tcc-nov04-scandinavian-4by-grid-proof.jpg")
    four_im.save(four_proof_path, format="JPEG", quality=94)
    print("Saved 4by grid close-up proof:", four_proof_path)

    # Complete Responsive Pure-ASCII HTML Circular
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:title" content="Timeless Character and Fine Craftsmanship | The Chapman Collection">
<meta property="og:description" content="A curated selection of statement European antiques, carved Spanish and English woodwork, 1700s Dutch marquetry, French Empire marble pedestals and luminous Silk Qum carpets from our Rancho Santa Fe showroom.">
<meta property="og:image" content="https://renderwithoutcode.com/drafts-for-pmc-approval/2026-11-04-scandinavian-gustavian-gallery/cuts/tcc-nov04-og-banner.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<title>Timeless Character and Fine Craftsmanship - The Chapman Collection</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&amp;display=swap">
<style type="text/css">
  body, table, td, p, a, h1, h2, h3, h4 {
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
    font-family: 'Garamond', 'EB Garamond', 'Apple Garamond', 'Georgia', serif;
  }
  table {
    border-collapse: collapse;
    mso-table-lspace: 0pt;
    mso-table-rspace: 0pt;
  }
  img {
    border: 0;
    height: auto;
    line-height: 100%;
    outline: none;
    text-decoration: none;
    max-width: 100%;
  }
  .tcc-btn {
    background-color: #F7F5F2 !important;
    color: #2B2F33 !important;
    transition: background-color 0.2s ease, color 0.2s ease;
  }
  .tcc-btn:hover {
    background-color: #2B2F33 !important;
    color: #F7F5F2 !important;
  }
  .tcc-btn-td:hover {
    background-color: #2B2F33 !important;
  }
  .tcc-carousel-arrow {
    position: absolute;
    top: 34%;
    transform: translateY(-50%);
    width: 36px;
    height: 36px;
    line-height: 34px;
    text-align: center;
    background-color: #F7F5F2;
    border: 1px solid #D9D3CC;
    color: #2B2F33;
    font-family: 'Garamond', 'EB Garamond', 'Georgia', serif;
    font-size: 16px;
    cursor: pointer;
    user-select: none;
    transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
    z-index: 5;
  }
  .tcc-carousel-arrow:hover {
    background-color: #2B2F33;
    color: #F7F5F2;
    border-color: #2B2F33;
  }
  .tcc-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #D9D3CC;
    margin: 0 5px;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.2s ease;
  }
  .tcc-dot.active {
    background-color: #B35A5E;
    transform: scale(1.18);
  }
  .tcc-hero-slide {
    animation: tccFadeIn 0.38s ease;
  }
  @keyframes tccFadeIn {
    from { opacity: 0.35; }
    to { opacity: 1; }
  }
  .tcc-kicker {
    min-height: 16px;
  }
  .tcc-title {
    min-height: 42px;
  }
  .tcc-desc {
    min-height: 68px;
  }
  @media only screen and (max-width: 520px) {
    .tcc-outer-frame {
      width: 96% !important;
      max-width: 96% !important;
    }
    .tcc-pad {
      padding-left: 4% !important;
      padding-right: 4% !important;
    }
    .tcc-brand-h1 {
      font-size: 21px !important;
      letter-spacing: 1.6px !important;
      white-space: nowrap !important;
    }
    .tcc-hero-h2 {
      font-size: 18.5px !important;
      line-height: 1.25 !important;
    }
    .tcc-hero-sub {
      font-size: 13.5px !important;
    }
    .tcc-carousel-arrow {
      top: 29% !important;
      width: 30px !important;
      height: 30px !important;
      line-height: 28px !important;
      font-size: 14px !important;
    }
    .tcc-subnav {
      font-size: 8px !important;
      letter-spacing: 0.15px !important;
      white-space: nowrap !important;
    }
    .tcc-col-top {
      width: 48.5% !important;
      max-width: 48.5% !important;
      padding: 8px 6px 4px 6px !important;
      box-sizing: border-box !important;
    }
    .tcc-col-bot {
      width: 48.5% !important;
      max-width: 48.5% !important;
      padding: 4px 6px 12px 6px !important;
      box-sizing: border-box !important;
    }
    .tcc-spacer {
      width: 3% !important;
    }
    .tcc-kicker {
      min-height: 26px !important;
    }
    .tcc-title {
      min-height: 42px !important;
    }
    .tcc-desc {
      min-height: 90px !important;
    }
  }
</style>
</head>
<body style="margin:0;padding:0;background-color:#D9D3CC;">
<!-- Hidden Preheader -->
<div style="display:none;font-size:1px;color:#D9D3CC;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
  A curated selection from our Rancho Santa Fe showroom: monumental English and Spanish woodwork, 1700s Dutch floral marquetry, French Empire marble pedestals and luminous Silk Qum carpets.
</div>

<!-- Outer Surround in #D9D3CC (Gustavian Putty) -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" style="width:100%;table-layout:fixed;margin:0 auto;background-color:#D9D3CC;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;">
  <tr>
    <td align="center" style="padding:24px 0;text-align:center;">

      <!-- 600px Eloquence-Width Inner Gallery Canvas in #F7F5F2 (Bleached Nordic Alabaster) -->
      <table role="presentation" class="tcc-outer-frame" cellspacing="0" cellpadding="0" border="0" width="600" align="center" style="width:600px;max-width:96%;table-layout:fixed;margin:0 auto;background-color:#F7F5F2;border-left:1px solid #8A8F97;border-right:1px solid #8A8F97;border-top:5px solid #2B2F33;border-bottom:5px solid #2B2F33;box-sizing:border-box;text-align:left;">

        <!-- Subtle 2px #B35A5E Swedish Falun Terracotta Rose Accent Bar -->
        <tr>
          <td height="2" style="height:2px;line-height:2px;font-size:2px;background-color:#B35A5E;">&nbsp;</td>
        </tr>

        <!-- ================================================================== -->
        <!-- 1. CENTERED CREST MASTHEAD & SINGLE-LINE CATEGORY SUBNAV           -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad" align="center" style="padding:22px 3.5% 12px 3.5%;background-color:#F7F5F2;box-sizing:border-box;text-align:center;">
            <a href="https://thechapmancollection.com/" target="_blank" style="text-decoration:none;">
              <img src="__IMG_PREFIX__tcc-crest.png" alt="The Chapman Collection" width="80" style="display:block;margin:0 auto 10px auto;width:80px;max-width:80px;height:auto;border:0;">
            </a>
            <h1 class="tcc-brand-h1" style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:26.5px;letter-spacing:2.5px;text-transform:uppercase;color:#2B2F33;font-weight:normal;line-height:1.25;text-align:center;">
              The Chapman Collection
            </h1>
            <p class="tcc-subnav" style="margin:0;padding:0 0 14px 0;border-bottom:1px solid #D9D3CC;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.5px;letter-spacing:0.2px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.6;text-align:center;white-space:nowrap;">
              <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Persian Carpets</a>
              <span style="color:#D9D3CC;padding:0 2px;">|</span>
              <a href="https://thechapmancollection.com/product-category/furniture/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Fine Furniture</a>
              <span style="color:#D9D3CC;padding:0 2px;">|</span>
              <a href="https://thechapmancollection.com/product-category/artwork-tapestries/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Artworks</a>
              <span style="color:#D9D3CC;padding:0 2px;">|</span>
              <a href="https://thechapmancollection.com/product-category/accessories/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Accessories</a>
            </p>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 2. ELOQUENCE EDITORIAL TITLE CARD (FANCY GARAMOND ITALIC + ROMAN)  -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad" align="center" style="padding:8px 6% 16px 6%;background-color:#F7F5F2;text-align:center;">
            <h2 class="tcc-hero-h2" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22.5px;font-weight:normal;font-style:italic;color:#B35A5E;line-height:1.25;text-align:center;">
              Timeless Character and Fine Craftsmanship
            </h2>
            <p class="tcc-hero-sub" style="margin:0 0 12px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15px;font-weight:normal;font-style:normal;color:#2B2F33;line-height:1.45;text-align:center;">
              A curated selection from our Rancho Santa Fe showroom
            </p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="48" align="center" style="width:48px;margin:0 auto;">
              <tr>
                <td height="2" style="height:2px;line-height:2px;font-size:2px;background-color:#B35A5E;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 3. AUTO-SLIDING + CLICK-ADVANCE HERO CAROUSEL (5 HERO PIECES)      -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad" style="padding:4px 5% 24px 5%;background-color:#F7F5F2;">
            <div id="tcc-hero-carousel" style="position:relative;width:100%;background-color:#F7F5F2;border:1px solid #D9D3CC;padding:18px;box-sizing:border-box;">

              <!-- Prev / Next Click-Advance Arrows -->
              <div class="tcc-carousel-arrow" style="left:12px;" onclick="tccMoveSlide(-1)" title="Previous Piece">&#10094;</div>
              <div class="tcc-carousel-arrow" style="right:12px;" onclick="tccMoveSlide(1)" title="Next Piece">&#10095;</div>

              <!-- Slide 1: Antique English Tall Gothic Hallstand (Default Visible) -->
              <div class="tcc-hero-slide" style="display:block;text-align:center;">
                <div style="padding:6px 28px 10px 28px;background-color:#F7F5F2;text-align:center;">
                  <a href="https://thechapmancollection.com/?s=Gothic+Hallstand&amp;post_type=product" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-02-english-gothic-hallstand.jpg" alt="Antique English Tall Gothic Hallstand" width="460" style="width:100%;max-width:460px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 14px 10px 14px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    Monumental English Oak &nbsp;&bull;&nbsp; 117&quot; H x 83&quot; W x 16&quot; D
                  </p>
                  <h3 style="margin:0 0 10px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/?s=Gothic+Hallstand&amp;post_type=product" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique English Tall Gothic Hallstand</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;min-height:52px;">
                    Rising nearly ten feet in warm carved oak with pierced Gothic tracery, spire finials, wrought iron coat hooks, a central beveled mirror and an integrated hall bench.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/?s=Gothic+Hallstand&amp;post_type=product" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 2: Antique Spanish Carved Cabinet with Knights -->
              <div class="tcc-hero-slide" style="display:none;mso-hide:all;text-align:center;">
                <div style="padding:6px 28px 10px 28px;background-color:#F7F5F2;text-align:center;">
                  <a href="https://thechapmancollection.com/?s=Spanish+Cabinet+Knights&amp;post_type=product" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-01-spanish-knights-cabinet.jpg" alt="Antique Spanish Carved Cabinet with Knights" width="460" style="width:100%;max-width:460px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 14px 10px 14px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    Spanish Renaissance Walnut &nbsp;&bull;&nbsp; 83.75&quot; H x 79.5&quot; W x 25.75&quot; D
                  </p>
                  <h3 style="margin:0 0 10px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/?s=Spanish+Cabinet+Knights&amp;post_type=product" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique Spanish Carved Cabinet with Knights</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;min-height:52px;">
                    Sculpted in warm walnut with figural knight caryatids, pierced architectural crestwork, heraldic medallions and deep relief door panels.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/?s=Spanish+Cabinet+Knights&amp;post_type=product" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 3: Antique Boulle and Floral Marquetry Credenza -->
              <div class="tcc-hero-slide" style="display:none;mso-hide:all;text-align:center;">
                <div style="padding:6px 28px 10px 28px;background-color:#F7F5F2;text-align:center;">
                  <a href="https://thechapmancollection.com/?s=Boulle+Marquetry+Credenza&amp;post_type=product" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-03-boulle-marquetry-credenza.jpg" alt="Antique Boulle and Floral Marquetry Credenza" width="460" style="width:100%;max-width:460px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 14px 10px 14px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    French Napoleon III &nbsp;&bull;&nbsp; Ebonized and Floral Marquetry
                  </p>
                  <h3 style="margin:0 0 10px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/?s=Boulle+Marquetry+Credenza&amp;post_type=product" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique Boulle and Floral Marquetry Credenza</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;min-height:52px;">
                    Ebonized serpentine display credenza with curved glass side vitrines, ormolu gilt bronze mounts and intricate central floral marquetry.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/?s=Boulle+Marquetry+Credenza&amp;post_type=product" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 4: Antique Dutch Floral Marquetry Armchair -->
              <div class="tcc-hero-slide" style="display:none;mso-hide:all;text-align:center;">
                <div style="padding:6px 28px 10px 28px;background-color:#F7F5F2;text-align:center;">
                  <a href="https://thechapmancollection.com/product/antique-dutch-floral-marquetry-armchair-circa-early-to-mid-1700s/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-04-dutch-marquetry-armchair.jpg" alt="Antique Dutch Floral Marquetry Armchair Circa Early to Mid 1700s" width="460" style="width:100%;max-width:460px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 14px 10px 14px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    Circa Early to Mid 1700s &nbsp;&bull;&nbsp; 45&quot; H x 24&quot; W x 19&quot; D
                  </p>
                  <h3 style="margin:0 0 10px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/antique-dutch-floral-marquetry-armchair-circa-early-to-mid-1700s/" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique Dutch Floral Marquetry Armchair</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;min-height:52px;">
                    Shaped vase splat, scrolling arms and cabriole legs on claw and ball feet inlaid throughout with botanical and bird marquetry.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/antique-dutch-floral-marquetry-armchair-circa-early-to-mid-1700s/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 5: Pair of French Empire Style Marble Pedestals -->
              <div class="tcc-hero-slide" style="display:none;mso-hide:all;text-align:center;">
                <div style="padding:6px 28px 10px 28px;background-color:#F7F5F2;text-align:center;">
                  <a href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-05-french-empire-pedestals.jpg" alt="Pair of French Empire Style Green Marble Pedestals" width="460" style="width:100%;max-width:460px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 14px 10px 14px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    Green Marble and Gilt Mounts &nbsp;&bull;&nbsp; 54.5&quot; H x 13.75&quot; W Each
                  </p>
                  <h3 style="margin:0 0 10px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="color:#2B2F33;text-decoration:none;">Pair of French Empire Green Marble Pedestals</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;min-height:52px;">
                    Tapered green veined marble columns adorned with classical gilt metal swags, neoclassical mounts and stepped square plinths.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Clickable Carousel Dots (1-5) -->
              <div style="padding-top:10px;text-align:center;">
                <span class="tcc-dot active" onclick="tccGoSlide(0)" title="Antique English Tall Gothic Hallstand"></span>
                <span class="tcc-dot" onclick="tccGoSlide(1)" title="Antique Spanish Carved Cabinet with Knights"></span>
                <span class="tcc-dot" onclick="tccGoSlide(2)" title="Antique Boulle and Floral Marquetry Credenza"></span>
                <span class="tcc-dot" onclick="tccGoSlide(3)" title="Antique Dutch Floral Marquetry Armchair"></span>
                <span class="tcc-dot" onclick="tccGoSlide(4)" title="Pair of French Empire Green Marble Pedestals"></span>
              </div>

            </div>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 5. 4BY GRID 01: STATEMENT FURNITURE, MARQUETRY AND EMPIRE MARBLE   -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad" style="padding:4px 5% 24px 5%;background-color:#F7F5F2;">
            <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:2px;text-transform:uppercase;color:#B35A5E;font-weight:bold;text-align:center;">
              Continental Craftsmanship
            </p>
            <h3 style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:24px;font-weight:normal;font-style:italic;color:#2B2F33;text-align:center;">
              Statement Furniture, 18th Century Marquetry and Marble
            </h3>

            <!-- 4BY GRID 01 - ROW 1: SPANISH KNIGHTS CABINET + BOULLE MARQUETRY CREDENZA -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;margin-bottom:16px;">
              <tr>
                <!-- Col 1 Top: Antique Spanish Carved Cabinet with Knights -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/?s=Spanish+Cabinet+Knights&amp;post_type=product" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-01-spanish-knights-cabinet.jpg" alt="Antique Spanish Carved Cabinet with Knights" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    Spanish Renaissance &bull; 83.75&quot; H
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/?s=Spanish+Cabinet+Knights&amp;post_type=product" target="_blank" style="color:#2B2F33;text-decoration:none;">Spanish Carved Cabinet<br>with Figural Knights</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Sculpted warm walnut with figural knight caryatids, pierced crestwork and deep relief panels.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Col 2 Top: Antique Boulle & Floral Marquetry Credenza -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/?s=Boulle+Marquetry+Credenza&amp;post_type=product" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-03-boulle-marquetry-credenza.jpg" alt="Antique Boulle and Floral Marquetry Credenza" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    French Napoleon III &bull; Ebonized
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/?s=Boulle+Marquetry+Credenza&amp;post_type=product" target="_blank" style="color:#2B2F33;text-decoration:none;">Boulle and Floral Inlay<br>Marquetry Credenza</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Ebonized serpentine display credenza with curved glass vitrines, gilt mounts and floral inlay.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 1 -->
              <tr>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/?s=Spanish+Cabinet+Knights&amp;post_type=product" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/?s=Boulle+Marquetry+Credenza&amp;post_type=product" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>

            <!-- 4BY GRID 01 - ROW 2: DUTCH MARQUETRY ARMCHAIR + FRENCH EMPIRE PEDESTALS -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;">
              <tr>
                <!-- Col 3 Top: Antique Dutch Floral Marquetry Armchair (WC-3184) -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/antique-dutch-floral-marquetry-armchair-circa-early-to-mid-1700s/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-04-dutch-marquetry-armchair.jpg" alt="Antique Dutch Floral Marquetry Armchair Circa Early to Mid 1700s" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    Circa Mid 1700s &bull; 45&quot; H x 24&quot; W
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/antique-dutch-floral-marquetry-armchair-circa-early-to-mid-1700s/" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique Dutch Floral<br>Marquetry Armchair</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Shaped vase splat, scrolling arms and cabriole legs inlaid with botanical and bird marquetry.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Col 4 Top: Pair of French Empire Style Marble Pedestals (WC-3306) -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-05-french-empire-pedestals.jpg" alt="Pair of French Empire Style Green Marble Pedestals" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    Green Marble and Gilt &bull; 54.5&quot; H
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="color:#2B2F33;text-decoration:none;">Pair of French Empire<br>Green Marble Pedestals</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Tapered green veined marble columns adorned with classical gilt metal swags and moldings.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 2 -->
              <tr>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/antique-dutch-floral-marquetry-armchair-circa-early-to-mid-1700s/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 6. 4BY GRID 02: SILK QUM WEAVES, FINE PORCELAIN & MODERN ART       -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad" style="padding:0 5% 24px 5%;background-color:#F7F5F2;">
            <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:2px;text-transform:uppercase;color:#B35A5E;font-weight:bold;text-align:center;">
              Curated Across the Gallery
            </p>
            <h3 style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:24px;font-weight:normal;font-style:italic;color:#2B2F33;text-align:center;">
              Luminous Silk Weaves, Fine Porcelain and Modern Art
            </h3>

            <!-- 4BY GRID 02 - ROW 1: SILK QUM CARPET + 10-FOOT SILK QUM RUNNER -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;margin-bottom:16px;">
              <tr>
                <!-- Col 1 Top: Silk Qum Carpet in Warm Red, Ivory & Soft Neutrals (WC-3078) -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-carpet-warm-red-ivory-soft-neutrals/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-06-silk-qum-warm-red-carpet.jpg" alt="New Persian Hand Finished Silk Qum Carpet in Warm Red, Ivory and Soft Neutrals" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    Silk Qum Weave &bull; 9&#39;10&quot; x 6&#39;5&quot;
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-carpet-warm-red-ivory-soft-neutrals/" target="_blank" style="color:#2B2F33;text-decoration:none;">Persian Hand Finished<br>Silk Qum Area Carpet</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Warm terracotta and muted red softened by champagne, ivory, taupe and subtle bird motifs.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Col 2 Top: 10-Foot Silk Qum Runner Medallion Close-Up (WC-3101) -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-runner-midnight-blue-ivory-medallions/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-07-silk-qum-runner-closeup.jpg" alt="New Persian Hand Finished Silk Qum Runner Close-Up Medallion Detail" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    Silk Qum Runner &bull; 10&#39;0&quot; x 3&#39;3&quot;
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-runner-midnight-blue-ivory-medallions/" target="_blank" style="color:#2B2F33;text-decoration:none;">Persian Hand Finished<br>10&#39; Silk Qum Runner</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    A close study of the midnight blue ground, radiant ivory medallion and knotted botanicals.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 3 -->
              <tr>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-carpet-warm-red-ivory-soft-neutrals/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-runner-midnight-blue-ivory-medallions/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>

            <!-- 4BY GRID 02 - ROW 2: 18-PIECE LIMOGES TEA SERVICE + JOAN MIRO GOLD OF THE AZURE -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;">
              <tr>
                <!-- Col 3 Top: 18-Piece Porcelain Limoges Style Tea Service in Cobalt Blue & Gold (WC-3301) -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/18-pc-porcelain-limoges-style-tea-service-cobalt-blue-and-gold/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-08-limoges-tea-service.jpg" alt="18 Piece Porcelain Limoges Style Tea Service in Cobalt Blue and Gold" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    Cobalt and Gold &bull; 18-Piece Set
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/18-pc-porcelain-limoges-style-tea-service-cobalt-blue-and-gold/" target="_blank" style="color:#2B2F33;text-decoration:none;">18-Piece Porcelain<br>Limoges Style Tea Set</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Rich cobalt glaze and raised gilt relief with hand painted courting scenes on cups and teapot.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Col 4 Top: Joan Miro, The Gold of the Azure, 1979 France (WC-3160) -->
                <td class="tcc-col-top" width="48.5%" valign="top" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;padding:12px 12px 4px 12px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/joan-miro-the-gold-of-the-azure-original-color-plate-in-custom-frame/" target="_blank" style="text-decoration:none;">
                    <img src="__IMG_PREFIX__tcc-f7f5f2-09-joan-miro-gold-of-azure.jpg" alt="Joan Miro The Gold of the Azure Original Color Plate in Custom Frame" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:9.5px;letter-spacing:1.3px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;">
                    1979 France &bull; 21.75&quot; x 19.25&quot;
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/joan-miro-the-gold-of-the-azure-original-color-plate-in-custom-frame/" target="_blank" style="color:#2B2F33;text-decoration:none;">Joan Miro, The Gold of<br>the Azure (1979 Plate)</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14.5px;line-height:1.55;color:#2B2F33;">
                    Original 1979 French color plate presented in a sculpted custom giltwood frame with linen liner.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 4 -->
              <tr>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/18-pc-porcelain-limoges-style-tea-service-cobalt-blue-and-gold/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot" width="48.5%" valign="bottom" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;padding:6px 12px 14px 12px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/joan-miro-the-gold-of-the-azure-original-color-plate-in-custom-frame/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;padding:8px 18px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 7. RANCHO SANTA FE SHOWROOM INVITATION & SIGNATURE                 -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad" style="padding:6px 6% 26px 6%;background-color:#F7F5F2;box-sizing:border-box;">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;border:1px solid #D9D3CC;background-color:#D9D3CC;margin:4px 0 22px 0;">
              <tr>
                <td align="center" style="padding:22px 20px;text-align:center;background-color:#F7F5F2;">
                  <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#B35A5E;font-weight:bold;">
                    Visit Our Rancho Santa Fe Gallery
                  </p>
                  <p style="margin:0 0 18px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16.5px;line-height:1.65;color:#2B2F33;">
                    Open seven days a week in the heart of the Rancho Santa Fe Village. Stop in to experience these pieces in person, or reply directly for private home trials and white glove delivery details.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:13px;letter-spacing:2px;text-transform:uppercase;padding:12px 30px;display:inline-block;">Explore the Full Collection</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>

            <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:17px;line-height:1.65;color:#2B2F33;text-align:left;">
              Warmly,<br>Melissa Chapman
            </p>

            <!-- Compact Signature Footer in Scandinavian Palette -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;background-color:#F7F5F2;border-top:1px solid #D9D3CC;padding-top:14px;">
              <tr>
                <td width="54" valign="middle" align="center" style="width:54px;padding-right:12px;border-right:1px solid #D9D3CC;">
                  <img src="__IMG_PREFIX__tcc-crest.png" alt="The Chapman Collection" width="46" style="width:46px;max-width:46px;height:auto;display:block;border:0;">
                </td>
                <td valign="middle" style="padding-left:12px;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;color:#2B2F33;text-align:left;">
                  <p style="margin:0 0 3px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12.5px;font-weight:bold;letter-spacing:1.2px;text-transform:uppercase;color:#2B2F33;line-height:1.35;">
                    THE CHAPMAN COLLECTION
                  </p>
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;line-height:1.45;color:#8A8F97;">
                    <a href="tel:+18583492638" style="color:#2B2F33;text-decoration:none;font-weight:bold;">858-349-2638</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.google.com/maps/search/?api=1&amp;query=The+Chapman+Collection+6014+La+Granada+Rancho+Santa+Fe+CA+92067" target="_blank" style="color:#8A8F97;text-decoration:none;">6014 La Granada, Rancho Santa Fe, CA 92067</a>
                  </p>
                  <p style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10px;letter-spacing:1px;color:#B35A5E;font-weight:bold;line-height:1.5;">
                    <a href="https://thechapmancollection.com/" target="_blank" style="color:#B35A5E;text-decoration:none;">WEBSITE</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.instagram.com/thechapmancollection/" target="_blank" style="color:#B35A5E;text-decoration:none;">INSTAGRAM</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.facebook.com/TheChapmanCollection" target="_blank" style="color:#B35A5E;text-decoration:none;">FACEBOOK</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.youtube.com/@TheChapmanCollection" target="_blank" style="color:#B35A5E;text-decoration:none;">YOUTUBE</a>
                  </p>
                </td>
              </tr>
            </table>

          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
<script type="text/javascript">
(function() {
  var currentSlide = 0;
  var slides = document.querySelectorAll('#tcc-hero-carousel .tcc-hero-slide');
  var dots = document.querySelectorAll('#tcc-hero-carousel .tcc-dot');
  var carousel = document.getElementById('tcc-hero-carousel');
  var timer = null;
  var touchStartX = 0;

  function showSlide(idx) {
    if (!slides.length) return;
    currentSlide = (idx + slides.length) % slides.length;
    for (var i = 0; i < slides.length; i++) {
      slides[i].style.display = (i === currentSlide) ? 'block' : 'none';
    }
    for (var j = 0; j < dots.length; j++) {
      if (j === currentSlide) {
        dots[j].classList.add('active');
      } else {
        dots[j].classList.remove('active');
      }
    }
  }

  window.tccMoveSlide = function(step) {
    showSlide(currentSlide + step);
    resetTimer();
  };

  window.tccGoSlide = function(idx) {
    showSlide(idx);
    resetTimer();
  };

  function startTimer() {
    stopTimer();
    timer = setInterval(function() {
      showSlide(currentSlide + 1);
    }, 4000);
  }

  function stopTimer() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  function resetTimer() {
    startTimer();
  }

  if (carousel) {
    carousel.addEventListener('mouseenter', stopTimer);
    carousel.addEventListener('mouseleave', startTimer);
    carousel.addEventListener('touchstart', function(e) {
      if (e.changedTouches && e.changedTouches.length > 0) {
        touchStartX = e.changedTouches[0].screenX;
      }
      stopTimer();
    }, {passive: true});
    carousel.addEventListener('touchend', function(e) {
      if (e.changedTouches && e.changedTouches.length > 0) {
        var dx = e.changedTouches[0].screenX - touchStartX;
        if (Math.abs(dx) > 40) {
          showSlide(currentSlide + (dx < 0 ? 1 : -1));
        }
      }
      startTimer();
    }, {passive: true});
  }

  startTimer();
})();
</script>
</body>
</html>
"""

    non_ascii = [c for c in html_template if ord(c) > 127]
    assert not non_ascii, f"Found non-ASCII chars: {non_ascii}"

    # Write local preview HTMLs (using relative `cuts/` path)
    local_html = html_template.replace("__IMG_PREFIX__", "cuts/")
    for p in (
        os.path.join(DRAFT_DIR, "index.html"),
        os.path.join(NRL_DRAFT_DIR, "index.html"),
    ):
        with open(p, "w", encoding="ascii") as f:
            f.write(local_html)
        print("Wrote preview HTML:", p)

    # Write Omnisend full-import HTML (using absolute HTTPS CDN path)
    cdn_prefix = "https://renderwithoutcode.com/drafts-for-pmc-approval/2026-11-04-scandinavian-gustavian-gallery/cuts/"
    omnisend_html = html_template.replace("__IMG_PREFIX__", cdn_prefix)
    for p in (
        os.path.join(DRAFT_DIR, "2026-11-04-Omnisend_Scandinavian_Gustavian_Gallery_Full_Import.html"),
        os.path.join(NRL_DRAFT_DIR, "2026-11-04-Omnisend_Scandinavian_Gustavian_Gallery_Full_Import.html"),
    ):
        with open(p, "w", encoding="ascii") as f:
            f.write(omnisend_html)
        print("Wrote Omnisend import HTML:", p)


if __name__ == "__main__":
    main()
