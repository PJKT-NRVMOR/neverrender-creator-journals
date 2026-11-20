#!/usr/bin/env python3
"""
NeverRender Labs // Area 33 Episode 03 Instagram Story Teaser Compiler (1080x1920, 24fps)
Builds a single-card Instagram Story teaser for Episode 03 (Super Dross: Russian Blair d'Etat)
with IG Story UI safe zones (top >= 245px, bottom <= 1620px), Pillow RGBA D-Suite HUD overlays,
synthesized metallic *DING!* bells and RenderWin chord, Overdrive synth beat-drop sync,
actual Big-Block V8 audio punch-in, and a corner-bracketed Link Sticker Landing Bay.
"""

import argparse
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


FONT_HERO = load_font(["impact.ttf", "bahnschrift.ttf", "arialbd.ttf"], 72)
FONT_TITLE = load_font(["bahnschrift.ttf", "segoeuib.ttf", "arialbd.ttf"], 54)
FONT_SUB = load_font(["consolab.ttf", "consola.ttf", "arialbd.ttf"], 30)
FONT_MONO = load_font(["consolab.ttf", "consola.ttf"], 26)
FONT_MONO_SM = load_font(["consolab.ttf", "consola.ttf"], 23)
FONT_CTA = load_font(["consolab.ttf", "consola.ttf", "segoeuib.ttf"], 31)
FONT_URL = load_font(["consolab.ttf", "consola.ttf"], 27)


def draw_centered_text(draw, y, text, font, fill, shadow=(0, 0, 0, 220), offset=3):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    if shadow:
        draw.text((x + offset, y + offset), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def wrap_lines(draw, text, font, max_w, max_lines=2):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:max_lines]


def draw_corner_brackets(draw, x0, y0, x1, y1, arm=34, width=5, color=(44, 229, 246, 255)):
    # Top-left
    draw.line([(x0, y0 + arm), (x0, y0), (x0 + arm, y0)], fill=color, width=width)
    # Top-right
    draw.line([(x1 - arm, y0), (x1, y0), (x1, y0 + arm)], fill=color, width=width)
    # Bottom-left
    draw.line([(x0, y1 - arm), (x0, y1), (x0 + arm, y1)], fill=color, width=width)
    # Bottom-right
    draw.line([(x1 - arm, y1), (x1, y1), (x1, y1 - arm)], fill=color, width=width)


def build_story_hud_overlay(
    out_path,
    counter_text,
    counter_mode,
    kicker,
    headline,
    subline,
    footer_url="RENDERWITHOUTCODE.COM/AREA-33/EP-03",
    is_outro=False,
    is_hook=False,
):
    """Render a 1080x1920 RGBA HUD tuned specifically for Instagram Stories safe zones."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top vignette (protects IG Story header + our y=250 telemetry pill)
    for row in range(0, 420):
        alpha = int(190 * (1.0 - row / 420.0) ** 1.5)
        draw.line([(0, row), (W, row)], fill=(5, 10, 15, alpha))

    # Bottom vignette (heavier on outro so the Link Sticker Bay pops cleanly)
    bot_span = 980 if is_outro else 660
    bot_max = 238 if is_outro else 225
    for row in range(H - bot_span, H):
        t = (row - (H - bot_span)) / float(bot_span)
        alpha = int(bot_max * (t ** 1.25))
        draw.line([(0, row), (W, row)], fill=(5, 10, 15, alpha))

    if counter_mode == "sin":
        accent = (255, 92, 102, 255)
        pill_bg = (42, 10, 17, 232)
        badge_txt = (255, 152, 160, 255)
        border_col = (255, 92, 102, 215)
    elif counter_mode == "win":
        accent = (0, 255, 136, 255)
        pill_bg = (7, 38, 29, 236)
        badge_txt = (128, 255, 196, 255)
        border_col = (0, 255, 136, 195)
    elif counter_mode == "outro":
        accent = (255, 107, 43, 255)
        pill_bg = (10, 24, 34, 238)
        badge_txt = (44, 229, 246, 255)
        border_col = (255, 107, 43, 220)
    else:
        accent = (255, 107, 43, 255)
        pill_bg = (8, 25, 35, 234)
        badge_txt = (44, 229, 246, 255)
        border_col = (44, 229, 246, 195)

    # 1. Top Telemetry Pill strictly BELOW IG Story username bar (y=252..326)
    pill_w, pill_h = 880, 74
    px0 = (W - pill_w) // 2
    py0 = 252
    draw.rounded_rectangle(
        [px0, py0, px0 + pill_w, py0 + pill_h],
        radius=8,
        fill=pill_bg,
        outline=accent,
        width=3,
    )
    draw.rectangle([px0 + 22, py0 + 26, px0 + 44, py0 + 48], fill=accent)
    draw.text((px0 + 60, py0 + 21), counter_text, font=FONT_SUB, fill=(246, 252, 255, 255))

    # 2. Main Story Glass Plaque
    card_x0, card_x1 = 64, W - 64
    head_font = FONT_HERO if (is_outro or is_hook) else FONT_TITLE
    max_w = (card_x1 - card_x0) - 64
    lines = wrap_lines(draw, headline, head_font, max_w, max_lines=2)
    sub_lines = wrap_lines(draw, subline, FONT_MONO_SM, max_w, max_lines=2) if subline else []

    line_step = 78 if (is_outro or is_hook) else 62
    sub_step = 32
    content_h = 22 + 38 + len(lines) * line_step + len(sub_lines) * sub_step + 22

    # Anchor higher on Outro to open up a dedicated Link Sticker Landing Bay below it
    card_y1 = 1225 if is_outro else 1538
    card_y0 = card_y1 - content_h

    draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1],
        radius=10,
        fill=(7, 21, 31, 232),
        outline=border_col,
        width=2,
    )
    draw.rectangle([card_x0, card_y0 + 2, card_x0 + 10, card_y1 - 2], fill=accent)

    y_cur = card_y0 + 20
    draw.text((card_x0 + 34, y_cur), kicker, font=FONT_MONO, fill=badge_txt)
    y_cur += 38

    for ln in lines:
        draw.text((card_x0 + 34, y_cur), ln, font=head_font, fill=(255, 255, 255, 255))
        y_cur += line_step

    for sl in sub_lines:
        draw.text((card_x0 + 34, y_cur + 2), sl, font=FONT_MONO_SM, fill=(198, 228, 238, 255))
        y_cur += sub_step

    if is_outro:
        # 3A. Glowing Link-Sticker Prompt Banner + Chevrons (y=1255..1345)
        draw.rounded_rectangle(
            [118, 1255, W - 118, 1315],
            radius=6,
            fill=(255, 107, 43, 240),
            outline=(255, 165, 110, 255),
            width=2,
        )
        draw_centered_text(
            draw,
            1269,
            "TAP LINK BELOW FOR FREE PROMPT + FULL POST",
            FONT_CTA,
            (8, 22, 31, 255),
            shadow=None,
        )
        draw_centered_text(
            draw,
            1326,
            "v      v      v",
            FONT_SUB,
            (44, 229, 246, 255),
            shadow=(0, 0, 0, 220),
        )

        # 3B. Clean Corner-Bracketed IG Link Sticker Landing Bay (y=1375..1525)
        bx0, by0, bx1, by1 = 185, 1375, W - 185, 1525
        draw.rounded_rectangle(
            [bx0, by0, bx1, by1],
            radius=12,
            fill=(6, 18, 28, 175),
            outline=(44, 229, 246, 110),
            width=2,
        )
        draw_corner_brackets(draw, bx0, by0, bx1, by1, arm=36, width=5, color=(44, 229, 246, 255))

        # 3C. Compact URL Signature safely above IG Story bottom reply bar (y=1552..1602)
        draw_centered_text(
            draw,
            1556,
            footer_url,
            FONT_URL,
            (215, 236, 244, 245),
            shadow=(0, 0, 0, 230),
        )
    else:
        # Compact bottom signature strip above IG Story bottom reply bar (y=1558..1612)
        draw.rounded_rectangle(
            [180, 1558, W - 180, 1610],
            radius=6,
            fill=(9, 28, 39, 225),
            outline=(255, 107, 43, 225),
            width=2,
        )
        draw_centered_text(
            draw,
            1570,
            footer_url,
            FONT_URL,
            (255, 255, 255, 255),
            shadow=None,
        )

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


def synth_win_chord(duration=0.78):
    t = np.linspace(0, duration, int(SR * duration), endpoint=False, dtype=np.float64)
    sig = np.zeros_like(t)
    notes = [(523.25, 0.00), (659.25, 0.055), (783.99, 0.11), (1046.50, 0.165)]
    for freq, delay in notes:
        mask = t >= delay
        dt = np.where(mask, t - delay, 0.0)
        env = np.where(mask, np.minimum(1.0, dt / 0.012) * np.exp(-5.6 * dt), 0.0)
        tone = 0.28 * (np.sin(2 * np.pi * freq * dt) + 0.25 * np.sin(2 * np.pi * 2 * freq * dt))
        sig += tone * env
    return np.stack([sig, sig], axis=1)


def load_audio_segment(path, start_sec, dur_sec):
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


def render_still_clip(img_path, overlay_path, dur_sec, out_mp4, zoom_start=1.0, zoom_end=1.07):
    frames = int(round(dur_sec * FPS))
    zoom_expr = f"{zoom_start:.4f}+({zoom_end - zoom_start:.4f})*on/{max(frames - 1, 1)}"
    vf = (
        f"[0:v]scale=1296:2304:force_original_aspect_ratio=increase:flags=lanczos,crop=1296:2304,setsar=1,"
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
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            str(out_mp4),
        ],
        check=True,
    )


def render_video_clip(src_mp4, start_sec, dur_sec, overlay_path, out_mp4):
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
            "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            str(out_mp4),
        ],
        check=True,
    )


def build_story(args):
    work = Path(tempfile.mkdtemp(prefix="area33_ep03_story_"))
    try:
        segments = [
            # 0: Cold Open Explosive Hook (2.4s) - Immediate V8 redline whip-pan off skyline
            {
                "kind": "video",
                "src": Path(args.beau_finale),
                "start": 0.0,
                "dur": 2.4,
                "counter": "AREA 33 // EP-03 DECLASSIFIED",
                "mode": "intro",
                "kicker": "NEVERRENDER LABS // THE RINDER-FILES",
                "headline": "HOW WE FORCED AI TO 360 DRIFT",
                "subline": "5 GLORIOUS FAILS + FREE OPEN-SOURCE PROMPT",
                "is_hook": True,
                "is_outro": False,
            },
            # 1: SIN #01 Pushmi-Pullyu Turntable (2.6s)
            {
                "kind": "video",
                "src": Path(args.sin_pushmi),
                "start": 2.0,
                "dur": 2.6,
                "counter": "SINS: 001 *DING!*  //  FROZEN HORIZON",
                "mode": "sin",
                "kicker": "ACT 01 // RENDERSIN #01",
                "headline": "THE LAZY-SUSAN TURNTABLE",
                "subline": "SKYLINE FROZE WHILE SUPER DROSS SPUN IN PLACE",
                "is_hook": False,
                "is_outro": False,
            },
            # 2: SIN #02 Force Ghost Morph (2.4s)
            {
                "kind": "video",
                "src": Path(args.sin_ghost),
                "start": 2.0,
                "dur": 2.4,
                "counter": "SINS: 002 *DING!*  //  PHASE-SHIFT FAIL",
                "mode": "sin",
                "kicker": "ACT 02 // RENDERSIN #02",
                "headline": "THE FORCE GHOST MORPH",
                "subline": "NOSE DISSOLVED INTO A TRUNK (AND GAVE US OUR PLATE)",
                "is_hook": False,
                "is_outro": False,
            },
            # 3: SIN #03 Spontaneous Mutant Side-Pipe Flamethrower (3.0s)
            {
                "kind": "video",
                "src": Path(args.sin_sidepipe),
                "start": 3.0,
                "dur": 3.0,
                "counter": "SINS: 003 *DING!*  //  ROGER THAT, BOSS",
                "mode": "sin",
                "kicker": "ACT 06 // RENDERSIN #05",
                "headline": "SPONTANEOUS MUTANT SIDE-PIPE",
                "subline": "ASKED FOR BACKFIRE -> SPROUTED A NEW EXHAUST",
                "is_hook": False,
                "is_outro": False,
            },
            # 4: WIN #01 270-Degree Russian Arm Orbit (3.8s) - HITS RIGHT ON OVERDRIVE BEAT DROP!
            {
                "kind": "video",
                "src": Path(args.win_orbit),
                "start": 1.4,
                "dur": 3.8,
                "counter": "SINS: 000 // PROTOCOL LOCKED",
                "mode": "win",
                "kicker": "ACT 04 // RENDERWIN // NATIVE 720P CLEAN SCALE",
                "headline": "THE 270-DEG RUSSIAN ARM WIN",
                "subline": "HARVESTED PLATE -> REAL 3D SKYLINE PARALLAX",
                "is_hook": False,
                "is_outro": False,
            },
            # 5: GRAND FINALE Beau's 14s 360 Eggbeater Climax (7.6s) - REAL V8 ROAR + CLUTCH KICK!
            {
                "kind": "video",
                "src": Path(args.beau_finale),
                "start": 6.2,
                "dur": 7.6,
                "counter": "SINS: 000 // KING CROWNED!",
                "mode": "win",
                "kicker": "ACT 07 // GRAND FINALE (ACTUAL AUDIO ON!)",
                "headline": "14-SECOND 360 EGGBEATER",
                "subline": "ZERO CRANES // ZERO SIDE-PIPES // PURE BOOST",
                "is_hook": False,
                "is_outro": False,
            },
            # 6: Dedicated Instagram Story Link-Sticker End Card (4.4s)
            {
                "kind": "still",
                "src": Path(args.outro_plate),
                "dur": 4.4,
                "zoom": (1.00, 1.07),
                "counter": "AREA 33 // EP-03: RUSSIAN BLAIR D'ETAT",
                "mode": "outro",
                "kicker": "OPEN-SOURCE WORKFLOW // STEAL THE EXACT PROMPT",
                "headline": "READ THE FULL TEARDOWN",
                "subline": "7 PLAYABLE TAKES + EXPORT FORENSICS + PROTOCOL",
                "is_hook": False,
                "is_outro": True,
            },
        ]

        part_paths = []
        starts = []
        t_cursor = 0.0
        for idx, seg in enumerate(segments):
            starts.append(t_cursor)
            ov = work / f"ov_{idx:02d}.png"
            build_story_hud_overlay(
                ov,
                counter_text=seg["counter"],
                counter_mode=seg["mode"],
                kicker=seg["kicker"],
                headline=seg["headline"],
                subline=seg["subline"],
                is_outro=seg["is_outro"],
                is_hook=seg["is_hook"],
            )
            part = work / f"part_{idx:02d}.mp4"
            if seg["kind"] == "still":
                render_still_clip(seg["src"], ov, seg["dur"], part, seg["zoom"][0], seg["zoom"][1])
            else:
                render_video_clip(seg["src"], seg["start"], seg["dur"], ov, part)
            part_paths.append(part)
            t_cursor += seg["dur"]

            # Save static Story End-Card Cover JPEG if requested
            if seg["is_outro"] and args.cover_out:
                cover_path = Path(args.cover_out)
                cover_path.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-v", "error",
                        "-ss", "1.5", "-i", str(part),
                        "-vframes", "1", "-q:v", "2",
                        str(cover_path),
                    ],
                    check=True,
                )

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

        # Overdrive Synth Bed synced so music t=15.0s massive beat drop hits EXACTLY at starts[4] (10.4s)!
        music_offset = 15.0 - starts[4]  # 4.60s
        bed = load_audio_segment(args.music_bed, music_offset, total_dur)
        env = np.full(len(bed), 0.56, dtype=np.float64)

        # Gentle 0.18s cold-open fade-in
        fi = int(0.18 * SR)
        env[:fi] = np.linspace(0.18, 0.56, fi)

        # Surge synth up on Beat Drop (starts[4] -> starts[5])
        s4 = int(round(starts[4] * SR))
        s5 = int(round(starts[5] * SR))
        s6 = int(round(starts[6] * SR))
        env[s4:s5] = 0.72

        # Duck synth smoothly under Beau's screaming V8 Finale (starts[5] -> starts[6])
        ramp = int(0.22 * SR)
        env[s5:s5 + ramp] = np.linspace(0.72, 0.34, ramp)
        env[s5 + ramp:s6] = 0.34

        # Swell synth back up for Link-Sticker Outro (starts[6] -> end), then smooth 0.9s fade-out
        env[s6:s6 + ramp] = np.linspace(0.34, 0.74, ramp)
        env[s6 + ramp:] = 0.74
        fo = int(0.90 * SR)
        env[-fo:] *= np.linspace(1.0, 0.0, fo)

        mix += bed * env[:, None]

        # Cold-open V8 launch roar punch-in (Seg 0: 0.0 -> 2.4s)
        hook_v8 = load_audio_segment(args.beau_finale, 0.0, segments[0]["dur"]) * 0.42
        h_env = np.ones(len(hook_v8), dtype=np.float64)
        h_env[-int(0.18 * SR):] = np.linspace(1.0, 0.0, int(0.18 * SR))
        mix[:len(hook_v8)] += hook_v8 * h_env[:, None]

        # Mutant Side-Pipe backfire audio pop punch-in (Seg 3: starts[3]..starts[4])
        sp_aud = load_audio_segment(args.sin_sidepipe, 3.0, segments[3]["dur"]) * 0.48
        sp_env = np.ones(len(sp_aud), dtype=np.float64)
        sp_env[:int(0.15 * SR)] = np.linspace(0.0, 1.0, int(0.15 * SR))
        sp_env[-int(0.18 * SR):] = np.linspace(1.0, 0.0, int(0.18 * SR))
        s3 = int(round(starts[3] * SR))
        mix[s3:s3 + len(sp_aud)] += sp_aud * sp_env[:, None]

        # Real screaming Big-Block V8 + clutch-kick tire-shredding Finale audio (Seg 5)
        v8_fin = load_audio_segment(args.beau_finale, 6.2, segments[5]["dur"]) * 0.88
        v8_env = np.ones(len(v8_fin), dtype=np.float64)
        v8_env[:int(0.16 * SR)] = np.linspace(0.0, 1.0, int(0.16 * SR))
        v8_env[-int(0.28 * SR):] = np.linspace(1.0, 0.0, int(0.28 * SR))
        mix[s5:s5 + len(v8_fin)] += v8_fin * v8_env[:, None]

        # Layer metallic *DING!* bells & RenderWin chords on exact visual beats
        ding = synth_ding(0.65) * 0.74
        win_ch = synth_win_chord(0.78) * 0.70

        def overlay_sfx(buf, sfx, at_sec):
            p0 = int(round(at_sec * SR))
            p1 = min(len(buf), p0 + len(sfx))
            if p0 < len(buf):
                buf[p0:p1] += sfx[: p1 - p0]

        overlay_sfx(mix, ding, starts[1] + 0.55)    # Pushmi-Pullyu *DING!*
        overlay_sfx(mix, ding, starts[2] + 0.65)    # Force Ghost *DING!*
        overlay_sfx(mix, ding, starts[3] + 1.60)    # Mutant Side-Pipe flame eruption *DING!*
        overlay_sfx(mix, win_ch, starts[4] + 0.05)  # 270-Deg Russian Arm Win + Beat Drop!
        overlay_sfx(mix, win_ch, starts[5] + 0.04)  # 14s Big-Block Bounce-Back Crown!

        raw_wav = work / "mix_raw.wav"
        write_wav(raw_wav, mix)

        # Broadcast Instagram Story Master (-13.5 LUFS, -1.5 dBTP, bt709 color lock, faststart)
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg", "-y", "-v", "error",
                "-i", str(video_only),
                "-i", str(raw_wav),
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "libx264", "-profile:v", "high", "-level:v", "4.1",
                "-preset", "slow", "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-movflags", "+faststart",
                "-af", "loudnorm=I=-13.5:TP=-1.5:LRA=7",
                "-c:a", "aac", "-b:a", "256k", "-ar", str(SR), "-ac", "2",
                "-shortest",
                str(out_path),
            ],
            check=True,
        )
        print(f"BUILT IG STORY: {out_path} ({out_path.stat().st_size / 1048576:.2f} MB, {total_dur:.2f}s)")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description="Build 1080x1920 24fps Area 33 Episode 03 Instagram Story Teaser.")
    p.add_argument("--sin-pushmi", required=True)
    p.add_argument("--sin-ghost", required=True)
    p.add_argument("--sin-sidepipe", required=True)
    p.add_argument("--win-orbit", required=True)
    p.add_argument("--beau-finale", required=True)
    p.add_argument("--outro-plate", required=True)
    p.add_argument("--music-bed", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--cover-out", default="")
    build_story(p.parse_args())


if __name__ == "__main__":
    main()
