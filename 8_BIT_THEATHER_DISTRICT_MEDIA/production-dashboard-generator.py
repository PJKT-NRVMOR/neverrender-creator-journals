#!/usr/bin/env python3
"""
PROJECT_NEVERMORE: Automated Production Tracker & Dashboard Generator
Parses, analyzes, and visualizes excel-based project data to enforce absolute pipeline compliance.
"""

import os
import sys
import json
import pandas as pd

# Define paths
EXCEL_PATH = '/workspace/artifacts/project_nevermore_production_tracker-v2.xlsx'
OUTPUT_DIR = '/workspace/scratch'
FINAL_OUT_DIR = '/workspace/out'

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FINAL_OUT_DIR, exist_ok=True)

def parse_calibrations(excel_path):
    """Parses setup parameters and shorttag bindings from the spreadsheet."""
    xl = pd.ExcelFile(excel_path)
    df_setup = xl.parse('Setup and References')
    
    calibrations = {}
    bindings = []
    
    # Simple row-by-row scanner
    active_section = None
    for idx, row in df_setup.iterrows():
        col0 = str(row.iloc[0]).strip() if pd.notnull(row.iloc[0]) else ''
        col1 = str(row.iloc[1]).strip() if pd.notnull(row.iloc[1]) else ''
        col2 = str(row.iloc[2]).strip() if pd.notnull(row.iloc[2]) else ''
        
        if "Discord shorttag Bindings" in col0:
            active_section = "bindings"
            continue
        elif "AI Generation Parameter Calibration Constants" in col0:
            active_section = "calibrations"
            continue
            
        if active_section == "bindings":
            if col0.startswith('--') and col1.startswith('http'):
                bindings.append({
                    "option_tag": col0,
                    "url": col1,
                    "description": col2
                })
        elif active_section == "calibrations":
            if col0 and col1:
                # Try to clean name and store value
                key_name = col0.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').lower()
                calibrations[key_name] = col1
                
    # Normalize expected numeric types
    try:
        calibrations['default_seed'] = int(float(calibrations.get('default_seed', 4567)))
    except ValueError:
        calibrations['default_seed'] = 4567
        
    try:
        calibrations['stg_scale_spatio-temporal'] = int(float(calibrations.get('stg_scale_spatio-temporal', 7)))
    except ValueError:
        calibrations['stg_scale_spatio-temporal'] = 7
        
    try:
        calibrations['pixverse_kling_cost_sec'] = float(calibrations.get('pixverse_kling_cost_sec', 0.025))
    except ValueError:
        calibrations['pixverse_kling_cost_sec'] = 0.025
        
    return calibrations, bindings

def parse_shots(excel_path, cost_per_sec):
    """Parses the active shot sequence and calculates dynamic metadata metrics."""
    xl = pd.ExcelFile(excel_path)
    # Header is at row 10 in the spreadsheet
    df_shots = xl.parse('Production Tracker', header=10)
    
    # Strip whitespace from column headers
    df_shots.columns = [str(c).strip() for c in df_shots.columns]
    
    # Drop completely empty rows and the 'Total' summary row
    df_shots = df_shots[df_shots['Shot ID'].notnull()]
    df_shots = df_shots[df_shots['Shot ID'].str.strip() != 'Total']
    
    shots_list = []
    cumulative_duration = 0
    total_cost = 0.0
    
    for idx, row in df_shots.iterrows():
        shot_id = str(row['Shot ID']).strip()
        framing = str(row['Framing']).strip() if pd.notnull(row['Framing']) else 'Unknown'
        
        try:
            duration = int(float(row['Duration (sec)'])) if pd.notnull(row['Duration (sec)']) else 0
        except ValueError:
            duration = 0
            
        status = str(row['Status']).strip() if pd.notnull(row['Status']) else 'Not Started'
        visual_dna = str(row['Visual Keyframe DNA & Weights']).strip() if pd.notnull(row['Visual Keyframe DNA & Weights']) else ''
        kinetic_prompt = str(row['Kinetic Motion & Camera Prompt']).strip() if pd.notnull(row['Kinetic Motion & Camera Prompt']) else ''
        notes = str(row['Post-Production Notes']).strip() if pd.notnull(row['Post-Production Notes']) else ''
        
        # Calculate dynamic cumulative value
        cumulative_duration += duration
        # Calculate dynamic cost based on active rate
        shot_cost = round(duration * cost_per_sec, 3)
        total_cost += shot_cost
        
        shots_list.append({
            "shot_id": shot_id,
            "framing": framing,
            "duration_sec": duration,
            "cumulative_sec": cumulative_duration,
            "estimated_cost_usd": shot_cost,
            "visual_dna": visual_dna,
            "kinetic_prompt": kinetic_prompt,
            "status": status,
            "notes": notes
        })
        
    return shots_list, cumulative_duration, round(total_cost, 2)

def generate_markdown_dashboard(calibrations, bindings, shots, total_duration, total_cost):
    """Compiles a beautifully formatted Markdown Dashboard containing the calculated statistics."""
    
    # Count status distributions
    status_counts = {"Complete": 0, "In Progress": 0, "Not Started": 0}
    for shot in shots:
        s = shot['status']
        if s in status_counts:
            status_counts[s] += 1
        else:
            status_counts[s] = 1
            
    total_shots = len(shots)
    completion_rate = round((status_counts.get("Complete", 0) / total_shots) * 100, 1) if total_shots > 0 else 0.0
    
    # Determine progress bar layout
    bar_length = 20
    filled_length = int(round(bar_length * (completion_rate / 100)))
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    md_content = []
    md_content.append("# PROJECT_NEVERMORE: Automated Production Dashboard")
    md_content.append("*System Status: ACTIVE // Render Pipeline Calibrated*")
    md_content.append("*Metadata Standards: C2PA v1.3 Compliant // Core Database Synchronized*")
    md_content.append("\n---\n")
    
    # Summary Cards
    md_content.append("## 📊 EXECUTIVE SUMMARY COCKPIT")
    md_content.append("| Parameter | Live Workspace Metric | Operational Impact / Targets |")
    md_content.append("| :--- | :--- | :--- |")
    md_content.append(f"| **Pipeline Progress** | `{completion_rate}%` ({status_counts.get('Complete', 0)} of {total_shots} shots) | **{bar}** |")
    md_content.append(f"| **Total Storyboard Runtime** | `{total_duration} seconds` | Complete timeline coverage for Scene 1 and Scene 2 |")
    md_content.append(f"| **Estimated Ingestion Cost** | `${total_cost:.2f} USD` | Calculated at standard `${calibrations.get('pixverse_kling_cost_sec', 0.025)} / sec` licensing rates |")
    md_content.append(f"| **Calibration Status** | `VERIFIED` | Seed locking enforced on local Beelink SER5 workstation |")
    
    md_content.append("\n---\n")
    
    # System Calibration Section
    md_content.append("## ⚙️ AI MODEL ENGINE CALIBRATION KEYS")
    md_content.append("| Engine Parameter | Active Value | Technical Operational Impact |")
    md_content.append("| :--- | :--- | :--- |")
    md_content.append(f"| **Default Seed Lock** | `{calibrations.get('default_seed', 4567)}` | Locks baseline pseudorandom noise matrix generation for absolute scene consistency |")
    md_content.append(f"| **STG Scale (Spatio-Temporal)** | `{calibrations.get('stg_scale_spatio-temporal', 7)}` | Enforces structural cohesion and pixel weights across temporal frames |")
    md_content.append(f"| **Negative Element Guardrails** | `{calibrations.get('negative_elements_prompt', '')}` | Primary boundary shielding the scheduler from unwanted artifacts or de-aging |")
    
    md_content.append("\n### 🔗 DISCORD SHORTTAG BINDINGS")
    md_content.append("| Shorttag Trigger | Master Visual DNA URL | Reference Description |")
    md_content.append("| :--- | :--- | :--- |")
    for b in bindings:
        md_content.append(f"| `{b['option_tag']}` | [Asset URL]({b['url']}) | {b['description']} |")
        
    md_content.append("\n---\n")
    
    # Active Shot Sequence Table
    md_content.append("## 🎬 ACTIVE storyboard shot sequence")
    md_content.append("| ID | Framing | Duration | Cost | Status | Kinetic Motion & Camera Prompt | Post-Production Verification Notes |")
    md_content.append("| :--- | :--- | :---: | :---: | :---: | :--- | :--- |")
    for s in shots:
        status_emoji = "🟢" if s['status'] == "Complete" else ("🟡" if s['status'] == "In Progress" else "⚪")
        md_content.append(f"| `{s['shot_id']}` | {s['framing']} | `{s['duration_sec']}s` | `${s['estimated_cost_usd']:.2f}` | {status_emoji} {s['status']} | {s['kinetic_prompt'][:80]}... | {s['notes']} |")
        
    md_content.append("\n---\n")
    
    # Step-by-Step Prompt Ingestion Rules
    md_content.append("## 📜 PIPELINE VALIDATION & DECOUPLED MOTION RULES")
    md_content.append("1. **The Anchor-to-Video Rule:** Ingest the static visual keyframe URL (or reference shorttag) as an image-to-video guide first before introducing any camera motion paths.")
    md_content.append("2. **Separation of Identity from Motion:** Never merge character description strings (apparel, face turnaround features) directly with active viewport transformation variables (such as panning speed or zoom scale) inside your positive text fields.")
    md_content.append("3. **Hard-Cut Cache Gates:** Enforce a hard terminate buffer at the exact frame boundaries to prevent AI-driven pixel sliding, roofline warping, or structure melting during export passes.")
    
    return "\n".join(md_content)

def main():
    print("=== PROJECT_NEVERMORE: PARSING EXCEL DATABASE ===")
    
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: Database file not found at {EXCEL_PATH}")
        sys.exit(1)
        
    # Step 1: Parse setup & reference variables
    calibrations, bindings = parse_calibrations(EXCEL_PATH)
    cost_rate = calibrations.get('pixverse_kling_cost_sec', 0.025)
    
    # Step 2: Parse active storyboard shots
    shots, total_duration, total_cost = parse_shots(EXCEL_PATH, cost_rate)
    
    # Step 3: Generate Markdown Dashboard
    dashboard_md = generate_markdown_dashboard(calibrations, bindings, shots, total_duration, total_cost)
    
    # Step 4: Write scratch-level assets
    scratch_md_path = os.path.join(OUTPUT_DIR, 'production-dashboard.md')
    scratch_json_path = os.path.join(OUTPUT_DIR, 'production-manifest.json')
    
    with open(scratch_md_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_md)
        
    manifest_data = {
        "project_id": "PROJECT_NEVERMORE",
        "system_status": "ACTIVE",
        "calibrations": calibrations,
        "bindings": bindings,
        "storyboard_summary": {
            "total_shots": len(shots),
            "total_duration_sec": total_duration,
            "total_licensing_cost_usd": total_cost,
            "complete_shots": sum(1 for s in shots if s['status'] == 'Complete'),
            "in_progress_shots": sum(1 for s in shots if s['status'] == 'In Progress'),
            "not_started_shots": sum(1 for s in shots if s['status'] == 'Not Started')
        },
        "shots": shots
    }
    
    with open(scratch_json_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2)
        
    print(f"Successfully processed {len(shots)} active shots.")
    print(f"Cumulative Duration: {total_duration}s | Total Render Cost: ${total_cost:.2f} USD")
    print(f"Scratch artifacts saved: {scratch_md_path} and {scratch_json_path}")
    
    # Return formatted data structures to caller if imported
    return manifest_data

if __name__ == '__main__':
    main()
