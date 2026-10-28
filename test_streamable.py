import asyncio
import httpx
from fastmcp import FastMCP

m = FastMCP("test")

@m.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

app = m.http_app(transport="streamable-http", path="/mcp")

async def run_test():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # Test HEAD
        r_head = await client.head("/mcp")
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
        r_post = await client.post("/mcp", json=init_payload)
        print("POST /mcp status:", r_post.status_code)
        print("POST /mcp response:", r_post.text[:200])

if __name__ == "__main__":
    asyncio.run(run_test())
