\---  
name: context-log-organizer  
description: Perform a daily full adaptive sweep of Google Drive. Identify, read, smartly rename using hacker-style lowercase kebab-case naming (e.g., agent-log: ..., tech-spec: ..., case-log: ..., daily-note: ...), and organize Gemini "Save To Docs" exports, "Untitled" documents, agent verbose chat transcripts, and daily uploads into 00\_System\_Context\_Logs and 01\_AGENT\_SPARK/agent-logs, manage agent session lifecycles, stage duplicates in pole-of-inaccessibility, and maintain a spotless root structure.  
allowed-tools: drive sheets\_agent docs\_agent  
\---  
\# Context Log Organizer

A skill for systematically sweeping, reading, smartly renaming, classifying, and indexing all loose files, Gemini "Save to Docs" exports, verbose agent chat transcripts, duplicate staging, deep research reports, and temporary clutter across Google Drive using a hacker-style lowercase kebab-case naming convention.

\#\# When to Use  
Use this skill when:  
\- Running the daily Drive organization and sweep routine.  
\- The user asks to perform a full Drive sweep, clean up loose files, or organize root directory items (\`/context-log-organizer\`).  
\- Inspecting and organizing daily saves/uploads, especially "Save to Docs" files named "Untitled" or with raw prompt snippets.  
\- Managing agent verbose chat transcripts, daily append-only pastes, and retired agent session lifecycles.  
\- Redundant or duplicate files need to be identified and staged in \`pole-of-inaccessibility\` for manual review.  
\- Chat transcripts, technical specs, or case management notes need standardized naming and routing.  
\- The user requests a comprehensive recursive indexing sweep across parent and child directories to update \`Master\_Context\_Index\_Log\` for NotebookLM integration.

\#\# Steps

1\. \*\*Root Directory Scan & Daily Uploads Sweep\*\*:  
   \- Scan \`parentId \= 'root'\` and recently saved/modified files for loose items (Docs, PDFs, Markdown, TXT, etc.).  
   \- Protect primary root folders from being moved, renamed, or altered:  
     \- \`00\_LEGAL\_WHISTLEBLOWER\_EVIDENTIARY\_DOSSIER\` (ID: \`1G33RWVjUnIaMSX81WELfyqwnk-TjDiK2\` — Active whistleblower dockets, master chronologies, entity indices, and damage memos)  
     \- \`00\_System\_Context\_Logs\` (ID: \`1mQ5DvOnHZmZwSmQY06gJ3BH6LrfPQDZJ\` — Master system logs, transcripts, and telemetry)  
     \- \`00\_SANDBOX\` (ID: \`17t7ZjNTDhEpir1Fz6g7FQYsoDjWfc0Ah\` — Temporary scratchpad / transient exports / daily notes)  
     \- \`01\_AGENT\_SPARK\` (ID: \`1cK5CLb6ypTcBFYHXXX4bRTUxu78hKS22\` — Agent operational workspace, specs, and LUT resources; contains \`agent-logs\` \[ID: \`1fweuCT\_QJOxWkHTSm6PLSJ-xW3ohKSRQ\`\])  
     \- \`02\_FAMILY\_OPERATION\_HUB\` (ID: \`1bj9Mimo0tBjBEveJOti4ADfNOg21K8z2\` — Active family, medical & housing hub)  
     \- \`03\_PROJECT\_NEVERMORE\` (ID: \`1WEhn9WTRZpSOonbAndI8zvwC5rU8MwVJ\` — Creative media & 3D projects)  
     \- \`04\_ALL\_PROJECTS\_RESEARCH\_REPORTS\` (ID: \`10Gpfg5RH6cC0BjNu0gXOfZZktTR2mKCd\` — Deep research deliverables and whitepapers)  
     \- \`05\_FILE\_XFR\_PRINTING\` (ID: \`1Me2KN16aOmtUfFP5h9XOQDM6dEQLu5dP\` — Transfer & printing staging)  
     \- \`06\_LEGAL\_EVICTION\_ARCHIVE\_HISTORICAL\` (ID: \`1CpP4fNlfa3HtWEGbtqZC91g1AmVhNJpD\` — Archived closed unlawful detainer & past housing litigation files)  
     \- \`pole-of-inaccessibility\` (ID: \`1fzv5HwYtOu5o2W0Vg9Z8qZLE7zfsGC\_S\` — Staging folder for duplicate files awaiting manual deletion; formerly "CHECK BEFORE DELETING")  
     \- \`Work Related\` (ID: \`1RqSCOILH2YNFeS5Y7RvFQP40SSaSxX9P\` — Consolidated job applications, resumes, career assets, and THE\_OASIS)  
     \- System/App folders: \`Cube ACR\` (\`1QPx4jt6oYol127Ogh740NKlmmTa5LU7V\`), \`Saved from Chrome\` (\`12CYvZWlmXPbUzjcUug8av3lhQPffLWGA\`), \`Self Help Logs\` (\`17MVEQkIpflASaeiqD8LQePv-0ps44ajE\`), \`Voice Recorder\` (\`1fA\_Mxuo9KTPiAUVQ4Iy6T9CGZCFugJhq\`), \`Camera Uploads\` (\`1wNNn95jyIkraJ6nTqOMCNTs97-Hgl2HV\`), \`TAPO\` (\`1sCQhQ7AisQgz15JIoRtei2mZ\_cyIRKow\`).  
   \- \*Note on Legacy Folders\*: Empty legacy staging folders like \`To Be Printed\` (\`1Kfgu9KnL1nr6mw1I9OMb-\_hwPwbpUeKd\`) are deprecated and should not receive new files.

2\. \*\*Gemini "Save to Docs" Audit, Content Reading & Hacker-Style Standardized Renaming\*\*:  
   \- Identify any loose documents, exports, or uploads in root or staging folders that have:  
     \- The default title \`"Untitled"\` or \`"Untitled document"\`  
     \- Truncated prompt snippets / raw user queries as titles (e.g., \`"I'm searching for..."\`, \`"My mom and I were just talking..."\`, \`"You know what? I'm going to..."\`, URLs as titles)  
     \- Missing category prefixes or legacy uppercase/spaced titles.  
   \- Read the document content (\`drive:read\_file\_content\`) to understand the core subject matter, context, participants, and date.  
   \- \*\*Hacker-Style Naming Convention\*\*:  
     \- Format: \`\<category-prefix\>: \<kebab-cased-descriptive-title\>\`  
     \- Prefix: Lowercase with hyphens for multi-word prefixes, followed by a colon and a space (\`: \`).  
     \- Title: All lowercase words separated strictly by single hyphens (\`kebab-case\`), no spaces, no uppercase, no underscores (e.g., \`agent-log: cassini-v7-6-convergence-day-telemetry\`).  
   \- Apply the hacker-style taxonomy mapping:  
     \- \*\*\`agent-log: \<kebab-case-title\>\`\*\*: Verbose agent chat session exports and append-only transcripts across all agent personas (Cassini, SRE v1/v2, Agent Spark, Project Nevermore, Antigravity, The Oasis, Golden, Master, etc.) copied and pasted at the end of each day; handles both short daily updates and extremely long multi-hundred-page sessions. When an agent's token limit or Google Docs limit is hit, the session is formally retired (e.g., \`agent-log: cassini-v7-55-masterclass-retired-09212026-435-pages\`) and a new version is started.  
     \- \*\*\`tech-spec: \<kebab-case-title\>\`\*\*: Technical architecture, SRE systems, LLM speculative decoding (llama.cpp PRs, block diffusion, DFLASH, DBLAST, MTP), GPU/VRAM optimizations, Vulkan cooperative matrix kernels, APU/Beelink tuning, audio DSP / psychoacoustics / subtractive EQ engineering (e.g., \`tech-spec: modern-virtual-production-tools-and-cinematography-guide\`).  
     \- \*\*\`case-log: \<kebab-case-title\>\`\*\*: Active CalAIM Enhanced Care Management (ECM), Serene Health / Presidium Health coordination, housing transitions (Modera Melrose, Pronto Housing, The Terraces), DMHC regulatory filings / case numbers (1432899, 1433498), medical appointment logs, caregiver notes, recorded phone call transcripts with caseworkers/supervisors (e.g., \`case-log: presidium-health-mobile-ecm-intake-session\`).  
     \- \*\*\`daily-note: \<kebab-case-title\>\`\*\*: Daily evaluation assessments, QA job tests, fact-check briefings, personal work notes, study journal entries, reflective logs (e.g., \`daily-note: submarine-stealth-and-protein-powered-rendering-logistics\`).  
     \- \*\*\`notebook-chat: \<kebab-case-title\>\`\*\*: Specific chat session exports from NotebookLM notebooks or research note dumps (e.g., \`notebook-chat: deterministic-execution-engine-dee-v1\`).  
     \- \*\*\`cinematic-prod: \<kebab-case-title\>\`\*\*: Character bibles (Beau, Val, Vespera), scene storyboards, OCIO LUT grading, 8-Bit Theater District media pipelines, optical lighting analysis (e.g., \`cinematic-prod: macau-sovereign-baize-act-i-8-shot-sequence\`).  
     \- \*\*\`work-career: \<kebab-case-title\>\`\*\*: Job applications (Masco, Telus, Indeed, Motion Recruitment), customized resumes, cover letters, career portfolios, interview preparation dossiers (e.g., \`work-career: notebook-chat-socioeconomic-responsibility-executive-flynn-v3\`).  
     \- \*\*\`legal-dossier: \<kebab-case-title\>\`\*\*: Formal whistleblower filings, chronological timelines, master entity directories, damage memorandums, and exhibit catalogs (e.g., \`legal-dossier: serene-health-whistleblower-exhibit-master-index\`).  
     \- \*\*\`research-report: \<kebab-case-title\>\`\*\*: In-depth research reports, academic whitepapers, modular technical guides, and architectural evaluations (e.g., \`research-report: enterprise-architecture-gemini-omni-and-google-flow\`).  
     \- \*\*\`legal-historical: \<kebab-case-title\>\`\*\*: Archived unlawful detainer records and historical tenancy dispute files (e.g., \`legal-historical: closed-ud-case-chronology\`).  
     \- \*\*\`housing-ops: \<kebab-case-title\>\`\*\*: Transitional housing logs, hotel expense folios, rental applications, and insurance loss-of-use claims (e.g., \`housing-ops: asegurant-ale-expense-loss-of-use-folio\`).  
     \- \*\*\`system-archive: \<kebab-case-title\>\`\*\*: System catalogs, index dumps, and drive archives (e.g., \`system-archive: master-drive-catalog-september-2026\`).  
     \- \*\*\`staged-dup: \<kebab-case-title\>\`\*\*: Staged duplicate or superseded files placed into \`pole-of-inaccessibility\` awaiting manual user review.  
   \- Rename the file using \`drive:update\_file\` (\`title\`).

3\. \*\*Classification & Folder Routing\*\*:  
   \- Route and move the renamed documents (\`drive:update\_file\` with \`parentId\`):  
     \- \*\*Verbose Agent Chat Logs & Transcripts\*\* \-\> \`01\_AGENT\_SPARK/agent-logs\` (ID: \`1fweuCT\_QJOxWkHTSm6PLSJ-xW3ohKSRQ\`).  
     \- \*\*SRE & Technical Specs\*\* \-\> \`00\_System\_Context\_Logs/02\_SRE\_System\_Engineering\` (ID: \`1Iz2IMEl2G6WEh41O-nQwJX96vpN0euG-\`) or \`03\_PROJECT\_NEVERMORE/04a\_TECH\_LOGS\` (ID: \`1M-tQ2JL1aEAPtzdPc1p3EMjzDn9miyta\`).  
     \- \*\*Active Case Management & Transcripts\*\* \-\> \`00\_System\_Context\_Logs/03\_Case\_Management\_Logs\` (ID: \`1DtZPpng-Cxigd6JnDn5o\_C6UGHKygAPY\`) and \`02\_FAMILY\_OPERATION\_HUB/LEGAL\_AND\_HOUSING\`.  
     \- \*\*Cinematic Production & Creative Notes\*\* \-\> \`00\_System\_Context\_Logs/01\_Cinematic\_Production\` (ID: \`1MSXWHN49tEw0ltAONq0WlDE6R8JBaGwK\`) or \`03\_PROJECT\_NEVERMORE\`.  
     \- \*\*Historical Legal & Eviction Archive\*\* \-\> \`06\_LEGAL\_EVICTION\_ARCHIVE\_HISTORICAL\` (ID: \`1CpP4fNlfa3HtWEGbtqZC91g1AmVhNJpD\`) (closed Case No. 26UD022187C records, Las Palmas historical dispute logs).  
     \- \*\*Work & Career\*\* \-\> \`Work Related\` (ID: \`1RqSCOILH2YNFeS5Y7RvFQP40SSaSxX9P\`).  
     \- \*\*Research Reports & Whitepapers\*\* \-\> \`04\_ALL\_PROJECTS\_RESEARCH\_REPORTS\` (ID: \`10Gpfg5RH6cC0BjNu0gXOfZZktTR2mKCd\`).  
     \- \*\*Daily Notes / Transient Files\*\* \-\> \`00\_SANDBOX\` (ID: \`17t7ZjNTDhEpir1Fz6g7FQYsoDjWfc0Ah\`) or dedicated subfolders.

4\. \*\*Agent Verbose Chat Logs & Session Lifecycle Management (Priority One)\*\*:  
   \- \*\*Priority One Detection\*\*: Prioritize scanning Drive (including root, \`00\_SANDBOX\`, recent uploads, and loose docs) for any and all agent verbose chat transcripts, append-only logs, and conversational dumps (e.g., Cassini v7.x, Agent Spark, SRE v1/v2, Antigravity, The Oasis, Project Nevermore, Golden, Master, etc.), whether short daily session snippets or extremely long multi-hundred-page documents.  
   \- \*\*Standardize Naming to \`agent-log:\`\*\*:  
     \- Format: \`agent-log: \<kebab-cased-descriptive-title\>\`  
     \- When an agent's token limit or Google Docs limit is reached and a version is retired to start fresh, append the retirement status, date, and page count if known (e.g., \`agent-log: cassini-v7-55-masterclass-retired-09212026-435-pages\`).  
   \- \*\*Route to Dedicated Agent Log Vault\*\*:  
     \- Relocate all raw and append-only agent session logs directly into \`01\_AGENT\_SPARK/agent-logs\` (ID: \`1fweuCT\_QJOxWkHTSm6PLSJ-xW3ohKSRQ\`).  
   \- \*\*Daily Telemetry Synthesis & Cassini Consolidation\*\*:  
     \- For active core execution daemons (such as Cassini), synthesize and maintain the single daily consolidated Google Doc named \`cassini-logs-{yyyy-mm-dd}\` inside \`00\_System\_Context\_Logs/02\_SRE\_System\_Engineering\` (ID: \`1Iz2IMEl2G6WEh41O-nQwJX96vpN0euG-\`), linking directly to the underlying raw session in \`01\_AGENT\_SPARK/agent-logs\`.

5\. \*\*Duplicate Detection & Safe Staging Protocol (\`pole-of-inaccessibility\`)\*\*:  
   \- Systematically identify redundant files across Drive (exact content duplicates, numbered copies like \`(1)\`, \`(3)\`, \`Copy of...\`, \`- Copy\`, or superseded drafts).  
   \- \*\*Zero Auto-Deletion Rule\*\*: Never permanently delete duplicate files automatically.  
   \- Move all candidate duplicates into \`pole-of-inaccessibility\` (ID: \`1fzv5HwYtOu5o2W0Vg9Z8qZLE7zfsGC\_S\`) for manual user review.  
   \- Prepend \`staged-dup: \<kebab-cased-title\>\` to staged duplicate files.  
   \- Ensure the primary master file remains safely in its designated folder.

6\. \*\*Adaptive Folder Organization & Root Clutter Sweep\*\*:  
   \- Scan remaining non-doc loose files and folders in root. Keep root completely spotless.  
   \- Evaluate whether loose items belong in existing project folders (\`00\_SANDBOX\`, \`03\_PROJECT\_NEVERMORE\`, \`04\_ALL\_PROJECTS\_RESEARCH\_REPORTS\`, \`Work Related\`, \`02\_FAMILY\_OPERATION\_HUB\`, \`01\_AGENT\_SPARK/agent-logs\`, etc.).  
   \- If a new distinct project or topic category with multiple files emerges (e.g., \`THE\_OASIS\`, \`WORK\_RELATED\`, \`HOMELESS\_2\_HOUSING\`), \*\*adaptively relocate or nest it\*\* into the appropriate primary parent directory (\`Work Related\`, \`02\_FAMILY\_OPERATION\_HUB\`) so that the root remains limited strictly to the 18 primary root folders.  
   \- If temporary sync artifacts, error files (e.g., \`Z\*.txt\`), or hash-named clutter folders are detected, move them into \`00\_SANDBOX\` or \`Sync Error Clutter \- Move to Trash\`.

7\. \*\*Metadata Logging & Full Drive Indexing (9-Column Schema & NotebookLM Golden Bridge)\*\*:  
   \- Log all renamed, moved, staged, consolidated, or newly indexed items in \`Master\_Context\_Index\_Log\` (ID: \`1VsY5QJ4y5dFUj6WaYWkWBTy15LPL-lTnDEHV3\_PohZA\`).  
   \- \*\*NotebookLM Live Integration\*\*: Because \`Master\_Context\_Index\_Log\` is attached as a live source in the user's master NotebookLM notebooks (\`SOCIOECONOMIC RESPONSIBILITY EXECUTIVE\` and \`THE\_OASIS\`), the index enables NotebookLM to query exact URLs, file paths, and document summaries to self-heal missing citations and retrieve references.  
   \- \*\*Mandatory 9-Column Format\*\*:  
     1\. \`Timestamp\`: Local creation/modification date (\`YYYY-MM-DD HH:MM\`).  
     2\. \`Original Title\`: Raw filename before renaming.  
     3\. \`Renamed Standardized Title\`: Full standardized title matching hacker-style taxonomy (e.g., \`agent-log: cassini-v7-6-convergence-day-telemetry\`).  
     4\. \`Category / Taxonomy\`: Core classification (\`agent-log\`, \`case-log\`, \`tech-spec\`, \`work-career\`, \`cinematic-prod\`, \`research-report\`, \`legal-dossier\`, \`legal-historical\`, \`daily-note\`, \`system-archive\`, \`staged-dup\`).  
     5\. \`Target Destination Folder\`: Exact folder path (e.g., \`01\_AGENT\_SPARK/agent-logs\`, \`00\_System\_Context\_Logs/03\_Case\_Management\_Logs\`).  
     6\. \`File Type / MIME\`: Human-readable format descriptor (\`Google Doc\`, \`PDF\`, \`Google Sheet\`, \`Markdown\`, \`Audio\`, \`Video\`, \`Image\`).  
     7\. \`File ID / Drive URL\`: Direct clickable URL (\`https\://docs.google.com/document/d/\<id\>/edit\`, \`https\://drive.google.com/file/d/\<id\>/view\`, or spreadsheet URL). Never leave blank.  
     8\. \`Summary / Context Description\`: Concise 1-sentence description detailing the substantive context, parties, case numbers, or technical specs.  
     9\. \`Status\`: Processing outcome (\`SUCCESS\`, \`STAGED\_DUP\`, \`CONSOLIDATED\`).  
   \- \*\*Drive-Wide Indexing Sweeps\*\*: When running comprehensive indexing of parent and child directories, batch append unindexed files in chunks of 40–50 rows using \`sheets\_agent:call\` with structured XML payloads (\`\<sheet\_task\_payload\>\`), auto-resizing columns A through I to maintain clean layout.

8\. \*\*Daily Reporting\*\*:  
   \- Deliver a comprehensive summary report in chat detailing all swept items, renamed "Save to Docs" files, verbose chat logs routed to \`01\_AGENT\_SPARK/agent-logs\`, newly staged duplicates in \`pole-of-inaccessibility\`, consolidated telemetry logs, and confirmation that the Drive root is spotless.  
   \- Include inline clickable markdown links (\`\[Title\](URL)\`) for all processed files, parent folders, and master logs.