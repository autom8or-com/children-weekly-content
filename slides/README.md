# Slides Image Generation System

Automated storybook illustration pipeline using WaveSpeed AI (Nano Banana).
Fully reusable — each new topic is a new project folder with three JSON files.

---

## Folder Structure

```
slides/
├── _lib/
│   └── wavespeed.py               # WaveSpeed API client
├── _scripts/
│   ├── generate_characters.py     # Step 1: Generate character reference sheets
│   ├── generate_scenes.py         # Step 2: Generate scene images
│   └── build_pptx.py              # Step 3: Assemble PPTX deck
├── _templates/
│   ├── character-prompt.md        # Guide for writing character prompts
│   └── scene-prompt.md            # Guide for writing scene prompts
└── projects/
    └── <project-name>/
        ├── plan.md                # Human-readable story plan (reference)
        ├── characters.json        # Character definitions → drives Step 1
        ├── scenes.json            # Scene prompts & modes → drives Step 2
        ├── slides.json            # Slide order, themes, CTAs → drives Step 3
        ├── prompts.md             # Full prompt document (human review copy)
        ├── characters/
        │   └── <id>/reference.png # Generated character reference images
        ├── scenes/
        │   └── scene-N/Na/
        │       └── output.png     # Generated scene images
        └── output/
            └── <project>.pptx    # Final assembled deck
```

---

## How to Run (Any Project)

```bash
# Step 1 — Generate character reference sheets (once per project)
python slides/_scripts/generate_characters.py <project>

# Step 2 — Generate all scene images (always 2K)
python slides/_scripts/generate_scenes.py <project>

# Step 3 — Assemble PPTX
python slides/_scripts/build_pptx.py <project>
```

### Useful flags

```bash
# Regenerate one specific scene (e.g. after tweaking its prompt)
python slides/_scripts/generate_scenes.py <project> --redo scene-3/3c

# Generate specific scenes only
python slides/_scripts/generate_scenes.py <project> scene-1/1a scene-1/1b

# Regenerate a specific character only
python slides/_scripts/generate_characters.py <project> angela

# Custom PPTX output filename
python slides/_scripts/build_pptx.py <project> --out "MyDeck_v2.pptx"
```

---

## How to Create a New Project

### Step A — Scaffold the folders

```bash
PROJECT=my-new-topic
mkdir -p slides/projects/$PROJECT/characters
mkdir -p slides/projects/$PROJECT/scenes
mkdir -p slides/projects/$PROJECT/output
```

### Step B — Create `characters.json`

Define each character that will appear across scenes.
One entry per character. Model always uses `nano-banana-pro text-to-image` at 2K.

```json
[
  {
    "id": "character-id",
    "prompt": "Character reference sheet. [Full physical description]. Full body view, standing facing forward. Storybook illustration style, flat digital art, clean outlines, warm vibrant colors. Plain white background."
  }
]
```

### Step C — Create `scenes.json`

One entry per image. Key decisions per scene:

| Situation | mode | model |
|---|---|---|
| No prior image exists for this scene | `text-to-image` | `nano-banana-pro` |
| New scene using established characters | `edit` | `nano-banana-2` |
| Minor change to a previous scene | `edit-fast` | `nano-banana-2` |
| Stitch existing images into panels (no API) | `composite` | — |
| Copy output from another scene (no API) | `reuse` | — |

**Core fields:**
```json
{
  "id": "scene-1/1a",
  "title": "Short description",
  "mode": "text-to-image | edit | edit-fast | composite | reuse",
  "model": "nano-banana-pro | nano-banana-2",
  "resolution": "2k",
  "chars": ["character-id-1", "character-id-2"],
  "base_scene": "scene-1/1a",
  "base_project": "other-project-name",
  "prompt": "Full image generation prompt..."
}
```

- `chars` — character IDs whose `reference.png` is passed as image input; resolves from current project first, then `char_project` in `project.json`
- `base_scene` — scene whose `output.png` (falls back to `draft.png`) becomes the base image
- `base_project` — name of another project to resolve `base_scene` from (cross-project edits)
- Omit `chars` and `base_scene` for pure `text-to-image` scenes

---

### PIL Config Options (post-processing — no extra API cost)

These optional fields can be added to any API-based scene entry. PIL runs locally after the image is downloaded.

**`pip` — picture-in-picture stamp**

Resizes a previously generated scene and stamps it onto the output at a specified position.
The source scene must appear earlier in `scenes.json` so it is generated first.

```json
"pip": {
  "source": "scene-1/1c",
  "position": "center-right",
  "scale": 0.28,
  "border": true
}
```

- `source` — scene ID within the current project to use as the inset image
- `position` — one of: `center`, `center-right`, `center-left`, `top-right`, `top-left`, `bottom-right`, `bottom-left`
- `scale` — inset width as a fraction of the canvas width (e.g. `0.28` = 28%)
- `border` — `true` adds a thin white border frame around the inset

**`overlay` — graphic asset stamp**

Stamps a PNG asset from `slides/_assets/` onto the output (e.g. stop-sign, tick, X mark).

```json
"overlay": {
  "asset": "stop-sign",
  "position": "center",
  "scale": 0.45,
  "opacity": 0.88
}
```

- `asset` — filename (without `.png`) inside `slides/_assets/`
- `position` — same position keys as `pip`
- `scale` — overlay width as a fraction of canvas width
- `opacity` — transparency from `0.0` (invisible) to `1.0` (fully opaque)

**`composite` mode — panel stitch (PIL only, no API)**

Stitches multiple existing images side by side or stacked. No `prompt` or `model` required.

```json
{
  "id": "scene-3/3a",
  "title": "3-panel collage",
  "mode": "composite",
  "layout": "3-panel-vertical",
  "sources": [
    "projects/deliverance/scenes/scene-4/4a/draft.png",
    "projects/deliverance/scenes/scene-4/4b/draft.png",
    "projects/deliverance/scenes/scene-4/4c/draft.png"
  ]
}
```

- `layout` — one of: `3-panel-vertical`, `3-panel-horizontal`, `2-panel-vertical`, `2-panel-horizontal`
- `sources` — paths relative to the `slides/` directory

**`reuse` mode — copy from another scene (no API)**

Copies `output.png` from a previously generated scene in the same project.

```json
{
  "id": "scene-5/5c",
  "title": "Reuse praying scene",
  "mode": "reuse",
  "source": "scene-4/4c"
}
```

---

### `project.json` (optional — for cross-project character reuse)

Place in the project root to inherit characters from another project:

```json
{
  "name": "My Project Name",
  "char_project": "deliverance"
}
```

When `char_project` is set, character refs not found in the current project are resolved from that project's `characters/` folder automatically.

### Step D — Create `slides.json`

Controls PPTX slide order, theme labels, and CTA text slides.

```json
[
  { "id": "scene-1/1a", "theme": "Slide Theme Title", "cta": null },
  { "id": "scene-1/1b", "theme": "Slide Theme Title", "cta": "CTA question?\n\nAnswer!" }
]
```

- `cta: null` — image slide only
- `cta: "text"` — image slide + white CTA slide after it
- Use `\n\n` for paragraph breaks in CTA text

### Step E — Run

```bash
python slides/_scripts/generate_characters.py my-new-topic
python slides/_scripts/generate_scenes.py my-new-topic
python slides/_scripts/build_pptx.py my-new-topic
```

---

## Pricing Reference (per image at 2K)

| Mode | Model | Cost |
|---|---|---|
| `text-to-image` | nano-banana-pro | $0.14 |
| `edit` | nano-banana-pro | $0.14 |
| `edit-ultra` | nano-banana-pro | $0.15 |
| `edit` | nano-banana-2 | $0.105 |
| `edit-fast` | nano-banana-2 | $0.045 |

**Rule of thumb:** character refs ($0.14 each, once only) + scenes (~$0.08–$0.14 each).
A 12-scene deck with 5 characters costs roughly **$1.50–$2.00 total**.

---

## Content Filter Notes

- Passing a child reference image + a distress/fear prompt triggers safety filters
- **Solution:** use `text-to-image` (no image refs) for scenes where a child is scared or in danger; describe the character fully inline in the prompt
- Calm/positive scenes with child refs are fine in `edit` mode
