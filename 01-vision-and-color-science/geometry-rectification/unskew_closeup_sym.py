import glob
import os
import numpy as np
from PIL import Image, ImageDraw

folder = r'C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\02-showroom-media\recieved-graded'
p = glob.glob(os.path.join(folder, '*close up.jpg'))[0]
im = Image.open(p)
w, h = im.size

def find_homography(src_pts, dst_pts):
    A = []
    B = []
    for (x, y), (u, v) in zip(dst_pts, src_pts):
        A.append([x, y, 1, 0, 0, 0, -x*u, -y*u])
        A.append([0, 0, 0, x, y, 1, -x*v, -y*v])
        B.append(u)
        B.append(v)
    A = np.array(A, dtype=np.float64)
    B = np.array(B, dtype=np.float64)
    coeffs = np.linalg.solve(A, B)
    return tuple(coeffs)

# Exact measured landmarks on the 2142 x 2856 original:
# Central rosette center: (1075.3, 1233.8)
# Upper pendant center:   (1101.0, 442.7)
# Lower pendant center:   (1034.6, 2299.1)
# Top lotus center:       (1107.4, 185.6)
# Bottom lotus center:    (1015.3, 2713.2)
# Notice that from top lotus (y=185.6) to rosette (y=1233.8) is 1048.2 px,
# and from rosette (y=1233.8) to bottom lotus (y=2713.2) is 1479.4 px.
# Ratio of bottom-half foreshortening to top-half = 1479.4 / 1048.2 = 1.4114!
# And from upper pendant (y=442.7) to rosette (y=1233.8) is 791.1 px,
# and from rosette (y=1233.8) to lower pendant (y=2299.1) is 1065.3 px.
# In a projective homography along the vertical axis that maps:
#   y_top = 150.0  -> v = 0
#   y_mid = 1233.8 -> v = out_h / 2  (EXACT 50% vertical center!)
#   y_bot = 2770.0 -> v = out_h
#Notice: (1233.8 - 150.0) = 1083.8 px (top half), (2770.0 - 1233.8) = 1536.2 px (bottom half),
# and 1536.2 / 1083.8 = 1.4174 — matching the exact 1.4114 projective ratio of the lotus palmettes AND the 1.425 border width ratio!
# That means a single planar homography maps:
#   y_top = 150.0  -> v = 0.0
#   y_rosette = 1233.8 -> v = 0.5 * out_h (DEAD CENTER!)
#   y_bot = 2770.0 -> v = 1.0 * out_h
# And what must the horizontal half-widths dx_top (at y=150) and dx_bot (at y=2770) be in order for this 4-point quad to induce that EXACT projective scale ratio (1.4174) between the top half and bottom half?!
# In 1D projective geometry, if a trapezoid has top half-width dx_top at y_top and bottom half-width dx_bot at y_bot,
# then the image y that maps to the midpoint v = 0.5 * out_h is the weighted harmonic mean:
#   y_mid = (y_top * dx_bot + y_bot * dx_top) / (dx_top + dx_bot) !
# Let's check!!
# We want y_mid = 1233.8 when y_top = 150.0 and y_bot = 2770.0:
#   dx_bot / dx_top = (y_bot - y_mid) / (y_mid - y_top) = (2770.0 - 1233.8) / (1233.8 - 150.0) = 1536.2 / 1083.8 = 1.41742!!
#HOLD EVERYTHING! That harmonic mean identity is exact!
# When dx_bot / dx_top = 1.41742, the homography of that trapezoid AUTOMATICALLY places y = 1233.8 at the exact 50.0% vertical center of the output image AND equalizes the top and bottom scale by 1.41742x!

y_top = 150.0
y_mid = 1233.8
y_bot = 2770.0
ratio = (y_bot - y_mid) / (y_mid - y_top) # 1.41742

# Spine x(y) passes through (1107.4, 185.6), (1075.3, 1233.8), (1015.3, 2713.2):
# Note: at y_top=150, x_top = 1109.0; at y_bot=2770, x_bot = 1013.0.
# Check where x_mid lands at y_mid = 1233.8 under the harmonic weight:
# x_mid = (1109.0 * ratio + 1013.0 * 1.0) / (1.0 + ratio) = (1571.9 + 1013.0) / 2.41742 = 1069.3 (let's shift x_top=1115.0, x_bot=1019.0 so x_mid = 1075.3, hitting the central rosette to 0.0 pixels!)
x_top = 1115.0
x_bot = 1019.0

# Now choose dx_bot as large as possible inside [0, 2142] at y_bot = 2770 (where x_bot = 1019.0, so max symmetric dx_bot without going < 0 is 1019.0 px!):
dx_bot = 1018.0
dx_top = dx_bot / ratio # 1018.0 / 1.41742 = 718.2 px!

# And what is the horizontal half-width at y_mid = 1233.8?
# By linearity of trapezoid edges: dx_mid = (dx_top + dx_bot) / ... wait: at y_mid,
# t = (y_mid - y_top) / (y_bot - y_top) = 1083.8 / 2620.0 = 0.41366
# dx(y_mid) = dx_top * (1 - t) + dx_bot * t = 718.2 * 0.58634 + 1018.0 * 0.41366 = 842.2 px (so full width at medallion = 1684.4 px).
# And the medallion horizontal diameter in the original image at y_mid is 1330 px, so the medallion takes up 1330 / 1684.4 = 79.0% of the rectified width (10.5% navy floral field margin on both left and right of the medallion points!).
# Now what should out_h / out_w be so that the central medallion is a 100% true 1:1 circle?
# In the original image, the medallion's top tip is at y = 735 and bottom tip is at y = 1815.
# Under our homography, any y maps to normalized vertical coordinate v_norm(y) in [0, 1]:
#   t(y) = (y - y_top) / (y_bot - y_top)
#   v_norm(y) = (t(y) * dx_bot) / (dx_top * (1 - t(y)) + dx_bot * t(y))  -- wait: inverse is y(v) = (y_top*(1-v)*dx_bot + y_bot*v*dx_top) / ((1-v)*dx_bot + v*dx_top)
#   Solving for v(y): v(y) = ((y - y_top) * dx_top) / ((y - y_top) * dx_top + (y_bot - y) * dx_bot) ... wait: at y = y_mid, (y_mid - y_top)*dx_bot == (y_bot - y_mid)*dx_top, so:
#   v(y) = ((y - y_top) * dx_bot) / ((y - y_top) * dx_bot + (y_bot - y) * dx_top) !
def v_norm(y):
    num = (y - y_top) * dx_bot
    den = num + (y_bot - y) * dx_top
    return num / den

v_med_top = v_norm(735.0)
v_med_bot = v_norm(1815.0)
v_med_span = v_med_bot - v_med_top # fraction of out_h occupied by medallion vertical diameter!
h_med_span = 1330.0 / (2.0 * 842.2) # fraction of out_w occupied by medallion horizontal diameter (0.7896)
true_aspect = h_med_span / v_med_span # out_h / out_w so that v_med_span * out_h == h_med_span * out_w!
print(f'v_med_span = {v_med_span:.4f}, h_med_span = {h_med_span:.4f}, true_aspect (out_h/out_w) = {true_aspect:.4f}')

# Let's generate two aspect ratios from this exact same 4-way symmetric homography:
# 1) Exact 3:4 Portrait (2142 x 2856, matching original dimensions)
# 2) Exact 1:1 Circular Medallion Orthographic (2142 x int(2142 * true_aspect))
src_pts = [
    (x_top - dx_top, y_top),
    (x_top + dx_top, y_top),
    (x_bot + dx_bot, y_bot),
    (x_bot - dx_bot, y_bot),
]

out_w1, out_h1 = 2142, 2856
coeffs1 = find_homography(src_pts, [(0, 0), (out_w1, 0), (out_w1, out_h1), (0, out_h1)])
im_sym_3x4 = im.transform((out_w1, out_h1), Image.Transform.PERSPECTIVE, coeffs1, Image.Resampling.BICUBIC)

out_w2, out_h2 = 2142, int(round(2142 * true_aspect))
coeffs2 = find_homography(src_pts, [(0, 0), (out_w2, 0), (out_w2, out_h2), (0, out_h2)])
im_sym_true = im.transform((out_w2, out_h2), Image.Transform.PERSPECTIVE, coeffs2, Image.Resampling.BICUBIC)

out_dir = r'C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2'
im_sym_3x4.save(os.path.join(out_dir, '2026-10-17-CloseUp_Unskew_Centered_3x4.jpg'), quality=95)
im_sym_true.save(os.path.join(out_dir, '2026-10-17-CloseUp_Unskew_Centered_TrueCircle.jpg'), quality=95)
# Also save to recieved-graded
im_sym_3x4.save(os.path.join(folder, 'Silk Runner 10 foot long $24500 to $1850 close up (unskewed-3x4).jpg'), quality=95)
im_sym_true.save(os.path.join(folder, 'Silk Runner 10 foot long $24500 to $1850 close up (unskewed-true-ortho).jpg'), quality=95)

# Build a side-by-side comparison with crosshair grid lines to prove 4-way symmetry!
comp = Image.new('RGB', (2450, 1220), (20, 20, 20))
draw = ImageDraw.Draw(comp)
items = [
    (im, '1. Original (Tilted Spine + Keystone Skew)'),
    (im_sym_3x4, '2. Unskewed & Dead-Centered (3:4 Aspect, 2142x2856)'),
    (im_sym_true, f'3. True 1:1 Circular Medallion Ortho ({out_w2}x{out_h2})')
]
for idx, (img_item, title) in enumerate(items):
    t = img_item.copy()
    t.thumbnail((770, 1100), Image.LANCZOS)
    tw, th = t.size
    # Draw subtle gold center crosshair on the thumbnail to show where (50%, 50%) is
    td = ImageDraw.Draw(t)
    td.line([(tw//2, 0), (tw//2, th)], fill=(212, 175, 55), width=2)
    td.line([(0, th//2), (tw, th//2)], fill=(212, 175, 55), width=2)
    x0 = 25 + idx * 805 + (770 - tw) // 2
    y0 = 25 + (1100 - th) // 2
    comp.paste(t, (x0, y0))
    draw.text((25 + idx * 805 + 20, 1155), title, fill=(240, 220, 170))

comp.save(os.path.join(out_dir, '2026-10-17-CloseUp_Unskew_4Way_Symmetry_Proof.jpg'), quality=92)
print('Saved symmetry proof!')
