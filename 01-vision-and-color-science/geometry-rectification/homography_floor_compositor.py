"""
NeverRender Labs // Vision & Color Science Toolkit
Module: homography_floor_compositor.py

Client-agnostic 2D projective homography (PGL(3, R)) and furniture-occlusion compositor
for rectifying keystone-skewed textile photographs onto perspective architectural floor planes.
"""

from typing import List, Optional, Tuple
import numpy as np
from PIL import Image, ImageFilter

Point2D = Tuple[float, float]


def compute_perspective_coeffs(src_pts: List[Point2D], dst_pts: List[Point2D]) -> List[float]:
    """
    Solve the 8-parameter perspective homography mapping destination (x, y) -> source (X, Y)
    for PIL.Image.transform(..., Image.Transform.PERSPECTIVE, coeffs).
    """
    matrix_a = []
    vector_b = []
    for (src_x, src_y), (dst_x, dst_y) in zip(src_pts, dst_pts):
        matrix_a.append([dst_x, dst_y, 1.0, 0.0, 0.0, 0.0, -dst_x * src_x, -dst_y * src_x])
        matrix_a.append([0.0, 0.0, 0.0, dst_x, dst_y, 1.0, -dst_x * src_y, -dst_y * src_y])
        vector_b.append(src_x)
        vector_b.append(src_y)
    a_arr = np.array(matrix_a, dtype=np.float64)
    b_arr = np.array(vector_b, dtype=np.float64)
    coeffs = np.linalg.solve(a_arr, b_arr)
    return coeffs.tolist()


def rectify_and_project_textile(
    src_image: Image.Image,
    src_corners: List[Point2D],
    dst_quad: List[Point2D],
    canvas_size: Tuple[int, int],
    uv_size: Tuple[int, int] = (800, 1200),
    top_fringe_px: int = 0,
    bottom_fringe_px: int = 36,
    mirror_heal_v: Optional[Tuple[float, float]] = None,
) -> Image.Image:
    """
    Rectifies a skewed source textile image defined by 4 pile corners into canonical UV space,
    synthesizes clean top/bottom fringes, and projects onto the target room canvas quad.
    """
    w_uv, h_uv = uv_size
    h_total = top_fringe_px + h_uv + bottom_fringe_px
    uv_dst = [
        (0.0, float(top_fringe_px)),
        (float(w_uv), float(top_fringe_px)),
        (float(w_uv), float(top_fringe_px + h_uv)),
        (0.0, float(top_fringe_px + h_uv)),
    ]

    coeffs_to_uv = compute_perspective_coeffs(src_corners, uv_dst)
    uv_rgb = src_image.convert("RGB").transform(
        (w_uv, h_total),
        Image.Transform.PERSPECTIVE,
        coeffs_to_uv,
        Image.Resampling.BICUBIC,
    )
    uv_arr = np.array(uv_rgb, dtype=np.float32)

    if mirror_heal_v is not None:
        v0 = top_fringe_px + int(mirror_heal_v[0] * h_uv)
        v1 = top_fringe_px + int(mirror_heal_v[1] * h_uv)
        for y_uv in range(v0, v1):
            y_sym = (2 * top_fringe_px + h_uv - 1) - y_uv
            alpha_h = np.sin(np.pi * (y_uv - v0) / float(max(1, v1 - v0)))
            uv_arr[y_uv] = uv_arr[y_uv] * (1.0 - alpha_h) + uv_arr[y_sym] * alpha_h

    uv_rgba = np.zeros((h_total, w_uv, 4), dtype=np.float32)
    uv_rgba[:, :, :3] = uv_arr
    uv_rgba[top_fringe_px : top_fringe_px + h_uv, :, 3] = 255.0

    rng = np.random.default_rng(42)
    if top_fringe_px > 0:
        strands_t = rng.uniform(0.76, 1.0, size=(1, w_uv, 1))
        for fy in range(top_fringe_px):
            t = (top_fringe_px - 1 - fy) / float(top_fringe_px)
            uv_rgba[fy, :, :3] = np.array([230.0, 222.0, 208.0])[None, :] * strands_t[0]
            strand_alpha = (1.0 - t**1.5) * (0.60 + 0.40 * (strands_t[0, :, 0] > 0.82))
            uv_rgba[fy, :, 3] = np.clip(strand_alpha * 255.0, 0.0, 255.0)

    if bottom_fringe_px > 0:
        strands_b = rng.uniform(0.76, 1.0, size=(1, w_uv, 1))
        for fy in range(bottom_fringe_px):
            t = fy / float(bottom_fringe_px)
            y_idx = top_fringe_px + h_uv + fy
            base_cream = np.array([232.0, 224.0, 210.0])[None, :] * strands_b[0]
            nat_row = uv_arr[y_idx]
            uv_rgba[y_idx, :, :3] = np.clip(0.45 * nat_row + 0.55 * base_cream, 150.0, 250.0)
            strand_alpha = (1.0 - t**1.6) * (0.65 + 0.35 * (strands_b[0, :, 0] > 0.83))
            uv_rgba[y_idx, :, 3] = np.clip(strand_alpha * 255.0, 0.0, 255.0)

    uv_rgba[:, :2, 3] *= 0.3
    uv_rgba[:, -2:, 3] *= 0.3

    uv_rgba_img = Image.fromarray(uv_rgba.astype(np.uint8))
    coeffs_to_canvas = compute_perspective_coeffs(uv_dst, dst_quad)
    return uv_rgba_img.transform(
        canvas_size,
        Image.Transform.PERSPECTIVE,
        coeffs_to_canvas,
        Image.Resampling.BICUBIC,
    )
