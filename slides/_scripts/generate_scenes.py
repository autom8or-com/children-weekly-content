"""
Step 2: Generate all scene images for a project.
Reads scene definitions from projects/<project>/scenes.json.
Always generates at each scene's configured resolution (2K by default).

Usage:
  python generate_scenes.py deliverance                        # all scenes
  python generate_scenes.py deliverance scene-1/1a scene-1/1b # specific scenes only
  python generate_scenes.py deliverance --redo scene-3/3c     # force re-generate
"""
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent / "_lib"))
from wavespeed import WaveSpeedClient

SLIDES = Path(__file__).parent.parent


def resolve_images(scene: dict, project: Path) -> list[str]:
    images = []
    # Scene-to-scene continuation: base scene output goes first
    if "base_scene" in scene:
        base_path = project / "scenes" / scene["base_scene"] / "output.png"
        if base_path.exists():
            images.append(str(base_path))
        else:
            print(f"  [WARN] Base scene missing: {scene['base_scene']} — generate it first")
    # Character reference images
    for char_id in scene.get("chars", []):
        path = project / "characters" / char_id / "reference.png"
        if path.exists():
            images.append(str(path))
        else:
            print(f"  [WARN] Character ref missing: {char_id} — run generate_characters.py first")
    return images


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python generate_scenes.py <project> [--redo] [scene-id ...]")
        sys.exit(1)

    project_name = args[0]
    redo = "--redo" in args
    only = [a for a in args[1:] if not a.startswith("--")]

    project = SLIDES / "projects" / project_name
    scenes_file = project / "scenes.json"

    if not scenes_file.exists():
        print(f"[ERROR] {scenes_file} not found")
        sys.exit(1)

    scenes = json.loads(scenes_file.read_text())
    client = WaveSpeedClient()

    for scene in scenes:
        scene_id = scene["id"]
        if only and scene_id not in only:
            continue

        out_path = project / "scenes" / scene_id / "output.png"
        if out_path.exists() and not redo:
            print(f"[SKIP] {scene_id} — already exists (use --redo to regenerate)")
            continue

        mode = scene["mode"]
        model = scene.get("model", "nano-banana-pro")
        resolution = scene.get("resolution", "2k")
        images = resolve_images(scene, project)

        print(f"[GEN]  {scene_id}  mode={mode}  model={model}  res={resolution}  refs={len(images)}")
        url = client.generate(
            prompt=scene["prompt"],
            mode=mode,
            model=model,
            images=images if images else None,
            aspect_ratio="16:9",
            resolution=resolution,
        )
        client.download(url, out_path)
        print(f"[DONE] {scene_id} → {out_path}  (cost so far: ${client.total_cost:.3f})")

    print(f"\nTotal cost this run: ${client.total_cost:.3f}")


if __name__ == "__main__":
    main()
