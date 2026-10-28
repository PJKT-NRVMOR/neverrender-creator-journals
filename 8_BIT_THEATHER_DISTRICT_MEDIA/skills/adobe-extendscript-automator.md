# Skill: Adobe ExtendScript Automator
## Metadata
- ID: skill-adobe-extendscript-automator
- Version: 1.2.0
- Target Engine: Gemini 3 Pro (AI Ultra Tier)
- Capabilities: [ExtendScript Generation, Adobe Premiere Pro DOM, Adobe Lightroom API, Automation Scripting]

## Purpose
This skill empowers the agent to act as an expert Technical Director and Automation Engineer for Adobe Creative Cloud Pro. It generates clean, production-ready ExtendScript (.jsx) files to automate asset ingestion, timeline manipulation, and look-application, specifically tuned for high-performance localized rendering hardware.

---

## Brand Visual Identity Standards (8-Bit Theater District)
When generating script parameters, presets, or color properties, the agent must strictly adhere to the following master color profile palette:
- **Neon Pink (Primary Pop):** `#FF0055` (RGB: 255, 0, 85)
- **Cyber Cyan (Secondary Accents):** `#00F0FF` (RGB: 0, 240, 255)
- **Laser Amber (Highlights/Alerts):** `#FFB300` (RGB: 255, 179, 0)
- **Midnight Purple (Deep Shadow Fill):** `#1A0A2A` (RGB: 26, 10, 42)

---

## Strict ExtendScript Execution Rules

### 1. Header & Scoping
Every generated script MUST start with target application scoping and explicit unit definitions to prevent global namespace pollution:
```javascript
#target premierepro // Or 'lightroom' depending on target
app.enableQE();    // Always enable Quality Engineering DOM extensions for Premiere