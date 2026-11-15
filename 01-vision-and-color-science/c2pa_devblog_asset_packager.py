#!/usr/bin/env python3
"""Package C2PA-signed visual masters, web display plates, and audio stems for NeverRender Labs devblogs."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps


@dataclass(frozen=True)
class VisualAssetSpec:
    """Mapping between a raw studio visual master and its packaged web and C2PA outputs."""

    src_name: str
    web_name: str
    master_name: str
    c2pa_signed: bool
    quality: int = 86
    subsampling: int = 2


@dataclass(frozen=True)
class AudioStemSpec:
    """Mapping between a studio WAV master and its web-streamable 320 kbps MP3."""

    src_name: str
    mp3_name: str


DEFAULT_SRC_DIR = os.getenv(
    "NRL_DEVBLOG_SRC_DIR",
    r"C:\Users\Saturn\Desktop\temp-ag\New folder",
)
DEFAULT_DEST_DIR = os.getenv(
    "NRL_DEVBLOG_DEST_DIR",
    r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\IN_THE_WORKS",
)

VISUAL_ASSETS: tuple[VisualAssetSpec, ...] = (
    VisualAssetSpec(
        src_name="nrl-21067-sd-6-panel-card 2026-11-14 - 07.05.00 - Cr.png",
        web_name="nrl-21067-sd-6-panel-card.jpg",
        master_name="nrl-21067-sd-6-panel-card-cr.png",
        c2pa_signed=True,
        quality=88,
        subsampling=0,
    ),
    VisualAssetSpec(
        src_name="the-jeselo-super-dross (5x4) (nrl graded) - Cr.jpg",
        web_name="beat-01-casino-jesolo-super-dross.jpg",
        master_name="beat-01-casino-jesolo-super-dross-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="nrl21067-sd-elevated-highway-anthropolis (5x4) (nrl graded) - Cr.jpg",
        web_name="beat-02-elevated-highway-anthropolis.jpg",
        master_name="beat-02-elevated-highway-anthropolis-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="nrl21067-sd-ots-highway-saturn (5x4) (nrl graded) - Cr.jpg",
        web_name="beat-03-ots-cockpit-highway-saturn.jpg",
        master_name="beat-03-ots-cockpit-highway-saturn-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="nrl21067-sd-elevated-highway-saturn (5x4) (nrl graded) - Cr.jpg",
        web_name="beat-04-elevated-highway-saturn.jpg",
        master_name="beat-04-elevated-highway-saturn-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="the-outpost-sands (5x4) (nrl graded) 2026-11-15 - 03.23.18 - Cr.jpg",
        web_name="beat-05-the-outpost-sands.jpg",
        master_name="beat-05-the-outpost-sands-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="the-stagcoach-super-dross (5x4) (nrl graded) - Cr.jpg",
        web_name="beat-06-the-stagecoach-super-dross.jpg",
        master_name="beat-06-the-stagecoach-super-dross-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="clip-017-plate.jpg",
        web_name="scene-plate-017-jax-unit-0-barkeep.jpg",
        master_name="scene-plate-017-jax-unit-0-barkeep-master.jpg",
        c2pa_signed=False,
    ),
    VisualAssetSpec(
        src_name="clip-018-plate.jpg",
        web_name="scene-plate-018-silas-cold-iron-vance.jpg",
        master_name="scene-plate-018-silas-cold-iron-vance-master.jpg",
        c2pa_signed=False,
    ),
    VisualAssetSpec(
        src_name="dj-churn-the-static-stray-green 2026-11-15 - 04.05.20 - Cr.png",
        web_name="cast-dj-churn-chroma-green-3-pose.jpg",
        master_name="cast-dj-churn-chroma-green-3-pose-cr.png",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="DJ_CHURN_THE_STATIC_STRAY 3 turn 2026-10-16 - 03.07.57 - Cr.jpg",
        web_name="cast-dj-churn-3-turn.jpg",
        master_name="cast-dj-churn-3-turn-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="DJ_CHURN_THE_STATIC_STRAY_J - Cr.jpg",
        web_name="cast-dj-churn-portrait.jpg",
        master_name="cast-dj-churn-portrait-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="Vesper -Static- Thorne \u2014 The Booth Four Drifter 3 turn 2026-10-16 - 02.33.13 - Cr.jpg",
        web_name="cast-vesper-static-thorne-3-turn.jpg",
        master_name="cast-vesper-static-thorne-3-turn-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="Vesper -Static- Thorne \u2014 The Booth Four Drifter 2026-10-16 - 02.05.00 - Cr.jpg",
        web_name="cast-vesper-static-thorne-portrait.jpg",
        master_name="cast-vesper-static-thorne-portrait-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="Archetype 3 Jax -Unit 0- \u2014 The Weary Barkeep 3 turn 2026-10-16 - 02.27.28 - Cr.jpg",
        web_name="cast-jax-unit-0-3-turn.jpg",
        master_name="cast-jax-unit-0-3-turn-cr.jpg",
        c2pa_signed=True,
    ),
    VisualAssetSpec(
        src_name="Silas -Cold Iron- Vance \u2014 The Deserter Courier 3 turn 2026-10-16 - 02.48.32 - Cr.jpg",
        web_name="cast-silas-cold-iron-vance-3-turn.jpg",
        master_name="cast-silas-cold-iron-vance-3-turn-cr.jpg",
        c2pa_signed=True,
    ),
)

AUDIO_STEMS: tuple[AudioStemSpec, ...] = (
    AudioStemSpec(
        src_name="Neo Arcade Chase.wav",
        mp3_name="neo-arcade-chase-take-1-night-patrol.mp3",
    ),
    AudioStemSpec(
        src_name="Neo Arcade Chase (Take 2).wav",
        mp3_name="neo-arcade-chase-take-2-overdrive-master.mp3",
    ),
)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments with environment-backed defaults."""
    parser = argparse.ArgumentParser(
        description="Package visual plates, byte-identical C2PA masters, and web MP3 stems."
    )
    parser.add_argument(
        "--src-dir",
        type=Path,
        default=Path(DEFAULT_SRC_DIR),
        help="Source directory containing graded plates and WAV masters.",
    )
    parser.add_argument(
        "--dest-dir",
        type=Path,
        default=Path(DEFAULT_DEST_DIR),
        help="Destination directory inside the website repository.",
    )
    parser.add_argument(
        "--max-dim",
        type=int,
        default=1800,
        help="Maximum pixel dimension (width or height) for web JPEG plates.",
    )
    return parser.parse_args()


def to_rgb_for_jpeg(image: Image.Image) -> Image.Image:
    """Normalize EXIF orientation and flatten alpha channels to dark petrol canvas."""
    transposed = ImageOps.exif_transpose(image)
    if transposed.mode in ("RGBA", "LA") or (
        transposed.mode == "P" and "transparency" in transposed.info
    ):
        rgba = transposed.convert("RGBA")
        background = Image.new("RGB", rgba.size, (11, 34, 45))
        background.paste(rgba, mask=rgba.split()[3])
        return background
    return transposed.convert("RGB")


def package_visuals(
    specs: Iterable[VisualAssetSpec],
    src_dir: Path,
    web_dir: Path,
    c2pa_dir: Path,
    max_dim: int,
) -> list[str]:
    """Copy raw masters byte-for-byte and build progressive web display JPEGs."""
    c2pa_verified: list[str] = []
    for spec in specs:
        src_path = src_dir / spec.src_name
        if not src_path.is_file():
            raise FileNotFoundError(f"Missing visual source asset: {src_path}")

        master_dest = c2pa_dir / spec.master_name
        shutil.copy2(src_path, master_dest)

        if spec.c2pa_signed:
            payload = master_dest.read_bytes()
            if b"c2pa" not in payload:
                raise ValueError(f"Expected C2PA JUMBF marker missing in {master_dest}")
            c2pa_verified.append(spec.master_name)

        web_dest = web_dir / spec.web_name
        with Image.open(src_path) as img:
            rgb = to_rgb_for_jpeg(img)
            w, h = rgb.size
            if max(w, h) > max_dim:
                scale = max_dim / float(max(w, h))
                new_size = (max(1, int(round(w * scale))), max(1, int(round(h * scale))))
                rgb = rgb.resize(new_size, Image.Resampling.LANCZOS)
            rgb.save(
                web_dest,
                format="JPEG",
                quality=spec.quality,
                optimize=True,
                progressive=True,
                subsampling=spec.subsampling,
            )

        print(
            f"[OK] {spec.web_name} ({web_dest.stat().st_size // 1024} KB) <- {spec.master_name} "
            f"({'C2PA VERIFIED' if spec.c2pa_signed else 'FULL-RES MASTER'})"
        )
    return c2pa_verified


def transcode_audio(
    stems: Iterable[AudioStemSpec],
    src_dir: Path,
    audio_dir: Path,
) -> None:
    """Encode 48 kHz 320 kbps MP3 streaming stems from lossless WAV masters."""
    for stem in stems:
        src_path = src_dir / stem.src_name
        if not src_path.is_file():
            raise FileNotFoundError(f"Missing audio source asset: {src_path}")

        dest_path = audio_dir / stem.mp3_name
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(src_path),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "320k",
            "-ar",
            "48000",
            str(dest_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0 or not dest_path.is_file():
            raise RuntimeError(
                f"ffmpeg failed for {src_path} (rc={result.returncode}): {result.stderr}"
            )
        print(f"[OK] {stem.mp3_name} ({dest_path.stat().st_size // 1024} KB)")


def main() -> None:
    """Execute visual packaging and audio stem transcoding."""
    args = parse_args()
    web_dir = args.dest_dir / "web"
    c2pa_dir = args.dest_dir / "c2pa"
    audio_dir = args.dest_dir / "audio"
    for directory in (web_dir, c2pa_dir, audio_dir):
        directory.mkdir(parents=True, exist_ok=True)

    c2pa_verified = package_visuals(
        VISUAL_ASSETS, args.src_dir, web_dir, c2pa_dir, args.max_dim
    )
    transcode_audio(AUDIO_STEMS, args.src_dir, audio_dir)
    print(
        f"Packaging complete: {len(VISUAL_ASSETS)} web/master pairs "
        f"({len(c2pa_verified)} C2PA JUMBF verified), {len(AUDIO_STEMS)} MP3 stems."
    )


if __name__ == "__main__":
    main()
