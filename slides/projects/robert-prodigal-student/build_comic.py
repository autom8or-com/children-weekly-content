"""Stitch 4 Robert-the-Prodigal-Student panels into a 4-panel wide comic strip."""
from pathlib import Path
from PIL import Image, ImageDraw

PROJECT = Path(__file__).parent
PANELS_DIR = PROJECT / "scenes"
OUT_PATH = PANELS_DIR / "scene-3" / "3a" / "output.png"

panel_files = [
    PANELS_DIR / "scene-1" / "1a" / "output.png",
    PANELS_DIR / "scene-1" / "1b" / "output.png",
    PANELS_DIR / "scene-2" / "2a" / "output.png",
    PANELS_DIR / "scene-2" / "2b" / "output.png",
]

# Open and normalise to the same height (they're all 2752x1536 already)
images = [Image.open(p).convert("RGB") for p in panel_files]
ref_w, ref_h = images[0].size
images = [img.resize((ref_w, ref_h), Image.LANCZOS) for img in images]

# Thin black gutter between panels
gutter = 12  # px
total_w = ref_w * len(images) + gutter * (len(images) - 1)
total_h = ref_h

canvas = Image.new("RGB", (total_w, total_h), (255, 255, 255))
draw = ImageDraw.Draw(canvas)
for i, img in enumerate(images):
    x = i * (ref_w + gutter)
    canvas.paste(img, (x, 0))
    if i < len(images) - 1:
        draw.rectangle(
            [x + ref_w, 0, x + ref_w + gutter - 1, total_h - 1],
            fill=(0, 0, 0),
        )

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUT_PATH, "PNG", optimize=True)
print(f"comic saved: {OUT_PATH}")
print(f"size: {canvas.size}")
