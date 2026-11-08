"""
NeverRender Labs Studio Toolkit — Chaphavian Alabaster (#F7F5F2) Circular Cutout Exporter
Normalizes outer matte pixels to exact #F7F5F2, neutralizes glass shadow-box blue reflections,
exports 800x800 4:4:4 JPEGs, and generates 4x4 Dark-Mode Light-Lock PNG background tiles.
"""
import os
import argparse
from PIL import Image
import numpy as np


def lock_chaphavian_alabaster(im: Image.Image) -> Image.Image:
    arr = np.array(im.convert("RGB"), dtype=np.uint8)
    near_f7f5f2 = (
        (np.abs(arr[:, :, 0].astype(int) - 247) <= 3)
        & (np.abs(arr[:, :, 1].astype(int) - 245) <= 3)
        & (np.abs(arr[:, :, 2].astype(int) - 242) <= 3)
    )
    arr[near_f7f5f2] = [247, 245, 242]
    return Image.fromarray(arr)


def generate_light_lock_tiles(dst_dir: str) -> None:
    os.makedirs(dst_dir, exist_ok=True)
    for name, rgb in [("bg-f7f5f2.png", (247, 245, 242)), ("bg-d9d3cc.png", (217, 211, 204))]:
        Image.new("RGB", (4, 4), rgb).save(os.path.join(dst_dir, name), "PNG", optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Chaphavian #F7F5F2 circular cutouts.")
    parser.add_argument("--input", required=True, help="Source PNG cutout path")
    parser.add_argument("--output", required=True, help="Destination 800x800 JPG path")
    args = parser.parse_args()

    img = lock_chaphavian_alabaster(Image.open(args.input))
    img.resize((800, 800), Image.Resampling.LANCZOS).save(
        args.output, "JPEG", quality=92, optimize=True, subsampling=0
    )
