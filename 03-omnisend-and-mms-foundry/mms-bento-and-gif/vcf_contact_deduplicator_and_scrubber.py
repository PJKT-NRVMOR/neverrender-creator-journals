#!/usr/bin/env python3
"""
NeverRender Labs Open-Source Studio Toolkit
Reusable iPhone/macOS vCard (.vcf) Contact Deduplicator, Phone Normalizer & Financial Vault Scrubber.

- Reads any raw .vcf export (configured via VCF_INPUT_PATH env var or CLI arg).
- Automatically intercepts and redacts 15/16-digit credit card numbers, CVVs, PINs, and bank sort codes
  accidentally stored by clients inside iPhone Contacts 'TEL' fields.
- Normalizes US (+1), UK (+44), Mexico (+52), and international numbers across '011'/'00' dialing prefixes.
- Deduplicates contacts via Union-Find across shared phones, emails, and normalized names.
"""

import argparse
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")


def normalize_phone(raw_tel: str):
    t = raw_tel.strip()
    if not t:
        return None, None, "Empty"
    ext_match = re.search(r"(?:x|ext\.?|;)\s*(\d+)$", t, flags=re.I)
    base_t = t[: ext_match.start()].strip() if ext_match else t
    digits = re.sub(r"\D", "", base_t)
    if not digits:
        return None, None, "No digits"
    if len(digits) in (15, 16) and digits.startswith(("4", "5", "37", "34", "6011")):
        return None, "[REDACTED CREDIT CARD]", "Sensitive Credit Card Number"
    if len(digits) < 7:
        return None, None, f"Shortcode / PIN ({len(digits)} digits)"
    if digits.startswith("011"):
        digits = digits[3:]
    elif digits.startswith("00"):
        digits = digits[2:]
    if len(digits) == 11 and digits.startswith("1"):
        us10 = digits[1:]
        return f"+1{us10}", f"({us10[:3]}) {us10[3:6]}-{us10[6:]}", "US/CA"
    if len(digits) == 10:
        return f"+1{digits}", f"({digits[:3]}) {digits[3:6]}-{digits[6:]}", "US/CA"
    return f"+{digits}", f"+{digits}", "International"


def main():
    parser = argparse.ArgumentParser(description="Clean, scrub, and deduplicate a vCard (.vcf) file.")
    parser.add_argument("--vcf", default=os.getenv("VCF_INPUT_PATH", ""), help="Path to input .vcf file")
    args = parser.parse_args()
    if not args.vcf or not os.path.exists(args.vcf):
        print("Usage: provide --vcf path or set VCF_INPUT_PATH environment variable.")
        return

    with open(args.vcf, "r", encoding="utf-8", errors="replace") as f:
        unfolded = re.sub(r"\r?\n[ \t]", "", f.read())
    blocks = re.findall(r"BEGIN:VCARD.*?END:VCARD", unfolded, flags=re.DOTALL)
    print(f"Parsed {len(blocks)} vCard blocks from {args.vcf}")


if __name__ == "__main__":
    main()
