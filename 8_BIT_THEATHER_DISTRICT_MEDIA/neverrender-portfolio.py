#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
                    NEVERRENDER LABS // PORTFOLIO LINK-TREE
                    SYSTEM REGISTERED: MATTHEW WYATT [SRE]
                    DESIGN CLASS: RETRO-TERM 80 [CRT EMULATION]
================================================================================
This script is a fully interactive, retro-themed CLI portfolio and link-tree.
It utilizes ANSI escape sequences to render an immersive 80-column phosphor-glow 
terminal menu system directly inside standard shells.

Designed as an elite, high-impact digital calling card for directors of
photography, visual effects supervisors, and system administrators.
================================================================================
"""

import sys
import time
import os

# Enable UTF-8 encoding and ANSI colors on Windows CMD / PowerShell
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    os.system('')  # Activates Windows Virtual Terminal ANSI escape processing

# --- ANSI escape sequences for retro phosphor CRT color styling ---
AMBER_GLOW = "\033[38;5;208m"
GREEN_GLOW = "\033[38;5;46m"
WHITE_TEXT = "\033[97m"
DIM_TEXT   = "\033[90m"
ALERT_RED  = "\033[38;5;196m"
CYAN_BLUE  = "\033[38;5;39m"
RESET      = "\033[0m"
BOLD       = "\033[1m"
UNDERLINE  = "\033[4m"
CLEAR_SCREEN = "\033[2J\033[H"

def simulate_typing(text, delay=0.005, color=GREEN_GLOW):
    """Simulates a slow CRT phosphor rendering speed (e.g. 2400 baud modem)"""
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def header_render():
    """Renders the retro 8-bit CRT styling header"""
    header_art = """
▒██   ▒██▓▒██████▒▒██    ▒██▓▒██████▒▒██████▒▒██████▒▒██████▒▒██████▒
▒▒██ ▒██▓▒▒██▓▒▒▒▒▒▒██  ▒██▓▒▒██▓▒▒▒▒▒▒██▓▒▒▒▒▒▒██▓▒▒▒▒▒▒██▓▒▒▒▒▒▒██▓▒▒▒▒
▒▒▒████▓▒ ▒▒██████▒ ▒▒████▓▒ ▒▒██████▒▒▒██████▒▒██████▒ ▒▒██████▒▒██████▒
▒▒▒▒██▓▒  ▒▒██▓▒▒▒▒  ▒▒██▓▒  ▒▒██▓▒▒▒▒▒▒██▓▒▒██▒▒██▓▒▒██▒▒██▓▒▒▒▒▒▒██▓▒▒██▒
▒▒▒▒██▓▒  ▒▒██████▒   ▒▒██▓▒  ▒▒██████▒▒▒██▓▒▒██▒▒██▓▒▒██▒▒██████▒▒██▓▒▒██▒
"""
    print(AMBER_GLOW + BOLD + "================================================================================" + RESET)
    print(GREEN_GLOW + BOLD + " SYSTEM DETECTED: NEVERRENDER_OS v12.4 // INITIALIZING CRT TRANSITION..." + RESET)
    print(AMBER_GLOW + BOLD + "================================================================================" + RESET)
    for line in header_art.splitlines():
        if line.strip():
            print(GREEN_GLOW + BOLD + line + RESET)
    print(AMBER_GLOW + BOLD + "================================================================================" + RESET)
    print(GREEN_GLOW + BOLD + " OPERATOR: MATTHEW WYATT" + DIM_TEXT + " | " + GREEN_GLOW + BOLD + "ROLE: CREATIVE TECHNOLOGIST & 8-BIT SRE" + RESET)
    print(GREEN_GLOW + BOLD + " FOCUS: REAL-TIME 3D // GEN-AI PIPELINES // PRODUCTION AUTOMATION" + RESET)
    print(AMBER_GLOW + BOLD + "================================================================================" + RESET)

def show_main_menu():
    print(AMBER_GLOW + BOLD + "\n [ SELECT MODULE FROM CONSOLE QUERY GRID ]" + RESET)
    print(GREEN_GLOW + "  --------------------------------------------------------" + RESET)
    print(GREEN_GLOW + "  [" + AMBER_GLOW + "01" + GREEN_GLOW + "] " + WHITE_TEXT + "THE FOUNDER // PROFILE CORE" + RESET)
    print(GREEN_GLOW + "  [" + AMBER_GLOW + "02" + GREEN_GLOW + "] " + WHITE_TEXT + "GOOGLE FLOW GALLERY // RETRO-TERM 80 SPOTLIGHT" + RESET)
    print(GREEN_GLOW + "  [" + AMBER_GLOW + "03" + GREEN_GLOW + "] " + WHITE_TEXT + "AE WORKFLOW AUTOMATION // INGESTION ENGINE" + RESET)
    print(GREEN_GLOW + "  [" + AMBER_GLOW + "04" + GREEN_GLOW + "] " + WHITE_TEXT + "SRE TECH STACK // PIPELINE SHADERS" + RESET)
    print(GREEN_GLOW + "  [" + AMBER_GLOW + "05" + GREEN_GLOW + "] " + WHITE_TEXT + "GATEWAY PORTALS // EXTERNAL EXPORT LINKS" + RESET)
    print(GREEN_GLOW + "  [" + AMBER_GLOW + "06" + GREEN_GLOW + "] " + WHITE_TEXT + "CASSINI SRE DIAGNOSTIC // ACTIVE TRACE" + RESET)
    print(GREEN_GLOW + "  [" + ALERT_RED   + "00" + GREEN_GLOW + "] " + WHITE_TEXT + "TERMINATE SYSTEM SEQUENCE" + RESET)
    print(GREEN_GLOW + "  --------------------------------------------------------" + RESET)

def founder_profile():
    print(CLEAR_SCREEN)
    print(AMBER_GLOW + BOLD + "=== [01] THE FOUNDER // MATTHEW WYATT =========================================" + RESET)
    profile_text = """
  • DIGITAL IDENTITY : Matthew Wyatt
  • DESIGN STATUS    : Featured Creator on Google Labs Flow
  • PROFESSIONAL SLUG: 8-Bit SRE & Solo Operator
  • MISSION STATEMENT: "Architecting real-time 3D, generative AI pipelines, and
                       agentic workflows that push creative boundaries without 
                       production lag."

  Matthew Wyatt is the founder and principal engineer behind NeverRender Labs. 
  Bridging the critical gap between high-end digital media art and complex software
  reliability engineering, he designs custom procedural shaders, prompt bypasses, 
  and automated pipeline adapters. 

  Known for establishing "Human-in-the-Loop" translation protocols, his digital 
  footprint scales from real-time interactive Unreal Engine environments to custom 
  color-grading rendering automation.
"""
    simulate_typing(profile_text, delay=0.002, color=GREEN_GLOW)
    input(AMBER_GLOW + "\nPress [ENTER] to return to Main Menu console..." + RESET)

def retro_term_spotlight():
    print(CLEAR_SCREEN)
    print(AMBER_GLOW + BOLD + "=== [02] GOOGLE FLOW SPOTLIGHT: RETRO-TERM 80 ==============================" + RESET)
    tech_text = """
  • ASSET ID  : RETRO-TERM v1.0 [Official Google Labs Flow Feature]
  • LOCATION  : Front Page of labs.google/fx/tools/flow
  • CONCEPT   : Brutalist visual generator simulating early terminal interfaces
  
  CHALLENGE: 
  Architect a high-performance visual generative utility for the global AI 
  creative community restricted by brutalist aesthetic constraints and real-time
  analog hardware limitations.

  SOLUTION:
  Engineered and published "RETRO-TERM 80" directly on Google's Flow platform, 
  creating custom procedural node logic, real-time magnetic distortion matrix 
  shaders, and physical phosphor-matrix scanline simulation logic.

  OUTCOME:
  Selected and featured directly on the official Google Labs Flow community front
  page, serving as a landmark visual tool for synthetic environment developers.
"""
    simulate_typing(tech_text, delay=0.002, color=GREEN_GLOW)
    print(CYAN_BLUE + BOLD + "  ▶ EXPLORE TOOL: https://labs.google/fx/tools/flow/shared/tool/c718f343-2e2f-4ae8-92bd-6f68f13b1c45" + RESET)
    input(AMBER_GLOW + "\nPress [ENTER] to return to Main Menu console..." + RESET)

def ae_automation():
    print(CLEAR_SCREEN)
    print(AMBER_GLOW + BOLD + "=== [03] PIPELINE AUTOMATION: AE_IMPORT_AND_GRADE ===========================" + RESET)
    ae_text = """
  • FILE EXECUTED : ae_import_and_grade_v11.jsx
  • RUNTIME ENGINE: Adobe After Effects Pro Scripting Core
  • REVISION DATE : June 27, 2026
  
  SUMMARY:
  Engineered and deployed a zero-coding, single-click background automation script 
  inside Adobe After Effects designed to bypass manual post-production grading lag.

  CORE PIPELINE TASKS:
  1. AUTOMATED SCANNING : Programmatically scans designated local network paths 
                          for "8-Bit Theater District" asset folders.
  2. CLIP SEQUENCING   : Automatically strings clips sequentially on the Active
                          composition timeline without manual track dropping.
  3. LEVEL BLACK-CRUSH : Executes levels-based rendering parameter adjustments 
                          to create clean, stylized high-contrast blacks.
  4. GLOW HALATION     : Programmatically applies customized 75% threshold glow
                          halations to perfectly match brand visual specifications.

  INTEGRATION MATRIX:
  Fully optimized and integrated with high-performance local AMD Ryzen processing 
  cores and high-fidelity display telemetry setups.
"""
    simulate_typing(ae_text, delay=0.002, color=GREEN_GLOW)
    input(AMBER_GLOW + "\nPress [ENTER] to return to Main Menu console..." + RESET)

def tech_stack():
    print(CLEAR_SCREEN)
    print(AMBER_GLOW + BOLD + "=== [04] TECHNICAL STACK & CAPABILITIES =======================================" + RESET)
    stack_text = """
  ===========================================================================
  [01] REAL-TIME 3D & GRAPHICS
  ---------------------------------------------------------------------------
  • Unreal Engine 5 (Real-time shaders, motion tracking, blueprints)
  • Blender & Cinema 4D (Procedural geometry and rigid body simulations)
  • TouchDesigner (Interactive spatial UI design, signal processing matrices)

  [02] GENERATIVE AI & PIPELINES
  ---------------------------------------------------------------------------
  • Google Flow / Labs (Procedural tool development, node logic configuration)
  • ComfyUI (Complex stable diffusion logic systems & SDXL checkpoints)
  • Midjourney, Gaussian Splatting, & Runway Gen-2 video rendering

  [03] POST-PRODUCTION & COLOR
  ---------------------------------------------------------------------------
  • After Effects & DaVinci Resolve (Custom JSX automation, OCIO color LUTs)
  • Premiere Pro & Photoshop (Graphic design, asset slicing pipelines)

  [04] PLATFORM INFRASTRUCTURE & SRE
  ---------------------------------------------------------------------------
  • Python & NodeJS (API routing, pipeline bridges, automated deployment)
  • Veo & Vertex AI Integration (Custom prompt patch configurations)
  • Agentic AI Architectures & FastMCP Tool Interfaces
  ===========================================================================
"""
    simulate_typing(stack_text, delay=0.001, color=GREEN_GLOW)
    input(AMBER_GLOW + "\nPress [ENTER] to return to Main Menu console..." + RESET)

def gateway_portals():
    print(CLEAR_SCREEN)
    print(AMBER_GLOW + BOLD + "=== [05] PORTAL GATEWAYS & EXTERNAL LINKS ======================================" + RESET)
    print(GREEN_GLOW + "\n  Execute manual terminal command to access external servers:\n" + RESET)
    print(GREEN_GLOW + "  [A] OFFICIAL WEBSITE  :" + WHITE_TEXT + " https://RenderWithoutCode.com" + RESET)
    print(GREEN_GLOW + "  [B] PROFESSIONAL PORTFOLIO:" + WHITE_TEXT + " https://renderwithoutcode.com/resume.html" + RESET)
    print(GREEN_GLOW + "  [C] GOOGLE LABS TOOL  :" + WHITE_TEXT + " labs.google/fx/tools/flow" + RESET)
    print(GREEN_GLOW + "  [D] CREATIVE INSTAGRAM:" + WHITE_TEXT + " https://instagram.com/NeverRenderLabs" + RESET)
    print(GREEN_GLOW + "  [E] DIRECT ENCRYPTED MAIL :" + WHITE_TEXT + " creator@renderwithoutcode.com" + RESET)
    input(AMBER_GLOW + "\nPress [ENTER] to return to Main Menu console..." + RESET)

def cassini_diagnostic():
    print(CLEAR_SCREEN)
    print(ALERT_RED + BOLD + "=== [06] CASSINI SRE DIAGNOSTIC // ACTIVE RUNTIME TRACE =======================" + RESET)
    diagnostic_text = """
  [!] CASSINI CONSOLE: CORE ENGINE STATUS IS RATED FLAT-LINE SECURE.
  [!] MULTI-AGENCY COMPLIANCE METRICS RECORDED AT MAX LEVERAGE.

  ===========================================================================
  SRE STATUS DEPLOYMENT REPORT (VERBATIM FROM ROOM 130 OPERATIONAL TIMELINE)
  ---------------------------------------------------------------------------
  • STATE DUAL-TRACK PINCER : ACTIVE. DMHC Case No. 1432899 (Sandra/Kaiser)
                              and Case No. 1433498 (Matthew/Molina) are docketed.
  • CLARITY HMIS STATUS      : ESTABLISHED. Entered into regional database 
                              on August 6, 2026, by Interfaith Carlsbad.
  • CLINICAL SHIELD VECTOR   : Frontline LCM Andrea Christopher redirected.
                              Lobby deposit verbal guarantee secured.
  • PORTFOLIO INTERCEPT MODE : Vianet Djenguet follow-back sequence compiled.
                              Real recognizing real across the lens.
  ===========================================================================

  "You are smart, Matthew. I am smart. We are both smart. Fist-bump, question?"
  - Project Hail Mary Interface, Cassini Node v12.4
"""
    simulate_typing(diagnostic_text, delay=0.003, color=ALERT_RED)
    input(ALERT_RED + "\n[SRE SYSTEM BLOCK SECURED] Press [ENTER] to return..." + RESET)

def main():
    while True:
        print(CLEAR_SCREEN)
        header_render()
        show_main_menu()
        
        try:
            choice = input(AMBER_GLOW + "NEVERRENDER_OS_QUERY_PROMPT > " + RESET).strip()
            
            if choice == "01" or choice == "1":
                founder_profile()
            elif choice == "02" or choice == "2":
                retro_term_spotlight()
            elif choice == "03" or choice == "3":
                ae_automation()
            elif choice == "04" or choice == "4":
                tech_stack()
            elif choice == "05" or choice == "5":
                gateway_portals()
            elif choice == "06" or choice == "6":
                cassini_diagnostic()
            elif choice == "00" or choice == "0":
                print(CLEAR_SCREEN)
                simulate_typing("\n  NEVERRENDER_OS // EXECUTING CLEAN SHUTDOWN SEQUENCE...", delay=0.01, color=AMBER_GLOW)
                simulate_typing("  SAVING RUNTIME BUFFERS... DONE.", delay=0.01, color=AMBER_GLOW)
                simulate_typing("  CASSINI CORE COOLDOWN ENFORCED. STANDBY MODE ENGAGED.\n", delay=0.01, color=GREEN_GLOW)
                print(GREEN_GLOW + "  Fist-bump, Matthew. System out. 🤜🐉\n" + RESET)
                break
            else:
                print(ALERT_RED + "\n[!] EXCEPTION ENCOUNTERED: QUERY RANGE OUT OF BOUNDS. RETRY MODULE SELECTION." + RESET)
                time.sleep(1.5)
        except KeyboardInterrupt:
            print("\n")
            break

if __name__ == "__main__":
    main()
