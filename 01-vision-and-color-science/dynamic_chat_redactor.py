"""
NeverRender Labs // Dynamic UI Canvas Redactor & Faststart Re-Encoder
Tracks the top horizontal border of the active prompt card across screen-capture
frames and seamlessly fills the region above it with exact sampled canvas RGB,
eliminating prior-message peek-through during collapsible thinking steps while
preserving native 1:1 SAR and GitHub-safe H.264 High +faststart delivery.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import numpy as np


def find_prompt_bubble_top(frame: np.ndarray, header_bottom: int = 84, search_bottom: int = 420) -> int:
    """Detect the top border y-coordinate of the dark rounded Antigravity prompt bubble."""
    roi = frame[header_bottom:search_bottom, 520:980]
    mask = (
        (roi[:, :, 0] >= 40) & (roi[:, :, 0] <= 64)
        & (roi[:, :, 1] >= 80) & (roi[:, :, 1] <= 104)
        & (roi[:, :, 2] >= 96) & (roi[:, :, 2] <= 120)
    )
    frac = mask.mean(axis=1)
    hits = np.where(frac > 0.70)[0]
    if len(hits) == 0:
        return -1
    return int(hits[0] + header_bottom)


def process_video(
    src_path: str,
    dst_path: str,
    start_sec: float = 0.8,
    redact_until_sec: float = 150.0,
    width: int = 1080,
    height: int = 936,
    fps: float = 24.0,
    header_bottom: int = 84,
    pane_left: int = 329,
    pane_right: int = 1077,
    canvas_rgb: tuple[int, int, int] = (21, 66, 83),
    margin_above_bubble: int = 8,
    crf: int = 24,
) -> None:
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Input video not found: {src_path}")

    decode_cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-ss", f"{start_sec:.3f}",
        "-i", src_path,
        "-vf", f"fps={fps},setsar=1",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
    ]
    encode_cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-an",
        "-c:v", "libx264", "-profile:v", "high",
        "-crf", str(crf), "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-vf", "setsar=1",
        "-movflags", "+faststart",
        dst_path,
    ]

    dec = subprocess.Popen(decode_cmd, stdout=subprocess.PIPE)
    enc = subprocess.Popen(encode_cmd, stdin=subprocess.PIPE)

    frame_bytes = width * height * 3
    canvas_color = np.array(canvas_rgb, dtype=np.uint8)
    frame_idx = 0
    masked_frames = 0
    max_masked_t = 0.0
    last_y_top = 295

    assert dec.stdout is not None and enc.stdin is not None
    try:
        while True:
            buf = dec.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            t = frame_idx / fps
            frame = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, 3)).copy()

            if t <= redact_until_sec:
                y_top = find_prompt_bubble_top(frame, header_bottom=header_bottom)
                if y_top > header_bottom:
                    mask_bottom = max(header_bottom, y_top - margin_above_bubble)
                    if mask_bottom > header_bottom:
                        frame[header_bottom:mask_bottom, pane_left:pane_right] = canvas_color
                        masked_frames += 1
                        max_masked_t = t
                    last_y_top = y_top
                elif frame_idx < int(fps * 2.0):
                    # Hold initial redaction cleanly across the first 2 seconds if bubble is settling
                    mask_bottom = max(header_bottom, last_y_top - margin_above_bubble)
                    frame[header_bottom:mask_bottom, pane_left:pane_right] = canvas_color
                    masked_frames += 1
                    max_masked_t = t

            enc.stdin.write(frame.tobytes())
            frame_idx += 1
    finally:
        dec.stdout.close()
        enc.stdin.close()
        dec_rc = dec.wait()
        enc_rc = enc.wait()

    if dec_rc != 0 or enc_rc != 0:
        raise RuntimeError(f"ffmpeg pipeline failed (dec={dec_rc}, enc={enc_rc})")

    out_size = os.path.getsize(dst_path)
    print(
        f"OK: {frame_idx} frames ({frame_idx / fps:.2f}s), "
        f"masked={masked_frames} frames (last_masked_t={max_masked_t:.2f}s), "
        f"size={out_size} bytes ({out_size / (1024 * 1024):.2f} MiB)"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Dynamically redact prior chat lines above active prompt bubble.")
    parser.add_argument("src", help="Input MP4 path")
    parser.add_argument("dst", help="Output MP4 path")
    parser.add_argument("--start", type=float, default=0.8, help="Start trim in seconds")
    parser.add_argument("--until", type=float, default=150.0, help="Stop checking for prior message after seconds")
    parser.add_argument("--crf", type=int, default=24, help="x264 CRF quality")
    args = parser.parse_args()
    process_video(args.src, args.dst, start_sec=args.start, redact_until_sec=args.until, crf=args.crf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
