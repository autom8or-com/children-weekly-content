#!/usr/bin/env python3
"""
TOD Content Generation — Checkpoint Manager

Writes/reads .claude/checkpoint.json in the project root.
The file is gitignored so it never pollutes the repo but survives process crashes.

Commands
--------
  init   <date> <activity> <teens_passage> <preteens_passage>
         Start a fresh checkpoint for this Sunday. Overwrites any existing one.

  show   Print the current checkpoint as pretty JSON.

  status Print a human-readable step summary.

  get    <step>
         Print the status of one step (done | pending | error).

  set    <step> <done|pending|error>
         Update one step's status and refresh last_updated.

  add-file  <cohort> <filename> <local_path> <file_type>
         Register a generated file (download_url starts as null).

  set-url   <cohort> <filename> <download_url> <record_id>
         Attach the NocoDB download URL and record ID to a registered file.

  clear  Delete the checkpoint file.

Steps (in order)
----------------
  rotation_lookup
  teens_spec_written
  teens_docx_built
  teens_nocodb_uploaded
  preteens_spec_written
  preteens_docx_built
  preteens_nocodb_uploaded
  telegram_sent

Usage examples
--------------
  python3 checkpoint.py init 2026-05-10 GAME "Acts 20" "John 7"
  python3 checkpoint.py set teens_spec_written done
  python3 checkpoint.py add-file teens "Game_Teens_Acts20.docx" \
      "content/teens/2026-05-10_GAME_Acts20/Game_Teens_Acts20.docx" GAME_SHEET
  python3 checkpoint.py set-url teens "Game_Teens_Acts20.docx" \
      "https://nocodb.example.com/api/v1/storage/..." 42
  python3 checkpoint.py status
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKPOINT_PATH = Path(__file__).resolve().parents[3] / ".claude" / "checkpoint.json"

ORDERED_STEPS = [
    "rotation_lookup",
    "teens_spec_written",
    "teens_docx_built",
    "teens_nocodb_uploaded",
    "preteens_spec_written",
    "preteens_docx_built",
    "preteens_nocodb_uploaded",
    "telegram_sent",
]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load() -> dict:
    if not CHECKPOINT_PATH.exists():
        print("No checkpoint found.", file=sys.stderr)
        sys.exit(1)
    return json.loads(CHECKPOINT_PATH.read_text())


def _save(cp: dict):
    cp["last_updated"] = _now()
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.write_text(json.dumps(cp, indent=2))


def cmd_init(date, activity, teens_passage, preteens_passage):
    cp = {
        "version": "1",
        "target_date": date,
        "activity": activity,
        "teens_passage": teens_passage,
        "preteens_passage": preteens_passage,
        "started_at": _now(),
        "last_updated": _now(),
        "steps": {step: "pending" for step in ORDERED_STEPS},
        "files": {"teens": [], "preteens": []},
    }
    _save(cp)
    print(f"Checkpoint initialised: {date} | {activity} | Teens: {teens_passage} | Pre-Teens: {preteens_passage}")


def cmd_show():
    cp = _load()
    print(json.dumps(cp, indent=2))


def cmd_status():
    cp = _load()
    print(f"\n📋 Checkpoint — {cp['target_date']}  |  {cp['activity']}")
    print(f"   Teens:     {cp['teens_passage']}")
    print(f"   Pre-Teens: {cp['preteens_passage']}")
    print(f"   Started:   {cp['started_at']}")
    print(f"   Updated:   {cp['last_updated']}\n")
    icons = {"done": "✅", "pending": "⏳", "error": "❌"}
    for step in ORDERED_STEPS:
        status = cp["steps"].get(step, "pending")
        print(f"   {icons.get(status, '?')}  {step}: {status}")
    print()
    for cohort in ("teens", "preteens"):
        files = cp["files"].get(cohort, [])
        if files:
            print(f"   {cohort.upper()} files:")
            for f in files:
                url = f.get("download_url") or "(not uploaded yet)"
                print(f"      • {f['filename']}  →  {url}")
    print()


def cmd_get(step):
    cp = _load()
    print(cp["steps"].get(step, "pending"))


def cmd_set(step, status):
    if status not in ("done", "pending", "error"):
        print(f"Invalid status '{status}'. Use: done | pending | error", file=sys.stderr)
        sys.exit(1)
    cp = _load()
    cp["steps"][step] = status
    _save(cp)
    print(f"{step} → {status}")


def cmd_add_file(cohort, filename, local_path, file_type):
    cohort = cohort.lower()
    cp = _load()
    # Avoid duplicates
    existing = [f for f in cp["files"][cohort] if f["filename"] == filename]
    if not existing:
        cp["files"][cohort].append({
            "filename": filename,
            "local_path": local_path,
            "file_type": file_type,
            "download_url": None,
            "nocodb_record_id": None,
        })
        _save(cp)
        print(f"Registered: [{cohort}] {filename}")
    else:
        print(f"Already registered: [{cohort}] {filename}")


def cmd_set_url(cohort, filename, download_url, record_id):
    cohort = cohort.lower()
    cp = _load()
    for f in cp["files"][cohort]:
        if f["filename"] == filename:
            f["download_url"] = download_url
            f["nocodb_record_id"] = int(record_id)
            _save(cp)
            print(f"URL set: [{cohort}] {filename} → {download_url}")
            return
    print(f"File not found in checkpoint: [{cohort}] {filename}", file=sys.stderr)
    sys.exit(1)


def cmd_clear():
    if CHECKPOINT_PATH.exists():
        CHECKPOINT_PATH.unlink()
        print("Checkpoint cleared.")
    else:
        print("No checkpoint to clear.")


# ── Dispatch ───────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    if cmd == "init" and len(args) == 5:
        cmd_init(*args[1:])
    elif cmd == "show":
        cmd_show()
    elif cmd == "status":
        cmd_status()
    elif cmd == "get" and len(args) == 2:
        cmd_get(args[1])
    elif cmd == "set" and len(args) == 3:
        cmd_set(args[1], args[2])
    elif cmd == "add-file" and len(args) == 5:
        cmd_add_file(*args[1:])
    elif cmd == "set-url" and len(args) == 5:
        cmd_set_url(*args[1:])
    elif cmd == "clear":
        cmd_clear()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
