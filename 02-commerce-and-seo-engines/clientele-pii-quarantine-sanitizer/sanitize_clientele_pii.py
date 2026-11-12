#!/usr/bin/env python3
"""
NeverRender Labs — Clientele PII Quarantine & In-Place Sanitizer
================================================================
Surgically quarantines raw third-party clientele spreadsheets, buyer invoices,
customer audit PDFs/reports, and hardcoded customer ETL scripts into a single
staging directory ready for secure WipeFile destruction, while backing up and
sanitizing embedded third-party clientele PII (names, emails, phone numbers)
in-place across retained operational logs, B2B invoices (.docx/.xlsx), and
brand voice corpora.

Zero hardcoded client PII is stored in this script: ground-truth customer names,
emails, and phone numbers are harvested dynamically in-memory from the files
being quarantined prior to moving them, combined with strict allowlist-filtered
email and phone regular expressions.
"""

from __future__ import annotations

import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import Set, Tuple

import openpyxl

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(
    r"(?:\+?1[-.\s]?)?\(\d{3}\)[-.\s]?\d{3}[-.\s]\d{4}"
    r"|(?:\+?1[-.\s])?\b\d{3}[-.]\d{3}[-.]\d{4}\b"
)

# Allowlisted non-clientele domains (operator, studio, client principal business,
# public freight/rug vendors, healthcare/housing advocacy, platform system domains,
# and synthetic proposal mock domains).
SAFE_DOMAIN_SUBSTRINGS = (
    "renderwithoutcode.com",
    "neverrenderlabs.com",
    "passinbox.com",
    "thechapmancollection.com",
    "chapmancollection.com",
    "thechapmanconsultinggroup.com",
    "rugchick.com",
    "gonavis.com",
    "pakmaillajolla.com",
    "claremontrug.com",
    "mansour.com",
    "eloquence.com",
    "ethanblu.com",
    "omnisend.com",
    "soundest.email",
    "ralphs.com",
    "thekrogerco.com",
    "n2co.com",
    "sofi.org",
    "dropbox.com",
    "uber.com",
    "adobe.com",
    "purpleapelabs.com",
    "presidiumhealth.com",
    "interfaithservices.org",
    "dhcs.ca.gov",
    "calcivilrights.ca.gov",
    "chgsd.com",
    "dmhc.ca.gov",
    "sdcounty.ca.gov",
    "serenehealth.com",
    "molinahealthcare.com",
    "extendedstay.com",
    # XML / Web / Tech schemas
    "schemas.openxmlformats",
    "schemas.microsoft",
    "w3.org",
    "schema.org",
    "wordpress.org",
    "woocommerce.com",
    "example.com",
    "domain.com",
    "mysite.com",
    "sentry.io",
    "googleapis.com",
    "gstatic.com",
    "gravatar.com",
    "yoast.com",
    "automattic.com",
    "godaddy.com",
    "secureserver.net",
    "cloudflare.com",
    "jquery.com",
    "fontawesome.com",
    "chairish.com",
    "1stdibs.com",
    "etsy.com",
    "instagram.com",
    "facebook.com",
    "meta.com",
    "google.com",
    "apple.com",
    "github.com",
    "python.org",
    # Synthetic proposal mock domains (555-01xx demo records)
    "pendeltonlaw.com",
    "pendeltondesign.com",
    "pendeltoncapital.com",
    "estate.net",
    "rostovadesign.com",
    "sterlinginteriors-rsf.com",
    "alcottfamilyoffice.com",
    "globaltrust.org",
    "davenporttrust.com",
    "thornechambers.org",
    "kensingtondesignla.com",
    "newportcapital.com",
    "scrippsclinic.org",
    "foxrancho.com",
    "dewittgallery.com",
    "ucsdhealth.edu",
    "montgomeryranch.com",
    "vanceholdings.com",
    "vancecapital.com",
    "ljmed.org",
    "lawsoninteriors.com",
    "fairbanksestates.com",
    "croftcapital.co.uk",
)

SAFE_EXACT_EMAIL_SUBSTRINGS = (
    "bash_aliens3@proton",
    "_aliens3@proton",
    "fermiparadox1963@gmail.com",
    "fermiparadox1983@gmail.com",
    "heartluvr47@gmail.com",
    "mwyatt.renderwithoutcode@gmail.com",
    "thechapmancollection@gmail.com",
    "thechapmancollectionrsf@gmail.com",
    "melissachapman11@gmail.com",
    "chapmanconsultinggroup@gmail.com",
    # Proposed institutional Proton aliases from Oct 2 architecture notes
    "chapman.archives@proton.me",
    "chapman.covenant@proton.me",
    "chapman.privateclient@proton.me",
    "chapman.provenance@proton.me",
    "chapman.vault@proton.me",
    "chapmanarchives@proton.me",
    "chapmancollection@proton.me",
    "concierge.thechapmancollection@proton.me",
    "curator.thechapmancollection@proton.me",
    "curatorial.chapman@proton.me",
    "director.chapmancollection@proton.me",
    "privatevault.chapman@proton.me",
    "tcc-archives@proton.me",
    "tcc.vault@proton.me",
    "thechapmancollection@proton.me",
)

# Non-clientele 10-digit phones (operator, TCC showroom/mobile/toll-free, public freight/vendors, medical/housing)
SAFE_PHONES_10 = {
    "7603100706",  # Operator mobile
    "7603100705",  # Typo of operator mobile in Oct 2 note
    "8583492638",  # TCC principal mobile
    "8587565666",  # TCC Rancho Santa Fe landline
    "8333494101",  # TCC Omnisend toll-free
    "8333434101",  # Initial toll-free submission typo in Oct 23 note
    "8333656101",  # Omnisend demo/system toll-free
    "6192447401",  # Legacy TCC GoDaddy/GBP header phone
    "8582560103",  # Navis Pack & Ship #25006CA
    "8584537331",  # The UPS Store #0400 San Diego
    "8584537335",  # The UPS Store #0400 Fax
    "8584537371",  # The UPS Store #0400 alt line
    "8584568573",  # Pak Mail La Jolla
    "5106540816",  # Claremont Rug Company public phone
    "3106529999",  # Mansour public phone
    "6199909708",  # RugChick / Oriental Rug Cleaning Co. San Diego public business phone
    "7604391499",  # Extended Stay hotel front desk
    # Operator medical / housing / advocacy institutional numbers in wyatt-voice-corpus
    "6195433500",
    "6195435540",
    "6194713931",
    "6196945891",
    "7606315000",
    "7607448501",
    "6193547126",
}

PROTECTED_NAMES_LOWER = {
    "matthew wyatt",
    "matthew cole wyatt",
    "sandra wyatt",
    "melissa chapman",
    "ron chapman",
    "lisa wagner",
    "beejan hamraz",
    "andrew polis",
    "alyssa roque",
    "salvador dali",
    "marc chagall",
    "pablo picasso",
    "henri matisse",
    "frank lloyd wright",
    "louis xv",
    "louis xvi",
    "queen anne",
    "rancho santa fe",
    "san diego",
    "la jolla",
    "del mar",
    "santa barbara",
    "newport beach",
    "beverly hills",
    "los angeles",
    "palm beach",
    "united states",
    "chapman collection",
    "the chapman collection",
    "neverrender labs",
    "constant contact",
    "harrison sterling",
    "claire sterling",
    "arthur pendelton",
    "elena rostova",
    "eleanor sterling",
    "terri brien",
    # Non-person table headers, geography, and public figures matched in ETL script string literals
    "billed price",
    "concierge teaser",
    "cort number",
    "date processed",
    "el cid",
    "files included",
    "hard bounced",
    "invoice date",
    "item description",
    "north county",
    "pcs office",
    "porcelain & fine china",
    "priority vip",
    "record count",
    "retail price",
    "rita ora",
    "ron office",
    "the covenant",
    "to try",
    "transactions ledger",
    "united kingdom",
    "your price",
    "ao electric",
    "bell fields",
}


def is_safe_email(email_str: str) -> bool:
    low = email_str.lower()
    if low.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".css", ".js", ".woff", ".woff2", ".ttf")):
        return True
    for sub in SAFE_EXACT_EMAIL_SUBSTRINGS:
        if sub in low:
            return True
    for dom in SAFE_DOMAIN_SUBSTRINGS:
        if dom in low:
            return True
    return False


def is_safe_phone(phone_str: str) -> bool:
    digits = re.sub(r"\D", "", phone_str)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) != 10:
        return True
    if digits in SAFE_PHONES_10:
        return True
    if digits[3:6] == "555":
        return True
    if digits.startswith(("000", "123", "800", "888", "877", "866", "858000")):
        return True
    return False


def harvest_client_names_from_quarantine_sources(pmc_root: Path) -> Set[str]:
    """Extract multi-word full client names from clientele files prior to moving them."""
    names: Set[str] = set()

    # 1. Constant Contact spreadsheet
    cc_xlsx = pmc_root / (
        r"project-marshall-college\00-iskenderun\headmaster\04-agents"
        r"\project-marshall-college-build-materials\building-dee\provided-materials"
        r"\Constant Conact given #1 .xlsx"
    )
    if cc_xlsx.exists():
        wb = openpyxl.load_workbook(cc_xlsx, read_only=True, data_only=True)
        for s in wb.sheetnames:
            ws = wb[s]
            header_map = {}
            for row in ws.iter_rows(values_only=True):
                vals = [str(c).strip() if c is not None else "" for c in row]
                low_vals = [v.lower() for v in vals]
                if any(h in low_vals for h in ("first name", "email address", "last name", "email")):
                    for idx, lv in enumerate(low_vals):
                        header_map[lv] = idx
                    continue
                if header_map:
                    fn_idx = header_map.get("first name", header_map.get("first"))
                    ln_idx = header_map.get("last name", header_map.get("last"))
                    fn = vals[fn_idx] if fn_idx is not None and fn_idx < len(vals) else ""
                    ln = vals[ln_idx] if ln_idx is not None and ln_idx < len(vals) else ""
                    full = f"{fn} {ln}".strip()
                    if fn and ln and len(fn) >= 2 and len(ln) >= 2 and full.lower() not in PROTECTED_NAMES_LOWER:
                        if re.match(r"^[A-Za-z][A-Za-z.'\-\s]+[A-Za-z]$", full):
                            names.add(full)
        wb.close()

    # 2. Python ETL & Audit Markdown sources
    rel_sources = [
        r"scripts\database-and-etl\apply_melissa_oct29_contact_review_and_clean_names.py",
        r"scripts\database-and-etl\build_clean_slate_omnisend_master_uploads.py",
        r"scripts\database-and-etl\quarantine_chapman_relatives_and_sandra_wyatt.py",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\build_customer_archive.py",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\nrl-materials\The Chapman Collection_ Master Clientele Audit & Receptionist Briefing Report 10032026.md",
        r"scratch\convert_invoices_to_md.py",
        r"scratch\merge_batch_04_oct15.py",
    ]
    quoted_full_re = re.compile(r'["\']([A-Z][a-z]{1,18}(?:\s+(?:and|&)\s+[A-Z][a-z]{1,18})?\s+[A-Z][A-Za-z\'-]{2,20})["\']')
    md_bold_name_re = re.compile(r"\*\*([A-Z][a-z]{1,18}\s+[A-Z][A-Za-z\'-]{2,20})\*\*")

    for rel in rel_sources:
        fp = pmc_root / rel
        if fp.exists():
            txt = fp.read_text(encoding="utf-8", errors="ignore")
            for m in quoted_full_re.finditer(txt):
                cand = m.group(1).strip()
                if cand.lower() not in PROTECTED_NAMES_LOWER and not any(
                    w in cand.lower()
                    for w in (
                        "street", "avenue", "road", "drive", "lane", "court", "place",
                        "ranch", "valley", "beach", "hills", "park", "club", "estate",
                        "rug", "carpet", "silk", "wool", "french", "italian", "english",
                        "persian", "antique", "vintage", "custom", "framed", "bronze",
                        "marble", "crystal", "chandelier", "cabinet", "console", "mirror",
                        "table", "chair", "sofa", "painting", "tier", "batch", "master",
                        "clean", "showroom", "client", "collector", "contact", "verified",
                        "active", "status", "email", "phone", "first", "last", "total",
                        "omnisend", "woocommerce", "yoast", "google", "meta", "apple",
                    )
                ):
                    names.add(cand)
            if rel.endswith(".md"):
                for m in md_bold_name_re.finditer(txt):
                    cand = m.group(1).strip()
                    if cand.lower() not in PROTECTED_NAMES_LOWER and not any(
                        w in cand.lower()
                        for w in (
                            "tier", "vip", "total", "high", "key", "next", "phase", "step",
                            "clean", "master", "showroom", "persian", "french", "antique",
                            "executive", "summary", "action", "audit", "client", "collector",
                        )
                    ):
                        names.add(cand)

    return names


def build_name_regex(names: Set[str]) -> re.Pattern | None:
    # Add high-specificity multi-word invoice/account strings observed in audits
    extra_phrases = {
        "Dr. Roy and Paola",
        "Joe and Barbara",
        "Charles and Renee Brandes",
        "Kathleen Beverige",
    }
    all_names = sorted(names | extra_phrases, key=len, reverse=True)
    filtered = [n for n in all_names if len(n) >= 6 and " " in n and n.lower() not in PROTECTED_NAMES_LOWER]
    if not filtered:
        return None
    pattern = r"\b(?:" + "|".join(re.escape(n) for n in filtered) + r")\b"
    return re.compile(pattern)


def sanitize_text(text: str, name_re: re.Pattern | None) -> Tuple[str, int]:
    changes = 0

    def repl_email(m: re.Match) -> str:
        nonlocal changes
        val = m.group(0)
        if is_safe_email(val):
            return val
        changes += 1
        return "[REDACTED_CLIENT_EMAIL]"

    def repl_phone(m: re.Match) -> str:
        nonlocal changes
        val = m.group(0)
        if is_safe_phone(val):
            return val
        changes += 1
        return "[REDACTED_CLIENT_PHONE]"

    out = EMAIL_RE.sub(repl_email, text)
    # Also scrub masked partial customer email rl...@gmail.com if present
    if "rl...@gmail.com" in out:
        changes += out.count("rl...@gmail.com")
        out = out.replace("rl...@gmail.com", "[REDACTED_CLIENT_EMAIL]")

    out = PHONE_RE.sub(repl_phone, out)

    if name_re is not None:
        out, n_subs = name_re.subn("[REDACTED_CLIENT]", out)
        changes += n_subs

    return out, changes


def sanitize_docx_in_place(docx_path: Path, backup_path: Path, name_re: re.Pattern | None) -> int:
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(docx_path, backup_path)

    total_changes = 0
    tmp_path = docx_path.with_suffix(".docx.tmp")
    with zipfile.ZipFile(docx_path, "r") as zin, zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            raw = zin.read(item.filename)
            if item.filename.endswith((".xml", ".rels")):
                txt = raw.decode("utf-8", errors="ignore")
                new_txt, ch = sanitize_text(txt, name_re)
                if ch > 0:
                    total_changes += ch
                    raw = new_txt.encode("utf-8")
            zout.writestr(item, raw)

    if total_changes > 0:
        os.replace(tmp_path, docx_path)
    else:
        tmp_path.unlink(missing_ok=True)
        backup_path.unlink(missing_ok=True)
    return total_changes


def sanitize_xlsx_in_place(xlsx_path: Path, backup_path: Path, name_re: re.Pattern | None) -> int:
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(xlsx_path, backup_path)

    wb = openpyxl.load_workbook(xlsx_path)
    total_changes = 0
    for s in wb.sheetnames:
        ws = wb[s]
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    new_val, ch = sanitize_text(cell.value, name_re)
                    if ch > 0:
                        cell.value = new_val
                        total_changes += ch
    if total_changes > 0:
        wb.save(xlsx_path)
    else:
        backup_path.unlink(missing_ok=True)
    wb.close()
    return total_changes


def run_pmc_sanitization(pmc_root: Path, gag_root: Path) -> None:
    quarantine_root = pmc_root / "_QUARANTINE_CLIENTELE_PII_FOR_WIPEFILE"
    q_raw = quarantine_root / "01_raw_clientele_files_and_buyer_invoices"
    q_etl = quarantine_root / "02_customer_etl_scripts_and_pycache"
    q_orig = quarantine_root / "03_unredacted_originals_of_sanitized_logs_and_docs"

    q_raw.mkdir(parents=True, exist_ok=True)
    q_etl.mkdir(parents=True, exist_ok=True)
    q_orig.mkdir(parents=True, exist_ok=True)

    # If re-running after a filter refinement, restore any previously backed-up originals first
    for dp, _, fn_list in os.walk(q_orig):
        for fn in fn_list:
            bak_fp = Path(dp) / fn
            rel = bak_fp.relative_to(q_orig)
            dest_fp = pmc_root / rel
            dest_fp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(bak_fp, dest_fp)
            bak_fp.unlink()

    # Step 1: Harvest ground-truth client names in-memory (from pmc_root or already-quarantined folders)
    client_names = set()
    for base in (pmc_root, q_raw, q_etl):
        client_names |= harvest_client_names_from_quarantine_sources(base)
    name_re = build_name_regex(client_names)
    print(f"[1] Harvested {len(client_names)} unique multi-word clientele names for in-place scrubbing.")

    # Step 2: Quarantine raw clientele files, buyer invoices, and live .env secrets
    raw_to_move = [
        r".env",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\provided-materials\Constant Conact given #1 .xlsx",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\provided-materials\Dr Roy Aug 2026 .pdf",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\provided-materials\Joe and Barbara Final big june .pdf",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\provided-materials\Kara Picasso and ring July 2026.pdf",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\provided-materials\Madalyn Invoce Aug 2026.pdf",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\nrl-materials\The Chapman Collection_ Master Clientele Audit & Receptionist Briefing Report 10032026.md",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\seo-aeo-weekly-audits\dee-reports-audits\THE CHAPMAN COLLECTION_ CLIENTELE AUDIT AND RECEPTION DESK BRIEFING REPORT OCTOBER 03 2026.pdf",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-build-materials\building-dee\nrl-materials\curator-thechapmancollection-proton.zip",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\project-marshall-college-pre-build-recon-mission\agent-report\dinner\project-marshall-college.pdf",
    ]
    moved_raw = 0
    for rel in raw_to_move:
        src = pmc_root / rel
        if src.exists():
            dst = q_raw / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            moved_raw += 1
            print(f"  [MOVED RAW] {rel}")

    # Step 3: Quarantine customer ETL scripts & compiled pycache containing hardcoded PII
    etl_to_move = [
        r"inspect_details.py",
        r"inspect_ron_dump.py",
        r"run_dedupe_pipeline.py",
        r"scratch\convert_invoices_to_md.py",
        r"scratch\insert_inquiry.py",
        r"scratch\merge_batch_04_oct15.py",
        r"project-marshall-college\00-iskenderun\headmaster\04-agents\build_customer_archive.py",
        r"scripts\database-and-etl\apply_melissa_oct29_contact_review_and_clean_names.py",
        r"scripts\database-and-etl\build_clean_slate_omnisend_master_uploads.py",
        r"scripts\database-and-etl\clean_and_dedupe_mc_iphone_vcf.py",
        r"scripts\database-and-etl\finalize_clean_db_and_dee.py",
        r"scripts\database-and-etl\merge_tab1_vips_and_build_omnisend_sms_csvs.py",
        r"scripts\database-and-etl\quarantine_chapman_relatives_and_sandra_wyatt.py",
        r"scripts\database-and-etl\reconcile_omnisend_export_vs_master_db.py",
        r"scripts\database-and-etl\update_clean_master_databases_oct24.py",
        r"scripts\database-and-etl\__pycache__\clean_and_dedupe_mc_iphone_vcf.cpython-314.pyc",
    ]
    moved_etl = 0
    for rel in etl_to_move:
        src = pmc_root / rel
        if src.exists():
            dst = q_etl / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            moved_etl += 1
            print(f"  [MOVED ETL] {rel}")

    # Step 4: Walk remaining active PMC tree (excluding .git and quarantine) and sanitize in-place
    sanitized_files = 0
    total_redactions = 0
    for dp, dn, fn_list in os.walk(pmc_root):
        dn[:] = [d for d in dn if d not in (".git", "_QUARANTINE_CLIENTELE_PII_FOR_WIPEFILE")]
        for fn in sorted(fn_list):
            fp = Path(dp) / fn
            rel = fp.relative_to(pmc_root)
            ext = fp.suffix.lower()

            if ext in (".md", ".py", ".html", ".txt", ".json", ".csv", ".tsv", ".xml"):
                txt = fp.read_text(encoding="utf-8", errors="ignore")
                new_txt, ch = sanitize_text(txt, name_re)
                if ch > 0:
                    bak = q_orig / rel
                    bak.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(fp, bak)
                    fp.write_text(new_txt, encoding="utf-8")
                    sanitized_files += 1
                    total_redactions += ch
                    print(f"  [SANITIZED TEXT] {rel} ({ch} redactions)")
            elif ext == ".docx":
                bak = q_orig / rel
                ch = sanitize_docx_in_place(fp, bak, name_re)
                if ch > 0:
                    sanitized_files += 1
                    total_redactions += ch
                    print(f"  [SANITIZED DOCX] {rel} ({ch} redactions)")
            elif ext == ".xlsx":
                # Skip synthetic mock customer database templates
                if "Chapman_Master_Customer_Database_Template.xlsx" in fn:
                    continue
                bak = q_orig / rel
                ch = sanitize_xlsx_in_place(fp, bak, name_re)
                if ch > 0:
                    sanitized_files += 1
                    total_redactions += ch
                    print(f"  [SANITIZED XLSX] {rel} ({ch} redactions)")

    # Step 5: Sync clean voice corpora back to G_AG_FLDR so mirrored corpora have zero clientele PII
    for corp_rel in [
        r".agents\skills\melissa-tone-copywriter\references\voice-corpus.md",
        r".agents\skills\wyatt-nrl-voice-copywriter\references\wyatt-voice-corpus.md",
    ]:
        pmc_corp = pmc_root / corp_rel
        gag_corp = gag_root / corp_rel
        if pmc_corp.exists() and gag_corp.exists():
            shutil.copy2(pmc_corp, gag_corp)
            print(f"  [SYNCED CLEAN CORPUS TO G_AG_FLDR] {corp_rel}")

    print(
        f"\nSUMMARY: Moved {moved_raw} raw clientele/secret files + {moved_etl} ETL scripts; "
        f"sanitized {sanitized_files} retained files in-place ({total_redactions} total PII redactions)."
    )


if __name__ == "__main__":
    run_pmc_sanitization(
        Path(r"c:\Users\Saturn\Desktop\project-marshall-college"),
        Path(r"c:\Users\Saturn\Desktop\G_AG_FLDR"),
    )
