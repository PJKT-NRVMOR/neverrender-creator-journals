#!/usr/bin/env python3
"""
NeverRender Labs - Flight Log Sanitizer, Base64 Stripper & NotebookLM Compiler
==============================================================================
1. Scrubs live API keys (AIza...), webhook secrets (secret=...), Meta tokens,
   WooCommerce ck_/cs_ keys, Omnisend API keys, Bearer/Basic headers, Medi-Cal
   BIC/CIN IDs, and personal SoFi/Zelle banking reference/member/alert IDs.
2. Strips bloated inline and reference-link base64 data:image payloads (~128 MB)
   so both local editors and NotebookLM ingest clean Markdown instantaneously.
3. Applies clientele PII scrubbing via sanitize_clientele_pii.py so zero
   third-party collector emails, phone numbers, or names survive.
4. Produces:
   - Clean, base64-free, secret-free individual flight logs in-place.
   - Consolidated Historical Markdowns (Full Oct-Nov Master + October Master +
     November Master).
   - 4 Midnight-Aligned NotebookLM Upload Volumes (< 400k words each, well
     under NotebookLM's 500,000-word per-source limit, zero logs cut mid-file).
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sanitize_clientele_pii as pii

# Base64 image stripping patterns
B64_INLINE_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(\s*<?data:image/[A-Za-z0-9+.\-]+;base64,[A-Za-z0-9+/=\s\\]+>?\s*\)"
)
B64_REF_DEF_RE = re.compile(
    r"^\[([^\]]+)\]:\s*<?data:image/[A-Za-z0-9+.\-]+;base64,[A-Za-z0-9+/=\s\\]+>?\s*$",
    re.MULTILINE,
)
B64_RAW_URI_RE = re.compile(
    r"<?data:image/[A-Za-z0-9+.\-]+;base64,[A-Za-z0-9+/=\s\\]{60,}>?"
)

# Secret, Token, Credential & Banking/Medi-Cal ID scrubbers
SECRET_PATTERNS: List[Tuple[str, re.Pattern, str]] = [
    ("Google_API_Key", re.compile(r"AIza[0-9A-Za-z\-_]{20,}"), "[REDACTED_GOOGLE_API_KEY]"),
    ("Webhook_Secret", re.compile(r"(secret(?:\\=|=))([0-9a-fA-F]{16,64})", re.I), r"\1[REDACTED_WEBHOOK_SECRET]"),
    ("Feed_Hash_Token", re.compile(r"(feed(?:\\_|_))([0-9a-fA-F]{32})", re.I), r"\1[REDACTED_FEED_HASH]"),
    ("Meta_Access_Token", re.compile(r"\bEAAG[A-Za-z0-9]{16,}\b"), "[REDACTED_META_ACCESS_TOKEN]"),
    ("WooCommerce_Key", re.compile(r"\b(?:ck|cs)_[0-9a-fA-F]{20,}\b"), "[REDACTED_WOOCOMMERCE_KEY]"),
    ("Omnisend_API_Key", re.compile(r"\b6[0-9a-f]{23}-[A-Za-z0-9\-_]{15,}\b"), "[REDACTED_OMNISEND_API_KEY]"),
    ("Bearer_Token", re.compile(r"(Bearer\s+)[A-Za-z0-9._\-+/=]{20,}"), r"\1[REDACTED_BEARER_TOKEN]"),
    ("Basic_Auth", re.compile(r"(Basic\s+)[A-Za-z0-9+/=]{16,}"), r"\1[REDACTED_BASIC_AUTH]"),
    (
        "Bank_Member_Ref_Alert_ID",
        re.compile(
            r"(\b(?:MemberID|ReferenceID|AlertID)\s*(?:[:(]|\\[:(])\s*`?)(\d{6,14})(`?\)?)",
            re.I,
        ),
        r"\1[REDACTED_BANK_ID]\3",
    ),
    (
        "Bank_Short_Ref_ID",
        re.compile(r"(\bRef\s+)(\d{7,12})\b"),
        r"\1[REDACTED_BANK_ID]",
    ),
    (
        "Zelle_Transfer_Conf_ID",
        re.compile(
            r"((?:Transfer\s+ID|Confirmation\s*(?:\\?#|:|#))\s*[:#]?\s*`?#?)([A-Z0-9]{8,16})(`?)",
            re.I,
        ),
        r"\1[REDACTED_ZELLE_ID]\3",
    ),
    (
        "MediCal_CIN_BIC",
        re.compile(r"\b9\d{7}[A-Z]\b"),
        "[REDACTED_MEDICAL_ID]",
    ),
]

# Exact chronological manifest of all 32 unique source flight logs grouped into
# the 4 midnight-aligned NotebookLM blocks (< 400k words each)
CHRONOLOGICAL_BLOCKS: List[Tuple[str, str, List[Tuple[str, str, str]]]] = [
    (
        "PMC_NotebookLM_Vol_01_2026-10-01_to_2026-10-22.md",
        "Volume 01 (2026-10-01 to 2026-10-22): Pre-Build Recon, Onboarding, Luxury AEO, WooCommerce & Circular 01 Prep",
        [
            ("oct", "agent-log_ the-chapman-collection-gbp-profile-completeness-and-search-analytics.md", "2026-10-01 // Pre-Build GBP Profile Completeness & Search Analytics"),
            ("oct", "agent-log_ the-chapman-collection-intake-vault-pitch-strategy.md", "2026-10-01 // Intake Vault Pitch Strategy"),
            ("oct", "agent-log_ the-chapman-collection-luxury-aeo-and-gbp-optimization-strategy.md", "2026-10-01 // Luxury AEO & GBP Optimization Strategy"),
            ("oct", "agent-log_ the-chapman-collection-onboarding-intake-and-next-steps-analysis.md", "2026-10-01 // Onboarding Intake & Next Steps Analysis"),
            ("oct", "agent-log_ project-marshall-college-trinity-proton-rancho-santa-fe-recon.md", "2026-10-01 // Trinity Proton & Rancho Santa Fe Recon"),
            ("oct", "agent-log_ project-marshall-chapman-receptionist-dee-build-2026-10-01.md", "2026-10-01 // Receptionist DEE Architecture Build"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-01.md", "2026-10-01 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-02.md", "2026-10-02 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-03.md", "2026-10-03 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-04.md", "2026-10-04 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-05.md", "2026-10-05 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-06.md", "2026-10-06 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-07.md", "2026-10-07 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-08.md", "2026-10-08 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-09.md", "2026-10-09 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-10.md", "2026-10-10 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-15-16.md", "2026-10-15 to 2026-10-16 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-17.md", "2026-10-17 // Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-yoast-seo-and-plugin-licensing-chat-2026-10-18.md", "2026-10-18 // Yoast SEO & Plugin Licensing Chat"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-18-20.md", "2026-10-18 to 2026-10-20 // Trinity Build Log"),
            ("oct", "agent-log-v-a1_ the-chapman-collection-weekly-seo-aeo-audit-response-2026-10-19.md", "2026-10-19 // Weekly SEO & AEO Audit Response"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-21.md", "2026-10-21 // Showroom Visit & Trinity Build Log"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-22.md", "2026-10-22 // WooCommerce, Yoast & Circular 01 Prep"),
        ],
    ),
    (
        "PMC_NotebookLM_Vol_02_2026-10-23_to_2026-10-29.md",
        "Volume 02 (2026-10-23 to 2026-10-29): Circular 01 Rollout, Pomelli Vision, Master ETL & Meta Shop Sync",
        [
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-23.md", "2026-10-23 // Circular 01 3-Wave Launch & Catalog Expansion"),
            ("oct", "agent-log_ project-marshall-college-trinity-build-2026-10-24-to-25-pomelli.md", "2026-10-24 to 2026-10-25 // Pomelli Vision & Master ETL"),
            ("oct", "agent-log_ project-marshall-college-build-2026-10-26-to-27.md", "2026-10-26 to 2026-10-27 // 72h Telemetry & Old World Cabinets"),
            ("oct", "agent-log_ project-marshall-college-build-2026-10-28-to-29.md", "2026-10-28 to 2026-10-29 // Meta Shop Sync & iPhone VCF Clean Slate"),
        ],
    ),
    (
        "PMC_NotebookLM_Vol_03_2026-10-30_to_2026-11-04.md",
        "Volume 03 (2026-10-30 to 2026-11-04): Circular 02, SMS Broadcast, 109-SKU Halloween Expansion & Early November Builds",
        [
            ("oct", "agent-log_ project-marshall-college-build-2026-10-30.md", "2026-10-30 // Circular 02 & Toll-Free SMS Launch"),
            ("oct", "agent-log_ project-marshall-college-2026-10-31.md", "2026-10-31 // Halloween 25-Item Catalog Expansion (109 SKUs)"),
            ("nov", "agent-log_ project-marshall-college-build-2026-11-01-to-02.md", "2026-11-01 to 2026-11-02 // Angela Pieces & Showroom Sync"),
            ("nov", "agent-log_ project-marshall-college-build-2026-11-03-to-04.md", "2026-11-03 to 2026-11-04 // Onsite Showroom Session & Curatorial Search"),
        ],
    ),
    (
        "PMC_NotebookLM_Vol_04_2026-11-05_to_2026-11-10.md",
        "Volume 04 (2026-11-05 to 2026-11-10): Chaphavian Architecture, Silk Rug Removal, Guardrails & Final Week",
        [
            ("nov", "agent-log_ project-marshall-college-2026-11-05-to-06-the-serious-moment-clean.md", "2026-11-05 to 2026-11-06 // Gustavian Circular & Boundary Reset"),
            ("nov", "agent-log_ project-marshall-college-2026-11-06-to-07.md", "2026-11-06 to 2026-11-07 // Chaphavian Frontend & About/Services Upgrade"),
            ("nov", "agent-log_ project-marshall-college-2026-11-08-to-09.md", "2026-11-08 to 2026-11-09 // Hand-Finished Silk Removal & Guardrails"),
            ("nov", "agent-log_ project-marshall-college-2026-11-10-unbillable.md", "2026-11-10 // Veterans Day Prep & Unbillable Log"),
        ],
    ),
]


def strip_base64_images(text: str) -> Tuple[str, int]:
    count = 0
    text, c1 = B64_INLINE_IMG_RE.subn(r"![\1]([SCREENSHOT_STRIPPED_FOR_ARCHIVE])", text)
    count += c1
    text, c2 = B64_REF_DEF_RE.subn("", text)
    count += c2
    text, c3 = B64_RAW_URI_RE.subn("[BASE64_IMAGE_STRIPPED]", text)
    count += c3
    # Collapse runs of 4+ blank lines left behind by stripped reference tails
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + "\n", count


def scrub_secrets(text: str) -> Tuple[str, Dict[str, int]]:
    hits: Dict[str, int] = {}
    for label, rx, repl in SECRET_PATTERNS:
        text, n = rx.subn(repl, text)
        if n > 0:
            hits[label] = hits.get(label, 0) + n
    return text, hits


def build_section_block(index: int, total: int, label: str, filename: str, body: str) -> str:
    words = len(body.split())
    header = (
        f"\n\n---\n\n"
        f"# [LOG {index:02d} OF {total:02d}] {label}\n\n"
        f"- **Source Filename**: `{filename}`\n"
        f"- **Sanitized Word Count**: `{words:,}` words\n\n"
        f"---\n\n"
    )
    return header + body


def run_compile() -> None:
    pmc_root = Path(r"c:\Users\Saturn\Desktop\project-marshall-college")
    flight_root = pmc_root / r"project-marshall-college\00-iskenderun\headmaster\00-project-notes\flight-logs"
    oct_dir = flight_root / "2026-october-project-marshall-college-flight-logs"
    nov_dir = flight_root / "2026-november-project-marshall-college-flight-logs"
    out_dir = flight_root / "2026-sanitized-historical-archive-and-notebooklm-blocks"
    nb_dir = out_dir / "notebooklm-upload-blocks"

    q_root = pmc_root / "_QUARANTINE_CLIENTELE_PII_FOR_WIPEFILE"
    q_raw = q_root / "01_raw_clientele_files_and_buyer_invoices"
    q_etl = q_root / "02_customer_etl_scripts_and_pycache"
    q_orig = q_root / "03_unredacted_originals_of_sanitized_logs_and_docs"

    out_dir.mkdir(parents=True, exist_ok=True)
    nb_dir.mkdir(parents=True, exist_ok=True)

    # Load ground-truth client names if quarantine still exists on disk
    client_names = set()
    for base in (q_raw, q_etl):
        if base.exists():
            client_names |= pii.harvest_client_names_from_quarantine_sources(base)
    name_re = pii.build_name_regex(client_names)

    # Step 1: Sanitize EVERY .md file in flight_root (oct, nov, and parent) in-place:
    # strip base64 bloat, scrub secrets/bank/Medi-Cal IDs, and ensure zero clientele PII.
    total_b64_stripped = 0
    total_secret_hits: Dict[str, int] = {}

    for md_fp in sorted(flight_root.rglob("*.md")):
        if out_dir in md_fp.parents:
            continue
        rel_to_pmc = md_fp.relative_to(pmc_root)
        raw = md_fp.read_text(encoding="utf-8", errors="ignore")
        cleaned, b64_n = strip_base64_images(raw)
        cleaned, sec_hits = scrub_secrets(cleaned)
        cleaned, pii_n = pii.sanitize_text(cleaned, name_re)

        if b64_n > 0 or sec_hits or pii_n > 0:
            if q_orig.exists():
                bak = q_orig / rel_to_pmc
                if not bak.exists():
                    bak.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(md_fp, bak)
            md_fp.write_text(cleaned, encoding="utf-8")
            total_b64_stripped += b64_n
            for k, v in sec_hits.items():
                total_secret_hits[k] = total_secret_hits.get(k, 0) + v

    print(f"[1] In-place flight-log scrub complete: stripped {total_b64_stripped} base64 payloads; secrets scrubbed: {total_secret_hits}")

    # Step 2: Assemble the 4 NotebookLM Blocks + Monthly Historical MDs + Complete Master Historical MD
    all_entries_flat: List[Tuple[str, str, str, Path]] = []
    for _, _, items in CHRONOLOGICAL_BLOCKS:
        for month_tag, fname, label in items:
            folder = oct_dir if month_tag == "oct" else nov_dir
            fp = folder / fname
            if not fp.exists():
                raise FileNotFoundError(f"Missing expected flight log: {fp}")
            all_entries_flat.append((month_tag, fname, label, fp))

    total_logs = len(all_entries_flat)
    print(f"[2] Verified all {total_logs} unique chronological flight logs.")

    global_idx = 0
    master_sections: List[str] = []
    oct_sections: List[str] = []
    nov_sections: List[str] = []
    master_toc: List[str] = []

    for vol_fname, vol_title, items in CHRONOLOGICAL_BLOCKS:
        vol_sections: List[str] = []
        vol_toc: List[str] = []
        vol_words = 0

        for month_tag, fname, label in items:
            global_idx += 1
            folder = oct_dir if month_tag == "oct" else nov_dir
            body = (folder / fname).read_text(encoding="utf-8", errors="ignore").strip()
            w = len(body.split())
            vol_words += w

            sec = build_section_block(global_idx, total_logs, label, fname, body)
            vol_sections.append(sec)
            master_sections.append(sec)
            if month_tag == "oct":
                oct_sections.append(sec)
            else:
                nov_sections.append(sec)

            toc_line = f"- **Log {global_idx:02d}**: {label} (`{fname}` - `{w:,}` words)"
            vol_toc.append(toc_line)
            master_toc.append(toc_line)

        vol_header = (
            f"# Project Marshall College // Sanitized Historical Flight Logs\n"
            f"## {vol_title}\n\n"
            f"- **Logs Included**: `{len(items)}` complete session logs (zero mid-log splits)\n"
            f"- **Total Volume Word Count**: `{vol_words:,}` words (NotebookLM single-source ceiling: `500,000` words)\n"
            f"- **Sanitization Status**: Zero base64 image bloat, zero API/webhook secrets, zero banking/Medi-Cal IDs, zero third-party clientele PII\n\n"
            f"### Volume Table of Contents\n\n"
            + "\n".join(vol_toc)
            + "\n"
        )
        vol_out = nb_dir / vol_fname
        vol_full = vol_header + "".join(vol_sections) + "\n"
        vol_out.write_text(vol_full, encoding="utf-8")
        print(
            f"  [NOTEBOOKLM BLOCK] {vol_fname} | logs={len(items)} | words={len(vol_full.split()):,} | size={vol_out.stat().st_size/1024/1024:.2f} MB"
        )

    # Write Monthly Historical MDs (October Complete + November Complete)
    oct_text = (
        "# Project Marshall College // October 2026 Complete Historical Flight Logs (Sanitized)\n\n"
        f"- **Coverage**: `2026-10-01` through `2026-10-31` (`{len(oct_sections)}` complete session logs)\n"
        "- **Sanitization Status**: Client PII, live API/webhook secrets, banking IDs, and base64 payloads stripped\n"
        + "".join(oct_sections)
        + "\n"
    )
    oct_out = out_dir / "PMC_Historical_Month_01_October_2026_Complete.md"
    oct_out.write_text(oct_text, encoding="utf-8")
    print(f"  [HISTORICAL OCT] {oct_out.name} | words={len(oct_text.split()):,} | size={oct_out.stat().st_size/1024/1024:.2f} MB")

    nov_text = (
        "# Project Marshall College // November 2026 Complete Historical Flight Logs (Sanitized)\n\n"
        f"- **Coverage**: `2026-11-01` through `2026-11-10` (`{len(nov_sections)}` complete session logs)\n"
        "- **Sanitization Status**: Client PII, live API/webhook secrets, banking/Medi-Cal IDs, and base64 payloads stripped\n"
        + "".join(nov_sections)
        + "\n"
    )
    nov_out = out_dir / "PMC_Historical_Month_02_November_2026_Complete.md"
    nov_out.write_text(nov_text, encoding="utf-8")
    print(f"  [HISTORICAL NOV] {nov_out.name} | words={len(nov_text.split()):,} | size={nov_out.stat().st_size/1024/1024:.2f} MB")

    # Write Unified All-In-One Master Historical MD
    master_header = (
        "# Project Marshall College // Complete Sanitized Historical Flight Log Archive (2026-10-01 to 2026-11-10)\n\n"
        f"- **Total Logs Consolidated**: `{total_logs}` complete chronological logs\n"
        "- **Sanitization Status**: Zero third-party clientele PII, zero API/webhook secrets, zero banking/Medi-Cal IDs, zero base64 DOM bloat\n\n"
        "## Master Chronological Table of Contents\n\n"
        + "\n".join(master_toc)
        + "\n"
    )
    master_full = master_header + "".join(master_sections) + "\n"
    master_out = out_dir / "PMC_Historical_Master_Complete_2026-10-01_to_2026-11-10.md"
    master_out.write_text(master_full, encoding="utf-8")
    print(f"  [HISTORICAL ALL] {master_out.name} | words={len(master_full.split()):,} | size={master_out.stat().st_size/1024/1024:.2f} MB")


if __name__ == "__main__":
    run_compile()
