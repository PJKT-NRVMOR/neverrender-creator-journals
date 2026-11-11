import math
import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\card"
ARTIFACT_DIR = r"C:\Users\Saturn\.gemini\antigravity\brain\ddfb1592-a0de-4352-8468-ba82ec391e08"


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


FONT_SANS_BOLD = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
]
FONT_SANS_REG = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
]
FONT_MONO_BOLD = [
    r"C:\Windows\Fonts\consolab.ttf",
    r"C:\Windows\Fonts\courbd.ttf",
]


def draw_star(draw, cx, cy, r_outer, r_inner, fill):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def render_dsuite_signature_card(mode="corporate_light", out_paths=()):
    """
    Renders a 2x Retina (1040 x 356 px -> 520 x 178 px @ 1x) email signature card.
    - 'corporate_light': Clean light 'corporate hacker' D-Suite card (#F8FAFC paper,
      #123544 Deep Petrol-Teal frame & primary button, #0090B8 Aqua-Cyan & #FF6B2B Solar Orange accents).
    - 'dark': Deep Petrol-Teal & Solar HUD dark studio card (#102E3C / #0B222D / #2CE5F6 / #FF6B2B).
    """
    W, H = 1040, 356
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if mode == "corporate_light":
        # Clean Light "Corporate Hacker" D-Suite Palette
        bg_outer_shadow = (18, 53, 68, 255)      # #123544 Deep Petrol-Teal architectural shadow
        shadow_rim = (0, 144, 184, 255)          # #0090B8 subtle cyan technical rim
        bg_card = (250, 252, 254, 255)           # #FAFCFE Crisp Executive Paper White
        bg_callout = (240, 246, 250, 255)        # #F0F6FA Soft Slate-Ice Callout
        border_main = (18, 53, 68, 255)          # #123544 Deep Petrol-Teal border
        hud_cyan = (0, 144, 184, 255)            # #0090B8 Crisp Executive Aqua-Cyan
        hud_cyan_bright = (44, 229, 246, 255)    # #2CE5F6 Electric Aqua-Cyan top bar highlight
        solar_orange = (255, 107, 43, 255)       # #FF6B2B Molten Solar Orange
        text_name = (11, 34, 45, 255)            # #0B222D Deep Petrol-Obsidian
        text_sub_primary = (18, 53, 68, 255)     # #123544 Deep Petrol-Teal
        text_sub_slash = (234, 88, 30, 255)      # #EA581E Solar Orange '//'
        text_sub_tag = (0, 130, 168, 255)        # #0082A8 Technical Cyan tag
        text_body = (30, 58, 72, 255)            # #1E3A48 Slate-Petrol body copy
        dash_color = (184, 206, 218, 255)        # #B8CEDA clean dashed rule
        callout_border = (206, 224, 234, 255)    # #CEE0EA crisp callout hairline

        # Left Badge: [ ► NEVERRENDER LABS // SRE ]
        badge_left_bg = (240, 246, 250, 255)     # #F0F6FA subtle slate-ice
        badge_left_fg = (18, 53, 68, 255)        # #123544 Deep Petrol text
        badge_left_tri = (255, 107, 43, 255)     # #FF6B2B Solar Orange play triangle
        badge_left_bd = (18, 53, 68, 255)        # #123544 crisp border

        # Right Badge: [ ★ GOOGLE LABS FEATURED ]
        badge_right_bg = (234, 248, 252, 255)    # #EAF8FC soft ice-cyan
        badge_right_fg = (0, 118, 154, 255)      # #00769A deep cyan text
        badge_right_star = (0, 144, 184, 255)    # #0090B8 cyan star
        badge_right_bd = (0, 144, 184, 255)      # #0090B8 border

        # Button 1: Executive Deep Petrol-Teal with Solar Orange Play Arrow
        btn1_bg = (18, 53, 68, 255)              # #123544 Deep Petrol-Teal
        btn1_fg = (255, 255, 255, 255)           # #FFFFFF
        btn1_tri = (255, 107, 43, 255)           # #FF6B2B Solar Orange play arrow
        btn1_bd = (11, 34, 45, 255)              # #0B222D
        btn1_shadow = (255, 107, 43, 255)        # #FF6B2B crisp Solar Orange offset shadow

        # Button 2: Crisp White with Deep Petrol text & Cyan offset shadow
        btn2_bg = (255, 255, 255, 255)           # #FFFFFF
        btn2_fg = (11, 34, 45, 255)              # #0B222D
        btn2_bd = (18, 53, 68, 255)              # #123544
        btn2_shadow = (0, 144, 184, 255)         # #0090B8 Cyan offset shadow

        tag_right_fg = (18, 53, 68, 255)         # #123544
        tag_bracket_fg = (234, 88, 30, 255)      # #EA581E
    else:
        # D-Suite Petrol-Teal & Solar HUD Dark Palette
        bg_outer_shadow = (6, 15, 21, 255)
        shadow_rim = (255, 107, 43, 255)
        bg_card = (16, 46, 60, 255)
        bg_callout = (11, 34, 45, 255)
        border_main = (44, 229, 246, 255)
        hud_cyan = (44, 229, 246, 255)
        hud_cyan_bright = (44, 229, 246, 255)
        solar_orange = (255, 107, 43, 255)
        text_name = (255, 255, 255, 255)
        text_sub_primary = (44, 229, 246, 255)
        text_sub_slash = (255, 107, 43, 255)
        text_sub_tag = (255, 140, 66, 255)
        text_body = (244, 250, 252, 255)
        dash_color = (34, 96, 118, 255)
        callout_border = (26, 78, 98, 255)

        badge_left_bg = (34, 42, 48, 255)
        badge_left_fg = (255, 122, 64, 255)
        badge_left_tri = (255, 107, 43, 255)
        badge_left_bd = (255, 107, 43, 255)

        badge_right_bg = (12, 54, 70, 255)
        badge_right_fg = (44, 229, 246, 255)
        badge_right_star = (44, 229, 246, 255)
        badge_right_bd = (44, 229, 246, 255)

        btn1_bg = (255, 107, 43, 255)
        btn1_fg = (255, 255, 255, 255)
        btn1_tri = (255, 255, 255, 255)
        btn1_bd = (255, 158, 94, 255)
        btn1_shadow = (7, 20, 28, 255)

        btn2_bg = (11, 34, 45, 255)
        btn2_fg = (44, 229, 246, 255)
        btn2_bd = (44, 229, 246, 255)
        btn2_shadow = (7, 20, 28, 255)

        tag_right_fg = (44, 229, 246, 255)
        tag_bracket_fg = (255, 107, 43, 255)

    # Fonts (scaled for 2x Retina 1040px width)
    f_badge = load_font(FONT_MONO_BOLD, 19)
    f_name = load_font(FONT_SANS_BOLD, 42)
    f_sub = load_font(FONT_MONO_BOLD, 22)
    f_body = load_font(FONT_SANS_REG, 22)
    f_btn = load_font(FONT_MONO_BOLD, 20)
    f_tag = load_font(FONT_MONO_BOLD, 19)

    cx0, cy0, cx1, cy1 = 8, 8, W - 14, H - 14

    # 1. Hard Pixel Offset Shadow (bottom-right)
    draw.rectangle([cx0 + 7, cy0 + 7, cx1 + 7, cy1 + 7], fill=bg_outer_shadow)
    draw.rectangle([cx0 + 9, cy0 + 9, cx1 + 9, cy1 + 9], outline=shadow_rim, width=2)

    # 2. Main Card Fill & 3px Structural Border
    draw.rectangle([cx0, cy0, cx1, cy1], fill=bg_card, outline=border_main, width=3)

    # Top Tri-Segment D-Suite Accent Bar (Deep Petrol -> Electric Aqua-Cyan -> Molten Solar Orange)
    seg1 = cx0 + int((cx1 - cx0) * 0.45)
    seg2 = cx0 + int((cx1 - cx0) * 0.78)
    draw.rectangle([cx0 + 3, cy0 + 3, seg1, cy0 + 8], fill=border_main)
    draw.rectangle([seg1, cy0 + 3, seg2, cy0 + 8], fill=hud_cyan_bright)
    draw.rectangle([seg2, cy0 + 3, cx1 - 3, cy0 + 8], fill=solar_orange)

    # Subtle HUD Corner Ticks (Top-Left Cyan, Bottom-Right Solar Orange)
    tick = 22
    draw.line([(cx0, cy0), (cx0 + tick, cy0)], fill=hud_cyan, width=5)
    draw.line([(cx0, cy0), (cx0, cy0 + tick)], fill=hud_cyan, width=5)
    draw.line([(cx1 - tick, cy1), (cx1, cy1)], fill=solar_orange, width=5)
    draw.line([(cx1, cy1 - tick), (cx1, cy1)], fill=solar_orange, width=5)

    pad_x = 40

    # 3. Row 1: Top Badges (y = 28..64)
    by0, by1 = 28, 64
    b1_x0, b1_x1 = pad_x, pad_x + 332
    draw.rectangle([b1_x0, by0, b1_x1, by1], fill=badge_left_bg, outline=badge_left_bd, width=2)
    tri_x, tri_y = b1_x0 + 15, by0 + 11
    draw.polygon([(tri_x, tri_y), (tri_x, tri_y + 14), (tri_x + 12, tri_y + 7)], fill=badge_left_tri)
    draw.text((b1_x0 + 35, by0 + 7), "NEVERRENDER LABS // SRE", font=f_badge, fill=badge_left_fg)

    b2_w = 304
    b2_x1 = cx1 - pad_x + 8
    b2_x0 = b2_x1 - b2_w
    draw.rectangle([b2_x0, by0, b2_x1, by1], fill=badge_right_bg, outline=badge_right_bd, width=2)
    draw_star(draw, b2_x0 + 22, by0 + 18, r_outer=8.0, r_inner=3.4, fill=badge_right_star)
    draw.text((b2_x0 + 38, by0 + 7), "GOOGLE LABS FEATURED", font=f_badge, fill=badge_right_fg)

    # 4. Row 2: Name & Multi-Tone Subtitle
    draw.text((pad_x, 76), "Matthew Wyatt", font=f_name, fill=text_name)

    sub_y = 128
    s1 = "Creative Technologist & 3D / AI Media Specialist "
    s2 = "// "
    s3 = "v4.1 D-SUITE"
    draw.text((pad_x, sub_y), s1, font=f_sub, fill=text_sub_primary)
    w1 = draw.textlength(s1, font=f_sub)
    draw.text((pad_x + w1, sub_y), s2, font=f_sub, fill=text_sub_slash)
    w2 = draw.textlength(s2, font=f_sub)
    draw.text((pad_x + w1 + w2, sub_y), s3, font=f_sub, fill=text_sub_tag)

    # 5. Row 3: Dashed HUD Divider (y = 166)
    div_y = 166
    dx = pad_x
    while dx < cx1 - pad_x + 8:
        draw.line([(dx, div_y), (min(dx + 12, cx1 - pad_x + 8), div_y)], fill=dash_color, width=2)
        dx += 20

    # 6. Row 4: Callout Box with Molten Solar Orange Left Accent Bar (y = 180..268)
    box_x0, box_y0, box_x1, box_y1 = pad_x, 180, cx1 - pad_x + 8, 268
    draw.rectangle([box_x0, box_y0, box_x1, box_y1], fill=bg_callout, outline=callout_border, width=2)
    draw.rectangle([box_x0, box_y0, box_x0 + 7, box_y1], fill=solar_orange)

    draw.text(
        (box_x0 + 22, box_y0 + 15),
        "Architecting real-time 3D, generative AI pipelines, and agentic workflows",
        font=f_body,
        fill=text_body,
    )
    draw.text(
        (box_x0 + 22, box_y0 + 45),
        "that push boundaries without production lag.",
        font=f_body,
        fill=text_body,
    )

    # 7. Row 5: Action Buttons & Right Model Tag (y = 284..330)
    bt_y0, bt_y1 = 284, 330

    # Button 1: [ ► RENDERWITHOUTCODE.COM ]
    bt1_x0, bt1_x1 = pad_x, pad_x + 312
    draw.rectangle([bt1_x0 + 4, bt_y0 + 4, bt1_x1 + 4, bt_y1 + 4], fill=btn1_shadow)
    draw.rectangle([bt1_x0, bt_y0, bt1_x1, bt_y1], fill=btn1_bg, outline=btn1_bd, width=2)
    t1_x, t1_y = bt1_x0 + 18, bt_y0 + 15
    draw.polygon([(t1_x, t1_y), (t1_x, t1_y + 16), (t1_x + 13, t1_y + 8)], fill=btn1_tri)
    draw.text((bt1_x0 + 40, bt_y0 + 11), "RENDERWITHOUTCODE.COM", font=f_btn, fill=btn1_fg)

    # Button 2: [ 8-BIT RESUME ]
    bt2_x0 = bt1_x1 + 20
    bt2_x1 = bt2_x0 + 190
    draw.rectangle([bt2_x0 + 4, bt_y0 + 4, bt2_x1 + 4, bt_y1 + 4], fill=btn2_shadow)
    draw.rectangle([bt2_x0, bt_y0, bt2_x1, bt_y1], fill=btn2_bg, outline=btn2_bd, width=2)
    w_btn2 = draw.textlength("8-BIT RESUME", font=f_btn)
    draw.text((bt2_x0 + (190 - w_btn2) / 2, bt_y0 + 11), "8-BIT RESUME", font=f_btn, fill=btn2_fg)

    # Right Tag: [GEMINI 4 CARBON] with Solar Orange brackets
    b_open = "["
    b_mid = "GEMINI 4 CARBON"
    b_close = "]"
    w_open = draw.textlength(b_open, font=f_tag)
    w_mid = draw.textlength(b_mid, font=f_tag)
    w_close = draw.textlength(b_close, font=f_tag)
    tx0 = cx1 - pad_x + 4 - (w_open + w_mid + w_close)
    draw.text((tx0, bt_y0 + 12), b_open, font=f_tag, fill=tag_bracket_fg)
    draw.text((tx0 + w_open, bt_y0 + 12), b_mid, font=f_tag, fill=tag_right_fg)
    draw.text((tx0 + w_open + w_mid, bt_y0 + 12), b_close, font=f_tag, fill=tag_bracket_fg)

    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, "PNG", optimize=True)
        print("Saved PNG:", p)


if __name__ == "__main__":
    # Make Clean Light "Corporate Hacker" D-Suite Card the primary default (signature-card.png)
    render_dsuite_signature_card(
        mode="corporate_light",
        out_paths=[
            os.path.join(OUT_DIR, "signature-card.png"),
            os.path.join(OUT_DIR, "signature-card-carbon.png"),
            os.path.join(OUT_DIR, "signature-card-argon.png"),
            os.path.join(OUT_DIR, "signature-card-argon-light.png"),
            os.path.join(ARTIFACT_DIR, "signature-card-dsuite-corporate-light.png"),
        ],
    )
    # Keep Dark HUD variant available as signature-card-carbon-dark.png & signature-card-argon-dark.png
    render_dsuite_signature_card(
        mode="dark",
        out_paths=[
            os.path.join(OUT_DIR, "signature-card-carbon-dark.png"),
            os.path.join(OUT_DIR, "signature-card-argon-dark.png"),
            os.path.join(ARTIFACT_DIR, "signature-card-dsuite-dark.png"),
        ],
    )
