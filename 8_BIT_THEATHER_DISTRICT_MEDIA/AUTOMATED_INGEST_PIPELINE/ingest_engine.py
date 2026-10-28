import os
import sys
import re
import subprocess
import json
import argparse
from pathlib import Path

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = "ffmpeg"

BASE_DIR = Path(__file__).resolve().parent
DROP_ZONE = BASE_DIR / "DROP_ZONE_RAW"
PROCESSED_DIR = BASE_DIR / "PROCESSED_TAKES"
EXPORTS_DIR = BASE_DIR / "EXPORTS_STRINGOUTS"

def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    return result

def get_duration(video_path):
    cmd = [FFMPEG_PATH, "-i", str(video_path)]
    res = run_cmd(cmd)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0

def detect_speech_boundaries(video_path, noise_db="-30dB", min_silence=0.8):
    """
    Detects start and end of silence intervals to determine where action/dialogue lives.
    Returns (in_point, out_point) with safety margins.
    """
    cmd = [
        FFMPEG_PATH, "-i", str(video_path),
        "-af", f"silencedetect=noise={noise_db}:d={min_silence}",
        "-f", "null", "-"
    ]
    res = run_cmd(cmd)
    
    total_duration = get_duration(video_path)
    if total_duration <= 0:
        return 0.0, 0.0
    
    silence_starts = [float(x) for x in re.findall(r"silence_start:\s*([\d\.]+)", res.stderr)]
    silence_ends = [float(x) for x in re.findall(r"silence_end:\s*([\d\.]+)", res.stderr)]
    
    in_point = 0.0
    out_point = total_duration

    # If clip starts with silence > 1.0s, trim head
    if silence_starts and silence_starts[0] < 0.5 and silence_ends:
        head_silence_end = silence_ends[0]
        if head_silence_end > 1.0:
            in_point = max(0.0, head_silence_end - 0.3)  # 300ms pre-roll breathing room
            
    # If clip ends with silence, trim tail
    if silence_starts and silence_starts[-1] > in_point:
        tail_silence_start = silence_starts[-1]
        if total_duration - tail_silence_start > 1.0:
            out_point = min(total_duration, tail_silence_start + 0.3)  # 300ms tail breathing room

    # Guardrails
    if out_point <= in_point or (out_point - in_point) < 1.0:
        in_point = 0.0
        out_point = total_duration

    return in_point, out_point

def get_audio_flags(audio_codec):
    """
    Returns audio encoding flags. Always locks sample rate to 48,000 Hz broadcast standard
    to prevent audio drift, clicks, or popping across mixed camera cards.
    """
    if audio_codec == "pcm24":
        return ["-c:a", "pcm_s24le", "-ar", "48000"]
    elif audio_codec == "pcm16":
        return ["-c:a", "pcm_s16le", "-ar", "48000"]
    else:  # aac
        return ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]

def trim_clip(src_path, dst_path, in_point, out_point, is_prores=False, audio_codec="aac"):
    """
    Trims raw clip into clean intermediate take with uniform 1080p framing and locked 48kHz audio.
    Supports 10-bit ProRes 422 (.mov) or standard high-bitrate H.264 (.mp4).
    """
    duration = out_point - in_point
    audio_flags = get_audio_flags(audio_codec)
    
    if is_prores:
        video_flags = [
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le"
        ]
    else:
        video_flags = [
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20"
        ]

    cmd = [
        FFMPEG_PATH, "-y",
        "-ss", str(in_point),
        "-i", str(src_path),
        "-t", str(duration)
    ] + video_flags + audio_flags + [str(dst_path)]
    
    return run_cmd(cmd)

def build_stringout_landscape(concat_list_path, output_path, is_prores=False, audio_codec="aac"):
    """
    Stream-Copy Concat (-c copy):
    Since intermediate trimmed takes are already uniformly encoded to exact specifications,
    stream-copy stitches the entire landscape master in ~3 seconds with ZERO generational loss.
    Falls back to re-encode if stream-copy encounters container variations.
    """
    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-c", "copy",
        str(output_path)
    ]
    res = run_cmd(cmd)
    
    # Fallback to re-encode if stream copy fails
    if res.returncode != 0 or not output_path.exists() or output_path.stat().st_size == 0:
        print("    [!] Stream-copy fallback: re-encoding landscape master...")
        audio_flags = get_audio_flags(audio_codec)
        if is_prores:
            v_flags = ["-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le"]
        else:
            v_flags = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]
            
        fallback_cmd = [
            FFMPEG_PATH, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list_path)
        ] + v_flags + audio_flags + [str(output_path)]
        return run_cmd(fallback_cmd)
    return res

def build_stringout_vertical_1080p(concat_list_path, output_path, is_prores=False, audio_codec="aac"):
    """
    Renders 1080x1920 (9:16) portrait format:
    Cinematic blurred background fill with razor-sharp centered original 16:9 action.
    """
    audio_flags = get_audio_flags(audio_codec)
    
    if is_prores:
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2"
        )
        v_flags = ["-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le"]
    else:
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p"
        )
        v_flags = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22"]

    cmd = [
        FFMPEG_PATH, "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list_path),
        "-filter_complex", filter_complex
    ] + v_flags + audio_flags + [str(output_path)]
    
    return run_cmd(cmd)

def process_pipeline(dry_run=False, noise_db="-30dB", min_silence=0.8, is_prores=False, audio_codec="aac"):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    video_exts = {".mp4", ".mov", ".mkv", ".m4v", ".avi"}
    raw_files = sorted([f for f in DROP_ZONE.iterdir() if f.is_file() and f.suffix.lower() in video_exts])

    if not raw_files:
        print(f"[!] No raw video files found in {DROP_ZONE}")
        print("    Drop raw .mp4 or .mov clips into that folder and run this script.")
        return

    ext = ".mov" if (is_prores or "pcm" in audio_codec) else ".mp4"
    codec_label = "ProRes 422 10-bit" if is_prores else "H.264 1080p"
    
    print(f"[*] Found {len(raw_files)} raw video clip(s) in drop zone.")
    print(f"[*] Target Profile: {codec_label} | Audio: {audio_codec.upper()} (48,000 Hz locked)")
    print(f"[*] Acoustic Thresholds: noise={noise_db} | min_silence={min_silence}s")
    print("=" * 65)

    report = []
    trimmed_files = []
    total_raw_sec = 0.0
    total_trimmed_sec = 0.0

    for idx, video in enumerate(raw_files, 1):
        raw_duration = get_duration(video)
        total_raw_sec += raw_duration
        in_p, out_p = detect_speech_boundaries(video, noise_db=noise_db, min_silence=min_silence)
        trimmed_duration = out_p - in_p
        total_trimmed_sec += trimmed_duration
        saved = raw_duration - trimmed_duration

        print(f"[{idx}/{len(raw_files)}] Analyzing: {video.name}")
        print(f"    Raw Duration: {raw_duration:.2f}s | Active Take: {in_p:.2f}s -> {out_p:.2f}s ({trimmed_duration:.2f}s)")
        print(f"    Dead air stripped: {saved:.2f}s ({((saved/raw_duration)*100 if raw_duration else 0):.1f}%)")

        out_clip_name = f"Take_{idx:03d}_{video.stem}_cleaned{ext}"
        out_clip_path = PROCESSED_DIR / out_clip_name

        if not dry_run:
            print(f"    Trimming to {out_clip_name} ({codec_label}, 48kHz)...")
            trim_clip(video, out_clip_path, in_p, out_p, is_prores=is_prores, audio_codec=audio_codec)
            trimmed_files.append(out_clip_path)

        report.append({
            "take_id": idx,
            "filename": video.name,
            "raw_duration_sec": round(raw_duration, 2),
            "in_point": round(in_p, 2),
            "out_point": round(out_p, 2),
            "clean_duration_sec": round(trimmed_duration, 2),
            "time_saved_sec": round(saved, 2)
        })

    if dry_run:
        print("\n[DRY RUN COMPLETE] Analysis finished without rendering video files.")
        return

    # Write concat manifest
    concat_txt_path = PROCESSED_DIR / "concat_manifest.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for clip in trimmed_files:
            f.write(f"file '{clip.as_posix()}'\n")

    print("\n" + "=" * 65)
    print("[*] Stitching clean takes into Master Assembly Reels...")
    
    # 1. Landscape Master via Stream-Copy Concat
    out_landscape = EXPORTS_DIR / f"ASSEMBLY_SELECTS_1080P_LANDSCAPE{ext}"
    print(f"    [1/2] Stitched Landscape (Stream-Copy Concat): {out_landscape.name}...")
    build_stringout_landscape(concat_txt_path, out_landscape, is_prores=is_prores, audio_codec=audio_codec)

    # 2. 1080p Vertical / Portrait Master
    out_vertical = EXPORTS_DIR / f"ASSEMBLY_SELECTS_1080P_VERTICAL_PORTRAIT{ext}"
    print(f"    [2/2] Rendering 9:16 Vertical Portrait (1080x1920): {out_vertical.name}...")
    build_stringout_vertical_1080p(concat_txt_path, out_vertical, is_prores=is_prores, audio_codec=audio_codec)

    time_saved_total = total_raw_sec - total_trimmed_sec
    pct_saved = (time_saved_total / total_raw_sec * 100) if total_raw_sec else 0.0

    report_md = EXPORTS_DIR / "INGEST_DECISION_LOG.md"
    with open(report_md, "w", encoding="utf-8") as f:
        f.write("# Nathan Doan Productions // Automated Ingest & Stringout Report\n\n")
        f.write(f"- **Total Raw Footage**: {total_raw_sec:.1f}s ({total_raw_sec/60:.2f} mins)\n")
        f.write(f"- **Clean Active Selects**: {total_trimmed_sec:.1f}s ({total_trimmed_sec/60:.2f} mins)\n")
        f.write(f"- **Junk/Silence Stripped**: {time_saved_total:.1f}s ({pct_saved:.1f}% reduction)\n")
        f.write(f"- **Video Profile**: `{codec_label}`\n")
        f.write(f"- **Audio Standard**: `48,000 Hz Locked` ({audio_codec.upper()})\n")
        f.write(f"- **Master Landscape Assembly**: `{out_landscape.name}` (Stream-Copy Stitched)\n")
        f.write(f"- **Master Vertical Assembly**: `{out_vertical.name}` (1080x1920 9:16 Mobile/Reels/Shorts)\n\n")
        f.write("## Clip Cut Index\n\n")
        f.write("| Take | Raw Clip Name | Raw Len | In Point | Out Point | Clean Len | Dead Air Removed |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in report:
            f.write(f"| {r['take_id']} | `{r['filename']}` | {r['raw_duration_sec']}s | {r['in_point']}s | {r['out_point']}s | {r['clean_duration_sec']}s | **-{r['time_saved_sec']}s** |\n")

    print("\n[SUCCESS] Pipeline Complete!")
    print(f"    Landscape Master: {out_landscape}")
    print(f"    Vertical Master:  {out_vertical}")
    print(f"    Ingest Log:       {report_md}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeverRender Labs Automated Ingest & Smart Selects Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Analyze clips and detect boundaries without rendering")
    parser.add_argument("--prores", action="store_true", help="Export 10-bit Apple ProRes 422 (.mov) for NLE editing (Sony/Canon/Panasonic Log)")
    parser.add_argument("--audio", choices=["aac", "pcm16", "pcm24"], default="aac", help="Audio format: aac (default), pcm16 (16-bit uncompressed), pcm24 (24-bit broadcast)")
    parser.add_argument("--noise", default="-30dB", help="Silence detection threshold (default: -30dB, e.g. -25dB for noisy rooms, -35dB for quiet studio)")
    parser.add_argument("--silence", type=float, default=0.8, help="Minimum silence duration in seconds to trigger split (default: 0.8s)")
    args = parser.parse_args()

    audio_choice = args.audio
    if args.prores and audio_choice == "aac":
        audio_choice = "pcm24"  # Default ProRes to pristine 24-bit PCM

    process_pipeline(
        dry_run=args.dry_run,
        noise_db=args.noise,
        min_silence=args.silence,
        is_prores=args.prores,
        audio_codec=audio_choice
    )

