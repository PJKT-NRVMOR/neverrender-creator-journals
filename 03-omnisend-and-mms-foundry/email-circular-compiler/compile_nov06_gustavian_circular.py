"""
Compile the updated November 6, 2026 Scandinavian Gustavian Gallery Circular
for The Chapman Collection:
- Applies Melissa Chapman's 14:24 PM 8-item lineup (Items 1 through 8 in exact order)
- Removes sold Joan Miro, Pink Silk Carpet, and Dutch Marquetry Armchair
- Updates Item 1 (Gothic Hall Stand) from English to French (Dated 1892)
- Adds Item 2 (Christ Before Pilate - Charles Amand-Durand, After Rembrandt)
- Updates Item 3 (French Napoleon III-Style Display Cabinet with Mother-of-Pearl and Ormolu) with straight-on front cut
- Adds Item 4 (Antique Hand-Painted Sevres Porcelain Plate in a Custom Shadow Box) with reflection-cleaned cut
- Adds Item 5 (Antique Renaissance Revival Fall-Front Writing Desk, Circa 1890)
- Retains Item 6 (Marble Pedestals), Item 7 (Blue Silk Qum Runner), and Item 8 (Limoges Tea Set)
- Updates closing showroom invitation text to Melissa's exact copy
- Enforces 3-Layer Chaphavian Dark-Mode Light-Lock (#F7F5F2 & #D9D3CC PNG tiles + linear-gradient + color-scheme: light only)
- Eliminates HTML entity double-parsing bugs in Omnisend (no &#10094;, &quot;, &nbsp;, or &bull; inside text nodes)
"""
import os

BASE_URL = "https://renderwithoutcode.com/drafts-for-pmc-approval/2026-11-04-scandinavian-gustavian-gallery/cuts"

OUT_DIRS = [
    r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-11-04-scandinavian-gustavian-gallery",
    r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\2026-11-04-scandinavian-gustavian-gallery",
]


def build_html(is_omnisend: bool) -> str:
    img_prefix = BASE_URL if is_omnisend else "cuts"
    bg_f7f5f2 = f"{img_prefix}/bg-f7f5f2.png"
    bg_d9d3cc = f"{img_prefix}/bg-d9d3cc.png"

    # For web preview (index.html), include optional 5-slide carousel for Items 1-5;
    # For Omnisend email import, render Item 1 cleanly without JS arrows/dots or 28px side pinch
    if not is_omnisend:
        carousel_controls_top = """
              <!-- Prev / Next Click-Advance Arrows (Web Preview Only) -->
              <div class="tcc-carousel-arrow" style="left:10px;" onclick="tccMoveSlide(-1)" title="Previous Piece">‹</div>
              <div class="tcc-carousel-arrow" style="right:10px;" onclick="tccMoveSlide(1)" title="Next Piece">›</div>
"""
        hero_img_pad = "padding:6px 16px 10px 16px;"
        extra_slides_and_dots = f"""
              <!-- Slide 2 (Web Preview): Christ Before Pilate - After Rembrandt -->
              <div class="tcc-hero-slide" style="display:none;text-align:center;">
                <div style="{hero_img_pad}background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);text-align:center;">
                  <a href="https://thechapmancollection.com/product/christ-before-pilate-ecce-homo-charles-amand-durand-after-rembrandt/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-10-christ-before-pilate-rembrandt.jpg" alt="Christ Before Pilate (Ecce Homo) - Charles Amand-Durand, After Rembrandt" width="480" style="width:100%;max-width:480px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 10px 8px 10px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    Heliogravure After Rembrandt · 35" H x 30.5" W
                  </p>
                  <h3 style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/christ-before-pilate-ecce-homo-charles-amand-durand-after-rembrandt/" target="_blank" style="color:#2B2F33;text-decoration:none;">Christ Before Pilate (Ecce Homo) - Charles Amand-Durand</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;line-height:1.65;color:#2B2F33;">
                    Finely detailed French heliogravure after Rembrandt's Large Plate, presented in a custom fluted black frame with a deep ivory mat and pewter inner trim.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/christ-before-pilate-ecce-homo-charles-amand-durand-after-rembrandt/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 3 (Web Preview): French Napoleon III-Style Display Cabinet -->
              <div class="tcc-hero-slide" style="display:none;text-align:center;">
                <div style="{hero_img_pad}background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);text-align:center;">
                  <a href="https://thechapmancollection.com/product/french-napoleon-iii-style-display-cabinet-with-mother-of-pearl-and-ormolu/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-11-french-napoleon-iii-cabinet-front.jpg" alt="French Napoleon III-Style Display Cabinet with Mother-of-Pearl and Ormolu" width="480" style="width:100%;max-width:480px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 10px 8px 10px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    French Napoleon III · 45.5" H x 48" W x 18" D
                  </p>
                  <h3 style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/french-napoleon-iii-style-display-cabinet-with-mother-of-pearl-and-ormolu/" target="_blank" style="color:#2B2F33;text-decoration:none;">French Napoleon III-Style Display Cabinet with Mother-of-Pearl</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;line-height:1.65;color:#2B2F33;">
                    Bow-ended ebonized display cabinet pairing floral marquetry, luminous mother-of-pearl blossoms and ormolu mounts with curved glass doors.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/french-napoleon-iii-style-display-cabinet-with-mother-of-pearl-and-ormolu/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 4 (Web Preview): Antique Hand-Painted Sevres Porcelain Plate -->
              <div class="tcc-hero-slide" style="display:none;text-align:center;">
                <div style="{hero_img_pad}background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);text-align:center;">
                  <a href="https://thechapmancollection.com/product/antique-hand-painted-sevres-porcelain-plate-in-a-custom-shadow-box/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-12-sevres-porcelain-plate-shadowbox.jpg" alt="Antique Hand-Painted Sevres Porcelain Plate in a Custom Shadow Box" width="480" style="width:100%;max-width:480px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 10px 8px 10px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    French Sèvres Porcelain · Custom Shadow Box · 21" H x 21" W
                  </p>
                  <h3 style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/antique-hand-painted-sevres-porcelain-plate-in-a-custom-shadow-box/" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique Hand-Painted Sèvres Porcelain Plate</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;line-height:1.65;color:#2B2F33;">
                    Rococo pastoral scene framed by a rich green rim, four floral panels of roses and violets and sweeping gold scrollwork in a gilded shadow box.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/antique-hand-painted-sevres-porcelain-plate-in-a-custom-shadow-box/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Slide 5 (Web Preview): Antique Renaissance Revival Fall-Front Writing Desk -->
              <div class="tcc-hero-slide" style="display:none;text-align:center;">
                <div style="{hero_img_pad}background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);text-align:center;">
                  <a href="https://thechapmancollection.com/product/antique-renaissance-revival-fall-front-writing-desk-circa-1890/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-13-renaissance-revival-writing-desk.jpg" alt="Antique Renaissance Revival Fall-Front Writing Desk, Circa 1890" width="480" style="width:100%;max-width:480px;height:auto;display:block;margin:0 auto;border:0;">
                  </a>
                </div>
                <div style="padding:2px 10px 8px 10px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.6px;text-transform:uppercase;color:#8A8F97;font-weight:bold;">
                    Renaissance Revival · Circa 1890 · 56" H x 58" W x 28.5" D
                  </p>
                  <h3 style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/antique-renaissance-revival-fall-front-writing-desk-circa-1890/" target="_blank" style="color:#2B2F33;text-decoration:none;">Antique Renaissance Revival Fall-Front Writing Desk</a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;line-height:1.65;color:#2B2F33;">
                    Richly carved late 19th-century writing desk crowned by a pierced scrollwork crest, winged creatures flanking a central cartouche and a fitted interior.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" align="center" style="background-color:#F7F5F2;background-image:linear-gradient(#F7F5F2,#F7F5F2);border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/antique-renaissance-revival-fall-front-writing-desk-circa-1890/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>

              <!-- Clickable Carousel Dots (1-5) -->
              <div style="padding-top:10px;text-align:center;">
                <span class="tcc-dot active" onclick="tccGoSlide(0)" title="Monumental Gothic Revival Oak Hall Stand"></span>
                <span class="tcc-dot" onclick="tccGoSlide(1)" title="Christ Before Pilate - After Rembrandt"></span>
                <span class="tcc-dot" onclick="tccGoSlide(2)" title="French Napoleon III Display Cabinet"></span>
                <span class="tcc-dot" onclick="tccGoSlide(3)" title="Hand-Painted Sevres Porcelain Plate"></span>
                <span class="tcc-dot" onclick="tccGoSlide(4)" title="Renaissance Revival Fall-Front Writing Desk"></span>
              </div>
"""
        carousel_script = """
<script type="text/javascript">
(function() {
  var currentSlide = 0;
  var slides = document.querySelectorAll('#tcc-hero-carousel .tcc-hero-slide');
  var dots = document.querySelectorAll('#tcc-hero-carousel .tcc-dot');
  var carousel = document.getElementById('tcc-hero-carousel');
  var timer = null;

  function showSlide(idx) {
    if (!slides.length) return;
    currentSlide = (idx + slides.length) % slides.length;
    for (var i = 0; i < slides.length; i++) {
      slides[i].style.display = (i === currentSlide) ? 'block' : 'none';
    }
    for (var j = 0; j < dots.length; j++) {
      if (j === currentSlide) {
        dots[j].classList.add('active');
      } else {
        dots[j].classList.remove('active');
      }
    }
  }

  window.tccMoveSlide = function(step) {
    showSlide(currentSlide + step);
    startTimer();
  };

  window.tccGoSlide = function(idx) {
    showSlide(idx);
    startTimer();
  };

  function startTimer() {
    if (timer) clearInterval(timer);
    timer = setInterval(function() {
      showSlide(currentSlide + 1);
    }, 4500);
  }

  if (carousel) {
    carousel.addEventListener('mouseenter', function() { if (timer) clearInterval(timer); });
    carousel.addEventListener('mouseleave', startTimer);
  }
  startTimer();
})();
</script>
"""
    else:
        carousel_controls_top = ""
        hero_img_pad = "padding:4px 0 12px 0;"
        extra_slides_and_dots = ""
        carousel_script = ""

    salutation = "Dear [[contact.first_name | default: 'Friend']]," if is_omnisend else "Dear Friends,"

    html = f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="color-scheme" content="light only">
<meta name="supported-color-schemes" content="light only">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:title" content="Timeless Character and Fine Craftsmanship | The Chapman Collection">
<meta property="og:description" content="A curated selection from our Rancho Santa Fe showroom: monumental French Gothic Revival oak, Old Master heliogravure after Rembrandt, Napoleon III mother-of-pearl marquetry, hand-painted Sevres porcelain and Persian carpets.">
<meta property="og:image" content="{BASE_URL}/tcc-nov04-og-banner.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<title>Timeless Character and Fine Craftsmanship - The Chapman Collection</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap">
<style type="text/css">
  :root {{
    color-scheme: light only;
    supported-color-schemes: light only;
  }}
  body, table, td, p, a, h1, h2, h3, h4 {{
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
    font-family: 'Garamond', 'EB Garamond', 'Apple Garamond', 'Georgia', serif;
  }}
  table {{
    border-collapse: collapse;
    mso-table-lspace: 0pt;
    mso-table-rspace: 0pt;
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
    color-scheme: light only !important;
    supported-color-schemes: light only !important;
    background-color: #F7F5F2 !important;
    color: #2B2F33 !important;
  }}
  .tcc-putty-surface {{
    color-scheme: light only !important;
    supported-color-schemes: light only !important;
    background-color: #D9D3CC !important;
  }}
  .tcc-btn {{
    background-color: #F7F5F2 !important;
    color: #2B2F33 !important;
    white-space: nowrap !important;
    transition: background-color 0.2s ease, color 0.2s ease;
  }}
  .tcc-btn:hover {{
    background-color: #2B2F33 !important;
    color: #F7F5F2 !important;
  }}
  .tcc-btn-td:hover {{
    background-color: #2B2F33 !important;
  }}
  .tcc-carousel-arrow {{
    position: absolute;
    top: 34%;
    transform: translateY(-50%);
    width: 34px;
    height: 34px;
    line-height: 30px;
    text-align: center;
    background-color: #F7F5F2;
    border: 1px solid #D9D3CC;
    color: #2B2F33;
    font-family: 'Garamond', 'EB Garamond', 'Georgia', serif;
    font-size: 22px;
    cursor: pointer;
    user-select: none;
    z-index: 5;
  }}
  .tcc-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #D9D3CC;
    margin: 0 5px;
    cursor: pointer;
  }}
  .tcc-dot.active {{
    background-color: #B35A5E;
  }}
  .tcc-kicker {{
    min-height: 15px;
    white-space: nowrap;
  }}
  .tcc-title {{
    min-height: 40px;
  }}
  .tcc-desc {{
    min-height: 64px;
  }}
  @media (prefers-color-scheme: dark) {{
    .tcc-putty-surface {{
      background-color: #D9D3CC !important;
    }}
    .tcc-root, .tcc-light-surface, .tcc-outer-frame, .tcc-col-top, .tcc-col-bot {{
      background-color: #F7F5F2 !important;
      color: #2B2F33 !important;
    }}
    h1, h2, h3, p, a, span {{
      mso-style-textfill-fill-color: #2B2F33;
    }}
  }}
  @media only screen and (max-width: 520px) {{
    .tcc-outer-frame {{
      width: 98% !important;
      max-width: 98% !important;
    }}
    .tcc-pad {{
      padding-left: 3% !important;
      padding-right: 3% !important;
    }}
    .tcc-brand-h1 {{
      font-size: 21px !important;
      letter-spacing: 1.6px !important;
      white-space: nowrap !important;
    }}
    .tcc-hero-h2 {{
      font-size: 18.5px !important;
      line-height: 1.25 !important;
    }}
    .tcc-hero-sub {{
      font-size: 13.5px !important;
    }}
    .tcc-subnav {{
      font-size: 8px !important;
      letter-spacing: 0.15px !important;
      white-space: nowrap !important;
    }}
    .tcc-col-top {{
      width: 48.5% !important;
      max-width: 48.5% !important;
      padding: 8px 6px 4px 6px !important;
      box-sizing: border-box !important;
    }}
    .tcc-col-bot {{
      width: 48.5% !important;
      max-width: 48.5% !important;
      padding: 4px 6px 12px 6px !important;
      box-sizing: border-box !important;
    }}
    .tcc-spacer {{
      width: 3% !important;
    }}
    .tcc-kicker {{
      font-size: 8px !important;
      letter-spacing: 0.5px !important;
      white-space: normal !important;
      min-height: 22px !important;
    }}
    .tcc-title {{
      font-size: 14.5px !important;
      line-height: 1.25 !important;
      min-height: 36px !important;
    }}
    .tcc-desc {{
      font-size: 13px !important;
      line-height: 1.45 !important;
      min-height: 76px !important;
    }}
    .tcc-btn-card {{
      font-size: 9.5px !important;
      letter-spacing: 1.1px !important;
      padding: 7px 12px !important;
      white-space: nowrap !important;
    }}
  }}
</style>
</head>
<body class="body tcc-putty-surface" bgcolor="#D9D3CC" style="margin:0;padding:0;background-color:#D9D3CC;background-image:url('{bg_d9d3cc}');background-repeat:repeat;">
<div class="tcc-root" style="color-scheme:light only;supported-color-schemes:light only;">
<!-- Hidden Preheader -->
<div style="display:none;font-size:1px;color:#D9D3CC;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
  Showroom Highlights &#183; Sunday Curatorial Selection from our Rancho Santa Fe gallery: monumental 1892 French Gothic Revival oak, Charles Amand-Durand after Rembrandt, French Napoleon III marquetry, hand-painted Sevres porcelain and Persian carpets.
</div>

<!-- Outer Surround in #D9D3CC (Chaphavian Putty) -->
<table role="presentation" class="tcc-putty-surface" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" bgcolor="#D9D3CC" background="{bg_d9d3cc}" style="width:100%;table-layout:fixed;margin:0 auto;background-color:#D9D3CC;background-image:url('{bg_d9d3cc}');background-repeat:repeat;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;">
  <tr>
    <td align="center" style="padding:20px 0;text-align:center;">

      <!-- 600px Eloquence-Width Inner Gallery Canvas in #F7F5F2 (Chaphavian Alabaster) -->
      <table role="presentation" class="tcc-outer-frame tcc-light-surface" cellspacing="0" cellpadding="0" border="0" width="600" align="center" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:600px;max-width:98%;table-layout:fixed;margin:0 auto;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border-left:1px solid #8A8F97;border-right:1px solid #8A8F97;border-top:5px solid #2B2F33;border-bottom:5px solid #2B2F33;box-sizing:border-box;text-align:left;">

        <!-- Subtle 2px #B35A5E Chaphavian Rose Accent Bar -->
        <tr>
          <td height="2" bgcolor="#B35A5E" style="height:2px;line-height:2px;font-size:2px;background-color:#B35A5E;"></td>
        </tr>

        <!-- ================================================================== -->
        <!-- 1. CENTERED CREST MASTHEAD & SINGLE-LINE CATEGORY SUBNAV           -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad tcc-light-surface" align="center" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:22px 3.5% 12px 3.5%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;box-sizing:border-box;text-align:center;">
            <a href="https://thechapmancollection.com/" target="_blank" style="text-decoration:none;">
              <img src="{img_prefix}/tcc-crest.png" alt="The Chapman Collection" width="80" style="display:block;margin:0 auto 10px auto;width:80px;max-width:80px;height:auto;border:0;">
            </a>
            <h1 class="tcc-brand-h1" style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:26.5px;letter-spacing:2.5px;text-transform:uppercase;color:#2B2F33;font-weight:normal;line-height:1.25;text-align:center;">
              The Chapman Collection
            </h1>
            <p class="tcc-subnav" style="margin:0;padding:0 0 14px 0;border-bottom:1px solid #D9D3CC;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.5px;letter-spacing:0.2px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.6;text-align:center;white-space:nowrap;">
              <a href="https://thechapmancollection.com/product-category/furniture/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Fine Furniture</a>
              <span style="color:#D9D3CC;padding:0 4px;">|</span>
              <a href="https://thechapmancollection.com/product-category/artwork-tapestries/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Artworks</a>
              <span style="color:#D9D3CC;padding:0 4px;">|</span>
              <a href="https://thechapmancollection.com/product-category/accessories/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Accessories</a>
              <span style="color:#D9D3CC;padding:0 4px;">|</span>
              <a href="https://thechapmancollection.com/services/" target="_blank" style="color:#8A8F97;text-decoration:none;white-space:nowrap;">Services</a>
            </p>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 2. ELOQUENCE EDITORIAL TITLE CARD & MELISSA'S PERSONAL INTRO       -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad tcc-light-surface" align="center" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:10px 5% 18px 5%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;text-align:center;">
            <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#8A8F97;font-weight:bold;text-align:center;">
              Showroom Highlights &#183; Sunday Curatorial Selection
            </p>
            <h2 class="tcc-hero-h2" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:22.5px;font-weight:normal;font-style:italic;color:#B35A5E;line-height:1.25;text-align:center;">
              Timeless Character and Fine Craftsmanship
            </h2>
            <p class="tcc-hero-sub" style="margin:0 0 12px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15px;font-weight:normal;font-style:normal;color:#2B2F33;line-height:1.45;text-align:center;">
              A curated selection from our Rancho Santa Fe showroom
            </p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="48" align="center" style="width:48px;margin:0 auto 14px auto;">
              <tr>
                <td height="2" bgcolor="#B35A5E" style="height:2px;line-height:2px;font-size:2px;background-color:#B35A5E;"></td>
              </tr>
            </table>
            <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;text-align:left;">
              {salutation}
            </p>
            <p style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16px;line-height:1.65;color:#2B2F33;text-align:left;">
              I hope you are enjoying a wonderful, relaxing weekend. Below is a special look at several favorite pieces currently in our Rancho Santa Fe showroom, from a monumental 1892 French Gothic Revival oak hall stand to fine European marquetry, hand-painted S&#232;vres porcelain and Persian carpets.
            </p>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 3. ITEM 1 HERO SHOWCASE: MONUMENTAL FRENCH GOTHIC HALL STAND (1892) -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad tcc-light-surface" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:4px 4% 24px 4%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;">
            <div id="tcc-hero-carousel" class="tcc-light-surface" style="position:relative;width:100%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #D9D3CC;padding:14px;box-sizing:border-box;">
{carousel_controls_top}
              <!-- Item 1: Monumental Gothic Revival Oak Hall Stand, Bearing the Date 1892 -->
              <div class="tcc-hero-slide" style="display:block;text-align:center;">
                <a href="https://thechapmancollection.com/product/monumental-gothic-revival-oak-hall-stand-dated-1892/" target="_blank" style="text-decoration:none;">
                  <img src="{img_prefix}/tcc-f7f5f2-02-english-gothic-hallstand.jpg" alt="Monumental Gothic Revival Oak Hall Stand, Bearing the Date 1892" width="480" style="width:100%;max-width:480px;height:auto;display:block;margin:0 auto 12px auto;border:0;">
                </a>
                <div style="padding:2px 6px 8px 6px;text-align:center;">
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">French Gothic Revival Oak &#183; 1892</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">117" H x 83" W x 16" D</span>
                  </p>
                  <h3 style="margin:0 0 8px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:21.5px;font-weight:normal;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/monumental-gothic-revival-oak-hall-stand-dated-1892/" target="_blank" style="color:#2B2F33;text-decoration:none;">Monumental Gothic Revival Oak Hall Stand, <span style="white-space:nowrap;">Dated 1892</span></a>
                  </h3>
                  <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;line-height:1.65;color:#2B2F33;">
                    Standing 9 feet 9 inches tall in carved French oak, four pinnacles rise above a stepped crown of pierced Gothic tracery, carved linenfold panels, a tall inset mirror and an upholstered lift-seat bench.
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/product/monumental-gothic-revival-oak-hall-stand-dated-1892/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;letter-spacing:1.8px;text-transform:uppercase;padding:10px 26px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </div>
              </div>
{extra_slides_and_dots}
            </div>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 4. SECTION 01 (ITEMS 2-5): OLD MASTER ART, MARQUETRY & CARVED OAK  -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad tcc-light-surface" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:4px 4% 24px 4%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;">
            <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:2px;text-transform:uppercase;color:#B35A5E;font-weight:bold;text-align:center;">
              Continental Craftsmanship
            </p>
            <h3 style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:23px;font-weight:normal;font-style:italic;color:#2B2F33;text-align:center;">
              Old Master Prints, French Marquetry, S&#232;vres and Carved Furniture
            </h3>

            <!-- ROW 1: ITEM 2 (CHRIST BEFORE PILATE) + ITEM 3 (FRENCH NAPOLEON III CABINET) -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;margin-bottom:16px;">
              <tr>
                <!-- Item 2 Top: Christ Before Pilate (Ecce Homo) - Charles Amand-Durand, After Rembrandt -->
                <td class="tcc-col-top tcc-light-surface" width="48.5%" valign="top" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:10px 8px 4px 8px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/christ-before-pilate-ecce-homo-charles-amand-durand-after-rembrandt/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-10-christ-before-pilate-rembrandt.jpg" alt="Christ Before Pilate (Ecce Homo) - Charles Amand-Durand, After Rembrandt" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">After Rembrandt</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">35" H x 30.5" W</span>
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/christ-before-pilate-ecce-homo-charles-amand-durand-after-rembrandt/" target="_blank" style="color:#2B2F33;text-decoration:none;">Christ Before Pilate<br>Charles Amand-Durand</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14px;line-height:1.55;color:#2B2F33;">
                    French heliogravure after Rembrandt's Large Plate in a fluted black frame with ivory mat and pewter trim.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Item 3 Top: French Napoleon III-Style Display Cabinet with Mother-of-Pearl and Ormolu -->
                <td class="tcc-col-top tcc-light-surface" width="48.5%" valign="top" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:10px 8px 4px 8px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/french-napoleon-iii-style-display-cabinet-with-mother-of-pearl-and-ormolu/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-11-french-napoleon-iii-cabinet-front.jpg" alt="French Napoleon III-Style Display Cabinet with Mother-of-Pearl and Ormolu" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">Napoleon III</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">45.5" H x 48" W</span>
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/french-napoleon-iii-style-display-cabinet-with-mother-of-pearl-and-ormolu/" target="_blank" style="color:#2B2F33;text-decoration:none;">Napoleon III Cabinet<br>with Mother-of-Pearl</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14px;line-height:1.55;color:#2B2F33;">
                    Bow-ended ebonized cabinet with floral marquetry, mother-of-pearl inlay, ormolu mounts and curved glass.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 1 -->
              <tr>
                <td class="tcc-col-bot tcc-light-surface" width="48.5%" valign="bottom" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:6px 8px 14px 8px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn tcc-btn-card" href="https://thechapmancollection.com/product/christ-before-pilate-ecce-homo-charles-amand-durand-after-rembrandt/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 16px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot tcc-light-surface" width="48.5%" valign="bottom" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:6px 8px 14px 8px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn tcc-btn-card" href="https://thechapmancollection.com/product/french-napoleon-iii-style-display-cabinet-with-mother-of-pearl-and-ormolu/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 16px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>

            <!-- ROW 2: ITEM 4 (SEVRES PORCELAIN PLATE) + ITEM 5 (RENAISSANCE REVIVAL DESK) -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;">
              <tr>
                <!-- Item 4 Top: Antique Hand-Painted Sevres Porcelain Plate in a Custom Shadow Box -->
                <td class="tcc-col-top tcc-light-surface" width="48.5%" valign="top" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:10px 8px 4px 8px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/antique-hand-painted-sevres-porcelain-plate-in-a-custom-shadow-box/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-12-sevres-porcelain-plate-shadowbox.jpg" alt="Antique Hand-Painted Sevres Porcelain Plate in a Custom Shadow Box" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">S&#232;vres Porcelain</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">21" H x 21" W</span>
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/antique-hand-painted-sevres-porcelain-plate-in-a-custom-shadow-box/" target="_blank" style="color:#2B2F33;text-decoration:none;">Hand-Painted S&#232;vres<br>Plate in Shadow Box</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14px;line-height:1.55;color:#2B2F33;">
                    Rococo pastoral scene with a rich green rim, four floral panels and gold scrollwork in a gilded shadow box.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Item 5 Top: Antique Renaissance Revival Fall-Front Writing Desk, Circa 1890 -->
                <td class="tcc-col-top tcc-light-surface" width="48.5%" valign="top" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:10px 8px 4px 8px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/antique-renaissance-revival-fall-front-writing-desk-circa-1890/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-13-renaissance-revival-writing-desk.jpg" alt="Antique Renaissance Revival Fall-Front Writing Desk, Circa 1890" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">Circa 1890</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">56" H x 58" W</span>
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/antique-renaissance-revival-fall-front-writing-desk-circa-1890/" target="_blank" style="color:#2B2F33;text-decoration:none;">Renaissance Revival<br>Fall-Front Writing Desk</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14px;line-height:1.55;color:#2B2F33;">
                    Crowned by a pierced scrollwork crest with carved winged figures, fluted legs and a fitted writing interior.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 2 -->
              <tr>
                <td class="tcc-col-bot tcc-light-surface" width="48.5%" valign="bottom" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:6px 8px 14px 8px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn tcc-btn-card" href="https://thechapmancollection.com/product/antique-hand-painted-sevres-porcelain-plate-in-a-custom-shadow-box/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 16px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot tcc-light-surface" width="48.5%" valign="bottom" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:6px 8px 14px 8px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn tcc-btn-card" href="https://thechapmancollection.com/product/antique-renaissance-revival-fall-front-writing-desk-circa-1890/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 16px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 5. SECTION 02 (ITEMS 6-7): EMPIRE MARBLE & HAND-FINISHED SILK      -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad tcc-light-surface" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:0 4% 24px 4%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;">
            <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:2px;text-transform:uppercase;color:#B35A5E;font-weight:bold;text-align:center;">
              Curated Across the Gallery
            </p>
            <h3 style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:23px;font-weight:normal;font-style:italic;color:#2B2F33;text-align:center;">
              Empire Marble and Persian Carpets
            </h3>

            <!-- ROW 3: ITEM 6 (MARBLE PEDESTALS) + ITEM 7 (BLUE SILK QUM RUNNER) -->
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;table-layout:fixed;">
              <tr>
                <!-- Item 6 Top: Pair of French Empire Style Marble Pedestals (WC-3306) -->
                <td class="tcc-col-top tcc-light-surface" width="48.5%" valign="top" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:10px 8px 4px 8px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-05-french-empire-pedestals.jpg" alt="Pair of French Empire Style Green Marble Pedestals" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">Green Marble and Gilt</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">54.5" H</span>
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="color:#2B2F33;text-decoration:none;">Pair of French Empire<br>Green Marble Pedestals</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14px;line-height:1.55;color:#2B2F33;">
                    Tapered green veined marble columns adorned with classical gilt metal swags and moldings.
                  </p>
                </td>

                <td class="tcc-spacer" width="3%" style="width:3%;"></td>

                <!-- Item 7 Top: 10-Foot Silk Qum Runner Medallion Close-Up (Redirected to Carpets Category) -->
                <td class="tcc-col-top tcc-light-surface" width="48.5%" valign="top" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-bottom:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:10px 8px 4px 8px;box-sizing:border-box;text-align:center;">
                  <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="text-decoration:none;">
                    <img src="{img_prefix}/tcc-f7f5f2-07-silk-qum-runner-closeup.jpg" alt="Persian Carpet Medallion Detail" width="236" style="width:100%;max-width:236px;height:auto;display:block;margin:0 auto 10px auto;border:0;">
                  </a>
                  <p class="tcc-kicker" style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:8.8px;letter-spacing:0.8px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.35;white-space:nowrap;">
                    <span style="white-space:nowrap;">Persian Carpets</span> <span style="padding:0 2px;">&#183;</span> <span style="white-space:nowrap;">Showroom Collection</span>
                  </p>
                  <p class="tcc-title" style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:15.5px;font-style:italic;color:#2B2F33;line-height:1.3;">
                    <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="color:#2B2F33;text-decoration:none;">Explore Our Collection<br>of Persian Carpets</a>
                  </p>
                  <p class="tcc-desc" style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:14px;line-height:1.55;color:#2B2F33;">
                    A close study of our midnight blue ground, radiant ivory medallion and classic botanicals.
                  </p>
                </td>
              </tr>
              <!-- Locked Symmetrical Button Row for Row 3 -->
              <tr>
                <td class="tcc-col-bot tcc-light-surface" width="48.5%" valign="bottom" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:6px 8px 14px 8px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn tcc-btn-card" href="https://thechapmancollection.com/product/pair-of-french-empire-style-marble-pedestals/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 16px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="tcc-spacer" width="3%" style="width:3%;"></td>
                <td class="tcc-col-bot tcc-light-surface" width="48.5%" valign="bottom" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:48.5%;border:1px solid #D9D3CC;border-top:0;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;padding:6px 8px 14px 8px;box-sizing:border-box;text-align:center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn tcc-btn-card" href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;padding:8px 16px;display:inline-block;white-space:nowrap;">Select this Piece</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ================================================================== -->
        <!-- 6. RANCHO SANTA FE SHOWROOM INVITATION & SIGNATURE                 -->
        <!-- ================================================================== -->
        <tr>
          <td class="tcc-pad tcc-light-surface" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:6px 5% 26px 5%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;box-sizing:border-box;">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;border:1px solid #D9D3CC;background-color:#D9D3CC;margin:4px 0 22px 0;">
              <tr>
                <td class="tcc-light-surface" align="center" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="padding:22px 18px;text-align:center;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;">
                  <p style="margin:0 0 6px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#B35A5E;font-weight:bold;">
                    Visit Our Rancho Santa Fe Gallery
                  </p>
                  <p style="margin:0 0 10px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:16.5px;line-height:1.65;color:#2B2F33;">
                    Visit our Rancho Santa Fe showroom or contact us directly for more information on any piece in our collection.
                  </p>
                  <p style="margin:0 0 18px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:11.5px;letter-spacing:0.6px;color:#8A8F97;font-weight:bold;line-height:1.55;">
                    Monday through Thursday 10:00 AM to 6:00 PM &#183; Friday and Saturday 10:00 AM to 7:00 PM &#183; Sunday by Appointment
                  </p>
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:0 auto;">
                    <tr>
                      <td class="tcc-btn-td" bgcolor="#F7F5F2" background="{bg_f7f5f2}" align="center" style="background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border:1px solid #2B2F33;text-align:center;">
                        <a class="tcc-btn" href="https://thechapmancollection.com/" target="_blank" style="background-color:#F7F5F2;color:#2B2F33;text-decoration:none;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:13px;letter-spacing:2px;text-transform:uppercase;padding:12px 30px;display:inline-block;white-space:nowrap;">Explore the Full Collection</a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin:14px 0 0 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10.5px;letter-spacing:1.4px;text-transform:uppercase;color:#8A8F97;font-weight:bold;line-height:1.5;">
                    <a href="https://thechapmancollection.com/services/#shipping-and-delivery" target="_blank" style="color:#8A8F97;text-decoration:none;border-bottom:1px solid #D9D3CC;padding-bottom:1px;">Worldwide and Local Shipping Available</a>
                  </p>
                </td>
              </tr>
            </table>

            <p style="margin:0 0 16px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:17px;line-height:1.65;color:#2B2F33;text-align:left;">
              Warmly,<br>Melissa Chapman
            </p>

            <!-- Compact Signature Footer in Chaphavian Palette -->
            <table role="presentation" class="tcc-light-surface" cellspacing="0" cellpadding="0" border="0" width="100%" bgcolor="#F7F5F2" background="{bg_f7f5f2}" style="width:100%;background-color:#F7F5F2;background-image:url('{bg_f7f5f2}');background-repeat:repeat;border-top:1px solid #D9D3CC;padding-top:14px;">
              <tr>
                <td width="54" valign="middle" align="center" style="width:54px;padding-right:12px;border-right:1px solid #D9D3CC;">
                  <img src="{img_prefix}/tcc-crest.png" alt="The Chapman Collection" width="46" style="width:46px;max-width:46px;height:auto;display:block;border:0;">
                </td>
                <td valign="middle" style="padding-left:12px;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;color:#2B2F33;text-align:left;">
                  <p style="margin:0 0 2px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12.5px;font-weight:bold;letter-spacing:1.2px;text-transform:uppercase;color:#2B2F33;line-height:1.35;">
                    THE CHAPMAN COLLECTION
                  </p>
                  <p style="margin:0 0 3px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:11.5px;font-style:italic;color:#8A8F97;line-height:1.4;">
                    Serving Collectors for Over 30 Years
                  </p>
                  <p style="margin:0 0 4px 0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:12px;line-height:1.45;color:#8A8F97;">
                    <a href="tel:+18583492638" style="color:#2B2F33;text-decoration:none;font-weight:bold;">858-349-2638</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.google.com/maps/search/?api=1&query=The+Chapman+Collection+6014+La+Granada+Rancho+Santa+Fe+CA+92067" target="_blank" style="color:#8A8F97;text-decoration:none;">6014 La Granada, Rancho Santa Fe, CA 92067</a>
                  </p>
                  <p style="margin:0;font-family:'Garamond','EB Garamond','Apple Garamond','Georgia',serif;font-size:10px;letter-spacing:1px;color:#B35A5E;font-weight:bold;line-height:1.5;">
                    <a href="https://thechapmancollection.com/" target="_blank" style="color:#B35A5E;text-decoration:none;">WEBSITE</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.instagram.com/thechapmancollection/" target="_blank" style="color:#B35A5E;text-decoration:none;">INSTAGRAM</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.facebook.com/TheChapmanCollection" target="_blank" style="color:#B35A5E;text-decoration:none;">FACEBOOK</a>
                    <span style="color:#D9D3CC;padding:0 5px;">|</span>
                    <a href="https://www.youtube.com/@TheChapmanCollection" target="_blank" style="color:#B35A5E;text-decoration:none;">YOUTUBE</a>
                  </p>
                </td>
              </tr>
            </table>

          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</div>
{carousel_script}
</body>
</html>
"""
    html = html.replace("&#183;", "·").replace("&#232;", "è")
    html = html.replace(f' background="{bg_f7f5f2}"', "").replace(f' background="{bg_d9d3cc}"', "")
    html = html.replace(f"background-image:url('{bg_f7f5f2}');background-repeat:repeat;", "")
    html = html.replace(f"background-image:url('{bg_d9d3cc}');background-repeat:repeat;", "")
    html = html.replace("background-image:linear-gradient(#F7F5F2,#F7F5F2);", "")
    html = html.replace("background-image:linear-gradient(#D9D3CC,#D9D3CC);", "")
    return html


def main():
    web_html = build_html(is_omnisend=False)
    omnisend_html = build_html(is_omnisend=True)

    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        idx_path = os.path.join(d, "index.html")
        omni_path = os.path.join(d, "2026-11-04-Omnisend_Scandinavian_Gustavian_Gallery_Full_Import.html")
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(web_html)
        with open(omni_path, "w", encoding="utf-8") as f:
            f.write(omnisend_html)
        print(f"Compiled: {idx_path} ({len(web_html)} bytes)")
        print(f"Compiled: {omni_path} ({len(omnisend_html)} bytes)")


if __name__ == "__main__":
    main()
