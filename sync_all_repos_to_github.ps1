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

function Resolve-CorpusRebaseIfNeeded {
    param([string]$RepoPath, [string]$Tag)
    $RebaseMerge = Join-Path $RepoPath ".git\rebase-merge"
    $RebaseApply = Join-Path $RepoPath ".git\rebase-apply"
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
    }
}

# ------------------------------------------------------------------------------
# Repo 1: Tree 1 (G_AG_FLDR -> PJKT-NRVMOR/neverrender-creator-journals)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Tree 1 (neverrender-creator-journals) ---"
Resolve-CorpusRebaseIfNeeded -RepoPath $Tree1 -Tag "Tree1"
git -C $Tree1 add .gitattributes AGENTS.md .agents/ 01-vision-and-color-science/ 02-commerce-and-seo-engines/ 03-omnisend-and-mms-foundry/ 04-print-and-vector-foundry/ sync_all_repos_to_github.ps1
$Status1 = git -C $Tree1 diff --cached --name-only
if ($Status1) {
    git -C $Tree1 commit -m "chore(studio): auto-sync NRL cortical stack, voice corpuses & toolkit [$Timestamp]"
}
git -C $Tree1 pull --rebase --autostash origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree1-Pull] $_" }
Resolve-CorpusRebaseIfNeeded -RepoPath $Tree1 -Tag "Tree1"
git -C $Tree1 push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree1-Push] $_" }

# ------------------------------------------------------------------------------
# Repo 2: Tree 2 (project-marshall-college -> PJKT-NRVMOR/project-marshall-college)
# Strictly stage ONLY code, rules, voice skills, and campaign HTML compilers (zero customer PII)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Tree 2 (project-marshall-college) ---"
Resolve-CorpusRebaseIfNeeded -RepoPath $Tree2 -Tag "Tree2"
git -C $Tree2 add .gitattributes AGENTS.md .agents/ scripts/ "project-marshall-college/00-iskenderun/headmaster/04-agents/seo-aeo-weekly-audits/" "project-marshall-college/04-campaigns-outreach-drops/chapman-curatorial-gallery-search.html" "project-marshall-college/04-campaigns-outreach-drops/2026-11-04-scandinavian-gustavian-gallery/index.html" "project-marshall-college/04-campaigns-outreach-drops/2026-11-04-scandinavian-gustavian-gallery/2026-11-04-Omnisend_Scandinavian_Gustavian_Gallery_Full_Import.html" "project-marshall-college/04-campaigns-outreach-drops/approved-active-drops/2026-10-25_Automated_Post_Click_Showroom_Touchpoint/2026-11-09_Automated_Post_Click_Showroom_Touchpoint_Chaphavian.html" "project-marshall-college/04-campaigns-outreach-drops/approved-active-drops/2026-11-09_Chaphavian_Automations_Refresh/"
$Status2 = git -C $Tree2 diff --cached --name-only
if ($Status2) {
    git -C $Tree2 commit -m "chore(pmc): auto-sync Chaphavian guardrails, voice corpuses & compilers [$Timestamp]"
}
git -C $Tree2 pull --rebase --autostash origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree2-Pull] $_" }
Resolve-CorpusRebaseIfNeeded -RepoPath $Tree2 -Tag "Tree2"
git -C $Tree2 push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Tree2-Push] $_" }

# ------------------------------------------------------------------------------
# Repo 3: Website (NEVERRENDER_LABS_WEBSITE -> PJKT-NRVMOR/neverrender-labs-website)
# ------------------------------------------------------------------------------
Write-SyncLog "--- Syncing Website Repo (neverrender-labs-website) ---"
git -C $WebsiteRepo add -u
$Status3 = git -C $WebsiteRepo diff --cached --name-only
if ($Status3) {
    git -C $WebsiteRepo commit -m "chore(web): auto-sync website & PMC approval previews [$Timestamp]"
}
git -C $WebsiteRepo pull --rebase --autostash origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Website-Pull] $_" }
git -C $WebsiteRepo push origin main 2>&1 | ForEach-Object { Write-SyncLog "  [Website-Push] $_" }

Write-SyncLog "=== Three-Repo GitHub Sync Complete ==="
