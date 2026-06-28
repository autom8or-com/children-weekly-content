"""Native python-pptx renderer for the storybook lesson deck.

Produces EDITABLE PowerPoint text (real text boxes) + the illustration placed as
a picture — so the deck can be edited in PowerPoint / Canva afterward. Reuses the
palette + schema from deck_html.py; the look is close to the Claude Design mock
(exact palette/layout/fonts; cards have uniform corners and no divider bar).

Fonts Caveat + Patrick Hand must be installed on whatever machine opens the file.
"""
import hashlib
import tempfile
from pathlib import Path

from PIL import Image
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

from deck_html import PALETTES, BG_CREAM, BG_DARK, TEXT_DARK, TEXT_BROWN

FONT_HEAD = "Caveat"
FONT_LABEL = "Patrick Hand"
IN_PER_PX = 13.33 / 1920

# the illustration only displays at ~1200px on the 1920px stage, so embedding the
# full 2K source bloats the .pptx (~5MB each). Downscale + recompress on the way in;
# originals are left untouched (collections still uses full-res).
IMG_MAX_W = 1600
IMG_QUALITY = 88
_IMG_CACHE = Path(tempfile.mkdtemp(prefix="deck-img-"))


def compress_image(path):
    """Return a downscaled, recompressed copy of `path` (cached by content+mtime)."""
    src = Path(path)
    try:
        mtime = src.stat().st_mtime
    except OSError:
        return path
    key = hashlib.md5(f"{src}|{mtime}|{IMG_MAX_W}|{IMG_QUALITY}".encode()).hexdigest()[:16]
    out = _IMG_CACHE / f"{key}.jpg"
    if out.exists():
        return out
    try:
        im = Image.open(src).convert("RGB")
    except Exception:
        return path  # unreadable — fall back to the original
    if im.width > IMG_MAX_W:
        im = im.resize((IMG_MAX_W, round(im.height * IMG_MAX_W / im.width)), Image.LANCZOS)
    im.save(out, "JPEG", quality=IMG_QUALITY, optimize=True)
    return out

# card geometry (px on the 1920x1080 stage)
CARD_X, TOP, CARD_W, CARD_H = 90, 202.5, 480, 675
PAD_X, PAD_Y = 48, 40
IMG_X, IMG_W = 630, 1200
TN_BAND, TN_GAP = 150, 16   # teacher's-note band height + gap above it


def px(n):
    return Inches(n * IN_PER_PX)


def C(hex6):
    return RGBColor.from_string(hex6)


def _bg(slide, hex6):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = C(hex6)


def _ring(slide, inset_px, width_px, hex6):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, px(inset_px), px(inset_px),
                                 px(1920 - 2 * inset_px), px(1080 - 2 * inset_px))
    shp.fill.background()
    shp.line.color.rgb = C(hex6)
    shp.line.width = px(width_px)
    shp.shadow.inherit = False


def _rect(slide, x, y, w, h, hex6, rounded=False):
    shape = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shape, px(x), px(y), px(w), px(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = C(hex6)
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _runs(paragraph, text, *, font, size, color, bold):
    """Add runs to a paragraph, turning **bold** segments bold."""
    for i, seg in enumerate(text.split("**")):
        if seg == "":
            continue
        run = paragraph.add_run()
        run.text = seg
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold or (i % 2 == 1)
        run.font.color.rgb = C(color)


def _textbox(slide, x, y, w, h, lines, *, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    first = True
    for ln in lines:
        for sub in str(ln["text"]).split("\n"):
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.alignment = align
            p.space_after = Pt(ln.get("space_after", 10))
            p.line_spacing = ln.get("line_spacing", 1.1)
            _runs(p, sub, font=ln.get("font", FONT_HEAD), size=ln["size"],
                  color=ln["color"], bold=ln.get("bold", False))
    return tb


def render_bookend(prs, *, bg, frame, lines):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, bg)
    if frame:
        _ring(slide, 18, 16, frame)
        _ring(slide, 46, 5, frame)
    _textbox(slide, 160, 0, 1600, 1080, lines, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return slide


def render_card(prs, *, sec_bg, card_bg, accent, chip, chip_font, chip_col,
                title, body_lines, footer, footer_col, image_path, stripe=None,
                teacher_note=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(slide, sec_bg)

    # a teacher's note shortens the card+image so the note strip fits underneath
    card_h = CARD_H - (TN_BAND + TN_GAP) if teacher_note else CARD_H

    # illustration (right)
    if image_path:
        slide.shapes.add_picture(str(compress_image(image_path)), px(IMG_X), px(TOP), px(IMG_W), px(card_h))
    else:
        _rect(slide, IMG_X, TOP, IMG_W, card_h, "D8C9A8", rounded=True)

    # card (left)
    _rect(slide, CARD_X, TOP, CARD_W, card_h, card_bg, rounded=True)
    if stripe:
        _rect(slide, CARD_X, TOP, 8, card_h, stripe)

    cx, cw = CARD_X + PAD_X, CARD_W - 2 * PAD_X
    # chip + title + body flow from the top
    head = [{"text": chip, "font": chip_font, "size": 22 if chip_font == FONT_LABEL else 26, "color": chip_col, "space_after": 14},
            {"text": title, "size": 50, "color": TEXT_DARK, "bold": True, "space_after": 18, "line_spacing": 1.0}]
    head += body_lines
    _textbox(slide, cx, TOP + PAD_Y, cw, card_h - 2 * PAD_Y - 60, head)
    # footer / prompt pinned near the bottom of the card
    if footer:
        _textbox(slide, cx, TOP + card_h - PAD_Y - 50, cw, 50,
                 [{"text": footer, "size": 22, "color": footer_col, "space_after": 0}])

    # teacher's note — full-width band under the card+image (teacher-facing layer)
    if teacher_note:
        ty = TOP + card_h + TN_GAP
        tw = (IMG_X + IMG_W) - CARD_X
        _rect(slide, CARD_X, ty, tw, TN_BAND, "ECE3F8", rounded=True)
        _rect(slide, CARD_X, ty, 8, TN_BAND, "7B4DB5")
        _textbox(slide, CARD_X + 28, ty + 16, tw - 56, TN_BAND - 28,
                 [{"text": "\U0001F4DD  Teacher's Note", "font": FONT_LABEL, "size": 20, "color": "7B4DB5", "space_after": 6},
                  {"text": teacher_note, "size": 19, "color": TEXT_DARK, "space_after": 0, "line_spacing": 1.1}])
    return slide


def _body_lines(body):
    return [{"text": p["text"], "size": 26, "color": (TEXT_BROWN if p.get("strong") else TEXT_DARK),
             "space_after": 12, "line_spacing": 1.25} for p in body]


def _bullet_lines(bullets):
    return [{"text": f'{b.get("emoji","•")}  {b["text"]}', "size": 26, "color": TEXT_DARK,
             "space_after": 14, "line_spacing": 1.2} for b in bullets]


def render_slide(prs, s, resolve_image):
    """Render one typed slide dict natively. `s['image']` is a scene id or None."""
    t = s.get("type")
    image = None
    if s.get("image"):
        image = resolve_image(s["image"])

    if t in ("title", "goodbye"):
        dark = (t == "goodbye")
        bg = BG_DARK if dark else BG_CREAM
        title_col = "FDF6E3" if dark else TEXT_DARK
        lines = [{"text": s["eyebrow"], "font": FONT_LABEL, "size": 28, "color": "C97B3A", "space_after": 28}]
        lines.append({"text": s["title"], "size": 120, "color": title_col, "bold": True, "space_after": 24, "line_spacing": 0.95})
        if s.get("subtitle"):
            lines.append({"text": s["subtitle"], "size": 50, "color": ("EDD9A3" if dark else TEXT_BROWN), "space_after": 24})
        if s.get("footer"):
            lines.append({"text": s["footer"], "font": FONT_LABEL, "size": 28, "color": "A0856A", "space_after": 0})
        return render_bookend(prs, bg=bg, frame="C97B3A", lines=lines)

    if t == "section-header":
        pal = PALETTES.get(s["palette"], PALETTES["preamble"])
        lines = [
            {"text": s["eyebrow"], "font": FONT_LABEL, "size": 32, "color": pal["hdr_text"], "space_after": 24},
            {"text": s["title"], "size": 140, "color": pal["hdr_title"], "bold": True, "space_after": 24, "line_spacing": 0.9},
            {"text": s["footer"], "size": 50, "color": pal["hdr_text"], "space_after": 0},
        ]
        return render_bookend(prs, bg=pal["hdr_bg"], frame=None, lines=lines)

    if t == "verse":
        lines = [
            {"text": s["eyebrow"], "font": FONT_LABEL, "size": 28, "color": "C97B3A", "space_after": 36},
            {"text": s["title"], "size": 76, "color": "FDF6E3", "bold": True, "space_after": 36, "line_spacing": 1.2},
            {"text": s["reference"], "font": FONT_LABEL, "size": 40, "color": "EDD9A3", "space_after": 0},
        ]
        return render_bookend(prs, bg=BG_DARK, frame="C97B3A", lines=lines)

    if t == "prayer":
        lines = [
            {"text": s["eyebrow"], "font": FONT_LABEL, "size": 28, "color": "C97B3A", "space_after": 36},
            {"text": s["title"], "size": 60, "color": TEXT_DARK, "bold": False, "space_after": 36, "line_spacing": 1.25},
        ]
        if s.get("footer"):
            lines.append({"text": s["footer"], "font": FONT_LABEL, "size": 32, "color": TEXT_BROWN, "space_after": 0})
        return render_bookend(prs, bg=BG_CREAM, frame="EDD9A3", lines=lines)

    if t == "story-card":
        pal = PALETTES.get(s["palette"], PALETTES["flies"])
        return render_card(prs, sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
                           chip=s["chip"], chip_font=FONT_LABEL, chip_col=pal["accent"],
                           title=s["title"], body_lines=_body_lines(s.get("body", [])),
                           footer=s.get("prompt", ""), footer_col=TEXT_BROWN, image_path=image)

    if t == "diary-card":
        pal = PALETTES["diary"]
        return render_card(prs, sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
                           chip=s["chip"], chip_font=FONT_HEAD, chip_col="7B4DB5",
                           title=s["title"], body_lines=_body_lines(s.get("body", [])),
                           footer=s.get("signature", ""), footer_col="7B4DB5",
                           image_path=image, stripe=pal["accent"],
                           teacher_note=s.get("teacher_note"))

    if t == "summary":
        pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
        return render_card(prs, sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
                           chip=s["chip"], chip_font=FONT_LABEL, chip_col=pal["accent"],
                           title=s["title"], body_lines=_bullet_lines(s.get("bullets", [])),
                           footer=s.get("prompt", ""), footer_col=TEXT_BROWN, image_path=image)

    raise ValueError(f"unknown slide type: {t!r}")
