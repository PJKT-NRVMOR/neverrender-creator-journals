# ==============================================================================
# NeverRender Labs // Automated Two-Repo GitHub Sync & Cortical Stack Mirror
# ==============================================================================
# Syncs:
#   1. Tree 1: c:\Users\Saturn\Desktop\G_AG_FLDR (PJKT-NRVMOR/neverrender-creator-journals)
#   2. Site:   c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE (PJKT-NRVMOR/neverrender-labs-website)
#
# Enforces Zero Secrets / Zero Client PII across studio tooling and corpuses.
# ==============================================================================

$ErrorActionPreference = "Continue"
$env:GIT_TERMINAL_PROMPT = "0"
$env:GCM_INTERACTIVE = "never"
$Timestamp = Get-Date -Format "HH:mm:ss-yyyy-MM-dd"
$LogFile = "c:\Users\Saturn\Desktop\G_AG_FLDR\github_daily_sync.log"

function Write-SyncLog {
    param([string]$Message)
    $Line = "[$Timestamp] $Message"
    Write-Output $Line
    Add-Content -Path $LogFile -Value $Line -Encoding UTF8
}

Write-SyncLog "=== Starting NeverRender Labs Two-Repo GitHub Sync ==="

$Tree1 = "c:\Users\Saturn\Desktop\G_AG_FLDR"
$WebsiteRepo = "c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE"

# Keep studio rules mirrored from Tree 1 -> Website repo root
Copy-Item -Path "$Tree1\AGENTS.md" -Destination "$WebsiteRepo\AGENTS.md" -Force

function Resolve-CorpusRebaseIfNeeded {
    param([string]$RepoPath, [string]$Tag)
    $RebaseMerge = Join-Path $RepoPath ".git\rebase-merge"
    $RebaseApply = Join-Path $RepoPath ".git\rebase-apply"
    if ((Test-Path $RebaseMerge) -and -not (Test-Path (Join-Path $RebaseMerge "head-name"))) {
        Remove-Item -Path $RebaseMerge -Recurse -Force -ErrorAction SilentlyContinue
    }
    if ((Test-Path $RebaseMerge) -or (Test-Path $RebaseApply)) {
        Write-SyncLog "  [$Tag-AutoResolve] Detected active rebase conflict on append-only corpus; union-merging both blocks..."
        $CorpusFiles = @(
            (Join-Path $RepoPath ".agents\skills\wyatt-nrl-voice-copywriter\references\wyatt-voice-corpus.md"),
            (Join-Path $RepoPath ".agents\skills\melissa-tone-copywriter\references\voice-corpus.md"),
            (Join-Path $RepoPath "AGENTS.md")
        )
        foreach ($File in $CorpusFiles) {
            if (Test-Path $File) {
                $Raw = Get-Content -Path $File -Raw -Encoding UTF8
                if ($Raw -match "(?m)^<<<<<<< ") {
                    $Cleaned = $Raw -replace "(?m)^<<<<<<< [^\r\n]*\r?\n", "" -replace "(?m)^=======\r?\n", "" -replace "(?m)^>>>>>>> [^\r\n]*\r?\n?", ""
                    Set-Content -Path $File -Value $Cleaned -Encoding UTF8 -NoNewline
                }
            }
        }
        git -C $RepoPath add -u
        $env:GIT_EDITOR = "true"
        git -C $RepoPath -c core.editor=true rebase --continue 2>&1 | ForEach-Object { Write-SyncLog "  [$Tag-AutoResolve] $_" }
        if ((Test-Path $RebaseMerge) -and -not (Test-Path (Join-Path $RebaseMerge "head-name"))) {
            Remove-Item -Path $RebaseMerge -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

# ------------------------------------------------------------------------------
# Repo 1: Tree 1 (G_AG_FLDR -> PJKT-NRVMOR/neverrender-creator-journals)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Tree 1 (neverrender-creator-journals) ---"
Resolve-CorpusRebaseIfNeeded -RepoPath $Tree1 -Tag "Tree1"
git -C $Tree1 add .gitattributes AGENTS.md .agents/ 01-vision-and-color-science/ 02-commerce-and-seo-engines/ 03-omnisend-and-mms-foundry/ 04-print-and-vector-foundry/ neverrender_mcp_gateway.py sync_all_repos_to_github.ps1
$Status1 = git -C $Tree1 diff --cached --name-only
if ($Status1) {
    git -C $Tree1 commit -m "chore(studio): auto-sync NRL cortical stack, voice corpuses & toolkit [$Timestamp]"
}
git -C $Tree1 pull --rebase --autostash origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree1-Pull] $_" }
Resolve-CorpusRebaseIfNeeded -RepoPath $Tree1 -Tag "Tree1"
git -C $Tree1 push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree1-Push] $_" }

# ------------------------------------------------------------------------------
# Repo 2: Website (NEVERRENDER_LABS_WEBSITE -> PJKT-NRVMOR/neverrender-labs-website)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Website Repo (neverrender-labs-website) ---"
git -C $WebsiteRepo add AGENTS.md
git -C $WebsiteRepo add -u
$Status3 = git -C $WebsiteRepo diff --cached --name-only
if ($Status3) {
    git -C $WebsiteRepo commit -m "chore(web): auto-sync NeverRender Labs website & studio rules [$Timestamp]"
}
git -C $WebsiteRepo pull --rebase --autostash origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Website-Pull] $_" }
git -C $WebsiteRepo push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Website-Push] $_" }

Write-SyncLog "=== Two-Repo GitHub Sync Complete ==="
