"""
Step 1: Generate character reference sheets for a project.
Reads character definitions from projects/<project>/characters.json.
Outputs saved to projects/<project>/characters/<id>/reference.png.
Run once per project. Re-run only when a character design needs updating.

Usage:
  python generate_characters.py deliverance
  python generate_characters.py deliverance angela jesus   # specific characters only
"""
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent / "_lib"))
from wavespeed import WaveSpeedClient

SLIDES = Path(__file__).parent.parent


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python generate_characters.py <project> [char_id ...]")
        sys.exit(1)

    project_name = args[0]
    only = args[1:]  # optional filter: specific character IDs

    project = SLIDES / "projects" / project_name
    chars_file = project / "characters.json"

    if not chars_file.exists():
        print(f"[ERROR] {chars_file} not found")
        sys.exit(1)

    characters = json.loads(chars_file.read_text())
    client = WaveSpeedClient()

    for char in characters:
        char_id = char["id"]
        if only and char_id not in only:
            continue

        out_path = project / "characters" / char_id / "reference.png"
        if out_path.exists():
            print(f"[SKIP] {char_id} — reference already exists")
            continue

        print(f"[GEN]  {char_id}...")
        url = client.generate(
            prompt=char["prompt"],
            mode="text-to-image",
            model="nano-banana-pro",
            aspect_ratio="16:9",
            resolution="2k",
        )
        client.download(url, out_path)
        print(f"[DONE] {char_id} → {out_path}  (cost so far: ${client.total_cost:.3f})")

    print(f"\nTotal: ${client.total_cost:.3f}")


if __name__ == "__main__":
    main()
