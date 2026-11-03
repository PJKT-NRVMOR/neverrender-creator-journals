"""
Reusable Multi-Variant Signature Contact Sheet Chopper & Pure-White (#FFFFFF) Normalizer
NeverRender Labs Open-Source Studio Toolkit (04-print-and-vector-foundry/business-cards/)
Zero hardcoded secrets or client PII.
"""
import argparse
import os
import numpy as np
from PIL import Image


def tight_crop_and_clean(crop_im, pad_x=28, pad_y=22):
    arr = np.array(crop_im, dtype=np.int16)
    bg_rgb = np.median(
        np.concatenate([arr[0:5, :, :].reshape(-1, 3), arr[-5:, :, :].reshape(-1, 3)], axis=0),
        axis=0,
    )
    diff = np.max(np.abs(arr - bg_rgb), axis=2)
    fg_mask = diff > 18
    ys, xs = np.where(fg_mask)
    if len(ys) > 0:
        y0 = max(0, int(ys.min()) - pad_y)
        y1 = min(crop_im.height, int(ys.max()) + pad_y)
        x0 = max(0, int(xs.min()) - pad_x)
        x1 = min(crop_im.width, int(xs.max()) + pad_x)
        crop_im = crop_im.crop((x0, y0, x1, y1))
        arr = np.array(crop_im, dtype=np.float32)

    bg_level = float(np.percentile(arr, 92))
    white_arr = np.clip((arr / max(bg_level, 220.0)) * 255.0, 0, 255).astype(np.uint8)
    near_w = (white_arr[:, :, 0] > 244) & (white_arr[:, :, 1] > 244) & (white_arr[:, :, 2] > 244)
    white_arr[near_w] = [255, 255, 255]
    white_im = Image.fromarray(white_arr)
    return crop_im, white_im


def chop_three_up_sheet(src_path: str, out_dir: str, prefix: str = "sig"):
    os.makedirs(out_dir, exist_ok=True)
    im = Image.open(src_path).convert("RGB")
    W, H = im.size
    regions = {
        "Variant_A": (int(W * 0.010), int(H * 0.045), int(W * 0.660), int(H * 0.422)),
        "Variant_B": (int(W * 0.010), int(H * 0.588), int(W * 0.505), int(H * 0.965)),
        "Variant_C": (int(W * 0.505), int(H * 0.588), int(W * 0.992), int(H * 0.965)),
    }
    for name, box in regions.items():
        cropped_orig, cropped_white = tight_crop_and_clean(im.crop(box))
        cropped_orig.save(os.path.join(out_dir, f"{prefix}-{name}-original.png"), optimize=True)
        cropped_white.save(os.path.join(out_dir, f"{prefix}-{name}-pure-white.png"), optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chop 3-up signature sheet into individual PNGs.")
    parser.add_argument("--src", required=True, help="Path to 3-up image")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--prefix", default="sig", help="Filename prefix")
    args = parser.parse_args()
    chop_three_up_sheet(args.src, args.out_dir, args.prefix)
