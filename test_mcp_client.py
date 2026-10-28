import asyncio
from fastmcp import Client

async def run_test():
    print("[*] Connecting to local FastMCP SSE endpoint (http://127.0.0.1:8765/sse)...")
    async with Client("http://127.0.0.1:8765/sse") as client:
        tools = await client.list_tools()
        print(f"[+] Connected! Discovered {len(tools)} tools:")
        for t in tools:
            print(f"    - {t.name}: {t.description}")
        
        print("[*] Invoking 'get_system_telemetry'...")
        res = await client.call_tool("get_system_telemetry")
        print("[+] Telemetry payload received:")
        print(f"    {res.data if hasattr(res, 'data') else res}")

async def main():
    try:
        await asyncio.wait_for(run_test(), timeout=5.0)
        print("[+] Test completed successfully within 5.0s timeout.")
    except asyncio.TimeoutError:
        print("[-] Error: Connection or tool invocation timed out after 5.0 seconds.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
