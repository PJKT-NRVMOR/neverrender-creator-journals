import os
import numpy as np
from PIL import Image

src_dir = r"c:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-graded"
assets_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars\assets"
cuts_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars\cuts"
os.makedirs(cuts_dir, exist_ok=True)

def find_file(d, prefix, exclude=None):
    for f in os.listdir(d):
        if f.startswith(prefix):
            if exclude and exclude in f:
                continue
            return os.path.join(d, f)
    raise FileNotFoundError(prefix)

cabinets = [
    ("cut-cab-01-metal-clad-59-5.jpg", find_file(src_dir, "Old World Cabinet metal 59.5 tall x 32.5 wide x 16.25 deep $2400")),
    ("cut-cab-02-carved-strap-61-5.jpg", find_file(src_dir, "Old World Cabinet 61.5 tall x 34.5 wide x 15.25")),
    ("cut-cab-03-blue-patina-88-5.jpg", find_file(assets_dir, "Old World Cabinet  ")),
    ("cut-cab-04-red-patina-88-5.jpg", find_file(src_dir, "Old World Cabinet 88.5 tall x 50 wide x 29 deep $3450 to $2450 c")),
]

# Target muted parchment: #FAF6F0 -> RGB(250, 246, 240)
target_bg = np.array([250.0, 246.0, 240.0])

for out_name, path in cabinets:
    im = Image.open(path).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    bg_sample = arr[:40, :40].mean(axis=(0, 1))
    dist = np.linalg.norm(arr - bg_sample, axis=2)
    alpha = np.clip((48.0 - dist) / (48.0 - 14.0), 0.0, 1.0)[..., None]
    shift = target_bg - bg_sample
    out_arr = np.clip(arr + alpha * shift, 0, 255).astype(np.uint8)
    out_im = Image.fromarray(out_arr)
    out_path = os.path.join(cuts_dir, out_name)
    out_im.save(out_path, quality=94)
    print(f"Saved {out_name}: original bg {bg_sample.round(1)} -> new corner {out_arr[10,10]}")
