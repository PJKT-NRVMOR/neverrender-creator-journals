# Project Marshall College & NeverRender Labs - Agent Rules

## 0. Mandatory Response Timestamp Header (`HH:MM:SS-YYYY-MM-DD`)

- You **MUST** begin **every** chat response to the user with the current 24-hour local time and date formatted as `HH:MM:SS-YYYY-MM-DD` (for example: `15:43:36-2026-10-24`) on the very first line before any other text.

## 1. Always-On Voice & Copywriting Standards (`wyatt-nrl-voice-copywriter` & `melissa-tone-copywriter`)

### A. Matthew Wyatt // NeverRender Labs Voice (`wyatt-nrl-voice-copywriter`)
Whenever drafting, editing, or sanitizing copy, client updates, executive summaries, technical proposals, devlogs, or scripts on behalf of **Matthew Cole Wyatt** or **NeverRender Labs**, you **MUST** follow [`wyatt-nrl-voice-copywriter`](./.agents/skills/wyatt-nrl-voice-copywriter/SKILL.md) and its living corpus at [`wyatt-voice-corpus.md`](./.agents/skills/wyatt-nrl-voice-copywriter/references/wyatt-voice-corpus.md):
- **Zero Em-Dashes (`—`) or En-Dashes (`–`)** anywhere in prose, bullet lists, email subjects, or table cells. Use commas, colons, parentheses, or standard ASCII hyphens (`-`) / double-slashes (`//`).
- **Zero Bracketed Citations or NotebookLM Artifacts** (`[1]`, `[2]`, `[cite: 1]`).
- **Zero Corporate AI Buzzwords** ("delve", "testament to", "tapestry", "symphony", "unlock", "elevate", "game-changer", etc.).
- **Route by Operational Register**:
  - *Register 1*: Unfiltered Creator & Studio Banter (`@NeverRenderLabs`, devlogs, Tron Grid / CinemaSins dry wit).
  - *Register 2*: Consultative Client Architect (calm authority, plain-English translation of True Delivered % vs. Raw Sent, explicit sign-off gates, 30-second install guides).
  - *Register 3*: Commercial Prospectus, SOW & Invoice (`NRL-TCC-2026-XXX`, decimal hour ledgers, 100% Client Data Sovereignty).
  - *Register 4*: Forensic Advocacy & Care Coordination.

### B. Melissa Chapman // The Chapman Collection Voice (`melissa-tone-copywriter`)
Whenever drafting, editing, or reviewing any client-facing copy for **The Chapman Collection** or **Melissa Chapman** (newsletters, flyers, website copy, product descriptions, Chairish/Etsy/Instagram posts, or client correspondence), you **MUST** follow [`melissa-tone-copywriter`](./.agents/skills/melissa-tone-copywriter/SKILL.md) and its living corpus at [`voice-corpus.md`](./.agents/skills/melissa-tone-copywriter/references/voice-corpus.md):
- **Zero Em-Dashes (`—`) or En-Dashes (`–`)** anywhere in prose.
- **No Serial / Oxford Comma** before `and` in simple lists (e.g., *"celebrities, politicians and even royalty"*, *"history, craftsmanship and beauty"*).
- **Warm, understated British-California elegance**: Grounded in her Harrington Road (London) roots and Rancho Santa Fe showroom (`6014 La Granada, Rancho Santa Fe, CA 92067`).
- **Short, balanced 2-sentence paragraphs** with gracious, low-pressure hospitality.

## 2. Automatic Multimodal Communication Ingestion

Whenever the user shares **any** new communication from **Matthew Wyatt** or **Melissa Chapman** (emails, Word/Docx redlines, SMS/RCS screenshots, audio recordings/voice notes, chat logs, or video walkthroughs), you **MUST** automatically:
- Inspect/transcribe the communication to extract exact phrasing, word substitutions, technical/aesthetic preferences, and spoken cadence.
- Append those newly observed phrases and takeaways into [`wyatt-voice-corpus.md`](./.agents/skills/wyatt-nrl-voice-copywriter/references/wyatt-voice-corpus.md) or [`voice-corpus.md`](./.agents/skills/melissa-tone-copywriter/references/voice-corpus.md) so both voice profiles continuously sharpen over time.

## 3. Mandatory Two-Tree Git Governance & Automatic Code Harvesting

Whenever you write or run any new Python script, tool, HTML compiler, color/vision pipeline, or automation utility, you **MUST** persist and commit it into the appropriate Git repository tree (instead of leaving it only in `scratch/`):
1. **Tree 1 (`c:\Users\Saturn\Desktop\G_AG_FLDR` — NeverRender Labs Open-Source Studio Toolkit)**:
   - Place reusable, client-agnostic scripts under:
     - `01-vision-and-color-science/` (`luts/`, `xmp-calibration/`, `matting-and-isolation/`, `geometry-rectification/`)
     - `02-commerce-and-seo-engines/` (`woocommerce-rest/`, `yoast-double-green/`, `meta-catalog-bridge/`)
     - `03-omnisend-and-mms-foundry/` (`email-circular-compiler/`, `mms-bento-and-gif/`)
     - `04-print-and-vector-foundry/` (`business-cards/`, `executive-resumes/`)
   - **Zero Secrets / Zero Client PII**: Always read credentials via `os.getenv()` (never hardcode API keys or passwords).
   - Stage, commit, and push (`git push origin main` once remote is linked) after completing any feature or tool build.
2. **Tree 2 (`c:\Users\Saturn\Desktop\project-marshall-college` — Project Marshall College Private Operations Repo)**:
   - Place client-specific scripts under `scripts/` (`campaigns-and-circulars/`, `woocommerce-and-yoast/`, `meta-commerce-and-feeds/`, `database-and-etl/`) and campaign deliverables under `project-marshall-college/04-campaigns-outreach-drops/`.
   - **100% Client Data Sovereignty**: Never stage or commit `.env`, customer contact spreadsheets (`*.csv`, `*.xlsx`, `*.tsv`), or raw showroom media dumps. Stage, commit, and push (`git push origin main` once remote is linked) after each task.
