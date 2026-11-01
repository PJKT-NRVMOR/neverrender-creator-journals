"""
NeverRender Labs - Local MCP Gateway for Gemini Spark & Agent Workflows
Transport: StreamableHTTP (Modern MCP Specification for Google Gemini)
Tunnel: Cloudflare Quick Tunnel (TLS/HTTPS)
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.parse
import psutil
import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server import create_proxy
from fastmcp.server.middleware import Middleware, MiddlewareContext, CallNext
from fastmcp.client.transports import StreamableHttpTransport
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

# Load Project Marshall College / NeverRender Labs credentials from .env
ENV_PATH = Path(r"C:\Users\Saturn\Desktop\project-marshall-college\.env")
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

OMNISEND_API_KEY = os.getenv("OMNISEND_API_KEY", "")
OMNISEND_MCP_URL = "https://mcp.omnisend.com/mcp?brand=the-chapman-collection"
OMNISEND_REST_BASE = "https://api.omnisend.com/v3"
WP_BASE = os.getenv("WP_BASE_URL", "https://thechapmancollection.com/wp-json")
WP_USER = os.getenv("WP_REST_USER", "neverrender-labs")
WP_APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")

MASTER_CONTACT_MD = Path(
    r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\02-clean-master-database\BATCH-08_Complete_1434_Master_Contact_Registry_DEE.md"
)
MASTER_INVENTORY_MD = Path(
    r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\02-clean-master-database\BATCH-09_Complete_Live_WooCommerce_Inventory_Catalog_DEE.md"
)

# Gemini Argon / Gemini Web injects UI telemetry kwargs into MCP tool calls; strip them cleanly before Pydantic validation
GEMINI_UI_META_KEYS = {"explanation", "toolSummary", "toolAction", "waitMsBeforeAsync"}

READ_ONLY_ANNOTATIONS = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}


class GeminiArgonMetadataSanitizerMiddleware(Middleware):
    """Strips Gemini Argon UI metadata fields (explanation, toolSummary, toolAction) before tool validation."""

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
        "Local edge gateway for NeverRender Labs workstation (Tiny Hyperion) & Project Marshall College "
        "(The Chapman Collection). Controls local filesystem, hardware telemetry, Omnisend MCP/REST v3 "
        "(True Delivered % vs. Raw Sent), Master Contact Registry (1,960 collectors), and WordPress/WooCommerce REST API."
    ),
)
mcp.add_middleware(GeminiArgonMetadataSanitizerMiddleware())

# Mount official Omnisend MCP Server via authenticated StreamableHttpTransport (zero OAuth required!)
if OMNISEND_API_KEY:
    omnisend_transport = StreamableHttpTransport(
        OMNISEND_MCP_URL,
        headers={
            "Authorization": f"Bearer {OMNISEND_API_KEY}",
            "X-API-KEY": OMNISEND_API_KEY,
        },
    )
    omnisend_proxy = create_proxy(omnisend_transport, name="Omnisend-MCP-Bridge")
    mcp.mount(omnisend_proxy, namespace="omnisend")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> Response:
    """Health check endpoint for NeverRender Gateway & Omnisend MCP Bridge."""
    return JSONResponse({
        "status": "ONLINE",
        "gateway": "NeverRender-Gateway (Tiny Hyperion)",
        "omnisend_mcp_mounted": bool(OMNISEND_API_KEY),
        "timestamp": datetime.datetime.now().isoformat(),
    })


@mcp.custom_route("/omnisend/mcp", methods=["GET", "POST", "DELETE", "OPTIONS"])
async def omnisend_raw_mcp_proxy(request: Request) -> Response:
    """
    Direct Streamable-HTTP pass-through to https://mcp.omnisend.com/mcp
    that automatically injects Authorization: Bearer <OMNISEND_API_KEY> and X-API-KEY
    so gemini.google.com/devmode can connect without OAuth registration!
    """
    if request.method == "OPTIONS":
        return Response(
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )

    body = await request.body()
    forward_headers = {
        "Authorization": f"Bearer {OMNISEND_API_KEY}",
        "X-API-KEY": OMNISEND_API_KEY,
        "Content-Type": request.headers.get("content-type", "application/json"),
        "Accept": request.headers.get("accept", "application/json, text/event-stream"),
        "User-Agent": "NeverRender-Gateway-MCP-Bridge/1.0",
    }
    if "mcp-session-id" in request.headers:
        forward_headers["Mcp-Session-Id"] = request.headers["mcp-session-id"]

    req = urllib.request.Request(
        OMNISEND_MCP_URL,
        data=body if body else None,
        method=request.method,
        headers=forward_headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            resp_bytes = resp.read()
            resp_headers = {"Access-Control-Allow-Origin": "*"}
            for h_key in ("Content-Type", "Mcp-Session-Id"):
                val = resp.headers.get(h_key)
                if val:
                    resp_headers[h_key] = val
            return Response(content=resp_bytes, status_code=resp.status, headers=resp_headers)
    except urllib.error.HTTPError as e:
        err_bytes = e.read()
        return Response(
            content=err_bytes,
            status_code=e.code,
            media_type="application/json",
            headers={"Access-Control-Allow-Origin": "*"},
        )


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
def query_woocommerce_catalog(search_term: str = "", per_page: int = 20) -> list:
    """Query live published products on The Chapman Collection (thechapmancollection.com) via WooCommerce REST v3."""
    if not WP_APP_PASS:
        return [{"error": "WP_REST_APP_PASSWORD not configured in .env"}]
    auth_str = base64.b64encode(f"{WP_USER}:{WP_APP_PASS}".encode("utf-8")).decode("utf-8")
    url = f"{WP_BASE}/wc/v3/products?status=publish&per_page={min(100, max(1, per_page))}"
    if search_term:
        url += f"&search={urllib.parse.quote(search_term)}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Basic {auth_str}",
            "User-Agent": "NeverRender-Gateway/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        items = json.loads(resp.read().decode("utf-8"))
        return [
            {
                "id": p.get("id"),
                "sku": p.get("sku") or f"WC-{p.get('id')}",
                "name": p.get("name"),
                "price": p.get("price"),
                "regular_price": p.get("regular_price"),
                "sale_price": p.get("sale_price"),
                "stock_status": p.get("stock_status"),
                "permalink": p.get("permalink"),
            }
            for p in items
        ]


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def query_omnisend_telemetry(limit: int = 15, campaign_type: str = "") -> dict:
    """
    One-shot Read-Only Omnisend campaign & audience telemetry reader.
    Returns recent Email and SMS campaigns from Omnisend REST v3 without triggering a Destructive tool confirmation.
    """
    if not OMNISEND_API_KEY:
        return {"error": "OMNISEND_API_KEY not configured in .env"}
    url = f"{OMNISEND_REST_BASE}/campaigns?limit={min(50, max(1, limit))}"
    if campaign_type:
        url += f"&type={urllib.parse.quote(campaign_type)}"
    req = urllib.request.Request(
        url,
        headers={
            "X-API-KEY": OMNISEND_API_KEY,
            "Accept": "application/json",
            "User-Agent": "NeverRender-Gateway/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            campaigns = data.get("campaigns", data if isinstance(data, list) else [])
            return {
                "count": len(campaigns),
                "campaigns": campaigns,
            }
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "details": e.read().decode("utf-8", errors="ignore")}


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def lookup_chapman_contact(query: str, max_results: int = 15) -> dict:
    """
    Search The Chapman Collection Master Contact Registry (1,960 records, TC-0001 to TC-2043)
    by name, email, phone number, city, segment, or TC-XXXX ID, plus live Omnisend contact lookup if query is an email.
    """
    q = query.strip().lower()
    local_matches = []
    if MASTER_CONTACT_MD.exists():
        with open(MASTER_CONTACT_MD, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("| `TC-") and q in line.lower():
                    cols = [c.strip() for c in line.strip().strip("|").split("|")]
                    if len(cols) >= 8:
                        local_matches.append({
                            "master_id": cols[0].strip("`"),
                            "full_name": cols[1],
                            "email": cols[2].strip("`"),
                            "phone": cols[3].strip("`"),
                            "location": cols[4],
                            "segment": cols[5],
                            "historical_spend": cols[6],
                            "notes": cols[7],
                            "deliverability": cols[8] if len(cols) > 8 else "",
                        })
                        if len(local_matches) >= max_results:
                            break

    omnisend_live = None
    if "@" in q and OMNISEND_API_KEY:
        try:
            url = f"{OMNISEND_REST_BASE}/contacts?email={urllib.parse.quote(query.strip())}&limit=5"
            req = urllib.request.Request(
                url,
                headers={"X-API-KEY": OMNISEND_API_KEY, "Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                omnisend_live = json.loads(resp.read().decode("utf-8")).get("contacts", [])
        except Exception as e:
            omnisend_live = [{"error": str(e)}]

    return {
        "query": query,
        "local_registry_matches_count": len(local_matches),
        "local_registry_matches": local_matches,
        "omnisend_live_contacts": omnisend_live,
    }


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
def read_local_markdown_or_doc(file_path: str, start_line: int = 1, end_line: int = 250) -> dict:
    """
    Read lines from any local markdown, script, JSON, or flight log file in G_AG_FLDR or project-marshall-college.
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


@mcp.resource("chapman://inventory/summary")
def resource_inventory_summary() -> str:
    """Live summary header of The Chapman Collection WooCommerce Inventory Catalog (113 Active SKUs)."""
    if not MASTER_INVENTORY_MD.exists():
        return "Inventory catalog file not found."
    with open(MASTER_INVENTORY_MD, "r", encoding="utf-8", errors="replace") as f:
        lines = [next(f, "") for _ in range(160)]
    return "".join(lines)


@mcp.prompt()
def chapman_morning_telemetry_brief() -> str:
    """Standard prompt template for running a full morning telemetry sweep across Tiny Hyperion, WooCommerce, and Omnisend."""
    return (
        "Run a complete morning telemetry sweep across trinity-spark-bridge:\n"
        "1. Call get_system_telemetry() to verify Tiny Hyperion hardware status.\n"
        "2. Call query_woocommerce_catalog(per_page=10) to inspect the newest published pieces on thechapmancollection.com.\n"
        "3. Call query_omnisend_telemetry(limit=5) to inspect our latest Omnisend Email and SMS campaigns.\n"
        "Report the combined readout in a clean executive table."
    )


if __name__ == "__main__":
    port = 8765
    print(f"[*] Starting NeverRender Gateway FastMCP Streamable-HTTP server on port {port}...")
    print(f"    -> Primary Gateway MCP Path:  http://127.0.0.1:{port}/mcp (includes mounted omnisend_* tools)")
    print(f"    -> Direct Omnisend Proxy Path: http://127.0.0.1:{port}/omnisend/mcp")
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=port,
        path="/mcp",
    )
