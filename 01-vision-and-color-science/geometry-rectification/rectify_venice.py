import os
import io
import glob
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
from PIL import Image, ImageFilter

BASE_URL = "https://thechapmancollection.com"
AUTH = HTTPBasicAuth("neverrender-labs", os.getenv("WP_REST_APP_PASSWORD", ""))
BRAIN_DIR = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2"

# Find high-res source or use current_venice.jpg
matches = glob.glob(os.path.join(BRAIN_DIR, "*italian_royal_canal*")) + glob.glob(os.path.join(BRAIN_DIR, "scratch", "*italian_royal_canal*"))
print("Found high-res candidates:", matches)
src_path = matches[0] if matches else os.path.join(BRAIN_DIR, "scratch", "current_venice.jpg")

im = Image.open(src_path).convert("RGB")
arr = np.array(im)
h, w, _ = arr.shape
print("Loaded size:", (w, h))

# Detect exact frame mask (exclude soft grey drop shadow which has R~G~B > 180, frame is warm dark brown/gold where B < 160)
frame_mask = (arr[:, :, 2] < 165) & (np.mean(arr, axis=2) < 195)

# Measure top, bottom, left, right edges via linear fit over central 70% of each side
xs = np.arange(int(w * 0.15), int(w * 0.85))
top_pts = []
bot_pts = []
for x in xs:
    ys = np.where(frame_mask[:, x])[0]
    if len(ys) > 10:
        top_pts.append((x, ys[0]))
        bot_pts.append((x, ys[-1]))

ys_range = np.arange(int(h * 0.15), int(h * 0.85))
left_pts = []
right_pts = []
for y in ys_range:
    xs_row = np.where(frame_mask[y, :])[0]
    if len(xs_row) > 10:
        left_pts.append((xs_row[0], y))
        right_pts.append((xs_row[-1], y))

m_top, b_top = np.polyfit([p[0] for p in top_pts], [p[1] for p in top_pts], 1)
m_bot, b_bot = np.polyfit([p[0] for p in bot_pts], [p[1] for p in bot_pts], 1)
# For left and right: x = m*y + b
m_left, b_left = np.polyfit([p[1] for p in left_pts], [p[0] for p in left_pts], 1)
m_right, b_right = np.polyfit([p[1] for p in right_pts], [p[0] for p in right_pts], 1)

print(f"Top slope: {np.degrees(np.arctan(m_top)):.3f} deg")
print(f"Bot slope: {np.degrees(np.arctan(m_bot)):.3f} deg")
print(f"Left slope: {np.degrees(np.arctan(m_left)):.3f} deg")
print(f"Right slope: {np.degrees(np.arctan(m_right)):.3f} deg")

def intersect(m_horiz, b_horiz, m_vert, b_vert):
    # y = m_horiz * x + b_horiz
    # x = m_vert * y + b_vert  => x = m_vert * (m_horiz * x + b_horiz) + b_vert
    x = (m_vert * b_horiz + b_vert) / (1.0 - m_vert * m_horiz)
    y = m_horiz * x + b_horiz
    return (x, y)

tl = intersect(m_top, b_top, m_left, b_left)
tr = intersect(m_top, b_top, m_right, b_right)
br = intersect(m_bot, b_bot, m_right, b_right)
bl = intersect(m_bot, b_bot, m_left, b_left)
print("Detected 4 corners (TL, TR, BR, BL):", tl, tr, br, bl)

# Target perfectly level rectangle dimensions
rect_w = int(round((tr[0] - tl[0] + br[0] - bl[0]) / 2.0))
rect_h = int(round((bl[1] - tl[1] + br[1] - tr[1]) / 2.0))

# Extract the exact quad into a dead-straight rectangle using PIL.Image.Transform.QUAD
# QUAD takes (x0, y0, x1, y1, x2, y2, x3, y3) in order: NW, SW, SE, NE
quad_coords = (
    tl[0], tl[1],
    bl[0], bl[1],
    br[0], br[1],
    tr[0], tr[1],
)
rectified_painting = im.transform((rect_w, rect_h), Image.Transform.QUAD, quad_coords, resample=Image.Resampling.BICUBIC)

# Place on clean pure white canvas (#FFFFFF) with a subtle, balanced gallery frame shadow
pad = int(round(rect_w * 0.032))
out_w = rect_w + 2 * pad
out_h = rect_h + 2 * pad

canvas = Image.new("RGBA", (out_w, out_h), (255, 255, 255, 255))
shadow = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
shadow_box = Image.new("RGBA", (rect_w, rect_h), (0, 0, 0, 55))
shadow.paste(shadow_box, (pad + int(pad * 0.2), pad + int(pad * 0.25)))
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=pad * 0.38))

canvas = Image.alpha_composite(canvas, shadow)
canvas.paste(rectified_painting.convert("RGBA"), (pad, pad))
final_im = canvas.convert("RGB")

# Resize to crisp 800px width for newsletter
nl_im = final_im.resize((800, int(round(800 * out_h / out_w))), Image.Resampling.LANCZOS)
out_path = os.path.join(BRAIN_DIR, "scratch", "rectified_venice_straight.jpg")
nl_im.save(out_path, format="JPEG", quality=94, optimize=True)
print("Saved rectified Venice image to:", out_path, nl_im.size)

# Upload to WordPress
buf = io.BytesIO()
nl_im.save(buf, format="JPEG", quality=94, optimize=True)
buf.seek(0)
headers = {
    "Content-Disposition": 'attachment; filename="tcc-oct23-art-1-italian-royal-canal-straight.jpg"',
    "Content-Type": "image/jpeg",
}
r_up = requests.post(f"{BASE_URL}/wp-json/wp/v2/media", auth=AUTH, headers=headers, data=buf.read(), timeout=60)
r_up.raise_for_status()
new_url = r_up.json()["source_url"]
print("Uploaded new straight Venice URL:", new_url)

# Update all newsletter HTML files to use new_url
nl_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval"
nl_files = [
    "2026-10-23-Omnisend_Saved_Template_Full_Import.html",
    "2026-10-23-Omnisend_Custom_HTML_Block_Table_Only.html",
    "a_little_overdue_new_arrivals_from_the_chapman_collection.html",
    "a_little_overdue_and_so_much_new_to_share.html",
    "2026-10-20-Thursday_Newsletter_Draft_2_White_Background_Linked.html",
]
old_url = "https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-art-1-italian-royal-canal.jpg"
for fn in nl_files:
    fp = os.path.join(nl_dir, fn)
    if not os.path.exists(fp):
        continue
    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace(old_url, new_url)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated Venice image URL in:", fn)
