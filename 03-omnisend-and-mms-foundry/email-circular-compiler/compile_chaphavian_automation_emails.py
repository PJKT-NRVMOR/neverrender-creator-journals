#!/usr/bin/env python3
"""
NeverRender Labs // Reusable Chaphavian Omnisend Automation & 9:16 Story Card Compiler
Generates light-locked 600px HTML automation templates (Post-Click Follow-Up &
18-Hour Post-Signup Welcome) plus 1080x1920 9:16 Instagram Story Link Sticker cards.

Reads all configuration via environment variables (zero hardcoded secrets or client PII).
"""

import os
from pathlib import Path


def render_light_locked_automation_shell(
    title: str,
    preheader: str,
    brand_name: str,
    crest_url: str,
    kicker: str,
    headline: str,
    subhead: str,
    body_paragraphs: list[str],
    cta_label: str,
    cta_url: str,
    hours_line: str,
    address_line: str,
    phone_display: str,
    phone_href: str,
    hero_image_url: str | None = None,
) -> str:
    """Render a 600px Chaphavian light-locked HTML email template for Omnisend automations."""
    hero_block = ""
    if hero_image_url:
        hero_block = (
            f'<div style="margin:4px 0 18px 0;border:1px solid #D9D3CC;">'
            f'<a href="{cta_url}" target="_blank" style="text-decoration:none;display:block;">'
            f'<img src="{hero_image_url}" alt="{headline or brand_name}" width="544" style="display:block;width:100%;max-width:544px;height:auto;border:0;">'
            f'</a></div>'
        )
    header_copy_block = ""
    if not hero_image_url:
        header_copy_block = (
            f'<p style="margin:0 0 6px 0;font-family:\'Garamond\',\'Georgia\',serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">{kicker}</p>'
            f'<h2 style="margin:0 0 6px 0;font-family:\'Garamond\',\'Georgia\',serif;font-size:23px;font-weight:normal;font-style:italic;color:#B35A5E;">{headline}</h2>'
            f'<p style="margin:0 0 18px 0;font-family:\'Garamond\',\'Georgia\',serif;font-size:14.5px;color:#2B2F33;">{subhead}</p>'
        )
    body_html = "\n".join(
        f'<p style="margin:0 0 14px 0;font-family:\'Garamond\',\'EB Garamond\',\'Georgia\',serif;font-size:16.5px;line-height:1.7;color:#2B2F33;text-align:left;">{p}</p>'
        for p in body_paragraphs
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>{title}</title>
</head>
<body bgcolor="#D9D3CC" style="margin:0;padding:0;background-color:#D9D3CC;">
<div style="display:none;font-size:1px;color:#D9D3CC;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
  {preheader}
</div>
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" bgcolor="#D9D3CC" style="width:100%;margin:0 auto;background-color:#D9D3CC;">
  <tr>
    <td align="center" style="padding:20px 0;">
      <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" bgcolor="#F7F5F2" style="width:600px;max-width:98%;margin:0 auto;background-color:#F7F5F2;border-left:1px solid #8A8F97;border-right:1px solid #8A8F97;border-top:5px solid #2B2F33;border-bottom:5px solid #2B2F33;">
        <tr>
          <td height="2" bgcolor="#B35A5E" style="height:2px;line-height:2px;font-size:2px;background-color:#B35A5E;"></td>
        </tr>
        <tr>
          <td align="center" bgcolor="#F7F5F2" style="padding:22px 6% 18px 6%;text-align:center;">
            <img src="{crest_url}" alt="{brand_name}" width="80" style="display:block;margin:0 auto 10px auto;width:80px;height:auto;border:0;">
            <h1 style="margin:0 0 12px 0;font-family:'Garamond','Georgia',serif;font-size:20px;font-size:clamp(17px,4.8vw,25px);letter-spacing:1.6px;text-transform:uppercase;color:#2B2F33;font-weight:normal;">{brand_name}</h1>
            {hero_block}
            {header_copy_block}
            {body_html}
            <p style="margin:18px 0 8px 0;font-family:'Garamond','Georgia',serif;font-size:11px;color:#8A8F97;font-weight:bold;">{hours_line}</p>
            <p style="margin:0 0 18px 0;font-family:'Garamond','Georgia',serif;font-size:12px;color:#8A8F97;"><a href="{phone_href}" style="color:#2B2F33;text-decoration:none;font-weight:bold;">{phone_display}</a> · {address_line}</p>
            <a href="{cta_url}" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;border:1px solid #2B2F33;text-decoration:none;font-family:'Garamond','Georgia',serif;font-size:11px;letter-spacing:1.4px;text-transform:uppercase;padding:11px 16px;display:inline-block;box-sizing:border-box;">{cta_label}</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""


if __name__ == "__main__":
    out_dir = Path(os.getenv("NRL_AUTOMATION_OUT_DIR", "."))
    print(f"[NRL] Automation compiler ready (target dir: {out_dir.resolve()})")
