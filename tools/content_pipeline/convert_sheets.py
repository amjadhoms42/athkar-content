"""
convert_sheets.py
Reads Google Sheets data and writes versioned JSON files to data/.

Usage (local):
  export GOOGLE_SERVICE_ACCOUNT_JSON='{ ...json content... }'
  export GOOGLE_SHEET_ID='your-sheet-id'
  python convert_sheets.py

Usage (CI – GitHub Actions injects the env vars automatically).
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

# ── Config ────────────────────────────────────────────────────────────────────

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

OUTPUT_DIR = Path(__file__).parent.parent.parent / "data"

SHEET_TABS = {
    "items":        "items",
    "readings":     "readings",
    "segments":     "segments",
    "hijri_content": "hijri_content",
}

# ── Auth ──────────────────────────────────────────────────────────────────────

def _get_client() -> gspread.Client:
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not sa_json:
        # Fall back to local file (never committed)
        local = Path(__file__).parent / "service_account.json"
        if local.exists():
            sa_json = local.read_text()
        else:
            sys.exit(
                "ERROR: Set GOOGLE_SERVICE_ACCOUNT_JSON env var or place "
                "service_account.json next to this script."
            )
    info = json.loads(sa_json)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)


def _get_sheet_id() -> str:
    sid = os.environ.get("GOOGLE_SHEET_ID")
    if not sid:
        cfg = Path(__file__).parent / "config.json"
        if cfg.exists():
            sid = json.loads(cfg.read_text()).get("GOOGLE_SHEET_ID")
    if not sid:
        sys.exit(
            "ERROR: Set GOOGLE_SHEET_ID env var or add it to config.json."
        )
    return sid

# ── Sheet → JSON ──────────────────────────────────────────────────────────────

def _sheet_to_records(spreadsheet, tab_name: str) -> list[dict]:
    """Return all non-empty rows from a worksheet as list-of-dicts."""
    try:
        ws = spreadsheet.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        print(f"  WARNING: tab '{tab_name}' not found — skipping.")
        return []

    records = ws.get_all_records(empty2zero=False, head=1)
    # Strip empty-string values so optional fields stay absent from JSON
    cleaned = []
    for row in records:
        entry = {k: v for k, v in row.items() if v != "" and v is not None}
        if entry:
            cleaned.append(entry)
    return cleaned


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = _get_client()
    sid = _get_sheet_id()
    print(f"Opening spreadsheet {sid}…")
    spreadsheet = client.open_by_key(sid)

    file_hashes: dict[str, str] = {}

    for filename, tab in SHEET_TABS.items():
        outfile = f"{filename}.json"
        print(f"  Fetching tab '{tab}' → {outfile}")
        records = _sheet_to_records(spreadsheet, tab)
        content = json.dumps(records, ensure_ascii=False, indent=2)
        (OUTPUT_DIR / outfile).write_text(content, encoding="utf-8")
        file_hashes[outfile] = _sha256(content)
        print(f"    {len(records)} records written.")

    # Read current manifest to bump version
    manifest_path = OUTPUT_DIR / "manifest.json"
    if manifest_path.exists():
        old = json.loads(manifest_path.read_text())
        parts = old.get("version", "0.0.0").split(".")
        parts[-1] = str(int(parts[-1]) + 1)
        version = ".".join(parts)
    else:
        version = "1.0.0"

    manifest = {
        "version": version,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "fileHashes": file_hashes,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nManifest written: version={version}")


if __name__ == "__main__":
    main()
