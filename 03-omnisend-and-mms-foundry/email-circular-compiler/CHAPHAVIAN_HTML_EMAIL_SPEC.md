# NeverRender Labs // Chaphavian & Omnisend HTML Email Engineering Spec

Reusable studio engineering standard for hand-coded responsive HTML email tables imported into **Omnisend** and rendered across **Gmail Desktop Web**, **Gmail Android / iOS**, **Apple Mail**, **Samsung Mail**, **ProtonMail (Light & Dark Mode)**, and **Classic Outlook**.

Validated automatically by [`chaphavian_html_linter_and_spec.py`](./chaphavian_html_linter_and_spec.py) and implemented in [`compile_chaphavian_automation_emails.py`](./compile_chaphavian_automation_emails.py).

---

## 1. Table Width, Column & Character Count Benchmarks

| Layout Element | Desktop Spec | Mobile Spec (`320px` Floor) | Technical Rationale |
| :--- | :--- | :--- | :--- |
| **Outer Frame Table** | `width="100%"` + `max-width:600px` | `width:98%` (`320px` to `480px`) | Omit fixed `width="600"` HTML attributes so Samsung Mail's auto-fit parser never locks the mobile viewport wide. |
| **Inner Reading Measure** | `480px` ideal (`520px` max) | `260px` to `290px` live width | Delivers the `~66` character desktop reading measure and `35` to `45` character mobile measure (`39` avg at `320px`) in `16px` serif. |
| **Multi-Column Grids** | `2 columns` (`48.5%` + `3%` gutter) | `1 column` stacked (`100%`) | Never exceed `2` columns for luxury gallery cards; stack `.tcc-grid-col` to `display:block; width:100% !important;` below `520px`. |
| **Caption Sub-Tables** | `max-width:480px` | `100%` fluid (`260px` to `290px`) | Never hardcode `width="400"`, which pinches captions below the `35`-character mobile floor. |
| **Body Copy Typography** | `16px-16.5px` serif, `1.5-1.72` LH, left-aligned | `14px` min (`16px` ideal), `1.45+` LH | Include `-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;` inline on `<body>` so iOS Mail does not auto-inflate `< 13px` labels. |
| **Unbreakable `nowrap` Spans** | `22` chars ideal (`24` hard max) | `22` chars ideal (`24` hard max) | Nested paddings leave only `225px` to `235px` (`28` to `34` chars) on a `320px` phone; keeping `nowrap` spans `<= 22-24` chars prevents border piercing. |
| **Retina `2x` Art & Weight** | `1088px` `2x` sRGB progressive JPG | `544px` display cap (`width="544"`) | Keep email JPEGs `< 200-350 KB` and raw HTML `< 75 KB` (Gmail clips footers and unsubscribe links above `102 KB`). |

---

## 2. Omnisend & Gmail Parser Invariants

1. **Omnisend Dual-Path Import**:
   - **Standalone Broadcasts**: Import full HTML via `Store Settings -> Saved Templates -> Import Template -> Paste in code` (zero `24px` `#FFFFFF` Visual Builder wrapper).
   - **Visual Builder Automations**: Set outer section padding to `0px` (`#D5D3CC` background), paste `*_body_only.html` into the **HTML** box, and paste `*_styles_only.css` (no `<style>` wrapper tags) into the **Styles** tab.
2. **Gmail `8,192-Character` `<style>` Sanitizer**:
   - Never use `:root`, `var(--...)`, `clamp()`, `@media (prefers-color-scheme: dark)`, `supported-color-schemes:` inside `<style>`, `@import`, CSS `url(...)`, or external `<link rel="stylesheet">` tags. Any single violation causes Gmail to strip the entire `<style>` block.
3. **Omnisend Named-Entity Slice-Offset Bug**:
   - Never use HTML character entities (`&amp;`, `&middot;`, `&nbsp;`, `&zwnj;`, `&#...;`). Omnisend's entity decoder miscomputes UTF-8 offsets and duplicates trailing characters (`Collectiontion`, `Chandeliersrs`). Use plain UTF-8 (`·`) or 7-bit ASCII (`and`, `|`).
4. **Contiguous Single-Line `.tcc-subnav` + Progressive Desktop Enhancement**:
   - Keep `<a>` and `<span class="tcc-subnav-pipe">|</span>` tags contiguous on a single line with zero inter-tag newlines, inline `font-size:7.5px;letter-spacing:0px;` (`~228px` mobile safe width), and `@media only screen and (min-width: 521px)` upscaling to `9px` alongside `.tcc-desk-pipe` (`display:inline !important`) and `.tcc-stack-br` (`display:none !important`).

---

## 3. CLI Usage

```powershell
python 03-omnisend-and-mms-foundry/email-circular-compiler/chaphavian_html_linter_and_spec.py --split <template.html>
```
