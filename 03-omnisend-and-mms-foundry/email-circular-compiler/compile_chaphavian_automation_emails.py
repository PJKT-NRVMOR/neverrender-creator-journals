#!/usr/bin/env python3
"""
NeverRender Labs // Reusable Chaphavian Omnisend Email & Automation Shell Compiler
Generates spec-compliant 600px fluid Chaphavian HTML templates obeying:
- Enshrined 5-Swatch Chaphavian Palette (#F7F5F2, #D5D3CC, #8A8F97, #B35A5E, #2B2F32)
- Samsung Mail fluid outer table rule (width="100%" + inline style="width:98%;max-width:600px;",
  never fixed HTML width="600")
- Gmail <style> 8,192-character sanitizer rule (zero :root, var(--), clamp(), @import,
  prefers-color-scheme, or external Google Fonts <link>)
- Omnisend entity-decoder safety (zero HTML character entities; plain UTF-8 or 7-bit ASCII)
- 320px nested-cell safety (all white-space:nowrap spans <= 22-26 visible characters;
  2-column 48.5% product/department grids stack vertically to 100% below 520px)
- Dual Omnisend export support via chaphavian_html_linter_and_spec.py

Reads all configuration via environment variables (zero hardcoded secrets or client PII).
"""

from __future__ import annotations

import os
from pathlib import Path

from chaphavian_html_linter_and_spec import lint_html_string, split_for_omnisend_visual_builder


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
    hours_spans: list[str],
    address_line: str,
    address_url: str,
    phone_display: str,
    phone_href: str,
    subnav_items: list[tuple[str, str]] | None = None,
    hero_image_url: str | None = None,
    preference_url: str = "[[preference_link]]",
    unsubscribe_url: str = "[[unsubscribe_link]]",
) -> str:
    """
    Render a spec-compliant 600px fluid Chaphavian HTML email template.
    Every item in `hours_spans` should be <= 22-25 characters so each renders cleanly
    inside its own `white-space:nowrap` span on 320px phones.
    """
    subnav_html = ""
    if subnav_items:
        joined_links = '<span class="tcc-subnav-pipe" style="color:#D5D3CC;padding:0 3px;">|</span>'.join(
            f'<a href="{href}" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">{label}</a>'
            for label, href in subnav_items
        )
        subnav_html = (
            f'<p class="tcc-subnav" style="margin:0;padding:0 0 14px 0;border-bottom:1px solid #D5D3CC;'
            f"font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:7.5px;"
            f'letter-spacing:0px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.6;'
            f'text-align:center;white-space:nowrap;">{joined_links}</p>'
        )

    hero_block = ""
    if hero_image_url:
        hero_block = (
            f'<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" '
            f'style="width:100%;border:1px solid #D5D3CC;background-color:#F7F5F2;margin:6px 0 16px 0;">'
            f'<tr><td align="center" style="padding:0;line-height:0;font-size:0;">'
            f'<a href="{cta_url}" target="_blank" style="text-decoration:none;display:block;">'
            f'<img src="{hero_image_url}" alt="{headline or brand_name}" width="544" '
            f'style="display:block;width:100%;max-width:544px;height:auto;border:0;">'
            f"</a></td></tr></table>"
        )

    header_copy_block = ""
    if not hero_image_url:
        header_copy_block = (
            f'<p style="margin:8px 0 6px 0;font-family:\'Garamond\',\'EB Garamond\',\'Georgia\',serif;font-size:10px;'
            f'letter-spacing:1.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">{kicker}</p>'
            f'<h2 style="margin:0 0 6px 0;font-family:\'Garamond\',\'EB Garamond\',\'Georgia\',serif;font-size:23px;'
            f'font-weight:normal;font-style:italic;color:#B35A5E;">{headline}</h2>'
            f'<p style="margin:0 0 18px 0;font-family:\'Garamond\',\'EB Garamond\',\'Georgia\',serif;font-size:14.5px;'
            f'color:#2B2F32;">{subhead}</p>'
        )

    body_html = "\n".join(
        f'<p style="margin:0 0 14px 0;font-family:\'Garamond\',\'EB Garamond\',\'Apple Garamond\',\'Georgia\',serif;'
        f'font-size:16px;line-height:1.68;color:#2B2F32;text-align:left;">{p}</p>'
        for p in body_paragraphs
    )

    hours_markup = " ".join(f'<span style="white-space:nowrap;">{chunk}</span>' for chunk in hours_spans)

    html = f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<title>{title}</title>
<style type="text/css">
  .tcc-root, table, td, p, a, h1, h2, h3, h4 {{
    font-family: 'Garamond', 'EB Garamond', 'Apple Garamond', 'Georgia', serif;
  }}
  table {{
    border-collapse: collapse;
  }}
  img {{
    border: 0;
    height: auto;
    line-height: 100%;
    outline: none;
    text-decoration: none;
    max-width: 100%;
  }}
  .tcc-root, .tcc-light-surface {{
    background-color: #F7F5F2 !important;
    color: #2B2F32 !important;
  }}
  .tcc-putty-surface {{
    background-color: #D5D3CC !important;
  }}
  .tcc-btn {{
    background-color: #F7F5F2 !important;
    color: #2B2F32 !important;
  }}
  .tcc-btn:hover {{
    background-color: #2B2F32 !important;
    color: #F7F5F2 !important;
  }}
  @media only screen and (min-width: 521px) {{
    .tcc-subnav {{
      font-size: 9px !important;
      letter-spacing: 0.4px !important;
    }}
    .tcc-subnav-pipe {{
      padding: 0 6px !important;
    }}
    .tcc-desk-pipe {{
      display: inline !important;
    }}
    .tcc-stack-br {{
      display: none !important;
    }}
  }}
  @media only screen and (max-width: 520px) {{
    .tcc-outer-frame {{
      width: 98% !important;
      max-width: 98% !important;
    }}
    .tcc-pad {{
      padding-left: 4.5% !important;
      padding-right: 4.5% !important;
    }}
    .tcc-grid-col {{
      display: block !important;
      width: 100% !important;
      max-width: 100% !important;
      margin-bottom: 12px !important;
    }}
    .tcc-grid-gutter {{
      display: none !important;
      width: 0 !important;
      height: 0 !important;
    }}
    .tcc-btn {{
      font-size: 10.5px !important;
      letter-spacing: 1.2px !important;
      padding: 10px 14px !important;
      white-space: normal !important;
    }}
    .tcc-brand-h1 {{
      font-size: 19px !important;
      letter-spacing: 1.4px !important;
    }}
    .tcc-subnav {{
      font-size: 7.5px !important;
      letter-spacing: 0px !important;
    }}
    .tcc-subnav-pipe {{
      padding: 0 3px !important;
    }}
  }}
</style>
</head>
<body class="body tcc-putty-surface" bgcolor="#D5D3CC" style="margin:0;padding:0;background-color:#D5D3CC;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
<div class="tcc-root">
<div style="display:none;font-size:1px;color:#D5D3CC;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
  {preheader}
</div>
<table role="presentation" class="tcc-putty-surface" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" bgcolor="#D5D3CC" style="width:100%;table-layout:fixed;margin:0 auto;background-color:#D5D3CC;">
  <tr>
    <td align="center" style="padding:20px 0 16px 0;text-align:center;">
      <table role="presentation" class="tcc-outer-frame tcc-light-surface" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" bgcolor="#F7F5F2" style="width:98%;max-width:600px;table-layout:fixed;margin:0 auto;background-color:#F7F5F2;border-left:1px solid #8A8F97;border-right:1px solid #8A8F97;border-top:5px solid #2B2F32;border-bottom:5px solid #2B2F32;box-sizing:border-box;text-align:left;">
        <tr>
          <td height="2" bgcolor="#B35A5E" style="height:2px;line-height:2px;font-size:2px;background-color:#B35A5E;"></td>
        </tr>
        <tr>
          <td class="tcc-pad tcc-light-surface" align="center" bgcolor="#F7F5F2" style="padding:22px 6% 24px 6%;text-align:center;background-color:#F7F5F2;box-sizing:border-box;">
            <img src="{crest_url}" alt="{brand_name}" width="80" style="display:block;margin:0 auto 10px auto;width:80px;max-width:80px;height:auto;border:0;">
            <h1 class="tcc-brand-h1" style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;letter-spacing:1.6px;text-transform:uppercase;color:#2B2F32;font-weight:normal;line-height:1.25;text-align:center;">{brand_name}</h1>
            {subnav_html}
            {hero_block}
            {header_copy_block}
            {body_html}
            <p style="margin:18px 0 8px 0;font-family:'Garamond','EB Garamond','Georgia',serif;font-size:11.5px;color:#8A8F97;line-height:1.65;">{hours_markup}</p>
            <p style="margin:0 0 18px 0;font-family:'Garamond','EB Garamond','Georgia',serif;font-size:12px;color:#8A8F97;"><span style="white-space:nowrap;"><a href="{phone_href}" style="color:#2B2F32;text-decoration:none;font-weight:bold;">{phone_display}</a> <span style="color:#D5D3CC;padding:0 4px;">|</span></span> <a href="{address_url}" target="_blank" style="color:#8A8F97;text-decoration:none;">{address_line}</a></p>
            <a class="tcc-btn" href="{cta_url}" target="_blank" style="background-color:#F7F5F2;color:#2B2F32;border:1px solid #2B2F32;text-decoration:none;font-family:'Garamond','EB Garamond','Georgia',serif;font-size:11px;letter-spacing:1.4px;text-transform:uppercase;padding:11px 18px;display:inline-block;box-sizing:border-box;">{cta_label}</a>
          </td>
        </tr>
      </table>
      <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" style="width:98%;max-width:600px;margin:0 auto;">
        <tr>
          <td align="center" style="padding:14px 10px 0 10px;font-family:'Garamond','EB Garamond','Georgia',serif;font-size:11px;letter-spacing:0.4px;color:#5C6066;line-height:1.5;text-align:center;">
            <a href="{preference_url}" style="color:#5C6066;text-decoration:underline;">Edit preferences</a><span style="color:#8A8F97;padding:0 6px;">|</span><a href="{unsubscribe_url}" style="color:#5C6066;text-decoration:underline;">Unsubscribe</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</div>
</body>
</html>
"""
    report = lint_html_string(html, source_path="<render_light_locked_automation_shell>")
    if not report.passed:
        raise ValueError("Chaphavian HTML Spec violation(s):\n" + "\n".join(report.errors))
    return html


if __name__ == "__main__":
    out_dir = Path(os.getenv("NRL_AUTOMATION_OUT_DIR", "."))
    sample_html = render_light_locked_automation_shell(
        title="Gallery Correspondence",
        preheader="Thank you for visiting our gallery online.",
        brand_name="The Gallery Collection",
        crest_url="https://example.com/crest.png",
        kicker="Private Gallery Note",
        headline="Thank You for Visiting",
        subhead="Curated Continental Antiques and Fine Carpets",
        body_paragraphs=[
            "Dear [[contact.first_name | default: 'Friend']],",
            "Thank you for exploring our latest arrivals online.",
        ],
        cta_label="Explore the Gallery",
        cta_url="https://example.com/shop/",
        hours_spans=["Monday through Friday", "10:00 AM to 7:00 PM"],
        address_line="Rancho Santa Fe Village",
        address_url="https://maps.google.com/?q=Rancho+Santa+Fe",
        phone_display="(858) 000-0000",
        phone_href="tel:+18580000000",
        subnav_items=[
            ("Fine Furniture", "https://example.com/furniture/"),
            ("Carpets", "https://example.com/carpets/"),
            ("Artworks", "https://example.com/artworks/"),
            ("Services", "https://example.com/services/"),
        ],
    )
    body_only, raw_css = split_for_omnisend_visual_builder(sample_html)
    print(
        f"[NRL] Chaphavian spec compiler verified "
        f"(Full HTML: {len(sample_html.encode('utf-8')):,} B | "
        f"Body-only: {len(body_only.encode('utf-8')):,} B | "
        f"Styles-only: {len(raw_css):,} chars | Target dir: {out_dir.resolve()})"
    )
