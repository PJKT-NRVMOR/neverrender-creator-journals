import os
import numpy as np
from PIL import Image

cuts_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars\cuts"
target_bg = np.array([248, 243, 236], dtype=np.uint8)

def tight_crop_on_parchment(in_name, out_name, pad_ratio=0.015, thresh=18.0):
    p = os.path.join(cuts_dir, in_name)
    im = Image.open(p).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    dist = np.linalg.norm(arr - target_bg.astype(np.float32), axis=2)
    ys, xs = np.where(dist > thresh)
    y0, y1 = max(0, ys.min()), min(arr.shape[0], ys.max() + 1)
    x0, x1 = max(0, xs.min()), min(arr.shape[1], xs.max() + 1)
    crop = im.crop((x0, y0, x1, y1))
    cw, ch = crop.size
    pad_x = int(cw * pad_ratio)
    pad_y = int(ch * pad_ratio)
    new_w = cw + 2 * pad_x
    new_h = ch + 2 * pad_y
    canvas = Image.new("RGB", (new_w, new_h), tuple(int(x) for x in target_bg))
    canvas.paste(crop, (pad_x, pad_y))
    out_p = os.path.join(cuts_dir, out_name)
    canvas.save(out_p, quality=94)
    print(f"Saved {out_name}: old={im.size} -> new={canvas.size}")

tight_crop_on_parchment("tcc-oct27-cut-01-polychrome-mirror.jpg", "tcc-oct27-cut-01-polychrome-mirror-v2.jpg", pad_ratio=0.012, thresh=22.0)
tight_crop_on_parchment("tcc-oct27-cut-05-silk-qum-runner.jpg", "tcc-oct27-cut-05-silk-qum-runner-v2.jpg", pad_ratio=0.015, thresh=20.0)
tight_crop_on_parchment("tcc-oct27-cut-02-knight-templar-sword.jpg", "tcc-oct27-cut-02-knight-templar-sword-v2.jpg", pad_ratio=0.02, thresh=20.0)
