#!/usr/bin/env python3
"""
NeverRender Labs — Hald CLUT to 3D LUT Cube Conversion Daemon
------------------------------------------------------------
Monitors the LUTS and TEST_CLIPS directories for Hald CLUT PNG files and
automatically generates standard 3D LUT .cube files on modification.
"""

import os
import json
import time
import re
from PIL import Image

# ==============================================================================
# NEVERRENDER LABS — RE-CALIBRATED AUTOMATED DISK WATCHER
# TARGET SUB-LEVEL: LUTS SECTOR PRODUCTION TUNING
# ==============================================================================

# Hardcoded absolute paths mapping your real-world Windows directory layout
WATCH_FOLDER = "C:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA/LUTS"
OUT_FOLDER = "C:/Users/Saturn/Desktop/G_AG_FLDR"
NEUTRAL_HALD_PATH = "C:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA/utils/hald_2026_64.png"

WATCH_FOLDERS = [WATCH_FOLDER]

def generate_neutral_hald(path, lut_size=64):
    width = int(lut_size ** 1.5)
    height = width
    print(f"[*] Generating reference neutral Hald CLUT (identity mapping) size {width}x{height}...")
    
    img = Image.new('RGB', (width, height))
    pixels = []
    
    for i in range(width * height):
        r = i % lut_size
        g = (i // lut_size) % lut_size
        b = (i // (lut_size ** 2)) % lut_size
        
        # Scale to [0, 255]
        R = int(round((r / (lut_size - 1)) * 255))
        G = int(round((g / (lut_size - 1)) * 255))
        B = int(round((b / (lut_size - 1)) * 255))
        
        pixels.append((R, G, B))
        
    img.putdata(pixels)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    print(f"[+] Neutral Hald CLUT generated successfully at: {path}")

def hald_to_cube(png_path, cube_path, lut_size=64):
    img = Image.open(png_path).convert('RGB')
    width, height = img.size
    
    if width * height != lut_size ** 3:
        target_dim = int(lut_size ** 1.5)
        print(f"[*] Non-standard CLUT dimensions {width}x{height} detected. Scaling to target grid {target_dim}x{target_dim}...")
        img = img.resize((target_dim, target_dim), Image.Resampling.LANCZOS)
        
    with open(cube_path, 'w', encoding='utf-8') as f:
        f.write("# Created by NeverRender Labs LUT Daemon\n")
        f.write(f"LUT_3D_SIZE {lut_size}\n")
        
        # Identity mapping pixels order: red changes fastest, then green, then blue
        pixels = img.getdata()
        for r, g, b in pixels:
            rf = r / 255.0
            gf = g / 255.0
            bf = b / 255.0
            f.write(f"{rf:.6f} {gf:.6f} {bf:.6f}\n")

def run_daemon():
    print("====================================================================")
    print("[i] INITIALIZING LOG: NEVERRENDER LABS LUT WATCHER DAEMON")
    print("====================================================================")
    for folder in WATCH_FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        print(f" * Monitoring path  : {folder}")
    print(f" * Output directory : {OUT_FOLDER}")
    print(f" * Hald reference   : {NEUTRAL_HALD_PATH}")
    print("====================================================================")
    
    # Pre-generate neutral reference if missing
    if not os.path.exists(NEUTRAL_HALD_PATH):
        generate_neutral_hald(NEUTRAL_HALD_PATH)
        
    print("\n[Standby] Watching for CLUT modifications. Press Ctrl+C to exit.\n")
    
    while True:
        try:
            for watch_folder in WATCH_FOLDERS:
                for filename in os.listdir(watch_folder):
                    if filename.lower().endswith('.png'):
                        png_path = os.path.join(watch_folder, filename)
                        cube_name = os.path.splitext(filename)[0] + ".cube"
                        cube_path = os.path.join(OUT_FOLDER, cube_name)
                        
                        should_convert = False
                        if not os.path.exists(cube_path):
                            should_convert = True
                        else:
                            png_mtime = os.path.getmtime(png_path)
                            cube_mtime = os.path.getmtime(cube_path)
                            if png_mtime > cube_mtime:
                                should_convert = True
                                
                        if should_convert:
                            print(f"[*] New CLUT detected: {filename} in {os.path.basename(watch_folder)}")
                            try:
                                hald_to_cube(png_path, cube_path)
                                print(f"[+] Successfully compiled: {cube_name}")
                            except Exception as e:
                                print(f"[!] Conversion error on {filename}: {e}")
                                
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[Stop] Stopping watch daemon.")
            break
        except Exception as e:
            print(f"[Error] Exception in monitoring loop: {e}")
            time.sleep(2)

if __name__ == "__main__":
    run_daemon()
