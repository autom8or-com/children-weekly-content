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

**Fields:**
```json
{
  "id": "scene-1/1a",
  "title": "Short description",
  "mode": "text-to-image | edit | edit-fast",
  "model": "nano-banana-pro | nano-banana-2",
  "resolution": "2k",
  "chars": ["character-id-1", "character-id-2"],
  "base_scene": "scene-1/1a",
  "prompt": "Full image generation prompt..."
}
```

- `chars` — list of character IDs whose `reference.png` will be passed as image inputs
- `base_scene` — scene ID whose `output.png` becomes the base image (for scene continuations)
- Omit `chars` and `base_scene` for pure `text-to-image` scenes

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
