<!--
LESSON BRIEF TEMPLATE — the single intake "request" for one storybook lesson deck.

HOW TO USE
  1. Copy this file to slides/projects/<slug>/brief.md and fill the blanks
     (or paste a rough version to Claude and let it expand the gaps).
  2. Claude turns the brief into the four pipeline files:
       project.json · scenes.json · slides.json · lesson-notes.md
  3. Claude shows the approval gate (scene + character + cost tables); you say go.
  4. generate_characters.py → generate_scenes.py → build_pptx.py → .pptx

This brief is story-agnostic: the SECTIONS and SLIDE TYPES are generic storybook
building blocks, so the same shape works for any Bible story — only the prose
in §2 (Lesson) and §5 (Story beats) changes.

Leave a field blank if it doesn't apply. Lines starting with "#" inside a field
are just hints — delete them.

GUARDRAIL: resolve every "OPEN DECISION" in the brief BEFORE authoring slides.json.
An unresolved decision left in the brief gets silently resolved by whoever builds —
usually wrong. build_pptx.py prints a [GUARD] warning if "OPEN DECISION" survives.
-->

# Lesson Brief — <Title>

## 1. Identity
- slug:             <folder-name, kebab-case>
- series / part:    <e.g. The Plagues of Egypt · Part 3>
- passage:          <book chapter:verse (translation)>
- sunday / date:    <YYYY-MM-DD>
- audience / tone:  <e.g. Pre-K storybook; gentle, no gore>

## 2. Lesson (the teaching spine)
- theme (one line):     <the single idea this week, e.g. Incomplete obedience>
- memory verse:         <"verse text" — Reference>
- big questions:        # 2-3 kid-level questions the lesson answers
    - <question 1>
    - <question 2>
- angela study title:   <Angela's diary headline, e.g. Sneaky Pharaoh>
- teaching points:      # one block per point Angela will document
    - point:         <short label>
      teacher_note:  <the deeper why, for the teacher>
      angela_line:   "<the simple kid-level line>"
      scripture:     <Book ch:vv>
      pull_slide:    <leave blank — filled once the deck is built>
    # - point: …  (repeat as needed)

## 3. Cast
# id : new | reuse ← <project> | copy ← <project> | inline (no ref sheet)
- <char-id> : <source>            # e.g. moses-b : reuse ← character-variants
- <char-id> : <source>
- <crowd/extras> : inline

## 4. Continuity
- base projects:    <prior projects whose rendered output.png to anchor scenes to>
# Anchor edits to a prior deck's output.png (not ref sheets); never reposition a
# character in a cross-edit (forces a redraw + appearance drift).

## 5. Story beats  (ordered → become illustrations + story slides)
# One line per narrative moment. Keep illustrations CLEAN scene art — the words
# live on the slide's text card, NOT baked into the image (no speech bubbles).
- 1: <beat>
- 2: <beat>
- 3: <beat>

## 6. Deck sections  (include / drop; order runs top → bottom)
- preamble:   [ title, scripture, last-week-recap, learning-goals, memory-verse, prayer ]
- per-story:  header + story-cards            # auto-built from §5 beats
- angela:     [ header, ONE diary-card per §2 teaching point, closing prayer ]
- wrap:       [ summary, goodbye ]
# DIARY RULE: the diary is defined ONCE — in §2 teaching points. Each teaching
# point becomes exactly one diary-card whose body + teacher_note are TRANSCRIBED
# from §2 (and lesson-notes.md), never invented during slides.json authoring. Do
# not restate a competing diary card-list here. Pull each card's picture from an
# existing story scene (§2 pull_slide), not a bespoke portrait, unless §2 says so.
# Slide types available: title · section-header · story-card · verse · prayer ·
# diary-card · summary · goodbye.  Palettes: preamble | flies | livestock | boils | diary

## 7. Constraints
- scene budget:     <approx # of illustrations>
- cost ceiling:     <$ — sanity bound for the approval gate>
- provider:         <kie.ai (default) | wavespeed>
- sensitivities:    <child-safe notes, e.g. injuries = gentle, no gore>

## 8. Delivery
- format:           .pptx (+ collections.zip)
- destination:      slides/projects/<slug>/output/
- deadline:         <when it's needed>

<!--
FIELD → PIPELINE MAPPING (what each section produces)
  §1, §3, §4         → project.json + plan.md header
  §5 + §3/§4         → scenes.json   (illustration manifest)
  §6 + §2 + §5       → slides.json   (typed deck: title/verse/story-card/diary-card/…)
  §2 (theme, points) → lesson-notes.md (your Angela's corner) + verse/recap/goals/summary text
  §7                 → the approval-gate cost table
-->
