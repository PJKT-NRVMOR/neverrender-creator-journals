#!/usr/bin/env python3
"""
NeverRender Labs // Chaphavian HTML Email Spec Linter & Omnisend Dual-Mode Exporter
Enforces the permanent 10-rule studio engineering spec across all standalone broadcast
circulars (imported via Omnisend Store Settings -> Saved Templates -> Import Template)
and automated workflow touchpoints (split into body-only HTML + raw Styles CSS for
Omnisend Visual Builder Custom HTML blocks with 0px section padding).

Zero secrets or client PII hardcoded.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MAX_HTML_BYTES_STUDIO = 75_000  # Studio ceiling (well below Gmail's 102,400-byte clip gate)
MAX_STYLE_CHARS_GMAIL = 8_192   # Gmail <style> block hard character ceiling
MAX_NOWRAP_VISIBLE_CHARS = 24   # 22-char ideal target, 24-char hard ceiling inside 320px nested cells

# CSS constructs inside <style> that cause Gmail's strict CSS parser to strip the ENTIRE <style> block
FORBIDDEN_STYLE_TOKENS = (
    ":root",
    "var(--",
    "clamp(",
    "prefers-color-scheme",
    "supported-color-schemes:",
    "@import",
    "mso-style-textfill",
    "url(",
)

# Inline CSS constructs that fail or trigger unpredictable client sanitization
FORBIDDEN_INLINE_TOKENS = (
    "clamp(",
    "var(--",
)

# Enshrined 5-Swatch Chaphavian Palette (active default; replaces legacy #D9D3CC / #2B2F33)
LEGACY_DRIFT_HEXES = (
    "#D9D3CC",
    "#2B2F33",
)

HTML_ENTITY_RE = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);")
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
BODY_INNER_RE = re.compile(r"<body[^>]*>(.*)</body>", re.IGNORECASE | re.DOTALL)
LINK_STYLESHEET_RE = re.compile(r"<link\b[^>]*rel=[\"']?stylesheet[\"']?[^>]*>", re.IGNORECASE)
TABLE_FIXED_WIDTH_RE = re.compile(r"<table\b[^>]*\bwidth=[\"']?(5\d\d|6\d\d|7\d\d|8\d\d)[\"']?", re.IGNORECASE)
NOWRAP_SPAN_RE = re.compile(
    r"<span\b[^>]*style=[\"'][^\"']*white-space\s*:\s*nowrap[^\"']*[\"'][^>]*>(.*?)</span>",
    re.IGNORECASE | re.DOTALL,
)
TAG_STRIP_RE = re.compile(r"<[^>]+>")


@dataclass
class LintReport:
    path: Path
    byte_length: int
    style_chars: int
    max_nowrap_len: int
    max_nowrap_text: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0


def lint_html_string(html: str, source_path: Path | str = "<memory>") -> LintReport:
    """Validate an HTML email string against all 10 Chaphavian & Omnisend/Gmail studio invariants."""
    p = Path(source_path)
    raw_bytes = html.encode("utf-8")
    byte_len = len(raw_bytes)
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Total HTML byte weight (< 75 KB target; 102 KB Gmail clip ceiling)
    if byte_len >= MAX_HTML_BYTES_STUDIO:
        errors.append(
            f"HTML byte weight {byte_len:,} B exceeds 75,000 B studio cap (Gmail clips footers at 102 KB)."
        )

    # 2. External <link rel="stylesheet"> check
    if LINK_STYLESHEET_RE.search(html):
        errors.append(
            'Found external <link rel="stylesheet"> tag; strip external font links and rely on font-family stack.'
        )

    # 3. <style> sanitizer checks (< 8,192 chars, zero :root / var(--) / clamp() / prefers-color-scheme / url())
    style_blocks = STYLE_BLOCK_RE.findall(html)
    total_style_chars = sum(len(b) for b in style_blocks)
    if total_style_chars >= MAX_STYLE_CHARS_GMAIL:
        errors.append(
            f"Combined <style> length {total_style_chars:,} chars exceeds Gmail's 8,192-char sanitizer limit."
        )
    for idx, block in enumerate(style_blocks, start=1):
        lower_block = block.lower()
        for token in FORBIDDEN_STYLE_TOKENS:
            if token in lower_block:
                errors.append(
                    f"<style> block #{idx} contains forbidden Gmail sanitizer trigger: '{token}'."
                )

    # 4. Inline CSS poison check (clamp(), var(--))
    lower_html = html.lower()
    for token in FORBIDDEN_INLINE_TOKENS:
        if token in lower_html:
            errors.append(f"HTML contains forbidden inline CSS construct: '{token}'.")

    # 5. Omnisend named/numeric HTML entity slice-offset bug check
    entities_found = sorted(set(HTML_ENTITY_RE.findall(html)))
    if entities_found:
        errors.append(
            f"Forbidden HTML entities found ({', '.join(entities_found)}); Omnisend's entity decoder "
            "corrupts byte offsets. Use plain UTF-8 or 7-bit ASCII instead."
        )

    # 6. Samsung Mail fixed-width layout table attribute check (width="600")
    fixed_tables = TABLE_FIXED_WIDTH_RE.findall(html)
    if fixed_tables:
        errors.append(
            f'Found fixed HTML table width attribute(s) ({", ".join(sorted(set(fixed_tables)))}px); '
            'omit width="600" and use width="100%" with inline style="width:98%;max-width:600px;" for Samsung Mail.'
        )

    # 7. Nested 320px mobile nowrap character limit check (<= 26 visible chars hard cap; 22 ideal)
    max_nw_len = 0
    max_nw_txt = ""
    for span_inner in NOWRAP_SPAN_RE.findall(html):
        clean_txt = " ".join(TAG_STRIP_RE.sub("", span_inner).split())
        if len(clean_txt) > max_nw_len:
            max_nw_len = len(clean_txt)
            max_nw_txt = clean_txt
        if len(clean_txt) > MAX_NOWRAP_VISIBLE_CHARS:
            errors.append(
                f"Unbreakable white-space:nowrap span is {len(clean_txt)} chars ('{clean_txt}'), "
                f"exceeding {MAX_NOWRAP_VISIBLE_CHARS}-char 320px nested-cell safety cap."
            )
        elif len(clean_txt) > 22:
            warnings.append(
                f"nowrap span '{clean_txt}' is {len(clean_txt)} chars (safe <= {MAX_NOWRAP_VISIBLE_CHARS}, ideal <= 22)."
            )

    # 8. Subnav inter-tag whitespace & inline mobile-safe fallback check (when .tcc-subnav is used)
    if "tcc-subnav" in html:
        if re.search(r"</a>\s+<span[^>]*tcc-subnav-pipe", html) or re.search(
            r'tcc-subnav-pipe[^>]*>\|</span>\s+<a\b', html
        ):
            errors.append(
                "Detected inter-tag whitespace/newlines around .tcc-subnav-pipe; keep subnav links and pipes "
                "contiguous on one line so Gmail Mobile never overflows 280px."
            )

    # 9. Palette drift check (#D9D3CC / #2B2F33 vs enshrined #D5D3CC / #2B2F32)
    upper_html = html.upper()
    for legacy_hex in LEGACY_DRIFT_HEXES:
        if legacy_hex in upper_html:
            errors.append(
                f"Legacy pre-enshrined hex '{legacy_hex}' detected; align to Chaphavian Putty (#D5D3CC) "
                "and Chaphavian Iron (#2B2F32)."
            )

    # 10. Zero em-dashes or en-dashes anywhere in source
    if "\u2014" in html or "\u2013" in html:
        errors.append("Forbidden em-dash (U+2014) or en-dash (U+2013) detected in HTML source.")

    return LintReport(
        path=p,
        byte_length=byte_len,
        style_chars=total_style_chars,
        max_nowrap_len=max_nw_len,
        max_nowrap_text=max_nw_txt,
        errors=errors,
        warnings=warnings,
    )


def lint_html_file(path: Path) -> LintReport:
    html = path.read_text(encoding="utf-8")
    return lint_html_string(html, source_path=path)


def split_for_omnisend_visual_builder(html: str) -> tuple[str, str]:
    """
    Split a full Chaphavian HTML document into the two clean payloads expected by
    Omnisend's Visual Builder Custom HTML item (with outer section padding set to 0px):
      1. body_only_html: inner contents of <body>...</body> (no <!DOCTYPE>, <head>, or <body> tags)
      2. raw_styles_css: combined CSS rules without <style>...</style> wrapper tags
    """
    style_blocks = [b.strip() for b in STYLE_BLOCK_RE.findall(html) if b.strip()]
    raw_css = "\n\n".join(style_blocks) + ("\n" if style_blocks else "")

    body_match = BODY_INNER_RE.search(html)
    if body_match:
        body_inner = body_match.group(1).strip() + "\n"
    else:
        body_inner = STYLE_BLOCK_RE.sub("", html).strip() + "\n"

    return body_inner, raw_css


def write_omnisend_visual_builder_pair(full_html_path: Path, out_dir: Path | None = None) -> tuple[Path, Path]:
    """Write *_body_only.html and *_styles_only.css alongside a validated full HTML template."""
    target_dir = out_dir or full_html_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)
    html = full_html_path.read_text(encoding="utf-8")
    body_only, raw_css = split_for_omnisend_visual_builder(html)

    stem = full_html_path.stem
    body_path = target_dir / f"{stem}_body_only.html"
    css_path = target_dir / f"{stem}_styles_only.css"
    body_path.write_text(body_only, encoding="utf-8")
    css_path.write_text(raw_css, encoding="utf-8")
    return body_path, css_path


def format_report(report: LintReport) -> str:
    status = "PASS" if report.passed else "FAIL"
    lines = [
        f"[{status}] {report.path.name}",
        f"       HTML Size: {report.byte_length:,} / {MAX_HTML_BYTES_STUDIO:,} B "
        f"| <style>: {report.style_chars:,} / {MAX_STYLE_CHARS_GMAIL:,} chars "
        f"| Max nowrap: {report.max_nowrap_len} chars ('{report.max_nowrap_text}')",
    ]
    for w in report.warnings:
        lines.append(f"       [WARN] {w}")
    for e in report.errors:
        lines.append(f"       [ERR]  {e}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("Usage: python chaphavian_html_linter_and_spec.py <html_file_1> [html_file_2 ...] [--split]")
        return 1

    do_split = "--split" in args
    files = [Path(a) for a in args if a != "--split"]
    any_failed = False

    for f in files:
        rep = lint_html_file(f)
        print(format_report(rep))
        if not rep.passed:
            any_failed = True
        elif do_split:
            b_path, c_path = write_omnisend_visual_builder_pair(f)
            print(f"       [SPLIT] Body -> {b_path.name} | Styles -> {c_path.name}")

    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
