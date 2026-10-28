# Nathan Doan Productions // The Automated Ingest & Smart Selects Machine
### Positioning Strategy & Interview Playbook for Matthew Wyatt (Tuesday 12:00 PM)

---

## 1. The Core Problem Nathan Is Facing

Nathan is operating largely solo or with a skeleton crew, looking to **cut production/post costs** while **expanding his narrative universe**.

In video production, the single biggest invisible money-pit and time-sink is **ingest and timeline scrubbing**:
- An actor resets 3 times on take 2, or the camera rolls for 20 seconds before "Action!" and 15 seconds after "Cut!".
- A director or editor has to scrub through 4 hours of raw footage just to mark in/out points, trim dead air, and assemble a "stringout" (selects roll).
- **The Pain**: It drains hours of creative energy, delays assembly edits, and costs hundreds of dollars in assistant editor (AE) hours.

---

## 2. The Pitch: Don't Offer Manual Scrubbing—Offer The "Smart Selects Machine"

> **"Nathan, instead of paying someone to sit in Premiere and manually scrub through 50 raw clips just to cut out dead air and false starts, I've engineered an agent-assisted ingest pipeline for skeleton crews."**

### How It Works (The 3-Step Flow):
1. **Drop Zone (`DROP_ZONE_RAW`)**:
   - Nathan dumps his raw camera files (`.mp4`, `.mov`, ProRes) into a single folder.
2. **Agent Analysis & Smart Dead-Air Stripping**:
   - The engine analyzes each clip at 50x–100x speed.
   - It runs acoustic silence & energy boundary detection to identify exactly when the performance starts and ends.
   - It strips the awkward 10-second pre-roll slating time, director chatter, and post-roll pauses, preserving only the active take with natural breathing room.
3. **Dual Master Delivery (Landscape + 1080p Vertical)**:
   - **`ASSEMBLY_SELECTS_1080P_LANDSCAPE.mp4`**: A single continuous video file containing every cleaned take back-to-back. Nathan can watch ONE file from start to finish and instantly pick his favorite takes.
   - **`ASSEMBLY_SELECTS_1080P_VERTICAL_PORTRAIT.mp4`**: A pristine 1080x1920 (9:16) portrait export with cinematic blurred-wing backfill, formatted immediately for mobile review, Instagram Reels, YouTube Shorts, or TikTok.
   - **`INGEST_DECISION_LOG.md`**: A clean tabular log showing exact in/out timestamps and showing Nathan how much dead air was eliminated (e.g. *35% dead air eliminated*).

---

## 3. Why This Wins the Room on Tuesday

| Traditional Junior Editor Pitch | Matthew Wyatt's Architect Pitch |
| :--- | :--- |
| "I know Premiere shortcuts and I can scrub timelines all night." | "I built an automated pipeline that ingests your raw cards, cuts out the dead air, and gives you a single stitched selects reel in both landscape and 9:16 vertical." |
| Nathan has to manage you and check your cuts clip by clip. | Nathan just drops footage into a folder and gets finished review reels. |
| Cost centers on manual hours ($30–$50/hr). | High-leverage systems engineering that saves Nathan 15+ hours every shoot. |
| High friction for a solo director. | Effortless leverage for a solo director. |

---

## 4. The 60-Second Spoken Elevator Pitch

> *"Nathan, I know you're running lean and want to put every dollar on screen rather than burning budget on manual post-prep. Because I specialize in agentic workflows, I built an automated ingest pipeline:*
>
> *At wrap, your crew drops the raw card into our drop folder. Our system scans every clip, strips out the dead air and resets between takes, and automatically stitches together a single, continuous Selects Reel.*
>
> *Even better, it exports a 1080p Vertical 9:16 mobile version right alongside the master 16:9, so you can review the whole shoot on your phone over lunch or instantly pull shorts and teaser cuts. You don't waste 4 hours scrubbing—you jump straight into creative direction."*

---

## 5. Pro Production Architecture & CLI Controls

The pipeline is built with broadcast & film engineering standards:
- **Locked 48,000 Hz Audio**: Prevents drift, popping, or phase artifacts across mixed camera sources (e.g. 44.1 kHz phone scratch audio vs. 48 kHz wireless lavs).
- **Stream-Copy Concat**: Stitches 1080p landscape master reels in **3 seconds flat** (`-c copy`) with **zero generational loss**.
- **10-bit Log / ProRes 422 Workflow**: Keeps 100% of color grading latitude for Sony S-Log3, Canon C-Log3, or Apple Log using `-c:v prores_ks -profile:v 2 -pix_fmt yuv422p10le`.
- **Uncompressed PCM Audio**: Supports pristine 24-bit broadcast wave audio (`pcm_s24le`) for direct dialogue editing.
- **Tuneable Thresholds**: Exposes noise floor and silence duration flags so Nathan can dial in boundary detection for noisy street shoots vs. treated voice booths.

### CLI Execution Cheat Sheet:
```powershell
# Standard Proxy / Web Review Mode (H.264 + 48kHz AAC)
python ingest_engine.py

# 10-bit Log Studio Mode (Apple ProRes 422 .mov + 24-bit PCM Uncompressed Audio)
python ingest_engine.py --prores

# Noisy Location Shoot (raises threshold to -25dB and 0.5s pause)
python ingest_engine.py --noise -25dB --silence 0.5

# Dry-Run Analysis (generates timing logs without rendering files)
python ingest_engine.py --dry-run
```

- **Pipeline Folder**: `C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\AUTOMATED_INGEST_PIPELINE`
- **Engine Script**: `ingest_engine.py`
- **Drop Zone**: `AUTOMATED_INGEST_PIPELINE\DROP_ZONE_RAW`
- **Output Destination**: `AUTOMATED_INGEST_PIPELINE\EXPORTS_STRINGOUTS`

