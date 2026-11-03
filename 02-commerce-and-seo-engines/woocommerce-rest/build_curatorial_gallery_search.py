#!/usr/bin/env python3
"""
Compile the Complete End-to-End Mansour-Style Two-Tier Click-Flow & White-Glove Checkout Prototype
for The Chapman Collection (`thechapmancollection.com`), powered by all 113 live WooCommerce products
plus the 3 new studio-slate flagship furniture pieces (116 total).

Architecture & Click-Flow:
1. Header:
   - Centered Crest + THE CHAPMAN COLLECTION (Cormorant Garamond, tracked uppercase)
   - Clean nav: HOME | GALLERY | MEET MELISSA | SERVICES | CURATE YOUR COLLECTION | SELECTION (N)
   - Zero big black phone icon next to Contact; zero filler/boilerplate pages.
2. View 1 — HOME (Landing Experience, ZERO Prices, ZERO Add-to-Cart):
   - Goodbye 2023 AI Green Couch -> Sliding Mansour Split Hero Carousel:
     - Slide 1: Hero Furniture on `pmc-slate-curved-backdrop.jpg` (Spanish Knights Armoire, English Tall Gothic Hallstand, Napoleon III Boulle Credenza) + minimalist off-greige geometric block (`#C4BEB4`) with `[ Curate Your Collection ]`.
     - Slide 2: Macro Collage of Persian & Silk Carpet Weaves + minimalist slate-stone geometric block (`#9EA9B2`) with `[ Curate Your Collection ]`.
     - Slide 3: Collage of Fine Bronzes, Sèvres Porcelain & Giltwood Trinkets on Slate + minimalist warm taupe block (`#B6AFA5`) with `[ Curate Your Collection ]`.
   - Mansour-Style Editorial Welcome Paragraph (with inline phone/concierge links).
   - Asymmetric `Featured Carpets & Tapestries` Collage Splash (`1fr : 2fr : 1fr` -> `1fr : 1fr` -> `1fr : 2fr : 1fr`) — clicking any tile routes into the Curate console filtered to that weave.
3. View 2 — GALLERY (Categorized Editorial Lookbook Slides, ZERO Prices, ZERO Add-to-Cart):
   - Horizontal categorized gallery sliders (`European Period Furniture`, `Court & Village Carpets`, `Flemish & Aubusson Tapestries`, `Fine Art, Bronzes & Peculiars`) over a minimalist off-greige stage.
   - Clicking any piece opens a clean Editorial Provenance Modal (no price, no cart button) with a single CTA: `[ Curate & Inquire in Collection Vault -> ]`.
4. View 3 — CURATE YOUR COLLECTION (The Itemized Search & Acquisition Vault):
   - Full Mansour filter console: Category boxes, 10 Color Swatches, Historical Period pills, `FT`/`CM` live dimension inputs, Keyword search.
   - ONLY inside this view do itemized prices (`$6,800` -> `$4,800`) and `+ Add to Selection` / `Acquire Piece` buttons appear!
5. View 4 — FULL WHITE-GLOVE CHECKOUT EXPERIENCE:
   - Slide-over Curated Selection Drawer + Full-Page Private Showroom Checkout:
     - Collector & Designer Details (with Optional Trade / ASID Tax-Exempt Resale ID toggle)
     - 3 White-Glove Fulfillment Modes:
       1. Complimentary Rancho Santa Fe Showroom Pickup (`6014 La Granada`)
       2. Complimentary 48-Hour Southern California In-Home Preview (Rancho Santa Fe / La Jolla / Del Mar / Newport)
       3. Client-Arranged Domestic or International White-Glove Carrier (Coordinated Post-Purchase)
     - Payment Method (Credit/Debit Card, Private Bank Wire / ACH with 3% Cash-Equivalent Courtesy, or Hold on 24-Hour Showroom Approval)
     - Instant Interactive Order Confirmation Dossier (`TCC-RSF-2026-XXXX`).
"""

import os
import re
import json
import shutil

SNAPSHOT_PATH = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\02-clean-master-database\inventory_snapshot.json"
SLATE_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\inspo-gustavian-eloquence-2026-11-02\pmc-custom-backdrops-preview"
CHALK_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\inspo-gustavian-eloquence-2026-11-02\gustavian-chalk-lightened"
OUT_DIR_NRL = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\chapman-curatorial-gallery-search"
OUT_FILE_PMC = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\chapman-curatorial-gallery-search.html"

COLOR_SWATCHES = [
    {"id": "walnut",     "label": "Walnut & Chestnut",   "hex": "#7D6256", "keywords": ["walnut", "mahogany", "oak", "chestnut", "wood", "brown", "carved", "giltwood", "teak", "cherry", "burl", "camel", "tan"]},
    {"id": "terracotta", "label": "Terracotta & Rust",   "hex": "#CE644A", "keywords": ["terracotta", "rust", "coral", "salmon", "copper", "brick", "burnt orange", "persimmon", "madder", "henna"]},
    {"id": "crimson",    "label": "Ruby & Crimson",      "hex": "#9E2A2B", "keywords": ["red", "crimson", "ruby", "burgundy", "claret", "wine", "carmine", "scarlet", "garnet", "rose"]},
    {"id": "ivory",      "label": "Ivory & Parchment",   "hex": "#F4EE9E", "keywords": ["ivory", "cream", "beige", "parchment", "alabaster", "white", "bone", "ecru", "champagne", "marble"]},
    {"id": "gold",       "label": "Ochre & Gilt Gold",   "hex": "#F7E600", "keywords": ["gold", "gilt", "ochre", "saffron", "yellow", "brass", "ormolu", "amber", "mustard", "honey", "bronze"]},
    {"id": "sage",       "label": "Sage & Celadon",      "hex": "#8ABF7F", "keywords": ["green", "sage", "celadon", "olive", "emerald", "moss", "forest", "jade", "pistachio", "foliage", "verdure"]},
    {"id": "sky",        "label": "Ice & Cerulean Blue", "hex": "#74C0FC", "keywords": ["light blue", "sky blue", "ice blue", "powder blue", "turquoise", "aqua", "cerulean", "teal", "robin", "blue"]},
    {"id": "navy",       "label": "Royal & Indigo",      "hex": "#4C6EF5", "keywords": ["navy", "indigo", "midnight", "cobalt", "sapphire", "royal blue", "lapis", "prussian"]},
    {"id": "plum",       "label": "Aubergine & Mauve",   "hex": "#7F5F99", "keywords": ["plum", "aubergine", "purple", "violet", "lavender", "mauve", "amethyst", "lilac", "mulberry"]},
    {"id": "charcoal",   "label": "Charcoal & Ebony",    "hex": "#666664", "keywords": ["black", "ebony", "charcoal", "slate", "iron", "graphite", "dark", "steel", "pewter", "silver"]},
]

PERIOD_BUCKETS = [
    {"id": "17th", "label": "17th Century & Earlier", "patterns": [r"15th", r"16th", r"17th", r"14\d\d", r"15\d\d", r"16\d\d", r"renaissance", r"gothic", r"tudor", r"jacobean"]},
    {"id": "18th", "label": "18th Century",           "patterns": [r"18th", r"17\d\d", r"louis xv", r"louis xvi", r"georgian", r"chippendale", r"queen anne", r"rococo"]},
    {"id": "19th", "label": "19th Century",           "patterns": [r"19th", r"18\d\d", r"victorian", r"napoleon", r"empire", r"regency", r"biedermeier", r"meiji", r"qajar", r"late 19th"]},
    {"id": "20th", "label": "Early 20th Century",     "patterns": [r"20th", r"190\d", r"191\d", r"192\d", r"193\d", r"194\d", r"195\d", r"art deco", r"art nouveau", r"edwardian", r"mid-century", r"vintage"]},
]


def strip_html(text):
    if not text:
        return ""
    return re.sub(r"<[^>]+>", " ", text)


def parse_dimensions_feet(name, desc, dims_obj):
    combined = f"{name} {strip_html(desc)}"
    m_ft = re.search(
        r"(\d{1,2})\s*['\u2032\u2019]\s*(?:(\d{1,2})\s*[\"\u2033\u201d]?)?\s*[xX\u00d7]\s*(\d{1,2})\s*['\u2032\u2019]\s*(?:(\d{1,2})\s*[\"\u2033\u201d]?)?",
        combined
    )
    if m_ft:
        f1 = int(m_ft.group(1)) + (int(m_ft.group(2)) / 12.0 if m_ft.group(2) else 0.0)
        f2 = int(m_ft.group(3)) + (int(m_ft.group(4)) / 12.0 if m_ft.group(4) else 0.0)
        w_ft, l_ft = min(f1, f2), max(f1, f2)
        s1 = f"{m_ft.group(1)}'{m_ft.group(2)}\"" if m_ft.group(2) else f"{m_ft.group(1)}'"
        s2 = f"{m_ft.group(3)}'{m_ft.group(4)}\"" if m_ft.group(4) else f"{m_ft.group(3)}'"
        return round(w_ft, 2), round(l_ft, 2), f"{s1} x {s2}"

    m_in = re.search(
        r"(\d{1,3}(?:\.\d+)?)\s*(?:[\"\u2033\u201d]|in(?:ches)?)\s*(?:[HWDL]\s*)?[xX\u00d7]\s*(\d{1,3}(?:\.\d+)?)\s*(?:[\"\u2033\u201d]|in(?:ches)?)",
        combined,
        re.I
    )
    if m_in:
        i1 = float(m_in.group(1))
        i2 = float(m_in.group(2))
        w_ft = round(min(i1, i2) / 12.0, 2)
        l_ft = round(max(i1, i2) / 12.0, 2)
        return w_ft, l_ft, f'{m_in.group(1)}" x {m_in.group(2)}"'

    if isinstance(dims_obj, dict):
        try:
            w = float(dims_obj.get("width") or 0)
            l = float(dims_obj.get("length") or dims_obj.get("height") or 0)
            if w > 0 and l > 0:
                w_ft = round(min(w, l) / 12.0, 2)
                l_ft = round(max(w, l) / 12.0, 2)
                return w_ft, l_ft, f'{int(w)}" x {int(l)}"'
        except Exception:
            pass

    return None, None, ""


def classify_top_category(cats, name):
    cat_set = {c.lower() for c in cats}
    nl = name.lower()
    if any(k in cat_set for k in ["carpets", "large carpet", "small carpet", "runner"]) or any(w in nl for w in ["carpet", "rug", "runner", "kilim"]):
        if "runner" in cat_set or "runner" in nl:
            return "CARPETS & RUNNERS", "Runners"
        elif "small carpet" in cat_set:
            return "CARPETS & RUNNERS", "Small & Area Carpets"
        return "CARPETS & RUNNERS", "Room & Palace Carpets"
    if any(k in cat_set for k in ["tapestry", "artwork & tapestries"]) and ("tapestry" in cat_set or "tapestry" in nl):
        return "TAPESTRIES", "Tapestries"
    if any(k in cat_set for k in ["furniture", "cabinets", "cabinets and consoles", "seating", "tables", "tables and office desks"]) or any(w in nl for w in ["cabinet", "armoire", "chair", "settee", "table", "desk", "console", "chest", "commode", "vitrine", "bench"]):
        return "EUROPEAN FURNITURE", "European Furniture"
    if any(k in cat_set for k in ["classic artwork", "modern artwork", "artwork & tapestries"]) or any(w in nl for w in ["painting", "oil on", "lithograph", "watercolor", "portrait"]):
        return "FINE ART", "Fine Art & Paintings"
    if any(k in cat_set for k in ["bronzes", "statuaries"]) or any(w in nl for w in ["bronze", "marble", "statue", "sculpture", "bust"]):
        return "BRONZES & SCULPTURE", "Bronzes & Sculpture"
    return "DECORATIVE ARTS", "Mirrors, Porcelain & Objects"


def main():
    with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    os.makedirs(os.path.join(OUT_DIR_NRL, "assets"), exist_ok=True)
    # Copy the 3 Slate Curved studio cutouts + 2 Airy Chalk cutouts into assets/
    for fn in [
        "spanish-knights-cabinet-slate-curved.jpg",
        "english-gothic-hallstand-slate-curved.jpg",
        "boulle-marquetry-credenza-slate-curved.jpg",
    ]:
        src_p = os.path.join(SLATE_DIR, fn)
        if os.path.exists(src_p):
            shutil.copy2(src_p, os.path.join(OUT_DIR_NRL, "assets", fn))

    for fn in ["spanish-knights-cabinet-airy-chalk.jpg", "english-gothic-hallstand-airy-chalk.jpg"]:
        src_p = os.path.join(CHALK_DIR, fn)
        if os.path.exists(src_p):
            shutil.copy2(src_p, os.path.join(OUT_DIR_NRL, "assets", fn))

    catalog = [
        {
            "id": 9901,
            "name": "Antique Spanish Carved Walnut Armoire with Conquistador Knights",
            "url": "https://thechapmancollection.com/",
            "image": "assets/spanish-knights-cabinet-slate-curved.jpg",
            "top_category": "EUROPEAN FURNITURE",
            "sub_category": "18th Century Spanish Case Piece",
            "all_categories": ["Furniture", "Cabinets and Consoles"],
            "colors": ["walnut"],
            "periods": ["17th", "18th"],
            "w_ft": 6.63,
            "l_ft": 6.98,
            "size_label": '83.75" H x 79.5" W x 25.75" D',
            "regular_price": "6800",
            "sale_price": "4800",
            "active_price": "4800",
            "search_blob": "antique spanish carved walnut armoire cabinet with conquistador knights 83.75 x 79.5 furniture",
        },
        {
            "id": 9902,
            "name": "Monumental English Carved Oak Tall Gothic Hallstand with Mirror & Bench",
            "url": "https://thechapmancollection.com/",
            "image": "assets/english-gothic-hallstand-slate-curved.jpg",
            "top_category": "EUROPEAN FURNITURE",
            "sub_category": "19th Century English Architectural Hallstand",
            "all_categories": ["Furniture", "Cabinets and Consoles"],
            "colors": ["walnut", "gold"],
            "periods": ["19th"],
            "w_ft": 6.92,
            "l_ft": 9.75,
            "size_label": '117" H x 83" W x 16" D',
            "regular_price": "12800",
            "sale_price": "9800",
            "active_price": "9800",
            "search_blob": "monumental english carved oak tall gothic hallstand mirror bench 117 x 83 furniture",
        },
        {
            "id": 9903,
            "name": "Napoleon III Ebonized Pearwood & Floral Marquetry Vitrine Credenza with Ormolu Mounts",
            "url": "https://thechapmancollection.com/",
            "image": "assets/boulle-marquetry-credenza-slate-curved.jpg",
            "top_category": "EUROPEAN FURNITURE",
            "sub_category": "19th Century French Boulle & Marquetry",
            "all_categories": ["Furniture", "Cabinets and Consoles"],
            "colors": ["charcoal", "gold", "walnut"],
            "periods": ["19th"],
            "w_ft": 3.50,
            "l_ft": 4.75,
            "size_label": '44" H x 57" W x 18" D',
            "regular_price": "8900",
            "sale_price": "6800",
            "active_price": "6800",
            "search_blob": "napoleon iii ebonized pearwood floral marquetry vitrine credenza ormolu mounts french furniture",
        },
    ]

    for pid, p in raw.items():
        if p.get("status") != "publish":
            continue
        name = p.get("name", "").strip()
        desc = p.get("description", "") or ""
        short_desc = p.get("short_description", "") or ""
        cats = [c if isinstance(c, str) else c.get("name", "") for c in p.get("categories", [])]
        tags = [t if isinstance(t, str) else t.get("name", "") for t in p.get("tags", [])]
        haystack = f"{name} {strip_html(short_desc)} {strip_html(desc)} {' '.join(cats)} {' '.join(tags)}".lower()

        top_cat, sub_cat = classify_top_category(cats, name)

        matched_colors = []
        for sw in COLOR_SWATCHES:
            if any(re.search(r"\b" + re.escape(kw) + r"\b", haystack) for kw in sw["keywords"]):
                matched_colors.append(sw["id"])
        if not matched_colors:
            if top_cat == "EUROPEAN FURNITURE":
                matched_colors.append("walnut")
            elif top_cat == "BRONZES & SCULPTURE":
                matched_colors.append("gold")
            else:
                matched_colors.append("ivory")

        matched_periods = []
        for pb in PERIOD_BUCKETS:
            if any(re.search(pat, haystack) for pat in pb["patterns"]):
                matched_periods.append(pb["id"])
        if not matched_periods:
            matched_periods.append("19th")

        w_ft, l_ft, size_label = parse_dimensions_feet(name, short_desc + " " + desc, p.get("dimensions"))

        images = p.get("images", [])
        img_url = ""
        if images:
            first_img = images[0]
            img_url = first_img if isinstance(first_img, str) else first_img.get("src", "")

        reg_price = str(p.get("regular_price") or p.get("active_price") or "").strip()
        sale_price = str(p.get("sale_price") or "").strip()
        active_price = str(p.get("active_price") or reg_price or "").strip()

        catalog.append({
            "id": int(pid),
            "name": name,
            "url": p.get("permalink", f"https://thechapmancollection.com/?p={pid}"),
            "image": img_url,
            "top_category": top_cat,
            "sub_category": sub_cat,
            "all_categories": cats,
            "colors": matched_colors,
            "periods": matched_periods,
            "w_ft": w_ft,
            "l_ft": l_ft,
            "size_label": size_label,
            "regular_price": reg_price,
            "sale_price": sale_price,
            "active_price": active_price,
            "search_blob": f"{name} {' '.join(cats)} {' '.join(tags)} {size_label}".lower(),
        })

    print(f"Compiled {len(catalog)} total curated pieces.")

    catalog_json = json.dumps(catalog, ensure_ascii=False)
    swatches_json = json.dumps(COLOR_SWATCHES, ensure_ascii=False)
    periods_json = json.dumps(PERIOD_BUCKETS, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Chapman Collection | Rancho Santa Fe &amp; London Heritage</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #FFFFFF;
    --off-greige: #F4F1EC;
    --greige-panel: #C2BCB2;
    --slate-panel: #9CA6B0;
    --taupe-panel: #AFA9A0;
    --text-main: #1E1D1B;
    --text-muted: #524F4A;
    --text-italic-hint: #5A7496;
    --border-hairline: #CFCAC0;
    --border-active: #232220;
    --gold-accent: #8C7044;
    --studio-grey-card: #F6F5F2;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    background-color: #FAF8F5;
    color: var(--text-main);
    font-family: 'Cormorant Garamond', Georgia, serif;
    -webkit-font-smoothing: antialiased;
    line-height: 1.5;
    overflow-x: hidden;
    position: relative;
  }}

  /* Layer 1 of NRL Curtain Draft: Strictly z-index: 0 behind all foreground cards & photos */
  .nrl-curtain-draft-canvas {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    z-index: 0;
    display: block;
  }}

  .nrl-linen-tooth-overlay {{
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.022;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='linenTooth'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23linenTooth)'/%3E%3C/svg%3E");
  }}

  /* Ensure all foreground sections sit cleanly at z-index: 10 above the curtain draft canvas */
  .flow-status-bar,
  .site-view,
  .hero-stage-wrap,
  .mansour-editorial-intro,
  .collage-splash-wrap,
  .gallery-lookbook-stage,
  .console-wrap,
  .results-wrapper,
  .checkout-wrap,
  .site-footer-wrap {{
    position: relative;
    z-index: 10;
  }}

  /* Interactive Flow Switcher Pill Bar (Top Sticky Demo Helper) */
  .flow-status-bar {{
    background: #1D1C1A;
    color: #EAE6DF;
    padding: 8px 20px;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }}
  .flow-steps {{
    display: flex;
    gap: 8px;
    align-items: center;
    flex-wrap: wrap;
  }}
  .flow-step-pill {{
    padding: 4px 10px;
    border: 1px solid rgba(255,255,255,0.22);
    color: #CCC8C0;
    cursor: pointer;
    background: transparent;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    transition: all 0.2s ease;
  }}
  .flow-step-pill.active, .flow-step-pill:hover {{
    background: #EAE6DF;
    color: #1D1C1A;
    border-color: #EAE6DF;
    font-weight: 500;
  }}

  /* Centered Crest + Mansour-Style Header (No Giant Phone Icon Next to Contact!) */
  .brand-header {{
    text-align: center;
    padding: 26px 20px 22px;
    border-bottom: 1px solid var(--border-hairline);
    background: #FFFFFF;
    position: sticky;
    top: 0;
    z-index: 90;
    transition: transform 0.34s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.25s ease;
    will-change: transform;
  }}
  .brand-header.header-tucked {{
    transform: translateY(-105%);
    pointer-events: none;
  }}
  .brand-header.header-scrolled {{
    box-shadow: 0 4px 18px rgba(30, 29, 27, 0.06);
  }}
  .brand-crest {{
    width: 68px;
    height: auto;
    margin: 0 auto 8px;
    display: block;
    cursor: pointer;
  }}
  .brand-title {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-weight: 400;
    font-size: 32px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #1F1F1E;
    margin-bottom: 4px;
    cursor: pointer;
  }}
  .brand-subtitle {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: 14px;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 18px;
  }}

  /* Whisper-Quiet Navigation Bar */
  .main-nav {{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 30px;
    list-style: none;
  }}
  .main-nav a {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 14px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #555553;
    text-decoration: none;
    padding-bottom: 4px;
    border-bottom: 1px solid transparent;
    transition: all 0.2s ease;
    cursor: pointer;
  }}
  .main-nav a:hover,
  .main-nav a.active {{
    color: #111111;
    border-bottom-color: #111111;
  }}
  .nav-curate-cta {{
    padding: 6px 14px !important;
    border: 1px solid #3A3835 !important;
    color: #1F1F1E !important;
    font-weight: 500;
  }}
  .nav-curate-cta:hover, .nav-curate-cta.active {{
    background: #232220 !important;
    color: #FFFFFF !important;
  }}
  .nav-selection-pill {{
    font-family: 'Montserrat', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 0.14em !important;
    color: #232220 !important;
    background: var(--off-greige);
    padding: 6px 13px !important;
    border: 1px solid var(--border-hairline) !important;
  }}

  /* Views Management */
  .site-view {{
    display: none;
    animation: fadeInView 0.35s ease;
  }}
  .site-view.active {{
    display: block;
  }}
  @keyframes fadeInView {{
    from {{ opacity: 0; transform: translateY(4px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}

  /* ==========================================================================
     VIEW 1: HOME (MANSOUR SPLIT HERO CAROUSEL + COLLAGE SPLASH, ZERO PRICES)
     ========================================================================== */
  .hero-stage-wrap {{
    max-width: 1180px;
    margin: 28px auto 0;
    padding: 0 24px;
  }}
  .hero-carousel {{
    position: relative;
    width: 100%;
    height: 490px;
    overflow: hidden;
    background: var(--off-greige);
    border: 1px solid var(--border-hairline);
  }}
  .hero-slide {{
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-columns: 64% 36%;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.65s ease;
  }}
  .hero-slide.active {{
    opacity: 1;
    pointer-events: auto;
  }}

  /* Slide Left Visual Stage */
  .hero-visual-stage {{
    position: relative;
    width: 100%;
    height: 100%;
    background: var(--off-greige);
    overflow: hidden;
  }}
  /* Slide 1: 3-Piece Hero Furniture Triptych on Slate Curved Backdrop */
  .hero-furniture-triptych {{
    display: grid;
    grid-template-columns: 1.05fr 1fr 1.05fr;
    gap: 5px;
    width: 100%;
    height: 100%;
    background: #FFFFFF;
  }}
  .hero-furniture-card {{
    position: relative;
    height: 100%;
    overflow: hidden;
    background: #C4C7CA;
    cursor: pointer;
  }}
  .hero-furniture-card img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.65s ease;
  }}
  .hero-furniture-card:hover img {{
    transform: scale(1.04);
  }}
  .hero-furniture-tag {{
    position: absolute;
    bottom: 12px;
    left: 12px;
    right: 12px;
    background: rgba(29, 28, 26, 0.72);
    backdrop-filter: blur(4px);
    color: #F6F4F0;
    padding: 6px 10px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 13px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
  }}

  /* Slide 2 & 3: Macro Collage Grid Over Minimalist Off-Greige */
  .hero-macro-collage {{
    display: grid;
    grid-template-columns: 1.35fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 5px;
    width: 100%;
    height: 100%;
    background: #FFFFFF;
  }}
  .hero-macro-cell {{
    position: relative;
    overflow: hidden;
    background: var(--off-greige);
    cursor: pointer;
  }}
  .hero-macro-cell.tall {{
    grid-row: 1 / span 2;
  }}
  .hero-macro-cell img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.65s ease;
  }}
  .hero-macro-cell:hover img {{
    transform: scale(1.05);
  }}

  /* Slide Right Mansour Geometric Color-Block Panel */
  .hero-colorblock-panel {{
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 42px 34px;
    text-align: center;
    color: #FFFFFF;
    overflow: hidden;
  }}
  /* Subtle Mansour-style translucent geometric rectangles inside right panel */
  .hero-colorblock-panel::before {{
    content: "";
    position: absolute;
    top: -30px;
    left: 28px;
    width: 170px;
    height: 160px;
    background: rgba(255, 255, 255, 0.09);
    pointer-events: none;
  }}
  .hero-colorblock-panel::after {{
    content: "";
    position: absolute;
    bottom: 24px;
    right: 28px;
    width: 190px;
    height: 150px;
    background: rgba(255, 255, 255, 0.08);
    pointer-events: none;
  }}
  .panel-slate-greige {{ background-color: #9FA8B0; }}
  .panel-warm-greige  {{ background-color: #B8B1A6; }}
  .panel-gustavian    {{ background-color: #A6A29A; }}

  .hero-kicker {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.88);
    margin-bottom: 14px;
    position: relative;
    z-index: 2;
  }}
  .hero-panel-title {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-weight: 400;
    font-size: 36px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #FFFFFF;
    line-height: 1.2;
    margin-bottom: 14px;
    position: relative;
    z-index: 2;
  }}
  .hero-panel-sub {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: 17px;
    color: rgba(255,255,255,0.92);
    max-width: 290px;
    margin-bottom: 28px;
    position: relative;
    z-index: 2;
  }}
  .hero-curate-btn {{
    position: relative;
    z-index: 2;
    background: #FFFFFF;
    color: #232220;
    border: 1px solid #FFFFFF;
    padding: 13px 26px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 14px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.25s ease;
  }}
  .hero-curate-btn:hover {{
    background: #232220;
    color: #FFFFFF;
    border-color: #232220;
  }}

  /* ==========================================================================
     THE NRL SUBTLE TOUCH: WEBGL SILK CAUSTICS + DIRECTIONAL GALLERY SPOTLIGHT
     ========================================================================== */
  .nrl-silk-webgl-canvas {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
    opacity: 0.55;
    mix-blend-mode: soft-light;
  }}
  .nrl-spotlight-surface {{
    position: relative;
    overflow: hidden;
  }}
  .nrl-spotlight-surface::after {{
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 3;
    opacity: 0;
    transition: opacity 0.4s ease;
    background: radial-gradient(
      340px circle at var(--spot-x, 50%) var(--spot-y, 50%),
      rgba(255, 248, 231, 0.22) 0%,
      rgba(218, 195, 148, 0.08) 42%,
      rgba(255, 255, 255, 0) 72%
    );
    mix-blend-mode: screen;
  }}
  .nrl-spotlight-surface:hover::after {{
    opacity: 1;
  }}
  .nrl-atelier-colophon {{
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px solid rgba(207, 202, 192, 0.55);
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #8A867E;
  }}
  .nrl-atelier-colophon a {{
    color: #524F4A;
    text-decoration: none;
    border-bottom: 1px solid rgba(82, 79, 74, 0.35);
    padding-bottom: 1px;
    transition: color 0.2s ease, border-color 0.2s ease;
  }}
  .nrl-atelier-colophon a:hover {{
    color: #1E1D1B;
    border-bottom-color: #1E1D1B;
  }}

  /* Carousel Dots & Arrows */
  .hero-controls {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 4px 0;
  }}
  .hero-dots {{
    display: flex;
    gap: 10px;
  }}
  .hero-dot {{
    width: 28px;
    height: 3px;
    background: #D6D3CD;
    border: none;
    cursor: pointer;
    transition: background 0.2s ease;
  }}
  .hero-dot.active {{
    background: #232220;
  }}
  .hero-arrows {{
    display: flex;
    gap: 14px;
  }}
  .hero-arrow {{
    background: none;
    border: 1px solid var(--border-hairline);
    padding: 4px 12px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-main);
    cursor: pointer;
  }}
  .hero-arrow:hover {{
    border-color: var(--text-main);
  }}

  /* Mansour-Style Editorial Welcome Copy (Replaces Header Phone Clutter) */
  .mansour-editorial-intro {{
    max-width: 1180px;
    margin: 34px auto 40px;
    padding: 0 24px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 19px;
    line-height: 1.75;
    color: #4A4845;
  }}
  .mansour-editorial-intro p + p {{
    margin-top: 16px;
  }}
  .mansour-editorial-intro a {{
    color: #232220;
    text-decoration: underline;
    text-underline-offset: 3px;
  }}

  /* MANSOUR-STYLE ASYMMETRIC COLLAGE SPLASH */
  .collage-splash-wrap {{
    max-width: 1180px;
    margin: 10px auto 56px;
    padding: 0 24px;
  }}
  .collage-splash-heading {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 15px;
    font-weight: 400;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 14px;
  }}
  .collage-row-3 {{
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 5px;
    margin-bottom: 5px;
  }}
  .collage-row-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    margin-bottom: 5px;
  }}
  .collage-tile {{
    position: relative;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    overflow: hidden;
    background: var(--studio-grey-card);
    text-decoration: none;
  }}
  .collage-tile-img-wrap {{
    width: 100%;
    height: 300px;
    overflow: hidden;
    background: #F4F2EE;
  }}
  .collage-tile-img-wrap img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.55s ease;
  }}
  .collage-tile:hover .collage-tile-img-wrap img {{
    transform: scale(1.04);
  }}
  .collage-caption-bar {{
    background-color: #AFA9A0;
    color: #FFFFFF;
    text-align: center;
    padding: 8px 12px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    transition: background-color 0.25s ease;
  }}
  .collage-tile:hover .collage-caption-bar {{
    background-color: #8E877E;
  }}

  /* ==========================================================================
     VIEW 2: GALLERY (CATEGORIZED LOOKBOOK SLIDES OVER MINIMALIST OFF-GREIGE, ZERO PRICES)
     ========================================================================== */
  .gallery-lookbook-stage {{
    background: var(--off-greige);
    padding: 44px 0 64px;
    border-bottom: 1px solid var(--border-hairline);
  }}
  .lookbook-container {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 24px;
  }}
  .lookbook-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 36px;
    padding-bottom: 18px;
    border-bottom: 1px solid #DCD7CE;
  }}
  .lookbook-top-bar h2 {{
    font-weight: 400;
    font-size: 28px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #1F1F1E;
  }}
  .lookbook-top-bar p {{
    font-style: italic;
    font-size: 16px;
    color: var(--text-muted);
    margin-top: 4px;
  }}
  .lookbook-chapter {{
    margin-bottom: 48px;
  }}
  .chapter-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }}
  .chapter-title {{
    font-size: 19px;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #232220;
  }}
  .chapter-Controls {{
    display: flex;
    gap: 10px;
    align-items: center;
  }}
  .chapter-curate-link {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #232220;
    background: #FFFFFF;
    border: 1px solid #C9C4BA;
    padding: 7px 14px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .chapter-curate-link:hover {{
    background: #232220;
    color: #FFFFFF;
    border-color: #232220;
  }}
  .chapter-track {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
  }}
  .lookbook-card {{
    background: #FFFFFF;
    border: 1px solid #E5E0D8;
    padding: 14px 14px 18px;
    cursor: pointer;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    text-align: center;
  }}
  .lookbook-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(35,34,32,0.06);
  }}
  .lookbook-img-box {{
    width: 100%;
    aspect-ratio: 1 / 1;
    background: var(--studio-grey-card);
    overflow: hidden;
    margin-bottom: 12px;
  }}
  .lookbook-img-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.45s ease;
  }}
  .lookbook-card:hover .lookbook-img-box img {{
    transform: scale(1.04);
  }}
  .lookbook-cat {{
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
  }}
  .lookbook-name {{
    font-size: 16px;
    font-weight: 500;
    color: #1F1F1E;
    line-height: 1.3;
    margin-bottom: 4px;
  }}
  .lookbook-dims {{
    font-style: italic;
    font-size: 13px;
    color: var(--text-muted);
  }}

  /* ==========================================================================
     VIEW 3: CURATE YOUR COLLECTION (ITEMIZED SEARCH + UNLOCKED PRICES + SELECTION)
     ========================================================================== */
  .console-wrap {{
    max-width: 1060px;
    margin: 0 auto;
    padding: 40px 24px 24px;
  }}
  .console-lead {{
    font-size: 26px;
    font-weight: 400;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #2B2B2A;
    margin-bottom: 8px;
  }}
  .filter-section {{
    margin-bottom: 30px;
  }}
  .filter-label {{
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #3A3A38;
    margin-bottom: 4px;
  }}
  .filter-subhint {{
    font-style: italic;
    font-size: 14px;
    color: var(--text-italic-hint);
    margin-bottom: 12px;
  }}

  .category-bar {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
    margin-top: 10px;
  }}
  .cat-tile {{
    border: 1px solid var(--border-hairline);
    background: #FFFFFF;
    padding: 16px 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4A4A48;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 78px;
  }}
  .cat-tile span.cat-count {{
    display: block;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.1em;
    color: #999995;
    margin-top: 6px;
  }}
  .cat-tile:hover {{
    border-color: #8E8A80;
    box-shadow:
      inset 2px 2px 6px rgba(95, 86, 72, 0.08),
      inset -2px -2px 6px rgba(255, 253, 248, 0.9),
      0 1px 0 rgba(255, 255, 255, 0.8);
    transform: translateY(0.5px);
  }}
  .cat-tile.active {{
    border-color: #232220;
    background-color: #F4F1EA;
    color: #111111;
    font-weight: 600;
    box-shadow:
      inset 3px 3px 8px rgba(60, 54, 45, 0.13),
      inset -2px -2px 6px rgba(255, 253, 248, 0.85);
    transform: translateY(1px);
  }}

  .swatch-row {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    padding: 6px 0;
  }}
  .color-swatch {{
    width: 34px;
    height: 34px;
    cursor: pointer;
    border: 2px solid transparent;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }}
  .color-swatch:hover {{
    transform: translateY(-2px);
  }}
  .color-swatch.active {{
    border-color: #111111;
    box-shadow: 0 0 0 2px #FFFFFF inset;
    transform: scale(1.08);
  }}

  .period-size-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 44px;
    align-items: start;
    margin-bottom: 30px;
  }}
  .period-pills {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }}
  .period-pill {{
    border: 1px solid var(--border-hairline);
    background: #FFFFFF;
    padding: 13px 12px;
    text-align: center;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 13px;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #4A4A48;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .period-pill:hover {{
    border-color: #8E8A80;
    box-shadow:
      inset 2px 2px 6px rgba(95, 86, 72, 0.08),
      inset -2px -2px 6px rgba(255, 253, 248, 0.9);
    transform: translateY(0.5px);
  }}
  .period-pill.active {{
    border-color: #232220;
    background: #F4F1EA;
    color: #111111;
    font-weight: 600;
    box-shadow:
      inset 3px 3px 8px rgba(60, 54, 45, 0.13),
      inset -2px -2px 6px rgba(255, 253, 248, 0.85);
    transform: translateY(1px);
  }}

  .size-header {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
  }}
  .unit-toggle {{
    display: inline-flex;
    border: 1px solid var(--border-hairline);
  }}
  .unit-btn {{
    padding: 4px 12px;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.12em;
    border: none;
    background: #FFFFFF;
    color: #666;
    cursor: pointer;
  }}
  .unit-btn.active {{
    background: #8E8D8A;
    color: #FFFFFF;
  }}
  .size-row {{
    display: grid;
    grid-template-columns: 90px 1fr 28px 1fr;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    font-size: 14px;
    color: #4A4A48;
  }}
  .size-input {{
    width: 100%;
    border: none;
    border-bottom: 1px solid #C8C6C0;
    padding: 6px 4px;
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    color: #2B2B2A;
    background: transparent;
    outline: none;
  }}
  .size-x {{
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    color: #888;
  }}

  .keyword-input {{
    width: 100%;
    border: none;
    border-bottom: 1px solid #C8C6C0;
    padding: 10px 4px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 16px;
    font-style: italic;
    color: #2B2B2A;
    outline: none;
  }}
  .search-actions {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    margin: 24px 0 12px;
  }}
  .search-trigger {{
    background: #232220;
    border: 1px solid #232220;
    padding: 10px 30px;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 15px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #FFFFFF;
    cursor: pointer;
  }}
  .reset-trigger {{
    background: none;
    border: none;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: 14px;
    color: var(--text-italic-hint);
    cursor: pointer;
    text-decoration: underline;
  }}

  /* Curate Results Grid (With Unlocked Prices + Add to Curated Selection) */
  .results-wrapper {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 16px 24px 72px;
  }}
  .results-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 0;
    margin-bottom: 28px;
    border-top: 1px solid var(--border-hairline);
    border-bottom: 1px solid var(--border-hairline);
    font-size: 13px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
  }}
  .results-sort {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 14px;
    letter-spacing: 0.1em;
    border: none;
    background: transparent;
    color: var(--text-main);
    cursor: pointer;
    outline: none;
  }}
  .gallery-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 36px 28px;
  }}
  .gallery-card {{
    display: flex;
    flex-direction: column;
    color: inherit;
    border: 1px solid transparent;
    padding: 12px;
    transition: border-color 0.2s ease, background 0.2s ease;
  }}
  .gallery-card:hover {{
    border-color: var(--border-hairline);
    background: #FCFBFA;
  }}
  .card-img-box {{
    width: 100%;
    aspect-ratio: 1 / 1;
    background-color: var(--studio-grey-card);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin-bottom: 14px;
    position: relative;
    cursor: pointer;
  }}
  .card-img-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.45s ease;
  }}
  .gallery-card:hover .card-img-box img {{
    transform: scale(1.03);
  }}
  .card-cat {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
    text-align: center;
  }}
  .card-title {{
    font-size: 18px;
    font-weight: 500;
    color: #1F1F1E;
    text-align: center;
    line-height: 1.35;
    margin-bottom: 6px;
    min-height: 48px;
  }}
  .card-meta {{
    font-style: italic;
    font-size: 14px;
    color: var(--text-muted);
    text-align: center;
    margin-bottom: 8px;
  }}
  .card-price {{
    font-family: 'Montserrat', sans-serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.08em;
    color: #232220;
    text-align: center;
    margin-bottom: 14px;
  }}
  .card-price del {{
    color: #999;
    margin-right: 8px;
    font-weight: 400;
  }}
  .card-actions {{
    margin-top: auto;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 8px;
  }}
  .btn-add-curate {{
    padding: 10px 14px;
    background: #232220;
    color: #FFFFFF;
    border: 1px solid #232220;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .btn-add-curate:hover {{
    background: #3D3B37;
  }}
  .btn-add-curate.in-cart {{
    background: #FAF9F6;
    color: #232220;
    border-color: #232220;
  }}
  .btn-instant-checkout {{
    padding: 10px 12px;
    background: #FFFFFF;
    color: #232220;
    border: 1px solid var(--border-hairline);
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    cursor: pointer;
  }}
  .btn-instant-checkout:hover {{
    border-color: #232220;
  }}

  /* ==========================================================================
     SLIDE-OVER CURATED SELECTION DRAWER
     ========================================================================== */
  .drawer-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(20, 19, 18, 0.45);
    z-index: 200;
    display: none;
  }}
  .drawer-backdrop.open {{
    display: block;
  }}
  .selection-drawer {{
    position: fixed;
    top: 0;
    right: -460px;
    width: 440px;
    max-width: 94vw;
    height: 100vh;
    background: #FFFFFF;
    z-index: 210;
    box-shadow: -8px 0 32px rgba(0,0,0,0.14);
    display: flex;
    flex-direction: column;
    transition: right 0.32s ease;
  }}
  .selection-drawer.open {{
    right: 0;
  }}
  .drawer-header {{
    padding: 22px 24px;
    border-bottom: 1px solid var(--border-hairline);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .drawer-header h3 {{
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }}
  .drawer-close {{
    background: none;
    border: none;
    font-size: 22px;
    cursor: pointer;
    color: var(--text-muted);
  }}
  .drawer-items {{
    flex: 1;
    overflow-y: auto;
    padding: 20px 24px;
  }}
  .drawer-item {{
    display: grid;
    grid-template-columns: 74px 1fr auto;
    gap: 14px;
    align-items: center;
    padding-bottom: 16px;
    margin-bottom: 16px;
    border-bottom: 1px solid var(--border-hairline);
  }}
  .drawer-item img {{
    width: 74px;
    height: 74px;
    object-fit: cover;
    background: var(--studio-grey-card);
  }}
  .drawer-item-title {{
    font-size: 15px;
    font-weight: 500;
    line-height: 1.3;
    margin-bottom: 4px;
  }}
  .drawer-item-price {{
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    color: var(--text-muted);
  }}
  .drawer-remove {{
    background: none;
    border: none;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999;
    cursor: pointer;
  }}
  .drawer-footer {{
    padding: 20px 24px 26px;
    border-top: 1px solid var(--border-hairline);
    background: #FAF9F6;
  }}
  .drawer-subtotal {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
    font-size: 16px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }}
  .drawer-checkout-btn {{
    width: 100%;
    padding: 14px;
    background: #232220;
    color: #FFFFFF;
    border: none;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 15px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    cursor: pointer;
  }}

  /* ==========================================================================
     VIEW 4: FULL WHITE-GLOVE ACQUISITION & CHECKOUT EXPERIENCE
     ========================================================================== */
  .checkout-wrap {{
    max-width: 1140px;
    margin: 0 auto;
    padding: 40px 24px 80px;
  }}
  .checkout-header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding-bottom: 18px;
    margin-bottom: 34px;
    border-bottom: 1px solid var(--border-hairline);
  }}
  .checkout-header-bar h2 {{
    font-size: 26px;
    font-weight: 400;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }}
  .checkout-grid {{
    display: grid;
    grid-template-columns: 1.35fr 1fr;
    gap: 48px;
    align-items: start;
  }}
  .checkout-block {{
    margin-bottom: 34px;
    padding-bottom: 28px;
    border-bottom: 1px solid var(--border-hairline);
  }}
  .checkout-step-title {{
    font-size: 15px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #232220;
    margin-bottom: 16px;
  }}
  .form-row-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 14px;
  }}
  .form-group {{
    margin-bottom: 14px;
  }}
  .form-group label {{
    display: block;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
  }}
  .form-control {{
    width: 100%;
    padding: 11px 12px;
    border: 1px solid #D5D2CA;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 16px;
    color: #232220;
    background: #FFFFFF;
    outline: none;
  }}
  .form-control:focus {{
    border-color: #232220;
  }}

  /* Fulfillment Option Cards */
  .shipping-option-card {{
    border: 1px solid var(--border-hairline);
    padding: 16px 18px;
    margin-bottom: 10px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 14px;
    background: #FFFFFF;
    transition: all 0.2s ease;
  }}
  .shipping-option-card.active {{
    border-color: #232220;
    background: #FAF9F6;
  }}
  .shipping-option-title {{
    font-size: 16px;
    font-weight: 600;
    color: #1F1F1E;
    margin-bottom: 3px;
  }}
  .shipping-option-desc {{
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.4;
  }}
  .shipping-option-badge {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #232220;
    white-space: nowrap;
    padding-top: 2px;
  }}

  /* Summary Ledger Card */
  .checkout-summary-card {{
    background: #FAF8F5;
    border: 1px solid #E2DDD4;
    padding: 28px;
    position: sticky;
    top: 140px;
  }}
  .summary-heading {{
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid #DFDAD0;
  }}
  .summary-line {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    font-size: 15px;
    color: #4A4845;
  }}
  .summary-total {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid #DFDAD0;
    font-size: 20px;
    font-weight: 600;
    color: #1F1F1E;
  }}
  .complete-acquisition-btn {{
    width: 100%;
    margin-top: 22px;
    padding: 16px;
    background: #232220;
    color: #FFFFFF;
    border: 1px solid #232220;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 15px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s ease;
  }}
  .complete-acquisition-btn:hover {{
    background: #3B3935;
  }}

  /* Editorial Provenance Modal (For Gallery Lookbook Inspection Without Prices) */
  .editorial-modal-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(20, 19, 18, 0.58);
    z-index: 250;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .editorial-modal-backdrop.open {{
    display: flex;
  }}
  .editorial-modal {{
    background: #FFFFFF;
    max-width: 820px;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    border: 1px solid var(--border-hairline);
    overflow: hidden;
  }}
  .editorial-modal-img {{
    background: var(--studio-grey-card);
    aspect-ratio: 1 / 1;
  }}
  .editorial-modal-img img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}
  .editorial-modal-body {{
    padding: 36px 32px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}

  @media (max-width: 920px) {{
    .brand-header {{ padding: 16px 14px 14px; }}
    .brand-crest {{ width: 52px; margin-bottom: 6px; }}
    .brand-title {{ font-size: 23px; letter-spacing: 0.16em; }}
    .brand-subtitle {{ font-size: 12px; margin-bottom: 12px; }}
    .main-nav {{ gap: 14px; }}
    .main-nav a {{ font-size: 12px; letter-spacing: 0.14em; }}
    .hero-carousel {{ height: auto; }}
    .hero-slide {{ position: relative; grid-template-columns: 1fr; display: none; }}
    .hero-slide.active {{ display: grid; }}
    .hero-visual-stage {{ height: 320px; }}
    .chapter-track {{ grid-template-columns: repeat(2, 1fr); }}
    .category-bar {{ grid-template-columns: repeat(2, 1fr); }}
    .period-size-grid {{ grid-template-columns: 1fr; }}
    .gallery-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .checkout-grid {{ grid-template-columns: 1fr; }}
    .editorial-modal {{ grid-template-columns: 1fr; }}
    .concierge-pillars-grid {{ grid-template-columns: 1fr !important; gap: 24px !important; }}
    .footer-bottom-flex {{ flex-direction: column; text-align: center; gap: 14px; }}
  }}

  /* Standard Showroom Footer & Legal Disclaimer Links */
  .site-footer-wrap {{
    border-top: 1px solid var(--border-hairline);
    background: #FAF8F5;
    margin-top: 40px;
    color: var(--text-main);
  }}
  .concierge-pillars-grid {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 44px 24px 36px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 36px;
    text-align: center;
    border-bottom: 1px solid var(--border-hairline);
  }}
  .concierge-pillar h4 {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 8px;
    color: #1E1D1B;
  }}
  .concierge-pillar p {{
    font-size: 15px;
    color: var(--text-muted);
    max-width: 330px;
    margin: 0 auto;
    line-height: 1.55;
  }}
  .footer-legal-strip {{
    max-width: 1180px;
    margin: 0 auto;
    padding: 26px 24px 34px;
  }}
  .footer-bottom-flex {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 18px;
    margin-bottom: 16px;
  }}
  .footer-brand-copy {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
  }}
  .footer-policy-links {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    list-style: none;
  }}
  .footer-policy-links a {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: color 0.2s ease, border-color 0.2s ease;
  }}
  .footer-policy-links a:hover {{
    color: var(--text-main);
    border-bottom-color: var(--text-main);
  }}
  .footer-disclaimer-fineprint {{
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 13px;
    font-style: italic;
    color: var(--text-muted);
    line-height: 1.55;
    text-align: center;
    max-width: 980px;
    margin: 0 auto;
  }}
</style>
</head>
<body>
  <!-- NRL Whisper-Fine Sheer Linen Curtain Draft Canvas (Strictly z-index: 0 behind all foreground cards) -->
  <canvas id="nrl-curtain-draft-canvas" class="nrl-curtain-draft-canvas" aria-hidden="true"></canvas>
  <div class="nrl-linen-tooth-overlay" aria-hidden="true"></div>

  <!-- TOP DEMO BAR SO MATTHEW CAN JUMP OR WATCH THE CLICK-FLOW -->
  <div class="flow-status-bar">
    <div>THE CHAPMAN COLLECTION // TWO-ROOM CLICK-FLOW &amp; WHITE-GLOVE CHECKOUT PROTOTYPE</div>
    <div class="flow-steps">
      <button type="button" class="flow-step-pill active" id="pill-home" onclick="switchView('home')">1. Landing (No Prices / No Cart)</button>
      <button type="button" class="flow-step-pill" id="pill-gallery" onclick="switchView('gallery')">2. Gallery Lookbook (No Prices)</button>
      <button type="button" class="flow-step-pill" id="pill-curate" onclick="switchView('curate')">3. Curate Your Collection (Prices + Filter)</button>
      <button type="button" class="flow-step-pill" id="pill-checkout" onclick="switchView('checkout')">4. White-Glove Checkout</button>
    </div>
  </div>

  <!-- MANSOUR-STYLE CENTERED HEADER (GOODBYE PHONE NUMBER NEXT TO CONTACT) -->
  <header class="brand-header">
    <img class="brand-crest" src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-crest.png" onerror="this.style.display='none'" alt="The Chapman Collection Crest" onclick="switchView('home')">
    <h1 class="brand-title" onclick="switchView('home')">The Chapman Collection</h1>
    <div class="brand-subtitle">Rancho Santa Fe &amp; London Heritage &middot; Fine European Antiques &amp; Carpets</div>
    <nav>
      <ul class="main-nav">
        <li><a id="nav-home" class="active" onclick="switchView('home')">Home</a></li>
        <li><a id="nav-gallery" onclick="switchView('gallery')">Gallery</a></li>
        <li><a id="nav-melissa" onclick="switchView('melissa')">Meet Melissa</a></li>
        <li><a id="nav-curate" class="nav-curate-cta" onclick="switchView('curate')">Curate Your Collection</a></li>
        <li><a id="nav-selection" class="nav-selection-pill" onclick="toggleDrawer(true)">Curated Selection (<span id="nav-cart-count">0</span>)</a></li>
      </ul>
    </nav>
  </header>

  <!-- ========================================================================
       VIEW 1: HOME (SLIDING CAROUSEL ON NEW SLATE BACKDROP + OFF-GREIGE + COLLAGE SPLASH)
       ======================================================================== -->
  <div id="view-home" class="site-view active">
    <section class="hero-stage-wrap">
      <div class="hero-carousel">

        <!-- SLIDE 1: HERO FURNITURE ON NEW SLATE CURVED BACKDROP -->
        <div class="hero-slide active" id="hero-slide-0">
          <div class="hero-visual-stage">
            <div class="hero-furniture-triptych">
              <div class="hero-furniture-card" onclick="openCurateWithCategory('EUROPEAN FURNITURE', 'spanish')">
                <img src="assets/spanish-knights-cabinet-slate-curved.jpg" alt="Spanish Carved Armoire with Knights">
                <div class="hero-furniture-tag">18th C. Spanish Knights Armoire</div>
              </div>
              <div class="hero-furniture-card" onclick="openCurateWithCategory('EUROPEAN FURNITURE', 'gothic')">
                <img src="assets/english-gothic-hallstand-slate-curved.jpg" alt="English Tall Gothic Hallstand">
                <div class="hero-furniture-tag">English Carved Gothic Hallstand</div>
              </div>
              <div class="hero-furniture-card" onclick="openCurateWithCategory('EUROPEAN FURNITURE', 'boulle')">
                <img src="assets/boulle-marquetry-credenza-slate-curved.jpg" alt="Napoleon III Marquetry Credenza">
                <div class="hero-furniture-tag">Napoleon III Marquetry Credenza</div>
              </div>
            </div>
          </div>
          <div class="hero-colorblock-panel panel-slate-greige">
            <div class="hero-kicker">Rancho Santa Fe Showroom</div>
            <h2 class="hero-panel-title">Period Furniture</h2>
            <p class="hero-panel-sub">17th to 19th Century European armoires, architectural hallstands and French marquetry</p>
            <button type="button" class="hero-curate-btn" onclick="openCurateWithCategory('EUROPEAN FURNITURE', '')">Curate Your Collection</button>
          </div>
        </div>

        <!-- SLIDE 2: COLLAGE OF CARPET WEAVE CLOSE-UPS OVER MINIMALIST OFF-GREIGE -->
        <div class="hero-slide" id="hero-slide-1">
          <div class="hero-visual-stage">
            <div class="hero-macro-collage" id="hero-carpet-collage"></div>
          </div>
          <div class="hero-colorblock-panel panel-warm-greige">
            <div class="hero-kicker">Hand-Knotted Masterworks</div>
            <h2 class="hero-panel-title">Tabriz &amp; Silk Qum</h2>
            <p class="hero-panel-sub">Palace-sized Persian carpets, corridor runners and Flemish tapestries selected by hand</p>
            <button type="button" class="hero-curate-btn" onclick="openCurateWithCategory('CARPETS & RUNNERS', '')">Curate Your Collection</button>
          </div>
        </div>

        <!-- SLIDE 3: COLLAGE OF BRONZES, PORCELAIN & TRINKETS OVER MINIMALIST OFF-GREIGE -->
        <div class="hero-slide" id="hero-slide-2">
          <div class="hero-visual-stage">
            <div class="hero-macro-collage" id="hero-trinket-collage"></div>
          </div>
          <div class="hero-colorblock-panel panel-gustavian">
            <div class="hero-kicker">Decorative Arts &amp; Objects</div>
            <h2 class="hero-panel-title">Bronzes &amp; S&egrave;vres</h2>
            <p class="hero-panel-sub">Signed 19th Century French bronzes, giltwood mirrors, marble sculpture and collector objects</p>
            <button type="button" class="hero-curate-btn" onclick="openCurateWithCategory('BRONZES & SCULPTURE', '')">Curate Your Collection</button>
          </div>
        </div>

      </div>

      <div class="hero-controls">
        <div class="hero-dots">
          <button type="button" class="hero-dot active" id="dot-0" onclick="setHeroSlide(0)"></button>
          <button type="button" class="hero-dot" id="dot-1" onclick="setHeroSlide(1)"></button>
          <button type="button" class="hero-dot" id="dot-2" onclick="setHeroSlide(2)"></button>
        </div>
        <div class="hero-arrows">
          <button type="button" class="hero-arrow" onclick="stepHeroSlide(-1)">Prev</button>
          <button type="button" class="hero-arrow" onclick="stepHeroSlide(1)">Next</button>
        </div>
      </div>
    </section>

    <!-- MANSOUR-STYLE EDITORIAL INTRO (ZERO CLUTTER, INLINE CONCIERGE) -->
    <section class="mansour-editorial-intro">
      <p>
        For over three decades, Melissa Chapman has sourced museum-caliber European period furniture, hand-knotted Persian and silk carpets, historical tapestries and fine decorative arts from her early showroom roots on Harrington Road in South Kensington, London to the heart of Rancho Santa Fe Village. Every piece is personally vetted for authenticity, architectural proportion and timeless warmth.
      </p>
      <p>
        Explore our editorial <a href="#gallery" onclick="switchView('gallery'); return false;">Gallery Lookbooks</a> or enter <a href="#curate" onclick="switchView('curate'); return false;">Curate Your Collection</a> to filter our live showroom inventory by color palette, historical period and room dimensions. For private in-home trials across Southern California, call or text Melissa directly at <a href="tel:+18583492638">(858) 349-2638</a>.
      </p>
    </section>

    <!-- MANSOUR ASYMMETRIC COLLAGE SPLASH FOR RUGS & TAPESTRIES -->
    <section class="collage-splash-wrap">
      <div class="collage-splash-heading">Featured Carpets &amp; Tapestries</div>
      <div id="collage-splash-mount"></div>
    </section>
  </div>

  <!-- ========================================================================
       VIEW 2: GALLERY (CATEGORIZED LOOKBOOK SLIDES ON MINIMALIST OFF-GREIGE, ZERO PRICES)
       ======================================================================== -->
  <div id="view-gallery" class="site-view">
    <section class="gallery-lookbook-stage">
      <div class="lookbook-container">
        <div class="lookbook-top-bar">
          <div>
            <h2>The Showroom Gallery</h2>
            <p>Categorized editorial lookbooks &middot; Click any piece to inspect provenance or open Curate Your Collection to view pricing and acquire</p>
          </div>
          <button type="button" class="search-trigger" onclick="switchView('curate')">Curate Your Collection &rarr;</button>
        </div>

        <div id="lookbook-chapters-mount"></div>
      </div>
    </section>
  </div>

  <!-- ========================================================================
       VIEW 2B: MEET MELISSA & THE DESIGNERS (EDITORIAL STORY)
       ======================================================================== -->
  <div id="view-melissa" class="site-view">
    <section class="console-wrap" style="max-width:920px; padding-top:52px; padding-bottom:72px;">
      <div class="hero-kicker" style="color:var(--text-muted); text-align:center;">Harrington Road, London to 6014 La Granada, Rancho Santa Fe</div>
      <h2 class="console-lead" style="text-align:center; margin-bottom:28px;">Meet Melissa Chapman</h2>
      <div style="background:var(--off-greige); border:1px solid var(--border-hairline); padding:40px; font-size:19px; line-height:1.8; color:#3A3835;">
        <p style="margin-bottom:18px;">
          Born and raised in England, Melissa Chapman began her career in the renowned antique district of Harrington Road in South Kensington, London, working alongside master restorers, estate curators and international interior designers. Over the past thirty years, her eye for rare European woodwork, 17th to 19th Century French and Spanish case pieces and luminous Persian carpets has graced private estates of celebrities, statesmen and royalty.
        </p>
        <p style="margin-bottom:28px;">
          At The Chapman Collection in Rancho Santa Fe Village, every acquisition is accompanied by complimentary Southern California in-home placement previews and white-glove nationwide delivery. Whether you are furnishing a single study or curating an entire residence with your interior designer, Melissa personally oversees every detail from showroom floor to final placement.
        </p>
        <div style="text-align:center;">
          <button type="button" class="search-trigger" onclick="switchView('curate')">Curate Your Collection</button>
        </div>
      </div>
    </section>
  </div>

  <!-- ========================================================================
       VIEW 3: CURATE YOUR COLLECTION (THE ONLY ROOM WITH PRICES & ACQUISITION CART)
       ======================================================================== -->
  <div id="view-curate" class="site-view">
    <main class="console-wrap" id="search-console">
      <h2 class="console-lead">Curate Your Collection</h2>
      <div class="filter-subhint" style="margin-bottom:26px;">Select one or multiple criteria below to filter by category, color palette, historical period and room dimensions. Pricing and direct acquisition are unlocked exclusively in this vault.</div>

      <!-- CATEGORIES -->
      <div class="filter-section">
        <div class="filter-label">Categories</div>
        <div class="category-bar" id="category-bar"></div>
      </div>

      <!-- COLORS -->
      <div class="filter-section">
        <div class="filter-label">Colors</div>
        <div class="filter-subhint">You may select multiple colors</div>
        <div class="swatch-row" id="swatch-row"></div>
      </div>

      <!-- PERIOD & SIZE -->
      <div class="period-size-grid">
        <div>
          <div class="filter-label">Period</div>
          <div class="filter-subhint">You may select multiple periods</div>
          <div class="period-pills" id="period-pills"></div>
        </div>

        <div>
          <div class="size-header">
            <div class="filter-label" style="margin-bottom:0;">Size</div>
            <div class="unit-toggle">
              <button type="button" class="unit-btn active" id="unit-ft" onclick="setUnit('FT')">FT</button>
              <button type="button" class="unit-btn" id="unit-cm" onclick="setUnit('CM')">CM</button>
            </div>
          </div>
          <div class="size-row">
            <span>Minimum</span>
            <input type="number" step="0.5" class="size-input" id="min-w" placeholder="W" oninput="applyFilters()">
            <span class="size-x">X</span>
            <input type="number" step="0.5" class="size-input" id="min-l" placeholder="L" oninput="applyFilters()">
          </div>
          <div class="size-row">
            <span>Maximum</span>
            <input type="number" step="0.5" class="size-input" id="max-w" placeholder="W" oninput="applyFilters()">
            <span class="size-x">X</span>
            <input type="number" step="0.5" class="size-input" id="max-l" placeholder="L" oninput="applyFilters()">
          </div>
        </div>
      </div>

      <!-- SEARCH KEYWORD -->
      <div class="filter-section">
        <div class="filter-label">Search Keyword</div>
        <input type="text" class="keyword-input" id="keyword-input" placeholder="Enter origin, style, or keyword (e.g., Spanish, Gothic, Tabriz, Heriz, Louis XV, Sèvres)..." oninput="applyFilters()">
      </div>

      <div class="search-actions">
        <button type="button" class="search-trigger" onclick="document.getElementById('gallery-anchor').scrollIntoView({{behavior:'smooth'}})">View Matching Pieces</button>
        <button type="button" class="reset-trigger" onclick="resetFilters()">Clear all criteria</button>
      </div>
    </main>

    <section class="results-wrapper" id="gallery-anchor">
      <div class="results-bar">
        <div class="results-count" id="results-count">Showing All Curated Pieces</div>
        <select class="results-sort" id="sort-select" onchange="applyFilters()">
          <option value="featured">Curatorial Order (Featured Slate Studio First)</option>
          <option value="price-desc">Price: High to Low</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="title-asc">Alphabetical (A to Z)</option>
        </select>
      </div>

      <div class="gallery-grid" id="gallery-grid"></div>
    </section>
  </div>

  <!-- ========================================================================
       VIEW 4: FULL WHITE-GLOVE ACQUISITION & CHECKOUT EXPERIENCE
       ======================================================================== -->
  <div id="view-checkout" class="site-view">
    <section class="checkout-wrap">
      <div class="checkout-header-bar">
        <div>
          <h2>Private Showroom Acquisition &amp; White-Glove Checkout</h2>
          <p style="font-style:italic; color:var(--text-muted); font-size:16px;">Every piece is backed by Melissa Chapman's Certificate of Provenance &amp; Authenticity</p>
        </div>
        <button type="button" class="reset-trigger" onclick="switchView('curate')">&larr; Return to Curate Your Collection</button>
      </div>

      <div id="checkout-live-form" class="checkout-grid">
        <div>
          <!-- STEP 1: COLLECTOR / DESIGNER PROFILE -->
          <div class="checkout-block">
            <div class="checkout-step-title">1. Collector &amp; Interior Designer Dossier</div>
            <div class="form-row-2">
              <div class="form-group">
                <label>First Name</label>
                <input type="text" class="form-control" id="chk-fname" value="Eleanor">
              </div>
              <div class="form-group">
                <label>Last Name</label>
                <input type="text" class="form-control" id="chk-lname" value="Vance-Sterling">
              </div>
            </div>
            <div class="form-row-2">
              <div class="form-group">
                <label>Email Address (For Provenance Dossier &amp; Receipt)</label>
                <input type="email" class="form-control" id="chk-email" value="eleanor@sterlinginteriors-rsf.com">
              </div>
              <div class="form-group">
                <label>Direct Mobile (For White-Glove Dispatch SMS)</label>
                <input type="tel" class="form-control" id="chk-phone" value="(858) 555-0194">
              </div>
            </div>
            <div class="form-group">
              <label>Optional Interior Designer / ASID Resale Certificate # (Tax-Exempt Trade Account)</label>
              <input type="text" class="form-control" id="chk-trade" placeholder="Enter CA Seller's Permit or ASID Trade ID if applicable">
            </div>
          </div>

          <!-- STEP 2: WHITE-GLOVE FULFILLMENT & IN-HOME TRIAL OPTIONS (MATCHING OUR LIVE WOOCOMMERCE ZONES) -->
          <div class="checkout-block">
            <div class="checkout-step-title">2. White-Glove Delivery, Showroom Pickup or 48-Hour In-Home Preview</div>

            <div class="shipping-option-card active" id="ship-card-preview" onclick="selectShipping('preview')">
              <div>
                <div class="shipping-option-title">Complimentary 48-Hour Southern California In-Home Preview</div>
                <div class="shipping-option-desc">Our team brings your curated carpets and furniture into your residence in Rancho Santa Fe, La Jolla, Del Mar or Newport Beach on approval before final settlement.</div>
              </div>
              <div class="shipping-option-badge">Complimentary</div>
            </div>

            <div class="shipping-option-card" id="ship-card-pickup" onclick="selectShipping('pickup')">
              <div>
                <div class="shipping-option-title">Complimentary Rancho Santa Fe Showroom Pickup (6014 La Granada)</div>
                <div class="shipping-option-desc">Reserved immediately in our showroom vault for private pickup by you or your designer's receiving warehouse.</div>
              </div>
              <div class="shipping-option-badge">Complimentary</div>
            </div>

            <div class="shipping-option-card" id="ship-card-carrier" onclick="selectShipping('carrier')">
              <div>
                <div class="shipping-option-title">Client-Arranged Domestic or International White-Glove Shipping (Coordinated Post-Purchase)</div>
                <div class="shipping-option-desc">Melissa personally coordinates custom crating, blanket-wrap fine-art transport and full-value transit insurance to your estate anywhere in the US or abroad.</div>
              </div>
              <div class="shipping-option-badge">Billed at Carrier Cost</div>
            </div>

            <div class="form-row-2" style="margin-top:16px;">
              <div class="form-group">
                <label>Estate / Delivery Street Address</label>
                <input type="text" class="form-control" id="chk-addr" value="16420 Via De Santa Fe">
              </div>
              <div class="form-group">
                <label>City, State &amp; Postal Code</label>
                <input type="text" class="form-control" id="chk-city" value="Rancho Santa Fe, CA 92067">
              </div>
            </div>
          </div>

          <!-- STEP 3: SETTLEMENT METHOD -->
          <div class="checkout-block" style="border-bottom:none;">
            <div class="checkout-step-title">3. Settlement &amp; Acquisition Method</div>

            <div class="shipping-option-card active" id="pay-card-cc" onclick="selectPayment('cc')">
              <div>
                <div class="shipping-option-title">Immediate Card Settlement (Visa, Mastercard, American Express)</div>
                <div class="shipping-option-desc">Encrypted direct capture via The Chapman Collection merchant vault.</div>
              </div>
              <div class="shipping-option-badge">Instant Lock</div>
            </div>

            <div class="shipping-option-card" id="pay-card-wire" onclick="selectPayment('wire')">
              <div>
                <div class="shipping-option-title">Private Bank Wire / ACH Transfer (3% Cash-Equivalent Courtesy)</div>
                <div class="shipping-option-desc">Automatically deducts a 3% collector wire courtesy and places a 48-hour showroom hold while funds clear.</div>
              </div>
              <div class="shipping-option-badge">-3% Courtesy</div>
            </div>

            <div class="shipping-option-card" id="pay-card-hold" onclick="selectPayment('hold')">
              <div>
                <div class="shipping-option-title">48-Hour In-Home Trial Authorization Hold ($0 Charged Today)</div>
                <div class="shipping-option-desc">Places a zero-charge card authorization while Melissa schedules your private in-home room placement.</div>
              </div>
              <div class="shipping-option-badge">$0 Due Today</div>
            </div>

            <div id="cc-fields-box" style="margin-top:16px; background:#FAF9F6; padding:18px; border:1px solid var(--border-hairline);">
              <div class="form-group">
                <label>Cardholder Name</label>
                <input type="text" class="form-control" value="Eleanor Vance-Sterling">
              </div>
              <div class="form-row-2" style="margin-bottom:0;">
                <div class="form-group" style="margin-bottom:0;">
                  <label>Card Number</label>
                  <input type="text" class="form-control" value="•••• •••• •••• 8842">
                </div>
                <div class="form-group" style="margin-bottom:0;">
                  <label>Expiration &amp; Security Code</label>
                  <input type="text" class="form-control" value="09 / 29   &middot;   841">
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: CURATED SELECTION SUMMARY LEDGER -->
        <aside class="checkout-summary-card">
          <div class="summary-heading">Your Curated Selection</div>
          <div id="checkout-items-list"></div>

          <div style="margin-top:18px;">
            <div class="summary-line">
              <span>Curated Pieces Subtotal</span>
              <span id="chk-subtotal">$0</span>
            </div>
            <div class="summary-line" id="chk-wire-row" style="display:none; color:#2E6B47;">
              <span>Private Bank Wire Courtesy (3%)</span>
              <span id="chk-wire-discount">-$0</span>
            </div>
            <div class="summary-line">
              <span>White-Glove Fulfillment</span>
              <span id="chk-shipping-label">Complimentary In-Home Preview</span>
            </div>
            <div class="summary-line">
              <span>Certificate of Provenance &amp; Appraisal</span>
              <span>Included</span>
            </div>
            <div class="summary-total">
              <span id="chk-total-label">Total Acquisition</span>
              <span id="chk-total-val">$0</span>
            </div>
          </div>

          <button type="button" class="complete-acquisition-btn" onclick="submitWhiteGloveOrder()">Complete White-Glove Acquisition</button>
          <div style="margin-top:14px; text-align:center; font-size:13px; font-style:italic; color:var(--text-muted);">
            Direct Showroom Concierge: (858) 349-2638 &middot; 6014 La Granada, Rancho Santa Fe
          </div>
        </aside>
      </div>

      <!-- INSTANT ORDER CONFIRMATION DOSSIER -->
      <div id="checkout-confirmation-box" style="display:none; background:#FAF8F5; border:1px solid #D8D2C7; padding:48px 36px; text-align:center; max-width:780px; margin:0 auto;">
        <div class="hero-kicker" style="color:var(--gold-accent);">RANCHO SANTA FE SHOWROOM VAULT RESERVATION CONFIRMED</div>
        <h3 style="font-size:30px; font-weight:400; letter-spacing:0.16em; text-transform:uppercase; margin:10px 0 14px;">Dossier #TCC-RSF-2026-8419</h3>
        <p style="font-size:18px; color:#3A3835; max-width:600px; margin:0 auto 24px;" id="confirm-dynamic-copy"></p>
        <div id="confirm-items-recap" style="text-align:left; background:#FFFFFF; border:1px solid var(--border-hairline); padding:20px; margin:0 auto 28px; max-width:560px;"></div>
        <button type="button" class="search-trigger" onclick="resetAfterOrder()">Return to Showroom Home</button>
      </div>
    </section>
  </div>

  <!-- SLIDE-OVER CURATED SELECTION DRAWER -->
  <div class="drawer-backdrop" id="drawer-backdrop" onclick="toggleDrawer(false)"></div>
  <aside class="selection-drawer" id="selection-drawer">
    <div class="drawer-header">
      <h3>Curated Selection</h3>
      <button type="button" class="drawer-close" onclick="toggleDrawer(false)">&times;</button>
    </div>
    <div class="drawer-items" id="drawer-items"></div>
    <div class="drawer-footer">
      <div class="drawer-subtotal">
        <span>Selection Total</span>
        <strong id="drawer-subtotal-val">$0</strong>
      </div>
      <button type="button" class="drawer-checkout-btn" onclick="proceedToCheckout()">Proceed to White-Glove Checkout &rarr;</button>
    </div>
  </aside>

  <!-- EDITORIAL PROVENANCE MODAL (FOR GALLERY LOOKBOOK — NO PRICES, NO ADD TO CART) -->
  <div class="editorial-modal-backdrop" id="editorial-modal-backdrop" onclick="closeEditorialModal()">
    <div class="editorial-modal" onclick="event.stopPropagation()">
      <div class="editorial-modal-img">
        <img id="modal-img" src="" alt="">
      </div>
      <div class="editorial-modal-body">
        <div class="card-cat" id="modal-cat" style="text-align:left;"></div>
        <h3 id="modal-title" style="font-size:24px; font-weight:400; line-height:1.3; margin-bottom:10px;"></h3>
        <div id="modal-dims" style="font-style:italic; font-size:15px; color:var(--text-muted); margin-bottom:18px;"></div>
        <p style="font-size:16px; color:#4A4845; margin-bottom:24px;">
          Personally selected by Melissa Chapman for The Chapman Collection in Rancho Santa Fe. Available for private Southern California in-home preview and nationwide white-glove delivery.
        </p>
        <div style="font-style:italic; font-size:13px; color:var(--text-italic-hint); margin-bottom:14px;">
          Itemized pricing and direct acquisition are exclusively unlocked inside Curate Your Collection.
        </div>
        <button type="button" class="search-trigger" id="modal-curate-btn">Unlock in Curate Your Collection &rarr;</button>
      </div>
    </div>
  </div>

  <!-- STANDARD SHOWROOM FOOTER & LEGAL DISCLAIMER LINKS (LINKS OUT TO LIVE WOOCOMMERCE POLICY PAGES) -->
  <footer class="site-footer-wrap">
    <div class="concierge-pillars-grid">
      <div class="concierge-pillar">
        <h4>Complimentary In-Home Preview</h4>
        <p>Experience our carpets and period furnishings inside your own residence across Rancho Santa Fe, La Jolla, Del Mar and Southern California on private approval.</p>
      </div>
      <div class="concierge-pillar">
        <h4>White-Glove Nationwide Delivery</h4>
        <p>Every acquisition is professionally crated, insured and delivered through our vetted fine-art and antique white-glove carriers throughout the United States.</p>
      </div>
      <div class="concierge-pillar">
        <h4>Rancho Santa Fe Village Showroom</h4>
        <p>6014 La Granada, Rancho Santa Fe, CA 92067 &middot; Private Showroom Concierge: <a href="tel:+18583492638" style="color:inherit;">(858) 349-2638</a></p>
      </div>
    </div>

    <div class="footer-legal-strip">
      <div class="footer-bottom-flex">
        <div class="footer-brand-copy">&copy; 2026 The Chapman Collection &middot; All Rights Reserved &middot; Rancho Santa Fe &amp; London Heritage</div>
        <ul class="footer-policy-links">
          <li><a href="https://thechapmancollection.com/privacy-policy/" target="_blank" rel="noopener">Privacy Policy</a></li>
          <li><a href="https://thechapmancollection.com/terms-and-conditions/" target="_blank" rel="noopener">Terms &amp; Conditions</a></li>
          <li><a href="https://thechapmancollection.com/refund_returns/" target="_blank" rel="noopener">Shipping, Returns &amp; In-Home Trial Policy</a></li>
          <li><a href="https://thechapmancollection.com/services/" target="_blank" rel="noopener">Appraisals &amp; Restoration</a></li>
          <li><a href="https://thechapmancollection.com/contact/" target="_blank" rel="noopener">Contact Showroom</a></li>
        </ul>
      </div>
      <div class="footer-disclaimer-fineprint">
        All period antiques, hand-knotted carpets, tapestries and works of art are offered subject to prior showroom sale. Dimensions are approximate as all pieces are handcrafted and centuries-old masterworks; condition reports and high-resolution macro photography are provided upon request prior to white-glove dispatch.
      </div>
      <div class="nrl-atelier-colophon">
        Curatorial Search Architecture &amp; Real-Time Gallery Light Engine by <a href="https://renderwithoutcode.com" target="_blank" rel="noopener">NeverRender Labs</a>
      </div>
    </div>
  </footer>

<script>
const CATALOG = {catalog_json};
const SWATCHES = {swatches_json};
const PERIODS = {periods_json};

const CATEGORY_TILES = [
  {{ id: "CARPETS & RUNNERS", label: "Antique & Vintage Carpets" }},
  {{ id: "EUROPEAN FURNITURE", label: "European Furniture" }},
  {{ id: "TAPESTRIES", label: "Tapestries" }},
  {{ id: "FINE ART", label: "Fine Art & Paintings" }},
  {{ id: "BRONZES & SCULPTURE", label: "Bronzes & Sculpture" }},
  {{ id: "ALL", label: "All Collection" }}
];

let state = {{
  view: "home",
  heroSlide: 0,
  category: "ALL",
  colors: new Set(),
  periods: new Set(),
  unit: "FT",
  cart: [CATALOG[0], CATALOG[1]], // Pre-seeded with the 2 Slate Curved hero pieces so checkout is immediately testable!
  shippingMode: "preview",
  paymentMode: "cc"
}};

function formatPrice(val) {{
  const num = parseFloat(val);
  if (isNaN(num) || num <= 0) return "Price Upon Request";
  return "$" + num.toLocaleString("en-US", {{ minimumFractionDigits: 0, maximumFractionDigits: 0 }});
}}

/* ==========================================================================
   VIEW NAVIGATION (HOME -> GALLERY -> CURATE -> CHECKOUT)
   ========================================================================== */
function switchView(viewName) {{
  state.view = viewName;
  ["home", "gallery", "melissa", "curate", "checkout"].forEach(v => {{
    const el = document.getElementById("view-" + v);
    if (el) el.classList.toggle("active", v === viewName);
    const nav = document.getElementById("nav-" + v);
    if (nav) nav.classList.toggle("active", v === viewName);
    const pill = document.getElementById("pill-" + v);
    if (pill) pill.classList.toggle("active", v === viewName);
  }});
  if (viewName === "checkout") {{
    document.getElementById("checkout-live-form").style.display = "grid";
    document.getElementById("checkout-confirmation-box").style.display = "none";
    renderCheckoutSummary();
  }}
  window.scrollTo({{ top: 0, behavior: "smooth" }});
}}

function openCurateWithCategory(catId, kw) {{
  state.category = catId || "ALL";
  state.colors.clear();
  state.periods.clear();
  document.getElementById("keyword-input").value = kw || "";
  renderControls();
  applyFilters();
  switchView("curate");
}}

/* ==========================================================================
   HERO CAROUSEL (SLIDE 1: SLATE FURNITURE, SLIDE 2: CARPET COLLAGE, SLIDE 3: TRINKET COLLAGE)
   ========================================================================== */
let heroAutoplayTimer = null;

function setHeroSlide(idx) {{
  state.heroSlide = (idx + 3) % 3;
  for (let i = 0; i < 3; i++) {{
    document.getElementById("hero-slide-" + i).classList.toggle("active", i === state.heroSlide);
    document.getElementById("dot-" + i).classList.toggle("active", i === state.heroSlide);
  }}
}}

function stepHeroSlide(delta) {{
  setHeroSlide(state.heroSlide + delta);
  restartHeroAutoplay();
}}

function startHeroAutoplay() {{
  if (heroAutoplayTimer) clearInterval(heroAutoplayTimer);
  heroAutoplayTimer = setInterval(() => {{
    if (state.view === "home") {{
      setHeroSlide(state.heroSlide + 1);
    }}
  }}, 4500);
}}

function restartHeroAutoplay() {{
  startHeroAutoplay();
}}

const heroEl = document.querySelector(".hero-carousel");
if (heroEl) {{
  heroEl.addEventListener("mouseenter", () => {{
    if (heroAutoplayTimer) clearInterval(heroAutoplayTimer);
  }});
  heroEl.addEventListener("mouseleave", () => {{
    startHeroAutoplay();
  }});
}}

function initHeroCollages() {{
  const carpets = CATALOG.filter(i => i.top_category === "CARPETS & RUNNERS" && i.image);
  const trinkets = CATALOG.filter(i => (i.top_category === "BRONZES & SCULPTURE" || i.top_category === "DECORATIVE ARTS") && i.image);

  const c1 = carpets[0] || CATALOG[0];
  const c2 = carpets[1] || CATALOG[0];
  const c3 = carpets[2] || CATALOG[0];
  document.getElementById("hero-carpet-collage").innerHTML = `
    <div class="hero-macro-cell tall" onclick="openCurateWithCategory('CARPETS & RUNNERS', '')">
      <img src="${{c1.image}}" alt="${{c1.name}}">
      <div class="hero-furniture-tag">${{c1.name.slice(0, 38)}}</div>
    </div>
    <div class="hero-macro-cell" onclick="openCurateWithCategory('CARPETS & RUNNERS', '')">
      <img src="${{c2.image}}" alt="${{c2.name}}">
    </div>
    <div class="hero-macro-cell" onclick="openCurateWithCategory('CARPETS & RUNNERS', '')">
      <img src="${{c3.image}}" alt="${{c3.name}}">
    </div>`;

  const t1 = trinkets[0] || CATALOG[0];
  const t2 = trinkets[1] || CATALOG[0];
  const t3 = trinkets[2] || CATALOG[0];
  document.getElementById("hero-trinket-collage").innerHTML = `
    <div class="hero-macro-cell tall" onclick="openCurateWithCategory('BRONZES & SCULPTURE', '')">
      <img src="${{t1.image}}" alt="${{t1.name}}">
      <div class="hero-furniture-tag">${{t1.name.slice(0, 38)}}</div>
    </div>
    <div class="hero-macro-cell" onclick="openCurateWithCategory('FINE ART', '')">
      <img src="${{t2.image}}" alt="${{t2.name}}">
    </div>
    <div class="hero-macro-cell" onclick="openCurateWithCategory('FINE ART', '')">
      <img src="${{t3.image}}" alt="${{t3.name}}">
    </div>`;
}}

/* ==========================================================================
   GALLERY LOOKBOOK CHAPTERS (ZERO PRICES, ZERO CART BUTTONS)
   ========================================================================== */
function renderGalleryLookbooks() {{
  const chapters = [
    {{ title: "European Period Furniture (Studio Slate & Showroom)", cat: "EUROPEAN FURNITURE", items: CATALOG.filter(i => i.top_category === "EUROPEAN FURNITURE").slice(0, 8) }},
    {{ title: "Court, Palace & Village Carpets", cat: "CARPETS & RUNNERS", items: CATALOG.filter(i => i.top_category === "CARPETS & RUNNERS").slice(0, 8) }},
    {{ title: "Historic Tapestries & Fine Art", cat: "TAPESTRIES", items: CATALOG.filter(i => i.top_category === "TAPESTRIES" || i.top_category === "FINE ART").slice(0, 8) }},
    {{ title: "Bronzes, Sèvres Porcelain & Giltwood Objects", cat: "BRONZES & SCULPTURE", items: CATALOG.filter(i => i.top_category === "BRONZES & SCULPTURE" || i.top_category === "DECORATIVE ARTS").slice(0, 8) }}
  ];

  const mount = document.getElementById("lookbook-chapters-mount");
  mount.innerHTML = chapters.map(ch => `
    <div class="lookbook-chapter">
      <div class="chapter-header">
        <div class="chapter-title">${{ch.title}}</div>
        <button type="button" class="chapter-curate-link" onclick="openCurateWithCategory('${{ch.cat}}', '')">Curate This Category &rarr;</button>
      </div>
      <div class="chapter-track">
        ${{ch.items.map(item => `
          <div class="lookbook-card" onclick="openEditorialModal(${{item.id}})">
            <div class="lookbook-img-box">
              <img src="${{item.image}}" alt="${{item.name.replace(/"/g, '&quot;')}}" loading="lazy">
            </div>
            <div class="lookbook-cat">${{item.sub_category}}</div>
            <div class="lookbook-name">${{item.name}}</div>
            ${{item.size_label ? `<div class="lookbook-dims">${{item.size_label}}</div>` : ''}}
          </div>
        `).join("")}}
      </div>
    </div>
  `).join("");
}}

function openEditorialModal(itemId) {{
  const item = CATALOG.find(i => i.id === itemId);
  if (!item) return;
  document.getElementById("modal-img").src = item.image;
  document.getElementById("modal-cat").textContent = item.sub_category;
  document.getElementById("modal-title").textContent = item.name;
  document.getElementById("modal-dims").textContent = item.size_label ? ("Dimensions: " + item.size_label) : "Rancho Santa Fe Showroom Collection";
  document.getElementById("modal-curate-btn").onclick = () => {{
    closeEditorialModal();
    openCurateWithCategory(item.top_category, item.name.split(" ").slice(0, 2).join(" "));
  }};
  document.getElementById("editorial-modal-backdrop").classList.add("open");
}}

function closeEditorialModal() {{
  document.getElementById("editorial-modal-backdrop").classList.remove("open");
}}

/* ==========================================================================
   CURATE YOUR COLLECTION CONSOLE (ITEMIZED FILTERS + UNLOCKED PRICES + CART)
   ========================================================================== */
function renderControls() {{
  const catBar = document.getElementById("category-bar");
  catBar.innerHTML = CATEGORY_TILES.map(cat => {{
    const count = cat.id === "ALL"
      ? CATALOG.length
      : CATALOG.filter(i => i.top_category === cat.id || (cat.id === "FINE ART" && i.top_category === "DECORATIVE ARTS")).length;
    const active = state.category === cat.id ? "active" : "";
    return `<div class="cat-tile ${{active}}" onclick="selectCategory('${{cat.id}}')">
      ${{cat.label}}
      <span class="cat-count">${{count}} Pieces</span>
    </div>`;
  }}).join("");

  const swatchRow = document.getElementById("swatch-row");
  swatchRow.innerHTML = SWATCHES.map(sw => {{
    const active = state.colors.has(sw.id) ? "active" : "";
    return `<div class="color-swatch ${{active}}" style="background-color:${{sw.hex}}" title="${{sw.label}}" onclick="toggleColor('${{sw.id}}')"></div>`;
  }}).join("");

  const periodPills = document.getElementById("period-pills");
  periodPills.innerHTML = PERIODS.map(p => {{
    const active = state.periods.has(p.id) ? "active" : "";
    return `<button type="button" class="period-pill ${{active}}" onclick="togglePeriod('${{p.id}}')">${{p.label}}</button>`;
  }}).join("");
}}

function selectCategory(catId) {{
  state.category = catId;
  renderControls();
  applyFilters();
}}

function toggleColor(colorId) {{
  if (state.colors.has(colorId)) state.colors.delete(colorId);
  else state.colors.add(colorId);
  renderControls();
  applyFilters();
}}

function togglePeriod(periodId) {{
  if (state.periods.has(periodId)) state.periods.delete(periodId);
  else state.periods.add(periodId);
  renderControls();
  applyFilters();
}}

function setUnit(unit) {{
  state.unit = unit;
  document.getElementById("unit-ft").classList.toggle("active", unit === "FT");
  document.getElementById("unit-cm").classList.toggle("active", unit === "CM");
  applyFilters();
}}

function resetFilters() {{
  state.category = "ALL";
  state.colors.clear();
  state.periods.clear();
  document.getElementById("min-w").value = "";
  document.getElementById("min-l").value = "";
  document.getElementById("max-w").value = "";
  document.getElementById("max-l").value = "";
  document.getElementById("keyword-input").value = "";
  renderControls();
  applyFilters();
}}

function applyFilters() {{
  const kw = document.getElementById("keyword-input").value.trim().toLowerCase();
  const minW = parseFloat(document.getElementById("min-w").value);
  const minL = parseFloat(document.getElementById("min-l").value);
  const maxW = parseFloat(document.getElementById("max-w").value);
  const maxL = parseFloat(document.getElementById("max-l").value);
  const toFt = state.unit === "CM" ? (1 / 30.48) : 1.0;

  let filtered = CATALOG.filter(item => {{
    if (state.category !== "ALL") {{
      if (state.category === "FINE ART") {{
        if (item.top_category !== "FINE ART" && item.top_category !== "DECORATIVE ARTS") return false;
      }} else if (item.top_category !== state.category) {{
        return false;
      }}
    }}
    if (state.colors.size > 0 && !item.colors.some(c => state.colors.has(c))) return false;
    if (state.periods.size > 0 && !item.periods.some(p => state.periods.has(p))) return false;
    if (!isNaN(minW) && item.w_ft !== null && item.w_ft < minW * toFt) return false;
    if (!isNaN(minL) && item.l_ft !== null && item.l_ft < minL * toFt) return false;
    if (!isNaN(maxW) && item.w_ft !== null && item.w_ft > maxW * toFt) return false;
    if (!isNaN(maxL) && item.l_ft !== null && item.l_ft > maxL * toFt) return false;
    if (kw && !item.search_blob.includes(kw)) return false;
    return true;
  }});

  const sortMode = document.getElementById("sort-select").value;
  if (sortMode === "price-desc") {{
    filtered.sort((a, b) => (parseFloat(b.active_price) || 0) - (parseFloat(a.active_price) || 0));
  }} else if (sortMode === "price-asc") {{
    filtered.sort((a, b) => (parseFloat(a.active_price) || 0) - (parseFloat(b.active_price) || 0));
  }} else if (sortMode === "title-asc") {{
    filtered.sort((a, b) => a.name.localeCompare(b.name));
  }}

  document.getElementById("results-count").textContent =
    `Showing ${{filtered.length}} of ${{CATALOG.length}} Curated Pieces (Prices Unlocked)`;

  const grid = document.getElementById("gallery-grid");
  grid.innerHTML = filtered.map(item => {{
    const hasSale = item.sale_price && item.sale_price !== item.regular_price;
    const priceHtml = hasSale
      ? `<del>${{formatPrice(item.regular_price)}}</del><span>${{formatPrice(item.sale_price)}}</span>`
      : `<span>${{formatPrice(item.active_price)}}</span>`;
    const inCart = state.cart.some(c => c.id === item.id);
    return `<div class="gallery-card">
      <div class="card-img-box" onclick="toggleCartItem(${{item.id}})">
        <img src="${{item.image}}" alt="${{item.name.replace(/"/g, '&quot;')}}" loading="lazy">
      </div>
      <div class="card-cat">${{item.sub_category}}</div>
      <div class="card-title">${{item.name}}</div>
      ${{item.size_label ? `<div class="card-meta">${{item.size_label}}</div>` : '<div class="card-meta">Rancho Santa Fe Showroom</div>'}}
      <div class="card-price">${{priceHtml}}</div>
      <div class="card-actions">
        <button type="button" class="btn-add-curate ${{inCart ? 'in-cart' : ''}}" onclick="toggleCartItem(${{item.id}})">
          ${{inCart ? '&#10003; In Your Selection' : '+ Add to Selection'}}
        </button>
        <button type="button" class="btn-instant-checkout" onclick="instantAcquire(${{item.id}})">Acquire &rarr;</button>
      </div>
    </div>`;
  }}).join("");
}}

/* ==========================================================================
   CURATED SELECTION DRAWER & WHITE-GLOVE CHECKOUT LOGIC
   ========================================================================== */
function toggleDrawer(open) {{
  document.getElementById("drawer-backdrop").classList.toggle("open", open);
  document.getElementById("selection-drawer").classList.toggle("open", open);
  renderCartDrawer();
}}

function toggleCartItem(itemId) {{
  const idx = state.cart.findIndex(c => c.id === itemId);
  if (idx >= 0) {{
    state.cart.splice(idx, 1);
  }} else {{
    const item = CATALOG.find(i => i.id === itemId);
    if (item) state.cart.push(item);
    toggleDrawer(true);
  }}
  updateCartBadge();
  applyFilters();
  renderCartDrawer();
}}

function instantAcquire(itemId) {{
  const item = CATALOG.find(i => i.id === itemId);
  if (item && !state.cart.some(c => c.id === itemId)) {{
    state.cart.push(item);
  }}
  updateCartBadge();
  applyFilters();
  switchView("checkout");
}}

function updateCartBadge() {{
  document.getElementById("nav-cart-count").textContent = state.cart.length;
}}

function getCartSubtotal() {{
  return state.cart.reduce((acc, item) => acc + (parseFloat(item.active_price) || 0), 0);
}}

function renderCartDrawer() {{
  const box = document.getElementById("drawer-items");
  if (state.cart.length === 0) {{
    box.innerHTML = `<p style="font-style:italic; color:var(--text-muted); text-align:center; padding:40px 0;">Your Curated Selection is currently empty. Add pieces inside Curate Your Collection.</p>`;
  }} else {{
    box.innerHTML = state.cart.map(item => `
      <div class="drawer-item">
        <img src="${{item.image}}" alt="">
        <div>
          <div class="drawer-item-title">${{item.name}}</div>
          <div class="drawer-item-price">${{formatPrice(item.active_price)}} ${{item.size_label ? '&middot; ' + item.size_label : ''}}</div>
        </div>
        <button type="button" class="drawer-remove" onclick="toggleCartItem(${{item.id}})">Remove</button>
      </div>
    `).join("");
  }}
  document.getElementById("drawer-subtotal-val").textContent = formatPrice(getCartSubtotal());
}}

function proceedToCheckout() {{
  toggleDrawer(false);
  switchView("checkout");
}}

function selectShipping(mode) {{
  state.shippingMode = mode;
  ["preview", "pickup", "carrier"].forEach(m => {{
    document.getElementById("ship-card-" + m).classList.toggle("active", m === mode);
  }});
  renderCheckoutSummary();
}}

function selectPayment(mode) {{
  state.paymentMode = mode;
  ["cc", "wire", "hold"].forEach(m => {{
    document.getElementById("pay-card-" + m).classList.toggle("active", m === mode);
  }});
  document.getElementById("cc-fields-box").style.display = (mode === "wire") ? "none" : "block";
  renderCheckoutSummary();
}}

function renderCheckoutSummary() {{
  const list = document.getElementById("checkout-items-list");
  list.innerHTML = state.cart.map(item => `
    <div class="drawer-item" style="grid-template-columns:60px 1fr auto;">
      <img src="${{item.image}}" style="width:60px; height:60px;" alt="">
      <div>
        <div class="drawer-item-title" style="font-size:14px;">${{item.name}}</div>
        <div class="drawer-item-price">${{item.size_label || 'Rancho Santa Fe Showroom'}}</div>
      </div>
      <div style="font-family:'Montserrat',sans-serif; font-size:12px; font-weight:500;">${{formatPrice(item.active_price)}}</div>
    </div>
  `).join("");

  const sub = getCartSubtotal();
  const wireDisc = state.paymentMode === "wire" ? Math.round(sub * 0.03) : 0;
  const finalTotal = state.paymentMode === "hold" ? 0 : (sub - wireDisc);

  document.getElementById("chk-subtotal").textContent = formatPrice(sub);
  document.getElementById("chk-wire-row").style.display = state.paymentMode === "wire" ? "flex" : "none";
  document.getElementById("chk-wire-discount").textContent = "-" + formatPrice(wireDisc);

  const shipLabels = {{
    preview: "Complimentary 48-Hr In-Home Preview",
    pickup: "Complimentary RSF Showroom Pickup",
    carrier: "Coordinated Post-Purchase"
  }};
  document.getElementById("chk-shipping-label").textContent = shipLabels[state.shippingMode];
  document.getElementById("chk-total-label").textContent = state.paymentMode === "hold" ? "Due Today (48-Hr Trial Hold)" : "Total Acquisition";
  document.getElementById("chk-total-val").textContent = state.paymentMode === "hold" ? "$0 (Auth Only)" : formatPrice(finalTotal);
}}

function submitWhiteGloveOrder() {{
  const fname = document.getElementById("chk-fname").value || "Collector";
  const addr = document.getElementById("chk-addr").value || "Rancho Santa Fe";
  const sub = getCartSubtotal();
  document.getElementById("checkout-live-form").style.display = "none";
  document.getElementById("checkout-confirmation-box").style.display = "block";

  document.getElementById("confirm-dynamic-copy").innerHTML =
    `Thank you, ${{fname}}. Your curated selection (${{state.cart.length}} pieces, valued at ${{formatPrice(sub)}}) has been placed on private showroom hold at 6014 La Granada. Melissa Chapman will text your mobile shortly from <strong>(858) 349-2638</strong> to confirm your white-glove appointment at ${{addr}}.`;

  document.getElementById("confirm-items-recap").innerHTML = state.cart.map(item => `
    <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #EEE; font-size:15px;">
      <span>${{item.name}}</span>
      <strong>${{formatPrice(item.active_price)}}</strong>
    </div>
  `).join("");
  window.scrollTo({{ top: 0, behavior: "smooth" }});
}}

function resetAfterOrder() {{
  switchView("home");
}}

/* ==========================================================================
   MANSOUR COLLAGE SPLASH ON HOME VIEW
   ========================================================================== */
function renderCollageSplash() {{
  const carpets = CATALOG.filter(i => i.top_category === "CARPETS & RUNNERS" && i.image);
  const tapestries = CATALOG.filter(i => i.top_category === "TAPESTRIES" && i.image);
  const findCarpet = (kw, fallbackIdx) => {{
    const m = carpets.find(c => c.search_blob.includes(kw));
    return m || carpets[fallbackIdx % carpets.length] || CATALOG[0];
  }};

  const tRunner   = findCarpet("runner", 0);
  const tTabriz   = findCarpet("tabriz", 1);
  const tQum      = findCarpet("qum", 2);
  const tHeriz    = findCarpet("heriz", 3);
  const tTapestry = tapestries[0] || findCarpet("pictorial", 4);
  const tKashan   = findCarpet("kashan", 5);
  const tSarouk   = findCarpet("sarouk", 6);
  const tBaluch   = findCarpet("baluch", 7);

  const tileHtml = (item, label, catId, kw) => `
    <div class="collage-tile" onclick="openCurateWithCategory('${{catId}}', '${{kw}}')">
      <div class="collage-tile-img-wrap">
        <img src="${{item.image}}" alt="${{label}}" loading="lazy">
      </div>
      <div class="collage-caption-bar">${{label}}</div>
    </div>`;

  const mount = document.getElementById("collage-splash-mount");
  mount.innerHTML = `
    <div class="collage-row-3">
      ${{tileHtml(tRunner,   "Gallery Runners", "CARPETS & RUNNERS", "runner")}}
      ${{tileHtml(tTabriz,   "Tabriz",          "CARPETS & RUNNERS", "tabriz")}}
      ${{tileHtml(tQum,      "Qum Silk",        "CARPETS & RUNNERS", "qum")}}
    </div>
    <div class="collage-row-2">
      ${{tileHtml(tHeriz,    "Heriz & Serapi",  "CARPETS & RUNNERS", "heriz")}}
      ${{tileHtml(tTapestry, "Tapestries",      "TAPESTRIES",        "")}}
    </div>
    <div class="collage-row-3">
      ${{tileHtml(tKashan,   "Kashan",          "CARPETS & RUNNERS", "kashan")}}
      ${{tileHtml(tSarouk,   "Sarouk & Palace", "CARPETS & RUNNERS", "sarouk")}}
      ${{tileHtml(tBaluch,   "Pictorial & Tribal", "CARPETS & RUNNERS", "baluch")}}
    </div>`;
}}

initHeroCollages();
startHeroAutoplay();
renderCollageSplash();
renderGalleryLookbooks();
renderControls();
updateCartBadge();
applyFilters();

/* Smart Scroll-Direction Header Tuck (Zero layout-height mutation -> zero scroll bounce) */
(function() {{
  const headerEl = document.querySelector(".brand-header");
  let lastScrollY = window.scrollY || 0;
  let ticking = false;

  window.addEventListener("scroll", () => {{
    if (!ticking) {{
      window.requestAnimationFrame(() => {{
        const currentY = Math.max(0, window.scrollY || 0);
        const delta = currentY - lastScrollY;

        if (currentY > 40) {{
          headerEl.classList.add("header-scrolled");
        }} else {{
          headerEl.classList.remove("header-scrolled");
          headerEl.classList.remove("header-tucked");
        }}

        if (currentY > 180 && delta > 10) {{
          // Scrolling down -> GPU-slide header smoothly out of the way (0px DOM layout shift)
          headerEl.classList.add("header-tucked");
        }} else if (delta < -8 || currentY <= 80) {{
          // Scrolling up or near top -> bring header right back
          headerEl.classList.remove("header-tucked");
        }}

        lastScrollY = currentY;
        ticking = false;
      }});
      ticking = true;
    }}
  }}, {{ passive: true }});
}})();

/* ==========================================================================
   THE NRL SUBTLE TOUCH:
   1. Real-Time WebGL Anisotropic Silk & Giltwood Specular Shader on Hero Colorblocks
   2. Cursor-Tracking Museum Gallery Spotlight (`--spot-x`, `--spot-y`) Across All Visual Stages
   ========================================================================== */
(function initNrlGalleryLightAndSilkShader() {{
  // 1. Attach WebGL Silk Sheen Canvas to each Hero Colorblock Panel
  const panels = document.querySelectorAll(".hero-colorblock-panel");
  const vsSource = `
    attribute vec2 a_pos;
    varying vec2 v_uv;
    void main() {{
      v_uv = a_pos * 0.5 + 0.5;
      gl_Position = vec4(a_pos, 0.0, 1.0);
    }}
  `;
  const fsSource = `
    precision mediump float;
    varying vec2 v_uv;
    uniform float u_time;
    uniform vec2 u_mouse;
    void main() {{
      vec2 uv = v_uv;
      float d = distance(uv, u_mouse);
      // Soft museum spotlight falloff around cursor
      float spot = smoothstep(0.68, 0.0, d);
      // Anisotropic woven silk & giltwood caustic waves
      float wave1 = sin((uv.x * 11.0 + uv.y * 7.0) + u_time * 0.55) * 0.5 + 0.5;
      float wave2 = cos((uv.x * 6.0 - uv.y * 13.0) - u_time * 0.38) * 0.5 + 0.5;
      float silk = pow(wave1 * wave2, 1.6);
      // Warm champagne-gold museum light (#FFF6E5)
      vec3 col = vec3(1.0, 0.965, 0.89) * (silk * 0.24 + spot * 0.34);
      gl_FragColor = vec4(col, silk * 0.26 + spot * 0.30);
    }}
  `;

  const glContexts = [];
  panels.forEach(panel => {{
    const canvas = document.createElement("canvas");
    canvas.className = "nrl-silk-webgl-canvas";
    canvas.width = 360;
    canvas.height = 360;
    panel.insertBefore(canvas, panel.firstChild);

    const gl = canvas.getContext("webgl", {{ alpha: true, premultipliedAlpha: false }});
    if (!gl) return;

    function compileShader(type, src) {{
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    }}
    const prog = gl.createProgram();
    gl.attachShader(prog, compileShader(gl.VERTEX_SHADER, vsSource));
    gl.attachShader(prog, compileShader(gl.FRAGMENT_SHADER, fsSource));
    gl.linkProgram(prog);
    gl.useProgram(prog);

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]), gl.STATIC_DRAW);
    const aPos = gl.getAttribLocation(prog, "a_pos");
    gl.enableVertexAttribArray(aPos);
    gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

    const uTime = gl.getUniformLocation(prog, "u_time");
    const uMouse = gl.getUniformLocation(prog, "u_mouse");
    const ctxObj = {{ gl, prog, uTime, uMouse, mx: 0.5, my: 0.5, tx: 0.5, ty: 0.5 }};
    glContexts.push(ctxObj);

    panel.addEventListener("mousemove", e => {{
      const r = panel.getBoundingClientRect();
      ctxObj.tx = (e.clientX - r.left) / Math.max(1, r.width);
      ctxObj.ty = 1.0 - (e.clientY - r.top) / Math.max(1, r.height);
    }});
    panel.addEventListener("mouseleave", () => {{
      ctxObj.tx = 0.5;
      ctxObj.ty = 0.5;
    }});
  }});

  function animateShaders(t) {{
    const sec = t * 0.001;
    glContexts.forEach(c => {{
      c.mx += (c.tx - c.mx) * 0.08;
      c.my += (c.ty - c.my) * 0.08;
      c.gl.viewport(0, 0, 360, 360);
      c.gl.clearColor(0, 0, 0, 0);
      c.gl.clear(c.gl.COLOR_BUFFER_BIT);
      c.gl.uniform1f(c.uTime, sec);
      c.gl.uniform2f(c.uMouse, c.mx, c.my);
      c.gl.drawArrays(c.gl.TRIANGLES, 0, 6);
    }});
    requestAnimationFrame(animateShaders);
  }}
  if (glContexts.length > 0) requestAnimationFrame(animateShaders);

  // 2. Attach Cursor-Reactive Museum Gallery Spotlight to Furniture, Carpet Collages & Cards
  function bindSpotlightTargets() {{
    const selectors = ".hero-furniture-card, .hero-macro-cell, .collage-tile-img-wrap, .lookbook-img-box, .card-img-box";
    document.querySelectorAll(selectors).forEach(el => {{
      if (el.dataset.nrlSpotBound) return;
      el.dataset.nrlSpotBound = "1";
      el.classList.add("nrl-spotlight-surface");
      el.addEventListener("mousemove", e => {{
        const r = el.getBoundingClientRect();
        el.style.setProperty("--spot-x", (e.clientX - r.left) + "px");
        el.style.setProperty("--spot-y", (e.clientY - r.top) + "px");
      }});
    }});
  }}
  bindSpotlightTargets();
  // Re-bind whenever filters re-render cards
  const origApply = window.applyFilters;
  if (typeof origApply === "function") {{
    window.applyFilters = function() {{
      origApply.apply(this, arguments);
      bindSpotlightTargets();
    }};
  }}

  // 3. NRL Butter-Muslin / Cheesecloth Gauze Weave Engine (Strictly z-index: 0 behind all products)
  const draftCanvas = document.getElementById("nrl-curtain-draft-canvas");
  if (draftCanvas) {{
    const ctx = draftCanvas.getContext("2d");
    const CELL = 18;         // Physics control cell size (18px)
    const SUB = 4;           // 4 fine cheesecloth yarns per cell (4.5px actual thread pitch)
    let width = 0, height = 0, cols = 0, rows = 0;
    let nodes = [];
    let warpCrimp = [];
    let weftCrimp = [];

    const pointer = {{ x: -9999, y: -9999, prevX: -9999, prevY: -9999, vx: 0, vy: 0, active: false }};

    function rebuildGrid() {{
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      draftCanvas.width = Math.floor(width * dpr);
      draftCanvas.height = Math.floor(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      cols = Math.ceil(width / CELL) + 2;
      rows = Math.ceil(height / CELL) + 2;
      nodes = new Array(cols * rows);
      for (let r = 0; r < rows; r++) {{
        for (let c = 0; c < cols; c++) {{
          nodes[r * cols + c] = {{
            bx: c * CELL,
            by: r * CELL,
            ox: 0,
            oy: 0,
            vx: 0,
            vy: 0,
            glow: 0
          }};
        }}
      }}

      const totalRows = rows * SUB;
      const totalCols = cols * SUB;
      warpCrimp = new Float32Array(totalRows);
      weftCrimp = new Float32Array(totalCols);
      for (let i = 0; i < totalRows; i++) {{
        warpCrimp[i] = Math.sin(i * 1.73) * 0.42 + Math.cos(i * 0.61) * 0.28;
      }}
      for (let j = 0; j < totalCols; j++) {{
        weftCrimp[j] = Math.cos(j * 1.91) * 0.42 + Math.sin(j * 0.79) * 0.28;
      }}
    }}
    window.addEventListener("resize", rebuildGrid, {{ passive: true }});
    rebuildGrid();

    window.addEventListener("pointermove", (e) => {{
      if (!pointer.active) {{
        pointer.prevX = e.clientX;
        pointer.prevY = e.clientY;
        pointer.active = true;
      }}
      const rawDx = e.clientX - pointer.prevX;
      const rawDy = e.clientY - pointer.prevY;
      pointer.prevX = e.clientX;
      pointer.prevY = e.clientY;
      pointer.x = e.clientX;
      pointer.y = e.clientY;

      pointer.vx = pointer.vx * 0.74 + rawDx * 0.26;
      pointer.vy = pointer.vy * 0.74 + rawDy * 0.26;

      const speed = Math.hypot(pointer.vx, pointer.vy);
      const draftRadius = 225;
      const rSq = draftRadius * draftRadius;

      const minC = Math.max(0, Math.floor((pointer.x - draftRadius) / CELL));
      const maxC = Math.min(cols - 1, Math.ceil((pointer.x + draftRadius) / CELL));
      const minR = Math.max(0, Math.floor((pointer.y - draftRadius) / CELL));
      const maxR = Math.min(rows - 1, Math.ceil((pointer.y + draftRadius) / CELL));

      const clampedSpeed = Math.min(speed, 22);
      const dirX = speed > 0.1 ? pointer.vx / speed : 0;
      const dirY = speed > 0.1 ? pointer.vy / speed : 0;

      for (let r = minR; r <= maxR; r++) {{
        const rowOffset = r * cols;
        for (let c = minC; c <= maxC; c++) {{
          const n = nodes[rowOffset + c];
          const dx = n.bx - pointer.x;
          const dy = n.by - pointer.y;
          const dSq = dx * dx + dy * dy;
          if (dSq < rSq) {{
            const dist = Math.sqrt(dSq);
            const falloff = Math.pow(1 - dist / draftRadius, 2.15);

            const pullStrength = falloff * (0.105 * clampedSpeed + 0.15);
            n.vx += dirX * pullStrength;
            n.vy += dirY * pullStrength;

            if (dist > 1) {{
              const radialPush = falloff * 0.085;
              n.vx += (dx / dist) * radialPush;
              n.vy += (dy / dist) * radialPush;
            }}

            const targetGlow = Math.min(1, falloff * (0.38 + clampedSpeed * 0.032));
            if (targetGlow > n.glow) {{
              n.glow = n.glow + (targetGlow - n.glow) * 0.32;
            }}
          }}
        }}
      }}
    }}, {{ passive: true }});

    const SPRING = 0.013;
    const DAMPING = 0.968;
    const GLOW_DECAY = 0.980;
    const MAX_DISP = 14.5;

    function renderCheeseclothGauze() {{
      pointer.vx *= 0.92;
      pointer.vy *= 0.92;
      ctx.clearRect(0, 0, width, height);

      let maxActiveGlow = 0;
      for (let i = 0; i < nodes.length; i++) {{
        const n = nodes[i];
        n.vx += -n.ox * SPRING;
        n.vy += -n.oy * SPRING;
        n.vx *= DAMPING;
        n.vy *= DAMPING;
        n.ox += n.vx;
        n.oy += n.vy;

        const disp = Math.hypot(n.ox, n.oy);
        if (disp > MAX_DISP) {{
          const scale = MAX_DISP / disp;
          n.ox *= scale;
          n.oy *= scale;
        }}
        n.glow *= GLOW_DECAY;
        if (n.glow < 0.002) n.glow = 0;
        else if (n.glow > maxActiveGlow) maxActiveGlow = n.glow;
      }}

      for (let pass = 0; pass < 2; pass++) {{
        ctx.beginPath();
        if (pass === 0) {{
          ctx.lineWidth = 0.55;
          ctx.strokeStyle = "rgba(174, 160, 138, 0.064)";
        }} else {{
          ctx.lineWidth = 0.40;
          ctx.strokeStyle = "rgba(182, 169, 148, 0.042)";
        }}

        for (let r = 0; r < rows - 1; r++) {{
          const r0 = r * cols;
          const r1 = (r + 1) * cols;
          for (let s = 0; s < SUB; s++) {{
            if ((s === 0) !== (pass === 0)) continue;
            const frac = s / SUB;
            const crimpY = warpCrimp[r * SUB + s];
            for (let c = 0; c < cols; c++) {{
              const n0 = nodes[r0 + c];
              const n1 = nodes[r1 + c];
              const ox = n0.ox + (n1.ox - n0.ox) * frac;
              const oy = n0.oy + (n1.oy - n0.oy) * frac;
              const wave = Math.sin(c * 0.9 + s * 1.7) * 0.38 + crimpY;
              const px = n0.bx + ox;
              const py = n0.by + frac * CELL + oy + wave;
              if (c === 0) ctx.moveTo(px, py);
              else ctx.lineTo(px, py);
            }}
          }}
        }}

        for (let c = 0; c < cols - 1; c++) {{
          for (let s = 0; s < SUB; s++) {{
            if ((s === 0) !== (pass === 0)) continue;
            const frac = s / SUB;
            const crimpX = weftCrimp[c * SUB + s];
            for (let r = 0; r < rows; r++) {{
              const rOff = r * cols;
              const n0 = nodes[rOff + c];
              const n1 = nodes[rOff + c + 1];
              const ox = n0.ox + (n1.ox - n0.ox) * frac;
              const oy = n0.oy + (n1.oy - n0.oy) * frac;
              const wave = Math.cos(r * 0.9 + s * 1.7) * 0.38 + crimpX;
              const px = n0.bx + frac * CELL + ox + wave;
              const py = n0.by + oy;
              if (r === 0) ctx.moveTo(px, py);
              else ctx.lineTo(px, py);
            }}
          }}
        }}
        ctx.stroke();
      }}

      if (maxActiveGlow > 0.008) {{
        for (let r = 0; r < rows - 1; r++) {{
          const r0 = r * cols;
          const r1 = (r + 1) * cols;
          for (let c = 0; c < cols - 1; c++) {{
            const n00 = nodes[r0 + c];
            const g = n00.glow;
            if (g < 0.012) continue;

            const n10 = nodes[r0 + c + 1];
            const n01 = nodes[r1 + c];
            const n11 = nodes[r1 + c + 1];

            ctx.beginPath();
            for (let s = 0; s < SUB; s++) {{
              const f = s / SUB;
              const hx0 = n00.bx + n00.ox + (n01.ox - n00.ox) * f;
              const hy0 = n00.by + f * CELL + n00.oy + (n01.oy - n00.oy) * f;
              const hx1 = n10.bx + n10.ox + (n11.ox - n10.ox) * f;
              const hy1 = n10.by + f * CELL + n10.oy + (n11.oy - n10.oy) * f;
              ctx.moveTo(hx0, hy0);
              ctx.lineTo(hx1, hy1);

              const vx0 = n00.bx + f * CELL + n00.ox + (n10.ox - n00.ox) * f;
              const vy0 = n00.by + n00.oy + (n10.oy - n00.oy) * f;
              const vx1 = n01.bx + f * CELL + n01.ox + (n11.ox - n01.ox) * f;
              const vy1 = n01.by + n01.oy + (n11.oy - n01.oy) * f;
              ctx.moveTo(vx0, vy0);
              ctx.lineTo(vx1, vy1);
            }}
            ctx.lineWidth = 0.55 + g * 0.35;
            ctx.strokeStyle = `rgba(176, 148, 98, ${{(g * 0.16).toFixed(3)}})`;
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(n00.bx + n00.ox, n00.by + n00.oy);
            ctx.lineTo(n10.bx + n10.ox, n10.by + n10.oy);
            ctx.lineWidth = 0.85;
            ctx.strokeStyle = `rgba(255, 253, 248, ${{(g * 0.52).toFixed(3)}})`;
            ctx.stroke();
          }}
        }}
      }}

      requestAnimationFrame(renderCheeseclothGauze);
    }}
    requestAnimationFrame(renderCheeseclothGauze);
  }}
}})();
</script>
</body>
</html>
"""

    os.makedirs(OUT_DIR_NRL, exist_ok=True)
    with open(os.path.join(OUT_DIR_NRL, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(OUT_DIR_NRL, "chapman-curatorial-gallery-search.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(OUT_FILE_PMC, "w", encoding="utf-8") as f:
        f.write(html)
    print("Compiled full 4-view Mansour click-flow & white-glove checkout prototype:")
    print(" ->", os.path.join(OUT_DIR_NRL, "chapman-curatorial-gallery-search.html"))
    print(" ->", OUT_FILE_PMC)


if __name__ == "__main__":
    main()
