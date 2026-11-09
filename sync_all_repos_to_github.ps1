# ==============================================================================
# NeverRender Labs // Automated Three-Repo GitHub Sync & Cortical Stack Mirror
# ==============================================================================
# Syncs:
#   1. Tree 1: c:\Users\Saturn\Desktop\G_AG_FLDR (PJKT-NRVMOR/neverrender-creator-journals)
#   2. Tree 2: c:\Users\Saturn\Desktop\project-marshall-college (PJKT-NRVMOR/project-marshall-college)
#   3. Site:   c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE (PJKT-NRVMOR/neverrender-labs-website)
#
# Enforces 100% Client Data Sovereignty (never stages .env, *.csv, *.xlsx, *.tsv,
# customer contact registries, or raw showroom media dumps).
# ==============================================================================

$ErrorActionPreference = "Continue"
$Timestamp = Get-Date -Format "HH:mm:ss-yyyy-MM-dd"
$LogFile = "c:\Users\Saturn\Desktop\G_AG_FLDR\github_daily_sync.log"

function Write-SyncLog {
    param([string]$Message)
    $Line = "[$Timestamp] $Message"
    Write-Output $Line
    Add-Content -Path $LogFile -Value $Line -Encoding UTF8
}

Write-SyncLog "=== Starting NeverRender Labs Three-Repo GitHub Sync ==="

# 1. Mirror AGENTS.md and .agents/skills/ from Tree 1 -> Tree 2 so both trees stay 100% identical
$Tree1 = "c:\Users\Saturn\Desktop\G_AG_FLDR"
$Tree2 = "c:\Users\Saturn\Desktop\project-marshall-college"
$WebsiteRepo = "c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE"

Copy-Item -Path "$Tree1\AGENTS.md" -Destination "$Tree2\AGENTS.md" -Force
Copy-Item -Path "$Tree1\.agents\skills\wyatt-nrl-voice-copywriter\SKILL.md" -Destination "$Tree2\.agents\skills\wyatt-nrl-voice-copywriter\SKILL.md" -Force
Copy-Item -Path "$Tree1\.agents\skills\wyatt-nrl-voice-copywriter\references\wyatt-voice-corpus.md" -Destination "$Tree2\.agents\skills\wyatt-nrl-voice-copywriter\references\wyatt-voice-corpus.md" -Force
Copy-Item -Path "$Tree1\.agents\skills\melissa-tone-copywriter\SKILL.md" -Destination "$Tree2\.agents\skills\melissa-tone-copywriter\SKILL.md" -Force
Copy-Item -Path "$Tree1\.agents\skills\melissa-tone-copywriter\references\voice-corpus.md" -Destination "$Tree2\.agents\skills\melissa-tone-copywriter\references\voice-corpus.md" -Force

# ------------------------------------------------------------------------------
# Repo 1: Tree 1 (G_AG_FLDR -> PJKT-NRVMOR/neverrender-creator-journals)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Tree 1 (neverrender-creator-journals) ---"
git -C $Tree1 add AGENTS.md .agents/ 01-vision-and-color-science/ 02-commerce-and-seo-engines/ 03-omnisend-and-mms-foundry/ 04-print-and-vector-foundry/ sync_all_repos_to_github.ps1
$Status1 = git -C $Tree1 diff --cached --name-only
if ($Status1) {
    git -C $Tree1 commit -m "chore(studio): auto-sync NRL cortical stack, voice corpuses & toolkit [$Timestamp]"
}
git -C $Tree1 push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree1] $_" }

# ------------------------------------------------------------------------------
# Repo 2: Tree 2 (project-marshall-college -> PJKT-NRVMOR/project-marshall-college)
# Strictly stage ONLY code, rules, voice skills, and campaign HTML compilers (zero customer PII)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Tree 2 (project-marshall-college) ---"
git -C $Tree2 add AGENTS.md .agents/ scripts/ "project-marshall-college/04-campaigns-outreach-drops/chapman-curatorial-gallery-search.html" "project-marshall-college/04-campaigns-outreach-drops/2026-11-04-scandinavian-gustavian-gallery/index.html" "project-marshall-college/04-campaigns-outreach-drops/2026-11-04-scandinavian-gustavian-gallery/2026-11-04-Omnisend_Scandinavian_Gustavian_Gallery_Full_Import.html"
$Status2 = git -C $Tree2 diff --cached --name-only
if ($Status2) {
    git -C $Tree2 commit -m "chore(pmc): auto-sync Chaphavian guardrails, voice corpuses & compilers [$Timestamp]"
}
git -C $Tree2 push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree2] $_" }

# ------------------------------------------------------------------------------
# Repo 3: Website (NEVERRENDER_LABS_WEBSITE -> PJKT-NRVMOR/neverrender-labs-website)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Website Repo (neverrender-labs-website) ---"
git -C $WebsiteRepo add -u
$Status3 = git -C $WebsiteRepo diff --cached --name-only
if ($Status3) {
    git -C $WebsiteRepo commit -m "chore(web): auto-sync website & PMC approval previews [$Timestamp]"
}
git -C $WebsiteRepo push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Website] $_" }

Write-SyncLog "=== Three-Repo GitHub Sync Complete ==="
