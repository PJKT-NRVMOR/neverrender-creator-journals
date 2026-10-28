import os
import numpy as np
from PIL import Image, ImageFilter
from collections import deque

src_graded = r"c:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-graded"
cuts_dirs = [
    r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars\cuts",
    r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-10-27-autumn-warmth-and-old-world-peculiars\cuts",
]
target_bg = np.array([248.0, 243.0, 236.0], dtype=np.float32)
target_bg_tuple = (248, 243, 236)

def clean_and_align_cabinet(src_path, canvas_size=(1000, 1500), target_cab_h=1360):
    im = Image.open(src_path).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    h, w, _ = arr.shape

    top_med = np.median(arr[:25, :], axis=(0, 1))
    bot_med = np.median(arr[h-25:, :], axis=(0, 1))
    y_grad = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    local_bg = top_med[None, None, :] * (1.0 - y_grad) + bot_med[None, None, :] * y_grad

    small_scale = 2
    sh, sw = h // small_scale, w // small_scale
    s_im = im.resize((sw, sh), Image.Resampling.BILINEAR)
    s_arr = np.array(s_im, dtype=np.float32)
    s_y = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None, None]
    s_bg = top_med[None, None, :] * (1.0 - s_y) + bot_med[None, None, :] * s_y
    s_dist = np.linalg.norm(s_arr - s_bg, axis=2)
    s_luma = s_arr.mean(axis=2)
    s_sat = s_arr.max(axis=2) - s_arr.min(axis=2)

    cand = ((s_dist < 88.0) & (s_luma > 140.0)) | ((s_sat < 36.0) & (s_luma > 130.0))
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

    fg_small = (~visited)
    # Find the cabinet's true left/right wall bounds in the mid-section (25%..65% height) where there is no floor shadow
    mid_fg = fg_small[int(sh*0.25):int(sh*0.65), :]
    _, mid_xs = np.where(mid_fg)
    left_wall_x = max(0, int(np.percentile(mid_xs, 0.5)) - 6)
    right_wall_x = min(sw, int(np.percentile(mid_xs, 99.5)) + 6)
    # Any floor shadow sticking out laterally beyond the cabinet's vertical walls in the lower 40% is background
    fg_small[int(sh*0.60):, :left_wall_x] = False
    fg_small[int(sh*0.60):, right_wall_x:] = False

    fg_mask_pil = Image.fromarray((fg_small.astype(np.uint8) * 255)).resize((w, h), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=1.5))
    fg_mask_arr = np.array(fg_mask_pil, dtype=np.float32) / 255.0

    cab_pixels = fg_mask_arr > 0.5
    ys, xs = np.where(cab_pixels)
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())

    halo_pil = fg_mask_pil.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(radius=8.0))
    halo = np.array(halo_pil, dtype=np.float32) / 255.0

    ratio = target_bg[None, None, :] / np.maximum(local_bg, 1.0)
    shifted = np.clip(arr * ratio, 0, 255)

    comp = arr * fg_mask_arr[..., None] + shifted * (1.0 - fg_mask_arr[..., None])
    halo_weight = np.clip(fg_mask_arr + (halo - fg_mask_arr) * 0.30, 0.0, 1.0)
    final_arr = comp * halo_weight[..., None] + target_bg[None, None, :] * (1.0 - halo_weight[..., None])
    final_im = Image.fromarray(np.clip(final_arr, 0, 255).astype(np.uint8))

    pad = 28
    cx0, cy0 = max(0, x0 - pad), max(0, y0 - pad)
    cx1, cy1 = min(w, x1 + pad), min(h, y1 + pad)
    cropped = final_im.crop((cx0, cy0, cx1, cy1))

    cw, ch = canvas_size
    max_w = int(cw * 0.90)
    max_h = target_cab_h
    cropped.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (cw, ch), target_bg_tuple)
    px = (cw - cropped.width) // 2
    py = (ch - cropped.height) // 2
    canvas.paste(cropped, (px, py))
    return canvas

cabinet_sources = [
    ("tcc-oct27-cab-01-metal-clad.jpg", os.path.join(src_graded, "Old World Cabinet metal 59.5 tall x 32.5 wide x 16.25 deep $2400 to $1990 cc.jpeg")),
    ("tcc-oct27-cab-02-carved-strap.jpg", os.path.join(src_graded, "Old World Cabinet 61.5 tall x 34.5 wide x e.jpeg")),
    ("tcc-oct27-cab-03-blue-patina.jpg", os.path.join(src_graded, "Old World Cabinet  .jpeg")),
    ("tcc-oct27-cab-04-red-patina.jpg", os.path.join(src_graded, "Old World Cabinet 88.5 tall x .jpeg")),
    ("tcc-oct27-cab-04-red-patina-angle.jpg", os.path.join(src_graded, "Old World Cabinet 88.5 tall sisex .jpeg")),
]

for out_name, src_path in cabinet_sources:
    canvas = clean_and_align_cabinet(src_path)
    for d in cuts_dirs:
        canvas.save(os.path.join(d, out_name), "JPEG", quality=94, optimize=True)
    print("Saved spotless v2:", out_name)
