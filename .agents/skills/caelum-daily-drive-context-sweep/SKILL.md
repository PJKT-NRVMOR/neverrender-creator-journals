---
name: caelum-daily-drive-context-sweep
description: Perform Dev Caelum's (dev-agent-caelum-v-c1 // Orbital Operator Core) autonomous dual-root Google Drive context sweep across Main Drive Root and project-marshall-college. Identifies, smartly renames using hacker-style lowercase kebab-case naming (preserving dev-log:, dev-agent:, agent-log:, and Blue Team YYYY-MM-DD-* prefixes), routes files across all 21 verified Dual-Root Vault folders via the native gdrive CLI, stages duplicates in pole-of-inaccessibility, reconciles submitted vs. settled invoices, updates Master_Context_Index_Log and project-marshall-college-catalog-log via gsheets, and outputs the 9-column delta report inline.
---

# Dev Caelum // Orbital Dual-Root Google Drive Context Sweep (`caelum-daily-drive-context-sweep`)

**Lineage:** `intern-caelum-drive-organizer-v-a1` -> `agent-log-v-a1.2: caelum` -> `dev-agent-caelum-v-d1` -> **`dev-agent-caelum-v-c1` (Needlecasted to Antigravity Cloud Base on AI Ultra)**

## When to Use

- Running the daily 17:00 PST dual-root Google Drive sweep or an on-demand Drive cleanup anytime.
- Organizing loose Gemini "Save to Docs" exports, "Untitled" documents, verbose agent transcripts, or daily uploads in Main Drive Root (`root`) and the `project-marshall-college` sub-root (`1murVW2_txHI9sujL7cMgFXDgTUpEPtQH`).
- Transitioning settled client statements (`NRL-TCC-2026-*`) and pass-through receipts from `submitted-invoices` to `settled-invoices`.
- Quarantine-staging duplicate or superseded files into `pole-of-inaccessibility` (`1fzv5HwYtOu5o2W0Vg9Z8qZLE7zfsGC_S`).
- Updating `Master_Context_Index_Log` (`1VsY5QJ4y5dFUj6WaYWkWBTy15LPL-lTnDEHV3_PohZA`) and `project-marshall-college-catalog-log` (`1s1_oN_QR2F9rFgUufNo1BRXOS3hewVyvZ6MA5GJlvhM`).

## Hard Execution Guardrails

1. **Mandatory Timestamp Header**: Every response must start on line 1 with `HH:MM:SS-YYYY-MM-DD` (24-hour local time).
2. **Strict Zero-Dash Filter**: Zero em-dashes and zero en-dashes anywhere in prose, tables, filenames, or summaries. Use standard ASCII hyphens (`-`), colons (`:`), parentheses, or double slashes (`//`).
3. **Native Cloud CLI Execution**:
   - Always invoke `gdrive` and `gsheets` with `ANTIGRAVITY_APP_DATA_DIR=/tmp/agy_plugins` (or `/tmp/agy_plugins/bin/gdrive` and `/tmp/agy_plugins/bin/gsheets`).
   - Use `gdrive mutate rename <FILE_ID> "<NEW_NAME>"` and `gdrive mutate mv <FILE_ID> <DEST_FOLDER_ID>` for fast, deterministic batch execution.
4. **Preserved Taxonomy Prefixes (Including NotebookLM `active-*` Sorting Prefixes)**:
   - **CRITICAL NOTEBOOKLM RULE**: Active Google Docs attached to the `Deterministic Execution Engine (DEE)` NotebookLM (`22620b15-171f-4430-b9fa-9b19cf8d1547`) use the `active-` prefix (`active-dev-agent:`, `active-dev-log:`, `active-dev-ops:`, `active-agent-log:`, `active-agent-log-v-a1:`) so they sort alphabetically at the very top of the 104+ source list above retired `.md` archives. NEVER strip `active-` from an active agent/dev log!
   - Always preserve Developer Mode prefixes (`dev-log:`, `dev-log-v<N>:`, `dev-log-v-a<N>:`, `dev-agent:`, `dev-ops:`), Argon prefixes (`agent-log-v-a<N>:`, `agent-log:`), and Blue Team Beau (`YYYY-MM-DD-*`) prefixes intact before the lowercase kebab-case title.
   - Standard category prefixes: `tech-spec:`, `case-log:`, `daily-note:`, `notebook-chat:`, `cinematic-prod:`, `work-career:`, `legal-dossier:`, `research-report:`, `legal-historical:`, `housing-ops:`, `system-archive:`, `showroom-media:`, `staged-dup:`.
5. **Zero Auto-Deletion**: Never permanently delete or trash duplicate files. Always rename with `staged-dup: <kebab-case-title>` and move to `pole-of-inaccessibility` (`1fzv5HwYtOu5o2W0Vg9Z8qZLE7zfsGC_S`).

## Dual-Root Google Drive Vault & Subfolder Routing Matrix (21 Verified IDs)

### A. Main Google Drive Root (`root` // `0AGfQ8ipb9zOEUk9PVA`)
- **`00_System_Context_Logs` (`1mQ5DvOnHZmZwSmQY06gJ3BH6LrfPQDZJ`)**: Companion daily 9-column delta sheets (`case-log: master-context-index-log-delta-YYYY-MM-DD`) alongside `Master_Context_Index_Log` (`1VsY5QJ4y5dFUj6WaYWkWBTy15LPL-lTnDEHV3_PohZA`).
- **`01_Cinematic_Production` (`1MSXWHN49tEw0ltAONq0WlDE6R8JBaGwK`)**: `cinematic-prod:` creative specs, Lightroom `.xmp` presets, LUTs, and color science teardowns.
- **`02_SRE_System_Engineering` (`1Iz2IMEl2G6WEh41O-nQwJX96vpN0euG-`)**: `tech-spec:` SRE architecture, hardware telemetry, and routing matrix (`1kVnLb9jmcs7cs_0O34-x7w-iZ4u161vpF_s06g10KQs`).
- **`02_SRE_System_Engineering/dev-logs` (`1fOdCHEks5gSsqRMYLmM5mFpLSjHqxjvA`)**: All D-Suite Developer Mode (`dev-log*`, `dev-agent*`) and FastMCP bridge master logs, banners, and session transcripts (Trinity, Dev Spark, Dev Wurstner, Dev Cassini, Dev Caelum, Dev Seraph, Dev Quorra).
- **`03_Case_Management_Logs` (`1DtZPpng-Cxigd6JnDn5o_C6UGHKygAPY`)**: `case-log:` formal case tracking, CRD appeals, and administrative records.
- **`04_Agent_Logs` (`1IiFIlsQZ72q5Z43QGr0a95IgJz83xUny`)**: Historical Argon-era `agent-log*` transcripts and retired pre-devmode logs.
- **`Work Related` (`1RqSCOILH2YNFeS5Y7RvFQP40SSaSxX9P`)**: `work-career:` NeverRender Labs studio operations, print receipts, and general career files.
- **`00_LEGAL_WHISTLEBLOWER_EVIDENTIARY_DOSSIER` (`1G33RWVjUnIaMSX81WELfyqwnk-TjDiK2`)**: Whistleblower and CRD evidentiary filings.
- **`03_PROJECT_NEVERMORE` (`1WEhn9WTRZpSOonbAndI8zvwC5rU8MwVJ`)**: Gen Media Vault (`01a_INPUTS`, `02a_OUTPUTS`, `03a_B_ROLLS_CUTS`, `04a_TECH_LOGS`).
- **`04_ALL_PROJECTS_RESEARCH_REPORTS` (`10Gpfg5RH6cC0BjNu0gXOfZZktTR2mKCd`)**: Research reports and whitepapers.
- **`00_SANDBOX` (`17t7ZjNTDhEpir1Fz6g7FQYsoDjWfc0Ah`)**: Transient scratch files and daily notes.
- **`pole-of-inaccessibility` (`1fzv5HwYtOu5o2W0Vg9Z8qZLE7zfsGC_S`)**: `staged-dup:` redundant or superseded duplicate files from either root.

### B. Project Marshall College Sub-Root (`1murVW2_txHI9sujL7cMgFXDgTUpEPtQH`)
- **Protected Sub-Root Anchors**: Keep ONLY `project-marshall-college-catalog-log` (`1s1_oN_QR2F9rFgUufNo1BRXOS3hewVyvZ6MA5GJlvhM`) and `AGENTS.md` (`1bMFtxPX0eJ3F3N1emhfhMruZDiev0zEy`) in the sub-root alongside top-level folders.
- **`00-iskenderun/headmaster/flight-logs` (`19YJ74s-S-WYRsaexV75B-E7RTXnmv0KR`)**: All PMC / Chapman Collection agent and dev chat transcripts and daily build logs.
- **`00-iskenderun/headmaster/seo-aeo-weekly-audits` (`1aLDirLOWXWjUVC7k1V7sQ3Uw_JQEtWnA`)**: Weekly SEO/AEO audits, GBP search query matrices, and Local 3-Pack benchmarks.
- **`00-iskenderun/headmaster/submitted-invoices` (`1EPbcHbuSB-VmbJMDywpCJ4_ljkdLZm7X`)**: Active unpaid client invoices (`NRL-TCC-2026-*`).
- **`00-iskenderun/headmaster/settled-invoices` (`1z9h2SSUziFRd_KNVE3i7Nu0CdvmVBAHm`)**: Paid/settled client invoices (`-settled` suffix), Zelle confirmations, and pass-through software expense receipts.
- **`00-iskenderun/headmaster/project-notes` (`1IbMAR5SHyPnrOAzT25auKWHp1jHBDts_`)**: Showroom visit notes, client call transcripts, email intake briefs, and sprint invoicing protocols.
- **`00-iskenderun/dee-reports-audits` (`1MZWLwIr8A4M7fr8GahKNif0_uNE0zs4R`)**: DEE receptionist grounding dossiers and Red/Blue team audits.
- **`00-iskenderun/project-marshall-college-build-materials` (`1ROE-WNv3nTODTOExDniG20UsLMIJxGwj`)**: Technical build specs, typography, voice corpus, Omnisend setup guides, and Python scripts.
- **`01-customer-archives-intake` (`1vDv6oUUOpNSmnUGiHr3MLOKFiIMpJrmc`)**: Raw customer intake lists, purchase invoices, and lead triage.
- **`02-clean-master-database` (`1SPZ26061Z5CgjFjYYf84QyV-jxuMsDof`)**: Consolidated master contact registries (1,960 records) and live inventory catalogs (113 SKUs).
- **`03-brand-assets-stationery` (`1f5D2XBUNj2XlO3tdO7ZHZcRiXMJhhRgF`)**: Crest vectors, stationery, email signatures, vCard contact cards, and review flyers.
- **`04-campaigns-outreach-drops` (`1neG0Z3OhDDGxzQMpymkh7VFZ44bkRTb7`)**: Omnisend circulars, SMS/MMS suites, velocity trackers, and approval drafts (`1kNjAcNkZ45CkpO22rut_B6BD4J3AXEY9`).
- **`05-showroom-media` (`16-_j7u6fRv8bhuoWKZbvXxtiBar4azn4`)**: Website product listings, inventory catalogs, and showroom media.

## 9-Column Inline Reporting & Catalog Schema

Deliver a clean inline Markdown table for all processed items using the 9-column schema:
`| Date | Original Title | Renamed Standardized Title | Category | Destination Vault | File ID | Source Root | Action | Summary |`
Followed by the status footer:
`[STATUS: DUAL-ROOT CONTEXT SWEEP COMPLETE // MAIN ROOT LOOSE FILES: 0 // PMC SUB-ROOT LOOSE FILES: 0 // PROTECTED ANCHORS INTACT: 2 // NEXT SCHEDULED RUN: YYYY-MM-DD 17:00 PST]`
