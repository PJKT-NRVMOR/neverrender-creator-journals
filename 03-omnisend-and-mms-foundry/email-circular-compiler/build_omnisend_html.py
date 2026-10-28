import os
import sys

sys.path.insert(0, r"C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\scratch")
from build_oct20_mel_final_newsletter import (
    SUBJECT_TITLE, GREETING, INTRO_P1, INTRO_P2, INTRO_P3,
    CARPETS_HEAD, CARPETS_P1, CARPETS_P2, CARPET_1_CAP, CARPET_2_CAP,
    FURN_HEAD, FURN_P1, FURN_1_CAP, FURN_2_CAP,
    ART_HEAD, ART_P1, ART_1_CAP, ART_2_CAP,
    ACC_HEAD, ACC_P1, ACC_CLOCK_CAP, ACC_URNS_CAP, ACC_VASES_CAP,
    AWARD_HEAD, AWARD_P1, CLOSING_P1, CLOSING_P2, CLOSING_P3, HOURS_LINE,
    yt_canonical
)

CDN = "https://thechapmancollection.com/wp-content/uploads/2026/10"
u_crest = f"{CDN}/tcc-oct23-crest.png"
u_c1    = f"{CDN}/tcc-oct23-carpet-1-medallion.jpg"
u_c2    = f"{CDN}/tcc-oct23-carpet-2-teal-silk.jpg"
u_f1    = f"{CDN}/tcc-oct23-furn-1-french-desk.jpg"
u_f2    = f"{CDN}/tcc-oct23-furn-2-french-commode.jpg"
u_a1    = f"{CDN}/tcc-oct23-art-1-venice-oil.jpg"
u_a2    = f"{CDN}/tcc-oct23-art-2-matisse-litho.jpg"
u_acc1  = f"{CDN}/tcc-oct23-acc-1-grandfather-clock.jpg"
u_acc2  = f"{CDN}/tcc-oct23-acc-2-vienna-urns.jpg"
u_acc3  = f"{CDN}/tcc-oct23-acc-3-dragon-vases.jpg"
u_awd   = f"{CDN}/tcc-oct23-award-ranch-and-coast-2026.jpg"

S_SEC_HEAD = "margin: 6px 0 10px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 24px; color: #701D32; font-weight: normal; letter-spacing: 0.5px; border-bottom: 1px solid #D5C7A3; padding-bottom: 5px; text-align: left;"
S_BODY_P   = "margin: 0 0 12px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 18px; line-height: 1.65; color: #24211F; text-align: left; overflow-wrap: break-word; word-wrap: break-word;"
S_CAP_P    = "margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.45; color: #2C2825; text-align: left; overflow-wrap: break-word; word-wrap: break-word;"
S_CAP_SM   = "margin: 8px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 13.5px; line-height: 1.4; color: #2C2825; text-align: left; overflow-wrap: break-word; word-wrap: break-word;"
S_CTA_BTN  = "background-color: #701D32; border: 1px solid #C5A059; color: #FFFFFF !important; text-decoration: none; font-family: 'Garamond', 'Georgia', 'Times New Roman', serif; font-size: 13.5px; font-weight: bold; letter-spacing: 1.5px; text-transform: uppercase; padding: 13px 20px; display: inline-block; border-radius: 2px; box-sizing: border-box; max-width: 96%; text-align: center;"

responsive_css = """<style type="text/css">
  body, table, td, p, a, h1, h2, h3 {
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  table {
    border-collapse: collapse;
    mso-table-lspace: 0pt;
    mso-table-rspace: 0pt;
  }
  img {
    border: 0;
    height: auto;
    line-height: 100%;
    outline: none;
    text-decoration: none;
    max-width: 100%;
  }
  @media only screen and (max-width: 480px) {
    .tcc-outer-td {
      padding: 10px 6px !important;
    }
    .tcc-main-card {
      width: 94% !important;
      max-width: 94% !important;
      margin: 0 auto !important;
    }
    .tcc-sec-td {
      padding-left: 6% !important;
      padding-right: 6% !important;
      text-align: center !important;
    }
    .tcc-sec-td h3, .tcc-sec-td p {
      text-align: center !important;
    }
    .tcc-grid, .tcc-grid tbody, .tcc-grid tr {
      display: block !important;
      width: 100% !important;
    }
    .tcc-col-card, .tcc-col-text {
      display: block !important;
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      margin: 0 auto 14px auto !important;
      text-align: center !important;
    }
    .tcc-spacer {
      display: none !important;
      width: 0 !important;
      height: 0 !important;
    }
    .tcc-h1 {
      font-size: 20px !important;
      letter-spacing: 1.6px !important;
    }
    .tcc-h2 {
      font-size: 22px !important;
    }
  }
</style>"""

table_body = f"""<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" style="width: 100%; margin: 0 auto; background-color: #F4F1EA; font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;">
  <tr>
    <td class="tcc-outer-td" align="center" style="padding: 16px 0; text-align: center;">
      <table role="presentation" class="tcc-main-card" cellspacing="0" cellpadding="0" border="0" width="94%" align="center" style="width: 94%; max-width: 650px; margin: 0 auto; background-color: #FFFFFF; border: 1.5px solid #B7A486; table-layout: fixed; box-sizing: border-box; text-align: left;">
        <tr>
          <td height="4" style="background-color: #701D32; height: 4px; font-size: 0; line-height: 0;"></td>
        </tr>
        <tr>
          <td class="tcc-sec-td" align="center" style="padding: 24px 4.5% 14px 4.5%; background-color: #FFFFFF; box-sizing: border-box; text-align: center;">
            <a href="https://thechapmancollection.com/" target="_blank" style="text-decoration: none;">
              <img src="{u_crest}" alt="The Chapman Collection Crest" width="80" style="display: block; margin: 0 auto 10px auto; width: 80px; max-width: 80px; height: auto; border: 0;">
            </a>
            <h1 class="tcc-h1" style="margin: 0 0 8px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 24px; letter-spacing: 2.2px; text-transform: uppercase; color: #1F1D1C; font-weight: normal; line-height: 1.25; text-align: center;">
              <a href="https://thechapmancollection.com/" target="_blank" style="color: #1F1D1C; text-decoration: none;">The Chapman Collection</a>
            </h1>
            <p style="margin: 0 0 14px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 11.5px; letter-spacing: 1.2px; text-transform: uppercase; color: #8C6D46; font-weight: bold; line-height: 1.6; text-align: center;">
              <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="color: #8C6D46; text-decoration: none;">Persian Carpets</a>
              <span style="color: #B7A486; padding: 0 4px;">|</span>
              <a href="https://thechapmancollection.com/product-category/furniture/" target="_blank" style="color: #8C6D46; text-decoration: none;">Fine Furniture</a>
              <span style="color: #B7A486; padding: 0 4px;">|</span>
              <a href="https://thechapmancollection.com/product-category/artwork-tapestries/" target="_blank" style="color: #8C6D46; text-decoration: none;">Artworks</a>
              <span style="color: #B7A486; padding: 0 4px;">|</span>
              <a href="https://thechapmancollection.com/product-category/accessories/" target="_blank" style="color: #8C6D46; text-decoration: none;">Accessories</a>
            </p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td height="1" style="background-color: #D5C7A3; height: 1px; font-size: 0; line-height: 0;"></td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" align="center" style="padding: 4px 4.5% 12px 4.5%; background-color: #FFFFFF; box-sizing: border-box; text-align: center;">
            <h2 class="tcc-h2" style="margin: 0; font-family: 'Garamond', 'Georgia', serif; font-size: 26px; line-height: 1.25; color: #701D32; font-weight: normal; font-style: italic; text-align: center;">{SUBJECT_TITLE}</h2>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" style="padding: 4px 5% 10px 5%; background-color: #FFFFFF; box-sizing: border-box;">
            <p style="{S_BODY_P} font-size: 19px; margin-bottom: 10px;">{GREETING}</p>
            <p style="{S_BODY_P}">{INTRO_P1}</p>
            <p style="{S_BODY_P}">{INTRO_P2}</p>
            <p style="{S_BODY_P} margin-bottom: 4px; font-style: italic; color: #5C554E;">{INTRO_P3}</p>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" style="padding: 8px 5% 16px 5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="{S_SEC_HEAD}">
              <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="color: #701D32; text-decoration: none;">{CARPETS_HEAD}</a>
            </h3>
            <p style="{S_BODY_P}">{CARPETS_P1}</p>
            <p style="{S_BODY_P} margin-bottom: 14px;">{CARPETS_P2}</p>
            <table role="presentation" class="tcc-grid" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col-card" width="48%" valign="top" style="width: 48%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2.5%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="text-decoration: none;">
                    <img src="{u_c1}" alt="Persian Medallion Carpet" style="width: 100%; max-width: 215px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_P}">{CARPET_1_CAP}</p>
                </td>
                <td class="tcc-spacer" width="4%" style="width: 4%; font-size: 0; line-height: 0;"></td>
                <td class="tcc-col-card" width="48%" valign="top" style="width: 48%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2.5%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="text-decoration: none;">
                    <img src="{u_c2}" alt="Pure Silk Teal Persian Carpet" style="width: 100%; max-width: 215px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_P}">{CARPET_2_CAP}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" style="padding: 8px 5% 16px 5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="{S_SEC_HEAD}">
              <a href="https://thechapmancollection.com/product-category/furniture/" target="_blank" style="color: #701D32; text-decoration: none;">{FURN_HEAD}</a>
            </h3>
            <p style="{S_BODY_P} margin-bottom: 14px;">{FURN_P1}</p>
            <table role="presentation" class="tcc-grid" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col-card" width="48%" valign="top" style="width: 48%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2.5%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product/french-louis-xv-style-writing-desk-with-bronze-mounts/" target="_blank" style="text-decoration: none;">
                    <img src="{u_f1}" alt="French Desk with Bronze Mounts" style="width: 100%; max-width: 235px; height: auto; display: block; margin: 12px auto; border: 0;">
                  </a>
                  <p style="{S_CAP_P}">{FURN_1_CAP}</p>
                </td>
                <td class="tcc-spacer" width="4%" style="width: 4%; font-size: 0; line-height: 0;"></td>
                <td class="tcc-col-card" width="48%" valign="top" style="width: 48%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2.5%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product/antique-french-louis-xv-style-marquetry-commode-with-rouge-marble-top/" target="_blank" style="text-decoration: none;">
                    <img src="{u_f2}" alt="French Marble-Top Commode" style="width: 100%; max-width: 195px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_P}">{FURN_2_CAP}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" style="padding: 8px 5% 16px 5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="{S_SEC_HEAD}">
              <a href="https://thechapmancollection.com/product-category/artwork-tapestries/" target="_blank" style="color: #701D32; text-decoration: none;">{ART_HEAD}</a>
            </h3>
            <p style="{S_BODY_P} margin-bottom: 14px;">{ART_P1}</p>
            <table role="presentation" class="tcc-grid" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col-card" width="48%" valign="top" style="width: 48%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2.5%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product/italian-oil-on-canvas-depicting-venetian-canal/" target="_blank" style="text-decoration: none;">
                    <img src="{u_a1}" alt="Original Oil on Canvas of Venice" style="width: 100%; max-width: 210px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_P}">{ART_1_CAP}</p>
                </td>
                <td class="tcc-spacer" width="4%" style="width: 4%; font-size: 0; line-height: 0;"></td>
                <td class="tcc-col-card" width="48%" valign="top" style="width: 48%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2.5%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product-category/artwork-tapestries/" target="_blank" style="text-decoration: none;">
                    <img src="{u_a2}" alt="Framed Lithograph of Henri Matisse Blue Nude III" style="width: 100%; max-width: 180px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_P}">{ART_2_CAP}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" style="padding: 8px 5% 16px 5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="{S_SEC_HEAD}">
              <a href="https://thechapmancollection.com/product-category/accessories/" target="_blank" style="color: #701D32; text-decoration: none;">{ACC_HEAD}</a>
            </h3>
            <p style="{S_BODY_P} margin-bottom: 14px;">{ACC_P1}</p>
            <table role="presentation" class="tcc-grid" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col-card" width="31%" valign="top" style="width: 31%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 8px 1.8%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product/traditional-american-grandfather-clock/" target="_blank" style="text-decoration: none;">
                    <img src="{u_acc1}" alt="American Grandfather Clock" style="width: 100%; max-width: 85px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_SM}">{ACC_CLOCK_CAP}</p>
                </td>
                <td class="tcc-spacer" width="3.5%" style="width: 3.5%; font-size: 0; line-height: 0;"></td>
                <td class="tcc-col-card" width="31%" valign="top" style="width: 31%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 8px 1.8%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product/pair-of-royal-vienna-style-hand-painted-porcelain-urns/" target="_blank" style="text-decoration: none;">
                    <img src="{u_acc2}" alt="Royal Vienna-Style Porcelain Urns" style="width: 100%; max-width: 155px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_SM}">{ACC_URNS_CAP}</p>
                </td>
                <td class="tcc-spacer" width="3.5%" style="width: 3.5%; font-size: 0; line-height: 0;"></td>
                <td class="tcc-col-card" width="31%" valign="top" style="width: 31%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 8px 1.8%; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/product-category/accessories/" target="_blank" style="text-decoration: none;">
                    <img src="{u_acc3}" alt="Pair of Chinese Vases with Raised Dragons" style="width: 100%; max-width: 155px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="{S_CAP_SM}">{ACC_VASES_CAP}</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-sec-td" style="padding: 8px 5% 18px 5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="{S_SEC_HEAD}">
              <a href="https://thechapmancollection.com/about-us/" target="_blank" style="color: #701D32; text-decoration: none;">{AWARD_HEAD}</a>
            </h3>
            <p style="{S_BODY_P} margin-bottom: 14px;">{AWARD_P1}</p>
            <table role="presentation" class="tcc-grid" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col-card" width="44%" valign="middle" style="width: 44%; background-color: #FFFFFF; border: 1px solid #C8B68E; padding: 10px 2%; text-align: center; box-sizing: border-box;">
                  <a href="https://thechapmancollection.com/about-us/" target="_blank" style="text-decoration: none;">
                    <img src="{u_awd}" alt="Ranch and Coast Best Antique Store 2026" style="width: 100%; max-width: 215px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                </td>
                <td class="tcc-spacer" width="4%" style="width: 4%; font-size: 0; line-height: 0;"></td>
                <td class="tcc-col-text" width="52%" valign="middle" style="width: 52%; padding: 4px 1%; box-sizing: border-box;">
                  <p style="{S_BODY_P} font-size: 16.5px; margin-bottom: 10px;">{CLOSING_P1}</p>
                  <p style="{S_BODY_P} font-size: 16.5px; margin-bottom: 10px;">{CLOSING_P2}</p>
                  <p style="{S_BODY_P} font-size: 16.5px; margin-bottom: 10px;">{CLOSING_P3}</p>
                  <p style="margin: 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; color: #701D32; font-style: italic; font-weight: bold; text-align: left;">{HOURS_LINE}</p>
                </td>
              </tr>
            </table>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; margin: 16px 0 18px 0; table-layout: fixed;">
              <tr>
                <td align="center" style="text-align: center;">
                  <a href="https://thechapmancollection.com/" target="_blank" style="{S_CTA_BTN}">Explore the Collection Online</a>
                </td>
              </tr>
            </table>
            <p style="{S_BODY_P} margin-bottom: 4px;">Kind regards,</p>
            <p style="margin: 0 0 14px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 21px; color: #701D32; font-weight: bold; text-align: left;">Melissa Chapman</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; background-color: #FFFFFF; border-top: 1px solid #EAE4D8; padding-top: 14px; table-layout: fixed;">
              <tr>
                <td width="54" valign="middle" align="center" style="width: 54px; padding-right: 8px; border-right: 1px solid #D5C7A3;">
                  <a href="https://thechapmancollection.com/" target="_blank" style="text-decoration: none;">
                    <img src="{u_crest}" alt="The Chapman Collection Crest" width="44" style="width: 44px; max-width: 44px; height: auto; display: block; border: 0;">
                  </a>
                </td>
                <td valign="middle" style="padding-left: 10px; font-family: 'Garamond', 'Georgia', serif; color: #1F1D1C; text-align: left; overflow-wrap: break-word; word-wrap: break-word;">
                  <p style="margin: 0 0 3px 0; font-size: 13px; font-weight: bold; letter-spacing: 0.7px; text-transform: uppercase; color: #1F1D1C; line-height: 1.35;">
                    MELISSA CHAPMAN | <a href="https://thechapmancollection.com/" target="_blank" style="color: #8C6D46; text-decoration: none;">THE CHAPMAN COLLECTION</a>
                  </p>
                  <p style="margin: 0 0 3px 0; font-size: 12px; line-height: 1.45; color: #3D3935;">
                    <a href="tel:+18583492638" style="color: #1F1D1C; text-decoration: none; font-weight: bold;">(858) 349-2638</a>
                    <span style="color: #B7A486; padding: 0 3px;">|</span>
                    <a href="https://maps.app.goo.gl/rqF7BedXYD9D87EJ6" target="_blank" style="color: #3D3935; text-decoration: none;">6014 La Granada, Rancho Santa Fe, CA 92067</a>
                  </p>
                  <p style="margin: 0; font-size: 11px; letter-spacing: 0.5px; color: #701D32; font-weight: bold; line-height: 1.5;">
                    <a href="https://thechapmancollection.com/" target="_blank" style="color: #701D32; text-decoration: none;">WEBSITE</a>
                    <span style="color: #B7A486; padding: 0 3px;">|</span>
                    <a href="https://www.instagram.com/thechapmancollection/" target="_blank" style="color: #701D32; text-decoration: none;">INSTAGRAM</a>
                    <span style="color: #B7A486; padding: 0 3px;">|</span>
                    <a href="https://www.facebook.com/TheChapmanCollection" target="_blank" style="color: #701D32; text-decoration: none;">FACEBOOK</a>
                    <span style="color: #B7A486; padding: 0 3px;">|</span>
                    <a href="{yt_canonical}" target="_blank" style="color: #701D32; text-decoration: none;">YOUTUBE</a>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td height="4" style="background-color: #701D32; height: 4px; font-size: 0; line-height: 0;"></td>
        </tr>
      </table>
    </td>
  </tr>
</table>"""

for bad_ent in ["&nbsp;", "&#8226;", "&bull;"]:
    table_body = table_body.replace(bad_ent, " ")
table_body = table_body.replace("&amp;", "and")

out_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval"

full_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{SUBJECT_TITLE}</title>
{responsive_css}
</head>
<body style="margin:0;padding:0;background-color:#F4F1EA;">
{table_body}
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width:100%;background-color:#F4F1EA;">
  <tr>
    <td align="center" style="padding: 8px 10px 24px 10px; font-family: 'Garamond', 'Georgia', serif; font-size: 12px; color: #6E675F; line-height: 1.6; text-align: center;">
      The Chapman Collection | 6014 La Granada, Rancho Santa Fe, CA 92067<br>
      <a href="[[unsubscribe_url]]" style="color: #701D32; text-decoration: underline;">Unsubscribe</a>
    </td>
  </tr>
</table>
</body>
</html>"""

for bad_ent in ["&nbsp;", "&#8226;", "&bull;"]:
    full_template = full_template.replace(bad_ent, " ")
full_template = full_template.replace("&amp;", "and")

linked_path = os.path.join(out_dir, "2026-10-20-Thursday_Newsletter_Draft_2_White_Background_Linked.html")
with open(linked_path, "w", encoding="utf-8") as f:
    f.write(full_template)

full_path = os.path.join(out_dir, "2026-10-23-Omnisend_Saved_Template_Full_Import.html")
with open(full_path, "w", encoding="utf-8") as f:
    f.write(full_template)

block_only_path = os.path.join(out_dir, "2026-10-23-Omnisend_Custom_HTML_Block_Table_Only.html")
with open(block_only_path, "w", encoding="utf-8") as f:
    f.write(table_body)

print("Wrote Primary Responsive Saved Template:", linked_path, os.path.getsize(linked_path), "bytes")
print("Wrote Mirror Saved Template:", full_path, os.path.getsize(full_path), "bytes")
print("Wrote Table-Only Block HTML:", block_only_path, os.path.getsize(block_only_path), "bytes")
