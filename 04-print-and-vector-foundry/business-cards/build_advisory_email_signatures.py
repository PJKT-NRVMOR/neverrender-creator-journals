"""
Reusable Executive & Advisory HTML + 4x Supersampled PNG Email Signature Compiler
NeverRender Labs Open-Source Studio Toolkit (04-print-and-vector-foundry/business-cards/)
Zero hardcoded secrets or client PII. Reads configuration via environment variables or CLI args.
"""
import argparse
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def draw_tracked_text(draw, x, y, text, font, fill, tracking_px=0.0):
    cur_x = float(x)
    for ch in text:
        draw.text((cur_x, y), ch, font=font, fill=fill)
        adv = draw.textlength(ch, font=font)
        cur_x += adv + tracking_px
    return cur_x


def build_advisory_signature_from_reference(
    ref_sig_path: str,
    out_dir: str,
    out_prefix: str,
    org_line: str,
    advisory_line: str,
    services_line: str,
):
    os.makedirs(out_dir, exist_ok=True)
    ref_im = Image.open(ref_sig_path).convert("RGB")
    rw, rh = ref_im.size

    font_sans_bold = ImageFont.truetype(os.getenv("NRL_FONT_SANS_BOLD", r"C:\Windows\Fonts\GOTHICB.TTF"), 42)
    font_sans_sub = ImageFont.truetype(os.getenv("NRL_FONT_SANS_SUB", r"C:\Windows\Fonts\GOTHICB.TTF"), 38)
    font_serif_ital = ImageFont.truetype(os.getenv("NRL_FONT_SERIF_ITAL", r"C:\Windows\Fonts\GARAIT.TTF"), 54)

    # 1. 4-Line Compact Side-by-Side
    canvas_v1 = ref_im.copy()
    arr_v1 = np.array(canvas_v1)
    arr_v1[98:, 185:, :] = 255
    canvas_v1 = Image.fromarray(arr_v1)

    ss_v1 = canvas_v1.resize((rw * 2, rh * 2), Image.Resampling.LANCZOS)
    draw_v1 = ImageDraw.Draw(ss_v1)
    x_start = 198 * 2
    y_row3 = 105 * 2
    cx = draw_tracked_text(draw_v1, x_start, y_row3, org_line.upper(), font_sans_bold, (140, 107, 50), tracking_px=4.2)
    cx = draw_tracked_text(draw_v1, cx + 22, y_row3, "•", font_sans_bold, (197, 160, 89), tracking_px=0)
    draw_tracked_text(draw_v1, cx + 22, y_row3, advisory_line.upper(), font_sans_bold, (61, 53, 46), tracking_px=4.2)
    draw_tracked_text(draw_v1, x_start, 143 * 2, services_line, font_serif_ital, (110, 93, 79), tracking_px=0.6)

    out_v1_2x = ss_v1.resize((rw, rh), Image.Resampling.LANCZOS)
    arr_out1 = np.array(out_v1_2x)
    non_w1 = np.where((arr_out1[:, :, 0] < 252) | (arr_out1[:, :, 1] < 252) | (arr_out1[:, :, 2] < 252))
    x_max1 = min(rw, int(non_w1[1].max()) + 28)
    out_v1_2x = out_v1_2x.crop((0, 0, x_max1, rh))
    out_v1_1x = out_v1_2x.resize((out_v1_2x.width // 2, out_v1_2x.height // 2), Image.Resampling.LANCZOS)

    out_v1_2x.save(os.path.join(out_dir, f"{out_prefix}-4line.png"), optimize=True)
    out_v1_1x.save(os.path.join(out_dir, f"{out_prefix}-4line-email-size.png"), optimize=True)

    # 2. 5-Line Stacked Side-by-Side
    h_v2 = 228
    canvas_v2 = Image.new("RGB", (rw, h_v2), (255, 255, 255))
    canvas_v2.paste(ref_im.crop((0, 10, 160, 190)), (0, 24))
    arr_v2 = np.array(canvas_v2)
    arr_v2[16:212, 168:170, :] = [216, 199, 168]
    canvas_v2 = Image.fromarray(arr_v2)
    canvas_v2.paste(ref_im.crop((185, 20, rw, 98)), (185, 16))

    ss_v2 = canvas_v2.resize((rw * 2, h_v2 * 2), Image.Resampling.LANCZOS)
    draw_v2 = ImageDraw.Draw(ss_v2)
    draw_tracked_text(draw_v2, x_start, 100 * 2, org_line.upper(), font_sans_bold, (140, 107, 50), tracking_px=4.2)
    draw_tracked_text(draw_v2, x_start, 135 * 2, advisory_line.upper(), font_sans_sub, (61, 53, 46), tracking_px=4.5)
    draw_tracked_text(draw_v2, x_start, 169 * 2, services_line, font_serif_ital, (110, 93, 79), tracking_px=0.6)

    out_v2_2x = ss_v2.resize((rw, h_v2), Image.Resampling.LANCZOS)
    arr_out2 = np.array(out_v2_2x)
    non_w2 = np.where((arr_out2[:, :, 0] < 252) | (arr_out2[:, :, 1] < 252) | (arr_out2[:, :, 2] < 252))
    x_max2 = min(rw, int(non_w2[1].max()) + 28)
    out_v2_2x = out_v2_2x.crop((0, 0, x_max2, h_v2))
    out_v2_1x = out_v2_2x.resize((out_v2_2x.width // 2, out_v2_2x.height // 2), Image.Resampling.LANCZOS)

    out_v2_2x.save(os.path.join(out_dir, f"{out_prefix}-5line-stacked.png"), optimize=True)
    out_v2_1x.save(os.path.join(out_dir, f"{out_prefix}-5line-stacked-email-size.png"), optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build 4-line and 5-line advisory email signatures.")
    parser.add_argument("--ref-sig", required=True, help="Path to reference 2x signature PNG")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--prefix", default="advisory-signature", help="Output filename prefix")
    parser.add_argument("--org", required=True, help="Organization name line")
    parser.add_argument("--advisory", required=True, help="Advisory subtitle line")
    parser.add_argument("--services", required=True, help="Services italic line")
    args = parser.parse_args()
    build_advisory_signature_from_reference(
        args.ref_sig, args.out_dir, args.prefix, args.org, args.advisory, args.services
    )
