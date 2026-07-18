"""Flatten the Pre-K storybook lesson-deck design into standalone per-slide HTML.

Each slide is one self-contained 1920x1080 HTML document (fonts via Google Fonts,
images inlined as base64 data URIs) faithful to the Claude Design mock. The deck
is composed in slides.json as a list of typed slide dicts; build_pptx.py resolves
each slide's `image` to an absolute path, then calls render_slide_html(slide).

Slide types and fields:
  title         {eyebrow, title, subtitle?, footer?}
  goodbye       {eyebrow, title, subtitle?, footer?}
  section-header{palette, eyebrow, title, footer}
  verse         {eyebrow, title, reference}
  prayer        {eyebrow, title, footer?}
  story-card    {palette, chip, title, body:[{text, strong?}], prompt?, image?}
  diary-card    {chip, title, body:[{text, strong?}], teacher_note?, signature, image?}
  summary       {palette, chip, title, bullets:[{emoji, text}], prompt?, image?}

`palette` is one of: preamble | flies | livestock | boils | diary.
Inline emphasis in any text: wrap in **double asterisks** -> bold.
"""
import html
import re
import base64
import datetime
import mimetypes
from pathlib import Path

# default A-B-C of salvation for the application slide; a project may override `steps`.
# Shared with deck_render.py (native) so both renderers stay in lockstep.
ABC_STEPS = [
    {"letter": "A", "text": "Acknowledge your sins"},
    {"letter": "B", "text": "Believe Christ died for you"},
    {"letter": "C", "text": "Confess your sins to Him"},
]


def resolve_date(val):
    """`date: "auto"` → today (e.g. "28th June 2026"); anything else passes through."""
    if str(val).lower() != "auto":
        return str(val)
    d = datetime.date.today()
    suf = "th" if 11 <= d.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d.day % 10, "th")
    return f"{d.day}{suf} {d.strftime('%B %Y')}"

PALETTES = {
    "preamble":  {"card": "F5E6C8", "accent": "C97B3A", "sec_bg": "FDF6E3", "hdr_bg": "C97B3A", "hdr_title": "3D2B1F", "hdr_text": "FDF6E3"},
    "flies":     {"card": "FDF0C0", "accent": "D4A817", "sec_bg": "FDF6E3", "hdr_bg": "D4A847", "hdr_title": "3D2B1F", "hdr_text": "6B4400"},
    "livestock": {"card": "E8F0D8", "accent": "6B8C3A", "sec_bg": "FDF6E3", "hdr_bg": "7DAF5A", "hdr_title": "1A3800", "hdr_text": "1E4200"},
    "boils":     {"card": "F5E0D0", "accent": "B5451B", "sec_bg": "FDF6E3", "hdr_bg": "B85A40", "hdr_title": "FDF6E3", "hdr_text": "FFD6C8"},
    "diary":     {"card": "FFFCE0", "accent": "C4ADE8", "sec_bg": "F5F0FF", "hdr_bg": "C4ADE8", "hdr_title": "2A1060", "hdr_text": "3A1870"},
}
BG_CREAM = "FDF6E3"
BG_DARK = "3D2B1F"
TEXT_DARK = "3D2B1F"
TEXT_BROWN = "8B4513"

HEAD = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&family=Patrick+Hand&display=swap" rel="stylesheet">
<style>*{margin:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden}
.cav{font-family:'Caveat',cursive}.ph{font-family:'Patrick Hand',cursive}</style></head><body>"""
FOOT = "</body></html>"


def fmt(text):
    """Escape, then **bold** -> <strong>, and newlines -> <br>."""
    s = html.escape(str(text))
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s.replace("\n", "<br>")


def img_data_uri(path):
    """Absolute local file path -> base64 data URI; missing/None -> ''."""
    if path and Path(path).exists():
        mime = mimetypes.guess_type(str(path))[0] or "image/png"
        data = base64.b64encode(Path(path).read_bytes()).decode()
        return f"data:{mime};base64,{data}"
    return ""


def _doc(inner):
    return HEAD + inner + FOOT


def _bookend(bg, frame, lines, image=None):
    """Centered full-bleed text slide. `lines` is a list of dicts:
    text line: {text, cls('cav'|'ph'), size, color, weight?, mb?, upper?, ls?}
    divider:   {divider: width_px, color, mb?}
    An optional `image` (abs path) renders centered beneath the text.
    """
    shadow = (f"box-shadow:inset 0 0 0 18px #{frame}, inset 0 0 0 32px #{bg}, inset 0 0 0 48px #{frame};"
              if frame else "")
    parts = [f'<section style="width:1920px;height:1080px;background:#{bg};display:flex;'
             f'align-items:center;justify-content:center;{shadow}">'
             '<div style="text-align:center;max-width:1500px;padding:60px;">']
    for ln in lines:
        if "divider" in ln:
            parts.append(f'<div style="width:{ln["divider"]}px;height:5px;background:#{ln["color"]};'
                         f'margin:0 auto {ln.get("mb",28)}px auto;"></div>')
            continue
        style = (f'font-size:{ln["size"]}px;color:#{ln["color"]};'
                 f'font-weight:{ln.get("weight",400)};line-height:1.1;'
                 f'margin-bottom:{ln.get("mb",24)}px;')
        if ln.get("upper"):
            style += "text-transform:uppercase;"
        if ln.get("ls"):
            style += f"letter-spacing:{ln['ls']}px;"
        parts.append(f'<div class="{ln.get("cls","cav")}" style="{style}">{fmt(ln["text"])}</div>')
    img_uri = img_data_uri(image)
    if img_uri:
        parts.append(f'<img src="{img_uri}" style="max-width:760px;max-height:430px;'
                     f'object-fit:contain;border-radius:18px;margin:18px auto 0;">')
    parts.append("</div></section>")
    return "".join(parts)


def _card(*, sec_bg, card_bg, accent, chip, chip_cls, chip_col, title, rows,
          footer, footer_col, image, stripe=None):
    """Left text card + right image slot. `rows` is pre-rendered HTML for the body."""
    stripe_css = f"border-left:8px solid #{stripe};" if stripe else ""
    chip_extra = "" if chip_cls == "cav" else "letter-spacing:2px;text-transform:uppercase;"
    img_uri = img_data_uri(image)
    img_html = (f'<img src="{img_uri}" style="width:1200px;height:675px;object-fit:cover;border-radius:20px;">'
                if img_uri else
                '<div style="width:1200px;height:675px;background:#D8C9A8;border-radius:20px;"></div>')
    return (
        f'<section style="width:1920px;height:1080px;background:#{sec_bg};display:flex;'
        f'align-items:center;justify-content:center;gap:60px;padding:0 90px;">'
        f'<div style="width:480px;height:675px;background:#{card_bg};border-radius:24px 72px 72px 24px;'
        f'padding:40px 48px;display:flex;flex-direction:column;gap:18px;'
        f'box-shadow:4px 4px 24px rgba(61,43,31,.12);{stripe_css}">'
        f'<div class="{chip_cls}" style="font-size:{26 if chip_cls=="cav" else 22}px;color:#{chip_col};{chip_extra}">{fmt(chip)}</div>'
        f'<h2 class="cav" style="font-size:52px;font-weight:700;color:#{TEXT_DARK};line-height:1.1;">{fmt(title)}</h2>'
        f'<div style="width:60px;height:3px;background:#{accent};"></div>'
        f'{rows}'
        f'<div class="cav" style="font-size:22px;color:#{footer_col};margin-top:auto;">{fmt(footer)}</div>'
        f'</div>{img_html}</section>'
    )


def _paragraph_rows(body):
    out = []
    for p in body:
        col = TEXT_BROWN if p.get("strong") else TEXT_DARK
        out.append(f'<p class="cav" style="font-size:26px;color:#{col};line-height:1.6;">{fmt(p["text"])}</p>')
    return "".join(out)


def _bullet_rows(bullets):
    out = ['<div style="display:flex;flex-direction:column;gap:16px;margin-top:4px;">']
    for b in bullets:
        out.append(
            '<div style="display:flex;gap:14px;align-items:flex-start;">'
            f'<span style="font-size:28px;line-height:1.2;">{fmt(b.get("emoji","•"))}</span>'
            f'<span class="cav" style="font-size:26px;color:#{TEXT_DARK};line-height:1.5;">{fmt(b["text"])}</span>'
            '</div>')
    out.append("</div>")
    return "".join(out)


def _bookend_with_thumbs(bg, lines, thumbs):
    """A bookend (centered text) with a row of thumbnails along the bottom."""
    parts = [f'<section style="position:relative;width:1920px;height:1080px;background:#{bg};'
             f'display:flex;align-items:center;justify-content:center;">'
             '<div style="text-align:center;max-width:1500px;padding:60px 60px 200px;">']
    for ln in lines:
        if "divider" in ln:
            parts.append(f'<div style="width:{ln["divider"]}px;height:5px;background:#{ln["color"]};'
                         f'margin:0 auto {ln.get("mb",28)}px auto;"></div>')
            continue
        style = (f'font-size:{ln["size"]}px;color:#{ln["color"]};font-weight:{ln.get("weight",400)};'
                 f'line-height:1.1;margin-bottom:{ln.get("mb",24)}px;')
        if ln.get("upper"):
            style += "text-transform:uppercase;"
        if ln.get("ls"):
            style += f"letter-spacing:{ln['ls']}px;"
        parts.append(f'<div class="{ln.get("cls","cav")}" style="{style}">{fmt(ln["text"])}</div>')
    parts.append("</div>")
    thumbs_html = "".join(
        f'<img src="{img_data_uri(t)}" style="width:300px;height:200px;object-fit:cover;'
        f'border-radius:16px;margin:0 20px;">' for t in thumbs if img_data_uri(t))
    parts.append(f'<div style="position:absolute;bottom:70px;width:100%;display:flex;'
                 f'justify-content:center;">{thumbs_html}</div></section>')
    return "".join(parts)


def _rules_html(s):
    pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
    rows = []
    for r in s.get("rules", []):
        icon = img_data_uri(r.get("icon"))
        icon_html = (f'<img src="{icon}" style="width:64px;height:64px;object-fit:contain;">'
                     if icon else f'<span style="font-size:52px;">{fmt(r.get("emoji","•"))}</span>')
        rows.append(
            f'<div style="display:flex;align-items:center;gap:28px;background:#{pal["card"]};border-radius:18px;'
            f'padding:22px 36px;box-shadow:2px 3px 14px rgba(61,43,31,.10);">'
            f'<div style="width:80px;text-align:center;">{icon_html}</div>'
            f'<div class="cav" style="font-size:30px;color:#{TEXT_DARK};line-height:1.2;">{fmt(r["text"])}</div></div>')
    return _doc(
        f'<section style="width:1920px;height:1080px;background:#{pal["sec_bg"]};display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;padding:0 90px;box-sizing:border-box;gap:30px;">'
        f'<div style="text-align:center;">'
        f'<div class="ph" style="font-size:30px;color:#{pal["accent"]};text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;">{fmt(s.get("chip","Before We Begin"))}</div>'
        f'<div class="cav" style="font-size:88px;font-weight:700;color:#{pal["hdr_title"]};">{fmt(s.get("title","House Rules"))}</div></div>'
        f'<div style="display:flex;flex-direction:column;gap:22px;width:1200px;">{"".join(rows)}</div></section>')


def _outlines_html(s):
    pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
    cards = []
    for i, it in enumerate(s.get("items", []), 1):
        img = img_data_uri(it.get("image"))
        thumb = (f'<img src="{img}" style="width:360px;height:300px;object-fit:cover;border-radius:18px;">'
                 if img else f'<div style="width:360px;height:300px;background:#{pal["card"]};border-radius:18px;"></div>')
        cards.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:16px;">{thumb}'
                     f'<div class="cav" style="font-size:32px;font-weight:700;color:#{pal["hdr_title"]};text-align:center;">{i}. {fmt(it["label"])}</div></div>')
    return _doc(
        f'<section style="width:1920px;height:1080px;background:#{pal["sec_bg"]};display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;padding:0 60px;box-sizing:border-box;gap:50px;">'
        f'<div style="text-align:center;">'
        f'<div class="ph" style="font-size:30px;color:#{pal["accent"]};text-transform:uppercase;letter-spacing:3px;margin-bottom:8px;">{fmt(s.get("chip","Today&#39;s Journey"))}</div>'
        f'<div class="cav" style="font-size:84px;font-weight:700;color:#{pal["hdr_title"]};">{fmt(s.get("title","Outlines"))}</div></div>'
        f'<div style="display:flex;justify-content:center;gap:40px;">{"".join(cards)}</div></section>')


def _bible_html(s):
    body = s.get("body", [])
    cols = s.get("columns", 2 if len(body) > 1 else 1)
    paras = "".join(f'<p class="cav" style="font-size:23px;color:#{TEXT_DARK};line-height:1.5;margin-bottom:14px;">{fmt(p)}</p>' for p in body)
    col_css = "column-count:2;column-gap:60px;" if cols == 2 else ""
    return _doc(
        f'<section style="width:1920px;height:1080px;background:#{BG_CREAM};box-sizing:border-box;padding:80px 110px;'
        f'box-shadow:inset 0 0 0 18px #C97B3A;">'
        f'<div class="ph" style="font-size:30px;color:#C97B3A;text-transform:uppercase;letter-spacing:3px;margin-bottom:6px;">{fmt(s.get("eyebrow","📖 Bible Text"))}</div>'
        f'<div class="cav" style="font-size:60px;font-weight:700;color:#{TEXT_DARK};margin-bottom:30px;">{fmt(s["reference"])}</div>'
        f'<div style="{col_css}">{paras}</div></section>')


def _application_html(s):
    intro = "".join(f'<p class="cav" style="font-size:28px;color:#{TEXT_BROWN};line-height:1.3;margin-bottom:14px;">{fmt(p)}</p>' for p in s.get("intro", []))
    title_html = (f'<div class="cav" style="font-size:46px;font-weight:700;color:#{TEXT_DARK};margin-bottom:22px;line-height:1.1;">{fmt(s["title"])}</div>'
                  if s.get("title") else "")
    steps = "".join(f'<div class="cav" style="font-size:32px;font-weight:700;color:#{TEXT_DARK};margin-bottom:10px;">{st["letter"]} – {fmt(st["text"])}</div>'
                    for st in s.get("steps", ABC_STEPS))
    img = img_data_uri(s.get("image"))
    img_html = (f'<img src="{img}" style="width:520px;height:700px;object-fit:cover;border-radius:20px;">' if img else "")
    left = (f'<div style="flex:1;">{title_html}{intro}'
            f'<div class="ph" style="font-size:30px;color:#C97B3A;margin:22px 0 14px;">{fmt(s.get("steps_lead","To be rescued:"))}</div>{steps}</div>')
    return _doc(
        f'<section style="width:1920px;height:1080px;background:#{BG_CREAM};box-sizing:border-box;padding:110px 120px;'
        f'box-shadow:inset 0 0 0 18px #C97B3A;display:flex;gap:60px;align-items:center;">{left}{img_html}</section>')


def render_slide_html(s):
    """Render one typed slide dict to a standalone HTML document string.
    `s['image']` (if present) must already be an absolute path or None."""
    t = s.get("type")

    if t in ("title", "goodbye"):
        dark = (t == "goodbye")
        bg = BG_DARK if dark else BG_CREAM
        title_col = "FDF6E3" if dark else TEXT_DARK
        lines = [{"text": s["eyebrow"], "cls": "ph", "size": 28, "color": "C97B3A", "upper": True, "ls": 5, "mb": 28}]
        lines.append({"text": s["title"], "size": 128, "color": title_col, "weight": 700, "mb": 20})
        lines.append({"divider": 220, "color": "C97B3A", "mb": 28})
        if s.get("subtitle"):
            lines.append({"text": s["subtitle"], "size": 52, "color": ("EDD9A3" if dark else TEXT_BROWN), "mb": 32})
        if s.get("date"):
            lines.append({"text": resolve_date(s["date"]), "cls": "ph", "size": 36, "color": "C97B3A", "mb": 0})
        if s.get("footer"):
            lines.append({"text": s["footer"], "cls": "ph", "size": 30, "color": "A0856A", "mb": 0})
        return _doc(_bookend(bg, "C97B3A", lines, image=s.get("image")))

    if t == "topic":
        lines = [
            {"text": s.get("eyebrow", "✦ TOPIC ✦"), "cls": "ph", "size": 34, "color": "C97B3A", "upper": True, "ls": 5, "mb": 28},
            {"text": s["title"], "size": 132, "color": "FDF6E3", "weight": 700, "mb": 0},
        ]
        return _doc(_bookend(BG_DARK, "C97B3A", lines, image=s.get("image")))

    if t == "section-header":
        pal = PALETTES.get(s["palette"], PALETTES["preamble"])
        lines = [
            {"text": s["eyebrow"], "cls": "ph", "size": 32, "color": pal["hdr_text"], "upper": True, "ls": 5, "mb": 24},
            {"text": s["title"], "size": 148, "color": pal["hdr_title"], "weight": 700, "mb": 24},
            {"divider": 220, "color": pal["hdr_title"], "mb": 28},
            {"text": s["footer"], "size": 52, "color": pal["hdr_text"], "mb": 0},
        ]
        return _doc(_bookend(pal["hdr_bg"], None, lines) if not s.get("thumbs")
                    else _bookend_with_thumbs(pal["hdr_bg"], lines, s["thumbs"]))

    if t == "verse":
        lines = [
            {"text": s["eyebrow"], "cls": "ph", "size": 28, "color": "C97B3A", "upper": True, "ls": 5, "mb": 36},
            {"text": s["title"], "size": 80, "color": "FDF6E3", "weight": 700, "mb": 36},
            {"divider": 140, "color": "C97B3A", "mb": 32},
            {"text": s["reference"], "cls": "ph", "size": 42, "color": "EDD9A3", "mb": 0},
        ]
        return _doc(_bookend(BG_DARK, "C97B3A", lines, image=s.get("image")))

    if t == "prayer":
        lines = [
            {"text": s["eyebrow"], "cls": "ph", "size": 28, "color": "C97B3A", "upper": True, "ls": 4, "mb": 36},
            {"text": s["title"], "size": 64, "color": TEXT_DARK, "weight": 600, "mb": 36},
        ]
        if s.get("footer"):
            lines.append({"text": s["footer"], "cls": "ph", "size": 34, "color": TEXT_BROWN, "mb": 0})
        return _doc(_bookend(BG_CREAM, "EDD9A3", lines, image=s.get("image")))

    if t == "story-card":
        pal = PALETTES.get(s["palette"], PALETTES["flies"])
        return _doc(_card(
            sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
            chip=s["chip"], chip_cls="ph", chip_col=pal["accent"],
            title=s["title"], rows=_paragraph_rows(s.get("body", [])),
            footer=s.get("prompt", ""), footer_col=TEXT_BROWN, image=s.get("image")))

    if t == "diary-card":
        pal = PALETTES["diary"]
        return _doc(_card(
            sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
            chip=s["chip"], chip_cls="cav", chip_col="7B4DB5",
            title=s["title"], rows=_paragraph_rows(s.get("body", [])),
            footer=s.get("signature", ""), footer_col="7B4DB5",
            image=s.get("image"), stripe=pal["accent"]))

    if t == "summary":
        pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
        return _doc(_card(
            sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
            chip=s["chip"], chip_cls="ph", chip_col=pal["accent"],
            title=s["title"], rows=_bullet_rows(s.get("bullets", [])),
            footer=s.get("prompt", ""), footer_col=TEXT_BROWN, image=s.get("image")))

    if t == "objectives":
        pal = PALETTES.get(s.get("palette", "preamble"), PALETTES["preamble"])
        lead = (f'<p class="cav" style="font-size:28px;color:#{TEXT_BROWN};line-height:1.25;margin-bottom:10px;">{fmt(s["lead"])}</p>'
                if s.get("lead") else "")
        return _doc(_card(
            sec_bg=pal["sec_bg"], card_bg=pal["card"], accent=pal["accent"],
            chip=s.get("chip", "🎯 Objectives"), chip_cls="ph", chip_col=pal["accent"],
            title=s.get("title", "Objectives"), rows=lead + _bullet_rows(s.get("bullets", [])),
            footer=s.get("prompt", ""), footer_col=TEXT_BROWN, image=s.get("image")))

    if t == "house-rules":
        return _rules_html(s)

    if t == "outlines":
        return _outlines_html(s)

    if t == "bible-text":
        return _bible_html(s)

    if t == "application":
        return _application_html(s)

    raise ValueError(f"unknown slide type: {t!r}")
