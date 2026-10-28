import os
import re
import math
import zlib

# ==============================================================================
# 1. PARSE ROUNDED-DOT QR CODE GEOMETRY FROM adobe-express-qr-code.svg
# ==============================================================================
SVG_PATH = r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\adobe-express-qr-code.svg"

def parse_qr_svg(svg_path):
    svg = open(svg_path, "r", encoding="utf-8").read()
    # Extract clip-path-dot-color inner elements
    m_clip = re.search(r'<clipPath id="clip-path-dot-color">(.*?)</clipPath>', svg, re.S)
    dot_body = m_clip.group(1) if m_clip else ""
    
    elements = []
    # 1. Rectangles: <rect x="18" y="178" width="16" height="16" transform="rotate(0,26,186)"/>
    for m in re.finditer(r'<rect x="(\d+)" y="(\d+)" width="16" height="16" transform="rotate\(([-0-9]+),(\d+),(\d+)\)"\s*/>', dot_body):
        x, y = int(m.group(1)), int(m.group(2))
        elements.append(("rect", x, y, 16, 16, 0))
        
    # 2. Circles: <circle cx="122" cy="154" r="8" transform="rotate(0,122,154)"/>
    for m in re.finditer(r'<circle cx="(\d+)" cy="(\d+)" r="8" transform="rotate\(([-0-9]+),(\d+),(\d+)\)"\s*/>', dot_body):
        cx, cy = int(m.group(1)), int(m.group(2))
        elements.append(("circle", cx, cy, 8))
        
    # 3. Endcap D-pills: <path d="M 18 162v 16h 8a 8 8, 0, 0, 0, 0 -16" transform="rotate(-90,26,170)"/>
    for m in re.finditer(r'<path d="M (\d+) (\d+)v 16h 8a 8 8, 0, 0, 0, 0 -16" transform="rotate\(([-0-9]+),(\d+),(\d+)\)"\s*/>', dot_body):
        x, y, ang = int(m.group(1)), int(m.group(2)), int(m.group(3))
        elements.append(("endcap", x, y, ang))
        
    # 4. 1-Corner-Rounded blocks: <path d="M 18 194v 16h 16v -8a 8 8, 0, 0, 0, -8 -8" transform="rotate(180,26,202)"/>
    for m in re.finditer(r'<path d="M (\d+) (\d+)v 16h 16v -8a 8 8, 0, 0, 0, -8 -8" transform="rotate\(([-0-9]+),(\d+),(\d+)\)"\s*/>', dot_body):
        x, y, ang = int(m.group(1)), int(m.group(2)), int(m.group(3))
        elements.append(("corner1", x, y, ang))

    # Finder patterns (top-left, top-right, bottom-left) in 500x500 space:
    # Outer square 112x112 at (18,18), (370,18), (18,370) with 80x80 inner cutout at +16,+16
    # Center dot circle r=24 at (74,74), (426,74), (74,426)
    finders = [
        (18, 18, 74, 74),
        (370, 18, 426, 74),
        (18, 370, 74, 426),
    ]
    return elements, finders, dot_body

QR_ELEMENTS, QR_FINDERS, QR_RAW_DOT_BODY = parse_qr_svg(SVG_PATH)
print(f"Parsed {len(QR_ELEMENTS)} QR vector primitives and {len(QR_FINDERS)} finder patterns.")

# ==============================================================================
# 2. PURE-PYTHON POSTSCRIPT TYPE1 VECTOR PDF ENGINE FOR BUSINESS CARDS
# ==============================================================================
# Standard US Business Card: 3.5" x 2.0" = 252pt x 144pt
PAGE_W = 252.0
PAGE_H = 144.0

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
    'x': 500, 'y': 500, 'z': 500, '{': 334, '|': 260, '}': 334, '~': 584,
}

HELV_BOLD_WIDTHS = {
    ' ': 278, '!': 333, '"': 474, '#': 556, '$': 556, '%': 889, '&': 722, "'": 238,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 333, ';': 333, '<': 584, '=': 584, '>': 584, '?': 611,
    '@': 975, 'A': 722, 'B': 722, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 556, 'K': 722, 'L': 611, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 584, '_': 556,
    '`': 333, 'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556, 'f': 333, 'g': 611,
    'h': 611, 'i': 278, 'j': 278, 'k': 556, 'l': 278, 'm': 889, 'n': 611, 'o': 611,
    'p': 611, 'q': 611, 'r': 389, 's': 556, 't': 333, 'u': 611, 'v': 556, 'w': 778,
    'x': 556, 'y': 556, 'z': 500, '{': 389, '|': 280, '}': 389, '~': 584,
}

def str_width(text, font, size):
    if font in ("F3", "F4"):
        return len(text) * 600.0 * size / 1000.0
    table = HELV_BOLD_WIDTHS if font == "F2" else HELV_WIDTHS
    return sum(table.get(ch, 556) for ch in text) * size / 1000.0

def pdf_escape(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

class PDFCanvas:
    def __init__(self, page_w=PAGE_W, page_h=PAGE_H):
        self.page_w = page_w
        self.page_h = page_h
        self.pages = []
        self.cur = []

    def new_page(self):
        if self.cur:
            self.pages.append("\n".join(self.cur))
        self.cur = []

    def set_fill(self, rgb):
        r, g, b = rgb
        self.cur.append(f"{r:.4f} {g:.4f} {b:.4f} rg")

    def set_stroke(self, rgb):
        r, g, b = rgb
        self.cur.append(f"{r:.4f} {g:.4f} {b:.4f} RG")

    def set_line_width(self, w):
        self.cur.append(f"{w:.3f} w")

    def rect(self, x, y_top, w, h, fill=None, stroke=None, line_w=0.6):
        py = PAGE_H - y_top - h
        if fill and stroke:
            self.set_fill(fill)
            self.set_stroke(stroke)
            self.set_line_width(line_w)
            self.cur.append(f"{x:.3f} {py:.3f} {w:.3f} {h:.3f} re B")
        elif fill:
            self.set_fill(fill)
            self.cur.append(f"{x:.3f} {py:.3f} {w:.3f} {h:.3f} re f")
        elif stroke:
            self.set_stroke(stroke)
            self.set_line_width(line_w)
            self.cur.append(f"{x:.3f} {py:.3f} {w:.3f} {h:.3f} re S")

    def line(self, x1, y1_top, x2, y2_top, stroke, line_w=0.6, dash=None):
        py1 = PAGE_H - y1_top
        py2 = PAGE_H - y2_top
        self.set_stroke(stroke)
        self.set_line_width(line_w)
        if dash:
            self.cur.append(f"[{dash[0]} {dash[1]}] 0 d")
        else:
            self.cur.append("[] 0 d")
        self.cur.append(f"{x1:.3f} {py1:.3f} m {x2:.3f} {py2:.3f} l S")
        if dash:
            self.cur.append("[] 0 d")

    def text(self, x, y_top, s, font="F1", size=8.0, color=(0,0,0)):
        py = PAGE_H - y_top
        self.set_fill(color)
        esc = pdf_escape(s)
        self.cur.append(f"BT /{font} {size:.2f} Tf {x:.3f} {py:.3f} Td ({esc}) Tj ET")

    def polygon_fill(self, pts_top, fill):
        self.set_fill(fill)
        p0x, p0y = pts_top[0][0], PAGE_H - pts_top[0][1]
        cmds = [f"{p0x:.3f} {p0y:.3f} m"]
        for px, py_top in pts_top[1:]:
            cmds.append(f"{px:.3f} {PAGE_H - py_top:.3f} l")
        cmds.append("h f")
        self.cur.append(" ".join(cmds))

    def draw_qr_vector(self, box_x, box_y_top, box_size, dot_color, finder_outer_color, finder_inner_color, bg_color=None):
        """Render the exact 500x500 rounded-dot QR code into (box_x, box_y_top, box_size, box_size)."""
        if bg_color:
            self.rect(box_x, box_y_top, box_size, box_size, fill=bg_color)
        scale = box_size / 500.0

        def tx(qx, qy):
            return (box_x + qx * scale, box_y_top + qy * scale)

        def rot_pt(px, py, cx, cy, ang_deg):
            if ang_deg == 0:
                return (px, py)
            rad = math.radians(ang_deg)
            ca, sa = math.cos(rad), math.sin(rad)
            dx, dy = px - cx, py - cy
            return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)

        def arc_pts(cx, cy, r, a0_deg, a1_deg, steps=8):
            pts = []
            for i in range(steps + 1):
                a = math.radians(a0_deg + (a1_deg - a0_deg) * i / steps)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            return pts

        # 1. Draw data dots
        for elem in QR_ELEMENTS:
            kind = elem[0]
            if kind == "rect":
                _, x, y, w, h, _ = elem
                self.rect(box_x + x * scale, box_y_top + y * scale, w * scale, h * scale, fill=dot_color)
            elif kind == "circle":
                _, cx, cy, r = elem
                pts = [tx(px, py) for px, py in arc_pts(cx, cy, r, 0, 360, steps=16)]
                self.polygon_fill(pts, dot_color)
            elif kind == "endcap":
                # M x y v 16 h 8 a 8 8 0 0 0 0 -16 rotated by ang around (x+8, y+8)
                _, x, y, ang = elem
                cx, cy = x + 8.0, y + 8.0
                # Base shape (ang=0): left edge (x, y)->(x, y+16), bottom (x, y+16)->(x+8, y+16),
                # right semicircle centered at (x+8, y+8) from +90 deg (x+8, y+16) to -90 deg (x+8, y)
                raw = [(x, y), (x, y + 16)] + arc_pts(x + 8, y + 8, 8.0, 90, -90, steps=10)
                rpts = [tx(*rot_pt(px, py, cx, cy, ang)) for px, py in raw]
                self.polygon_fill(rpts, dot_color)
            elif kind == "corner1":
                # M x y v 16 h 16 v -8 a 8 8 0 0 0 -8 -8 rotated by ang around (x+8, y+8)
                _, x, y, ang = elem
                cx, cy = x + 8.0, y + 8.0
                # Base shape (ang=0): (x,y)->(x,y+16)->(x+16,y+16)->(x+16,y+8) + quarter arc centered at (x+8,y+8) from 0 deg to -90 deg
                raw = [(x, y), (x, y + 16), (x + 16, y + 16)] + arc_pts(x + 8, y + 8, 8.0, 0, -90, steps=6)
                rpts = [tx(*rot_pt(px, py, cx, cy, ang)) for px, py in raw]
                self.polygon_fill(rpts, dot_color)

        # 2. Draw Finder Patterns (3 corners)
        for fx, fy, fcx, fcy in QR_FINDERS:
            # Outer 112x112 ring with 80x80 hole (4 bars of thickness 16)
            # Top bar: (fx, fy, 112, 16)
            self.rect(box_x + fx * scale, box_y_top + fy * scale, 112 * scale, 16 * scale, fill=finder_outer_color)
            # Bottom bar: (fx, fy+96, 112, 16)
            self.rect(box_x + fx * scale, box_y_top + (fy + 96) * scale, 112 * scale, 16 * scale, fill=finder_outer_color)
            # Left bar: (fx, fy+16, 16, 80)
            self.rect(box_x + fx * scale, box_y_top + (fy + 16) * scale, 16 * scale, 80 * scale, fill=finder_outer_color)
            # Right bar: (fx+96, fy+16, 16, 80)
            self.rect(box_x + (fx + 96) * scale, box_y_top + (fy + 16) * scale, 16 * scale, 80 * scale, fill=finder_outer_color)
            # Center dot circle r=24 at (fcx, fcy)
            cpts = [tx(px, py) for px, py in arc_pts(fcx, fcy, 24.0, 0, 360, steps=24)]
            self.polygon_fill(cpts, finder_inner_color)

    def save(self, path):
        if self.cur:
            self.pages.append("\n".join(self.cur))
            self.cur = []

        objs = []
        def add_obj(body_bytes):
            objs.append(body_bytes)
            return len(objs)

        f1_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        f2_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        f3_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding >>")
        f4_id = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold /Encoding /WinAnsiEncoding >>")

        pages_id = len(objs) + 1 + len(self.pages) * 2
        page_ids = []
        for p_str in self.pages:
            raw = p_str.encode("latin-1", errors="replace")
            comp = zlib.compress(raw, 9)
            stream_obj = f"<< /Length {len(comp)} /Filter /FlateDecode >>\nstream\n".encode("ascii") + comp + b"\nendstream"
            s_id = add_obj(stream_obj)
            p_obj = (
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {self.page_w:.2f} {self.page_h:.2f}] "
                f"/Contents {s_id} 0 R "
                f"/Resources << /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R /F4 {f4_id} 0 R >> >> >>"
            ).encode("ascii")
            p_id = add_obj(p_obj)
            page_ids.append(p_id)

        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        actual_pages_id = add_obj(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii"))
        assert actual_pages_id == pages_id
        cat_id = add_obj(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode("ascii"))

        out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for idx, body in enumerate(objs, start=1):
            offsets.append(len(out))
            out.extend(f"{idx} 0 obj\n".encode("ascii"))
            out.extend(body)
            out.extend(b"\nendobj\n")

        xref_pos = len(out)
        out.extend(f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode("ascii"))
        for off in offsets:
            out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
        out.extend(
            f"trailer\n<< /Size {len(objs)+1} /Root {cat_id} 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(out)

# ==============================================================================
# 3. PALETTES: TRINITY OBSIDIAN LIGHT (PRINTER-FRIENDLY) & TRINITY OLED DARK
# ==============================================================================
def hex_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16)/255.0, int(h[2:4], 16)/255.0, int(h[4:6], 16)/255.0)

PALETTE_LIGHT = {
    "mode": "light",
    "bg_card":       hex_rgb("#FFFFFF"),
    "bg_inner":      hex_rgb("#F8FAFE"),
    "bg_box":        hex_rgb("#F2F6FC"),
    "bg_pill_mag":   hex_rgb("#FDF2FA"),
    "bg_pill_cyan":  hex_rgb("#F0FAFD"),
    "bg_pill_uv":    hex_rgb("#F6F0FF"),
    "obsidian":      hex_rgb("#0B0E1E"),
    "obsidian_soft": hex_rgb("#1E253C"),
    "slate":         hex_rgb("#4A5578"),
    "magenta":       hex_rgb("#D416B8"),
    "cyan":          hex_rgb("#0090B8"),
    "uv":            hex_rgb("#6E2CD8"),
    "rule":          hex_rgb("#DCE5F2"),
    "qr_bg":         hex_rgb("#FFFFFF"),
    "qr_dot":        hex_rgb("#0B0E1E"),
    "qr_finder_out": hex_rgb("#D416B8"),
    "qr_finder_in":  hex_rgb("#0090B8"),
}

PALETTE_DARK = {
    "mode": "dark",
    "bg_card":       hex_rgb("#05060D"),
    "bg_inner":      hex_rgb("#080B16"),
    "bg_box":        hex_rgb("#0D1224"),
    "bg_pill_mag":   hex_rgb("#1E0924"),
    "bg_pill_cyan":  hex_rgb("#061C29"),
    "bg_pill_uv":    hex_rgb("#140B29"),
    "obsidian":      hex_rgb("#F4F7FF"),  # Primary display text on OLED dark
    "obsidian_soft": hex_rgb("#C9D4F0"),
    "slate":         hex_rgb("#8292B8"),
    "magenta":       hex_rgb("#FF2AE5"),
    "cyan":          hex_rgb("#00E5FF"),
    "uv":            hex_rgb("#B845FF"),
    "rule":          hex_rgb("#1B2340"),
    "qr_bg":         hex_rgb("#FFFFFF"),  # High-contrast crisp white pad for 100% instant camera scan
    "qr_dot":        hex_rgb("#070A16"),
    "qr_finder_out": hex_rgb("#D416B8"),
    "qr_finder_in":  hex_rgb("#0088B0"),
}

def draw_hud_frame(pdf, pal):
    # Full card background
    pdf.rect(0, 0, PAGE_W, PAGE_H, fill=pal["bg_card"])
    # Subtle inner card frame
    fx, fy, fw, fh = 7.0, 7.0, PAGE_W - 14.0, PAGE_H - 14.0
    pdf.rect(fx, fy, fw, fh, fill=pal["bg_inner"], stroke=pal["rule"], line_w=0.6)

    # Top Tri-Segment Agent Trinity Bar (Argon Cyan -> Trinity Magenta -> Ultraviolet)
    seg = fw / 3.0
    pdf.rect(fx, fy, seg, 2.2, fill=pal["cyan"])
    pdf.rect(fx + seg, fy, seg, 2.2, fill=pal["magenta"])
    pdf.rect(fx + 2 * seg, fy, seg, 2.2, fill=pal["uv"])

    # Bottom Tri-Segment Bar
    pdf.rect(fx, fy + fh - 1.8, seg, 1.8, fill=pal["uv"])
    pdf.rect(fx + seg, fy + fh - 1.8, seg, 1.8, fill=pal["magenta"])
    pdf.rect(fx + 2 * seg, fy + fh - 1.8, seg, 1.8, fill=pal["cyan"])

    # HUD Corner Brackets (L-shapes outside/on frame corners)
    cl = 8.5
    lw = 1.3
    # Top-Left (Cyan)
    pdf.line(fx, fy, fx + cl, fy, pal["cyan"], lw)
    pdf.line(fx, fy, fx, fy + cl, pal["cyan"], lw)
    # Top-Right (Magenta)
    pdf.line(fx + fw - cl, fy, fx + fw, fy, pal["magenta"], lw)
    pdf.line(fx + fw, fy, fx + fw, fy + cl, pal["magenta"], lw)
    # Bottom-Left (Magenta)
    pdf.line(fx, fy + fh - cl, fx, fy + fh, pal["magenta"], lw)
    pdf.line(fx, fy + fh, fx + cl, fy + fh, pal["magenta"], lw)
    # Bottom-Right (Cyan)
    pdf.line(fx + fw - cl, fy + fh, fx + fw, fy + fh, pal["cyan"], lw)
    pdf.line(fx + fw, fy + fh - cl, fx + fw, fy + fh, pal["cyan"], lw)

def draw_front_page(pdf, pal, email="creator@renderwithoutcode.com"):
    pdf.new_page()
    draw_hud_frame(pdf, pal)

    # 1. Top Pill Badges
    # Left badge: [ > NEVERRENDER LABS // SRE ]
    b1_txt = "> NEVERRENDER LABS // SRE"
    b1_w = str_width(b1_txt, "F4", 5.4) + 9.0
    pdf.rect(16.0, 15.0, b1_w, 10.5, fill=pal["bg_pill_mag"], stroke=pal["magenta"], line_w=0.65)
    pdf.text(20.5, 22.1, b1_txt, "F4", 5.4, pal["magenta"])

    # Right badge: [ * GOOGLE LABS FEATURED ]
    b2_txt = "* GOOGLE LABS FEATURED"
    b2_w = str_width(b2_txt, "F4", 5.4) + 9.0
    b2_x = PAGE_W - 16.0 - b2_w
    pdf.rect(b2_x, 15.0, b2_w, 10.5, fill=pal["bg_pill_cyan"], stroke=pal["cyan"], line_w=0.65)
    pdf.text(b2_x + 4.5, 22.1, b2_txt, "F4", 5.4, pal["cyan"])

    # 2. Name & Primary Title
    pdf.text(16.0, 43.5, "MATTHEW COLE WYATT", "F2", 16.5, pal["obsidian"])
    
    # Subtitle with multi-color accents
    sub1 = "CREATIVE TECHNOLOGIST & AI SYSTEMS ARCHITECT "
    sub2 = "//"
    sub3 = " v3.1 ARGON"
    pdf.text(16.0, 54.0, sub1, "F4", 6.1, pal["cyan"])
    w_sub1 = str_width(sub1, "F4", 6.1)
    pdf.text(16.0 + w_sub1, 54.0, sub2, "F4", 6.1, pal["magenta"])
    w_sub2 = str_width(sub2, "F4", 6.1)
    pdf.text(16.0 + w_sub1 + w_sub2, 54.0, sub3, "F4", 6.1, pal["uv"])

    # Dashed HUD divider
    pdf.line(16.0, 60.0, PAGE_W - 16.0, 60.0, pal["rule"], 0.6, dash=(3, 2))

    # 3. Callout Box with Trinity Magenta Left Bar
    bx, by, bw, bh = 16.0, 65.0, PAGE_W - 32.0, 35.5
    pdf.rect(bx, by, bw, bh, fill=pal["bg_box"], stroke=pal["rule"], line_w=0.5)
    pdf.rect(bx, by, 2.6, bh, fill=pal["magenta"])

    pdf.text(bx + 8.0, by + 10.5, "> No Code. No Pulp. All Pixels. Zero B.S.", "F4", 6.6, pal["obsidian"])
    pdf.text(bx + 8.0, by + 20.5, "Architecting autonomous AI systems, full-stack commerce pipelines,", "F1", 6.3, pal["obsidian_soft"])
    pdf.text(bx + 8.0, by + 29.0, "and real-time 3D/generative media without production lag.", "F1", 6.3, pal["obsidian_soft"])

    # 4. Bottom Contact Matrix & Action Pills
    # Left solid Magenta pill: [ > RENDERWITHOUTCODE.COM ]
    p1_txt = "> RENDERWITHOUTCODE.COM"
    p1_w = str_width(p1_txt, "F4", 5.6) + 10.0
    pdf.rect(16.0, 107.0, p1_w, 12.0, fill=pal["magenta"])
    pdf.text(21.0, 114.8, p1_txt, "F4", 5.6, (1.0, 1.0, 1.0))

    # Middle Cyan outline pill: [ 760.310.0706 ]
    p2_txt = "760.310.0706"
    p2_w = str_width(p2_txt, "F4", 5.6) + 9.0
    p2_x = 16.0 + p1_w + 5.0
    pdf.rect(p2_x, 107.0, p2_w, 12.0, fill=pal["bg_pill_cyan"], stroke=pal["cyan"], line_w=0.65)
    pdf.text(p2_x + 4.5, 114.8, p2_txt, "F4", 5.6, pal["obsidian"])

    # Right tag: [ @NeverRenderLabs ]
    p3_txt = "@NeverRenderLabs"
    p3_w = str_width(p3_txt, "F4", 5.6)
    pdf.text(PAGE_W - 16.0 - p3_w, 114.8, p3_txt, "F4", 5.6, pal["uv"])

    # Footer micro-line: email + location
    pdf.text(16.0, 129.5, f"MAIL // {email}", "F4", 4.65, pal["obsidian_soft"])
    loc_txt = "SAN DIEGO, CA // [GEMINI 4 ARGON]"
    loc_w = str_width(loc_txt, "F4", 4.55)
    pdf.text(PAGE_W - 16.0 - loc_w, 129.5, loc_txt, "F4", 4.55, pal["slate"])


def draw_back_page(pdf, pal, email="creator@renderwithoutcode.com"):
    pdf.new_page()
    draw_hud_frame(pdf, pal)

    # Left Column: CONNECT TERMINAL + Endpoints
    lx = 16.0
    pdf.text(lx, 21.5, "SYSTEM DETECTED // AGENT TRINITY v3.1", "F4", 4.85, pal["cyan"])
    pdf.text(lx, 33.5, "NEVERRENDER LABS", "F2", 11.0, pal["obsidian"])
    pdf.text(lx, 41.5, "AUTONOMOUS AI & GENERATIVE MEDIA", "F4", 5.1, pal["magenta"])

    # Accent divider under header
    pdf.rect(lx, 45.8, 42.0, 1.3, fill=pal["magenta"])
    pdf.rect(lx + 42.0, 45.8, 42.0, 1.3, fill=pal["cyan"])
    pdf.rect(lx + 84.0, 45.8, 38.0, 1.3, fill=pal["uv"])

    # Terminal Endpoints Table
    rows = [
        ("WEB ", "renderwithoutcode.com", pal["cyan"]),
        ("PORT", "renderwithoutcode.com/resume.html", pal["magenta"]),
        ("MAIL", email, pal["obsidian"]),
        ("TEL ", "760.310.0706 // San Diego, CA", pal["obsidian_soft"]),
        ("FEED", "@NeverRenderLabs", pal["uv"]),
    ]
    ry = 57.0
    for lbl, val, col in rows:
        pdf.rect(lx, ry - 5.0, 16.5, 6.8, fill=pal["bg_box"], stroke=pal["rule"], line_w=0.4)
        pdf.text(lx + 1.8, ry, lbl, "F4", 4.55, pal["magenta"])
        pdf.text(lx + 19.5, ry, val, "F4", 4.7, col)
        ry += 10.2

    # Bottom Call-to-Action Box pointing to QR Code
    cta_y = 111.5
    cta_w = 123.5
    pdf.rect(lx, cta_y, cta_w, 18.0, fill=pal["bg_pill_uv"], stroke=pal["uv"], line_w=0.6)
    pdf.rect(lx, cta_y, 2.4, 18.0, fill=pal["cyan"])
    pdf.text(lx + 6.0, cta_y + 7.4, "SCAN QR TO LAUNCH STUDIO HOMEPAGE ->", "F4", 4.65, pal["uv"])
    pdf.text(lx + 6.0, cta_y + 14.4, "HTTPS://RENDERWITHOUTCODE.COM", "F4", 4.9, pal["obsidian"])

    # Right Column: Framed Rounded-Dot QR Code to https://renderwithoutcode.com/
    qr_box_size = 86.0
    qr_x = PAGE_W - 15.5 - qr_box_size
    qr_y = 21.0

    # Outer HUD container around QR code
    pdf.rect(qr_x - 3.5, qr_y - 3.5, qr_box_size + 7.0, qr_box_size + 17.0, fill=pal["bg_box"], stroke=pal["rule"], line_w=0.6)
    # Corner ticks on QR container
    qx0, qy0, qw0, qh0 = qr_x - 3.5, qr_y - 3.5, qr_box_size + 7.0, qr_box_size + 17.0
    tl = 6.0
    pdf.line(qx0, qy0, qx0 + tl, qy0, pal["magenta"], 1.1)
    pdf.line(qx0, qy0, qx0, qy0 + tl, pal["magenta"], 1.1)
    pdf.line(qx0 + qw0 - tl, qy0, qx0 + qw0, qy0, pal["cyan"], 1.1)
    pdf.line(qx0 + qw0, qy0, qx0 + qw0, qy0 + tl, pal["cyan"], 1.1)
    pdf.line(qx0, qy0 + qh0 - tl, qx0, qy0 + qh0, pal["cyan"], 1.1)
    pdf.line(qx0, qy0 + qh0, qx0 + tl, qy0 + qh0, pal["cyan"], 1.1)
    pdf.line(qx0 + qw0 - tl, qy0 + qh0, qx0 + qw0, qy0 + qh0, pal["magenta"], 1.1)
    pdf.line(qx0 + qw0, qy0 + qh0 - tl, qx0 + qw0, qy0 + qh0, pal["magenta"], 1.1)

    # Render the vector QR code
    pdf.draw_qr_vector(
        qr_x, qr_y, qr_box_size,
        dot_color=pal["qr_dot"],
        finder_outer_color=pal["qr_finder_out"],
        finder_inner_color=pal["qr_finder_in"],
        bg_color=pal["qr_bg"],
    )
    # Subtle border around white QR pad
    pdf.rect(qr_x, qr_y, qr_box_size, qr_box_size, stroke=pal["rule"], line_w=0.4)

    # Caption inside bottom of QR container
    cap = "[ HOMEPAGE // QR TERMINAL ]"
    cap_w = str_width(cap, "F4", 4.65)
    pdf.text(qr_x + (qr_box_size - cap_w) / 2.0, qr_y + qr_box_size + 8.8, cap, "F4", 4.65, pal["magenta"])


def build_10up_sheet(single_card_pdf):
    """Build a 2-page 8.5x11 US Letter 10-up (2x5 Avery 8371 / standard cardstock) print sheet with crop marks."""
    sheet = PDFCanvas(page_w=612.0, page_h=792.0)
    # 2 columns (x = 54, 306), 5 rows (y_bottom = 36, 180, 324, 468, 612)
    xs = [54.0, 306.0]
    ys = [36.0, 180.0, 324.0, 468.0, 612.0]
    for page_stream in single_card_pdf.pages:
        sheet.new_page()
        # Draw 10 cards via PDF coordinate matrix translation
        for dx in xs:
            for dy in ys:
                sheet.cur.append(f"q 1 0 0 1 {dx:.2f} {dy:.2f} cm")
                sheet.cur.append(page_stream)
                sheet.cur.append("Q")
        # Draw subtle outer crop marks around the 2x5 grid (x = 54, 306, 558; y = 36, 180, 324, 468, 612, 756)
        sheet.cur.append("0.65 0.70 0.78 RG 0.35 w")
        for cx in [54.0, 306.0, 558.0]:
            sheet.cur.append(f"{cx:.2f} 14.00 m {cx:.2f} 30.00 l S")
            sheet.cur.append(f"{cx:.2f} 762.00 m {cx:.2f} 778.00 l S")
        for cy in [36.0, 180.0, 324.0, 468.0, 612.0, 756.0]:
            sheet.cur.append(f"32.00 {cy:.2f} m 48.00 {cy:.2f} l S")
            sheet.cur.append(f"564.00 {cy:.2f} m 580.00 {cy:.2f} l S")
    return sheet

def build_all_pdfs():
    out_dirs = [
        r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\card",
        r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS",
        r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2",
    ]

    # 1. Trinity Light (Printer-Friendly Deep Obsidian + Trinity Accents - Studio Email)
    pdf_light = PDFCanvas()
    draw_front_page(pdf_light, PALETTE_LIGHT, email="creator@renderwithoutcode.com")
    draw_back_page(pdf_light, PALETTE_LIGHT, email="creator@renderwithoutcode.com")

    pdf_light_front = PDFCanvas()
    draw_front_page(pdf_light_front, PALETTE_LIGHT, email="creator@renderwithoutcode.com")

    pdf_light_back = PDFCanvas()
    draw_back_page(pdf_light_back, PALETTE_LIGHT, email="creator@renderwithoutcode.com")

    # 2. Trinity Dark (OLED Obsidian + Glowing Trinity Accents - Studio Email)
    pdf_dark = PDFCanvas()
    draw_front_page(pdf_dark, PALETTE_DARK, email="creator@renderwithoutcode.com")
    draw_back_page(pdf_dark, PALETTE_DARK, email="creator@renderwithoutcode.com")

    pdf_dark_front = PDFCanvas()
    draw_front_page(pdf_dark_front, PALETTE_DARK, email="creator@renderwithoutcode.com")

    pdf_dark_back = PDFCanvas()
    draw_back_page(pdf_dark_back, PALETTE_DARK, email="creator@renderwithoutcode.com")

    # 3. Universal Job-Search Edition (Light Printer-Friendly with jobs.net757@passinbox.com)
    pdf_univ = PDFCanvas()
    draw_front_page(pdf_univ, PALETTE_LIGHT, email="jobs.net757@passinbox.com")
    draw_back_page(pdf_univ, PALETTE_LIGHT, email="jobs.net757@passinbox.com")

    # Save everywhere needed
    paths = [
        # Website card directory
        (pdf_light, r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\card\Matthew_Wyatt_Business_Card_Trinity_Light_PRINT_READY.pdf"),
        (pdf_dark,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\card\Matthew_Wyatt_Business_Card_Trinity_Dark_PRINT_READY.pdf"),
        # APPS directory
        (pdf_light,       r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_light_PRINT_READY.pdf"),
        (pdf_light_front, r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_light_front_PRINT_READY.pdf"),
        (pdf_light_back,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_light_back_PRINT_READY.pdf"),
        (pdf_dark,        r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_dark_PRINT_READY.pdf"),
        (pdf_dark_front,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_dark_front_PRINT_READY.pdf"),
        (pdf_dark_back,   r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_dark_back_PRINT_READY.pdf"),
        # Job-search directory
        (pdf_light, r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_Business_Card_Trinity_Light.pdf"),
        (pdf_dark,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_Business_Card_Trinity_Dark.pdf"),
        (pdf_univ,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\01a_AGENTS_EYES_ONLY\DEBUGGING_LIFE\job-search\Matthew_Cole_Wyatt_Business_Card_Universal.pdf"),
        # Artifact directory for inspection
        (pdf_light, r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\Matthew_Wyatt_Business_Card_Trinity_Light_PRINT_READY.pdf"),
        (pdf_dark,  r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\Matthew_Wyatt_Business_Card_Trinity_Dark_PRINT_READY.pdf"),
    ]
    for canvas_obj, p in paths:
        canvas_obj.save(p)
        print("Saved:", p)

    # Also build 10-Up US Letter (8.5" x 11" Avery 8371 / Standard Cardstock) sheets
    sheet_light = build_10up_sheet(pdf_light)
    sheet_dark  = build_10up_sheet(pdf_dark)
    sheet_paths = [
        (sheet_light, r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\card\Matthew_Wyatt_Business_Card_Trinity_Light_10UP_LETTER_SHEET.pdf"),
        (sheet_dark,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\card\Matthew_Wyatt_Business_Card_Trinity_Dark_10UP_LETTER_SHEET.pdf"),
        (sheet_light, r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_light_10UP_LETTER_SHEET.pdf"),
        (sheet_dark,  r"c:\Users\Saturn\Desktop\G_AG_FLDR\8_BIT_THEATHER_DISTRICT_MEDIA\APPS\matthew_wyatt_trinity_dark_10UP_LETTER_SHEET.pdf"),
    ]
    for s_obj, sp in sheet_paths:
        s_obj.save(sp)
        print("Saved 10-Up Sheet:", sp)

if __name__ == "__main__":
    build_all_pdfs()
