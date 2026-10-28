import os
import numpy as np
from PIL import Image

ART_DIR = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2"
SCRATCH_DIR = os.path.join(ART_DIR, "scratch")

im1 = Image.open(os.path.join(ART_DIR, "img_01_white_1792536896013.jpg")).convert("RGB")
im2 = Image.open(os.path.join(ART_DIR, "img_02_white_1792536928222.jpg")).convert("RGB")

def analyze_rug(im, name):
    arr = np.array(im)
    mask = (arr[:, :, 0] < 240) | (arr[:, :, 1] < 240) | (arr[:, :, 2] < 240)
    ys, xs = np.where(mask)
    print(f"{name} size={im.size}: x=[{xs.min()}, {xs.max()}], y=[{ys.min()}, {ys.max()}]")
    # Check top row and bottom row on left half vs right half
    mid_x = (xs.min() + xs.max()) // 2
    ys_l, xs_l = np.where(mask[:, :mid_x])
    ys_r, xs_r = np.where(mask[:, mid_x:])
    print(f"  Left half y=[{ys_l.min()}, {ys_l.max()}], Right half y=[{ys_r.min()}, {ys_r.max()}]")

analyze_rug(im1, "Beige Rug (img_01)")
analyze_rug(im2, "Teal Rug (img_02)")
