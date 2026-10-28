# NeverRender Labs // Studio Engine & Open-Source Toolkit

**Author:** Matthew Cole Wyatt // [NeverRender Labs](https://renderwithoutcode.com)  
**Architecture:** Deterministic Vision, Headless Commerce Automation, Pure-ASCII Omnisend/MMS Compilers, and Vector Print Foundry.

---

## Directory Architecture

```text
G_AG_FLDR/
├── .agents/skills/                         # Agentic Voice, Anti-Slop & Context Log Skills
│   └── wyatt-nrl-voice-copywriter/
├── 01-vision-and-color-science/
│   ├── luts/                               # 3D .cube LUTs (OCIO v1.4, BEAU_POST, MoebiusTeal, etc.)
│   ├── xmp-calibration/                    # Polynomial & 1D LUT Lightroom .xmp color science engines
│   ├── matting-and-isolation/              # Alpha-matting, studio parchment unification & plinth cleanup
│   └── geometry-rectification/             # Planar homography perspective straighteners for frames & textiles
├── 02-commerce-and-seo-engines/
│   ├── woocommerce-rest/                   # Headless WP/WooCommerce REST media & gallery publishers
│   ├── yoast-double-green/                 # Automated Yoast SEO + Readability double-green auditors
│   └── meta-catalog-bridge/                # Meta Commerce TSV feed compilers & native checkout bridges
├── 03-omnisend-and-mms-foundry/
│   ├── email-circular-compiler/            # Pure-ASCII spam-hardened HTML circular compilers
│   └── mms-bento-and-gif/                  # 9:16 MMS Bento cards, animated GIFs & iOS SMS preview simulators
├── 04-print-and-vector-foundry/
│   ├── business-cards/                     # Pure-Python PostScript Type1 vector PDF business card engine
│   └── executive-resumes/                  # Zero-dependency vector PDF resume compiler
└── 8_BIT_THEATHER_DISTRICT_MEDIA/          # Adobe UXP/JSX pipelines, Foley automation & SRE dashboards
```

## Environment Setup

1. Copy `.env.example` to `.env` and populate your API credentials:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
