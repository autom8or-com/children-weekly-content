"""
Step 1: Generate character reference sheets for a project.
Reads character definitions from projects/<project>/characters.json.
Outputs saved to projects/<project>/characters/<id>/reference.png.
Run once per project. Re-run only when a character design needs updating.

Usage:
  python generate_characters.py deliverance
  python generate_characters.py deliverance angela jesus            # specific characters only
  python generate_characters.py deliverance --redo                  # force regenerate all
  python generate_characters.py deliverance god-a --redo            # force regenerate one
  python generate_characters.py deliverance --provider wavespeed    # override provider
  python generate_characters.py deliverance --provider mmx          # mmx CLI (no per-image $)

Provider defaults to kie.ai. Override with --provider, a "provider" field in
project.json, or the IMAGE_PROVIDER env var.

Available providers:
  kie        kie.ai API (default; needs KIE_API_KEY)
  wavespeed  WaveSpeed API (needs WAVESPEEDAI_API_KEY)
  mmx        local `mmx` CLI (needs `mmx auth login`; quota only, no $ per image)
"""
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent / "_lib"))
from provider import resolve_provider, get_client

SLIDES = Path(__file__).parent.parent


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python generate_characters.py <project> [--provider kie|wavespeed|mmx] [char_id ...]")
        sys.exit(1)

    project_name = args[0]
    rest = args[1:]

    provider_cli = None
    if "--provider" in rest:
        i = rest.index("--provider")
        provider_cli = rest[i + 1]
        del rest[i:i + 2]

    redo = "--redo" in rest
    only = [a for a in rest if not a.startswith("--")]

    project = SLIDES / "projects" / project_name
    chars_file = project / "characters.json"

    if not chars_file.exists():
        print(f"[ERROR] {chars_file} not found")
        sys.exit(1)

    characters = json.loads(chars_file.read_text())
    provider = resolve_provider(provider_cli, project)
    client = get_client(provider)
    print(f"[PROVIDER] {provider}")

    for char in characters:
        char_id = char["id"]
        if only and char_id not in only:
            continue

        out_path = project / "characters" / char_id / "reference.png"
        if out_path.exists() and not redo:
            print(f"[SKIP] {char_id} — reference already exists (use --redo to regenerate)")
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
