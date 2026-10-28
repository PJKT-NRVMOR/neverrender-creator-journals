import os
import numpy as np
from PIL import Image

ART_DIR = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2"

def find_persp_coeffs(pa, pb):
    # pa: 4 destination points, pb: 4 source points
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

# 1. Straighten img_05 (Venetian oil painting)
im5 = Image.open(os.path.join(ART_DIR, "img_05_white_png_1792536935707.jpg")).convert("RGB")
# Source corners: TL=(64, 47), TR=(999, 44), BR=(1005, 978), BL=(80, 985)
w5, h5 = 940, 940
pad5 = 16
dst5 = [(pad5, pad5), (w5 - pad5, pad5), (w5 - pad5, h5 - pad5), (pad5, h5 - pad5)]
src5 = [(64, 47), (999, 44), (1005, 978), (80, 985)]
coeffs5 = find_persp_coeffs(dst5, src5)
im5_straight = im5.transform((w5, h5), Image.Transform.PERSPECTIVE, coeffs5, Image.Resampling.BICUBIC, fillcolor=(255, 255, 255))
out5 = os.path.join(ART_DIR, "scratch", "img_05_straight.jpg")
im5_straight.save(out5, quality=95)

# 2. Straighten img_06 (Matisse silver frame)
im6 = Image.open(os.path.join(ART_DIR, "img_06_white_png_1792536957006.jpg")).convert("RGB")
# Source corners: TL=(87, 176), TR=(813, 176), BR=(825, 1042), BL=(82, 1034)
w6, h6 = 760, 890
pad6 = 14
dst6 = [(pad6, pad6), (w6 - pad6, pad6), (w6 - pad6, h6 - pad6), (pad6, h6 - pad6)]
src6 = [(87, 176), (813, 176), (825, 1042), (82, 1034)]
coeffs6 = find_persp_coeffs(dst6, src6)
im6_straight = im6.transform((w6, h6), Image.Transform.PERSPECTIVE, coeffs6, Image.Resampling.BICUBIC, fillcolor=(255, 255, 255))
out6 = os.path.join(ART_DIR, "scratch", "img_06_straight.jpg")
im6_straight.save(out6, quality=95)
print("Saved straightened img_05 and img_06")
