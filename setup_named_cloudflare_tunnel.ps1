#Requires -Version 5.1
<#
.SYNOPSIS
    Provisions a Permanent Sovereign Cloudflare Named Tunnel (https://mcp.renderwithoutcode.com/mcp)
    for NeverRender-Gateway (Port 8765) on Tiny Hyperion.
#>

param(
    [string]$Hostname = "mcp.renderwithoutcode.com",
    [string]$TunnelName = "trinity-spark-bridge"
)

$ErrorActionPreference = "Stop"
$WorkDir = "C:\Users\Saturn\Desktop\G_AG_FLDR"
$CloudflaredBin = Join-Path $WorkDir "cloudflared-windows-amd64.exe"
$CfDir = "C:\Users\Saturn\.cloudflared"
$CertPath = Join-Path $CfDir "cert.pem"
$ConfigPath = Join-Path $CfDir "config.yml"
$UrlFile = Join-Path $WorkDir "CURRENT_TRINITY_SPARK_BRIDGE_URL.txt"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  NEVERRENDER LABS // SOVEREIGN NAMED TUNNEL PROVISIONER        " -ForegroundColor Cyan
Write-Host "  Target Endpoint: https://$Hostname/mcp                        " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Step 1: Ensure Cloudflare Origin Certificate (cert.pem) exists
if (-not (Test-Path $CertPath)) {
    Write-Host "[1/4] Launching browser for one-time Cloudflare domain authorization..." -ForegroundColor Yellow
    Write-Host "      -> Select your domain (renderwithoutcode.com) in the browser and click Authorize." -ForegroundColor White
    & $CloudflaredBin tunnel login
    if (-not (Test-Path $CertPath)) {
        throw "cert.pem was not created at $CertPath. Please complete the browser login and re-run."
    }
} else {
    Write-Host "[1/4] Found existing Cloudflare authorization cert at $CertPath" -ForegroundColor Green
}

# Step 2: Locate or create Named Tunnel (trinity-spark-bridge)
Write-Host "[2/4] Checking for named tunnel '$TunnelName'..." -ForegroundColor Yellow
$existingJsonFiles = Get-ChildItem -Path $CfDir -Filter "*.json" -ErrorAction SilentlyContinue
if (-not $existingJsonFiles) {
    Write-Host "      -> Creating named tunnel '$TunnelName'..." -ForegroundColor Yellow
    & $CloudflaredBin tunnel create $TunnelName
    $existingJsonFiles = Get-ChildItem -Path $CfDir -Filter "*.json" -ErrorAction SilentlyContinue
}
$TunnelId = $existingJsonFiles[0].BaseName
Write-Host "      -> Tunnel '$TunnelName' ready (ID: $TunnelId)" -ForegroundColor Green

$CredFile = Join-Path $CfDir "$TunnelId.json"

# Step 3: Route DNS CNAME (mcp.renderwithoutcode.com -> <TunnelId>.cfargotunnel.com)
Write-Host "[3/4] Binding Cloudflare DNS CNAME for $Hostname -> $TunnelName..." -ForegroundColor Yellow
& $CloudflaredBin tunnel route dns -f $TunnelName $Hostname

# Step 4: Write C:\Users\Saturn\.cloudflared\config.yml
Write-Host "[4/4] Writing permanent tunnel config to $ConfigPath..." -ForegroundColor Yellow
$yaml = @"
tunnel: $TunnelId
credentials-file: $CredFile

ingress:
  - hostname: $Hostname
    service: http://127.0.0.1:8765
  - service: http_status:404
"@
Set-Content -Path $ConfigPath -Value $yaml -Encoding UTF8

$PermanentEndpoint = "https://$Hostname/mcp"
Set-Content -Path $UrlFile -Value $PermanentEndpoint -Encoding UTF8

Write-Host "`n================================================================" -ForegroundColor Green
Write-Host "  SOVEREIGN NAMED TUNNEL CONFIGURED!                            " -ForegroundColor Green
Write-Host "  Permanent MCP Endpoint: $PermanentEndpoint                    " -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Green
