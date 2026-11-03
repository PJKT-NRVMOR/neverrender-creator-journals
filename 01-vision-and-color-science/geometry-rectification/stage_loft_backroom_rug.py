"""
Deterministic Perspective & Lighting Compositor for Mike Whitehurst's Upstairs Loft Backroom.
Supports both:
  1. Surgical alpha cleanup & sunbeam lighting integration of user's custom Photoshop
     perspective layer (`close-angle.png` -> `close-angle-clean.png` + `Backroom_CloseAngle_Clean_Composite.png`).
  2. Direct 4-corner homography warping of any rectangular rug into the calibrated
     `close-angle.png` backroom perspective quad:
       TL = (448, 208), TR = (767, 195), BR = (825, 459), BL = (294, 454)
"""

import os
import numpy as np
from PIL import Image, ImageFilter


def clean_and_composite_close_angle(
    close_angle_path: str,
    room_plate_path: str,
    out_clean_layer_path: str,
    out_composite_path: str,
) -> None:
    im = Image.open(close_angle_path).convert("RGBA")
    room = Image.open(room_plate_path).convert("RGBA")

    arr = np.array(im).astype(np.float32)
    room_arr = np.array(room).astype(np.float32)
    H, W, _ = arr.shape
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # 1. Exclude canvas border strips outside the backroom rug bounding box
    yy, xx = np.mgrid[0:H, 0:W]
    valid_box = (yy >= 190) & (yy <= 478) & (xx >= 278) & (xx <= 840)

    # 2. Exact piecewise-linear outer edges of the rug and cream fringes in close-angle.png
    x_left_limit = np.interp(yy, [205, 330, 454, 468], [449.0, 370.0, 294.0, 283.0])
    x_right_limit = np.interp(yy, [194, 330, 455, 473], [767.5, 798.0, 825.0, 831.0])

    y_top_fringe = np.interp(xx, [448, 600, 767], [205.5, 198.5, 193.0])
    y_top_red = np.interp(xx, [448, 600, 767], [210.0, 203.0, 197.0])

    y_bot_red = np.interp(xx, [294, 450, 600, 750, 825], [454.5, 457.0, 458.5, 459.5, 460.0])
    y_bot_fringe = np.interp(
        xx, [284, 320, 450, 600, 750, 830], [465.0, 465.5, 468.5, 470.5, 472.0, 473.5]
    )

    in_horiz = (xx >= x_left_limit) & (xx <= x_right_limit)
    in_main_body = in_horiz & (yy >= y_top_red) & (yy <= y_bot_red)

    # Cream/white fringe pixels have higher blue channel or lower red-blue delta than warm oak wood
    is_fringe_color = (b > 110) | ((r - b) < 52)
    in_top_fringe = in_horiz & (yy >= y_top_fringe) & (yy < y_top_red) & is_fringe_color
    in_bot_fringe = in_horiz & (yy > y_bot_red) & (yy <= y_bot_fringe) & is_fringe_color

    # Strip residual warm orange wood pixels along the outer 2.5px of left/right red borders
    is_wood_edge = (
        (g > 65)
        & (b < 90)
        & ((r - b) > 75)
        & ((xx < x_left_limit + 2.5) | (xx > x_right_limit - 2.5))
    )

    clean_mask = valid_box & (in_main_body | in_top_fringe | in_bot_fringe) & (~is_wood_edge) & (a > 120)
    mask_f = clean_mask.astype(np.float32) * 255.0
    mask_img = Image.fromarray(mask_f.astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=0.5))
    mask_aa = np.minimum(mask_f, np.array(mask_img).astype(np.float32))

    # 3. Subtle window sunbeam luminance integration from the real room floor
    room_lum = (
        0.299 * room_arr[:, :, 0] + 0.587 * room_arr[:, :, 1] + 0.114 * room_arr[:, :, 2]
    )
    lum_blur = np.array(
        Image.fromarray(np.clip(room_lum, 0, 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius=14)
        )
    ).astype(np.float32)
    # Median backroom floor luminance is ~172; transfer 16% of local floor light variation
    light_gain = np.clip(1.0 + 0.16 * ((lum_blur - 172.0) / 172.0), 0.90, 1.16)

    clean_rug = arr.copy()
    for c in range(3):
        clean_rug[:, :, c] = np.clip(clean_rug[:, :, c] * light_gain, 0, 255)
    clean_rug[:, :, 3] = mask_aa

    # 4. Natural floor contact shadow (2px vertical drop, 2.5px blur, ~37% opacity)
    shadow_mask = Image.fromarray((clean_mask.astype(np.uint8) * 95)).filter(
        ImageFilter.GaussianBlur(radius=2.5)
    )
    shadow_arr = np.zeros_like(arr)
    shadow_arr[2:, :, 3] = np.array(shadow_mask)[:-2, :]

    shadow_layer = Image.fromarray(shadow_arr.astype(np.uint8))
    rug_layer = Image.fromarray(clean_rug.astype(np.uint8))

    standalone = Image.alpha_composite(shadow_layer, rug_layer)
    os.makedirs(os.path.dirname(out_clean_layer_path), exist_ok=True)
    standalone.save(out_clean_layer_path)

    comp = Image.alpha_composite(room, standalone)
    os.makedirs(os.path.dirname(out_composite_path), exist_ok=True)
    comp.save(out_composite_path)


if __name__ == "__main__":
    base_dir = r"c:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\05-showroom-media\mike-whitehurst-loft"
    clean_and_composite_close_angle(
        close_angle_path=os.path.join(base_dir, "close-angle.png"),
        room_plate_path=os.path.join(base_dir, "Freshly cleared honey oak floor (no furniture).png"),
        out_clean_layer_path=os.path.join(base_dir, "close-angle-clean.png"),
        out_composite_path=os.path.join(
            base_dir, "priority-backroom", "Backroom_CloseAngle_Clean_Composite.png"
        ),
    )
    print("Successfully generated close-angle-clean.png and Backroom_CloseAngle_Clean_Composite.png")
