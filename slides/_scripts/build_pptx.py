"""
Step 3: Assemble generated scene images into a PowerPoint deck.
Reads slide metadata from projects/<project>/slides.json.
Each scene produces two slides:
  1. Full-bleed image slide
  2. Plain CTA text slide (white background) — only if cta is defined

Usage:
  python build_pptx.py deliverance
  python build_pptx.py deliverance --out my_custom_name.pptx
"""
import sys
import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SLIDES_DIR = Path(__file__).parent.parent

SLIDE_W = Inches(13.33)  # 16:9 widescreen
SLIDE_H = Inches(7.5)


def add_image_slide(prs, image_path: Path, theme: str):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    slide.shapes.add_picture(str(image_path), Emu(0), Emu(0), SLIDE_W, SLIDE_H)
    # Small theme label bottom-left
    tb = slide.shapes.add_textbox(Inches(0.3), Inches(6.8), Inches(8), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = theme
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)


def add_cta_slide(prs, cta_text: str, theme: str):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Theme label top centre
    tb_top = slide.shapes.add_textbox(Inches(0), Inches(0.4), SLIDE_W, Inches(0.6))
    p_top = tb_top.text_frame.paragraphs[0]
    p_top.text = theme
    p_top.alignment = PP_ALIGN.CENTER
    p_top.font.size = Pt(18)
    p_top.font.bold = True
    p_top.font.color.rgb = RGBColor(100, 100, 100)

    # CTA text centred
    tb = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.33), Inches(5))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(cta_text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(30, 30, 30)


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python build_pptx.py <project> [--out filename.pptx]")
        sys.exit(1)

    project_name = args[0]
    out_name = project_name + ".pptx"
    if "--out" in args:
        out_name = args[args.index("--out") + 1]

    project = SLIDES_DIR / "projects" / project_name
    slides_file = project / "slides.json"

    if not slides_file.exists():
        print(f"[ERROR] {slides_file} not found")
        sys.exit(1)

    slides_meta = json.loads(slides_file.read_text())

    # Load scenes.json to resolve reuse/skip modes
    scenes_file = project / "scenes.json"
    scenes_by_id = {}
    if scenes_file.exists():
        for s in json.loads(scenes_file.read_text()):
            scenes_by_id[s["id"]] = s

    def resolve_image(slide_id: str) -> Path | None:
        scene = scenes_by_id.get(slide_id, {})
        mode  = scene.get("mode", "")

        # Reuse — point at another scene's output
        if mode == "reuse":
            source_id           = scene.get("source", "")
            source_project_name = scene.get("source_project")
            src_project         = SLIDES_DIR / "projects" / source_project_name if source_project_name else project
            for fname in ("output.png", "draft.png"):
                p = src_project / "scenes" / source_id / fname
                if p.exists():
                    return p
            return None

        # Normal — output.png preferred, draft.png fallback
        for fname in ("output.png", "draft.png"):
            p = project / "scenes" / slide_id / fname
            if p.exists():
                return p
        return None

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    missing = []
    for slide in slides_meta:
        img_path = resolve_image(slide["id"])
        if img_path is None:
            print(f"[MISSING] {slide['id']} — no image found, skipping")
            missing.append(slide["id"])
            continue

        suffix = " (draft)" if img_path.name == "draft.png" else ""
        print(f"[SLIDE]  {slide['id']}{suffix} → {img_path.name}")
        add_image_slide(prs, img_path, slide.get("theme", ""))
        if slide.get("cta"):
            add_cta_slide(prs, slide["cta"], slide.get("theme", ""))

    out_path = project / "output" / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    print(f"[SAVED] {out_path}")
    if missing:
        print(f"[WARN]  {len(missing)} scene(s) missing — run generate_scenes.py first")


if __name__ == "__main__":
    main()
