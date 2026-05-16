#!/usr/bin/env python3
"""
TOD Content — NocoDB File Uploader

Uploads a .docx file to NocoDB's storage endpoint, then creates a record
in the TOD content library table. Prints JSON on success so the caller can
capture the download URL and record ID.

Usage
-----
  python3 nocodb_upload.py \\
    --file        content/teens/2026-05-10_GAME_Acts20/Game_Teens_Acts20.docx \\
    --sunday-date 2026-05-10 \\
    --cohort      TEENS \\
    --activity    GAME \\
    --passage     "Acts 20" \\
    --file-type   GAME_SHEET \\
    --settings    config/settings.json

Output (stdout, JSON)
---------------------
  {
    "download_url": "https://nocodb.example.com/api/v1/db/storage/uploads/...",
    "record_id": 42
  }

File type values
----------------
  GAME_SHEET | QUIZ_VARIANT_A | QUIZ_VARIANT_B | QUIZ_VARIANT_C |
  QUIZ_ANSWER_KEYS | PRESENTATION_GUIDELINE | PRESENTATION_GROUPS

NocoDB table columns expected
-----------------------------
  sunday_date   SingleLineText
  passage       SingleLineText
  file_name     SingleLineText
  file_size_kb  Number
  download_url  URL
  cohort        SingleSelect  (TEENS | PRE-TEENS)
  activity      SingleSelect  (GAME | QUIZ | PRESENTATION)
  file_type     SingleSelect  (see values above)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' package is required. Run: pip3 install requests", file=sys.stderr)
    sys.exit(1)


def load_settings(_settings_path: str) -> dict:
    required_env = ["NOCODB_API_TOKEN", "NOCODB_BASE_URL", "NOCODB_TABLE_ID"]
    missing = [k for k in required_env if not os.environ.get(k)]
    if missing:
        print(f"Missing env vars: {', '.join(missing)} — source .env before running.", file=sys.stderr)
        sys.exit(1)
    return {
        "api_token": os.environ["NOCODB_API_TOKEN"],
        "base_url":  os.environ["NOCODB_BASE_URL"],
        "table_id":  os.environ["NOCODB_TABLE_ID"],
    }


def upload_file(base_url: str, api_token: str, file_path: Path) -> str:
    """Upload file to NocoDB storage. Returns the download URL."""
    url = f"{base_url.rstrip('/')}/api/v1/db/storage/upload"
    with open(file_path, "rb") as fh:
        resp = requests.post(
            url,
            headers={"xc-token": api_token},
            files={"file": (file_path.name, fh, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            params={"path": f"tod/{datetime.now(timezone.utc).strftime('%Y/%m')}"},
            timeout=60,
        )
    if not resp.ok:
        print(f"Upload failed [{resp.status_code}]: {resp.text}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    # NocoDB returns a list; grab first item's url
    if isinstance(result, list):
        item = result[0]
    else:
        item = result

    # Prefer signedPath if present (NocoDB local storage), else url
    raw_url = item.get("signedPath") or item.get("url") or item.get("path", "")
    if raw_url and not raw_url.startswith("http"):
        raw_url = f"{base_url.rstrip('/')}/{raw_url.lstrip('/')}"
    return raw_url


def create_record(base_url: str, api_token: str, table_id: str, payload: dict) -> int:
    """Create a record in the content library table. Returns the record ID."""
    # v1 endpoint is more reliable — returns the full created record directly
    base_id = os.environ.get("NOCODB_BASE_ID", "")
    url = f"{base_url.rstrip('/')}/api/v1/db/data/noco/{base_id}/{table_id}"
    resp = requests.post(
        url,
        headers={"xc-token": api_token, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    if not resp.ok:
        print(f"Record creation failed [{resp.status_code}]: {resp.text}", file=sys.stderr)
        sys.exit(1)
    data = resp.json()
    return data.get("Id") or data.get("id")


def main():
    parser = argparse.ArgumentParser(description="Upload a TOD content file to NocoDB")
    parser.add_argument("--file",        required=True, help="Path to the .docx file")
    parser.add_argument("--sunday-date", required=True, help="Target Sunday YYYY-MM-DD")
    parser.add_argument("--cohort",      required=True, choices=["TEENS", "PRE-TEENS"])
    parser.add_argument("--activity",    required=True, choices=["GAME", "QUIZ", "PRESENTATION"])
    parser.add_argument("--passage",     required=True, help="e.g. Acts 20")
    parser.add_argument("--file-type",   required=True,
                        choices=["GAME_SHEET", "QUIZ_VARIANT_A", "QUIZ_VARIANT_B",
                                 "QUIZ_VARIANT_C", "QUIZ_ANSWER_KEYS",
                                 "PRESENTATION_GUIDELINE", "PRESENTATION_GROUPS"])
    parser.add_argument("--settings",    default="config/settings.json")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    nc = load_settings(args.settings)
    file_size_kb = round(file_path.stat().st_size / 1024, 1)

    # 1. Upload file to NocoDB storage
    download_url = upload_file(nc["base_url"], nc["api_token"], file_path)

    # 2. Create record in the content library table
    record_payload = {
        "sunday_date":  args.sunday_date,
        "passage":      args.passage,
        "file_name":    file_path.name,
        "file_size_kb": file_size_kb,
        "download_url": download_url,
        "cohort":       args.cohort,
        "activity":     args.activity,
        "file_type":    args.file_type,
    }
    record_id = create_record(nc["base_url"], nc["api_token"], nc["table_id"], record_payload)

    # 3. Output result for caller to capture
    print(json.dumps({"download_url": download_url, "record_id": record_id}))


if __name__ == "__main__":
    main()
