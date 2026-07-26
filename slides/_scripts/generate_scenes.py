"""
Step 2: Generate all scene images for a project.
Reads scene definitions from projects/<project>/scenes.json.

Supported modes:
  text-to-image  — pure AI generation, no reference images required
  edit           — AI edit using character refs and/or a base scene image
  edit-fast      — lightweight AI edit of a base scene (nano-banana-2 only)
  composite      — PIL-only: stitch multiple images into a panel layout (no API call)
  reuse          — copy output from another scene in this project (no API call)

Optional post-processing fields (applied after the API call):
  pip     — stamp a smaller version of another scene onto the output (picture-in-picture)
  overlay — stamp a graphic asset from slides/_assets/ onto the output

Usage:
  python generate_scenes.py <project>                              # all scenes
  python generate_scenes.py <project> scene-1/1a scene-1/1b       # specific scenes only
  python generate_scenes.py <project> --redo scene-3/3c           # force re-generate
  python generate_scenes.py <project> --provider wavespeed        # override provider
  python generate_scenes.py <project> --provider mmx              # mmx CLI (quota only)

Provider defaults to kie.ai. Override with --provider, a "provider" field in
project.json, or the IMAGE_PROVIDER env var.

Available providers:
  kie        kie.ai API (default; needs KIE_API_KEY)
  wavespeed  WaveSpeed API (needs WAVESPEEDAI_API_KEY)
  mmx        local `mmx` CLI (needs `mmx auth login`; quota only, no $ per image).
             Subject-ref takes a single image per call — for multi-ref consistency
             in edit-mode scenes, fall back to --provider kie or --provider wavespeed.
"""
import sys
import json
import shutil
import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent.parent / "_lib"))
from provider import resolve_provider, get_client

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

SLIDES = Path(__file__).parent.parent
ASSETS = SLIDES / "_assets"

# One timestamp per invocation, so a whole regen run is grouped in one folder.
RUN_TS = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def backup_existing(out_path: Path, project: Path, scene_id: str):
    """Copy an existing output.png to a timestamped backup folder before it is
    overwritten by a regeneration. No-op if there is nothing to back up."""
    if not out_path.exists():
        return
    backup_dir = project / "_backups" / RUN_TS / scene_id.replace("/", "_")
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / out_path.name
    shutil.copy2(out_path, dest)
    print(f"  [BACKUP] {scene_id} → {dest.relative_to(project)}")


# ---------------------------------------------------------------------------
# Image resolution helpers
# ---------------------------------------------------------------------------

def resolve_base_scene(scene: dict, project: Path) -> Path | None:
    if "base_scene" not in scene:
        return None
    base_project_name = scene.get("base_project")
    if base_project_name:
        base_project = SLIDES / "projects" / base_project_name
    else:
        base_project = project
    base_id = scene["base_scene"]
    for filename in ("output.png", "draft.png"):
        p = base_project / "scenes" / base_id / filename
        if p.exists():
            return p
    print(f"  [WARN] Base scene not found: {base_id} in {base_project.name} — generate it first")
    return None


def resolve_chars(scene: dict, project: Path, char_project: Path) -> list[str]:
    paths = []
    for char_id in scene.get("chars", []):
        for search_project in (project, char_project):
            if search_project is None:
                continue
            p = search_project / "characters" / char_id / "reference.png"
            if p.exists():
                paths.append(str(p))
                break
        else:
            print(f"  [WARN] Character ref missing: {char_id} — run generate_characters.py first")
    return paths


def resolve_images(scene: dict, project: Path, char_project: Path) -> list[str]:
    images = []
    base = resolve_base_scene(scene, project)
    if base:
        images.append(str(base))
    images.extend(resolve_chars(scene, project, char_project))
    for ref in scene.get("scene_refs", []):
        ref_id            = ref["source"]
        ref_project_name  = ref.get("project")
        ref_project       = SLIDES / "projects" / ref_project_name if ref_project_name else project
        for fname in ("output.png", "draft.png"):
            p = ref_project / "scenes" / ref_id / fname
            if p.exists():
                images.append(str(p))
                break
        else:
            print(f"  [WARN] scene_ref not found: {ref_id} in {ref_project.name} — skipping")
    return images


# ---------------------------------------------------------------------------
# PIL post-processing
# ---------------------------------------------------------------------------

def require_pil(feature: str):
    if not PIL_AVAILABLE:
        print(f"  [ERROR] PIL not installed — cannot process {feature}. Run: pip install Pillow")
        sys.exit(1)


POSITION_MAP = {
    "center":        lambda w, h, pw, ph: ((w - pw) // 2, (h - ph) // 2),
    "center-right":  lambda w, h, pw, ph: (w - pw - int(w * 0.04), (h - ph) // 2),
    "center-left":   lambda w, h, pw, ph: (int(w * 0.04), (h - ph) // 2),
    "top-right":     lambda w, h, pw, ph: (w - pw - int(w * 0.04), int(h * 0.04)),
    "top-left":      lambda w, h, pw, ph: (int(w * 0.04), int(h * 0.04)),
    "bottom-right":  lambda w, h, pw, ph: (w - pw - int(w * 0.04), h - ph - int(h * 0.04)),
    "bottom-left":   lambda w, h, pw, ph: (int(w * 0.04), h - ph - int(h * 0.04)),
}


def apply_pip(out_path: Path, pip_cfg: dict, project: Path):
    require_pil("pip")
    source_id = pip_cfg["source"]
    pip_type  = pip_cfg.get("type", "scene")

    if pip_type == "character":
        source_path = project / "characters" / source_id / "reference.png"
        if not source_path.exists():
            print(f"  [WARN] PiP character not found: {source_id} — skipping pip")
            return
    else:
        pip_project_name = pip_cfg.get("project")
        pip_project = SLIDES / "projects" / pip_project_name if pip_project_name else project
        for filename in ("output.png", "draft.png"):
            source_path = pip_project / "scenes" / source_id / filename
            if source_path.exists():
                break
        else:
            print(f"  [WARN] PiP source not found: {source_id} — skipping pip")
            return

    base_img = Image.open(out_path).convert("RGBA")
    pip_img  = Image.open(source_path).convert("RGBA")

    scale    = pip_cfg.get("scale", 0.28)
    position = pip_cfg.get("position", "center-right")
    border   = pip_cfg.get("border", True)

    pw = int(base_img.width * scale)
    ph = int(pip_img.height * (pw / pip_img.width))
    pip_img = pip_img.resize((pw, ph), Image.LANCZOS)

    if border:
        from PIL import ImageDraw
        border_px = max(3, int(pw * 0.015))
        bordered = Image.new("RGBA", (pw + border_px * 2, ph + border_px * 2), (255, 255, 255, 230))
        bordered.paste(pip_img, (border_px, border_px))
        pip_img = bordered
        pw, ph = pip_img.size

    pos_fn = POSITION_MAP.get(position, POSITION_MAP["center-right"])
    x, y = pos_fn(base_img.width, base_img.height, pw, ph)

    base_img.paste(pip_img, (x, y), pip_img)
    base_img.convert("RGB").save(out_path)
    print(f"  [PiP]  stamped {source_id} at {position} (scale={scale})")


def apply_overlay(out_path: Path, overlay_cfg: dict):
    require_pil("overlay")
    asset_name = overlay_cfg["asset"]
    asset_path = ASSETS / f"{asset_name}.png"
    if not asset_path.exists():
        print(f"  [WARN] Overlay asset not found: {asset_path} — skipping overlay")
        return

    base_img    = Image.open(out_path).convert("RGBA")
    overlay_img = Image.open(asset_path).convert("RGBA")

    scale    = overlay_cfg.get("scale", 0.40)
    opacity  = overlay_cfg.get("opacity", 0.90)
    position = overlay_cfg.get("position", "center")

    pw = int(base_img.width * scale)
    ph = int(overlay_img.height * (pw / overlay_img.width))
    overlay_img = overlay_img.resize((pw, ph), Image.LANCZOS)

    if opacity < 1.0:
        r, g, b, a = overlay_img.split()
        a = a.point(lambda v: int(v * opacity))
        overlay_img = Image.merge("RGBA", (r, g, b, a))

    pos_fn = POSITION_MAP.get(position, POSITION_MAP["center"])
    x, y = pos_fn(base_img.width, base_img.height, pw, ph)

    base_img.paste(overlay_img, (x, y), overlay_img)
    base_img.convert("RGB").save(out_path)
    print(f"  [OVR]  stamped {asset_name} at {position} (scale={scale}, opacity={opacity})")


# ---------------------------------------------------------------------------
# Composite (panel stitch)
# ---------------------------------------------------------------------------

LAYOUT_PANELS = {
    "3-panel-vertical":     3,
    "3-panel-horizontal":   3,
    "2-panel-vertical":     2,
    "2-panel-horizontal":   2,
    "4-panel-horizontal":   4,   # NEW: true horizontal strip, 4 wide × 1 tall (comic strip)
}

def build_composite(scene: dict, out_path: Path):
    require_pil("composite")
    layout  = scene.get("layout", "3-panel-vertical")
    sources = scene.get("sources", [])
    panels  = LAYOUT_PANELS.get(layout, len(sources))
    gutter  = int(scene.get("gutter", 0))  # px between panels (optional)

    images = []
    for src in sources[:panels]:
        p = SLIDES / src
        if not p.exists():
            print(f"  [WARN] Composite source not found: {p} — skipping")
            return
        images.append(Image.open(p).convert("RGB"))

    if not images:
        print(f"  [WARN] No valid composite sources found — skipping")
        return

    ref_w = images[0].width
    ref_h = images[0].height

    images = [img.resize((ref_w, ref_h), Image.LANCZOS) for img in images]

    # 4-panel-horizontal: ALWAYS a horizontal strip (wide canvas), regardless of the
    # "vertical in name" branch below. With optional thin black gutter.
    if layout == "4-panel-horizontal":
        total_w = ref_w * len(images) + gutter * (len(images) - 1)
        canvas = Image.new("RGB", (total_w, ref_h))
        for i, img in enumerate(images):
            x = i * (ref_w + gutter)
            canvas.paste(img, (x, 0))
    else:
        is_vertical = "vertical" in layout
        if is_vertical:
            canvas = Image.new("RGB", (ref_w * len(images), ref_h))
            for i, img in enumerate(images):
                canvas.paste(img, (ref_w * i, 0))
        else:
            canvas = Image.new("RGB", (ref_w, ref_h * len(images)))
            for i, img in enumerate(images):
                canvas.paste(img, (0, ref_h * i))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)
    print(f"  [PIL]  composite saved → {out_path}  (layout={layout}, panels={len(images)}, gutter={gutter})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_char_project(project: Path) -> Path | None:
    cfg_file = project / "project.json"
    if cfg_file.exists():
        cfg = json.loads(cfg_file.read_text())
        name = cfg.get("char_project")
        if name:
            return SLIDES / "projects" / name
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python generate_scenes.py <project> [--provider kie|wavespeed|mmx] [--redo] [scene-id ...]")
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
    scenes_file = project / "scenes.json"

    if not scenes_file.exists():
        print(f"[ERROR] {scenes_file} not found")
        sys.exit(1)

    scenes       = json.loads(scenes_file.read_text())
    char_project = load_char_project(project)
    provider     = resolve_provider(provider_cli, project)
    client       = get_client(provider)
    print(f"[PROVIDER] {provider}")

    for scene in scenes:
        scene_id = scene["id"]
        if only and scene_id not in only:
            continue

        out_path = project / "scenes" / scene_id / "output.png"
        mode     = scene["mode"]

        # ── Reuse ──────────────────────────────────────────────────────────
        if mode == "reuse":
            source_id            = scene.get("source", scene_id)
            source_project_name  = scene.get("source_project")
            source_project       = SLIDES / "projects" / source_project_name if source_project_name else project
            source_path          = source_project / "scenes" / source_id / "output.png"
            if source_path.exists():
                out_path.parent.mkdir(parents=True, exist_ok=True)
                backup_existing(out_path, project, scene_id)
                shutil.copy2(source_path, out_path)
                print(f"[REUSE] {scene_id} ← {source_id}")
            else:
                print(f"[SKIP]  {scene_id} — reuse source not found: {source_id}")
            continue

        # ── Composite (PIL only) ────────────────────────────────────────────
        if mode == "composite":
            if out_path.exists() and not redo:
                print(f"[SKIP] {scene_id} — already exists (use --redo to regenerate)")
                continue
            out_path.parent.mkdir(parents=True, exist_ok=True)
            backup_existing(out_path, project, scene_id)
            build_composite(scene, out_path)
            continue

        # ── API-based modes ─────────────────────────────────────────────────
        if out_path.exists() and not redo:
            print(f"[SKIP] {scene_id} — already exists (use --redo to regenerate)")
            continue

        backup_existing(out_path, project, scene_id)

        model      = scene.get("model", "nano-banana-pro")
        resolution = scene.get("resolution", "2k")
        images     = resolve_images(scene, project, char_project)

        if mode == "edit-fast" and resolution == "1k":
            resolution = "2k"

        print(f"[GEN]  {scene_id}  mode={mode}  model={model}  res={resolution}  refs={len(images)}")
        url = client.generate(
            prompt=scene["prompt"],
            mode=mode,
            model=model,
            images=images if images else None,
            aspect_ratio="16:9",
            resolution=resolution,
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        client.download(url, out_path)
        print(f"[DONE] {scene_id} → {out_path}  (cost so far: ${client.total_cost:.3f})")

        # ── PIL post-processing ─────────────────────────────────────────────
        if "pip" in scene:
            apply_pip(out_path, scene["pip"], project)
        for pip_cfg in scene.get("pips", []):
            apply_pip(out_path, pip_cfg, project)

        if "overlay" in scene:
            apply_overlay(out_path, scene["overlay"])

    print(f"\nTotal cost this run: ${client.total_cost:.3f}")


if __name__ == "__main__":
    main()
