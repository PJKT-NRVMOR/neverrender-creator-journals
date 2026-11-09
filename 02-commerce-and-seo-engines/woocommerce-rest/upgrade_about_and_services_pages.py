#!/usr/bin/env python3
"""
Upgrade https://thechapmancollection.com/services/ (Page ID 12),
https://thechapmancollection.com/about-us/ (Page ID 10), and the sitewide
Beaver Builder Header (ID 203) & Footer (ID 24) to the enshrined
Chaphavian Editorial Architecture (#F7F5F2 Alabaster, #D5D3CC Putty,
#8A8F97 Slate, #B35A5E Rose, #2B2F32 Iron, Cormorant Garamond + Montserrat).

Updates in v1.2 (2026-11-07 05:40 PST):
1. Hides the ugly thick cartoon phone receiver icon in the top header bar (.fl-node-vh40jnmt5opx .pp-icon-wrapper,
   .fl-node-xeirb431vmsj .pp-icon-wrapper, .fl-node-15igb2qrhzxt .pp-icon-wrapper) and styles `(858) 349-2638`
   as a clean Chaphavian editorial pill link matching the top navigation.
2. Removes the 3 jump buttons from the top "Explore Our Services at The Chapman Collection" hero card on `/services/`.
3. Matches our local `chapman-curatorial-gallery-search` About Us page 1:1:
   - Exact rose-tinted drop shadow & hover elevation (`0 10px 26px -10px rgba(179, 90, 94, 0.16)` ->
     `0 22px 44px -8px rgba(179, 90, 94, 0.34), 0 0 0 1px rgba(179, 90, 94, 0.28)`).
   - Zero balloon/zoom scale effect on photos (`transform: none !important` on `.nrl-framed-photo img`) and crisp
     1px border frame without thick inner matting.
   - Ghost-to-Dark Iron buttons (`#F7F5F2` Alabaster default -> `#2B2F32` Dark Iron on hover) in `Cormorant Garamond`.
"""

import os
import sys
import json
import base64
import urllib.request
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(r"c:\Users\Saturn\Desktop\project-marshall-college\.env")

WP_BASE = "https://thechapmancollection.com/wp-json"
USER = os.getenv("WP_REST_USER", "neverrender-labs")
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")

SHOWROOM_LOCAL_PATH = (
    r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE"
    r"\drafts-for-pmc-approval\chapman-curatorial-gallery-search\assets\showroom-6014-la-granada.jpg"
)
WELCOME_ALCOVE_LOCAL_PATH = (
    r"C:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE"
    r"\drafts-for-pmc-approval\homepage-refresh-preview\a-chaphavian-welcome-alcove.jpg"
)


def api_request(url, method="GET", data=None, raw_bytes=None, content_type="application/json", extra_headers=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "NRL-Chaphavian-Page-Upgrader/1.2",
        "Content-Type": content_type,
    }
    if extra_headers:
        headers.update(extra_headers)
    if raw_bytes is not None:
        body = raw_bytes
    elif data is not None:
        body = json.dumps(data).encode("utf-8")
    else:
        body = None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}


def ensure_showroom_photo_uploaded():
    search_url = f"{WP_BASE}/wp/v2/media?search=chapman-collection-showroom-6014-la-granada-rsf&per_page=5"
    existing = api_request(search_url)
    if existing and isinstance(existing, list) and len(existing) > 0:
        url = existing[0].get("source_url")
        print(f"[MEDIA] Found existing 6014 La Granada showroom photo: {url}")
        return url

    with open(SHOWROOM_LOCAL_PATH, "rb") as f:
        img_bytes = f.read()

    res = api_request(
        f"{WP_BASE}/wp/v2/media",
        method="POST",
        raw_bytes=img_bytes,
        content_type="image/jpeg",
        extra_headers={
            "Content-Disposition": 'attachment; filename="chapman-collection-showroom-6014-la-granada-rsf.jpg"'
        },
    )
    url = res.get("source_url")
    media_id = res.get("id")
    if media_id:
        api_request(
            f"{WP_BASE}/wp/v2/media/{media_id}",
            method="POST",
            data={
                "alt_text": "The Chapman Collection Showroom at 6014 La Granada, Rancho Santa Fe, CA",
                "title": "The Chapman Collection Showroom at 6014 La Granada, Rancho Santa Fe",
            },
        )
    print(f"[MEDIA] Uploaded 6014 La Granada showroom photo (ID {media_id}): {url}")
    return url


def ensure_welcome_alcove_uploaded():
    search_url = f"{WP_BASE}/wp/v2/media?search=a-chaphavian-welcome-alcove&per_page=5"
    existing = api_request(search_url)
    if existing and isinstance(existing, list) and len(existing) > 0:
        url = existing[0].get("source_url")
        print(f"[MEDIA] Found existing Chaphavian Welcome Alcove hero photo: {url}")
        return url

    with open(WELCOME_ALCOVE_LOCAL_PATH, "rb") as f:
        img_bytes = f.read()

    res = api_request(
        f"{WP_BASE}/wp/v2/media",
        method="POST",
        raw_bytes=img_bytes,
        content_type="image/jpeg",
        extra_headers={
            "Content-Disposition": 'attachment; filename="a-chaphavian-welcome-alcove.jpg"'
        },
    )
    url = res.get("source_url")
    media_id = res.get("id")
    if media_id:
        api_request(
            f"{WP_BASE}/wp/v2/media/{media_id}",
            method="POST",
            data={
                "alt_text": "The Chapman Collection Digital Gallery - Polychrome Carved Marble Statue in Chaphavian Plaster Alcove",
                "title": "The Chapman Collection - A Chaphavian Welcome",
            },
        )
    print(f"[MEDIA] Uploaded Chaphavian Welcome Alcove hero photo (ID {media_id}): {url}")
    return url


def build_about_us_html(showroom_img_url):
    portrait_url = "https://thechapmancollection.com/wp-content/uploads/2026/11/melissa-chapman-the-hero-nrl-graded-2026-11-07-15.58.30-Cr-1.jpg"

    return f"""
<div class="nrl-chaphavian-stage">
  <div class="nrl-chaphavian-container">

    <!-- Main Split Editorial Hero (True 1fr / 1fr 4-Corner Cross Intersection Symmetry with Lower Grid) -->
    <div class="nrl-melissa-hero-split">

      <!-- Left Column: Singular Ranch and Coast Portrait Card + Credit + Explore the Gallery CTA -->
      <div class="nrl-hover-box nrl-portrait-card">
        <div class="nrl-portrait-top">
          <div class="nrl-framed-photo nrl-portrait-frame">
            <img src="{portrait_url}" alt="Melissa Chapman in The Chapman Collection Rancho Santa Fe Showroom" loading="eager" fetchpriority="high" />
          </div>
          <div class="nrl-portrait-caption">
            Melissa Chapman &middot; Photo courtesy of Ranch and Coast Magazine
          </div>
        </div>

        <div class="nrl-portrait-cta-bar">
          <a href="https://thechapmancollection.com/shop/" class="nrl-search-trigger nrl-btn-full">Explore the Gallery</a>
        </div>
      </div>

      <!-- Right Column: Melissa's Verbatim Approved 6-Paragraph Bio -->
      <div class="nrl-bio-column">
        <div class="nrl-bio-copy">
          <div class="nrl-kicker" style="margin-bottom:14px;">
            From Harrington Road in London to Rancho Santa Fe, California
          </div>

          <p>
            Melissa Chapman is an experienced antiques and Persian carpet dealer whose lifelong passion began in her family&rsquo;s Persian carpet stores. At just 19, she opened her first shop on Harrington Road in London, specializing in fine Persian carpets alongside a carefully curated selection of antiques.
          </p>

          <p>
            As Melissa&rsquo;s discerning eye and love for timeless design grew, so did her business. She began importing full containers of antique and fine European furniture, establishing herself as a distinguished antiques dealer with an exceptional collection of Persian rugs.
          </p>

          <p>
            Over the years, Melissa has opened several successful locations in London and San Diego, building a loyal and prestigious clientele that includes celebrities, politicians and even royalty.
          </p>

          <p>
            Today, she runs The Chapman Collection from her elegant showroom in Rancho Santa Fe, California, offering exceptional pieces selected for their history, craftsmanship and beauty, all at remarkable value.
          </p>

          <p>
            The Collection brings together classical European antiques, Old World furnishings, tapestries, artwork, decorative accessories and an extraordinary selection of Persian carpets. Whether you are seeking a statement piece or a subtle accent, there is something special to discover.
          </p>

          <p class="nrl-last-bio-p">
            Beyond the showroom, Melissa is a devoted single mother to two wonderful sons, with two much-loved dogs completing the family. She also helps manage her family&rsquo;s International Real Estate Portfolio, bringing the same dedication and attention to detail to every aspect of her life.
          </p>
        </div>

        <!-- Signature Block (Flush with Left Portrait Card Bottom Edge) -->
        <div class="nrl-signature-block">
          <div class="nrl-signature-script">
            Warm regards, Melissa Chapman
          </div>
          <div class="nrl-signature-title">
            Founder and Principal Curator &middot; The Chapman Collection
          </div>
        </div>
      </div>

    </div>

    <!-- Lower Band: The Rancho Santa Fe Showroom & White-Glove Shipping / In-Home Trial Architecture -->
    <div class="nrl-melissa-lower-grid">

      <!-- Card 1: 6014 La Granada Showroom in the Heart of the Village -->
      <div class="nrl-hover-box nrl-lower-card">
        <div>
          <div class="nrl-framed-photo nrl-showroom-frame">
            <img src="{showroom_img_url}" alt="The Chapman Collection Showroom at 6014 La Granada, Rancho Santa Fe" loading="lazy" />
          </div>
          <div class="nrl-kicker">
            Rancho Santa Fe Village &middot; 6014 La Granada, Rancho Santa Fe, CA 92067
          </div>
          <h3 class="nrl-card-h2">
            Visit Our Rancho Santa Fe Showroom
          </h3>
          <p class="nrl-card-body">
            Located at the corner of La Granada and Paseo Delicias in the heart of the Rancho Santa Fe Village, our gallery welcomes collectors and interior designers seven days a week, Monday through Saturday from 10:00 AM to 6:00 PM and Sundays from 11:00 AM to 4:00 PM. Explore our curated rooms of European antiques, Old World furnishings, fine art and hand-knotted Persian carpets in person.
          </p>
        </div>
        <div class="nrl-card-footer-meta">
          Recognized in Ranch and Coast Magazine &middot; Private Designer Appointments Available
        </div>
      </div>

      <!-- Card 2: White-Glove Shipping Partners & Trade Concierge -->
      <div class="nrl-hover-box nrl-lower-card">
        <div>
          <div class="nrl-kicker">
            Domestic and International Fine-Art Logistics
          </div>
          <h3 class="nrl-card-h2">
            White-Glove Shipping and Carrier Coordination
          </h3>
          <p class="nrl-card-body">
            Because Melissa has imported full containers of European antiques and palace-sized carpets for over thirty years, every acquisition outside Southern California is handled with museum-grade care. Our preferred shipping partners offer professional packing, insurance options and worldwide shipping.
          </p>
          <div class="nrl-linen-callout">
            <div class="nrl-linen-callout-title">
              Three Effortless Fulfillment Pathways
            </div>
            <ul class="nrl-fulfillment-list">
              <li><strong>1. Accessories, Artwork and Carpets:</strong> Professional packing and insured shipping via The UPS Store #0400 in San Diego (858-453-7331).</li>
              <li><strong>2. Large Furniture, Accessories, Artwork and Carpets:</strong> White-glove crating and freight via Beejan Hamraz at Navis Pack &amp; Ship #25006CA (858-256-0103).</li>
              <li><strong>3. International Container Shipping:</strong> Worldwide half-container and full 40-foot container loads arranged directly with Melissa.</li>
            </ul>
          </div>
        </div>

        <div class="nrl-card-footer-cta">
          <div class="nrl-card-footer-italic">
            Request a shipping quote or private showroom appointment directly with Melissa.
          </div>
          <div class="nrl-card-footer-btns">
            <a href="https://thechapmancollection.com/services/#shipping-and-delivery" class="nrl-reset-trigger">Preferred Shippers</a>
            <a href="mailto:info@thechapmancollection.com?subject=Showroom%20%26%20Shipping%20Inquiry%20-%20The%20Chapman%20Collection" class="nrl-search-trigger">Email Showroom</a>
          </div>
        </div>
      </div>

    </div>

  </div>
</div>
""".strip()


def build_services_html():
    restoration_img_url = "https://thechapmancollection.com/wp-content/uploads/2026/10/GoDaddy_-5844-scaled.jpg"

    return f"""
<div class="nrl-chaphavian-stage">
  <div class="nrl-chaphavian-container">

    <!-- Top Editorial Intro Banner (Clean — Zero Redundant Buttons) -->
    <div class="nrl-hover-box nrl-services-hero-card">
      <div class="nrl-kicker">
        Rancho Santa Fe Showroom Concierge &middot; Worldwide Logistics and Conservation
      </div>
      <h1 class="nrl-page-h1" style="margin-bottom:10px;">
        Explore Our Services at The Chapman Collection
      </h1>
      <p class="nrl-services-lead" style="margin-bottom:0;">
        From private showroom consultations and white-glove local delivery across Southern California to domestic crating, international container freight and master conservation, we ensure every piece arrives and endures with timeless beauty.
      </p>
    </div>

    <!-- SECTION 1: SHIPPING AND DELIVERY + PREFERRED SHIPPING PARTNERS -->
    <section id="shipping-and-delivery" class="nrl-service-anchor-section">
      <div class="nrl-hover-box nrl-shipping-master-card">
        <div class="nrl-shipping-header-block">
          <div class="nrl-kicker">
            Worldwide White-Glove Delivery &middot; Preferred Shipping Partners
          </div>
          <h2 class="nrl-section-h2">
            Shipping and Delivery
          </h2>
          <p class="nrl-card-body" style="max-width:900px;">
            The Chapman Collection provides international, national and local delivery for your pieces. Let our specialists take care of all the logistics for you. All pieces go professionally packed and insured by reputable freight-forwarding companies. We can also arrange a White Glove Service, which includes full delivery and installation.
          </p>
          <p class="nrl-card-body" style="max-width:900px; margin-bottom:0; font-weight:600;">
            Our preferred shipping partners offer professional packing, insurance options and worldwide shipping. Please contact them directly for a quote.
          </p>
        </div>

        <!-- 3-Column Preferred Shipping Partners Grid (Verbatim from Melissa's Nov 6, 2026 Email) -->
        <div class="nrl-shippers-grid">

          <!-- Partner 1: The UPS Store #0400 -->
          <div class="nrl-hover-box nrl-shipper-card">
            <div>
              <div class="nrl-shipper-badge">
                Accessories, Artwork and Carpets
              </div>
              <h3 class="nrl-shipper-name">
                The UPS Store #0400
              </h3>
              <div class="nrl-shipper-contact-person">
                San Diego Fine Packing &amp; Parcel Specialist
              </div>
              <div class="nrl-shipper-details">
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Address</span>
                  <span>7770 Regents Road, Suite 113<br>San Diego, CA 92122</span>
                </div>
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Phone &amp; Fax</span>
                  <span><a href="tel:+18584537331">858-453-7331</a> &middot; Fax 858-453-7335</span>
                </div>
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Website</span>
                  <a href="https://www.theupsstore.com/0400" target="_blank" rel="noopener">Visit The UPS Store #0400</a>
                </div>
              </div>
            </div>
            <div class="nrl-shipper-actions">
              <a href="tel:+18584537331" class="nrl-search-trigger nrl-btn-sm">Call 858-453-7331</a>
              <a href="https://www.theupsstore.com/0400" target="_blank" rel="noopener" class="nrl-reset-trigger nrl-btn-sm">Visit The UPS Store</a>
            </div>
          </div>

          <!-- Partner 2: Navis Pack & Ship #25006CA -->
          <div class="nrl-hover-box nrl-shipper-card">
            <div>
              <div class="nrl-shipper-badge">
                Large Furniture, Accessories, Artwork and Carpets
              </div>
              <h3 class="nrl-shipper-name">
                Navis Pack &amp; Ship #25006CA
              </h3>
              <div class="nrl-shipper-contact-person">
                Contact <strong>Beejan Hamraz</strong>
              </div>
              <div class="nrl-shipper-details">
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Address</span>
                  <span>7716 Clairemont Mesa Blvd.<br>San Diego, CA 92111</span>
                </div>
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Phone</span>
                  <a href="tel:+18582560103">858-256-0103</a>
                </div>
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Email</span>
                  <a href="mailto:CA25006@goNavis.com">CA25006@goNavis.com</a>
                </div>
              </div>
            </div>
            <div class="nrl-shipper-actions">
              <a href="tel:+18582560103" class="nrl-search-trigger nrl-btn-sm">Call 858-256-0103</a>
              <a href="mailto:CA25006@goNavis.com?subject=Shipping%20Quote%20Request%20-%20The%20Chapman%20Collection" class="nrl-reset-trigger nrl-btn-sm">Email Beejan</a>
            </div>
          </div>

          <!-- Partner 3: International Container Shipping -->
          <div class="nrl-hover-box nrl-shipper-card">
            <div>
              <div class="nrl-shipper-badge">
                International Container Shipping
              </div>
              <h3 class="nrl-shipper-name">
                Worldwide Container Loads
              </h3>
              <div class="nrl-shipper-contact-person">
                Direct Coordination: <strong>Melissa Chapman</strong>
              </div>
              <div class="nrl-shipper-details">
                <p class="nrl-container-copy">
                  The Chapman Collection can arrange worldwide shipping for half-container or full 40-foot container loads. For a quote, please contact Melissa directly.
                </p>
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Showroom Phone</span>
                  <a href="tel:+18583492638">(858) 349-2638</a>
                </div>
                <div class="nrl-shipper-row">
                  <span class="nrl-shipper-label">Email</span>
                  <a href="mailto:info@thechapmancollection.com">info@thechapmancollection.com</a>
                </div>
              </div>
            </div>
            <div class="nrl-shipper-actions">
              <a href="tel:+18583492638" class="nrl-search-trigger nrl-btn-sm">Call (858) 349-2638</a>
              <a href="mailto:info@thechapmancollection.com?subject=International%20Container%20Shipping%20Quote" class="nrl-reset-trigger nrl-btn-sm">Email Showroom</a>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- SECTION 2: INTERIOR DESIGN SERVICES & COMPLIMENTARY IN-HOME PLACEMENT TRIALS -->
    <section id="interior-design-services" class="nrl-service-anchor-section">
      <div class="nrl-melissa-lower-grid">

        <!-- Left Card: Interior Design Services -->
        <div class="nrl-hover-box nrl-lower-card">
          <div>
            <div class="nrl-kicker">
              Trade Concierge &middot; Designer Partnerships
            </div>
            <h2 class="nrl-card-h2">
              Interior Design Services
            </h2>
            <p class="nrl-card-body">
              The Chapman Collection loves working alongside designers! We know how hard they work to make their clients&rsquo; homes beautiful, so we try to be as helpful as we can.
            </p>
            <p class="nrl-card-body">
              We have an excellent response time, and we can deliver and install any items for our designer clients. We are always looking for additional designers to work with, and we do offer courtesy to the trade.
            </p>
            <p class="nrl-card-body" style="margin-bottom:0;">
              If you are interested in working with The Chapman Collection, please contact us directly for private showroom appointments or tear-sheet specifications.
            </p>
          </div>
          <div class="nrl-card-footer-cta" style="margin-top:24px;">
            <div class="nrl-card-footer-italic">
              Courtesy to the trade and prompt installation across Southern California.
            </div>
            <div class="nrl-card-footer-btns">
              <a href="https://thechapmancollection.com/contact-us/" class="nrl-search-trigger">Contact Us</a>
            </div>
          </div>
        </div>

        <!-- Right Card: Private Showroom Consultations & White-Glove Local Delivery -->
        <div class="nrl-hover-box nrl-lower-card">
          <div>
            <div class="nrl-kicker">
              Rancho Santa Fe &middot; Del Mar &middot; La Jolla &middot; Coastal San Diego
            </div>
            <h2 class="nrl-card-h2">
              Private Showroom Appointments and Local Delivery
            </h2>
            <p class="nrl-card-body">
              Whether you are furnishing an entire residence or searching for a singular period piece, Melissa and her showroom team provide personal curatorial guidance at our Rancho Santa Fe Village gallery.
            </p>
            <p class="nrl-card-body" style="margin-bottom:0;">
              We coordinate full White Glove delivery and careful placement across Rancho Santa Fe, Del Mar, La Jolla and Southern California so every carpet, artwork and antique arrives ready to enjoy in your home.
            </p>
          </div>
          <div class="nrl-card-footer-cta" style="margin-top:24px;">
            <div class="nrl-card-footer-italic">
              Call Melissa directly at (858) 349-2638 for private appointments or delivery inquiries.
            </div>
            <div class="nrl-card-footer-btns">
              <a href="https://thechapmancollection.com/contact-us/" class="nrl-search-trigger">Contact Us</a>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- SECTION 3: ANTIQUE FURNITURE AND CARPET RESTORATION -->
    <section id="antique-furniture-and-carpet-restoration" class="nrl-service-anchor-section">
      <div class="nrl-hover-box nrl-restoration-split-card">

        <div class="nrl-restoration-copy-col">
          <div>
            <div class="nrl-kicker">
              Three Decades of Master Conservation &middot; San Diego and Rancho Santa Fe
            </div>
            <h2 class="nrl-section-h2">
              Antique Furniture and Carpet Restoration
            </h2>
            <p class="nrl-card-body">
              The Chapman Collection works with an extremely talented San Diego furniture restorer who has been bringing fine antique furniture back to life for the past three decades. He is very reasonable, easy to work with and will come to your home or office to repair your pieces on the spot. Please contact us for details.
            </p>
            <p class="nrl-card-body">
              We also offer professional hand-knotted carpet repair and museum-grade cleaning services. Simply email us a photo of your carpet, along with the measurements and details, and we will gladly email you back a quote.
            </p>
          </div>

          <div class="nrl-restoration-cta-row">
            <a href="https://thechapmancollection.com/contact-us/" class="nrl-search-trigger">Contact Us</a>
          </div>
        </div>

        <div class="nrl-restoration-photo-col">
          <div class="nrl-framed-photo nrl-restoration-frame">
            <img src="{restoration_img_url}" alt="Fine Antique Furniture, Giltwood Frames and Bronze Sculpture at The Chapman Collection" loading="lazy" />
          </div>
        </div>

      </div>
    </section>

  </div>
</div>
""".strip()


def build_contact_us_html(showroom_img_url):
    return f"""
<div class="nrl-chaphavian-stage">
  <div class="nrl-chaphavian-container">

    <!-- ROW 1: SPLIT CHAPHAVIAN CONTACT CONCIERGE & DIRECT INQUIRY FORM -->
    <div class="nrl-melissa-hero-split" style="margin-bottom:32px;">

      <!-- Left Card: Showroom Contact Ledger & Framed 6014 La Granada Photograph -->
      <div class="nrl-hover-box nrl-lower-card">
        <div>
          <div class="nrl-kicker">
            Rancho Santa Fe Village &middot; Open Seven Days a Week
          </div>
          <h1 class="nrl-page-h1" style="margin-bottom:12px;">
            Get in Touch With Us for <em class="nrl-em-accent">Beautiful Antiques and Furniture</em>
          </h1>
          <div style="width:52px;height:2px;background-color:#B35A5E;margin:0 0 16px 0;"></div>
          <p class="nrl-card-body">
            Whether you are inquiring about a specific piece in our online gallery, arranging domestic or international delivery or planning a visit to our Rancho Santa Fe Village showroom, we would be delighted to assist you.
          </p>

          <div class="nrl-linen-callout" style="margin-bottom:22px;">
            <div class="nrl-linen-callout-title">
              Showroom &amp; Direct Concierge
            </div>
            <ul class="nrl-fulfillment-list">
              <li><strong>Showroom Address:</strong> <a href="https://maps.app.goo.gl/rqF7BedXYD9D87EJ6" target="_blank" rel="noopener" style="color:#2B2F32;text-decoration:underline;text-decoration-color:#B35A5E;">6014 La Granada, Rancho Santa Fe, CA 92067</a></li>
              <li><strong>Direct Phone &amp; Text:</strong> <a href="tel:+18583492638" style="color:#2B2F32;text-decoration:underline;text-decoration-color:#B35A5E;">(858) 349-2638</a></li>
              <li><strong>Email:</strong> <a href="mailto:info@thechapmancollection.com" style="color:#2B2F32;text-decoration:underline;text-decoration-color:#B35A5E;">info@thechapmancollection.com</a></li>
              <li><strong>Showroom Hours:</strong> Mon - Sat: 10:00 AM - 6:00 PM &middot; Sun: 11:00 AM - 4:00 PM</li>
            </ul>
          </div>

          <div class="nrl-framed-photo nrl-showroom-frame" style="margin-bottom:10px;">
            <img src="{showroom_img_url}" alt="The Chapman Collection Showroom at 6014 La Granada, Rancho Santa Fe" loading="eager" />
          </div>
          <div class="nrl-portrait-caption" style="margin-bottom:0;">
            The Chapman Collection &middot; Corner of La Granada and Paseo Delicias, Rancho Santa Fe Village
          </div>
        </div>
      </div>

      <!-- Right Card: Live Gravity Form #1 Styled in Chaphavian Alabaster & Putty -->
      <div class="nrl-hover-box nrl-lower-card nrl-contact-form-card" style="display:flex;flex-direction:column;justify-content:space-between;">
        <div style="display:flex;flex-direction:column;flex:1;justify-content:space-between;">
          <div>
            <div class="nrl-kicker">
              Private Client &amp; Interior Designer Inquiries
            </div>
            <h2 class="nrl-card-h2" style="margin-bottom:10px;">
              Send Us a <em class="nrl-em-accent" style="font-size:27px;">Direct Message</em>
            </h2>
            <p class="nrl-card-body" style="margin-bottom:20px;">
              Complete the form below and Melissa or a member of our showroom team will respond promptly. For immediate assistance, call or text <a href="tel:+18583492638" style="color:#2B2F32;font-weight:600;text-decoration:underline;text-decoration-color:#B35A5E;">(858) 349-2638</a>.
            </p>
          </div>
          <div class="nrl-chaphavian-gform-wrap" style="display:flex;flex-direction:column;flex:1;justify-content:space-between;">
            __GRAVITY_FORM_1__
          </div>
        </div>
      </div>

    </div>

    <!-- ROW 2: WORKING INTERACTIVE GOOGLE MAP OF 6014 LA GRANADA, RANCHO SANTA FE -->
    <div class="nrl-hover-box nrl-shipping-master-card">
      <div class="nrl-contact-map-header">
        <div>
          <div class="nrl-kicker">
            In the Heart of the Rancho Santa Fe Village &middot; Corner of La Granada &amp; Paseo Delicias
          </div>
          <h2 class="nrl-section-h2" style="margin-bottom:6px;">
            Visit Our <em class="nrl-em-accent">Rancho Santa Fe Showroom</em>
          </h2>
          <p class="nrl-card-body" style="margin-bottom:0;">
            6014 La Granada, Rancho Santa Fe, CA 92067 &middot; Convenient Village parking directly outside our showroom doors.
          </p>
        </div>
        <div class="nrl-card-footer-btns">
          <a href="https://maps.app.goo.gl/rqF7BedXYD9D87EJ6" target="_blank" rel="noopener" class="nrl-search-trigger">Open in Google Maps</a>
          <a href="tel:+18583492638" class="nrl-reset-trigger">Call (858) 349-2638</a>
        </div>
      </div>

      <div class="nrl-framed-photo nrl-contact-map-frame">
        <iframe
          src="https://maps.google.com/maps?q=6014+La+Granada,+Rancho+Santa+Fe,+CA+92067&amp;t=&amp;z=16&amp;ie=UTF8&amp;iwloc=&amp;output=embed"
          width="100%"
          height="420"
          style="border:0; display:block; width:100%; height:420px;"
          allowfullscreen=""
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          title="The Chapman Collection at 6014 La Granada, Rancho Santa Fe, CA 92067">
        </iframe>
      </div>
    </div>

  </div>
</div>
""".strip()


CHAPHAVIAN_CSS = r"""
/* ==========================================================================
   THE CHAPMAN COLLECTION - ENSHRINED CHAPHAVIAN EDITORIAL ARCHITECTURE
   Palette: Alabaster #F7F5F2 | Putty #D5D3CC | Slate #8A8F97 | Rose #B35A5E | Iron #2B2F32
   ========================================================================== */
:root {
    --chaphavian-alabaster: #F7F5F2;
    --chaphavian-putty:     #D5D3CC;
    --chaphavian-slate:     #8A8F97;
    --chaphavian-rose:      #B35A5E;
    --chaphavian-iron:      #2B2F32;
}

/* 1. SITEWIDE CHAPHAVIAN HEADER OVERRIDE (Beaver Builder Header 203 & Homepage Header 22) */
header.fl-builder-content-203,
header.fl-builder-content-22 {
    background-color: #F7F5F2 !important;
    border-bottom: 1px solid #D5D3CC !important;
    box-shadow: 0 8px 24px -8px rgba(179, 90, 94, 0.16) !important;
    margin-bottom: 0 !important;
}
header.fl-builder-content-203 .headmain > .fl-row-content-wrap,
header.fl-builder-content-22 .headmain > .fl-row-content-wrap,
.fl-node-b76zmierogyj > .fl-row-content-wrap,
.fl-node-67pvcrni3kox > .fl-row-content-wrap,
.fl-node-lpvdq32ygfot > .fl-row-content-wrap,
.fl-node-huxc5oflv90j > .fl-row-content-wrap,
.fl-node-ivd741tconb6 > .fl-row-content-wrap,
.fl-node-3uoip10m7wd9 > .fl-row-content-wrap {
    background-color: #F7F5F2 !important;
    border: none !important;
    border-bottom: none !important;
    box-shadow: none !important;
    margin-bottom: 0 !important;
    padding-top: 8px !important;
    padding-bottom: 8px !important;
}
header.fl-builder-content-22 {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    z-index: 999 !important;
}
body.admin-bar header.fl-builder-content-22,
body.admin-bar header.fl-builder-content-203.fl-theme-builder-header-sticky {
    top: 32px !important;
}
@media screen and (max-width: 782px) {
    body.admin-bar header.fl-builder-content-22,
    body.admin-bar header.fl-builder-content-203.fl-theme-builder-header-sticky {
        top: 46px !important;
    }
}

/* Top Navbar Menu Typography & Colors (Desktop, Tablet & Mobile - Header 203 & Header 22) */
header.fl-builder-content-203 .fl-node-n8iprdfb9olu,
header.fl-builder-content-22 .fl-node-jcip8sex7u1g {
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    justify-content: space-between !important;
}
header.fl-builder-content-203 .fl-node-rjgq0oecl2iy,
header.fl-builder-content-22 .fl-node-8zk9le2yvmoj {
    width: auto !important;
    flex: 0 0 auto !important;
    display: flex !important;
    align-items: center !important;
}
header.fl-builder-content-203 .fl-node-qdb9tz2y4g0m,
header.fl-builder-content-22 .fl-node-sdzu9rtf2wnb {
    width: auto !important;
    flex: 1 1 auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
}
header.fl-builder-content-203 .fl-node-n8iprdfb9olu .fl-col-content,
header.fl-builder-content-22 .fl-node-jcip8sex7u1g .fl-col-content,
header.fl-builder-content-203 .fl-node-n8iprdfb9olu .fl-module-content,
header.fl-builder-content-22 .fl-node-jcip8sex7u1g .fl-module-content {
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
}
header.fl-builder-content-203 .fl-node-8q49rlent1kw,
header.fl-builder-content-22 .fl-node-fb5vx0k72tsn {
    display: none !important;
}
.fl-node-jl5rp8gqstdu .pp-advanced-menu-horizontal,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu-horizontal {
    flex-wrap: nowrap !important;
    justify-content: flex-end !important;
}
.fl-node-jl5rp8gqstdu .pp-advanced-menu .menu > li > a,
.fl-node-jl5rp8gqstdu .pp-advanced-menu .menu > li > .pp-has-submenu-container > a,
.fl-node-vqcolj7s3pb6 .pp-advanced-menu .menu > li > a,
.fl-node-vqcolj7s3pb6 .pp-advanced-menu .menu > li > .pp-has-submenu-container > a,
.fl-node-ake9xj6i82hn .pp-advanced-menu .menu > li > a,
.fl-node-ake9xj6i82hn .pp-advanced-menu .menu > li > .pp-has-submenu-container > a,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu .menu > li > a,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu .menu > li > .pp-has-submenu-container > a,
.fl-node-igfoejhvnqk3 .pp-advanced-menu .menu > li > a,
.fl-node-igfoejhvnqk3 .pp-advanced-menu .menu > li > .pp-has-submenu-container > a,
.fl-node-63qfeujok79d .pp-advanced-menu .menu > li > a,
.fl-node-63qfeujok79d .pp-advanced-menu .menu > li > .pp-has-submenu-container > a {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #2B2F32 !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
    white-space: nowrap !important;
    transition: color 0.2s ease !important;
}
.fl-node-jl5rp8gqstdu .pp-advanced-menu-horizontal.pp-toggle-arrows .pp-has-submenu-container a,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu-horizontal.pp-toggle-arrows .pp-has-submenu-container a {
    padding-right: 24px !important;
}

/* Hover & Current Active Menu Item -> Chaphavian Rose (#B35A5E) instead of GoDaddy Yellow */
.fl-node-jl5rp8gqstdu .pp-advanced-menu .menu > li > a:hover,
.fl-node-jl5rp8gqstdu .pp-advanced-menu .menu > li > .pp-has-submenu-container > a:hover,
.fl-node-jl5rp8gqstdu .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-jl5rp8gqstdu .pp-advanced-menu .menu > li.current-menu-item > .pp-has-submenu-container > a,
.fl-node-vqcolj7s3pb6 .pp-advanced-menu .menu > li > a:hover,
.fl-node-vqcolj7s3pb6 .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-ake9xj6i82hn .pp-advanced-menu .menu > li > a:hover,
.fl-node-ake9xj6i82hn .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu .menu > li > a:hover,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu .menu > li > .pp-has-submenu-container > a:hover,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-uyjbe7l5ahz4 .pp-advanced-menu .menu > li.current-menu-item > .pp-has-submenu-container > a,
.fl-node-igfoejhvnqk3 .pp-advanced-menu .menu > li > a:hover,
.fl-node-igfoejhvnqk3 .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-63qfeujok79d .pp-advanced-menu .menu > li > a:hover,
.fl-node-63qfeujok79d .pp-advanced-menu .menu > li.current-menu-item > a {
    color: #B35A5E !important;
}

/* Submenu Dropdown Arrows */
header.fl-builder-content-203 .pp-advanced-menu-horizontal.pp-toggle-arrows .pp-has-submenu-container a .pp-menu-toggle:before,
header.fl-builder-content-22 .pp-advanced-menu-horizontal.pp-toggle-arrows .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-ake9xj6i82hn .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-ake9xj6i82hn-clone .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-63qfeujok79d .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-63qfeujok79d-clone .pp-has-submenu-container a .pp-menu-toggle:before {
    border-color: #2B2F32 !important;
}
header.fl-builder-content-203 .pp-advanced-menu-horizontal.pp-toggle-arrows li:hover .pp-has-submenu-container a .pp-menu-toggle:before,
header.fl-builder-content-203 .pp-advanced-menu-horizontal.pp-toggle-arrows li.current-menu-item .pp-has-submenu-container a .pp-menu-toggle:before,
header.fl-builder-content-22 .pp-advanced-menu-horizontal.pp-toggle-arrows li:hover .pp-has-submenu-container a .pp-menu-toggle:before,
header.fl-builder-content-22 .pp-advanced-menu-horizontal.pp-toggle-arrows li.current-menu-item .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-ake9xj6i82hn li:hover .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-ake9xj6i82hn li.current-menu-item .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-ake9xj6i82hn-clone li:hover .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-ake9xj6i82hn-clone li.current-menu-item .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-63qfeujok79d li:hover .pp-has-submenu-container a .pp-menu-toggle:before,
.fl-node-63qfeujok79d-clone li:hover .pp-has-submenu-container a .pp-menu-toggle:before {
    border-color: #B35A5E !important;
}

/* Submenu Dropdown Panel & Mobile Off-Canvas Clone (`div.fl-node-ake9xj6i82hn-clone` & `63qfeujok79d-clone`) */
header.fl-builder-content-203 .pp-advanced-menu .sub-menu,
header.fl-builder-content-22 .pp-advanced-menu .sub-menu,
.fl-node-ake9xj6i82hn .pp-advanced-menu .sub-menu,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .sub-menu,
.fl-node-63qfeujok79d .pp-advanced-menu .sub-menu,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .sub-menu {
    background-color: #F7F5F2 !important;
    border: 1px solid #D5D3CC !important;
    box-shadow: 0 14px 32px rgba(43, 47, 50, 0.08) !important;
}
header.fl-builder-content-203 .pp-advanced-menu .sub-menu > li > a,
header.fl-builder-content-203 .pp-advanced-menu .sub-menu > li > .pp-has-submenu-container > a,
header.fl-builder-content-22 .pp-advanced-menu .sub-menu > li > a,
header.fl-builder-content-22 .pp-advanced-menu .sub-menu > li > .pp-has-submenu-container > a,
.fl-node-ake9xj6i82hn .pp-advanced-menu .sub-menu > li > a,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .sub-menu > li > a,
.fl-node-63qfeujok79d .pp-advanced-menu .sub-menu > li > a,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .sub-menu > li > a,
.pp-advanced-menu.off-canvas .sub-menu > li > a,
.pp-advanced-menu.off-canvas .sub-menu > li > a > span.menu-item-text,
.fl-node-ake9xj6i82hn .pp-advanced-menu.off-canvas .sub-menu > li > a,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu.off-canvas .sub-menu > li > a,
.fl-node-63qfeujok79d .pp-advanced-menu.off-canvas .sub-menu > li > a,
.fl-node-63qfeujok79d-clone .pp-advanced-menu.off-canvas .sub-menu > li > a {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    color: #52575D !important;
    background-color: #F7F5F2 !important;
    border-bottom: 1px solid #EFECE6 !important;
    white-space: normal !important;
    line-height: 1.35 !important;
    padding: 8px 12px 8px 14px !important;
}
header.fl-builder-content-203 .pp-advanced-menu .sub-menu > li > a:hover,
header.fl-builder-content-203 .pp-advanced-menu .sub-menu > li > .pp-has-submenu-container > a:hover,
header.fl-builder-content-22 .pp-advanced-menu .sub-menu > li > a:hover,
header.fl-builder-content-22 .pp-advanced-menu .sub-menu > li > .pp-has-submenu-container > a:hover,
.fl-node-ake9xj6i82hn .pp-advanced-menu .sub-menu > li > a:hover,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .sub-menu > li > a:hover,
.fl-node-63qfeujok79d .pp-advanced-menu .sub-menu > li > a:hover,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .sub-menu > li > a:hover,
.pp-advanced-menu.off-canvas .sub-menu > li > a:hover,
.pp-advanced-menu.off-canvas .sub-menu > li > a:hover > span.menu-item-text {
    color: #B35A5E !important;
    background-color: #EFECE6 !important;
}

/* BLUE TEAM BEAU QA FIX: Mobile Off-Canvas Drawer & "S" Chevron Collision Fix */
.pp-advanced-menu .pp-off-canvas-menu,
.fl-node-ake9xj6i82hn .pp-off-canvas-menu,
.fl-node-ake9xj6i82hn-clone .pp-off-canvas-menu,
.fl-node-ake9xj6i82hn-clone.pp-menu-off-canvas,
.fl-node-63qfeujok79d .pp-off-canvas-menu,
.fl-node-63qfeujok79d-clone .pp-off-canvas-menu,
.fl-node-63qfeujok79d-clone.pp-menu-off-canvas {
    background-color: #F7F5F2 !important;
    border-left: 1px solid #D5D3CC !important;
    border-right: 1px solid #D5D3CC !important;
}
.pp-advanced-menu.off-canvas .pp-off-canvas-menu .pp-menu-close-btn {
    color: #2B2F32 !important;
}
.pp-advanced-menu.off-canvas .menu > li > a,
.pp-advanced-menu.off-canvas .menu > li > .pp-has-submenu-container > a,
.pp-advanced-menu.off-canvas .menu > li > a > span.menu-item-text,
.pp-advanced-menu.off-canvas .menu > li > .pp-has-submenu-container > a > span.menu-item-text,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .menu > li > a,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .menu > li > .pp-has-submenu-container > a,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .menu > li > a,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .menu > li > .pp-has-submenu-container > a {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #2B2F32 !important;
    padding-left: 0 !important;
    padding-right: 32px !important;
}
.pp-advanced-menu.off-canvas .menu > li.current-menu-item > a,
.pp-advanced-menu.off-canvas .menu > li.current-menu-item > a > span.menu-item-text,
.pp-advanced-menu.off-canvas .menu > li.current-menu-item > .pp-has-submenu-container > a > span.menu-item-text,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .menu > li.current-menu-item > .pp-has-submenu-container > a,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .menu > li > a:hover,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .menu > li > .pp-has-submenu-container > a:hover,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .menu > li.current-menu-item > a,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .menu > li.current-menu-item > .pp-has-submenu-container > a,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .menu > li > a:hover,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .menu > li > .pp-has-submenu-container > a:hover {
    color: #B35A5E !important;
}
/* Override PowerPack's high-specificity .off-canvas rule so SERVICES and SHOP align flush-left and chevrons sit on right */
.fl-node-ake9xj6i82hn .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
.fl-node-63qfeujok79d .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
.fl-node-63qfeujok79d-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
.pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
.fl-node-ake9xj6i82hn .pp-advanced-menu .pp-has-submenu-container > a > span,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu .pp-has-submenu-container > a > span,
.fl-node-63qfeujok79d .pp-advanced-menu .pp-has-submenu-container > a > span,
.fl-node-63qfeujok79d-clone .pp-advanced-menu .pp-has-submenu-container > a > span {
    padding-left: 0 !important;
    padding-right: 32px !important;
}
.fl-node-ake9xj6i82hn .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
.fl-node-ake9xj6i82hn-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
.fl-node-63qfeujok79d .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
.fl-node-63qfeujok79d-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
.pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle {
    left: auto !important;
    right: 8px !important;
}
.pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle:before {
    border-color: #2B2F32 !important;
}
/* Fix GoDaddy's 28px padding-left + left:28px chevron collision on Services & Shop in mobile drawer */
@media (max-width: 992px) {
    .fl-node-ake9xj6i82hn .pp-advanced-menu .pp-has-submenu-container > a > span,
    .fl-node-ake9xj6i82hn-clone .pp-advanced-menu .pp-has-submenu-container > a > span,
    .fl-node-63qfeujok79d .pp-advanced-menu .pp-has-submenu-container > a > span,
    .fl-node-63qfeujok79d-clone .pp-advanced-menu .pp-has-submenu-container > a > span,
    .fl-node-vqcolj7s3pb6 .pp-advanced-menu .pp-has-submenu-container > a > span,
    .fl-node-igfoejhvnqk3 .pp-advanced-menu .pp-has-submenu-container > a > span,
    .fl-node-ake9xj6i82hn .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
    .fl-node-ake9xj6i82hn-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
    .fl-node-63qfeujok79d .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span,
    .fl-node-63qfeujok79d-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-has-submenu-container > a > span {
        padding-left: 0 !important;
        padding-right: 32px !important;
    }
    .fl-node-ake9xj6i82hn .pp-advanced-menu.pp-toggle-arrows .pp-menu-toggle,
    .fl-node-ake9xj6i82hn-clone .pp-advanced-menu.pp-toggle-arrows .pp-menu-toggle,
    .fl-node-63qfeujok79d .pp-advanced-menu.pp-toggle-arrows .pp-menu-toggle,
    .fl-node-63qfeujok79d-clone .pp-advanced-menu.pp-toggle-arrows .pp-menu-toggle,
    .fl-node-vqcolj7s3pb6 .pp-advanced-menu.pp-toggle-arrows .pp-menu-toggle,
    .fl-node-igfoejhvnqk3 .pp-advanced-menu.pp-toggle-arrows .pp-menu-toggle,
    .fl-node-ake9xj6i82hn .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
    .fl-node-ake9xj6i82hn-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
    .fl-node-63qfeujok79d .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle,
    .fl-node-63qfeujok79d-clone .pp-advanced-menu.off-canvas .pp-toggle-arrows .pp-menu-toggle {
        left: auto !important;
        right: 8px !important;
    }
}

/* HIDE REDUNDANT UPPER-RIGHT HEADER PHONE NUMBER NEXT TO CONTACT US */
.fl-node-vh40jnmt5opx,
.fl-node-xeirb431vmsj,
.fl-node-15igb2qrhzxt,
.fl-node-motnbglcxikv,
.fl-node-rp8l53odkxus,
.fl-node-cw18ioxds6e4 {
    display: none !important;
}

/* Mobile Hamburger Icon */
header.fl-builder-content-203 .pp-hamburger-inner,
header.fl-builder-content-203 .pp-hamburger-inner::before,
header.fl-builder-content-203 .pp-hamburger-inner::after,
header.fl-builder-content-22 .pp-hamburger-inner,
header.fl-builder-content-22 .pp-hamburger-inner::before,
header.fl-builder-content-22 .pp-hamburger-inner::after {
    background-color: #2B2F32 !important;
}

/* Override legacy wp-custom-css "Was / Sale" labels to "Was / Is" in Chaphavian palette */
html body .fl-module-fl-woo-product-price .price del,
html body .woocommerce ul.products li.product .price del,
html body .fl-post-grid-text .price del,
html body .woocommerce div.product p.price del,
html body .woocommerce div.product span.price del {
    color: #8A8F97 !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-weight: 500 !important;
    margin-right: 8px !important;
    display: inline-block !important;
}

html body .fl-module-fl-woo-product-price .price del::before,
html body .woocommerce ul.products li.product .price del::before,
html body .fl-post-grid-text .price del::before,
html body .woocommerce div.product p.price del::before,
html body .woocommerce div.product span.price del::before {
    content: "Was " !important;
    color: #8A8F97 !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-weight: 500 !important;
}

html body .fl-module-fl-woo-product-price .price ins,
html body .woocommerce ul.products li.product .price ins,
html body .fl-post-grid-text .price ins,
html body .woocommerce div.product p.price ins,
html body .woocommerce div.product span.price ins {
    color: #B35A5E !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    display: inline-block !important;
}

html body .fl-module-fl-woo-product-price .price ins::before,
html body .woocommerce ul.products li.product .price ins::before,
html body .fl-post-grid-text .price ins::before,
html body .woocommerce div.product p.price ins::before,
html body .woocommerce div.product span.price ins::before {
    content: "Is " !important;
    color: #B35A5E !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-weight: 600 !important;
}

/* 2. SITEWIDE CHAPHAVIAN FOOTER CLEANUP & PALETTE (Beaver Builder Footer 24 & Contact Footer 131) */
/* Hide Broken Old GoDaddy Google Maps API-v1 Row in Footer 131 */
footer.fl-builder-content-131 .fl-node-rmi6v0g3tf2a {
    display: none !important;
}

/* Hide Row 3: Redundant 8-Link Sitemap Dump */
footer.fl-builder-content-24 .fl-node-8kzm5gvc03fo,
footer.fl-builder-content-131 .fl-node-dnuc3kp8j9z1 {
    display: none !important;
}

/* Hide Broken GoDaddy Web Design 404 Image & Center Copyright Text */
footer.fl-builder-content-24 .fl-node-kdgbsihalj6q,
footer.fl-builder-content-24 .fl-node-edxg4n60z9wj,
footer.fl-builder-content-131 .fl-node-kj3zhv4mupnc,
footer.fl-builder-content-131 .fl-node-z6d2e7cmv5gw {
    display: none !important;
}
footer.fl-builder-content-24 .fl-node-k4rfvonagbsl,
footer.fl-builder-content-131 .fl-node-s4uqj0yto1r6 {
    width: 100% !important;
    max-width: 100% !important;
    text-align: center !important;
}
footer.fl-builder-content-24 .fl-node-hcwktay1uq45 .fl-rich-text p,
footer.fl-builder-content-131 .fl-node-1t8guv7he9b3 .fl-rich-text p {
    text-align: center !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 10.5px !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #F7F5F2 !important;
    margin: 0 !important;
}

/* Footer Social Group (Facebook, Instagram & YouTube in Chaphavian Iron -> Rose) */
footer.fl-builder-content-24 .fl-node-j0vcbdxirfw4 .fl-icon,
footer.fl-builder-content-131 .fl-node-3kam1dqgebz7 .fl-icon {
    display: inline-block !important;
}

/* Footer Row 1: Mailing List Signup Band */
footer.fl-builder-content-24 .fl-node-j7ob3epfki6m > .fl-row-content-wrap,
footer.fl-builder-content-131 .fl-node-yfxs1wbjnc8r > .fl-row-content-wrap {
    background-color: #EFECE6 !important;
    border-top: 1px solid #D5D3CC !important;
    border-bottom: 1px solid #D5D3CC !important;
    padding-top: 36px !important;
    padding-bottom: 36px !important;
}
footer.fl-builder-content-24 .fl-node-nv9kqsze317j .heading-title,
footer.fl-builder-content-24 .fl-node-nv9kqsze317j .heading-title span.title-text,
footer.fl-builder-content-131 .fl-node-9ndwuxj2e8pk .heading-title,
footer.fl-builder-content-131 .fl-node-9ndwuxj2e8pk .heading-title span.title-text {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 28px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    color: #2B2F32 !important;
}
footer.fl-builder-content-24 .fl-node-ftvcr2o856q0 .pp-subscribe-form input[type="text"],
footer.fl-builder-content-24 .fl-node-ftvcr2o856q0 .pp-subscribe-form input[type="email"],
footer.fl-builder-content-131 .fl-node-2chaeqz5ou6b .pp-subscribe-form input[type="text"],
footer.fl-builder-content-131 .fl-node-2chaeqz5ou6b .pp-subscribe-form input[type="email"] {
    background-color: #F7F5F2 !important;
    border: 1px solid #D5D3CC !important;
    border-radius: 0 !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 17px !important;
    color: #2B2F32 !important;
}
footer.fl-builder-content-24 .fl-node-ftvcr2o856q0 .pp-subscribe-form a.fl-button,
footer.fl-builder-content-131 .fl-node-2chaeqz5ou6b .pp-subscribe-form a.fl-button {
    background-color: #2B2F32 !important;
    border: 1px solid #2B2F32 !important;
    border-radius: 0 !important;
    color: #F7F5F2 !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    transition: all 0.22s ease !important;
}
footer.fl-builder-content-24 .fl-node-ftvcr2o856q0 .pp-subscribe-form a.fl-button span.fl-button-text,
footer.fl-builder-content-131 .fl-node-2chaeqz5ou6b .pp-subscribe-form a.fl-button span.fl-button-text {
    color: #F7F5F2 !important;
}
footer.fl-builder-content-24 .fl-node-ftvcr2o856q0 .pp-subscribe-form a.fl-button:hover,
footer.fl-builder-content-131 .fl-node-2chaeqz5ou6b .pp-subscribe-form a.fl-button:hover {
    background-color: #B35A5E !important;
    border-color: #B35A5E !important;
}
footer.fl-builder-content-24 .fl-node-ftvcr2o856q0 .pp-subscribe-form a.fl-button:hover span.fl-button-text,
footer.fl-builder-content-131 .fl-node-2chaeqz5ou6b .pp-subscribe-form a.fl-button:hover span.fl-button-text {
    color: #F7F5F2 !important;
}

/* Footer Row 2: Crest & Showroom Contact Details */
footer.fl-builder-content-24 .fl-node-lg7c64xuts2v > .fl-row-content-wrap,
footer.fl-builder-content-131 .fl-node-usp3alcqerwg > .fl-row-content-wrap {
    background-color: #F7F5F2 !important;
    border-top: none !important;
    border-bottom: 1px solid #D5D3CC !important;
    padding-top: 32px !important;
    padding-bottom: 32px !important;
}
footer.fl-builder-content-24 .fl-node-lg7c64xuts2v .pp-infolist-description p,
footer.fl-builder-content-24 .fl-node-lg7c64xuts2v .pp-infolist-description a,
footer.fl-builder-content-131 .fl-node-usp3alcqerwg .pp-infolist-description p,
footer.fl-builder-content-131 .fl-node-usp3alcqerwg .pp-infolist-description a {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 18px !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    color: #2B2F32 !important;
    text-decoration: none !important;
}
footer.fl-builder-content-24 .fl-node-lg7c64xuts2v .pp-infolist-description a:hover,
footer.fl-builder-content-131 .fl-node-usp3alcqerwg .pp-infolist-description a:hover {
    color: #B35A5E !important;
}
footer.fl-builder-content-24 .fl-node-lg7c64xuts2v .pp-icon,
footer.fl-builder-content-131 .fl-node-usp3alcqerwg .pp-icon {
    color: #B35A5E !important;
}
footer.fl-builder-content-24 .fl-node-j0vcbdxirfw4 .fl-icon i,
footer.fl-builder-content-131 .fl-node-3kam1dqgebz7 .fl-icon i {
    color: #2B2F32 !important;
    transition: color 0.2s ease !important;
}
footer.fl-builder-content-24 .fl-node-j0vcbdxirfw4 .fl-icon a:hover i,
footer.fl-builder-content-131 .fl-node-3kam1dqgebz7 .fl-icon a:hover i {
    color: #B35A5E !important;
}

/* Footer Row 4: Deep Iron Copyright Bar */
footer.fl-builder-content-24 .fl-node-usz8px3cm4d9 > .fl-row-content-wrap,
footer.fl-builder-content-131 .fl-node-jibpsxwfzcqr > .fl-row-content-wrap {
    background-color: #2B2F32 !important;
    border-top: 1px solid #2B2F32 !important;
    padding-top: 14px !important;
    padding-bottom: 14px !important;
}

/* 3. HIDE STRAY DEFAULT WORDPRESS POST HEADER TITLE ON /ABOUT-US/, /SERVICES/ & /CONTACT-US/ */
body.page-id-10 .fl-post-header,
body.page-id-12 .fl-post-header,
body.page-id-16 .fl-post-header,
body.page-id-10 header.fl-post-header,
body.page-id-12 header.fl-post-header,
body.page-id-16 header.fl-post-header {
    display: none !important;
}

/* 4. PAGE CANVAS & EDITORIAL STAGE (/about-us/, /services/ & /contact-us/) + CHILD PAGE COMPACT HEADER LOCK */
html, body, .fl-page {
    overflow-x: clip !important;
    max-width: 100vw !important;
}
body.page-id-10,
body.page-id-12,
body.page-id-16,
body.page-id-10 .fl-page,
body.page-id-12 .fl-page,
body.page-id-16 .fl-page,
body.page-id-10 .fl-page-content,
body.page-id-12 .fl-page-content,
body.page-id-16 .fl-page-content {
    background-color: #F7F5F2 !important;
    color: #2B2F32 !important;
}

/* ALL PAGES (INCLUDING HOMEPAGE HEADER 22 & CHILD HEADER 203): PERMANENT COMPACT HEADER BAR + BRAND WORDMARK */
header.fl-builder-content-203 .fl-node-hg3twqezby75 .fl-photo-content,
header.fl-builder-content-203 .fl-node-kmz43r5nfbyw .fl-photo-content,
header.fl-builder-content-203 .fl-node-ax3wbdrtmy6e .fl-photo-content,
header.fl-builder-content-22 .fl-node-hxt4b2izrqlv .fl-photo-content,
header.fl-builder-content-22 .fl-node-woq7yzf4ikx0 .fl-photo-content,
header.fl-builder-content-22 .fl-node-5cayw7mkqhte .fl-photo-content {
    width: auto !important;
}
header.fl-builder-content-203 .fl-node-hg3twqezby75 .fl-photo-img,
header.fl-builder-content-203 .fl-node-kmz43r5nfbyw .fl-photo-img,
header.fl-builder-content-203 .fl-node-ax3wbdrtmy6e .fl-photo-img,
header.fl-builder-content-22 .fl-node-hxt4b2izrqlv .fl-photo-img,
header.fl-builder-content-22 .fl-node-woq7yzf4ikx0 .fl-photo-img,
header.fl-builder-content-22 .fl-node-5cayw7mkqhte .fl-photo-img {
    max-height: 50px !important;
    width: auto !important;
    height: auto !important;
    transition: none !important;
}
/* Brand Wordmark injected on Header ("THE CHAPMAN COLLECTION") */
.nrl-child-header-brand {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #2B2F32 !important;
    text-decoration: none !important;
    text-align: center !important;
    white-space: nowrap !important;
    line-height: 1.2 !important;
    transition: color 0.2s ease !important;
}
.nrl-child-header-brand:hover {
    color: #B35A5E !important;
}
header.fl-builder-content-203 .fl-node-hg3twqezby75 .fl-photo-content,
header.fl-builder-content-203 .fl-node-kmz43r5nfbyw .fl-photo-content,
header.fl-builder-content-22 .fl-node-hxt4b2izrqlv .fl-photo-content,
header.fl-builder-content-22 .fl-node-woq7yzf4ikx0 .fl-photo-content {
    display: inline-flex !important;
    align-items: center !important;
    gap: 14px !important;
}
body .fl-page-content,
body.page-id-10 .fl-page-content,
body.page-id-12 .fl-page-content,
body.page-id-16 .fl-page-content {
    padding-top: 78px !important;
}
body.home .fl-page-content {
    padding-top: 66px !important;
}
@media (max-width: 992px) {
    body .fl-page-content,
    body.page-id-10 .fl-page-content,
    body.page-id-12 .fl-page-content,
    body.page-id-16 .fl-page-content {
        padding-top: 72px !important;
    }
    body.home .fl-page-content {
        padding-top: 64px !important;
    }
}

/* ==========================================================================
   5. HOMEPAGE (PAGE ID 8 / body.home) CHAPHAVIAN ALCOVE HERO & GALLERY CARDS
   ========================================================================== */
body.home,
body.home .fl-page,
body.home .fl-page-content {
    background-color: #F7F5F2 !important;
    color: #2B2F32 !important;
}
body.home .fl-content-full.container {
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}
body.home .fl-content-full.container > .row,
body.home .fl-content-full.container .fl-content {
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* HOMEPAGE FULL-BLEED EDGE-TO-EDGE 1792x756 HERO STAGE */
body.home .fl-node-dlrf1zpevkn9 {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 auto !important;
    padding: 0 !important;
    background-color: #F7F5F2 !important;
    box-sizing: border-box !important;
}
body.home .fl-node-dlrf1zpevkn9 > .fl-row-content-wrap {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 0 !important;
    max-height: none !important;
    height: auto !important;
    aspect-ratio: 1792 / 756 !important;
    margin: 0 auto !important;
    padding: 0 !important;
    border: none !important;
    border-bottom: 1px solid #D5D3CC !important;
    box-shadow: none !important;
    background-image: url('__WELCOME_ALCOVE_URL__') !important;
    background-attachment: scroll !important;
    background-size: 100% 100% !important;
    background-position: center center !important;
    background-repeat: no-repeat !important;
    filter: none !important;
    mix-blend-mode: normal !important;
    position: relative !important;
    display: block !important;
}
body.home .fl-node-dlrf1zpevkn9 > .fl-row-content-wrap::after {
    display: none !important;
    background: transparent !important;
}
body.home .fl-node-dlrf1zpevkn9 .fl-node-bhrnwy2otm6k,
body.home .fl-node-dlrf1zpevkn9 .fl-node-7fdpo4ezy6sa {
    display: none !important;
}
.nrl-home-mobile-hero-img {
    display: none !important;
}

/* Editorial Block inside the Full-Bleed Hero (aligned to scooched 1792x756 wall lettering at left: 16.8%, top: 68.85%) */
.nrl-home-plaster-block {
    position: absolute !important;
    left: 16.8% !important;
    top: 68.85% !important;
    width: 41.5% !important;
    max-width: 680px !important;
    z-index: 5 !important;
    text-align: left !important;
    pointer-events: auto !important;
}
.nrl-home-plaster-rule {
    width: 52px !important;
    height: 2px !important;
    background-color: #B35A5E !important;
    margin: 0 0 8px 0 !important;
}
.nrl-home-plaster-subtitle {
    font-family: 'Montserrat', sans-serif !important;
    font-size: clamp(8.5px, 0.64vw, 11.5px) !important;
    font-weight: 700 !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: #16181A !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.35 !important;
    white-space: nowrap !important;
}
.nrl-home-plaster-copy {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: clamp(14px, 0.96vw, 18px) !important;
    font-weight: 600 !important;
    line-height: 1.44 !important;
    color: #16181A !important;
    -webkit-text-stroke: 0.28px rgba(22, 24, 26, 0.50) !important;
    margin: 0 0 12px 0 !important;
}
.nrl-home-plaster-actions {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
    align-items: center !important;
}
a.nrl-home-btn-primary,
a.nrl-home-btn-secondary {
    display: inline-block !important;
    background-color: #2B2F32 !important;
    color: #F7F5F2 !important;
    border: 1px solid #2B2F32 !important;
    padding: 8px 18px !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: clamp(10px, 0.72vw, 12.5px) !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    white-space: nowrap !important;
    transition: all 0.24s ease !important;
}
a.nrl-home-btn-primary:hover,
a.nrl-home-btn-secondary:hover {
    background-color: #B35A5E !important;
    border-color: #B35A5E !important;
    color: #F7F5F2 !important;
    transform: translateY(-2px);
}

/* Hide Legacy Beaver Builder Lower Homepage Rows in Favor of Cohesive Chaphavian Editorial Stage */
body.home .fl-node-bsvna1rj9ypm,
body.home .fl-node-97sxp0z4cm1h,
body.home .fl-node-82ohnrb7ea9y,
body.home .fl-node-3ohm2qw4zy8r,
body.home .fl-node-k9pi23l5rcog,
body.home .fl-node-4qgbh1cz8xmw {
    display: none !important;
}

/* Homepage Open-Canvas Editorial Stage (Zero Card Boxes - Burned Onto #F7F5F2 Alabaster Background) */
.nrl-home-editorial-stage {
    padding-top: 56px !important;
    padding-bottom: 72px !important;
    border-top: none !important;
    background-color: #F7F5F2 !important;
}
.nrl-home-open-split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 56px;
    align-items: center;
    margin-bottom: 72px;
}
.nrl-home-open-split:last-child {
    margin-bottom: 0;
}
.nrl-home-open-photo-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.nrl-home-open-photo-col .nrl-framed-photo {
    width: fit-content !important;
    max-width: 520px !important;
    margin: 0 auto !important;
    border: 1px solid #D5D3CC !important;
    background-color: #FFFFFF !important;
    padding: 8px !important;
    box-shadow: 0 14px 32px -12px rgba(43, 47, 50, 0.14) !important;
}
.nrl-home-open-photo-col .nrl-framed-photo img {
    width: auto !important;
    height: auto !important;
    max-width: 100% !important;
    max-height: 520px !important;
    object-fit: contain !important;
    display: block !important;
}
.nrl-home-open-text-col {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.nrl-home-open-text-col .nrl-card-body {
    font-size: 19px !important;
    font-weight: 500 !important;
    line-height: 1.72 !important;
    color: #2B2F32 !important;
    margin: 0 0 18px 0 !important;
}
@media (max-width: 992px) {
    .nrl-home-open-split {
        grid-template-columns: 1fr;
        gap: 36px;
        margin-bottom: 52px;
    }
    .nrl-home-open-photo-col .nrl-framed-photo {
        width: 100% !important;
        max-width: 100% !important;
    }
    .nrl-home-open-photo-col .nrl-framed-photo img {
        width: 100% !important;
        max-height: none !important;
    }
}
.nrl-em-accent {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0.02em !important;
}

@media (max-width: 992px) {
    body.home .fl-node-dlrf1zpevkn9 {
        padding: 12px 14px 24px !important;
    }
    body.home .fl-node-dlrf1zpevkn9 > .fl-row-content-wrap {
        background-image: none !important;
        aspect-ratio: auto !important;
        max-width: 100% !important;
        min-height: 0 !important;
        max-height: none !important;
        height: auto !important;
        border: 1px solid #D5D3CC !important;
        background-color: #F7F5F2 !important;
    }
    .nrl-home-mobile-hero-img {
        display: block !important;
        width: 100% !important;
        height: auto !important;
        aspect-ratio: 1792 / 756 !important;
        object-fit: cover !important;
        border-bottom: 1px solid #D5D3CC !important;
        margin: 0 !important;
    }
    .nrl-home-plaster-block {
        position: relative !important;
        left: auto !important;
        top: auto !important;
        width: 100% !important;
        max-width: 100% !important;
        background-color: #F7F5F2 !important;
        border-top: none !important;
        border-bottom: none !important;
        padding: 24px 20px !important;
    }
    .nrl-home-plaster-rule {
        width: 56px !important;
        margin-bottom: 14px !important;
    }
    .nrl-home-plaster-subtitle {
        font-size: 10.5px !important;
        line-height: 1.45 !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        margin-bottom: 10px !important;
    }
    .nrl-home-plaster-copy {
        font-size: 18px !important;
        margin-bottom: 20px !important;
    }
    .nrl-home-plaster-actions {
        flex-wrap: wrap !important;
    }
    a.nrl-home-btn-primary,
    a.nrl-home-btn-secondary {
        font-size: 12px !important;
        letter-spacing: 0.12em !important;
        padding: 12px 10px !important;
        width: 100% !important;
        text-align: center !important;
    }
}

body.page-id-10 .fl-content-full.container,
body.page-id-12 .fl-content-full.container,
body.page-id-16 .fl-content-full.container {
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}
body.page-id-10 .fl-content-full.container > .row,
body.page-id-12 .fl-content-full.container > .row,
body.page-id-16 .fl-content-full.container > .row,
body.page-id-10 .fl-content-full.container .fl-content,
body.page-id-12 .fl-content-full.container .fl-content,
body.page-id-16 .fl-content-full.container .fl-content {
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

.nrl-chaphavian-stage {
    background-color: #F7F5F2;
    color: #2B2F32;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-weight: 500;
    -webkit-text-stroke: 0.15px rgba(43, 47, 50, 0.32);
    padding: 28px 24px 76px;
    box-sizing: border-box;
    width: 100%;
}
.nrl-chaphavian-stage *,
.nrl-chaphavian-stage *::before,
.nrl-chaphavian-stage *::after {
    box-sizing: border-box;
}

.nrl-chaphavian-container {
    width: 100% !important;
    max-width: 1180px !important;
    margin: 0 auto !important;
}

/* EXACT LOCAL ABOUT US DROP SHADOW & FLOATING CARD SYSTEM (Zero Balloon Effect on Photos) */
.nrl-hover-box {
    background: #F7F5F2;
    border: 1px solid #D5D3CC;
    box-shadow: 0 10px 26px -10px rgba(179, 90, 94, 0.16),
                0 4px 12px -4px rgba(179, 90, 94, 0.08);
    transition: transform 0.34s cubic-bezier(0.22, 1, 0.36, 1),
                border-color 0.28s ease,
                background-color 0.28s ease,
                box-shadow 0.34s cubic-bezier(0.22, 1, 0.36, 1);
    will-change: transform, box-shadow;
}
.nrl-hover-box:hover {
    transform: translateY(-6px);
    background: #FAF9F7;
    border-color: #B35A5E;
    box-shadow: 0 22px 44px -8px rgba(179, 90, 94, 0.34),
                0 10px 22px -4px rgba(179, 90, 94, 0.22),
                0 0 0 1px rgba(179, 90, 94, 0.28);
}

/* Crisp 1px Photo Frame — ZERO Balloon/Scale Warp on Hover */
.nrl-framed-photo {
    position: relative;
    overflow: hidden;
    background: #EFECE6;
    border: 1px solid #D5D3CC;
    padding: 0;
    transition: border-color 0.28s ease;
}
.nrl-hover-box:hover .nrl-framed-photo {
    border-color: #B35A5E;
}
.nrl-framed-photo img {
    width: 100% !important;
    max-width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    display: block !important;
    transform: none !important;
    transition: none !important;
}

/* Typography Hierarchy */
.nrl-kicker {
    font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #B35A5E;
    margin-bottom: 10px;
    line-height: 1.4;
}

.nrl-page-h1 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 38px !important;
    font-weight: 600 !important;
    color: #2B2F32 !important;
    letter-spacing: 0.04em !important;
    line-height: 1.18 !important;
    margin: 0 0 8px 0 !important;
}

.nrl-section-h2 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 30px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #2B2F32 !important;
    margin: 0 0 14px 0 !important;
    line-height: 1.2 !important;
}

.nrl-card-h2 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 24px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #2B2F32 !important;
    margin: 0 0 12px 0 !important;
    line-height: 1.25 !important;
}

.nrl-card-body {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 18px;
    font-weight: 500;
    line-height: 1.7;
    color: #2B2F32;
    margin: 0 0 16px 0;
}

/* About Us Hero Split (Exact 1:1 Match with Local Prototype + Print-Safe minmax(0, 1fr)) */
.nrl-melissa-hero-split {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 32px;
    padding: 12px 0 32px;
    align-items: stretch;
}

.nrl-portrait-card {
    padding: 32px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0 !important;
    max-width: 100% !important;
    overflow: hidden;
}
.nrl-portrait-top {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-width: 0 !important;
    max-width: 100% !important;
}
.nrl-portrait-frame {
    flex: 1;
    min-height: 480px;
    width: 100% !important;
    max-width: 100% !important;
}
.nrl-portrait-frame img {
    width: 100% !important;
    max-width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center top;
    filter: none !important;
}
.nrl-portrait-caption {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-weight: 600;
    font-size: 15.5px;
    color: #2B2F32;
    text-align: center;
    margin-top: 14px;
    line-height: 1.45;
}
.nrl-portrait-cta-bar {
    margin-top: 18px;
    padding-top: 18px;
    border-top: 1px solid #D5D3CC;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.nrl-bio-column {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 20px;
    font-weight: 500;
    line-height: 1.8;
    color: #2B2F32;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0 !important;
    max-width: 100% !important;
}
.nrl-bio-copy p {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 20px;
    font-weight: 500;
    line-height: 1.8;
    color: #2B2F32;
    margin: 0 0 20px 0;
}
.nrl-bio-copy p.nrl-last-bio-p {
    margin-bottom: 24px;
}

.nrl-signature-block {
    padding: 20px 0 22px;
    border-top: 1px solid #D5D3CC;
    border-bottom: 1px solid #D5D3CC;
}
.nrl-signature-script {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 26px;
    font-weight: 600;
    font-style: italic;
    color: #2B2F32;
    line-height: 1.2;
}
.nrl-signature-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #52575D;
    margin-top: 4px;
}

/* Lower 2-Column Grid */
.nrl-melissa-lower-grid {
    margin-top: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    align-items: stretch;
}
.nrl-lower-card {
    padding: 32px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.nrl-showroom-frame {
    aspect-ratio: 16 / 10;
    margin-bottom: 20px;
}
.nrl-card-footer-meta {
    border-top: 1px solid #D5D3CC;
    padding-top: 16px;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #52575D;
}

.nrl-linen-callout {
    background: #EFECE6;
    border: 1px solid #D5D3CC;
    padding: 18px 20px;
    margin-bottom: 18px;
}
.nrl-linen-callout-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 10.5px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #2B2F32;
    font-weight: 700;
    margin-bottom: 8px;
}
.nrl-fulfillment-list {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 17px;
    font-weight: 500;
    line-height: 1.65;
    color: #2B2F32;
}
.nrl-fulfillment-list li {
    margin-bottom: 6px;
}
.nrl-fulfillment-list li:last-child {
    margin-bottom: 0;
}
.nrl-fulfillment-list strong {
    color: #B35A5E;
    font-weight: 700;
}

.nrl-card-footer-cta {
    border-top: 1px solid #D5D3CC;
    padding-top: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.nrl-card-footer-italic {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 16px;
    font-weight: 600;
    font-style: italic;
    color: #2B2F32;
}
.nrl-card-footer-btns {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

/* DARK-TO-ROSE CHAPHAVIAN BUTTONS (.nrl-search-trigger & .nrl-reset-trigger) */
.nrl-search-trigger,
a.nrl-search-trigger {
    display: inline-block;
    background: #2B2F32 !important;
    color: #F7F5F2 !important;
    border: 1px solid #2B2F32 !important;
    padding: 10px 30px;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    text-align: center;
    cursor: pointer;
    white-space: nowrap;
    transition: transform 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                border-color 0.22s ease,
                background-color 0.22s ease,
                color 0.22s ease !important;
    will-change: transform, box-shadow;
}
.nrl-search-trigger:hover,
a.nrl-search-trigger:hover {
    background: #B35A5E !important;
    color: #F7F5F2 !important;
    border-color: #B35A5E !important;
    transform: translateY(-3px);
    box-shadow: 0 12px 24px -6px rgba(179, 90, 94, 0.28);
}

.nrl-reset-trigger,
a.nrl-reset-trigger {
    display: inline-block;
    background: #2B2F32 !important;
    color: #F7F5F2 !important;
    border: 1px solid #2B2F32 !important;
    padding: 9px 22px;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    text-align: center;
    cursor: pointer;
    white-space: nowrap;
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                border-color 0.24s ease,
                background-color 0.24s ease,
                color 0.24s ease !important;
    will-change: transform, box-shadow;
}
.nrl-reset-trigger:hover,
a.nrl-reset-trigger:hover {
    background: #B35A5E !important;
    color: #F7F5F2 !important;
    border-color: #B35A5E !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -6px rgba(179, 90, 94, 0.24);
}

.nrl-btn-full {
    width: 100%;
}
.nrl-btn-sm,
a.nrl-btn-sm {
    padding: 8px 10px !important;
    font-size: 11.5px !important;
    letter-spacing: 0.12em !important;
    width: 100% !important;
}

/* ==========================================================================
   SERVICES & PREFERRED SHIPPING PARTNERS STYLES (/services/)
   ========================================================================== */
.nrl-services-hero-card {
    padding: 36px 40px;
    text-align: center;
    margin-bottom: 32px;
}
.nrl-services-lead {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 20px;
    font-weight: 500;
    line-height: 1.72;
    color: #2B2F32;
    max-width: 820px;
    margin: 0 auto;
}

.nrl-service-anchor-section {
    scroll-margin-top: 130px;
    margin-bottom: 32px;
}

.nrl-shipping-master-card {
    padding: 36px 32px;
    width: 100%;
    overflow: hidden;
}
.nrl-shipping-header-block {
    padding-bottom: 24px;
    margin-bottom: 26px;
    border-bottom: 1px solid #D5D3CC;
}

.nrl-shippers-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
    align-items: stretch;
    width: 100%;
}
.nrl-shipper-card {
    background-color: #EFECE6;
    border: 1px solid #D5D3CC;
    padding: 24px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
    width: 100%;
}
.nrl-shipper-badge {
    font-family: 'Montserrat', sans-serif;
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #B35A5E;
    margin-bottom: 8px;
    line-height: 1.45;
    min-height: 28px;
}
.nrl-shipper-name {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 23px !important;
    font-weight: 600 !important;
    color: #2B2F32 !important;
    margin: 0 0 6px 0 !important;
    line-height: 1.2 !important;
}
.nrl-shipper-contact-person {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 17px;
    font-style: italic;
    color: #52575D;
    padding-bottom: 12px;
    margin-bottom: 14px;
    border-bottom: 1px solid #D5D3CC;
}
.nrl-shipper-contact-person strong {
    color: #2B2F32;
    font-style: normal;
    font-weight: 600;
}
.nrl-shipper-details {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 17.5px;
    line-height: 1.55;
    color: #2B2F32;
    margin-bottom: 18px;
    overflow-wrap: break-word;
    word-break: break-word;
}
.nrl-shipper-row {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
}
.nrl-shipper-row:last-child {
    margin-bottom: 0;
}
.nrl-shipper-label {
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8A8F97;
    margin-bottom: 2px;
}
.nrl-shipper-row a,
.nrl-container-copy a {
    color: #2B2F32 !important;
    font-weight: 600;
    text-decoration: underline !important;
    text-decoration-color: #B35A5E !important;
}
.nrl-shipper-row a:hover,
.nrl-container-copy a:hover {
    color: #B35A5E !important;
}
.nrl-container-copy {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 17.5px;
    line-height: 1.58;
    color: #2B2F32;
    margin: 0 0 12px 0;
}
.nrl-shipper-actions {
    border-top: 1px solid #D5D3CC;
    padding-top: 14px;
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 8px;
    width: 100%;
}

/* Restoration Split Card */
.nrl-restoration-split-card {
    padding: 36px;
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 36px;
    align-items: center;
}
.nrl-restoration-copy-col {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.nrl-restoration-cta-row {
    margin-top: 12px;
    padding-top: 20px;
    border-top: 1px solid #D5D3CC;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.nrl-restoration-frame {
    max-height: 460px;
}

/* ==========================================================================
   CONTACT US PAGE (/contact-us/ - PAGE ID 16) & GRAVITY FORM CHAPHAVIAN STYLING
   ========================================================================== */
.nrl-contact-map-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    flex-wrap: wrap;
    gap: 18px;
    padding-bottom: 22px;
    margin-bottom: 22px;
    border-bottom: 1px solid #D5D3CC;
}
.nrl-contact-map-frame {
    padding: 6px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #D5D3CC !important;
    width: 100% !important;
}
.nrl-contact-map-frame iframe {
    display: block !important;
    width: 100% !important;
    height: 420px !important;
    border: 0 !important;
}

/* Chaphavian Gravity Form #1 Overrides */
.nrl-chaphavian-gform-wrap .gform_validation_container,
.nrl-chaphavian-gform-wrap .gfield--type-honeypot,
.nrl-chaphavian-gform-wrap #field_1_6 {
    display: none !important;
}
.nrl-chaphavian-gform-wrap .gform_fields {
    display: flex !important;
    flex-direction: column !important;
    gap: 18px !important;
}
.nrl-chaphavian-gform-wrap .gfield_label,
.nrl-chaphavian-gform-wrap label.gform-field-label {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #2B2F32 !important;
    margin-bottom: 6px !important;
    display: block !important;
}
.nrl-chaphavian-gform-wrap .gfield_required,
.nrl-chaphavian-gform-wrap .gfield_required_text {
    color: #B35A5E !important;
    font-weight: 600 !important;
    font-size: 9.5px !important;
    margin-left: 4px !important;
}
.nrl-chaphavian-gform-wrap input[type="text"],
.nrl-chaphavian-gform-wrap input[type="email"],
.nrl-chaphavian-gform-wrap input[type="tel"],
.nrl-chaphavian-gform-wrap textarea {
    width: 100% !important;
    background-color: #FFFFFF !important;
    border: 1px solid #D5D3CC !important;
    border-radius: 0 !important;
    padding: 12px 14px !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 18px !important;
    font-weight: 500 !important;
    color: #2B2F32 !important;
    box-sizing: border-box !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.nrl-contact-form-card,
.nrl-contact-form-card > div,
.nrl-chaphavian-gform-wrap,
.nrl-chaphavian-gform-wrap .gform_wrapper,
.nrl-chaphavian-gform-wrap form {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 auto !important;
    justify-content: space-between !important;
}
.nrl-chaphavian-gform-wrap .gform_body,
.nrl-chaphavian-gform-wrap .gform-body {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 auto !important;
}
.nrl-chaphavian-gform-wrap textarea {
    min-height: 220px !important;
    resize: vertical !important;
}
.nrl-chaphavian-gform-wrap input[type="text"]:focus,
.nrl-chaphavian-gform-wrap input[type="email"]:focus,
.nrl-chaphavian-gform-wrap input[type="tel"]:focus,
.nrl-chaphavian-gform-wrap textarea:focus {
    border-color: #B35A5E !important;
    outline: none !important;
    box-shadow: 0 0 0 1px rgba(179, 90, 94, 0.25) !important;
}
.nrl-chaphavian-gform-wrap .gform_footer,
.nrl-chaphavian-gform-wrap .gform-footer {
    margin-top: 20px !important;
    padding: 0 !important;
}
.nrl-chaphavian-gform-wrap input[type="submit"],
.nrl-chaphavian-gform-wrap #gform_submit_button_1,
.nrl-chaphavian-gform-wrap .gform_button {
    display: inline-block !important;
    width: 100% !important;
    background-color: #2B2F32 !important;
    color: #F7F5F2 !important;
    border: 1px solid #2B2F32 !important;
    border-radius: 0 !important;
    padding: 13px 30px !important;
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: transform 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                background-color 0.22s ease,
                border-color 0.22s ease !important;
}
.nrl-chaphavian-gform-wrap input[type="submit"]:hover,
.nrl-chaphavian-gform-wrap #gform_submit_button_1:hover,
.nrl-chaphavian-gform-wrap .gform_button:hover {
    background-color: #B35A5E !important;
    border-color: #B35A5E !important;
    color: #F7F5F2 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 24px -6px rgba(179, 90, 94, 0.28) !important;
}

@media (max-width: 992px) {
    .nrl-melissa-hero-split,
    .nrl-melissa-lower-grid,
    .nrl-shippers-grid,
    .nrl-restoration-split-card {
        grid-template-columns: 1fr;
    }
    .nrl-portrait-frame {
        min-height: 380px;
    }
    .nrl-services-hero-card,
    .nrl-shipping-master-card,
    .nrl-lower-card,
    .nrl-portrait-card,
    .nrl-restoration-split-card {
        padding: 24px 20px;
    }
}
@media (max-width: 768px) {
    /* Single-bar compact mobile header across all pages (Header 203 & Homepage Header 22) */
    header.fl-builder-content-203 .fl-node-hrzs1p5fkl4t,
    header.fl-builder-content-203 .fl-node-15igb2qrhzxt,
    header.fl-builder-content-203 .fl-node-z2608ox7jgep,
    header.fl-builder-content-22 .fl-node-afz98wykp1jt,
    header.fl-builder-content-22 .fl-node-8k7cfiyw1eso,
    header.fl-builder-content-22 .fl-node-cw18ioxds6e4 {
        display: none !important;
        height: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }
    header.fl-builder-content-203 .fl-node-izcy7580xsrd,
    header.fl-builder-content-22 .fl-node-dh469t78u0ri {
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 6px 14px !important;
        width: 100% !important;
    }
    header.fl-builder-content-203 .fl-node-10hltjmni6y4,
    header.fl-builder-content-203 .fl-node-a35lewp7xv09,
    header.fl-builder-content-22 .fl-node-oeg3v86u1yml,
    header.fl-builder-content-22 .fl-node-91sne8drkwu5 {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    header.fl-builder-content-203 .fl-node-ax3wbdrtmy6e > .fl-module-content,
    header.fl-builder-content-203 .fl-node-ake9xj6i82hn > .fl-module-content,
    header.fl-builder-content-22 .fl-node-5cayw7mkqhte > .fl-module-content,
    header.fl-builder-content-22 .fl-node-63qfeujok79d > .fl-module-content {
        margin: 0 !important;
    }
    header.fl-builder-content-203 .fl-node-ax3wbdrtmy6e .fl-photo-img,
    header.fl-builder-content-22 .fl-node-5cayw7mkqhte .fl-photo-img {
        max-height: 42px !important;
        width: auto !important;
    }
    .nrl-child-header-brand {
        font-size: 13.5px !important;
        letter-spacing: 0.14em !important;
        flex: 1 1 auto !important;
        text-align: center !important;
        padding: 0 8px !important;
    }
    body .fl-page-content,
    body.home .fl-page-content,
    body.page-id-10 .fl-page-content,
    body.page-id-12 .fl-page-content,
    body.page-id-16 .fl-page-content {
        padding-top: 58px !important;
    }
    .nrl-chaphavian-stage {
        padding: 16px 16px 56px !important;
    }
    /* Uncrop Melissa portrait & match full-width Restoration CTA on mobile */
    .nrl-portrait-frame {
        min-height: 0 !important;
        height: auto !important;
        aspect-ratio: 920 / 1080;
    }
    .nrl-restoration-cta-row,
    .nrl-restoration-cta-row a {
        width: 100% !important;
    }
    .fl-node-15igb2qrhzxt.fl-module > .fl-module-content {
        margin-left: 0 !important;
        text-align: center !important;
    }
    .fl-node-15igb2qrhzxt .pp-infolist-wrap .layout-1 .pp-list-item-content {
        justify-content: center !important;
    }
    .nrl-shipper-actions {
        grid-template-columns: 1fr !important;
        gap: 10px !important;
    }
    .nrl-btn-sm,
    a.nrl-btn-sm {
        padding: 10px 14px !important;
        font-size: 12.5px !important;
        letter-spacing: 0.14em !important;
        white-space: normal !important;
    }
    .nrl-card-footer-btns {
        width: 100%;
        flex-direction: column;
    }
    .nrl-card-footer-btns a {
        width: 100%;
    }
}

/* ==========================================================================
   PRINT / PDF EXPORT ARCHITECTURE (@media print)
   Fixes 2211x2211 portrait overflow, blank Page 1 box, 1-word squished bio,
   and Bootstrap's ugly raw URL suffixes when printing to PDF.
   ========================================================================== */
@media print {
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    a[href]::after {
        content: none !important;
        display: none !important;
    }
    #wpadminbar,
    .acsb-trigger,
    #acsb-trigger,
    [class*="acsb"],
    [id*="acsb"],
    .uwy,
    #userwayAccessibilityIcon,
    .userway_buttons_wrapper {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    header.fl-builder-content-203,
    header.fl-builder-content-22 {
        position: static !important;
        box-shadow: none !important;
    }
    body .fl-page-content,
    body.home .fl-page-content,
    body.page-id-10 .fl-page-content,
    body.page-id-12 .fl-page-content,
    body.page-id-16 .fl-page-content {
        padding-top: 0 !important;
    }
    /* 1. Homepage Hero Button Fit in Portrait Print */
    .nrl-home-plaster-block {
        top: 66.2% !important;
        width: 46% !important;
    }
    .nrl-home-plaster-rule {
        margin: 0 0 3px 0 !important;
    }
    .nrl-home-plaster-subtitle {
        font-size: 7.5px !important;
        margin: 0 0 3px 0 !important;
    }
    .nrl-home-plaster-copy {
        font-size: 10.5px !important;
        line-height: 1.32 !important;
        margin: 0 0 6px 0 !important;
    }
    a.nrl-home-btn-primary,
    a.nrl-home-btn-secondary {
        padding: 4px 10px !important;
        font-size: 8.5px !important;
    }
    /* 2. Prevent Chromium Print Grid Overlap via Row Flexbox */
    .nrl-chaphavian-stage {
        padding: 16px 0 24px !important;
    }
    .nrl-melissa-hero-split,
    .nrl-melissa-lower-grid,
    .nrl-home-open-split {
        display: flex !important;
        flex-direction: row !important;
        align-items: flex-start !important;
        justify-content: space-between !important;
        gap: 20px !important;
    }
    .nrl-melissa-hero-split > *,
    .nrl-melissa-lower-grid > *,
    .nrl-home-open-split > * {
        flex: 1 1 48% !important;
        min-width: 0 !important;
        max-width: 48% !important;
    }
    .nrl-portrait-card,
    .nrl-portrait-top,
    .nrl-portrait-frame,
    .nrl-lower-card,
    .nrl-bio-column,
    .nrl-shipping-master-card,
    .nrl-services-hero-card,
    .nrl-restoration-split-card {
        display: block !important;
        height: auto !important;
        min-height: 0 !important;
        box-shadow: none !important;
        break-inside: avoid;
        page-break-inside: avoid;
    }
    .nrl-portrait-card,
    .nrl-lower-card,
    .nrl-shipping-master-card,
    .nrl-services-hero-card,
    .nrl-restoration-split-card {
        padding: 18px !important;
    }
    .nrl-portrait-frame {
        width: 100% !important;
        max-width: 100% !important;
        max-height: 340px !important;
        overflow: hidden !important;
    }
    .nrl-portrait-frame img,
    .nrl-framed-photo img {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        max-height: 340px !important;
        object-fit: cover !important;
        display: block !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }
    .nrl-bio-column,
    .nrl-bio-copy p {
        font-size: 13.5px !important;
        line-height: 1.55 !important;
        margin-bottom: 10px !important;
    }
}
"""

FOOTER_POLISH_JS = r"""
document.addEventListener('DOMContentLoaded', function() {
    // 1. Inject "THE CHAPMAN COLLECTION" wordmark into compact header across all pages (Header 203 & Homepage Header 22)
    var mobilePairs = [
        ['header.fl-builder-content-203 .fl-node-izcy7580xsrd', 'header.fl-builder-content-203 .fl-node-a35lewp7xv09'],
        ['header.fl-builder-content-22 .fl-node-dh469t78u0ri', 'header.fl-builder-content-22 .fl-node-91sne8drkwu5']
    ];
    mobilePairs.forEach(function(pair) {
        var mRow = document.querySelector(pair[0]);
        var mHam = document.querySelector(pair[1]);
        if (mRow && mHam && !mRow.querySelector('.nrl-child-header-brand')) {
            var brandLink = document.createElement('a');
            brandLink.href = 'https://thechapmancollection.com/';
            brandLink.className = 'nrl-child-header-brand';
            brandLink.textContent = 'THE CHAPMAN COLLECTION';
            mRow.insertBefore(brandLink, mHam);
        }
    });
    var desktopCrests = document.querySelectorAll(
        'header.fl-builder-content-203 .fl-node-hg3twqezby75 .fl-photo-content, ' +
        'header.fl-builder-content-203 .fl-node-kmz43r5nfbyw .fl-photo-content, ' +
        'header.fl-builder-content-22 .fl-node-hxt4b2izrqlv .fl-photo-content, ' +
        'header.fl-builder-content-22 .fl-node-woq7yzf4ikx0 .fl-photo-content'
    );
    desktopCrests.forEach(function(wrap) {
        if (!wrap.querySelector('.nrl-child-header-brand')) {
            var dLink = document.createElement('a');
            dLink.href = 'https://thechapmancollection.com/';
            dLink.className = 'nrl-child-header-brand';
            dLink.textContent = 'THE CHAPMAN COLLECTION';
            wrap.appendChild(dLink);
        }
    });

    // 2. Homepage (body.home): Sync header offset to eliminate top double-fold gap & inject Chaphavian Plaster Editorial Block
    if (document.body.classList.contains('home')) {
        var syncHomeHeaderOffset = function() {
            var hdr = document.querySelector('header.fl-builder-content-22') || document.querySelector('header.fl-builder-content-203');
            var pageContent = document.querySelector('.fl-page-content');
            if (hdr && pageContent) {
                var h = hdr.offsetHeight;
                if (h > 30) {
                    pageContent.style.setProperty('padding-top', h + 'px', 'important');
                }
            }
        };
        syncHomeHeaderOffset();
        window.addEventListener('load', syncHomeHeaderOffset);
        window.addEventListener('resize', syncHomeHeaderOffset);

        var heroWrap = document.querySelector('.fl-node-dlrf1zpevkn9 > .fl-row-content-wrap');
        if (heroWrap && !heroWrap.querySelector('.nrl-home-plaster-block')) {
            var mobileHeroImg = document.createElement('img');
            mobileHeroImg.className = 'nrl-home-mobile-hero-img';
            mobileHeroImg.src = '__WELCOME_ALCOVE_URL__';
            mobileHeroImg.alt = 'The Chapman Collection Digital Gallery';
            heroWrap.insertBefore(mobileHeroImg, heroWrap.firstChild);

            var plasterBlock = document.createElement('div');
            plasterBlock.className = 'nrl-home-plaster-block';
            plasterBlock.innerHTML =
                '<div class="nrl-home-plaster-rule"></div>' +
                '<div class="nrl-home-plaster-subtitle">Providing Fine Furniture and Antiques for Over 30 Years</div>' +
                '<p class="nrl-home-plaster-copy">We are currently updating our online gallery to showcase our curated European and Asian collection. Explore our featured selection below or visit us seven days a week in the heart of the Rancho Santa Fe Village.</p>' +
                '<div class="nrl-home-plaster-actions">' +
                    '<a href="https://thechapmancollection.com/shop/" class="nrl-home-btn-primary">Browse Our Collection</a>' +
                    '<a href="https://thechapmancollection.com/services/" class="nrl-home-btn-secondary">Explore Our Services</a>' +
                '</div>';
            heroWrap.appendChild(plasterBlock);
        }

        // Inject Open-Canvas Homepage Flow: Timeless Furniture + Vintage Decor & One-of-a-Kind Shop Burned Directly Onto #F7F5F2 Alabaster Background (Zero Card Boxes)
        var heroRow = document.querySelector('.fl-node-dlrf1zpevkn9');
        if (heroRow && !document.querySelector('.nrl-home-editorial-stage')) {
            var homeStage = document.createElement('div');
            homeStage.className = 'nrl-chaphavian-stage nrl-home-editorial-stage';
            homeStage.innerHTML =
                '<div class="nrl-chaphavian-container">' +

                    '<!-- ROW 1: SHOWROOM VIGNETTE PHOTO LEFT + TIMELESS FURNITURE & VINTAGE DECOR RIGHT (Burned Onto #F7F5F2 Background, Zero Card Boxes, Zero Extra Buttons) -->' +
                    '<div class="nrl-home-open-split">' +
                        '<div class="nrl-home-open-photo-col">' +
                            '<div class="nrl-framed-photo">' +
                                '<img src="https://thechapmancollection.com/wp-content/uploads/2026/10/GoDaddy_-5774-scaled.jpg" alt="Curated Old World and European Antiques at The Chapman Collection" loading="lazy" />' +
                            '</div>' +
                        '</div>' +

                        '<div class="nrl-home-open-text-col">' +
                            '<div class="nrl-kicker">' +
                                'Curated for Timeless Interiors &middot; Rancho Santa Fe Village' +
                            '</div>' +
                            '<h1 class="nrl-page-h1" style="margin-bottom:12px;">' +
                                'Timeless Furniture That <em class="nrl-em-accent">Elevates Your Home</em>' +
                            '</h1>' +
                            '<div style="width:52px;height:2px;background-color:#B35A5E;margin:0 0 18px 0;"></div>' +
                            '<p class="nrl-card-body">' +
                                'Transform your interior design with The Chapman Collection&rsquo;s antique furniture. We curate Old World and European styles that effortlessly juxtapose and complement both classical residences and modern design themes.' +
                            '</p>' +
                            '<p class="nrl-card-body">' +
                                'Our vintage furnishings, fine art, bronzes and hand-knotted Persian carpets add distinct charm and provenance to any space, whether chosen as singular statement pieces or subtle complementary accents.' +
                            '</p>' +
                            '<div style="border-top:1px solid #D5D3CC;margin:18px 0 18px 0;"></div>' +
                            '<div class="nrl-kicker">' +
                                'Rarity, Provenance and Authenticity' +
                            '</div>' +
                            '<h2 class="nrl-card-h2" style="margin-bottom:10px;">' +
                                'Vintage D&eacute;cor as <em class="nrl-em-accent" style="font-size:26px;">Finishing Touches</em>' +
                            '</h2>' +
                            '<p class="nrl-card-body" style="margin-bottom:0;">' +
                                'We have accent pieces that give homes more layers of personality. Sourced directly from across Europe and the Near East, each piece is selected for its history, craftsmanship and enduring beauty.' +
                            '</p>' +
                        '</div>' +
                    '</div>' +

                    '<!-- ROW 2: ONE-OF-A-KIND ANTIQUE FURNITURE SHOP + WARM REGARDS, MELISSA CHAPMAN SIGN-OFF LEFT + SHOWROOM PHOTO RIGHT (Burned Onto #F7F5F2 Background, Zero Card Boxes) -->' +
                    '<div class="nrl-home-open-split" style="border-top:1px solid #D5D3CC;padding-top:64px;">' +
                        '<div class="nrl-home-open-text-col">' +
                            '<div class="nrl-kicker">' +
                                'From Harrington Road in London to Rancho Santa Fe, California' +
                            '</div>' +
                            '<h2 class="nrl-section-h2" style="margin-bottom:14px;">' +
                                'One-of-a-Kind <em class="nrl-em-accent">Antique Furniture Shop</em>' +
                            '</h2>' +
                            '<div style="width:52px;height:2px;background-color:#B35A5E;margin:0 0 18px 0;"></div>' +
                            '<p class="nrl-card-body">' +
                                'Seasoned proprietor Melissa Chapman has developed a keen eye for spotting and evaluating antiques and fine furniture. Her collection features handmade Old World and European pieces from around the globe, including fine accessories, period European furniture, artwork and hand-knotted Persian carpets.' +
                            '</p>' +
                            '<p class="nrl-card-body" style="margin-bottom:24px !important;">' +
                                'Our showroom in the heart of the Rancho Santa Fe Village operates seven days a week and offers local, national and overseas delivery. Schedule a visit with us at The Chapman Collection to learn how we can best serve you. We would be delighted to answer your questions.' +
                            '</p>' +
                            '<div class="nrl-signature-block" style="margin-bottom:0;">' +
                                '<div class="nrl-signature-script">Warm regards, Melissa Chapman</div>' +
                                '<div class="nrl-signature-title">Founder and Principal Curator &middot; The Chapman Collection</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="nrl-home-open-photo-col">' +
                            '<div class="nrl-framed-photo">' +
                                '<img src="https://thechapmancollection.com/wp-content/uploads/2026/10/IMG_4249.jpg" alt="The Chapman Collection Rancho Santa Fe Showroom Vignette" loading="lazy" />' +
                            '</div>' +
                        '</div>' +
                    '</div>' +

                '</div>';
            heroRow.insertAdjacentElement('afterend', homeStage);
        }
    }

    var hoursNodes = document.querySelectorAll('.fl-node-xy035d48fthl .pp-infolist-description p, .fl-node-362z8hfto1iy .pp-infolist-description p');
    hoursNodes.forEach(function(hoursNode) {
        hoursNode.innerHTML = 'Open Seven Days a Week<br />Mon - Sat: 10:00 AM - 6:00 PM &middot; Sun: 11:00 AM - 4:00 PM';
    });
    var copyrightNodes = document.querySelectorAll('footer.fl-builder-content-24 .fl-node-hcwktay1uq45 .fl-rich-text p, footer.fl-builder-content-131 .fl-node-1t8guv7he9b3 .fl-rich-text p');
    copyrightNodes.forEach(function(copyrightNode) {
        copyrightNode.innerHTML = '&copy; 2026 The Chapman Collection. All Rights Reserved. &middot; Digital Architecture by <a href="https://renderwithoutcode.com/" target="_blank" rel="noopener" style="color:#F7F5F2;text-decoration:underline;text-decoration-color:#B35A5E;">NeverRender Labs</a>';
    });
    var fbLinks = document.querySelectorAll('footer.fl-builder-content-24 .fl-node-j0vcbdxirfw4 a[href*="facebook.com"], footer.fl-builder-content-131 .fl-node-3kam1dqgebz7 a[href*="facebook.com"]');
    fbLinks.forEach(function(a) {
        a.href = 'https://www.facebook.com/TheChapmanCollection';
        a.target = '_blank';
        a.rel = 'noopener';
    });
    var igLinks = document.querySelectorAll('footer.fl-builder-content-24 .fl-node-j0vcbdxirfw4 a[href*="instagram.com"], footer.fl-builder-content-131 .fl-node-3kam1dqgebz7 a[href*="instagram.com"]');
    igLinks.forEach(function(a) {
        a.href = 'https://www.instagram.com/thechapmancollection/';
        a.target = '_blank';
        a.rel = 'noopener';
    });
    var ytLinks = document.querySelectorAll('footer.fl-builder-content-24 .fl-node-j0vcbdxirfw4 a[href*="youtube.com"], footer.fl-builder-content-131 .fl-node-3kam1dqgebz7 a[href*="youtube.com"]');
    ytLinks.forEach(function(a) {
        a.href = 'https://www.youtube.com/@TheChapmanCollection';
        a.target = '_blank';
        a.rel = 'noopener';
    });

    // Rename "Shop" to "Gallery" across desktop and mobile off-canvas navigation menus (preserving the <span class="pp-menu-toggle"> chevron)
    var shopNavSpans = document.querySelectorAll('.pp-advanced-menu .menu-item a span.menu-item-text');
    shopNavSpans.forEach(function(span) {
        Array.from(span.childNodes).forEach(function(node) {
            if (node.nodeType === 3 && node.nodeValue.trim() === 'Shop') {
                node.nodeValue = 'Gallery';
            }
        });
        var toggle = span.querySelector('.pp-menu-toggle');
        if (toggle && toggle.getAttribute('aria-label') === 'Shop: submenu') {
            toggle.setAttribute('aria-label', 'Gallery: submenu');
        }
    });

    // Also update the Beaver Themer archive heading on /shop/ if it renders "Archives: Products" or "Shop"
    var archiveHeading = document.querySelector('.fl-node-x9jdom6vwbfs .pp-heading .heading-title span.pp-primary-title');
    if (archiveHeading) {
        var hText = archiveHeading.textContent.trim();
        if (hText === 'Shop' || hText === 'Archives: Products' || hText === 'Products') {
            archiveHeading.textContent = 'The Gallery';
        }
    }

    // Bust GoDaddy Varnish Edge Cache on internal menu & product links across the site
    var navLinks = document.querySelectorAll('a[href*="thechapmancollection.com/"], a[href^="/"]');
    navLinks.forEach(function(a) {
        try {
            if (a.href.indexOf('wp-admin') !== -1 || a.href.indexOf('mailto:') === 0 || a.href.indexOf('tel:') === 0) return;
            var u = new URL(a.href, window.location.origin);
            if (u.hostname === window.location.hostname && !u.searchParams.has('v')) {
                u.searchParams.set('v', '12');
                a.href = u.toString();
            }
        } catch(e) {}
    });
});
""".strip()


def build_snippet_25_php(about_html, services_html, contact_html, css_text, js_text):
    about_b64 = base64.b64encode(about_html.encode("utf-8")).decode("ascii")
    services_b64 = base64.b64encode(services_html.encode("utf-8")).decode("ascii")
    contact_b64 = base64.b64encode(contact_html.encode("utf-8")).decode("ascii")
    css_b64 = base64.b64encode(css_text.encode("utf-8")).decode("ascii")
    js_b64 = base64.b64encode(js_text.encode("utf-8")).decode("ascii")

    return f"""
// NRL Chaphavian Editorial Upgrade: Sitewide Header/Footer Palette + Homepage Alcove Hero + /about-us/ (Page 10), /services/ (Page 12) & /contact-us/ (Page 16)
// Bypasses 2024 GoDaddy Beaver Builder locked layout while keeping original postmeta intact.

// Stop WP Smush Pro from converting PNG uploads to 70 KB JPEGs or auto-downscaling gallery masters
add_filter('wp_smush_image', '__return_false', 99999);
add_filter('big_image_size_threshold', '__return_false', 99999);

add_action('init', function () {{
    $smush_settings = get_option('wp-smush-settings');
    if (is_array($smush_settings) && (!empty($smush_settings['png_to_jpg']) || !empty($smush_settings['lossy']) || !empty($smush_settings['original']) || !empty($smush_settings['resize']))) {{
        $smush_settings['png_to_jpg'] = false;
        $smush_settings['lossy'] = 0;
        $smush_settings['original'] = false;
        $smush_settings['resize'] = false;
        update_option('wp-smush-settings', $smush_settings);
    }}
    $uploads = wp_upload_dir();
    $dir_2026_11 = trailingslashit($uploads['basedir']) . '2026/11/';
    if (file_exists($dir_2026_11 . 'the-chaphavian-hero-2-5-lossless.png') && !file_exists($dir_2026_11 . 'the-chaphavian-hero-2-5.png')) {{
        @copy($dir_2026_11 . 'the-chaphavian-hero-2-5-lossless.png', $dir_2026_11 . 'the-chaphavian-hero-2-5.png');
    }}
    if (!is_admin()) {{
        // Attempt to flush GoDaddy / WPaaS / object cache when ?flush_nrl_cache=1 is passed
        if (isset($_GET['flush_nrl_cache'])) {{
            if (function_exists('wp_cache_flush')) {{
                wp_cache_flush();
            }}
            if (class_exists('\\WPaaS\\Cache')) {{
                do_action('wpaas_purge_cache');
            }}
        }}
    }}
}});

add_filter('wp_get_custom_css', function ($css) {{
    return str_replace('content: "Sale " !important;', 'content: "Is " !important;', $css);
}}, 999);

// Rename "Shop" to "Gallery" across desktop and mobile nav menus (including PowerPack walker's <span class="menu-item-text">Shop<span class="pp-menu-toggle">)
add_filter('nav_menu_item_title', function ($title, $item, $args, $depth) {{
    $clean = trim(strip_tags($title));
    if ($clean === 'Shop') {{
        return 'Gallery';
    }}
    return $title;
}}, 20, 4);
add_filter('walker_nav_menu_start_el', function ($item_output, $item, $depth, $args) {{
    if (isset($item->title) && trim(strip_tags($item->title)) === 'Shop') {{
        $item_output = str_replace('>Shop<', '>Gallery<', $item_output);
        $item_output = str_replace('aria-label="Shop: submenu"', 'aria-label="Gallery: submenu"', $item_output);
    }}
    return $item_output;
}}, 999, 4);

// Also rename the WooCommerce Shop Archive breadcrumb / page heading if visited directly
add_filter('woocommerce_page_title', function ($page_title) {{
    if (trim($page_title) === 'Shop') {{
        return 'The Gallery';
    }}
    return $page_title;
}}, 20);
add_filter('get_the_archive_title', function ($title) {{
    if (function_exists('is_shop') && is_shop()) {{
        return 'The Gallery';
    }}
    return $title;
}}, 999);
add_filter('woocommerce_get_breadcrumb', function ($crumbs) {{
    if (is_array($crumbs)) {{
        foreach ($crumbs as &$crumb) {{
            if (isset($crumb[0]) && trim($crumb[0]) === 'Shop') {{
                $crumb[0] = 'Gallery';
            }}
        }}
    }}
    return $crumbs;
}}, 999);

// Force Yoast SEO, OpenGraph, Twitter Cards & WordPress oEmbed (Google Messages / iMessage Link Previews) to use the Chaphavian Marble Lady Hero (zero legacy green couch)
$chaphavian_og_hero = 'https://thechapmancollection.com/wp-content/uploads/2026/11/the-chaphavian-hero-2-5-scooch-lossless.png';
add_filter('wpseo_opengraph_image', function ($image) use ($chaphavian_og_hero) {{
    if (is_front_page() || is_home() || is_page(array(8, 10, 12, 16, 'about-us', 'services', 'contact-us'))) {{
        return $chaphavian_og_hero;
    }}
    return $image;
}}, 99999);
add_filter('wpseo_twitter_image', function ($image) use ($chaphavian_og_hero) {{
    if (is_front_page() || is_home() || is_page(array(8, 10, 12, 16, 'about-us', 'services', 'contact-us'))) {{
        return $chaphavian_og_hero;
    }}
    return $image;
}}, 99999);
add_filter('oembed_response_data', function ($data, $post) use ($chaphavian_og_hero) {{
    if ($post && in_array((int) $post->ID, array(8, 10, 12, 16), true)) {{
        $data['thumbnail_url'] = $chaphavian_og_hero;
        $data['thumbnail_width'] = 1792;
        $data['thumbnail_height'] = 756;
    }}
    return $data;
}}, 99999, 2);
add_action('wp_head', function () use ($chaphavian_og_hero) {{
    if (is_front_page() || is_home() || is_page(array(8, 10, 12, 16, 'about-us', 'services', 'contact-us'))) {{
        echo '<meta property="og:image" content="' . esc_url($chaphavian_og_hero) . '" />' . "\n";
        echo '<meta property="og:image:secure_url" content="' . esc_url($chaphavian_og_hero) . '" />' . "\n";
        echo '<meta property="og:image:width" content="1792" />' . "\n";
        echo '<meta property="og:image:height" content="756" />' . "\n";
        echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
        echo '<meta name="twitter:image" content="' . esc_url($chaphavian_og_hero) . '" />' . "\n";
    }}
}}, 1);

add_action('wp_head', function () {{
    if (is_admin()) {{
        return;
    }}
    echo '<link rel="preconnect" href="https://fonts.googleapis.com">';
    echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>';
    echo '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">';
    echo '<style id="nrl-chaphavian-global-css">' . base64_decode('{css_b64}') . '</style>';
}}, 999);

add_action('wp_footer', function () {{
    if (is_admin()) {{
        return;
    }}
    echo '<script id="nrl-chaphavian-footer-js">' . base64_decode('{js_b64}') . '</script>';
}}, 999);

add_filter('the_content', function ($content) {{
    if (is_admin() || !is_singular('page') || !in_the_loop() || !is_main_query()) {{
        return $content;
    }}
    if (is_page(10)) {{
        return base64_decode('{about_b64}');
    }}
    if (is_page(12)) {{
        return base64_decode('{services_b64}');
    }}
    if (is_page(16)) {{
        $c_html = base64_decode('{contact_b64}');
        $gf_html = do_shortcode('[gravityform id="1" title="false" description="false" ajax="true"]');
        return str_replace('__GRAVITY_FORM_1__', $gf_html, $c_html);
    }}
    return $content;
}}, 99999);
""".strip()


def ensure_lossless_hero_png_uploaded():
    search_url = f"{WP_BASE}/wp/v2/media?search=the-chaphavian-hero-2-5-scooch-lossless&per_page=5"
    existing = api_request(search_url)
    if existing and isinstance(existing, list):
        for item in existing:
            src = item.get("source_url", "")
            if "the-chaphavian-hero-2-5-scooch-lossless.png" in src:
                print(f"[MEDIA] Found untouched scooched lossless 1792x756 PNG hero: {src}")
                return src

    import io
    import numpy as np
    from PIL import Image, ImageFilter
    local_png = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college-rebranding\the-chaphavian-hero-2-5.png"
    im = Image.open(local_png).convert("RGB")
    arr = np.array(im, dtype=np.float32)

    # Coons-patch + Venetian plaster grain inpainting to scooch "The Chapman Collection / Refreshing Our Digital Gallery" down 64px (6.35%)
    y0, y1, x0, x1 = 310, 605, 370, 1020
    h, w = y1 - y0, x1 - x0
    left_strip = arr[y0:y1, x0 - 25:x0].mean(axis=1, keepdims=True)
    right_strip = arr[y0:y1, x1:x1 + 25].mean(axis=1, keepdims=True)
    t_x = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :, None]
    bg_horiz = left_strip * (1.0 - t_x) + right_strip * t_x

    top_strip = arr[y0 - 20:y0, x0:x1].mean(axis=0, keepdims=True)
    bot_strip = arr[y1:y1 + 20, x0:x1].mean(axis=0, keepdims=True)
    t_y = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None, None]
    bg_vert = top_strip * (1.0 - t_y) + bot_strip * t_y
    bg_low = 0.55 * bg_horiz + 0.45 * bg_vert

    clean_below_im = im.crop((x0, 615, x1, 615 + h))
    clean_below = np.array(clean_below_im, dtype=np.float32)
    clean_below_low = np.array(clean_below_im.filter(ImageFilter.GaussianBlur(14)), dtype=np.float32)
    grain = clean_below - clean_below_low

    roi = arr[y0:y1, x0:x1]
    diff = np.clip(bg_low.mean(axis=-1) - roi.mean(axis=-1), 0, None)
    ink_mask = np.clip((diff - 5.5) / 7.5, 0.0, 1.0)
    ink_mask_im = Image.fromarray((ink_mask * 255).astype(np.uint8))
    heal_mask = np.clip(
        np.array(ink_mask_im.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2.5)), dtype=np.float32)
        / 255.0
        * 1.6,
        0.0,
        1.0,
    )[..., None]

    healed_roi = roi * (1.0 - heal_mask) + (bg_low + grain) * heal_mask
    ink_ratio = np.clip(roi / np.maximum(bg_low, 1.0), 0.0, 1.0)
    ink_transmission = 1.0 - ink_mask[..., None] * (1.0 - ink_ratio)

    arr_clean = arr.copy()
    arr_clean[y0:y1, x0:x1] = healed_roi

    shift = 64
    dest_roi = arr_clean[y0 + shift:y1 + shift, x0:x1]
    arr_clean[y0 + shift:y1 + shift, x0:x1] = np.clip(dest_roi * ink_transmission, 0, 255)

    out_im = Image.fromarray(arr_clean.astype(np.uint8)).resize((1792, 756), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    out_im.save(buf, format="PNG", optimize=True)
    png_bytes = buf.getvalue()

    res = api_request(
        f"{WP_BASE}/wp/v2/media",
        method="POST",
        raw_bytes=png_bytes,
        content_type="image/png",
        extra_headers={
            "Content-Disposition": 'attachment; filename="the-chaphavian-hero-2-5-scooch-lossless.png"'
        },
    )
    url = res.get("source_url")
    media_id = res.get("id")
    print(f"[MEDIA] Uploaded untouched scooched lossless 1792x756 PNG hero (ID {media_id}): {url}")
    return url


def main():
    showroom_url = ensure_showroom_photo_uploaded()
    about_html = build_about_us_html(showroom_url)
    services_html = build_services_html()
    contact_html = build_contact_us_html(showroom_url)

    # 1. Update post_content on Page 10 and Page 12 for SEO / crawlers
    p10 = api_request(
        f"{WP_BASE}/wp/v2/pages/10",
        method="POST",
        data={
            "content": about_html,
        },
    )
    print(f"[WP PAGE 10] Updated /about-us/ post_content (modified={p10.get('modified')})")

    p12 = api_request(
        f"{WP_BASE}/wp/v2/pages/12",
        method="POST",
        data={
            "content": services_html,
        },
    )
    print(f"[WP PAGE 12] Updated /services/ post_content (modified={p12.get('modified')})")

    # 2. Find Code Snippet #25
    snippets = api_request(f"{WP_BASE}/code-snippets/v1/snippets")
    target_snippet_id = None
    for s in snippets:
        if "Chaphavian Editorial Upgrade" in s.get("name", ""):
            target_snippet_id = s.get("id")
            break

    # 3. Pre-deploy Snippet #25 in global scope to disable WP Smush png_to_jpg/lossy before uploading lossless PNG
    temp_url = "https://thechapmancollection.com/wp-content/uploads/2026/11/the-chaphavian-hero-2-5.jpg"
    pre_php = build_snippet_25_php(
        about_html,
        services_html,
        contact_html,
        CHAPHAVIAN_CSS.replace("__WELCOME_ALCOVE_URL__", temp_url),
        FOOTER_POLISH_JS.replace("__WELCOME_ALCOVE_URL__", temp_url),
    )
    pre_payload = {
        "name": "NRL Chaphavian Editorial Upgrade (/about-us/ & /services/ Preferred Shippers)",
        "code": pre_php,
        "scope": "global",
        "priority": 10,
        "active": True,
    }
    if target_snippet_id:
        res = api_request(f"{WP_BASE}/code-snippets/v1/snippets/{target_snippet_id}", method="PUT", data=pre_payload)
    else:
        res = api_request(f"{WP_BASE}/code-snippets/v1/snippets", method="POST", data=pre_payload)
        target_snippet_id = res.get("id")

    # 4. Now upload or locate the untouched lossless 1792x756 PNG master
    welcome_alcove_url = ensure_lossless_hero_png_uploaded() + "?v=2"
    print(f"[MEDIA] Active Homepage Hero URL: {welcome_alcove_url}")

    # Set Page 8 (Homepage) featured_media to 3369 so Yoast SEO & oEmbed permanently index the Chaphavian Marble Lady Hero instead of the legacy green couch
    try:
        p8 = api_request(f"{WP_BASE}/wp/v2/pages/8", method="POST", data={"featured_media": 3369})
        print(f"[WP PAGE 8] Updated Homepage featured_media={p8.get('featured_media')} (modified={p8.get('modified')})")
    except Exception as e:
        print(f"[WP PAGE 8] Warning updating featured_media: {e}")

    compiled_css = CHAPHAVIAN_CSS.replace("__WELCOME_ALCOVE_URL__", welcome_alcove_url)
    compiled_js = FOOTER_POLISH_JS.replace("__WELCOME_ALCOVE_URL__", welcome_alcove_url)
    php_code = build_snippet_25_php(about_html, services_html, contact_html, compiled_css, compiled_js)
    payload = {
        "name": "NRL Chaphavian Editorial Upgrade (/about-us/ & /services/ Preferred Shippers)",
        "code": php_code,
        "scope": "global",
        "priority": 10,
        "active": True,
    }
    res = api_request(f"{WP_BASE}/code-snippets/v1/snippets/{target_snippet_id}", method="PUT", data=payload)
    print(f"[CODE SNIPPET #{target_snippet_id}] Updated & Active: {res.get('name')} (active={res.get('active')})")


if __name__ == "__main__":
    main()
