import os
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

src_graded = r"c:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-graded"
assets_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars\assets"
brain_dir = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2"
cuts_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars\cuts"
os.makedirs(cuts_dir, exist_ok=True)

def find_file(d, prefix):
    for f in os.listdir(d):
        if f.startswith(prefix):
            return os.path.join(d, f)
    raise FileNotFoundError(f"{prefix} in {d}")

items = [
    # 4 Top Cabinets
    ("tcc-oct27-cab-01-metal-clad.jpg", find_file(src_graded, "Old World Cabinet metal 59.5 tall x 32.5 wide x 16.25 deep $2400")),
    ("tcc-oct27-cab-02-carved-strap.jpg", find_file(src_graded, "Old World Cabinet 61.5 tall x 34.5 wide x 15.25")),
    ("tcc-oct27-cab-03-blue-patina.jpg", find_file(assets_dir, "Old World Cabinet  ")),
    ("tcc-oct27-cab-04-red-patina.jpg", find_file(src_graded, "Old World Cabinet 88.5 tall x 50 wide x 29 deep")),
    # 7 Newly Stripped Products from assets/need-graded
    ("tcc-oct27-cut-01-polychrome-mirror.jpg", os.path.join(brain_dir, "cut_01_antique_polychrome_mirror_1793117636671.jpg")),
    ("tcc-oct27-cut-02-knight-templar-sword.jpg", os.path.join(brain_dir, "cut_02_knight_templar_sword_1793117637329.jpg")),
    ("tcc-oct27-cut-03-pink-sevres-chest.jpg", os.path.join(brain_dir, "cut_03_pink_sevres_chest_1793117657803.jpg")),
    ("tcc-oct27-cut-04-mother-of-pearl-chest.jpg", os.path.join(brain_dir, "cut_04_mother_of_pearl_chest_1793117683222.jpg")),
    ("tcc-oct27-cut-05-silk-qum-runner.jpg", os.path.join(brain_dir, "cut_05_silk_qum_runner_1793117647718.jpg")),
    ("tcc-oct27-cut-06-pair-gilt-gesso-shelves.jpg", os.path.join(brain_dir, "cut_06_pair_gilt_gesso_shelves_1793117678476.jpg")),
    ("tcc-oct27-cut-07-persian-tabriz-carpet.jpg", os.path.join(brain_dir, "cut_07_persian_tabriz_carpet_1793117668501.jpg")),
]

# Exact muted parchment hex: #F8F3EC -> RGB(248, 243, 236)
target_bg = np.array([248.0, 243.0, 236.0], dtype=np.float32)

for out_name, path in items:
    im = Image.open(path).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    h, w, _ = arr.shape
    
    # Build a smooth spatially varying background reference using top/bottom/left/right border strips
    top_med = np.median(arr[:20, :], axis=(0, 1))
    bot_med = np.median(arr[h-20:, :], axis=(0, 1))
    y_grad = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    local_bg = top_med[None, None, :] * (1.0 - y_grad) + bot_med[None, None, :] * y_grad
    
    dist = np.linalg.norm(arr - local_bg, axis=2)
    
    # Downsample by 4x for fast floodfill from outer borders
    small_im = im.resize((w // 4, h // 4), Image.Resampling.BILINEAR)
    s_arr = np.array(small_im, dtype=np.float32)
    sh, sw, _ = s_arr.shape
    s_y = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None, None]
    s_bg = top_med[None, None, :] * (1.0 - s_y) + bot_med[None, None, :] * s_y
    s_dist = np.linalg.norm(s_arr - s_bg, axis=2)
    
    cand = s_dist < 42.0
    visited = np.zeros((sh, sw), dtype=bool)
    q = deque()
    for x in range(sw):
        if cand[0, x]:
            visited[0, x] = True
            q.append((0, x))
        if cand[sh-1, x] and not visited[sh-1, x]:
            visited[sh-1, x] = True
            q.append((sh-1, x))
    for y in range(sh):
        if cand[y, 0] and not visited[y, 0]:
            visited[y, 0] = True
            q.append((y, 0))
        if cand[y, sw-1] and not visited[y, sw-1]:
            visited[y, sw-1] = True
            q.append((y, sw-1))
            
    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)):
            if 0 <= ny < sh and 0 <= nx < sw and not visited[ny, nx] and cand[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))
                
    mask_small = Image.fromarray((visited.astype(np.uint8) * 255))
    mask_full = mask_small.resize((w, h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=4.0))
    outer_bg_mask = np.array(mask_full, dtype=np.float32) / 255.0
    
    color_weight = np.clip((48.0 - dist) / (48.0 - 10.0), 0.0, 1.0)
    blend = (outer_bg_mask * color_weight)[..., None]
    
    # Multiplicative + direct lock so pure background becomes exact #F8F3EC and soft shadows scale naturally
    ratio = target_bg[None, None, :] / np.maximum(local_bg, 1.0)
    shifted_bg = arr * ratio
    pure_lock = (outer_bg_mask * np.clip((18.0 - dist) / 10.0, 0.0, 1.0))[..., None]
    shifted_bg = shifted_bg * (1.0 - pure_lock) + target_bg[None, None, :] * pure_lock
    
    out_arr = np.clip(arr * (1.0 - blend) + shifted_bg * blend, 0, 255).astype(np.uint8)
    out_im = Image.fromarray(out_arr)
    out_path = os.path.join(cuts_dir, out_name)
    out_im.save(out_path, quality=94)
    print(f"Saved {out_name}: top_med={top_med.round(1)} -> new_corner={out_arr[5, 5]}")
