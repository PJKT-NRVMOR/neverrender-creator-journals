# Clientele PII Quarantine & In-Place Sanitizer

Zero-PII Python forensic utility for isolating raw third-party customer files, buyer invoices, and ETL scripts into a dedicated quarantine directory for secure destruction (such as `WipeFile`), while preserving and sanitizing operational logs, B2B `.docx` / `.xlsx` ledgers, and voice corpora in-place.

## Key Capabilities

- **Dynamic Ground-Truth Harvesting**: Extracts multi-word customer names in-memory from quarantined spreadsheets and ETL scripts before moving them, keeping zero hardcoded PII inside the repository source code.
- **Allowlist-Filtered Regex Scrubbing**: Replaces third-party emails (`[REDACTED_CLIENT_EMAIL]`) and phone numbers (`[REDACTED_CLIENT_PHONE]`) across `.md`, `.py`, `.html`, `.txt`, `.json`, `.docx` XML streams, and `.xlsx` workbooks while preserving operator, studio, principal business, and public vendor identifiers.
- **Non-Destructive Quarantine Staging**: Moves raw clientele artifacts and saves pre-redaction originals under `_QUARANTINE_CLIENTELE_PII_FOR_WIPEFILE/` so the operator can verify diffs before running cryptographic/multi-pass file wiping.
