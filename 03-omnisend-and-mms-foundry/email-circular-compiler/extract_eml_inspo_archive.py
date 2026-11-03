"""
Reusable EML Newsletter Inspiration & Attachment Extractor
NeverRender Labs Open-Source Studio Toolkit (03-omnisend-and-mms-foundry/email-circular-compiler/)
Zero hardcoded secrets or client PII.
"""
import argparse
import email
from email import policy
import os
import re


def extract_eml_archive(eml_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    with open(eml_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    html_parts = []
    text_parts = []
    for idx, part in enumerate(msg.walk()):
        ctype = part.get_content_type()
        fname = part.get_filename()
        if ctype == "text/html" and not fname:
            html_parts.append(part.get_content())
        elif ctype == "text/plain" and not fname:
            text_parts.append(part.get_content())
        elif fname or ctype.startswith("image/"):
            payload = part.get_payload(decode=True)
            if payload:
                safe_name = fname if fname else f"inline_{idx}.{ctype.split('/')[-1]}"
                safe_name = re.sub(r'[<>:"/\\|?*]', "_", safe_name)
                with open(os.path.join(out_dir, safe_name), "wb") as out_f:
                    out_f.write(payload)

    if html_parts:
        with open(os.path.join(out_dir, "email_body.html"), "w", encoding="utf-8") as f:
            f.write("\n".join(html_parts))
    if text_parts:
        with open(os.path.join(out_dir, "email_body.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(text_parts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract HTML, text, and attachments from an .eml file.")
    parser.add_argument("--eml", required=True, help="Path to .eml file")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    args = parser.parse_args()
    extract_eml_archive(args.eml, args.out_dir)
