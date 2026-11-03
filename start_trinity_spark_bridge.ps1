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

# 1. Check if FastMCP Gateway is responding on http://127.0.0.1:8765/health
$gwOnline = $false
try {
    $h = Invoke-RestMethod -Uri "http://127.0.0.1:8765/health" -TimeoutSec 2 -ErrorAction Stop
    if ($h.status -eq "ONLINE") { $gwOnline = $true }
} catch {}

if ($gwOnline) {
    Write-Host "[OK] NeverRender-Gateway is ALREADY ONLINE on http://127.0.0.1:8765/mcp" -ForegroundColor Green
} else {
    Write-Host "[*] Launching detached NeverRender-Gateway on http://127.0.0.1:8765/mcp..." -ForegroundColor Yellow
    $gwProc = Start-Process -FilePath "python" `
        -ArgumentList "`"$GatewayScript`"" `
        -WorkingDirectory $WorkDir `
        -WindowStyle Hidden `
        -RedirectStandardOutput $GatewayLog `
        -RedirectStandardError $GatewayErrLog `
        -PassThru
    Start-Sleep -Seconds 8
    Write-Host "[OK] NeverRender-Gateway started in detached background mode (PID: $($gwProc.Id))" -ForegroundColor Green
}

# 2. Check if a Named Sovereign Tunnel config exists (C:\Users\Saturn\.cloudflared\config.yml)
$NamedConfig = "C:\Users\Saturn\.cloudflared\config.yml"
$UseNamedTunnel = Test-Path $NamedConfig
$CfArgs = if ($UseNamedTunnel) { "tunnel --config `"$NamedConfig`" run trinity-spark-bridge" } else { "tunnel --url http://127.0.0.1:8765" }

# 3. Check if cloudflared is already running
$cfProc = Get-Process -Name "cloudflared-windows-amd64" -ErrorAction SilentlyContinue
if ($cfProc -and -not $RestartTunnel) {
    Write-Host "[OK] Cloudflared Tunnel is ALREADY RUNNING (PID: $($cfProc[0].Id)) - preserving active tunnel!" -ForegroundColor Green
} else {
    if ($cfProc -and $RestartTunnel) {
        Write-Host "[*] Stopping existing Cloudflared tunnel as requested (-RestartTunnel)..." -ForegroundColor Yellow
        Stop-Process -Id $cfProc.Id -Force
        Start-Sleep -Seconds 1
    }
    if (Test-Path $TunnelLog) { Remove-Item $TunnelLog -Force -ErrorAction SilentlyContinue }
    Write-Host "[*] Launching detached Cloudflared Tunnel ($CfArgs)..." -ForegroundColor Yellow
    $newCf = Start-Process -FilePath $CloudflaredBin `
        -ArgumentList $CfArgs `
        -WorkingDirectory $WorkDir `
        -WindowStyle Hidden `
        -RedirectStandardError $TunnelLog `
        -PassThru
    Start-Sleep -Seconds 5
    Write-Host "[OK] Cloudflared Tunnel started (PID: $($newCf.Id))" -ForegroundColor Green
}

# 4. Extract and save the active endpoint URL
if ($UseNamedTunnel) {
    $cfgText = Get-Content -Path $NamedConfig -Raw
    if ($cfgText -match "hostname:\s*([^\s\r\n]+)") {
        $mcpEndpoint = "https://$($Matches[1])/mcp"
        Set-Content -Path $UrlFile -Value $mcpEndpoint -Encoding UTF8
        Write-Host "`nActive Sovereign MCP Endpoint (Saved to CURRENT_TRINITY_SPARK_BRIDGE_URL.txt):" -ForegroundColor Cyan
        Write-Host "  -> $mcpEndpoint" -ForegroundColor White
    }
} else {
    $searchLogs = @($TunnelLog) + (Get-ChildItem "C:\Users\Saturn\.gemini\antigravity\brain\*\*\tasks\*.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -ExpandProperty FullName)
    $foundUrl = $null
    foreach ($logPath in $searchLogs) {
        if ($logPath -and (Test-Path $logPath)) {
            $matches = Select-String -Path $logPath -Pattern "https://[a-z0-9-]+\.trycloudflare\.com" -AllMatches -ErrorAction SilentlyContinue
            if ($matches) {
                $foundUrl = $matches[-1].Matches[-1].Value
                break
            }
        }
    }
    if ($foundUrl) {
        $mcpEndpoint = "$foundUrl/mcp"
        Set-Content -Path $UrlFile -Value $mcpEndpoint -Encoding UTF8
        Write-Host "`nActive MCP Endpoint (Saved to CURRENT_TRINITY_SPARK_BRIDGE_URL.txt):" -ForegroundColor Cyan
        Write-Host "  -> $mcpEndpoint" -ForegroundColor White
    }
}
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:8765/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "[OK] Local Gateway /health check PASSED: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "[WARN] Local Gateway /health check failed: $_" -ForegroundColor Red
}
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "[*] Holding self-healing watchdog loop open (checks Port 8765 & Cloudflared every 5s)..." -ForegroundColor DarkGray
while ($true) {
    Start-Sleep -Seconds 10
    $gwAlive = $false
    try {
        $hc = Invoke-RestMethod -Uri "http://127.0.0.1:8765/health" -TimeoutSec 3 -ErrorAction Stop
        if ($hc.status -eq "ONLINE") { $gwAlive = $true }
    } catch {}
    if (-not $gwAlive) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] [WATCHDOG] Port 8765 dropped! Respawning NeverRender-Gateway..." -ForegroundColor Yellow
        Start-Process -FilePath "python" `
            -ArgumentList "`"$GatewayScript`"" `
            -WorkingDirectory $WorkDir `
            -WindowStyle Hidden `
            -RedirectStandardOutput $GatewayLog `
            -RedirectStandardError $GatewayErrLog | Out-Null
        Start-Sleep -Seconds 8
    }
    $cfAlive = Get-Process -Name "cloudflared-windows-amd64" -ErrorAction SilentlyContinue
    if (-not $cfAlive) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] [WATCHDOG] Cloudflared dropped! Respawning Tunnel..." -ForegroundColor Yellow
        Start-Process -FilePath $CloudflaredBin `
            -ArgumentList $CfArgs `
            -WorkingDirectory $WorkDir `
            -WindowStyle Hidden `
            -RedirectStandardError $TunnelLog | Out-Null
        Start-Sleep -Seconds 5
    }
}
