"""
NeverRender Labs - Local MCP Gateway for Gemini Spark & Agent Workflows
Transport: StreamableHTTP (Modern MCP Specification for Google Gemini)
Tunnel: Cloudflare Quick Tunnel (TLS/HTTPS)
"""

import os
import sys
import psutil
import datetime
from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    name="NeverRender-Gateway",
    instructions="Local edge gateway for NeverRender Labs workstation. Controls local filesystem, telemetry, and media assets."
)

@mcp.tool()
def get_system_telemetry() -> dict:
    """Retrieve real-time hardware, memory, and disk telemetry from the Beelink 6800U workstation."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")
    
    return {
        "status": "ONLINE",
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_load_percent": cpu_percent,
        "memory_used_gb": round((mem.total - mem.available) / (1024**3), 2),
        "memory_total_gb": round(mem.total / (1024**3), 2),
        "memory_free_percent": round(mem.available / mem.total * 100, 1),
        "disk_c_free_gb": round(disk.free / (1024**3), 2),
        "disk_c_total_gb": round(disk.total / (1024**3), 2),
        "python_runtime": sys.version.split()[0]
    }

@mcp.tool()
def list_workspace_files(directory_path: str = "C:\\Users\\Saturn\\Desktop\\G_AG_FLDR", max_files: int = 25) -> list:
    """List recent files in a workspace directory to inspect projects, assets, or renders."""
    p = Path(directory_path)
    if not p.exists() or not p.is_dir():
        return [{"error": f"Directory not found: {directory_path}"}]
    
    entries = []
    for item in sorted(p.iterdir(), key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True):
        if len(entries) >= max_files:
            break
        try:
            stat = item.stat()
            entries.append({
                "name": item.name,
                "is_dir": item.is_dir(),
                "size_kb": round(stat.st_size / 1024, 2) if item.is_file() else 0,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception:
            continue
    return entries

@mcp.tool()
def search_vault_records(keyword: str, max_results: int = 10) -> list:
    """Search legal, medical, and municipal case records in the evidentiary vault by keyword."""
    vault_dir = Path(r"C:\Users\Saturn\Proton Drive\WYATT_LEGAL_EVIDENTIARY_VAULT")
    if not vault_dir.exists():
        vault_dir = Path(r"C:\Users\Saturn\Desktop\city-of-vista-fullfilled-cpra-request")
    
    results = []
    keyword_lower = keyword.lower()
    for root, dirs, files in os.walk(vault_dir):
        for f in files:
            if keyword_lower in f.lower():
                full_p = Path(root) / f
                try:
                    stat = full_p.stat()
                    results.append({
                        "filename": f,
                        "path": str(full_p),
                        "size_kb": round(stat.st_size / 1024, 2),
                        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
                    if len(results) >= max_results:
                        return results
                except Exception:
                    continue
    return results

if __name__ == "__main__":
    port = 8765
    print(f"[*] Starting NeverRender Gateway FastMCP Streamable-HTTP server on port {port}...")
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=port,
        path="/mcp"
    )
