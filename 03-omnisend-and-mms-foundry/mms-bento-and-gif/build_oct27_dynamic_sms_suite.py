import os
from PIL import Image, ImageDraw, ImageFont

BASE_CAMPAIGN_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars"
CUTS_DIR = os.path.join(BASE_CAMPAIGN_DIR, "cuts")
NRL_ROOT = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval"
NRL_SUB = os.path.join(NRL_ROOT, "2026-10-27-autumn-warmth-and-old-world-peculiars")
NRL_CUTS = os.path.join(NRL_SUB, "cuts")

os.makedirs(CUTS_DIR, exist_ok=True)
os.makedirs(NRL_CUTS, exist_ok=True)

CREST_PATH = os.path.join(NRL_CUTS, "tcc-oct23-crest.png")

BG_OUTER = (239, 233, 223)      # #EFE9DF
BG_PARCHMENT = (248, 243, 236)  # #F8F3EC
BURGUNDY = (112, 29, 50)        # #701D32
GOLD_LINE = (200, 182, 142)     # #C8B68E
GOLD_TEXT = (140, 109, 70)      # #8C6D46
INK_DARK = (31, 29, 28)         # #1F1D1C

def load_font(names, size):
    for name in names:
        p = os.path.join(r"C:\Windows\Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

f_reg = lambda sz: load_font(["gara.ttf", "georgia.ttf", "times.ttf"], sz)
f_bold = lambda sz: load_font(["garabd.ttf", "georgiab.ttf", "timesbd.ttf"], sz)
f_ital = lambda sz: load_font(["garait.ttf", "georgiai.ttf", "timesi.ttf"], sz)

def paste_centered(canvas, img_path, box, bg_color=BG_PARCHMENT):
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

# ==============================================================================
# 1. BUILD HIGH-RES MMS COMPILATION CARD (1080 x 1350 Portrait 4:5) - NO SWORD
# ==============================================================================
W, H = 1080, 1350
card = Image.new("RGB", (W, H), BG_OUTER)
draw = ImageDraw.Draw(card)

pad = 28
draw.rectangle([pad, pad, W - pad, H - pad], fill=BG_PARCHMENT, outline=GOLD_LINE, width=3)
draw.rectangle([pad, pad, W - pad, pad + 10], fill=BURGUNDY)
draw.rectangle([pad, H - pad - 10, W - pad, H - pad], fill=BURGUNDY)

if os.path.exists(CREST_PATH):
    crest = Image.open(CREST_PATH).convert("RGBA")
    crest.thumbnail((86, 86), Image.Resampling.LANCZOS)
    card.paste(crest, ((W - crest.width) // 2, 54), mask=crest.split()[-1])

draw_centered_text(draw, 148, "THE CHAPMAN COLLECTION", f_reg(30), INK_DARK, W)
draw_centered_text(draw, 186, "RANCHO SANTA FE  •  OLD WORLD CABINETS & AUTUMN SALE", f_bold(15), GOLD_TEXT, W)
draw.line([(90, 214), (W - 90, 214)], fill=GOLD_LINE, width=2)
draw_centered_text(draw, 224, "Autumn warmth and Old World charm", f_ital(38), BURGUNDY, W)

# Balanced 2x3 Bento Grid showcasing all 4 Old World Cabinets + Polychrome Mirror + Persian Silk Qum Runner
items_bento = [
    ("tcc-oct27-cab-01-metal-clad.jpg", "Metal Clad Door Cabinet", "Sale $2,400"),
    ("tcc-oct27-cab-02-carved-strap.jpg", "Carved Antique Door Cabinet", "Sale $2,400"),
    ("tcc-oct27-cab-04-red-patina.jpg", "Red Patina Door Cabinet", "Sale $2,450"),
    ("tcc-oct27-cab-03-blue-patina.jpg", "Pale Blue Patina Cabinet", "Sale $2,800"),
    ("tcc-oct27-cut-01-polychrome-mirror-v2.jpg", "75¾\" Polychrome Mirror", "Sale $2,950"),
    ("tcc-oct27-cut-05-silk-qum-runner-v2.jpg", "9'10\" Silk Qum Runner", "Sale $1,850"),
]

grid_left = 60
grid_top = 284
col_w = 304
row_h = 435
gap_x = 24
gap_y = 22

for idx, (img_name, label, price) in enumerate(items_bento):
    r = idx // 3
    c = idx % 3
    cx1 = grid_left + c * (col_w + gap_x)
    cy1 = grid_top + r * (row_h + gap_y)
    cx2 = cx1 + col_w
    cy2 = cy1 + row_h

    draw.rectangle([cx1, cy1, cx2, cy2], fill=BG_PARCHMENT, outline=GOLD_LINE, width=2)
    paste_centered(card, os.path.join(CUTS_DIR, img_name), (cx1 + 12, cy1 + 12, cx2 - 12, cy2 - 78))

    lbl_font = f_bold(19)
    pr_font = f_bold(19)
    lb_box = draw.textbbox((0, 0), label, font=lbl_font)
    lw = lb_box[2] - lb_box[0]
    draw.text((cx1 + (col_w - lw) // 2, cy2 - 64), label, font=lbl_font, fill=INK_DARK)

    pr_box = draw.textbbox((0, 0), price, font=pr_font)
    pw = pr_box[2] - pr_box[0]
    draw.text((cx1 + (col_w - pw) // 2, cy2 - 36), price, font=pr_font, fill=BURGUNDY)

btn_w, btn_h = 560, 56
btn_x1 = (W - btn_w) // 2
btn_y1 = 1196
draw.rectangle([btn_x1, btn_y1, btn_x1 + btn_w, btn_y1 + btn_h], fill=BURGUNDY, outline=GOLD_LINE, width=2)
draw_centered_text(draw, btn_y1 + 13, "Tap Link Below to View Full Autumn Circular", f_reg(24), (255, 255, 255), W)
draw_centered_text(draw, 1268, "6014 La Granada, Rancho Santa Fe  •  (858) 349-2638  •  Open 7 Days", f_bold(17), GOLD_TEXT, W)

mms_card_name = "tcc-oct27-mms-compilation-card.jpg"
for out_dir in [CUTS_DIR, NRL_CUTS]:
    card.save(os.path.join(out_dir, mms_card_name), "JPEG", quality=92, optimize=True)
print("Saved static MMS compilation card (no sword):", mms_card_name)

# ==============================================================================
# 2. BUILD OPENGRAPH 1200x630 LINK PREVIEW BANNER - NO SWORD
# ==============================================================================
OG_W, OG_H = 1200, 630
og = Image.new("RGB", (OG_W, OG_H), BG_OUTER)
og_draw = ImageDraw.Draw(og)
og_draw.rectangle([18, 18, OG_W - 18, OG_H - 18], fill=BG_PARCHMENT, outline=GOLD_LINE, width=2)
og_draw.rectangle([18, 18, OG_W - 18, 25], fill=BURGUNDY)
og_draw.rectangle([18, OG_H - 25, OG_W - 18, OG_H - 18], fill=BURGUNDY)

if os.path.exists(CREST_PATH):
    cr_og = Image.open(CREST_PATH).convert("RGBA")
    cr_og.thumbnail((76, 76), Image.Resampling.LANCZOS)
    og.paste(cr_og, (64, 58), mask=cr_og.split()[-1])

og_draw.text((64, 150), "THE CHAPMAN COLLECTION", font=f_bold(22), fill=GOLD_TEXT)
og_draw.text((64, 188), "Autumn warmth and", font=f_ital(44), fill=BURGUNDY)
og_draw.text((64, 240), "Old World charm", font=f_ital(44), fill=BURGUNDY)
og_draw.line([(64, 304), (470, 304)], fill=GOLD_LINE, width=2)
og_draw.text((64, 324), "Four custom made Old World", font=f_reg(24), fill=INK_DARK)
og_draw.text((64, 356), "antique door cabinets alongside", font=f_reg(24), fill=INK_DARK)
og_draw.text((64, 388), "a 75¾\" carved architectural", font=f_reg(24), fill=INK_DARK)
og_draw.text((64, 420), "mirror and a nearly ten foot", font=f_reg(24), fill=INK_DARK)
og_draw.text((64, 452), "Persian silk Qum runner on sale.", font=f_reg(24), fill=INK_DARK)

og_draw.rectangle([64, 505, 390, 555], fill=BURGUNDY, outline=GOLD_LINE, width=2)
og_draw.text((92, 517), "Explore the Collection →", font=f_reg(23), fill=(255, 255, 255))

og_items = [
    ("tcc-oct27-cab-01-metal-clad.jpg", (510, 52, 665, 565)),
    ("tcc-oct27-cab-03-blue-patina.jpg", (678, 52, 833, 565)),
    ("tcc-oct27-cut-01-polychrome-mirror-v2.jpg", (846, 52, 1001, 565)),
    ("tcc-oct27-cut-05-silk-qum-runner-v2.jpg", (1014, 52, 1168, 565)),
]
for fname, box in og_items:
    og_draw.rectangle(box, fill=BG_PARCHMENT, outline=GOLD_LINE, width=2)
    paste_centered(og, os.path.join(CUTS_DIR, fname), (box[0]+8, box[1]+10, box[2]-8, box[3]-10))

og_name = "tcc-oct27-og-share-banner.jpg"
for out_dir in [CUTS_DIR, NRL_CUTS]:
    og.save(os.path.join(out_dir, og_name), "JPEG", quality=90, optimize=True)
print("Saved OpenGraph share banner (no sword):", og_name)

# ==============================================================================
# 3. BUILD ANIMATED MMS GIF SHOWCASE (< 500 KB) - NO SWORD
# ==============================================================================
GW, GH = 600, 750
frames = []

f1 = card.resize((GW, GH), Image.Resampling.LANCZOS)
frames.append(f1)

slides_spec = [
    (
        "OLD WORLD COLLECTION",
        "Repurposed Antique Door Cabinets",
        [
            ("tcc-oct27-cab-01-metal-clad.jpg", "Metal Clad Door Cabinet", "59½\" H × 32½\" W • Sale $2,400"),
            ("tcc-oct27-cab-03-blue-patina.jpg", "Pale Blue Patina Cabinet", "88½\" H × 50\" W • Sale $2,800"),
        ]
    ),
    (
        "OLD WORLD COLLECTION",
        "Carved Timber & Iron Strap Doors",
        [
            ("tcc-oct27-cab-02-carved-strap.jpg", "Carved Antique Door Cabinet", "61½\" H × 34½\" W • Sale $2,400"),
            ("tcc-oct27-cab-04-red-patina.jpg", "Red Patina Carved Cabinet", "88½\" H × 50\" W • Sale $2,450"),
        ]
    ),
    (
        "ARCHITECTURAL SCALE & SILK QUM",
        "Carved Mirror & Persian Silk Runner",
        [
            ("tcc-oct27-cut-01-polychrome-mirror-v2.jpg", "Polychrome Mirror", "75¾\" H × 53½\" W • Sale $2,950"),
            ("tcc-oct27-cut-05-silk-qum-runner-v2.jpg", "9'10\" Silk Qum Runner", "Turquoise & Taupe • Sale $1,850"),
        ]
    ),
]

for kicker, headline, pair in slides_spec:
    fr = Image.new("RGB", (GW, GH), BG_OUTER)
    d = ImageDraw.Draw(fr)
    d.rectangle([16, 16, GW - 16, GH - 16], fill=BG_PARCHMENT, outline=GOLD_LINE, width=2)
    d.rectangle([16, 16, GW - 16, 22], fill=BURGUNDY)
    d.rectangle([16, GH - 22, GW - 16, GH - 16], fill=BURGUNDY)

    draw_centered_text(d, 38, "THE CHAPMAN COLLECTION", f_bold(15), GOLD_TEXT, GW)
    draw_centered_text(d, 64, kicker, f_bold(12), BURGUNDY, GW)
    draw_centered_text(d, 86, headline, f_ital(26), INK_DARK, GW)
    d.line([(50, 124), (GW - 50, 124)], fill=GOLD_LINE, width=1)

    for idx, (img_f, title, sub) in enumerate(pair):
        bx1 = 36 + idx * 270
        by1 = 142
        bx2 = bx1 + 258
        by2 = 610
        d.rectangle([bx1, by1, bx2, by2], fill=BG_PARCHMENT, outline=GOLD_LINE, width=2)
        paste_centered(fr, os.path.join(CUTS_DIR, img_f), (bx1 + 10, by1 + 10, bx2 - 10, by2 - 74))

        tf = f_bold(16)
        sf = f_bold(14)
        tb = d.textbbox((0, 0), title, font=tf)
        tw = tb[2] - tb[0]
        d.text((bx1 + (258 - tw) // 2, by2 - 58), title, font=tf, fill=INK_DARK)

        sb = d.textbbox((0, 0), sub, font=sf)
        sw = sb[2] - sb[0]
        d.text((bx1 + (258 - sw) // 2, by2 - 32), sub, font=sf, fill=BURGUNDY)

    d.rectangle([90, 636, GW - 90, 678], fill=BURGUNDY, outline=GOLD_LINE, width=2)
    draw_centered_text(d, 646, "Tap Link Below to Browse the Collection", f_reg(18), (255, 255, 255), GW)
    draw_centered_text(d, 694, "6014 La Granada, Rancho Santa Fe  •  (858) 349-2638", f_bold(13), GOLD_TEXT, GW)
    frames.append(fr)

gif_name = "tcc-oct27-mms-dynamic-showcase.gif"
quantized_frames = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT) for f in frames]
for out_dir in [CUTS_DIR, NRL_CUTS]:
    gif_path = os.path.join(out_dir, gif_name)
    quantized_frames[0].save(
        gif_path,
        save_all=True,
        append_images=quantized_frames[1:],
        duration=[2200, 2000, 2000, 2000],
        loop=0,
        optimize=True,
    )
print("Saved animated MMS GIF (no sword):", gif_name, os.path.getsize(os.path.join(CUTS_DIR, gif_name)), "bytes")
