"""Standalone builder for the once-a-term REVISION deck.

The revision format (Pre-K "Who is this? / What plague is this?" flip-card quiz)
is intentionally NOT wired into the core lesson-deck engine (deck_render.py /
deck_html.py / build_pptx.py). It is a rare deliverable, so instead of leaving a
`qa-answer` slide type in the shared renderers forever (and keeping the native +
screenshot renderers in lockstep for it), this script *imports* the visual
primitives from deck_render and defines only the one new thing it needs:
`render_qa_answer` (the big-box answer reveal). Native / editable output only.

Schema (slides/projects/revision/slides.json is a list of typed dicts):
  title         {eyebrow, title, subtitle?, footer?}          -> reuses render_title_goodbye
  goodbye       {eyebrow, title, subtitle?, footer?}          -> reuses render_title_goodbye
  section       {palette, eyebrow, title, footer}             -> reuses render_section_header
  qa-question   {palette, question, hint?, prompt?, image}    -> reuses render_card (two-box)
  qa-answer     {palette, chip?, answer, lesson?}             -> render_qa_answer (this file)
  diary-list    {title, lead?, items:[{emoji, story, lesson}]}-> render_diary_list (this file)

`image` is a path relative to slides/ (e.g. projects/passover/scenes/scene-1/1c/output.png).

Run:  python3 slides/_scripts/build_revision.py [--out Revision.pptx]
"""
import argparse
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

import deck_render as dr
from deck_render import (
    render_title_goodbye, render_section_header, render_card,
    render_prayer, render_house_rules,
    _rect, _bg, _textbox, PALETTES, TEXT_DARK, TEXT_BROWN,
    FONT_LABEL, IN_PER_PX,
)

SLIDES_DIR = Path(__file__).resolve().parent.parent          # .../slides
PROJECT = SLIDES_DIR / "projects" / "revision"
PARTIALS = SLIDES_DIR / "_templates" / "partials"
SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)


def resolve_image(ref):
    """slides.json image ref (path relative to slides/) -> absolute path str or None."""
    if not ref:
        return None
    p = (SLIDES_DIR / ref).resolve()
    return str(p) if p.exists() else None


# ─────────────────────────── new: the answer reveal ───────────────────────────

def render_qa_answer(prs, s):
    """Big-box answer reveal — one large card, '✅ ANSWER' chip, huge answer word,
    optional one-line Pre-K lesson. Distinct from the two-box question slide."""
    pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, pal["sec_bg"])

    cx, cy, cw, ch = 170, 150, 1580, 780
    _rect(slide, cx, cy, cw, ch, pal["card"], rounded=True)
    _rect(slide, cx, cy, cw, 14, pal["accent"], rounded=True)   # accent cap stripe

    lines = [
        {"text": s.get("chip", "✅ ANSWER"), "font": FONT_LABEL, "size": 40,
         "color": pal["accent"], "space_after": 22, "line_spacing": 1.0},
        {"text": s["answer"], "size": 120, "color": TEXT_DARK, "bold": True,
         "space_after": 18, "line_spacing": 0.95},
    ]
    if s.get("lesson"):
        lines.append({"text": "▬▬▬", "font": FONT_LABEL, "size": 20,
                      "color": pal["accent"], "space_after": 18, "line_spacing": 1.0})
        lines.append({"text": s["lesson"], "size": 48, "color": TEXT_BROWN,
                      "space_after": 0, "line_spacing": 1.05})
    _textbox(slide, (cx + 70) * IN_PER_PX, cy * IN_PER_PX, (cw - 140) * IN_PER_PX,
             ch * IN_PER_PX, lines, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
             auto_fit_shrink=True)
    return slide


def render_diary_list(prs, s):
    """Angela's-Diary roundup — one lesson per story, stacked rows (diary palette)."""
    pal = PALETTES["diary"]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, pal["sec_bg"])

    head = [
        {"text": s.get("chip", "📔 Angela's Diary"), "font": FONT_LABEL, "size": 32,
         "color": pal["accent"], "space_after": 14, "line_spacing": 1.0},
        {"text": s.get("title", "What We Learned"), "size": 60, "color": pal["hdr_title"],
         "bold": True, "space_after": 0, "line_spacing": 1.0},
    ]
    _textbox(slide, 200 * IN_PER_PX, 60 * IN_PER_PX, 1520 * IN_PER_PX, 210 * IN_PER_PX,
             head, align=PP_ALIGN.CENTER, auto_fit_shrink=False)

    items = s.get("items", [])
    n = len(items)
    if n == 0:
        return slide
    row_h, gap, y0 = 116, 18, 360
    for i, it in enumerate(items):
        ry = y0 + i * (row_h + gap)
        _rect(slide, 260, ry, 1400, row_h, pal["card"], rounded=True)
        _rect(slide, 260, ry, 10, row_h, pal["accent"])
        _textbox(slide, 300 * IN_PER_PX, (ry + 20) * IN_PER_PX, 110 * IN_PER_PX,
                 (row_h - 40) * IN_PER_PX,
                 [{"text": it.get("emoji", "•"), "size": 48, "color": TEXT_DARK,
                   "space_after": 0}], align=PP_ALIGN.CENTER, auto_fit_shrink=False)
        _textbox(slide, 430 * IN_PER_PX, (ry + 18) * IN_PER_PX, 1200 * IN_PER_PX,
                 (row_h - 34) * IN_PER_PX,
                 [{"text": f"**{it['story']}** — {it['lesson']}", "size": 30,
                   "color": TEXT_DARK, "space_after": 0, "line_spacing": 1.15}],
                 anchor=MSO_ANCHOR.MIDDLE, auto_fit_shrink=True)
    return slide


# ─────────────────────────── dispatch + build ───────────────────────────

def expand_includes(slides):
    """Replace {"include": "welcome"} with slides/_templates/partials/welcome.json.
    Extra keys on the include dict override the partial's fields."""
    out = []
    for s in slides:
        if isinstance(s, dict) and "include" in s:
            partial = json.loads((PARTIALS / f"{s['include']}.json").read_text())
            overrides = {k: v for k, v in s.items() if k != "include"}
            partial.update(overrides)
            out.append(partial)
        else:
            out.append(s)
    return out


def render(prs, s):
    t = s.get("type")
    if t == "title":
        return render_title_goodbye(prs, s, is_goodbye=False)
    if t == "goodbye":
        return render_title_goodbye(prs, s, is_goodbye=True)
    if t == "section":
        return render_section_header(prs, s)
    if t == "prayer":
        return render_prayer(prs, s, resolve_image(s.get("image")))
    if t == "house-rules":
        return render_house_rules(prs, s)
    if t == "qa-question":
        pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
        body = []
        if s.get("hint"):
            body.append({"text": s["hint"], "size": 30, "color": TEXT_BROWN,
                         "space_after": 4, "line_spacing": 1.25})
        return render_card(
            prs, sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
            chip=s.get("chip", "❓ QUESTION"), chip_font=FONT_LABEL, chip_col=pal["accent"],
            title=s["question"], body_lines=body, footer=s.get("prompt", "🤔 Can you guess?"),
            footer_col=TEXT_BROWN, image_path=resolve_image(s.get("image")),
            body_size=30, chip_size=22, title_size=56)
    if t == "qa-answer":
        return render_qa_answer(prs, s)
    if t == "diary-list":
        return render_diary_list(prs, s)
    raise ValueError(f"unknown revision slide type: {t!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="Revision.pptx")
    args = ap.parse_args()

    slides = expand_includes(json.loads((PROJECT / "slides.json").read_text()))
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    missing = []
    for s in slides:
        if s.get("type") == "qa-question" and not resolve_image(s.get("image")):
            missing.append(s.get("image"))
        render(prs, s)
    if missing:
        print("[WARN] missing images (rendered as placeholder blocks):")
        for m in missing:
            print("   ", m)

    out = PROJECT / args.out
    prs.save(str(out))
    print(f"✅ {len(slides)} slides -> {out}")


if __name__ == "__main__":
    main()
