#!/usr/bin/env python3
"""
NeverRender Labs — S22 Ultra 8-Bit CRT Terminal Video Lock Screen Generator
---------------------------------------------------------------------------
Renders a 1080x2340 (19.5:9 Samsung Galaxy S22 Ultra) 10-second vertical video loop.
Simulates a phosphor CRT terminal running NEVERRENDER_OS v12.4 with typewriter
rendering, scanlines, chromatic glow, phosphor beam sweep, and CRT vignette.
"""

import os
import sys
import math
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Output directory & file paths
BASE_DIR = "C:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA"
OUTPUT_VIDEO = os.path.join(BASE_DIR, "S22_ULTRA_CRT_LOCKSCREEN.mp4")

# Display Resolution for Samsung Galaxy S22 Ultra (1080 x 2340)
WIDTH = 1080
HEIGHT = 2340
FPS = 24
DURATION = 10.0  # seconds
TOTAL_FRAMES = int(FPS * DURATION)

# Color Palette (Phosphor Glow Matrix)
COLOR_BG = (6, 9, 14)
COLOR_GREEN = (0, 255, 102)
COLOR_AMBER = (255, 179, 0)
COLOR_CYAN = (0, 229, 255)
COLOR_PINK = (255, 0, 85)
COLOR_WHITE = (240, 246, 252)
COLOR_DIM = (70, 90, 110)

# Load Fonts
FONT_PATH = "C:/Windows/Fonts/consolab.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/courbd.ttf"

font_header = ImageFont.truetype(FONT_PATH, 34)
font_title = ImageFont.truetype(FONT_PATH, 44)
font_body = ImageFont.truetype(FONT_PATH, 36)
font_bold = ImageFont.truetype(FONT_PATH, 38)
font_small = ImageFont.truetype(FONT_PATH, 28)

# Terminal Script Timeline Definition
# (start_sec, end_sec, text, color, font, is_typewriter)
TERMINAL_EVENTS = [
    # Header Block (0.0s - 1.2s)
    (0.2, "========================================", COLOR_AMBER, font_small),
    (0.4, " SYSTEM DETECTED: NEVERRENDER_OS v12.4", COLOR_GREEN, font_header),
    (0.7, " OPERATOR: MATTHEW WYATT [8-BIT SRE]", COLOR_AMBER, font_bold),
    (0.9, " FOCUS: REAL-TIME 3D // GEN-AI PIPELINES", COLOR_GREEN, font_small),
    (1.1, "========================================", COLOR_AMBER, font_small),
    
    # Feature Callout (1.3s - 2.8s)
    (1.5, " [★] GOOGLE LABS FEATURED CREATOR", COLOR_AMBER, font_bold),
    (1.8, " [★] TOOL: RETRO-TERM 80 (labs.google)", COLOR_CYAN, font_bold),
    (2.1, "----------------------------------------", COLOR_DIM, font_small),
    
    # Core Capabilities (2.8s - 5.0s)
    (2.6, "> CORE PIPELINES & ARCHITECTURE:", COLOR_PINK, font_header),
    (3.0, "  • REAL-TIME 3D // UNREAL & COMFYUI", COLOR_WHITE, font_body),
    (3.4, "  • VEO & VERTEX PROMPT PATCHES", COLOR_WHITE, font_body),
    (3.8, "  • AE ZERO-LAG BATCH GRADING (JSX)", COLOR_WHITE, font_body),
    (4.2, "  • FASTMCP AGENTIC TOOL BRIDGES", COLOR_WHITE, font_body),
    (4.6, "----------------------------------------", COLOR_DIM, font_small),
    
    # Active SRE & Industry Trace (5.0s - 7.2s)
    (5.0, "> ACTIVE TELEMETRY & RECON:", COLOR_PINK, font_header),
    (5.4, "  • DMHC DUAL-TRACK PINCER : ENGAGED", COLOR_GREEN, font_body),
    (5.8, "  • VIANET DJENGUET : FOLLOWING @NEVERRENDERLABS", COLOR_AMBER, font_body),
    (6.2, "  • SRE SYSTEM RESILIENCE : 100% NOMINAL", COLOR_GREEN, font_body),
    (6.6, "----------------------------------------", COLOR_DIM, font_small),
    
    # Gateway Portals (7.0s - 8.5s)
    (7.0, "> GATEWAY PORTALS:", COLOR_CYAN, font_header),
    (7.4, "  ▶ WEB : RENDERWITHOUTCODE.COM", COLOR_CYAN, font_bold),
    (7.8, "  ▶ INSTA : @NEVERRENDERLABS", COLOR_PINK, font_bold),
    (8.1, "----------------------------------------", COLOR_DIM, font_small),
    
    # Shutdown / Standby Sign-Off (8.5s - 10.0s)
    (8.6, ' "Fist-bump, Matthew. System out. 🤜🐉"', COLOR_GREEN, font_bold),
    (9.1, " [ BUFFER SYNCED // STANDBY LOOP ACTIVE ]", COLOR_AMBER, font_small),
]

def get_ffmpeg_binary():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def create_scanline_mask():
    """Generates pre-rendered 1080x2340 CRT scanlines pattern."""
    scanlines = np.ones((HEIGHT, WIDTH, 3), dtype=np.float32)
    # Every 4th line has a scanline shadow
    for y in range(0, HEIGHT, 4):
        scanlines[y:y+2, :, :] = 0.55
    return scanlines

def create_vignette_mask():
    """Generates a radial vignette for CRT curve falloff."""
    Y, X = np.ogrid[:HEIGHT, :WIDTH]
    center_y, center_x = HEIGHT / 2, WIDTH / 2
    # Normalized radial distance
    dist = np.sqrt(((X - center_x) / (WIDTH * 0.55))**2 + ((Y - center_y) / (HEIGHT * 0.55))**2)
    vignette = 1.0 - np.clip(dist**2.5 * 0.45, 0.0, 0.8)
    return np.dstack([vignette]*3).astype(np.float32)

print("[1/3] Pre-generating CRT scanlines and optical vignette buffers...")
SCANLINES = create_scanline_mask()
VIGNETTE = create_vignette_mask()

def render_frame(t):
    """Renders a single frame at timestamp t (in seconds)."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_BG + (255,))
    draw = ImageDraw.Draw(img)

    # Starting layout positions (centered on S22 Ultra screen)
    start_y = 160
    current_y = start_y
    line_spacing = 42

    # Draw Terminal Lines according to timestamp
    for event in TERMINAL_EVENTS:
        start_time, text, color, font = event
        
        if t < start_time:
            continue
        
        # Calculate typewriter reveal
        time_since_start = t - start_time
        chars_to_show = int(time_since_start * 75) # 75 chars per second typing speed
        visible_text = text[:chars_to_show]
        
        if len(visible_text) > 0:
            # Draw glow shadow
            draw.text((68, current_y + 1), visible_text, font=font, fill=(color[0]//3, color[1]//3, color[2]//3, 120))
            # Draw crisp foreground text
            draw.text((66, current_y), visible_text, font=font, fill=color + (255,))
        
        current_y += line_spacing

    # Blinking cursor at the active typing position
    cursor_blink = int(t * 3.5) % 2 == 0
    if cursor_blink:
        draw.text((66, current_y), "_", font=font_bold, fill=COLOR_GREEN + (255,))

    # Convert PIL Image to NumPy array
    frame_arr = np.array(img.convert("RGB")).astype(np.float32) / 255.0

    # CRT Beam Scanline Sweep (slow moving scanline wave)
    beam_y = int((t * 0.8 % 1.0) * HEIGHT)
    beam_height = 80
    y_indices = np.arange(HEIGHT)
    beam_mask = np.exp(-((y_indices - beam_y) ** 2) / (2 * (beam_height ** 2)))
    beam_mask = np.tile(beam_mask[:, None, None], (1, WIDTH, 3)) * 0.08
    frame_arr = np.clip(frame_arr + beam_mask, 0.0, 1.0)

    # Apply Scanlines & Vignette
    frame_arr = frame_arr * SCANLINES * VIGNETTE

    # CRT Phosphor Flicker
    flicker = 1.0 + 0.02 * math.sin(t * 120.0) + 0.015 * math.sin(t * 37.0)
    frame_arr = np.clip(frame_arr * flicker * 255.0, 0, 255).astype(np.uint8)

    return frame_arr

def main():
    ffmpeg_exe = get_ffmpeg_binary()
    print(f"[2/3] Initializing Video Render Engine...")
    print(f"      Resolution: {WIDTH}x{HEIGHT} (19.5:9 Samsung S22 Ultra)")
    print(f"      Duration: {DURATION}s ({TOTAL_FRAMES} frames @ {FPS} fps)")
    print(f"      Target: {OUTPUT_VIDEO}")
    print(f"      FFmpeg Engine: {ffmpeg_exe}")

    # Start FFmpeg subprocess streaming raw video frames
    cmd = [
        ffmpeg_exe,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level:v", "4.2",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUTPUT_VIDEO
    ]

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    print("[3/3] Rendering CRT Phosphor Frames...")
    for frame_idx in range(TOTAL_FRAMES):
        t = frame_idx / FPS
        frame = render_frame(t)
        process.stdin.write(frame.tobytes())
        
        if frame_idx % 24 == 0 or frame_idx == TOTAL_FRAMES - 1:
            progress = (frame_idx + 1) / TOTAL_FRAMES * 100
            sys.stdout.write(f"\r  ▶ Render Progress: {progress:5.1f}% [{frame_idx+1}/{TOTAL_FRAMES} frames] (t={t:.2f}s)")
            sys.stdout.flush()

    process.stdin.close()
    process.wait()
    
    # Verify file integrity with FFmpeg
    verify_cmd = [ffmpeg_exe, "-v", "error", "-i", OUTPUT_VIDEO, "-f", "null", "-"]
    verify_res = subprocess.run(verify_cmd, capture_output=True, text=True)
    if verify_res.returncode == 0:
        print("\n\n[✔] VIDEO INTEGRITY VERIFIED: Playback stream is 100% valid & clean!")
    else:
        print(f"\n\n[!] Warning during verification: {verify_res.stderr}")

    print(f"    File: {OUTPUT_VIDEO}")
    print(f"    Size: {os.path.getsize(OUTPUT_VIDEO) / (1024*1024):.2f} MB\n")

if __name__ == "__main__":
    main()
