import asyncio
import httpx
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from fastmcp import FastMCP

m = FastMCP("test")

@m.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

mcp_app = m.http_app(transport="http", path="/mcp")

app = Starlette(
    routes=[
        Mount("", app=mcp_app),
    ],
    lifespan=mcp_app.lifespan
)

def run_test():
    # Test with Starlette TestClient or lifespan context
    from starlette.testclient import TestClient
    with TestClient(app) as client:
        # Test HEAD
        r_head = client.head("/mcp")
        print("HEAD /mcp status:", r_head.status_code)
        
        # Test POST initialize
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "Gemini-Test", "version": "1.0"}
            }
        }
        r_post = client.post("/mcp", json=init_payload)
        print("POST /mcp status:", r_post.status_code)
        print("POST /mcp headers:", r_post.headers)
        print("POST /mcp response:", r_post.text[:200])

if __name__ == "__main__":
    run_test()
