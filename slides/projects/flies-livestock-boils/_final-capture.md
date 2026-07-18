<!--
STATUS (2026-06-28): IMPLEMENTED. The slide types below now exist in deck_render.py +
deck_html.py, the boilerplate is in _templates/partials/, and slides.json was rebuilt
to the 32-slide structure — the regenerated deck matches final.pptx 1:1. Kept as the
authoring reference for these types and the verbatim Bible passages.

CAPTURE of content from flies-livestock-boils-final.pptx (Odun's hand-polished deck).
Deck typos were FIXED on the way in ("your sis"→"your sins"). Carried-over text edits
were backported into slides.json (diary #2 reworded, verse → 1 Sam 15:23, goodbye → "Next Week").
-->

# Final-deck content not yet in the pipeline

## Structural changes to existing types
- **title (#01):** became a weekly boilerplate welcome with a live date —
  eyebrow "✦ Pre-K Bible Story ✦", title "Welcome to Bible Club", date line
  "28th June 2026". The story-title slide ("The Plagues of Egypt · Part 2") was
  dropped; story identity now lives in the Topic slide.
- **prayer (#02):** moved to the top as "Let Us Pray" with a decorative image
  (the verbose "Dear God, thank you for this amazing story…" body was dropped).
- **verse (#08):** now carries a decorative image alongside the text.
- **section-header (#25 diary, also outlines/objectives):** carry decorative
  images / thumbnails.
- **Dropped:** "Today's Story Comes From Exodus 8 & 9" summary; "My Prayer Tonight"
  diary card.

## New slide types + verbatim content

### house-rules (boilerplate, weekly)  — title + N rule lines, each with an icon
- Heading: **House Rules**
- SIT STILL DURING THE CLASS
- KEEP YOUR MICROPHONE MUTED UNLESS YOUR TEACHER TELLS YOU TO MUTE
- THERE SHOULD BE AN ADULT CLOSE TO YOU
- KEEP YOUR VIDEO ON AT ALL TIMES

### objectives (per-lesson)  — heading + side panels + lead-in + objective list
- Side panels: "The Plagues" · "Partial Obedience"
- Heading: **Objectives**
- Lead-in: "At the end of this lecture students will be able to understand:"
- (objective bullet list — Odun to supply per lesson)

### topic (per-lesson)  — standalone topic bookend
- Eyebrow "✦ TOPIC ✦", title "Incomplete Obedience"

### outlines (per-lesson, auto-derivable from story sections)  — agenda grid + thumbs
- The Flies · Sick Animals · The Boils · Angela's Diary

### bible-text (per-lesson)  — eyebrow + reference + long passage (1–2 columns)
- **Exodus 8:20–28** (NIV): "20 Then the Lord said to Moses, 'Get up early in the
  morning and confront Pharaoh as he goes to the river… 28 …but you must not go very
  far. Now pray for me.'"  [full passage stored in the final.pptx, slide 9]
- **Exodus 8:29–9:12** (NIV): "29 Moses answered… 9:12 …Yet his heart was unyielding
  and he would not let the people go."  [full passage, slide 10 — two columns]

### application (hybrid: per-lesson intro + boilerplate ABC)
- "You cannot worship God as a slave to sin."
- "Pharaoh was a slave to sin. Sin is smelly to God like the boils."
- "If you too must serve God and be obedient to Him, he must first deliver you from a
  powerful king like Pharaoh."
- "To be rescued:"
- **A** – Acknowledge your sins   *(deck typo "your sis" — fixed here)*
- **B** – Believe Christ died for you
- **C** – Confess your sins to Him

## Static assets to extract from final.pptx (reusable clip-art, not AI scenes)
- 4 House Rules icons (sit still / mute mic / adult nearby / video on)
- "Let Us Pray" art · diary-header decorations · application-slide art
- These need a static-asset image path (`_assets/…`), since `resolve_image`
  currently only looks under `scenes/`.
