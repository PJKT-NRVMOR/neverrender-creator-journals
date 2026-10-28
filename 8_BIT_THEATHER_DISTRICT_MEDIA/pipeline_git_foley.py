#!/usr/bin/env python3
"""
NeverRender Labs — Automated Foley Alignment Pipeline
------------------------------------------------------
Monitors Foley Asset directories and automatically compiles sound layers
onto the target video cut (BOUNDARY_CROSSOVER_SMALL.mp4) using MoviePy 2.x.
"""

import os
import sys
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

# --- PATH CONFIGURATION ---
BASE_DIR = "C:/Users/Saturn/Desktop/G_AG_FLDR"
VIDEO_PATH = os.path.join(BASE_DIR, "BOUNDARY_CROSSOVER_SMALL.mp4")
OUTPUT_PATH = os.path.join(BASE_DIR, "BOUNDARY_CROSSOVER_SMALL_FOLEY_MASTER.mp4")

# --- FOLEY ASSETS DIRECTORY ---
FOLEY_DIR = os.path.join(BASE_DIR, "8_BIT_THEATHER_DISTRICT_MEDIA", "FOLEY_ASSETS")

PATHS = {
    "foley": os.path.join(FOLEY_DIR, "AFX_FOLEY"),
    "footsteps": os.path.join(FOLEY_DIR, "AFX_FOLEY_FOOTSTEPS"),
    "human": os.path.join(FOLEY_DIR, "AFX_HUMAN_ELEMENTS"),
    "industry": os.path.join(FOLEY_DIR, "AFX_INDUSTRY"),
    "multimedia": os.path.join(FOLEY_DIR, "AFX_MULTIMEDIA"),
    "noise_tech": os.path.join(FOLEY_DIR, "AFX_NOISE_TONES_TECH"),
    "pro_ess": os.path.join(FOLEY_DIR, "AFX_PRO_ESS"),
    "prod_elements": os.path.join(FOLEY_DIR, "AFX_PROD_ELEMENTS"),
    "scifi": os.path.join(FOLEY_DIR, "AFX_SCIFI"),
    "tech_beeps": os.path.join(FOLEY_DIR, "AFX_TECH_NOISE_BEEPS"),
    "ambience_1": os.path.join(FOLEY_DIR, "AFX_AMBIENCE1"),
    "ambience_2": os.path.join(FOLEY_DIR, "AFX_AMBIENCE2"),
}

def find_all_wavs(directory):
    """Recursively scans a directory and returns all .wav files found."""
    wav_files = []
    if not os.path.exists(directory):
        return wav_files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files

def main():
    print(f"[*] Starting Automated Foley Alignment for: {os.path.basename(VIDEO_PATH)}")
    
    if not os.path.exists(VIDEO_PATH):
        print(f"[Error] Target video not found at {VIDEO_PATH}")
        sys.exit(1)
        
    video = VideoFileClip(VIDEO_PATH)
    audio_clips = []
    print(f"[+] Loaded Video Duration: {video.duration:.2f}s | Resolution: {video.size[0]}x{video.size[1]}")
    
    # 1. Ambient Background Hum / Neon Drone (Loop across video duration)
    amb_files = find_all_wavs(PATHS["ambience_1"]) or find_all_wavs(PATHS["noise_tech"])
    if amb_files:
        bg_hum_path = amb_files[0]
        print(f"[+] Ambient Neon Drone: {os.path.basename(bg_hum_path)}")
        bg_hum = AudioFileClip(bg_hum_path).with_volume_scaled(0.35).with_duration(video.duration)
        audio_clips.append(bg_hum)

    # 2. Tech Beeps / Arcade Pulse Accents (Staggered at 2.0s and 25.0s)
    tech_files = find_all_wavs(PATHS["tech_beeps"]) or find_all_wavs(PATHS["scifi"])
    if tech_files:
        t1_path = tech_files[0]
        print(f"[+] Tech Beep Layer 1: {os.path.basename(t1_path)}")
        t1 = AudioFileClip(t1_path).with_start(2.0).with_volume_scaled(0.75)
        audio_clips.append(t1)
        
        if len(tech_files) > 1:
            t2_path = tech_files[1]
            print(f"[+] Tech Beep Layer 2: {os.path.basename(t2_path)}")
            t2 = AudioFileClip(t2_path).with_start(25.0).with_volume_scaled(0.75)
            audio_clips.append(t2)

    # 3. Arcade Foley Mechanical Switches / Rustles (Staggered at 8.0s and 42.0s)
    foley_files = find_all_wavs(PATHS["foley"]) or find_all_wavs(PATHS["multimedia"])
    if foley_files:
        f1_path = foley_files[0]
        print(f"[+] Arcade Foley Layer 1: {os.path.basename(f1_path)}")
        f1 = AudioFileClip(f1_path).with_start(8.0).with_volume_scaled(0.8)
        audio_clips.append(f1)

    # 4. Sci-Fi Glitch / Neon Pulse Accent at 35.0s
    scifi_files = find_all_wavs(PATHS["scifi"])
    if scifi_files:
        s1_path = scifi_files[0]
        print(f"[+] Sci-Fi Accent: {os.path.basename(s1_path)}")
        s1 = AudioFileClip(s1_path).with_start(35.0).with_volume_scaled(0.85)
        audio_clips.append(s1)

    # 5. Footsteps Alignment at 57.0s
    footstep_files = find_all_wavs(PATHS["footsteps"])
    if footstep_files and video.duration > 57.0:
        fs_path = footstep_files[0]
        print(f"[+] Footstep Foley Layer: {os.path.basename(fs_path)}")
        fs = AudioFileClip(fs_path).with_start(57.0).with_volume_scaled(0.7)
        audio_clips.append(fs)

    # --- RENDER SEQUENCE ---
    if audio_clips:
        final_audio = CompositeAudioClip(audio_clips)
        video = video.with_audio(final_audio)
        
        print(f"\n[*] Rendering Foley Master -> {OUTPUT_PATH}")
        video.write_videofile(
            OUTPUT_PATH, 
            codec="libx264", 
            audio_codec="aac",
            temp_audiofile='temp-audio.m4a', 
            remove_temp=True
        )
        print(f"\n[SUCCESS] Master Foley Render Complete! Saved to: {OUTPUT_PATH}")
    else:
        print("[Error] No foley audio files found in FOLEY_ASSETS!")

if __name__ == "__main__":
    main()
