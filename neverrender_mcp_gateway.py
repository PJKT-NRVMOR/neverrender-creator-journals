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
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext, CallNext
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

# Load NeverRender Labs studio environment variables if present
ENV_PATH = Path(r"C:\Users\Saturn\Desktop\G_AG_FLDR\.env")
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

# Gemini UI injects telemetry kwargs into MCP tool calls; strip them cleanly before Pydantic validation
GEMINI_UI_META_KEYS = {"explanation", "toolSummary", "toolAction", "waitMsBeforeAsync"}

READ_ONLY_ANNOTATIONS = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}


class GeminiArgonMetadataSanitizerMiddleware(Middleware):
    """Strips Gemini UI metadata fields (explanation, toolSummary, toolAction) before tool validation."""

    async def on_call_tool(self, context: MiddlewareContext, call_next: CallNext):
        msg = context.message
        if msg and getattr(msg, "arguments", None) and isinstance(msg.arguments, dict):
            for k in list(msg.arguments.keys()):
                if k in GEMINI_UI_META_KEYS:
                    msg.arguments.pop(k, None)
        return await call_next(context)


# Initialize FastMCP Server
mcp = FastMCP(
    name="NeverRender-Gateway",
    instructions=(
        "Local edge gateway for the NeverRender Labs workstation (Tiny Hyperion). "
        "Provides local filesystem inspection, hardware telemetry, evidentiary vault search, "
        "and workspace document reading over Streamable-HTTP MCP."
    ),
)
mcp.add_middleware(GeminiArgonMetadataSanitizerMiddleware())


@mcp.custom_route("/", methods=["GET", "HEAD"])
@mcp.custom_route("/health", methods=["GET", "HEAD"])
async def health_check(request: Request) -> Response:
    """Health check endpoint for NeverRender Gateway (Tiny Hyperion)."""
    return JSONResponse({
        "status": "ONLINE",
        "gateway": "NeverRender-Gateway (Tiny Hyperion)",
        "timestamp": datetime.datetime.now().isoformat(),
    })


@mcp.custom_route("/.well-known/{filename:path}", methods=["GET", "HEAD"])
async def well_known_verification(request: Request) -> Response:
    """
    Serves Google Connected Apps Platform /.well-known/ domain verification files
    from C:\\Users\\Saturn\\Desktop\\G_AG_FLDR\\.well-known\\ for permanent custom domain tunnels.
    """
    filename = request.path_params.get("filename", "")
    well_known_dir = Path(r"C:\Users\Saturn\Desktop\G_AG_FLDR\.well-known").resolve()
    target = (well_known_dir / filename).resolve()
    if str(target).startswith(str(well_known_dir)) and target.is_file():
        return Response(content=target.read_text(encoding="utf-8", errors="replace"), media_type="text/plain")
    return JSONResponse({
        "gateway": "NeverRender-Gateway (Tiny Hyperion)",
        "mcp_endpoint": "/mcp",
        "well_known_path": filename,
        "status": "READY_FOR_DOMAIN_VERIFICATION",
    })


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def get_system_telemetry() -> dict:
    """Retrieve real-time hardware, memory, and disk telemetry from the Beelink 6800U workstation (Tiny Hyperion)."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\")

    return {
        "status": "ONLINE",
        "workstation": "Tiny Hyperion (Beelink SER6 // Ryzen 7 6800U)",
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_load_percent": cpu_percent,
        "memory_used_gb": round((mem.total - mem.available) / (1024**3), 2),
        "memory_total_gb": round(mem.total / (1024**3), 2),
        "memory_free_percent": round(mem.available / mem.total * 100, 1),
        "disk_c_free_gb": round(disk.free / (1024**3), 2),
        "disk_c_total_gb": round(disk.total / (1024**3), 2),
        "python_runtime": sys.version.split()[0],
    }


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
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
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception:
            continue
    return entries


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
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
                        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    })
                    if len(results) >= max_results:
                        return results
                except Exception:
                    continue
    return results


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def read_local_markdown_or_doc(file_path: str, start_line: int = 1, end_line: int = 250) -> dict:
    """
    Read lines from any local markdown, script, JSON, or log file in the NeverRender Labs workspace.
    """
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": f"File not found: {file_path}"}
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
        total = len(all_lines)
        s = max(1, start_line)
        e = min(total, max(s, end_line))
        snippet = "".join(f"{idx}: {all_lines[idx - 1]}" for idx in range(s, e + 1))
        return {
            "path": str(p),
            "total_lines": total,
            "start_line": s,
            "end_line": e,
            "content": snippet,
        }
    except Exception as exc:
        return {"error": str(exc)}


if __name__ == "__main__":
    port = 8765
    print(f"[*] Starting NeverRender Gateway FastMCP Streamable-HTTP server on port {port}...")
    print(f"    -> Primary Gateway MCP Path:  http://127.0.0.1:{port}/mcp")
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=port,
        path="/mcp",
    )
