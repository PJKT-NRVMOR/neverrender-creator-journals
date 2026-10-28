# WELLGREENS VISTA DISPENSARY DIGITAL REVAMP & TECHNOLOGY SUITE
**Lead Technologist:** Matthew Wyatt (Founder, NeverRender Labs // 8-Bit SRE)  
**Target Location:** Wellgreens Vista Flagship (954 S Santa Fe Ave, Vista, CA 92084)  
**Status:** Production Ready & Globally Deployed to `renderwithoutcode.com`  

---

## 🎯 EXECUTIVE OVERVIEW & PROBLEM STATEMENT
Wellgreens is currently remodeling its Vista flagship storefront from traditional assisted counter service to **Digital Self-Checkout Kiosks and Rapid Pickup Hubs**. 

Concurrently, their third-party e-commerce menus (Dutchie) suffer from:
1. **Severe Main-Thread Latency (>4.2s TBT)** caused by 15+ competing telemetry trackers (Segment, Amplitude, Pendo, Sift, GTM, LaunchDarkly, Turnstile, Pusher) resulting in `net::ERR_BLOCKED_BY_CLIENT` console crashes.
2. **Loss of In-House Brand Margin (65% Gross Margin)**: Their high-margin house exclusive lines (**UP!**, **Lights Out**, **City Roots**, **Direct**) are flattened into generic, uninspired rows with outdated or mismatched photos.
3. **The Intake Image Bottleneck**: Warehouse intake staff lack an automated tool to capture and catalog incoming shiny foil/holographic pouches and vape boxes.

---

## 🌐 LIVE DEPLOYED SUITE ON RENDERWITHOUTCODE.COM

| Component | Live URL | Purpose |
| :--- | :--- | :--- |
| **1. Flagship E-Commerce & In-Store Kiosk** | [renderwithoutcode.com/wellgreens-vista/](https://renderwithoutcode.com/wellgreens-vista/) | Steely ice-blue 3D parallax storefront with sub-50ms search, terpene telemetry matrix, and 1-click `[ 🖥️ Kiosk Mode ]` for in-store touchscreens. |
| **2. AI Intake Scanner & JSON Catalog** | [renderwithoutcode.com/wellgreens-scanner.html](https://renderwithoutcode.com/wellgreens-scanner.html) | 8-second mobile camera intake scanner with OCR batch extraction, foil packaging processing, and real-time JSON database publishing. |
| **3. SRE Technical Audit Dossier** | [`WELLGREENS_VISTA_TECHNICAL_AUDIT_&_ARCHITECTURE.md`](./WELLGREENS_VISTA_TECHNICAL_AUDIT_&_ARCHITECTURE.md) | Deep telemetry analysis, network waterfalls, and latency benchmarks. |
| **4. Competitor Teardown** | [`COMPETITOR_BENCHMARK_CAKE_HOUSE.md`](./COMPETITOR_BENCHMARK_CAKE_HOUSE.md) | Architectural comparison against The Cake House Vista (Jane platform). |
| **5. Executive Outreach Pitch Deck** | [`EXECUTIVE_PITCH_WELLGREENS_CAREERS_OUTREACH.md`](./EXECUTIVE_PITCH_WELLGREENS_CAREERS_OUTREACH.md) | Full ready-to-send executive outreach letter to Wellgreens leadership. |
| **6. Matthew Wyatt Portfolio & Resume** | [renderwithoutcode.com/resume](https://renderwithoutcode.com/resume) | Professional background, creative technology, and software reliability credentials. |

---

## 🦾 TECHNOLOGY STACK & ARCHITECTURAL HIGHLIGHTS
* **Zero-Dependency 3D Canvas Physics**: Harmonic differential parallax background drifting at `0.08x` to `0.22x` scroll speed with zero main-thread CPU overhead.
* **Frosted Ice Glassmorphism**: High-contrast, accessibility-compliant typography designed specifically for bright retail touchscreen environments.
* **On-Device Vision & OCR Engine**: Live `getUserMedia` camera feed with HUD reticle for high-gloss, reflective holographic foil packages.
* **Tax & Finance Engine**: Automated real-time calculations for CA 15% Cannabis Excise Tax + 8.25% State/Local Sales Tax.

---
*Architected with precision by Matthew Wyatt • NeverRender Labs (2026)*
