import os

BASE_CAMPAIGN_DIR = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-27-autum-warmth-and-old-world-peculiars"
NRL_ROOT = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval"
NRL_SUB = os.path.join(NRL_ROOT, "2026-10-27-autumn-warmth-and-old-world-peculiars")

def build_sms_html(cuts_prefix, circular_href):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="website">
<meta property="og:title" content="Autumn warmth and Old World peculiars | Dynamic VIP SMS &amp; MMS Preview">
<meta property="og:description" content="Interactive iPhone MMS &amp; SMS preview for The Chapman Collection's Autumn Warmth and Old World Peculiars campaign.">
<meta property="og:image" content="https://renderwithoutcode.com/drafts-for-pmc-approval/2026-10-27-autumn-warmth-and-old-world-peculiars/cuts/tcc-oct27-og-share-banner.jpg">
<title>Dynamic VIP SMS &amp; MMS Preview | Autumn Warmth and Old World Peculiars</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 0;
    background-color: #EFE9DF;
    font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;
    color: #1F1D1C;
  }}
  .top-bar {{
    background-color: #701D32;
    color: #F8F3EC;
    padding: 12px 20px;
    text-align: center;
    border-bottom: 2px solid #C8B68E;
    font-size: 15px;
    letter-spacing: 0.4px;
  }}
  .top-bar a {{
    color: #F8F3EC;
    text-decoration: none;
    font-weight: bold;
    border: 1px solid #C8B68E;
    padding: 5px 14px;
    border-radius: 3px;
    margin-left: 12px;
    background-color: rgba(255,255,255,0.08);
    display: inline-block;
  }}
  .top-bar a:hover {{
    background-color: rgba(255,255,255,0.18);
  }}
  .wrapper {{
    max-width: 1120px;
    margin: 26px auto 50px auto;
    padding: 0 18px;
    display: flex;
    flex-wrap: wrap;
    gap: 32px;
    align-items: flex-start;
    justify-content: center;
  }}
  /* Left Column: iPhone Mockup */
  .phone-col {{
    flex: 0 0 390px;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .mode-switcher {{
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
    background: #F8F3EC;
    padding: 6px;
    border-radius: 8px;
    border: 1px solid #C8B68E;
    width: 100%;
    justify-content: center;
  }}
  .mode-btn {{
    flex: 1;
    font-family: 'Garamond', 'Georgia', serif;
    font-size: 14px;
    font-weight: bold;
    padding: 8px 10px;
    border: 1px solid transparent;
    border-radius: 5px;
    cursor: pointer;
    background: transparent;
    color: #3D3935;
    transition: all 0.15s ease;
  }}
  .mode-btn.active {{
    background: #701D32;
    color: #FFFFFF;
    border-color: #C8B68E;
  }}
  .iphone-frame {{
    width: 375px;
    max-width: 100%;
    background: #1C1C1E;
    border-radius: 46px;
    padding: 13px;
    box-shadow: 0 18px 42px rgba(31, 29, 28, 0.25);
    border: 2px solid #4A443C;
  }}
  .iphone-screen {{
    background: #FFFFFF;
    border-radius: 35px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  .ios-statusbar {{
    padding: 12px 24px 6px 24px;
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    color: #111;
    background: #F7F7F7;
  }}
  .ios-header {{
    background: #F7F7F7;
    border-bottom: 1px solid #E5E5EA;
    padding: 6px 14px 10px 14px;
    text-align: center;
  }}
  .ios-avatar {{
    width: 42px;
    height: 42px;
    border-radius: 50%;
    margin: 0 auto 4px auto;
    background: #F8F3EC;
    border: 1px solid #C8B68E;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}
  .ios-avatar img {{
    width: 30px;
    height: auto;
  }}
  .ios-sender {{
    font-size: 13px;
    font-weight: 600;
    color: #111;
  }}
  .ios-sub {{
    font-size: 10.5px;
    color: #8E8E93;
    margin-top: 1px;
  }}
  .ios-thread {{
    padding: 14px 12px 18px 12px;
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    gap: 8px;
    max-height: 670px;
    overflow-y: auto;
  }}
  .ios-timestamp {{
    text-align: center;
    font-size: 11px;
    color: #8E8E93;
    margin-bottom: 4px;
  }}
  .mms-media-bubble {{
    width: 86%;
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #E5E5EA;
    background: #F8F3EC;
  }}
  .mms-media-bubble img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .sms-text-bubble {{
    width: 86%;
    background: #E9E9EB;
    color: #111111;
    padding: 11px 14px;
    border-radius: 18px;
    border-bottom-left-radius: 5px;
    font-size: 14px;
    line-height: 1.42;
    word-wrap: break-word;
  }}
  .sms-text-bubble a {{
    color: #701D32;
    text-decoration: underline;
    font-weight: 500;
  }}
  .og-unfurl-card {{
    width: 86%;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #E5E5EA;
    background: #F2F2F7;
    text-decoration: none;
    color: inherit;
    display: block;
    margin-top: 2px;
  }}
  .og-unfurl-card img {{
    width: 100%;
    height: auto;
    display: block;
  }}
  .og-unfurl-meta {{
    padding: 9px 12px 11px 12px;
  }}
  .og-domain {{
    font-size: 10.5px;
    text-transform: uppercase;
    color: #8E8E93;
    letter-spacing: 0.3px;
    margin-bottom: 2px;
  }}
  .og-title {{
    font-size: 13px;
    font-weight: 600;
    color: #111;
    line-height: 1.28;
    margin-bottom: 2px;
  }}
  .og-desc {{
    font-size: 11.5px;
    color: #636366;
    line-height: 1.32;
  }}
  .ios-inputbar {{
    padding: 9px 14px 14px 14px;
    background: #F7F7F7;
    border-top: 1px solid #E5E5EA;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .ios-pill {{
    flex: 1;
    border: 1px solid #C7C7CC;
    background: #FFFFFF;
    border-radius: 18px;
    padding: 7px 14px;
    font-size: 13px;
    color: #8E8E93;
  }}

  /* Right Column: Controls & Copy */
  .details-col {{
    flex: 1 1 560px;
    background: #F8F3EC;
    border: 1.5px solid #B7A486;
    border-top: 4px solid #701D32;
    border-bottom: 4px solid #701D32;
    padding: 26px 28px;
  }}
  .details-col h1 {{
    margin: 0 0 6px 0;
    font-size: 26px;
    color: #701D32;
    font-weight: normal;
    font-style: italic;
  }}
  .details-col .subhead {{
    margin: 0 0 18px 0;
    font-size: 15.5px;
    color: #3D3935;
    line-height: 1.5;
    border-bottom: 1px solid #D5C7B2;
    padding-bottom: 14px;
  }}
  .dynamic-tester {{
    background: #EFE9DF;
    border: 1px solid #C8B68E;
    padding: 14px 16px;
    border-radius: 4px;
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
  }}
  .dynamic-tester label {{
    font-size: 15px;
    font-weight: bold;
    color: #701D32;
  }}
  .dynamic-tester input {{
    font-family: 'Garamond', 'Georgia', serif;
    font-size: 16px;
    padding: 6px 12px;
    border: 1px solid #B7A486;
    border-radius: 3px;
    background: #FFFFFF;
    color: #1F1D1C;
    width: 190px;
  }}
  .card-box {{
    border: 1px solid #C8B68E;
    background: #FFFFFF;
    padding: 16px 18px;
    margin-bottom: 18px;
  }}
  .card-box h3 {{
    margin: 0 0 8px 0;
    font-size: 18px;
    color: #701D32;
  }}
  .code-block {{
    font-family: Consolas, Monaco, monospace;
    font-size: 12.5px;
    line-height: 1.55;
    background: #F8F3EC;
    border: 1px solid #D5C7B2;
    padding: 12px;
    color: #1F1D1C;
    white-space: pre-wrap;
    margin-bottom: 10px;
  }}
  .btn-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 8px;
  }}
  .btn {{
    display: inline-block;
    background: #701D32;
    color: #FFFFFF;
    text-decoration: none;
    padding: 9px 16px;
    font-family: 'Garamond', 'Georgia', serif;
    font-size: 15px;
    border: 1px solid #C5A059;
    border-radius: 2px;
    cursor: pointer;
  }}
  .btn.secondary {{
    background: #F8F3EC;
    color: #701D32;
    border: 1px solid #701D32;
    font-weight: bold;
  }}
</style>
</head>
<body>

<div class="top-bar">
  THE CHAPMAN COLLECTION  •  Dynamic VIP SMS &amp; MMS Preview Suite
  <a href="{circular_href}">View Full Email Circular &rarr;</a>
</div>

<div class="wrapper">
  <!-- LEFT COLUMN: LIVE IPHONE SIMULATOR -->
  <div class="phone-col">
    <div class="mode-switcher">
      <button class="mode-btn active" id="btn-gif" onclick="setMediaMode('gif')">Animated MMS (.GIF)</button>
      <button class="mode-btn" id="btn-jpg" onclick="setMediaMode('jpg')">Static Bento Card (.JPG)</button>
    </div>

    <div class="iphone-frame">
      <div class="iphone-screen">
        <div class="ios-statusbar">
          <span>10:45</span>
          <span>5G • 100%</span>
        </div>
        <div class="ios-header">
          <div class="ios-avatar">
            <img src="{cuts_prefix}tcc-oct23-crest.png" alt="The Chapman Collection">
          </div>
          <div class="ios-sender">The Chapman Collection &rsaquo;</div>
          <div class="ios-sub">Verified Toll-Free VIP Concierge</div>
        </div>

        <div class="ios-thread">
          <div class="ios-timestamp">Today 10:45 AM</div>

          <!-- MMS Visual Compilation Bubble -->
          <div class="mms-media-bubble">
            <img id="mms-preview-img" src="{cuts_prefix}tcc-oct27-mms-dynamic-showcase.gif" alt="Autumn Warmth and Old World Peculiars MMS Compilation">
          </div>

          <!-- Dynamic Personalized SMS Text Bubble -->
          <div class="sms-text-bubble" id="live-sms-bubble">
            Hi <span id="preview-fname">Victoria</span>, a quick look at four newly arrived Old World antique-door cabinets, a framed Knight Templar sword, a 75&Prime; carved mirror and a Persian silk runner just added at The Chapman Collection. Tap below to browse, or reply if you would like photos or an in-home trial:<br><br>
            <a href="{circular_href}">https://thechapmancollection.com/furniture/cabinets/</a><br><br>
            Warmly, Melissa<br>
            <span style="font-size: 11.5px; color: #636366;">Reply STOP to opt out</span>
          </div>

          <!-- Rich Link Preview Card (OpenGraph Unfurl) -->
          <a class="og-unfurl-card" href="{circular_href}">
            <img src="{cuts_prefix}tcc-oct27-og-share-banner.jpg" alt="OpenGraph Link Preview">
            <div class="og-unfurl-meta">
              <div class="og-domain">thechapmancollection.com</div>
              <div class="og-title">Autumn warmth and Old World peculiars | The Chapman Collection</div>
              <div class="og-desc">Four newly arrived Old World antique-door cabinets, Knight Templar sword, 75¾″ carved mirror and Persian silk Qum runner.</div>
            </div>
          </a>
        </div>

        <div class="ios-inputbar">
          <div class="ios-pill">Text Message • SMS</div>
        </div>
      </div>
    </div>
  </div>

  <!-- RIGHT COLUMN: DYNAMIC CONTROLS, OMNISEND MERGE COPY & DOWNLOADS -->
  <div class="details-col">
    <h1>Dynamic VIP SMS and MMS Companion Drop</h1>
    <p class="subhead">
      Designed for your <strong>225 carrier-verified VIP mobile numbers</strong> on Omnisend. Combines a muted-parchment visual compilation card (just like Melissa requested during our showroom session) with dynamic first-name personalization and direct tap-through links.
    </p>

    <div class="dynamic-tester">
      <label for="fname-input">Test Dynamic First Name (<code>[[contact.first_name]]</code>):</label>
      <input type="text" id="fname-input" value="Victoria" oninput="updateFirstName(this.value)" placeholder="Enter client name...">
      <button class="btn secondary" onclick="document.getElementById('fname-input').value='there';updateFirstName('there');">Test Fallback ("there")</button>
    </div>

    <div class="card-box">
      <h3>Option 1: VIP Visual MMS + Dynamic Personalization (Recommended)</h3>
      <p style="margin: 0 0 8px 0; font-size: 15px; color: #3D3935;">
        Pairs the 6-piece muted-parchment compilation image (or 5-slide animated GIF) with a warm, concise note in Melissa's voice (zero em-dashes, no Oxford comma):
      </p>
      <div class="code-block" id="omnisend-copy-1">Hi [[contact.first_name | default: 'there']], a quick look at four newly arrived Old World antique-door cabinets, a framed Knight Templar sword, a 75" carved mirror and a Persian silk runner just added at The Chapman Collection. Tap below to browse, or reply if you would like photos or an in-home trial:

https://thechapmancollection.com/product-category/furniture/cabinets/

Warmly, Melissa
Reply STOP to opt out</div>
      <div class="btn-row">
        <button class="btn" onclick="copyText('omnisend-copy-1', this)">Copy Omnisend MMS Text</button>
        <a class="btn secondary" href="{cuts_prefix}tcc-oct27-mms-dynamic-showcase.gif" download>Download Animated MMS (.GIF • 406 KB)</a>
        <a class="btn secondary" href="{cuts_prefix}tcc-oct27-mms-compilation-card.jpg" download>Download Static Bento Card (.JPG)</a>
      </div>
    </div>

    <div class="card-box">
      <h3>Option 2: Ultra-Short VIP Text Linking to the Full Circular</h3>
      <p style="margin: 0 0 8px 0; font-size: 15px; color: #3D3935;">
        Sends a crisp two-sentence text whose link automatically unfurls into the rich 4-item preview banner on iMessage and Google Messages:
      </p>
      <div class="code-block" id="omnisend-copy-2">Hi [[contact.first_name | default: 'there']], we just shared our new autumn circular featuring four Old World antique-door cabinets, a framed Knight Templar sword, a 75" carved mirror and a Persian silk Qum runner. Take a look here or reply if anything catches your eye:

https://renderwithoutcode.com/drafts-for-pmc-approval/autumn-warmth-and-old-world-peculiars.html

Warmly, Melissa
Reply STOP to opt out</div>
      <div class="btn-row">
        <button class="btn" onclick="copyText('omnisend-copy-2', this)">Copy Short Circular SMS</button>
        <a class="btn secondary" href="{circular_href}">Open Full HTML Circular &rarr;</a>
      </div>
    </div>
  </div>
</div>

<script>
  const cutsPrefix = "{cuts_prefix}";
  function setMediaMode(mode) {{
    const img = document.getElementById('mms-preview-img');
    const btnGif = document.getElementById('btn-gif');
    const btnJpg = document.getElementById('btn-jpg');
    if (mode === 'gif') {{
      img.src = cutsPrefix + 'tcc-oct27-mms-dynamic-showcase.gif';
      btnGif.classList.add('active');
      btnJpg.classList.remove('active');
    }} else {{
      img.src = cutsPrefix + 'tcc-oct27-mms-compilation-card.jpg';
      btnJpg.classList.add('active');
      btnGif.classList.remove('active');
    }}
  }}
  function updateFirstName(val) {{
    const clean = (val && val.trim().length > 0) ? val.trim() : 'there';
    document.getElementById('preview-fname').textContent = clean;
  }}
  function copyText(id, btn) {{
    const txt = document.getElementById(id).innerText;
    navigator.clipboard.writeText(txt).then(() => {{
      const orig = btn.textContent;
      btn.textContent = 'Copied to Clipboard!';
      setTimeout(() => {{ btn.textContent = orig; }}, 1800);
    }});
  }}
</script>
</body>
</html>
"""

# Write subfolder SMS preview HTML
sub_sms_html = build_sms_html("cuts/", "autumn-warmth-and-old-world-peculiars.html")
for p in [
    os.path.join(NRL_SUB, "sms-autumn-warmth-and-old-world-peculiars.html"),
    os.path.join(BASE_CAMPAIGN_DIR, "2026-10-27-SMS_MMS_Dynamic_Preview_Autumn_Warmth.html"),
    os.path.join(BASE_CAMPAIGN_DIR, "drafts", "2026-10-27-SMS_MMS_Dynamic_Preview_Autumn_Warmth.html"),
]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(sub_sms_html)
    print("Wrote:", p)

# Write root SMS preview HTML
root_sms_html = build_sms_html(
    "2026-10-27-autumn-warmth-and-old-world-peculiars/cuts/",
    "autumn-warmth-and-old-world-peculiars.html"
)
root_sms_path = os.path.join(NRL_ROOT, "sms-autumn-warmth-and-old-world-peculiars.html")
with open(root_sms_path, "w", encoding="utf-8") as f:
    f.write(root_sms_html)
print("Wrote:", root_sms_path)
