import os
import glob
import shutil
from PIL import Image

NEED_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-need-graded"
GRADED_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\recieved-graded"
BACKUP_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\graded-backups"
BRAIN_DIR = r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2"

os.makedirs(BACKUP_DIR, exist_ok=True)

matches = glob.glob(os.path.join(NEED_DIR, "*Matisse Blue Nude III*"))
src_path = matches[0]
print("High-res source:", repr(src_path))

# Copy original high-res patio photo to graded-backups first
backup_orig = os.path.join(BACKUP_DIR, os.path.basename(src_path))
if not os.path.exists(backup_orig):
    shutil.copy2(src_path, backup_orig)
    print("Backed up original to:", backup_orig)

# Move any extra backup files out of recieved-need-graded and recieved-graded into graded-backups
for folder in [NEED_DIR, GRADED_DIR]:
    for extra in glob.glob(os.path.join(folder, "henri-matisse-blue-nude-iii-1958-color-plate-*")):
        dst = os.path.join(BACKUP_DIR, os.path.basename(extra))
        shutil.move(extra, dst)
        print("Moved backup to graded-backups:", dst)

im = Image.open(src_path).convert("RGB")
w, h = im.size
scale = w / 810.0  # 1440 / 810 = 1.7777777777777777
print(f"Loaded {w}x{h} (scale={scale:.4f}x)")

tl = (81.0 * scale, 153.0 * scale)
tr = (737.5 * scale, 158.5 * scale)
br = (739.0 * scale, 932.0 * scale)
bl = (73.0 * scale, 934.5 * scale)

rect_w = int(round((tr[0] - tl[0] + br[0] - bl[0]) / 2.0))
rect_h = int(round((bl[1] - tl[1] + br[1] - tr[1]) / 2.0))
print("High-res rectified frame size:", (rect_w, rect_h))

quad_outer = (
    tl[0], tl[1],
    bl[0], bl[1],
    br[0], br[1],
    tr[0], tr[1],
)
frame_rect = im.transform((rect_w, rect_h), Image.Transform.QUAD, quad_outer, resample=Image.Resampling.BICUBIC)

# Level the 0.32-deg framer mounting tilt of the inner white Matisse plate at full resolution
inner_box = (
    int(round(170 * scale)),
    int(round(175 * scale)),
    int(round(492 * scale)),
    int(round(600 * scale)),
)
inner_crop = frame_rect.crop(inner_box)
inner_leveled = inner_crop.rotate(0.32, resample=Image.Resampling.BICUBIC, expand=False, fillcolor=(2, 4, 7))
margin = int(round(10 * scale))
frame_rect.paste(
    inner_leveled.crop((margin, margin, inner_crop.width - margin, inner_crop.height - margin)),
    (inner_box[0] + margin, inner_box[1] + margin),
)

# 1. Build High-Res 4:5 Portrait (1536 x 1920) with ~10% pure #FFFFFF white studio border
c45_w, c45_h = 1536, 1920
target_fh_45 = int(round(c45_h * 0.80))  # 1536px tall frame (192px top & bottom white border)
target_fw_45 = int(round(rect_w * target_fh_45 / rect_h))
f45 = frame_rect.resize((target_fw_45, target_fh_45), Image.Resampling.LANCZOS)
canvas_45 = Image.new("RGB", (c45_w, c45_h), (255, 255, 255))
canvas_45.paste(f45, ((c45_w - target_fw_45) // 2, (c45_h - target_fh_45) // 2))

# 2. Build High-Res 1:1 Square (1800 x 1800) with ~9% pure #FFFFFF white studio border
c11_w, c11_h = 1800, 1800
target_fh_11 = int(round(c11_h * 0.82))  # 1476px tall frame (162px top & bottom white border)
target_fw_11 = int(round(rect_w * target_fh_11 / rect_h))
f11 = frame_rect.resize((target_fw_11, target_fh_11), Image.Resampling.LANCZOS)
canvas_11 = Image.new("RGB", (c11_w, c11_h), (255, 255, 255))
canvas_11.paste(f11, ((c11_w - target_fw_11) // 2, (c11_h - target_fh_11) // 2))

# Save main high-res 4:5 files in recieved-graded and recieved-need-graded
main_paths = [
    os.path.join(GRADED_DIR, "henri-matisse-blue-nude-iii-1958-color-plate.jpg"),
    os.path.join(GRADED_DIR, os.path.basename(src_path)),
    os.path.join(NEED_DIR, "henri-matisse-blue-nude-iii-1958-color-plate.jpg"),
    os.path.join(BRAIN_DIR, "matisse_hires_1536x1920_4x5.jpg"),
]
for p in main_paths:
    canvas_45.save(p, format="JPEG", quality=96, optimize=True)
    print("Saved High-Res 4:5 (1536x1920):", p)

# Save 1:1 Square variant in graded-backups and recieved-graded
sq_paths = [
    os.path.join(GRADED_DIR, "henri-matisse-blue-nude-iii-1958-color-plate-1800x1800-square.jpg"),
    os.path.join(BACKUP_DIR, "henri-matisse-blue-nude-iii-1958-color-plate-1800x1800-square.jpg"),
    os.path.join(BRAIN_DIR, "matisse_hires_1800x1800_1x1.jpg"),
]
for p in sq_paths:
    canvas_11.save(p, format="JPEG", quality=96, optimize=True)
    print("Saved High-Res 1:1 (1800x1800):", p)
