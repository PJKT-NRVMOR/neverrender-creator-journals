#!/usr/bin/env python3
"""
NeverRender Labs // Omnisend Campaign Export (.xlsx) True-Delivered Telemetry Engine
Computes True Delivered (Total Sent - Bounced/Failed), True Open Rate, True Click Rate,
CTOR (Clicks / Opens), True Unsubscribe Rate, and Spam Complaint Rate alongside raw
percentages across single or multi-campaign Omnisend Excel exports.

Usage:
    python audit_omnisend_xlsx_telemetry.py path/to/campaign_export.xlsx
"""

import os
import sys
import openpyxl

sys.stdout.reconfigure(encoding="utf-8")


def audit_workbook(xlsx_path: str) -> None:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    headers = [c for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    rows = [
        dict(zip(headers, r))
        for r in ws.iter_rows(min_row=2, values_only=True)
        if any(r)
    ]

    print(f"=== OMNISEND TRUE-DELIVERED TELEMETRY: {os.path.basename(xlsx_path)} ===")
    email_totals = {"sent": 0, "fail": 0, "open": 0, "click": 0, "spam": 0, "unsub": 0, "count": 0}
    sms_totals = {"sent": 0, "fail": 0, "click": 0, "unsub": 0, "count": 0}

    for r in rows:
        ctype = str(r.get("Campaign type") or "")
        cname = str(r.get("Campaign name") or "")
        sdate = str(r.get("Send date") or "")
        sent = int(r.get("Messages sent") or 0)
        fail = int(r.get("Messages failed to deliver") or 0)
        deliv = max(sent - fail, 0)
        unsub = int(r.get("Messages resulted in unsubscribes") or 0)
        deliv_pct = (deliv / sent * 100.0) if sent else 0.0
        unsub_true = (unsub / deliv * 100.0) if deliv else 0.0
        unsub_raw = (unsub / sent * 100.0) if sent else 0.0

        if ctype == "Email":
            opened = int(r.get("Messages opened") or 0)
            clicked = int(r.get("Messages clicked") or 0)
            spam = int(r.get("Messages marked as spam") or 0)
            true_open = (opened / deliv * 100.0) if deliv else 0.0
            raw_open = (opened / sent * 100.0) if sent else 0.0
            true_click = (clicked / deliv * 100.0) if deliv else 0.0
            raw_click = (clicked / sent * 100.0) if sent else 0.0
            ctor = (clicked / opened * 100.0) if opened else 0.0
            print(
                f"[EMAIL] {sdate} | {cname}\n"
                f"  True Delivered: {deliv}/{sent} ({deliv_pct:.2f}% | Bounced: {fail})\n"
                f"  True Open: {true_open:.2f}% (Raw: {raw_open:.2f}% | {opened} opens)\n"
                f"  True Click: {true_click:.2f}% (Raw: {raw_click:.2f}% | {clicked} clicks) | CTOR: {ctor:.2f}%\n"
                f"  Spam: {spam} | Unsubscribes: {unsub} (True: {unsub_true:.2f}%, Raw: {unsub_raw:.2f}%)"
            )
            email_totals["sent"] += sent
            email_totals["fail"] += fail
            email_totals["open"] += opened
            email_totals["click"] += clicked
            email_totals["spam"] += spam
            email_totals["unsub"] += unsub
            email_totals["count"] += 1
        elif ctype == "SMS":
            clicked = int(r.get("Messages clicked") or 0)
            print(
                f"[SMS]   {sdate} | {cname}\n"
                f"  True Delivered: {deliv}/{sent} ({deliv_pct:.2f}% | Failed: {fail})\n"
                f"  Clicks: {clicked} | Unsubscribes: {unsub} (True: {unsub_true:.2f}%, Raw: {unsub_raw:.2f}%)"
            )
            sms_totals["sent"] += sent
            sms_totals["fail"] += fail
            sms_totals["click"] += clicked
            sms_totals["unsub"] += unsub
            sms_totals["count"] += 1

    if email_totals["count"] > 1:
        ed = email_totals["sent"] - email_totals["fail"]
        print(
            f"\n[ROLLUP - {email_totals['count']} EMAIL SENDS] "
            f"True Delivered: {ed}/{email_totals['sent']} ({ed/email_totals['sent']*100:.2f}%) | "
            f"True Open: {email_totals['open']/ed*100:.2f}% (Raw: {email_totals['open']/email_totals['sent']*100:.2f}%) | "
            f"True Click: {email_totals['click']/ed*100:.2f}% (Raw: {email_totals['click']/email_totals['sent']*100:.2f}%) | "
            f"CTOR: {email_totals['click']/email_totals['open']*100:.2f}% | "
            f"Spam: {email_totals['spam']} | Unsubs: {email_totals['unsub']}"
        )
    if sms_totals["count"] > 1:
        sd = sms_totals["sent"] - sms_totals["fail"]
        print(
            f"[ROLLUP - {sms_totals['count']} SMS SENDS]   "
            f"True Delivered: {sd}/{sms_totals['sent']} ({sd/sms_totals['sent']*100:.2f}%) | "
            f"Unsubs: {sms_totals['unsub']} (True: {sms_totals['unsub']/sd*100:.2f}%, Raw: {sms_totals['unsub']/sms_totals['sent']*100:.2f}%)"
        )


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if os.path.exists(arg):
            audit_workbook(arg)
