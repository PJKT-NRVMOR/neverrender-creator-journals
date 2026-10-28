import subprocess
import os
import psutil
from fastmcp import FastMCP, Context

# Initialize FastMCP Server
mcp = FastMCP(name="Studio Command Bridge")

@mcp.tool
def get_system_telemetry() -> str:
    """
    Returns CPU, RAM, and GPU status on the workstation.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    return (
        f"🖥️ Workstation Telemetry:\n"
        f"- CPU Load: {cpu_usage}%\n"
        f"- RAM Used: {ram.percent}% ({round(ram.used / (1024**3), 2)}GB / {round(ram.total / (1024**3), 2)}GB)"
    )

@mcp.tool
def trigger_antigravity_task(task_prompt: str) -> str:
    """
    Kicks off a multi-agent Antigravity or Trinity task on the local machine.
    """
    # Execute local Antigravity CLI call in the background
    try:
        # Example call to local antigravity binary / python runner
        process = subprocess.Popen(
            ["antigravity", "run", "--prompt", task_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return f"🚀 Task dispatched to Antigravity (PID: {process.pid}) for: '{task_prompt}'"
    except Exception as e:
        return f"❌ Failed to dispatch Antigravity process: {str(e)}"

@mcp.tool
def list_active_render_jobs() -> str:
    """
    Checks if llama-server, Premiere, or python daemons are running.
    """
    active_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if any(k in name for k in ['llama', 'python', 'adobe', 'ffmpeg']):
                active_processes.append(f"- {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    if active_processes:
        return "⚙️ Active Studio Processes:\n" + "\n".join(active_processes[:10])
    return "🟢 No heavy studio render jobs currently active."

if __name__ == "__main__":
    # Runs the HTTP/SSE server on port 8000
    mcp.run(transport="http", host="0.0.0.0", port=8000)