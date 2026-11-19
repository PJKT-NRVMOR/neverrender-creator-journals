#!/usr/bin/env python3
"""
NeverRender Labs // Area 33 Vertical Social Trailer Compiler (1080x1920, 24fps)
Composites custom 9:16 welcome plates, real Google Flow RenderSin vs. RenderWin
footage, Pillow RGBA D-Suite HUD overlays with safe-zone telemetry, synthesized
Web-Audio-style metallic *DING!* bells, original clip audio punch-ins (Wahl clippers),
and the mastered WAWYS midnight saxophone groove into a broadcast-ready social reel.
"""

import argparse
import os
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 24
SR = 48000

FONT_DIR = Path(r"C:\Windows\Fonts")


def load_font(candidates, size):
    for name in candidates:
        p = FONT_DIR / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


FONT_TITLE = load_font(["bahnschrift.ttf", "segoeuib.ttf", "arialbd.ttf"], 54)
FONT_HERO = load_font(["impact.ttf", "bahnschrift.ttf", "arialbd.ttf"], 84)
FONT_SUB = load_font(["consolab.ttf", "consola.ttf", "arialbd.ttf"], 32)
FONT_MONO = load_font(["consolab.ttf", "consola.ttf"], 28)
FONT_MONO_SM = load_font(["consolab.ttf", "consola.ttf"], 24)
FONT_URL = load_font(["consolab.ttf", "consola.ttf", "segoeuib.ttf"], 36)


def draw_centered_text(draw, y, text, font, fill, shadow=(0, 0, 0, 210), offset=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    if shadow:
        draw.text((x + offset, y + offset), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def build_hud_overlay(
    out_path,
    counter_text,
    counter_mode,
    kicker,
    headline,
    subline,
    footer_cta="RENDERWITHOUTCODE.COM/AREA-33",
    is_title_card=False,
):
    """Render a 1080x1920 transparent RGBA HUD overlay respecting 9:16 social safe zones."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Subtle top & bottom vignette gradient for guaranteed text contrast
    for row in range(0, 340):
        alpha = int(175 * (1.0 - row / 340.0) ** 1.6)
        draw.line([(0, row), (W, row)], fill=(5, 11, 15, alpha))
    for row in range(H - 640, H):
        t = (row - (H - 640)) / 640.0
        alpha = int(225 * (t ** 1.35))
        draw.line([(0, row), (W, row)], fill=(5, 11, 15, alpha))

    # Color theme by mode: 'sin', 'win', 'intro', 'outro'
    if counter_mode == "sin":
        accent = (255, 92, 102, 255)
        pill_bg = (38, 10, 16, 228)
        badge_txt = (255, 145, 154, 255)
    elif counter_mode == "win":
        accent = (0, 255, 136, 255)
        pill_bg = (7, 36, 28, 232)
        badge_txt = (120, 255, 192, 255)
    else:
        accent = (255, 107, 43, 255)
        pill_bg = (8, 25, 34, 232)
        badge_txt = (44, 229, 246, 255)

    # 1. Top Safe-Zone Running Telemetry Pill (y=175..245)
    pill_w, pill_h = 840, 74
    px0 = (W - pill_w) // 2
    py0 = 175
    draw.rounded_rectangle(
        [px0, py0, px0 + pill_w, py0 + pill_h],
        radius=8,
        fill=pill_bg,
        outline=accent,
        width=3,
    )
    # Small indicator square
    draw.rectangle([px0 + 22, py0 + 26, px0 + 44, py0 + 48], fill=accent)
    draw.text((px0 + 62, py0 + 20), counter_text, font=FONT_SUB, fill=(245, 252, 255, 255))

    # 2. Lower Safe-Zone Glass Plaque (tightly fitted above y=1562 for Reels/Shorts UI)
    card_x0, card_x1 = 68, W - 68
    head_font = FONT_HERO if is_title_card else FONT_TITLE
    words = headline.split()
    lines = []
    cur = ""
    max_w = (card_x1 - card_x0) - 68
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=head_font)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    lines = lines[:2]

    line_step = 88 if is_title_card else 62
    content_h = 24 + 42 + len(lines) * line_step + (38 if subline else 0) + 22
    card_y1 = 1562
    card_y0 = card_y1 - content_h

    draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1],
        radius=10,
        fill=(7, 22, 31, 228),
        outline=(44, 229, 246, 175) if counter_mode != "sin" else (255, 92, 102, 205),
        width=2,
    )
    # Left solid neon accent stripe
    draw.rectangle([card_x0, card_y0 + 2, card_x0 + 10, card_y1 - 2], fill=accent)

    y_cur = card_y0 + 22
    draw.text((card_x0 + 34, y_cur), kicker, font=FONT_MONO, fill=badge_txt)
    y_cur += 42

    for ln in lines:
        draw.text((card_x0 + 34, y_cur), ln, font=head_font, fill=(255, 255, 255, 255))
        y_cur += line_step

    if subline:
        y_cur += 4
        draw.text((card_x0 + 34, y_cur), subline, font=FONT_MONO_SM, fill=(196, 226, 236, 255))

    # Bottom URL Ribbon right inside safe zone (y=1585..1648)
    if footer_cta:
        by0 = 1585
        draw.rounded_rectangle(
            [170, by0, W - 170, by0 + 60],
            radius=6,
            fill=(255, 107, 43, 238) if counter_mode == "outro" else (11, 34, 45, 225),
            outline=(255, 107, 43, 255),
            width=2,
        )
        cta_color = (7, 25, 34, 255) if counter_mode == "outro" else (255, 255, 255, 255)
        draw_centered_text(draw, by0 + 12, footer_cta, FONT_URL, cta_color, shadow=None)

    img.save(out_path, "PNG")


def synth_ding(duration=0.65):
    t = np.linspace(0, duration, int(SR * duration), endpoint=False, dtype=np.float64)
    sig = (
        0.55 * np.sin(2 * np.pi * 2093.0 * t) * np.exp(-6.5 * t)
        + 0.28 * np.sin(2 * np.pi * 4186.0 * t) * np.exp(-10.0 * t)
        + 0.14 * np.sin(2 * np.pi * 5274.0 * t) * np.exp(-14.0 * t)
    )
    attack = np.minimum(1.0, t / 0.004)
    sig = sig * attack
    return np.stack([sig, sig], axis=1)


def synth_win_chord(duration=0.75):
    t = np.linspace(0, duration, int(SR * duration), endpoint=False, dtype=np.float64)
    sig = np.zeros_like(t)
    notes = [(523.25, 0.00), (659.25, 0.055), (783.99, 0.11), (1046.50, 0.165)]
    for freq, delay in notes:
        mask = t >= delay
        dt = np.where(mask, t - delay, 0.0)
        env = np.where(mask, np.minimum(1.0, dt / 0.012) * np.exp(-5.8 * dt), 0.0)
        tone = 0.28 * (np.sin(2 * np.pi * freq * dt) + 0.25 * np.sin(2 * np.pi * 2 * freq * dt))
        sig += tone * env
    return np.stack([sig, sig], axis=1)


def load_audio_segment(path, start_sec, dur_sec):
    """Extract exact stereo float64 PCM slice at 48 kHz using ffmpeg."""
    cmd = [
        "ffmpeg", "-v", "error",
        "-ss", f"{start_sec:.3f}",
        "-t", f"{dur_sec:.3f}",
        "-i", str(path),
        "-f", "f32le", "-acodec", "pcm_f32le", "-ar", str(SR), "-ac", "2",
        "pipe:1",
    ]
    raw = subprocess.check_output(cmd)
    arr = np.frombuffer(raw, dtype=np.float32).astype(np.float64).reshape(-1, 2)
    need = int(round(dur_sec * SR))
    if len(arr) < need:
        pad = np.zeros((need - len(arr), 2), dtype=np.float64)
        arr = np.vstack([arr, pad])
    return arr[:need]


def write_wav(path, stereo_float):
    clipped = np.clip(stereo_float, -0.98, 0.98)
    pcm16 = (clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm16.tobytes())


def render_still_clip(img_path, overlay_path, dur_sec, out_mp4, zoom_start=1.0, zoom_end=1.06):
    """Render a smooth 24fps 1080x1920 Ken Burns clip from a still plate + RGBA HUD overlay."""
    frames = int(round(dur_sec * FPS))
    # Pre-scale image cleanly to 1296x2304 (1.2x headroom) so zoompan stays buttery sharp
    zoom_expr = f"{zoom_start:.4f}+({zoom_end - zoom_start:.4f})*on/{max(frames - 1, 1)}"
    vf = (
        f"[0:v]scale=1296:2304:force_original_aspect_ratio=increase,crop=1296:2304,setsar=1,"
        f"zoompan=z='{zoom_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}[bg];"
        f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-loop", "1", "-t", f"{dur_sec:.3f}", "-i", str(img_path),
            "-i", str(overlay_path),
            "-filter_complex", vf,
            "-map", "[v]",
            "-t", f"{dur_sec:.3f}",
            "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            str(out_mp4),
        ],
        check=True,
    )


def render_video_clip(src_mp4, start_sec, dur_sec, overlay_path, out_mp4):
    """Trim, scale to 1080x1920 24fps, and composite the RGBA HUD overlay."""
    vf = (
        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
        f"crop={W}:{H},setsar=1,fps={FPS}[bg];"
        f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-ss", f"{start_sec:.3f}", "-t", f"{dur_sec:.3f}", "-i", str(src_mp4),
            "-i", str(overlay_path),
            "-filter_complex", vf,
            "-map", "[v]",
            "-t", f"{dur_sec:.3f}",
            "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
            str(out_mp4),
        ],
        check=True,
    )


def build_trailer(args):
    work = Path(tempfile.mkdtemp(prefix="area33_trailer_"))
    try:
        segments = [
            # 0: Cold Open Welcome Plate (3.2s)
            {
                "kind": "still",
                "src": Path(args.welcome_plate),
                "dur": 3.2,
                "zoom": (1.00, 1.05),
                "counter": "AREA 33 // PROVING GROUND DECLASSIFIED",
                "mode": "intro",
                "kicker": "NEVERRENDER LABS // THE RINDER-FILES",
                "headline": "WELCOME TO AREA 33",
                "subline": "RINDERSIN, NEVADA  //  REAL AI FAILS & REAL FIXES",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": True,
            },
            # 1: EP-01 SIN #01 (Reverse Gear + M18 Smoke) (3.0s)
            {
                "kind": "video",
                "src": Path(args.ep01_sin),
                "start": 1.2,
                "dur": 3.0,
                "counter": "SINS: 001 *DING!*  //  EP-01: BASSAKWARDS",
                "mode": "sin",
                "kicker": "EPISODE 01 // RENDERSIN #01",
                "headline": "REVERSE GEAR + M18 SMOKE",
                "subline": "SUPER DROSS BACKS UP INSIDE A TEAL SMOKE SCREEN",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": False,
            },
            # 2: EP-01 WIN (55 MPH Parallax) (2.2s)
            {
                "kind": "video",
                "src": Path(args.ep01_win),
                "start": 1.0,
                "dur": 2.2,
                "counter": "SINS: 000 // REDEEMED: 55 MPH PARALLAX",
                "mode": "win",
                "kicker": "SAME PLATE // SAME MODEL // PURE PROMPT FIX",
                "headline": "FORWARD DRIVE LOCKED",
                "subline": "MONOPOLE CLEARS A-PILLAR RIGHT AT SECOND 3",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": False,
            },
            # 3: EP-02 SIN #02 (Knights of WEE / NEE) (3.0s)
            {
                "kind": "video",
                "src": Path(args.ep02_wee),
                "start": 2.8,
                "dur": 3.0,
                "counter": "SINS: 002 *DING!*  //  EP-02: BROADWAY",
                "mode": "sin",
                "kicker": "EPISODE 02 // TAKE 02 RENDERSIN",
                "headline": "THE KNIGHTS OF WEE / NEE",
                "subline": "OMNI SMASHED THE BROADWAY TICKER INTO 'WEE'",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": False,
            },
            # 4: EP-02 SIN #03 (Tim Burton Spiral Hill) (3.2s)
            {
                "kind": "video",
                "src": Path(args.ep02_spiral),
                "start": 2.3,
                "dur": 3.2,
                "counter": "SINS: 003 *DING!*  //  GOTHIC PRIOR HIT",
                "mode": "sin",
                "kicker": "EPISODE 02 // TAKE 03 RENDERSIN",
                "headline": "JACK SKELLINGTON SMOKE-BOMB",
                "subline": "'SWIRLING' + 'GOTHIC' SUMMONED SPIRAL HILL",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": False,
            },
            # 5: EP-02 SIN #04 (1994 Chrysler Wind Tunnel + Wahl Clippers) (3.8s)
            {
                "kind": "video",
                "src": Path(args.ep02_wind),
                "start": 1.3,
                "dur": 3.8,
                "counter": "SINS: 004 *DING!*  //  1080P HALL OF FAME",
                "mode": "sin",
                "kicker": "EPISODE 02 // TAKE 04 (ACTUAL AUDIO ON!)",
                "headline": "1994 CHRYSLER WIND TUNNEL",
                "subline": "NASA STREAMLINES + ANGRY WAHL HAIR CLIPPERS",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": False,
            },
            # 6: EP-02 WIN (Take 05 Draft Parade Keeper) (4.6s)
            {
                "kind": "video",
                "src": Path(args.ep02_win),
                "start": 0.9,
                "dur": 4.6,
                "counter": "SINS: 000 // CERTIFIED 1080P KEEPER!",
                "mode": "win",
                "kicker": "EPISODE 02 // TAKE 05: THE DRAFT PARADE",
                "headline": "ZERO SINS. ZERO CLIPPERS.",
                "subline": "CALM TEAL MIST + RAZOR-SHARP MARQUEE + PUDDLE GLOW",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": False,
            },
            # 7: Closing CTA Billboard Card (4.0s)
            {
                "kind": "still",
                "src": Path(args.outro_plate),
                "dur": 4.0,
                "zoom": (1.00, 1.07),
                "counter": "RINDERSIN, NEVADA // ZERO CHERRY-PICKING",
                "mode": "outro",
                "kicker": "WATCH BOTH EPISODES + FREE DRIVE SWEEP TEMPLATE",
                "headline": "ENTER AREA 33",
                "subline": "EP-01 BASSAKWARDS  //  EP-02 DRAFT PARADE",
                "cta": "RENDERWITHOUTCODE.COM/AREA-33",
                "title_card": True,
            },
        ]

        part_paths = []
        t_cursor = 0.0
        starts = []
        for idx, seg in enumerate(segments):
            starts.append(t_cursor)
            ov = work / f"ov_{idx:02d}.png"
            build_hud_overlay(
                ov,
                counter_text=seg["counter"],
                counter_mode=seg["mode"],
                kicker=seg["kicker"],
                headline=seg["headline"],
                subline=seg["subline"],
                footer_cta=seg["cta"],
                is_title_card=seg["title_card"],
            )
            part = work / f"part_{idx:02d}.mp4"
            if seg["kind"] == "still":
                render_still_clip(seg["src"], ov, seg["dur"], part, seg["zoom"][0], seg["zoom"][1])
            else:
                render_video_clip(seg["src"], seg["start"], seg["dur"], ov, part)
            part_paths.append(part)
            t_cursor += seg["dur"]

        total_dur = t_cursor
        concat_list = work / "concat.txt"
        concat_list.write_text(
            "\n".join(f"file '{p.as_posix()}'" for p in part_paths),
            encoding="utf-8",
        )
        video_only = work / "video_concat.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-f", "concat", "-safe", "0", "-i", str(concat_list),
                "-c", "copy", str(video_only),
            ],
            check=True,
        )

        # --- Studio Stereo Audio Mix (48 kHz) ---
        total_samples = int(round(total_dur * SR))
        mix = np.zeros((total_samples, 2), dtype=np.float64)

        # Music bed 1 (00:00 -> 18.4s): WAWYS energetic groove starting at 00:07.5
        bed1_dur = starts[6]
        bed1 = load_audio_segment(args.wawys_audio, 7.5, bed1_dur) * 0.56
        # Duck music smoothly under Take 04 Wahl clippers (starts[5]..starts[6])
        w0 = int(starts[5] * SR)
        w1 = int(starts[6] * SR)
        env1 = np.ones(len(bed1), dtype=np.float64)
        fade = int(0.25 * SR)
        env1[w0:w0 + fade] = np.linspace(1.0, 0.14, fade)
        env1[w0 + fade:w1] = 0.14
        # Gentle intro fade-in (0.35s)
        in_f = int(0.35 * SR)
        env1[:in_f] *= np.linspace(0.0, 1.0, in_f)
        mix[:len(bed1)] += bed1 * env1[:, None]

        # Real Wahl Hair Clipper audio punch-in on Take 04 (starts[5]..starts[6])!
        wahl = load_audio_segment(args.ep02_wind, 1.3, segments[5]["dur"]) * 0.92
        wf_in = int(0.12 * SR)
        wf_out = int(0.18 * SR)
        wenv = np.ones(len(wahl), dtype=np.float64)
        wenv[:wf_in] = np.linspace(0.0, 1.0, wf_in)
        wenv[-wf_out:] = np.linspace(1.0, 0.0, wf_out)
        mix[w0:w0 + len(wahl)] += wahl * wenv[:, None]

        # Subtle eerie ghost-howl punch-in on Take 03 Spiral Hill
        g0 = int(starts[4] * SR)
        ghost = load_audio_segment(args.ep02_spiral, 2.3, segments[4]["dur"]) * 0.34
        mix[g0:g0 + len(ghost)] += ghost

        # Music bed 2 (starts[6] -> end): WAWYS 01:02 MIDNIGHT SAXOPHONE SOLO DROP!
        bed2_len = total_samples - int(starts[6] * SR)
        bed2_dur = bed2_len / SR
        bed2 = load_audio_segment(args.wawys_audio, 62.0, bed2_dur) * 0.78
        b2_env = np.ones(len(bed2), dtype=np.float64)
        b2_in = int(0.15 * SR)
        b2_out = int(1.0 * SR)
        b2_env[:b2_in] = np.linspace(0.15, 1.0, b2_in)
        b2_env[-b2_out:] = np.linspace(1.0, 0.0, b2_out)
        s6 = int(starts[6] * SR)
        mix[s6:s6 + len(bed2)] += bed2 * b2_env[:, None]

        # Layer crisp synthesized *DING!* bells & RenderWin chords at exact comedy beats
        ding = synth_ding(0.65) * 0.72
        win_ch = synth_win_chord(0.75) * 0.68

        def overlay_sfx(buf, sfx, at_sec):
            p0 = int(round(at_sec * SR))
            p1 = min(len(buf), p0 + len(sfx))
            if p0 < len(buf):
                buf[p0:p1] += sfx[: p1 - p0]

        overlay_sfx(mix, ding, starts[1] + 0.35)   # EP-01 Reverse Gear *DING!*
        overlay_sfx(mix, win_ch, starts[2] + 0.08) # EP-01 Parallax Win
        overlay_sfx(mix, ding, starts[3] + 1.20)   # EP-02 Knights of WEE *DING!*
        overlay_sfx(mix, ding, starts[4] + 1.15)   # EP-02 Spiral Hill *DING!*
        overlay_sfx(mix, ding, starts[5] + 0.55)   # EP-02 Chrysler Wind Tunnel *DING!*
        overlay_sfx(mix, win_ch, starts[6] + 0.05) # EP-02 Take 05 Certified Keeper!

        raw_wav = work / "mix_raw.wav"
        write_wav(raw_wav, mix)

        # Final Broadcast Mux + EBU R128 / ITU-R BS.1770 Loudness Normalization (-13.5 LUFS, -1.5 dBTP)
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(video_only),
                "-i", str(raw_wav),
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-af", "loudnorm=I=-13.5:TP=-1.5:LRA=7",
                "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2",
                "-shortest",
                str(out_path),
            ],
            check=True,
        )
        print(f"BUILT TRAILER: {out_path} ({out_path.stat().st_size / 1048576:.2f} MB, {total_dur:.2f}s)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description="Build 1080x1920 24fps Area 33 vertical social trailer.")
    p.add_argument("--welcome-plate", required=True)
    p.add_argument("--outro-plate", required=True)
    p.add_argument("--ep01-sin", required=True)
    p.add_argument("--ep01-win", required=True)
    p.add_argument("--ep02-wee", required=True)
    p.add_argument("--ep02-spiral", required=True)
    p.add_argument("--ep02-wind", required=True)
    p.add_argument("--ep02-win", required=True)
    p.add_argument("--wawys-audio", required=True)
    p.add_argument("--output", required=True)
    build_trailer(p.parse_args())


if __name__ == "__main__":
    main()
