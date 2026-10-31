import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from collections import deque

src_graded = r"c:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-graded"
cuts_dirs = [
    r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\approved-active-drops\2026-10-30-autumn-warmth-old-world-peculiars\cuts",
    r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-10-27-autumn-warmth-and-old-world-peculiars\cuts",
]
target_bg = np.array([248.0, 243.0, 236.0], dtype=np.float32)
target_bg_tuple = (248, 243, 236)

def isolate_unrectified_metal_clad_cabinet(raw_gray_path):
    """Isolate unrectified tcc-oct27-cab-04-metal-clad.jpg onto #F8F3EC parchment without changing perspective."""
    im = Image.open(raw_gray_path).convert("RGB")
    w, h = im.size
    arr = np.array(im, dtype=np.float32)

    poly = [
        (71, 61),       # top-left crown corner
        (648, 128),     # top-right crown corner
        (645, 151),     # right crown bottom lip
        (603, 155),     # right body top under crown molding
        (587, 300),     # right body upper-mid
        (562, 500),     # right body mid
        (543, 700),     # right body lower-mid
        (525, 874),     # right base bottom corner
        (523, 916),     # right foot outer bottom
        (490, 918),     # right foot inner bottom
        (489, 882),     # under-skirt right
        (165, 922),     # under-skirt left
        (165, 956),     # left foot inner bottom
        (119, 958),     # left foot outer bottom
        (119, 920),     # left base bottom corner
        (79, 95),       # left body top under crown
        (71, 90),       # left crown bottom lip
    ]

    scale = 4
    mask_hi = Image.new("L", (w * scale, h * scale), 0)
    draw_hi = ImageDraw.Draw(mask_hi)
    draw_hi.polygon([(x * scale, y * scale) for x, y in poly], fill=255)
    mask_pil = mask_hi.resize((w, h), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=0.8))
    alpha = np.array(mask_pil, dtype=np.float32) / 255.0

    yy, xx = np.mgrid[0:h, 0:w]
    shadow_l = np.exp(-(((xx - 142.0) / 36.0) ** 2 + ((yy - 958.0) / 9.0) ** 2)) * 0.16
    shadow_r = np.exp(-(((xx - 506.0) / 32.0) ** 2 + ((yy - 918.0) / 8.0) ** 2)) * 0.14
    line_y = 955.0 + (xx - 142.0) * (916.0 - 955.0) / (506.0 - 142.0)
    in_span = (xx >= 115) & (xx <= 530)
    shadow_bar = np.where(in_span, np.exp(-(((yy - (line_y - 12.0)) / 14.0) ** 2)) * 0.08, 0.0)
    total_shadow = np.clip(shadow_l + shadow_r + shadow_bar, 0.0, 0.20)
    shadowed_bg = target_bg[None, None, :] * (1.0 - total_shadow[..., None])

    comp = arr * alpha[..., None] + shadowed_bg * (1.0 - alpha[..., None])
    return Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8))

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
    mid_fg = fg_small[int(sh*0.25):int(sh*0.65), :]
    _, mid_xs = np.where(mid_fg)
    left_wall_x = max(0, int(np.percentile(mid_xs, 0.5)) - 6)
    right_wall_x = min(sw, int(np.percentile(mid_xs, 99.5)) + 6)
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

if __name__ == "__main__":
    raw_gray_cab04 = os.path.join(cuts_dirs[1], "tcc-oct27-cab-04-metal-clad-raw-gray.jpg")
    if os.path.exists(raw_gray_cab04):
        out_cab04 = isolate_unrectified_metal_clad_cabinet(raw_gray_cab04)
        for d in cuts_dirs:
            out_cab04.save(os.path.join(d, "tcc-oct27-cab-04-metal-clad.jpg"), "JPEG", quality=95, optimize=True)
        print("Saved parchment-isolated unrectified tcc-oct27-cab-04-metal-clad.jpg")
