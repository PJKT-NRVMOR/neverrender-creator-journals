import os
import zlib

HELV_WIDTHS = {
    ' ': 278, '!': 278, '"': 355, '#': 556, '$': 556, '%': 889, '&': 667, "'": 191,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 278, ';': 278, '<': 584, '=': 584, '>': 584, '?': 556,
    '@': 1015, 'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 278, '\\': 278, ']': 278, '^': 469, '_': 556,
    '`': 333, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556, 'f': 278, 'g': 556,
    'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222, 'm': 833, 'n': 556, 'o': 556,
    'p': 556, 'q': 556, 'r': 333, 's': 500, 't': 278, 'u': 556, 'v': 500, 'w': 722,
    'x': 500, 'y': 500, 'z': 500, '{': 334, '|': 260, '}': 334, '~': 584, '•': 350,
}

HELV_BOLD_WIDTHS = {
    ' ': 278, '!': 333, '"': 474, '#': 556, '$': 556, '%': 889, '&': 722, "'": 278,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 333, ';': 333, '<': 584, '=': 584, '>': 584, '?': 611,
    '@': 975, 'A': 722, 'B': 722, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 556, 'K': 722, 'L': 611, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 584, '_': 556,
    'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556, 'f': 333, 'g': 611, 'h': 611,
    'i': 278, 'j': 278, 'k': 556, 'l': 278, 'm': 889, 'n': 611, 'o': 611, 'p': 611,
    'q': 611, 'r': 389, 's': 556, 't': 333, 'u': 611, 'v': 556, 'w': 778, 'x': 556,
    'y': 556, 'z': 500, '|': 280, '•': 350,
}


def font_key_width(text, font_key, font_size):
    if font_key in ("F3", "F4"):
        return len(text) * 0.600 * font_size
    table = HELV_BOLD_WIDTHS if font_key == "F1" else HELV_WIDTHS
    total = sum(table.get(ch, 556) for ch in text)
    return (total / 1000.0) * font_size


def text_width(text, font_name, font_size):
    if font_name.startswith("Courier"):
        return len(text) * 0.600 * font_size
    table = HELV_BOLD_WIDTHS if font_name == "Helvetica-Bold" else HELV_WIDTHS
    total = sum(table.get(ch, 556) for ch in text)
    return (total / 1000.0) * font_size


def pdf_escape(s):
    out = []
    for ch in s:
        if ch == '•':
            out.append('\\225')
        elif ch == '\\':
            out.append('\\\\')
        elif ch == '(':
            out.append('\\(')
        elif ch == ')':
            out.append('\\)')
        else:
            out.append(ch)
    return "".join(out)


def wrap_courier_segments(segments, max_width, font_size):
    """
    Tokenizes styled Courier segments while preserving exact attachment for punctuation.
    """
    char_w = 0.600 * font_size
    max_chars = int(max_width // char_w)

    composite_words = []
    current_word = []

    for text, fkey, col in segments:
        if not text:
            continue
        i = 0
        n = len(text)
        while i < n:
            if text[i] == ' ':
                if current_word:
                    composite_words.append(current_word)
                    current_word = []
                while i < n and text[i] == ' ':
                    i += 1
            else:
                j = i
                while j < n and text[j] != ' ':
                    j += 1
                current_word.append((text[i:j], fkey, col))
                i = j

    if current_word:
        composite_words.append(current_word)

    lines = []
    curr_line = []
    curr_len = 0

    for cword in composite_words:
        w_len = sum(len(piece[0]) for piece in cword)
        add_len = w_len if curr_len == 0 else (1 + w_len)
        if curr_len + add_len <= max_chars or curr_len == 0:
            if curr_len > 0:
                curr_line.append((' ', cword[0][1], cword[0][2]))
                curr_len += 1
            curr_line.extend(cword)
            curr_len += w_len
        else:
            lines.append(curr_line)
            curr_line = list(cword)
            curr_len = w_len

    if curr_line:
        lines.append(curr_line)
    return lines


def wrap_proportional_segments(segments, max_width, font_size):
    """
    Tokenizes styled Helvetica/Helvetica-Bold segments using exact Type1 glyph widths.
    """
    composite_words = []
    current_word = []

    for text, fkey, col in segments:
        if not text:
            continue
        i = 0
        n = len(text)
        while i < n:
            if text[i] == ' ':
                if current_word:
                    composite_words.append(current_word)
                    current_word = []
                while i < n and text[i] == ' ':
                    i += 1
            else:
                j = i
                while j < n and text[j] != ' ':
                    j += 1
                current_word.append((text[i:j], fkey, col))
                i = j

    if current_word:
        composite_words.append(current_word)

    lines = []
    curr_line = []
    curr_w = 0.0

    for cword in composite_words:
        word_w = sum(font_key_width(piece[0], piece[1], font_size) for piece in cword)
        space_fk = cword[0][1]
        space_w = font_key_width(' ', space_fk, font_size)
        add_w = word_w if curr_w == 0.0 else (space_w + word_w)
        if curr_w + add_w <= max_width or curr_w == 0.0:
            if curr_w > 0.0:
                curr_line.append((' ', space_fk, cword[0][2]))
                curr_w += space_w
            curr_line.extend(cword)
            curr_w += word_w
        else:
            lines.append(curr_line)
            curr_line = list(cword)
            curr_w = word_w

    if curr_line:
        lines.append(curr_line)
    return lines


class VectorPDFPage:
    def __init__(self, width=612, height=792):
        self.width = width
        self.height = height
        self.ops = []
        self.links = []

    def set_fill_rgb(self, r, g, b):
        self.ops.append(f"{r:.4f} {g:.4f} {b:.4f} rg")

    def set_stroke_rgb(self, r, g, b):
        self.ops.append(f"{r:.4f} {g:.4f} {b:.4f} RG")

    def set_line_width(self, w):
        self.ops.append(f"{w:.2f} w")

    def rect_fill(self, x, y, w, h, rgb):
        self.set_fill_rgb(*rgb)
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re f")

    def rect_stroke(self, x, y, w, h, rgb, line_w=1.0):
        self.set_stroke_rgb(*rgb)
        self.set_line_width(line_w)
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re S")

    def rect_fill_stroke(self, x, y, w, h, fill_rgb, stroke_rgb, line_w=1.0):
        self.set_fill_rgb(*fill_rgb)
        self.set_stroke_rgb(*stroke_rgb)
        self.set_line_width(line_w)
        self.ops.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re B")

    def line(self, x1, y1, x2, y2, rgb, line_w=1.0):
        self.set_stroke_rgb(*rgb)
        self.set_line_width(line_w)
        self.ops.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def hud_corner_ticks(self, x, y, w, h, top_left_rgb, bottom_right_rgb, tick_len=7.0, line_w=1.8):
        self.set_stroke_rgb(*top_left_rgb)
        self.set_line_width(line_w)
        self.ops.append(f"{x:.2f} {y + h - tick_len:.2f} m {x:.2f} {y + h:.2f} l {x + tick_len:.2f} {y + h:.2f} l S")
        self.set_stroke_rgb(*bottom_right_rgb)
        self.set_line_width(line_w)
        self.ops.append(f"{x + w - tick_len:.2f} {y:.2f} m {x + w:.2f} {y:.2f} l {x + w:.2f} {y + tick_len:.2f} l S")

    def text(self, x, y, s, font_key="F3", size=9.0, rgb=(0.043, 0.055, 0.110)):
        self.set_fill_rgb(*rgb)
        esc = pdf_escape(s)
        self.ops.append(f"BT /{font_key} {size:.2f} Tf {x:.2f} {y:.2f} Td ({esc}) Tj ET")

    def text_center(self, cx, y, s, font_key="F1", size=10.0, rgb=(0.043, 0.055, 0.110)):
        w = font_key_width(s, font_key, size)
        self.text(cx - w / 2.0, y, s, font_key=font_key, size=size, rgb=rgb)

    def text_right(self, rx, y, s, font_key="F3", size=8.0, rgb=(0.043, 0.055, 0.110)):
        w = font_key_width(s, font_key, size)
        self.text(rx - w, y, s, font_key=font_key, size=size, rgb=rgb)

    def draw_styled_lines(self, x, y_top, lines, size=8.6, leading=12.0):
        y = y_top
        for line in lines:
            cx = x
            merged = []
            for tok, fkey, col in line:
                if merged and merged[-1][1] == fkey and merged[-1][2] == col:
                    merged[-1] = (merged[-1][0] + tok, fkey, col)
                else:
                    merged.append((tok, fkey, col))
            for tok, fkey, col in merged:
                self.text(cx, y, tok, font_key=fkey, size=size, rgb=col)
                cx += font_key_width(tok, fkey, size)
            y -= leading
        return y

    def add_link(self, x, y, w, h, url):
        self.links.append((x, y, x + w, y + h, url))


def write_pdf(pages, output_path, pdf_title="Matthew Cole Wyatt - Resume (Nov 2026)"):
    objects = []

    def add_obj(content_bytes):
        objects.append(content_bytes)
        return len(objects)

    f1_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    f2_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    f3_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
    f4_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>")

    res_dict = f"<< /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R /F4 {f4_id} 0 R >> >>".encode("ascii")
    res_id = add_obj(res_dict)

    page_ids = []
    pages_tree_placeholder_id = add_obj(b"")

    for p in pages:
        stream_raw = "\n".join(p.ops).encode("latin1")
        compressed = zlib.compress(stream_raw)
        stream_obj = (
            f"<< /Length {len(compressed)} /Filter /FlateDecode >>\nstream\n".encode("ascii")
            + compressed
            + b"\nendstream"
        )
        content_id = add_obj(stream_obj)

        annot_refs = []
        for (x1, y1, x2, y2, url) in p.links:
            annot_bytes = (
                f"<< /Type /Annot /Subtype /Link /Rect [{x1:.2f} {y1:.2f} {x2:.2f} {y2:.2f}] "
                f"/Border [0 0 0] /A << /Type /Action /S /URI /URI ({url}) >> >>"
            ).encode("ascii")
            annot_refs.append(f"{add_obj(annot_bytes)} 0 R")

        annots_str = f"/Annots [{' '.join(annot_refs)}]" if annot_refs else ""
        page_dict = (
            f"<< /Type /Page /Parent {pages_tree_placeholder_id} 0 R "
            f"/MediaBox [0 0 {p.width} {p.height}] "
            f"/Resources {res_id} 0 R "
            f"/Contents {content_id} 0 R {annots_str} >>"
        ).encode("ascii")
        page_ids.append(add_obj(page_dict))

    kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[pages_tree_placeholder_id - 1] = (
        f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_ids)} >>".encode("ascii")
    )

    catalog_id = add_obj(f"<< /Type /Catalog /Pages {pages_tree_placeholder_id} 0 R >>".encode("ascii"))
    info_id = add_obj(
        f"<< /Title ({pdf_escape(pdf_title)}) "
        f"/Author (Matthew Cole Wyatt // NeverRender Labs) "
        f"/Creator (NeverRender Labs Vector PDF Engine v4.2) "
        f"/Producer (NeverRender Labs Vector PDF Engine v4.2) >>".encode("ascii")
    )

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for idx, obj_bytes in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{idx} 0 obj\n".encode("ascii"))
        out.extend(obj_bytes)
        out.extend(b"\nendobj\n")

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))

    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R /Info {info_id} 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(out)


# ==============================================================================
# COLOR PALETTE: AGENT TRINITY // GEMINI 4 CARBON v4.2 (PRINTER-FRIENDLY OBSIDIAN)
# ==============================================================================
OBSIDIAN       = (0.043, 0.055, 0.118)  # #0B0E1E - Primary Deep Obsidian
OBSIDIAN_BODY  = (0.090, 0.114, 0.200)  # #171D33 - Rich Obsidian-Indigo body text
OBSIDIAN_MUTED = (0.310, 0.357, 0.475)  # #4F5B79 - Muted Slate-Indigo metadata
TRINITY_MAG    = (0.831, 0.086, 0.722)  # #D416B8 - Electric Trinity Magenta (printer-crisp)
CARBON_CYAN    = (0.000, 0.565, 0.722)  # #0090B8 - Holographic Carbon Cyan (printer-crisp)
CARBON_BRIGHT  = (0.000, 0.780, 0.920)  # #00C7EB - Bright Cyan for banner end-caps
ULTRAVIOLET    = (0.431, 0.173, 0.847)  # #6E2CD8 - Deep Ultraviolet Purple accent
TINT_ICE       = (0.965, 0.976, 0.996)  # #F6F9FE - Ultra-light 3% Ice card fill
TINT_LAVENDER  = (0.984, 0.969, 0.996)  # #FBF7FE - Ultra-light 3% Trinity Lavender fill
BORDER_SUBTLE  = (0.800, 0.843, 0.918)  # #CCD7EA - Crisp structural hairline
WHITE          = (1.000, 1.000, 1.000)

# Clean Corporate Navy/Slate Palette for 1-Column ATS Fast-Hire Edition
ATS_INK        = (0.067, 0.094, 0.153)  # #111827 - Crisp Slate-Black
ATS_BODY       = (0.145, 0.188, 0.255)  # #253041 - Clean Dark Slate
ATS_MUTED      = (0.333, 0.388, 0.463)  # #556376 - Muted Metadata
ATS_NAVY       = (0.071, 0.208, 0.267)  # #123544 - D-Suite Petrol Navy
ATS_RULE       = (0.780, 0.824, 0.875)  # #C7D2DF - Clean Section Divider


def draw_top_and_bottom_bars(page, page_num):
    margin = 36.0
    w = 612.0 - 2 * margin  # 540 pt
    page.rect_fill(margin, 758, w * 0.58, 3.0, TRINITY_MAG)
    page.rect_fill(margin + w * 0.58, 758, w * 0.17, 3.0, ULTRAVIOLET)
    page.rect_fill(margin + w * 0.75, 758, w * 0.25, 3.0, CARBON_CYAN)

    node_str = f"SYSTEM_NODE: 0{page_num} // MATTHEW_COLE_WYATT"
    ver_str = "AGENT_TRINITY_GEMINI_4_CARBON_v4.2 // NOV 2026"
    page.text(margin + 4, 34, node_str, font_key="F4", size=7.2, rgb=OBSIDIAN_MUTED)
    page.text_right(612 - margin - 4, 34, ver_str, font_key="F4", size=7.2, rgb=CARBON_CYAN)
    page.rect_fill(margin, 24, w * 0.25, 2.2, CARBON_CYAN)
    page.rect_fill(margin + w * 0.25, 24, w * 0.17, 2.2, ULTRAVIOLET)
    page.rect_fill(margin + w * 0.42, 24, w * 0.58, 2.2, TRINITY_MAG)


def draw_section_banner(page, y_top, title):
    margin = 36.0
    w = 540.0
    h = 19.5
    y_bot = y_top - h
    page.rect_fill(margin, y_bot, w, h, OBSIDIAN)
    page.rect_fill(margin, y_bot, 6.0, h, TRINITY_MAG)
    page.rect_fill(margin + w - 6.0, y_bot, 6.0, h, CARBON_BRIGHT)
    page.text(margin + 14.0, y_bot + 5.8, title, font_key="F1", size=9.5, rgb=WHITE)
    return y_bot


def build_resume_pdf(email_address, location_label, title_subtitle, role1_subtitle, output_path):
    p1 = VectorPDFPage()
    p2 = VectorPDFPage()
    margin = 36.0
    full_w = 540.0

    # ==========================================================================
    # PAGE 1: HEADER, PROFILE, CORE COMPETENCY MATRIX & FEATURED PROJECTS
    # ==========================================================================
    draw_top_and_bottom_bars(p1, 1)

    p1.text_center(306.0, 726.0, "MATTHEW COLE WYATT", font_key="F1", size=22.5, rgb=OBSIDIAN)
    p1.text_center(306.0, 710.0, title_subtitle, font_key="F4", size=8.8, rgb=CARBON_CYAN)

    p1.text_center(
        306.0,
        697.5,
        "[ AGENT TRINITY // GEMINI 4 CARBON ]   *   [ GOOGLE LABS FEATURED TECHNOLOGIST ]   *   [ 100% DATA SOVEREIGNTY ]",
        font_key="F4",
        size=7.1,
        rgb=TRINITY_MAG,
    )

    contact_y = 683.0
    contact_segments = [
        ("LOC: ", "F4", OBSIDIAN),
        (location_label, "F3", OBSIDIAN_BODY),
        ("  |  ", "F4", TRINITY_MAG),
        ("PH: ", "F4", OBSIDIAN),
        ("760.310.0706", "F3", OBSIDIAN_BODY),
        ("  |  ", "F4", CARBON_CYAN),
        ("EM: ", "F4", OBSIDIAN),
        (email_address, "F4", ULTRAVIOLET),
        ("  |  ", "F4", TRINITY_MAG),
        ("WEB: ", "F4", OBSIDIAN),
        ("renderwithoutcode.com", "F4", CARBON_CYAN),
    ]
    total_chars = sum(len(t) for t, _, _ in contact_segments)
    char_w_contact = 0.600 * 7.8
    start_x = 306.0 - (total_chars * char_w_contact) / 2.0
    cx = start_x
    for tok, fk, col in contact_segments:
        p1.text(cx, contact_y, tok, font_key=fk, size=7.8, rgb=col)
        if tok == email_address:
            p1.add_link(cx, contact_y - 2, len(tok) * char_w_contact, 10, f"mailto:{email_address}")
        elif tok == "renderwithoutcode.com":
            p1.add_link(cx, contact_y - 2, len(tok) * char_w_contact, 10, "https://renderwithoutcode.com/resume.html")
        cx += len(tok) * char_w_contact

    p1.line(margin, 675.0, margin + full_w, 675.0, BORDER_SUBTLE, 0.8)

    # 2. Section 1: PROFESSIONAL PROFILE & CORE ETHOS
    y = draw_section_banner(p1, 667.0, "PROFESSIONAL PROFILE & CORE ETHOS")
    profile_lines = wrap_courier_segments(
        [
            ("Over 15 years of mission-critical technical operations, secure logistics, and systems infrastructure paired with autonomous ", "F3", OBSIDIAN_BODY),
            ("multi-agent AI orchestration", "F4", OBSIDIAN),
            (", enterprise ", "F3", OBSIDIAN_BODY),
            ("REST API automation", "F4", OBSIDIAN),
            (", and real-time 3D/generative media synthesis. A ", "F3", OBSIDIAN_BODY),
            ("Google Labs Featured", "F4", TRINITY_MAG),
            (" technologist who architects cloud-decoupled, local-first pipelines and high-converting luxury commerce engines with ", "F3", OBSIDIAN_BODY),
            ("100% client data sovereignty", "F4", CARBON_CYAN),
            (", eliminating operational bottlenecks while preserving authentic human brand voice.", "F3", OBSIDIAN_BODY),
        ],
        full_w - 4,
        8.5,
    )
    y = p1.draw_styled_lines(margin + 2, y - 13.0, profile_lines, size=8.5, leading=11.6)

    # Active Stack Strip Box
    stack_box_y = y - 17.0
    p1.rect_fill_stroke(margin, stack_box_y, full_w, 16.5, TINT_ICE, BORDER_SUBTLE, 0.7)
    p1.rect_fill(margin, stack_box_y, 3.5, 16.5, ULTRAVIOLET)
    p1.text(margin + 8, stack_box_y + 5.0, "ACTIVE STACK:", font_key="F4", size=7.0, rgb=ULTRAVIOLET)
    p1.text(
        margin + 67,
        stack_box_y + 5.0,
        "Antigravity IDE + Cloud // Gemini 4 Carbon // NotebookLM RAG // WooCommerce REST v3 // Omnisend // Python CV",
        font_key="F3",
        size=6.7,
        rgb=OBSIDIAN,
    )

    # 3. Section 2: CORE ARCHITECTURAL PILLARS (2 Side-by-Side HUD Boxes)
    y = draw_section_banner(p1, stack_box_y - 9.5, "CORE ARCHITECTURAL PILLARS (CLOUD-DECOUPLED & AGENTIC SYSTEMS)")
    box_top = y - 7.5
    box_h = 162.0
    box_bot = box_top - box_h
    col_w = 264.0
    left_x = margin
    right_x = margin + full_w - col_w

    p1.rect_fill_stroke(left_x, box_bot, col_w, box_h, TINT_ICE, CARBON_CYAN, 0.85)
    p1.hud_corner_ticks(left_x, box_bot, col_w, box_h, CARBON_CYAN, TRINITY_MAG, tick_len=7.0, line_w=1.8)
    p1.text(left_x + 9, box_top - 14.0, "[01] AGENTIC COMMERCE & INFRASTRUCTURE", font_key="F1", size=8.3, rgb=OBSIDIAN)
    p1.line(left_x + 9, box_top - 18.5, left_x + col_w - 9, box_top - 18.5, CARBON_CYAN, 0.6)

    left_bullets = [
        ("• Dual-Layer AI Concierge: ", "F4", OBSIDIAN, "Air-gapped public NotebookLM front desks paired with private operational intelligence vaults (DEE).", "F3", OBSIDIAN_BODY),
        ("• Full-Stack Catalog & CRM: ", "F4", OBSIDIAN, "Headless WooCommerce REST v3, Yoast SEO/AEO schema, 2,900+ record ETL & 99.5% True Delivered CRM.", "F3", OBSIDIAN_BODY),
        ("• Cloud & Local Compute: ", "F4", OBSIDIAN, "Xeon Linux Cloud Agents + local Ryzen 6800U APU pipelines, WireGuard VPN & strict PII quarantine.", "F3", OBSIDIAN_BODY),
        ("• Forensic Chain-of-Custody: ", "F4", OBSIDIAN, "Electromechanical diagnostics, federal vault balancing & clinical-legal audit systems.", "F3", OBSIDIAN_BODY),
    ]
    ly = box_top - 29.5
    for b_head, fk1, c1, b_body, fk2, c2 in left_bullets:
        b_lines = wrap_courier_segments([(b_head, fk1, c1), (b_body, fk2, c2)], col_w - 18, 7.75)
        ly = p1.draw_styled_lines(left_x + 9, ly, b_lines, size=7.75, leading=10.0)
        ly -= 2.4

    p1.rect_fill_stroke(right_x, box_bot, col_w, box_h, TINT_LAVENDER, TRINITY_MAG, 0.85)
    p1.hud_corner_ticks(right_x, box_bot, col_w, box_h, TRINITY_MAG, CARBON_CYAN, tick_len=7.0, line_w=1.8)
    p1.text(right_x + 9, box_top - 14.0, "[02] GENERATIVE AI & VISUAL SYNTHESIS", font_key="F1", size=8.3, rgb=OBSIDIAN)
    p1.line(right_x + 9, box_top - 18.5, right_x + col_w - 9, box_top - 18.5, TRINITY_MAG, 0.6)

    right_bullets = [
        ("• CV Grading & Provenance: ", "F4", OBSIDIAN, "Python planar homography rectification, storefront glass frosting, studio compositing & C2PA signing.", "F3", OBSIDIAN_BODY),
        ("• Context Engineering: ", "F4", OBSIDIAN, "Custom multi-agent memory layouts, living multimodal voice-corpus skills & quadratic token-tax elimination.", "F3", OBSIDIAN_BODY),
        ("• Cinematic 3D Pipelines: ", "F4", OBSIDIAN, "Real-time 3D (Unreal Engine 5 / Blender), physical optical lens simulation & custom OCIO color LUTs.", "F3", OBSIDIAN_BODY),
        ("• Audio & Video Synthesis: ", "F4", OBSIDIAN, "Parallel ffmpeg speech chunking, multi-agent transcription & Google Lyria 3 / Flow production.", "F3", OBSIDIAN_BODY),
    ]
    ry = box_top - 29.5
    for b_head, fk1, c1, b_body, fk2, c2 in right_bullets:
        b_lines = wrap_courier_segments([(b_head, fk1, c1), (b_body, fk2, c2)], col_w - 18, 7.75)
        ry = p1.draw_styled_lines(right_x + 9, ry, b_lines, size=7.75, leading=10.0)
        ry -= 2.4

    # 4. Section 3: FEATURED PROJECTS & LIVE PRODUCTION DEPLOYMENTS
    y = draw_section_banner(p1, box_bot - 11.0, "FEATURED PROJECTS & LIVE PRODUCTION DEPLOYMENTS")
    py = y - 13.5

    projects = [
        (
            "Full-Stack Luxury Retail & Omnichannel CRM Engine // Enterprise Architecture",
            "[ENTERPRISE COMMERCE // NOV 2026]",
            TRINITY_MAG,
            "https://renderwithoutcode.com/front-desk.html",
            [
                ("Architected the end-to-end digital commerce transformation for a Southern California European antiques and fine art gallery. Scrubbed ", "F3", OBSIDIAN_BODY),
                ("2,900+ customer records", "F4", OBSIDIAN),
                (" into ", "F3", OBSIDIAN_BODY),
                ("1,783 collector profiles & 625+ E.164 SMS/MMS contacts", "F4", OBSIDIAN),
                ("; scaled a 90+ asset WooCommerce catalog via headless Python/REST automation with planar homography CV, C2PA provenance, and 100% green Yoast SEO/AEO schema; and resolved Meta Shop checkout routing via a PHP cart handler and TSV feed override. Custom HTML circulars and Meta ads achieved a ", "F3", OBSIDIAN_BODY),
                ("99.5% True Delivered rate", "F4", TRINITY_MAG),
                (", ", "F3", OBSIDIAN_BODY),
                ("48.9% open rate", "F4", CARBON_CYAN),
                (", ", "F3", OBSIDIAN_BODY),
                ("$0.12 Meta CPC (270 clicks)", "F4", ULTRAVIOLET),
                (", and ", "F3", OBSIDIAN_BODY),
                ("$7,000 in live customer carts", "F4", OBSIDIAN),
                (" within hours of Sunday broadcast dispatch.", "F3", OBSIDIAN_BODY),
            ],
        ),
        (
            "RETRO-TERM 80 // Selected by Google Labs Community Gallery",
            "[OFFICIAL GOOGLE FEATURE // JULY 2026]",
            CARBON_CYAN,
            "https://labs.google/fx/tools/flow/shared/tool/c718f343-2e2f-4ae8-92bd-6f68f13b1c45",
            [
                ("Designed and compiled a browser-native image and video terminal processor executing brutalist visual styles, phosphor matrix rendering, and magnetic tape distortion effects directly on client-side GPUs via custom CSS/JS. Completed the full build and deployment loop through natural-language orchestration matrices (", "F3", OBSIDIAN_BODY),
                ("labs.google", "F4", CARBON_CYAN),
                (").", "F3", OBSIDIAN_BODY),
            ],
        ),
        (
            "Generative Cinematics & Research Compendium // NeverRender Labs Pipeline",
            "[BBC / NATGEO VALIDATED]",
            ULTRAVIOLET,
            "https://renderwithoutcode.com/notebook-research.html",
            [
                ("Developed an offline, cloud-decoupled synthetic media rendering factory and published a 5-Part Master Research Compendium plus 6 Open-Source NotebookLM vaults covering Agentic Content Workflows, Physics-Informed World Models, and Virtual Production. Architected physical camera optics, sensor noise, and anamorphic lens simulation within AI video engines, earning organic validation from award-winning BBC/PBS National Geographic Wildlife Cinematographer ", "F3", OBSIDIAN_BODY),
                ("Vianet Djenguet", "F4", OBSIDIAN),
                (".", "F3", OBSIDIAN_BODY),
            ],
        ),
    ]

    for p_title, p_badge, badge_col, p_url, p_segs in projects:
        p1.rect_fill(margin, py - 1.5, 3.0, 9.5, badge_col)
        p1.text(margin + 7.0, py, p_title, font_key="F4", size=8.4, rgb=OBSIDIAN)
        p1.text_right(margin + full_w, py, p_badge, font_key="F4", size=7.1, rgb=badge_col)
        p1.add_link(margin, py - 2, full_w, 11, p_url)
        py -= 11.2
        p_lines = wrap_courier_segments(p_segs, full_w - 8, 8.0)
        py = p1.draw_styled_lines(margin + 7.0, py, p_lines, size=8.0, leading=10.35)
        py -= 7.0

    # ==========================================================================
    # PAGE 2: PROFESSIONAL EXPERIENCE & TECHNICAL VERIFICATION MATRIX
    # ==========================================================================
    draw_top_and_bottom_bars(p2, 2)

    y2 = draw_section_banner(p2, 742.0, "PROFESSIONAL EXPERIENCE & INFRASTRUCTURE CHRONOLOGY")
    ey = y2 - 16.0

    roles = [
        (
            "PRINCIPAL AI SYSTEMS ARCHITECT & TECHNICAL DIRECTOR",
            " // NEVERRENDER LABS",
            role1_subtitle,
            TRINITY_MAG,
            [
                "Lead full-stack digital infrastructure, WooCommerce/WordPress REST API v3 automation, Meta Commerce ad and catalog synchronization ($0.12 CPC), and Omnisend CRM architecture (2,900+ scrubbed records, $7,000 live broadcast carts).",
                "Engineered custom Python computer-vision pipelines for planar homography perspective rectification, storefront glass frosting, C2PA provenance signing, and studio backdrop compositing across 90+ fine art and antique assets.",
                "Built dual-layer NotebookLM + Gemini 4 Carbon autonomous reception vaults (DEE) and Xeon Linux cloud-agent workflows alongside living multimodal voice-corpus skills with strict AI-tell sanitization.",
            ],
        ),
        (
            "INDEPENDENT AI EVALUATION & DIGITAL MEDIA CONTRACTOR",
            " // REMOTE",
            "Frontier Multimodal Evaluation Contractor | June 2024 - Present",
            CARBON_CYAN,
            [
                "Stress-test and evaluate frontier language and vision models across technical reasoning, agentic browser control, prompt compliance, and token-efficiency benchmarks.",
                "Maintain dedicated secure workstation utilizing custom WireGuard VPN tunnels and local AMD Ryzen 6800U APU multi-threaded rendering pipelines.",
                "Execute automated multi-track audio/video asset management pipelines, parallel ffmpeg speech chunking, and custom generative media synthesis.",
            ],
        ),
        (
            "CARE LOGISTICS & COMPLIANCE SYSTEMS COORDINATOR",
            " // OCEANSIDE, CA",
            "Family Caregiver & Authorized Representative | 2011 - 2024",
            ULTRAVIOLET,
            [
                "Managed long-term household logistics, fiduciary accounting, and multi-agency benefit coordination across county CalSAWS and state MEDS systems.",
                "Built high-fidelity background logging systems integrating audio-to-text transcription to audit plan-level care compliance, compiling unassailable 113-page clinical-legal evidence payloads for state regulatory dockets.",
                "Coordinated high-acuity crisis de-escalation, medical schedules, and physical therapy adaptive overrides under demanding environmental constraints.",
            ],
        ),
        (
            "RETAIL OPERATIONS, COURIER & LOGISTICS SPECIALIST",
            " // TARGET, UBER, SCHNUCKS",
            "Midwest Division | May 2021 - June 2024",
            CARBON_CYAN,
            [
                "Maintained top-tier service ratings and transaction velocity through structured inventory auditing, register balancing, and route optimization.",
                "Resolved customer escalations calmly in high-volume retail environments and executed secure transit for time-sensitive deliveries.",
            ],
        ),
        (
            "FIELD SERVICE SPECIALIST II",
            " // DISH NETWORK",
            "San Diego, CA & Saint Charles, MO | May 2007 - February 2009",
            TRINITY_MAG,
            [
                "Managed autonomous daily field routes, completing electrical installations and line-of-sight RF diagnostics in strict compliance with NEC standards.",
                "Solved complex RF signaling and hardware failures on-site, educating clients on system operation to maintain high trust and eliminate repeat dispatches.",
            ],
        ),
        (
            "ATM LEAD & SECURE LOGISTICS",
            " // LOOMIS, FARGO & CO.",
            "San Diego, CA & Ballwin, MO | September 2003 - February 2007",
            ULTRAVIOLET,
            [
                "Commanded high-value Federal Reserve cash transit and vault balancing protocols under strict federal chain-of-custody regulations.",
                "Performed on-site electromechanical diagnostics, troubleshooting, and modular hardware repairs on commercial ATM terminals.",
                "Trained incoming personnel on balancing math, dual-custody lock protocols, and audit verification standards.",
            ],
        ),
    ]

    for r_title, r_org, r_sub, r_col, r_bullets in roles:
        p2.rect_fill(margin, ey - 1.0, 3.2, 9.5, r_col)
        char_w_title = 0.600 * 9.0
        p2.text(margin + 7.5, ey, r_title, font_key="F4", size=9.0, rgb=OBSIDIAN)
        p2.text(margin + 7.5 + len(r_title) * char_w_title, ey, r_org, font_key="F4", size=9.0, rgb=r_col)
        ey -= 10.8
        p2.text(margin + 7.5, ey, r_sub, font_key="F3", size=7.8, rgb=OBSIDIAN_MUTED)
        ey -= 11.2
        for bul in r_bullets:
            b_lines = wrap_courier_segments([("• " + bul, "F3", OBSIDIAN_BODY)], full_w - 12, 8.0)
            ey = p2.draw_styled_lines(margin + 7.5, ey, b_lines, size=8.0, leading=10.05)
            ey -= 1.8
        ey -= 6.0

    # Bottom Verification & Architecture Box on Page 2
    vbox_top = ey - 2.0
    vbox_h = 79.0
    vbox_bot = vbox_top - vbox_h
    p2.rect_fill_stroke(margin, vbox_bot, full_w, vbox_h, TINT_ICE, BORDER_SUBTLE, 0.85)
    p2.hud_corner_ticks(margin, vbox_bot, full_w, vbox_h, CARBON_CYAN, TRINITY_MAG, tick_len=7.0, line_w=1.8)
    p2.text(margin + 10, vbox_top - 13.5, "VERIFICATION ENDPOINTS & PRODUCTION ARCHITECTURE", font_key="F1", size=8.3, rgb=OBSIDIAN)
    p2.line(margin + 10, vbox_top - 18.0, margin + full_w - 10, vbox_top - 18.0, BORDER_SUBTLE, 0.6)

    v_rows = [
        ("• Interactive Resume:  ", "F4", OBSIDIAN, "renderwithoutcode.com/resume.html", "F4", CARBON_CYAN, "  |  AI Front Desk: renderwithoutcode.com/front-desk.html", "F3", OBSIDIAN_BODY),
        ("• Commerce Telemetry:  ", "F4", OBSIDIAN, "WooCommerce REST v3 + Omnisend CRM", "F4", TRINITY_MAG, "  |  2,900+ Records // 99.5% True Delivered // $0.12 CPC", "F3", OBSIDIAN_BODY),
        ("• Google Labs Feature: ", "F4", OBSIDIAN, "labs.google/fx/tools/flow (RETRO-TERM 80)", "F4", ULTRAVIOLET, "  |  Vaults: renderwithoutcode.com/notebook-research.html", "F3", OBSIDIAN_BODY),
        ("• Security & Compute:  ", "F4", OBSIDIAN, "Xeon Cloud + Ryzen 6800U // WireGuard VPN", "F4", OBSIDIAN_BODY, "  |  Zero-PII Air-Gapped Dual-Layer NotebookLM RAG", "F3", OBSIDIAN_BODY),
    ]
    vy = vbox_top - 29.0
    for r1, fk1, c1, r2, fk2, c2, r3, fk3, c3 in v_rows:
        line_segs = [((r1, fk1, c1)), ((r2, fk2, c2)), ((r3, fk3, c3))]
        p2.draw_styled_lines(margin + 10, vy, [line_segs], size=6.65, leading=10.6)
        vy -= 11.6

    write_pdf([p1, p2], output_path, pdf_title="Matthew Cole Wyatt - Agent Trinity Resume v4.2 (Nov 2026)")
    print("Generated HUD PDF:", output_path)


def build_ats_clean_resume_pdf(output_path):
    """
    100% Single-Column ATS-Compliant & Toner-Saver Fast-Hire Edition
    (Engineered for Workday, Greenhouse, iCIMS, Indeed, LinkedIn Easy Apply & Staffing Portals).
    Zero multi-column tables, zero HUD graphics that scramble linear OCR/ATS parsers.
    """
    p1 = VectorPDFPage()
    p2 = VectorPDFPage()
    margin = 44.0
    full_w = 612.0 - 2 * margin  # 524 pt

    def ats_section_header(page, y_top, label):
        page.text(margin, y_top, label, font_key="F1", size=10.2, rgb=ATS_NAVY)
        page.line(margin, y_top - 4.0, margin + full_w, y_top - 4.0, ATS_NAVY, 1.0)
        return y_top - 16.5

    # ================= PAGE 1 =================
    p1.text(margin, 744.0, "MATTHEW COLE WYATT", font_key="F1", size=20.0, rgb=ATS_INK)
    p1.text(
        margin,
        727.5,
        "E-Commerce Operations Specialist | Technical Systems & Catalog Coordinator | AI Workflow & QA Lead",
        font_key="F1",
        size=9.5,
        rgb=ATS_NAVY,
    )
    c_prefix = "Oceanside, CA 92056 (North County / San Diego & Remote)  |  760-310-0706  |  "
    c_email = "jobs.net757@passinbox.com"
    c_sep = "  |  "
    c_web = "renderwithoutcode.com"
    contact_line = c_prefix + c_email + c_sep + c_web
    c_size = 8.2
    p1.text(margin, 713.5, contact_line, font_key="F2", size=c_size, rgb=ATS_MUTED)
    em_x = margin + font_key_width(c_prefix, "F2", c_size)
    em_w = font_key_width(c_email, "F2", c_size)
    wb_x = em_x + em_w + font_key_width(c_sep, "F2", c_size)
    wb_w = font_key_width(c_web, "F2", c_size)
    p1.add_link(em_x, 711, em_w, 10, "mailto:jobs.net757@passinbox.com")
    p1.add_link(wb_x, 711, wb_w, 10, "https://renderwithoutcode.com/resume.html")
    p1.line(margin, 705.5, margin + full_w, 705.5, ATS_RULE, 0.8)

    # Summary
    y = ats_section_header(p1, 690.0, "PROFESSIONAL SUMMARY")
    sum_lines = wrap_proportional_segments(
        [(
            "Operations-hardened E-Commerce, Digital Catalog, and Technical Systems Specialist with 15+ years of experience across secure logistics, field hardware diagnostics, retail inventory operations, and full-stack digital storefront management. Proven track record scrubbing multi-thousand-record CRM databases, scaling 90+ SKU WooCommerce and Meta Shop catalogs via Python/REST automation, managing high-deliverability Omnisend email/SMS campaigns (99.5% True Delivered, $0.12 Meta CPC), and resolving complex technical escalations cleanly under pressure.",
            "F2",
            ATS_BODY,
        )],
        full_w,
        9.2,
    )
    y = p1.draw_styled_lines(margin, y, sum_lines, size=9.2, leading=12.8)

    # Core Skills (1-Column Keyword-Dense ATS Rows)
    y = ats_section_header(p1, y - 8.0, "CORE TECHNICAL & OPERATIONAL SKILLS")
    skill_rows = [
        ("E-Commerce & Merchandising: ", "WooCommerce, WordPress Admin & REST API v3, Meta Business Suite & Commerce Catalog, Yoast SEO, JSON-LD Schema, TSV Product Feeds, Cart & Checkout QA"),
        ("CRM, Email & Paid Growth: ", "Omnisend Email/SMS/MMS, E.164 Carrier Normalization, CSV/Excel/XLSX ETL Deduplication (2,900+ Records), Deliverability & Dark-Mode HTML QA, Meta Ads ($0.12 CPC)"),
        ("AI, Scripting & Media Ops: ", "Python Automation, Linux CLI, Git, Prompt Engineering & Multimodal Model QA, NotebookLM RAG, Adobe Photoshop, FFmpeg, Image Perspective & Color Grading"),
        ("Field Tech, Logistics & Compliance: ", "Hardware & Electromechanical Diagnostics, RF Signal Troubleshooting (NEC Compliant), Federal Vault & Cash-in-Transit Auditing, CalSAWS/MEDS Regulatory Documentation"),
    ]
    for sk_head, sk_body in skill_rows:
        sk_lines = wrap_proportional_segments(
            [(sk_head, "F1", ATS_INK), (sk_body, "F2", ATS_BODY)],
            full_w,
            8.9,
        )
        y = p1.draw_styled_lines(margin, y, sk_lines, size=8.9, leading=12.0)
        y -= 3.0

    # Professional Experience (Top Half on Page 1)
    y = ats_section_header(p1, y - 6.0, "PROFESSIONAL EXPERIENCE")

    p1_roles = [
        (
            "E-Commerce Systems & Digital Operations Consultant",
            "NeverRender Labs  |  Oceanside & San Diego, CA",
            "2025 - Present",
            [
                "Managed end-to-end digital storefront operations, catalog publishing, CRM hygiene, and paid social merchandising for a Southern California luxury fine art and antiques retailer.",
                "Cleaned, normalized, and deduplicated 2,900+ fragmented customer records across iPhone exports, showroom ledgers, and e-commerce logs into 1,783 active CRM profiles and 625+ carrier-verified E.164 SMS/MMS subscribers.",
                "Published and audited 90+ high-ticket WooCommerce product listings via Python REST API v3 scripts with standardized studio photography, C2PA metadata, and 100% double-green Yoast SEO scores.",
                "Resolved Meta Commerce Shop checkout and shipping bottlenecks by deploying a server-side PHP cart router and custom TSV feed override.",
                "Built and dispatched responsive HTML email circulars, MMS campaigns, and targeted Meta ads achieving a 99.5% True Delivered rate, 48.9% open rate, $0.12 Cost-Per-Click (270 link clicks), and $7,000 in live customer carts within hours of Sunday launch.",
            ],
        ),
        (
            "AI Quality Assurance & Multimodal Evaluation Specialist (Contract)",
            "Independent Remote Contractor  |  Oceanside, CA",
            "June 2024 - Present",
            [
                "Evaluate and stress-test enterprise language, vision, and browser-automation models for factual accuracy, instruction compliance, structured output quality, and safety edge cases.",
                "Operate a secure local Linux/Windows testing environment with encrypted WireGuard VPN routing, Python data validation scripts, and automated FFmpeg audio/video processing pipelines.",
                "Selected for the official Google Labs Community Gallery (July 2026) for designing and shipping RETRO-TERM 80, a browser-native GPU visual processor.",
            ],
        ),
    ]

    for r_title, r_comp, r_dates, r_buls in p1_roles:
        p1.text(margin, y, r_title, font_key="F1", size=9.8, rgb=ATS_INK)
        p1.text_right(margin + full_w, y, r_dates, font_key="F1", size=9.0, rgb=ATS_NAVY)
        y -= 12.0
        p1.text(margin, y, r_comp, font_key="F2", size=8.9, rgb=ATS_MUTED)
        y -= 12.5
        for b in r_buls:
            blines = wrap_proportional_segments([("•  " + b, "F2", ATS_BODY)], full_w - 6, 8.9)
            y = p1.draw_styled_lines(margin + 4, y, blines, size=8.9, leading=11.9)
            y -= 2.5
        y -= 6.5

    p1.text_right(margin + full_w, 28.0, "Matthew Cole Wyatt  |  Page 1 of 2", font_key="F2", size=8.0, rgb=ATS_MUTED)

    # ================= PAGE 2 =================
    y2 = ats_section_header(p2, 744.0, "PROFESSIONAL EXPERIENCE (CONTINUED)")

    p2_roles = [
        (
            "Care Logistics, Fiduciary & Compliance Coordinator",
            "Authorized Family Representative  |  Oceanside, CA",
            "2011 - 2024",
            [
                "Directed full-time household operations, fiduciary accounting, medical scheduling, and multi-agency benefit compliance across county CalSAWS and state MEDS databases.",
                "Designed structured digital audit logs and transcription workflows to track care-plan compliance, assembling comprehensive 113-page evidentiary filings for state regulatory review.",
                "Managed high-pressure crisis de-escalation, vendor scheduling, and adaptive equipment coordination with zero compliance lapses.",
            ],
        ),
        (
            "Retail Operations, Inventory & Fulfillment Associate",
            "Target, Schnucks & Uber  |  Midwest Division",
            "May 2021 - June 2024",
            [
                "Maintained top-tier accuracy and customer satisfaction ratings across high-volume point-of-sale operations, register balancing, inventory cycle counts, and last-mile delivery routing.",
                "Resolved customer service escalations calmly on the floor while meeting strict fulfillment and time-sensitive transit windows.",
            ],
        ),
        (
            "Field Service Technician II",
            "DISH Network  |  San Diego, CA & Saint Charles, MO",
            "May 2007 - February 2009",
            [
                "Managed autonomous daily service routes performing residential and commercial electrical installations, coaxial cabling, and line-of-sight RF signal diagnostics in full NEC compliance.",
                "Diagnosed and repaired complex receiver, switch, and signal-path hardware issues on-site, training customers on system operation to eliminate repeat service calls.",
            ],
        ),
        (
            "ATM Lead Technician & Secure Cash Logistics Custodian",
            "Loomis, Fargo & Co.  |  San Diego, CA & Ballwin, MO",
            "September 2003 - February 2007",
            [
                "Led high-value Federal Reserve cash-in-transit routes and commercial vault-balancing operations under strict federal chain-of-custody and dual-custody security protocols.",
                "Performed on-site electromechanical diagnostics, bill-dispenser/reader repairs, and preventative maintenance on commercial banking ATM terminals.",
                "Trained incoming route personnel on settlement accounting, dual-custody lock procedures, and audit reconciliation standards.",
            ],
        ),
    ]

    for r_title, r_comp, r_dates, r_buls in p2_roles:
        p2.text(margin, y2, r_title, font_key="F1", size=9.8, rgb=ATS_INK)
        p2.text_right(margin + full_w, y2, r_dates, font_key="F1", size=9.0, rgb=ATS_NAVY)
        y2 -= 12.0
        p2.text(margin, y2, r_comp, font_key="F2", size=8.9, rgb=ATS_MUTED)
        y2 -= 12.5
        for b in r_buls:
            blines = wrap_proportional_segments([("•  " + b, "F2", ATS_BODY)], full_w - 6, 8.9)
            y2 = p2.draw_styled_lines(margin + 4, y2, blines, size=8.9, leading=11.9)
            y2 -= 2.5
        y2 -= 7.5

    # Selected Recognition & Portfolio Verification
    y2 = ats_section_header(p2, y2 - 4.0, "SELECTED TECHNICAL RECOGNITION & PORTFOLIO")
    rec_bullets = [
        ("Google Labs Official Feature (July 2026): ", "Selected for the Google Labs Community Gallery for RETRO-TERM 80 (labs.google/fx/tools/flow), a browser-based GPU media processor."),
        ("Industry Cinematography Validation: ", "Published a 5-part open-source research compendium on physical camera optics and generative media workflows, earning organic recognition from BBC/PBS National Geographic cinematographer Vianet Djenguet."),
        ("Live Portfolio & Technical Work Samples: ", "renderwithoutcode.com  |  Interactive Resume: renderwithoutcode.com/resume.html"),
    ]
    for rh, rb in rec_bullets:
        rlines = wrap_proportional_segments(
            [("•  " + rh, "F1", ATS_INK), (rb, "F2", ATS_BODY)],
            full_w - 6,
            8.9,
        )
        y2 = p2.draw_styled_lines(margin + 4, y2, rlines, size=8.9, leading=11.9)
        y2 -= 3.0

    p2.text_right(margin + full_w, 28.0, "Matthew Cole Wyatt  |  Page 2 of 2", font_key="F2", size=8.0, rgb=ATS_MUTED)

    write_pdf([p1, p2], output_path, pdf_title="Matthew Cole Wyatt - Operations, E-Commerce & Technical Specialist Resume (Nov 2026)")
    print("Generated ATS PDF:", output_path)


if __name__ == "__main__":
    # 1. Studio / B2B Client Edition (creator@renderwithoutcode.com)
    studio_paths = [
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\Matthew_Cole_Wyatt_NeverRender_Labs_Resume.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\Matthew_Cole_Wyatt_NeverRender_Labs_Resume_Nov_2026.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\.antigravity\8-BIT_RESUME\MCW_NeverRender_Labs_Resume_Light.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_NeverRender_Labs_Resume.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_NeverRender_Labs_Resume_Nov_2026.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\matthew-wyatt-sre-creative-resume-studio-trinity.pdf",
    ]
    for sp in studio_paths:
        build_resume_pdf(
            email_address="creator@renderwithoutcode.com",
            location_label="Oceanside & San Diego, CA",
            title_subtitle="AGENTIC SYSTEMS ARCHITECT, FULL-STACK E-COMMERCE DIRECTOR & LEAD OF VISUAL SYNTHESIS",
            role1_subtitle="Founder & Principal Systems Architect (Oceanside & San Diego, CA) | 2025 - Present",
            output_path=sp,
        )

    # 2. Universal HUD Job-Search Edition (jobs.net757@passinbox.com)
    universal_paths = [
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\Matthew_Cole_Wyatt_Universal_Resume.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\Matthew_Cole_Wyatt_Universal_Resume_Nov_2026.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_Universal_Resume.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_Universal_Resume_Nov_2026.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\matthew-wyatt-sre-creative-resume-universal-trinity.pdf",
    ]
    for up in universal_paths:
        build_resume_pdf(
            email_address="jobs.net757@passinbox.com",
            location_label="Oceanside, CA 92056",
            title_subtitle="SYSTEMS ARCHITECT, E-COMMERCE AUTOMATION LEAD & TECHNICAL OPERATIONS SPECIALIST",
            role1_subtitle="Principal E-Commerce & AI Systems Architect (Oceanside, CA) | 2025 - Present",
            output_path=up,
        )

    # 3. Clean 1-Column ATS Fast-Hire & Toner-Saver Edition (jobs.net757@passinbox.com)
    ats_paths = [
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\Matthew_Cole_Wyatt_ATS_FastHire_Resume_Nov_2026.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_ATS_FastHire_Resume_Nov_2026.pdf",
        r"C:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\matthew-wyatt-sre-creative-resume-toner-saver.pdf",
    ]
    for ap in ats_paths:
        build_ats_clean_resume_pdf(output_path=ap)
