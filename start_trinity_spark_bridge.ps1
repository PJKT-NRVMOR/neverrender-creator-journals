#Requires -Version 5.1
<#
.SYNOPSIS
    Detached 24/7 Windows Launcher for NeverRender-Gateway (Port 8765) & Cloudflare Quick Tunnel.
    Ensures trinity-spark-bridge stays alive across Antigravity thread switches without dropping the tunnel URL.
#>

param(
    [switch]$RestartTunnel
)

$ErrorActionPreference = "Stop"
$WorkDir = "C:\Users\Saturn\Desktop\G_AG_FLDR"
$GatewayScript = Join-Path $WorkDir "neverrender_mcp_gateway.py"
$CloudflaredBin = Join-Path $WorkDir "cloudflared-windows-amd64.exe"
$GatewayLog = Join-Path $WorkDir "trinity_gateway_8765.log"
$GatewayErrLog = Join-Path $WorkDir "trinity_gateway_8765.err.log"
$TunnelLog = Join-Path $WorkDir "trinity_cloudflared_8765.log"
$UrlFile = Join-Path $WorkDir "CURRENT_TRINITY_SPARK_BRIDGE_URL.txt"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  NEVERRENDER LABS // TRINITY-SPARK-BRIDGE 24/7 DAEMON MANAGER  " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# 1. Check if FastMCP Gateway is listening on 127.0.0.1:8765
$port8765 = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if ($port8765) {
    $gwPid = $port8765[0].OwningProcess
    Write-Host "[OK] NeverRender-Gateway is ALREADY ONLINE on http://127.0.0.1:8765/mcp (PID: $gwPid)" -ForegroundColor Green
} else {
    Write-Host "[*] Launching detached NeverRender-Gateway on http://127.0.0.1:8765/mcp..." -ForegroundColor Yellow
    $gwProc = Start-Process -FilePath "python" `
        -ArgumentList "`"$GatewayScript`"" `
        -WorkingDirectory $WorkDir `
        -WindowStyle Hidden `
        -RedirectStandardOutput $GatewayLog `
        -RedirectStandardError $GatewayErrLog `
        -PassThru
    Start-Sleep -Seconds 3
    Write-Host "[OK] NeverRender-Gateway started in detached background mode (PID: $($gwProc.Id))" -ForegroundColor Green
}

# 2. Check if cloudflared is already running (preserve existing Quick Tunnel URL!)
$cfProc = Get-Process -Name "cloudflared-windows-amd64" -ErrorAction SilentlyContinue
if ($cfProc -and -not $RestartTunnel) {
    Write-Host "[OK] Cloudflared Quick Tunnel is ALREADY RUNNING (PID: $($cfProc[0].Id)) - preserving active tunnel URL!" -ForegroundColor Green
} else {
    if ($cfProc -and $RestartTunnel) {
        Write-Host "[*] Stopping existing Cloudflared tunnel as requested (-RestartTunnel)..." -ForegroundColor Yellow
        Stop-Process -Id $cfProc.Id -Force
        Start-Sleep -Seconds 1
    }
    if (Test-Path $TunnelLog) { Remove-Item $TunnelLog -Force -ErrorAction SilentlyContinue }
    Write-Host "[*] Launching detached Cloudflared Quick Tunnel -> http://127.0.0.1:8765..." -ForegroundColor Yellow
    $newCf = Start-Process -FilePath $CloudflaredBin `
        -ArgumentList "tunnel --url http://127.0.0.1:8765" `
        -WorkingDirectory $WorkDir `
        -WindowStyle Hidden `
        -RedirectStandardError $TunnelLog `
        -PassThru
    Start-Sleep -Seconds 5
    Write-Host "[OK] Cloudflared Quick Tunnel started (PID: $($newCf.Id))" -ForegroundColor Green
}

# 3. Extract and save the active trycloudflare.com URL if available in logs
$searchLogs = @($TunnelLog) + (Get-ChildItem "C:\Users\Saturn\.gemini\antigravity\brain\*\*\tasks\*.log" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName)
$foundUrl = $null
foreach ($logPath in $searchLogs) {
    if ($logPath -and (Test-Path $logPath)) {
        $matches = Select-String -Path $logPath -Pattern "https://[a-z0-9-]+\.trycloudflare\.com" -AllMatches -ErrorAction SilentlyContinue
        if ($matches) {
            $foundUrl = $matches[-1].Matches[-1].Value
        }
    }
}

if ($foundUrl) {
    $mcpEndpoint = "$foundUrl/mcp"
    Set-Content -Path $UrlFile -Value $mcpEndpoint -Encoding UTF8
    Write-Host "`nActive MCP Endpoint (Saved to CURRENT_TRINITY_SPARK_BRIDGE_URL.txt):" -ForegroundColor Cyan
    Write-Host "  -> $mcpEndpoint" -ForegroundColor White
}
Write-Host "================================================================" -ForegroundColor Cyan
