# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

Children's Sunday school content pipeline — two distinct systems:
1. **TOD (Teaching of the Day)**: Word document generation for weekly presentations/quizzes
2. **Slides**: AI-generated storybook illustration pipeline → PowerPoint decks

---

## Slides Pipeline

### Mandatory Pre-Work Before Any New Project

Read these files **before writing prompts or making any API calls**:
1. `slides/README.md` — pricing table, folder structure, PIL config options
2. `slides/projects/<source-project>/characters.json` — exact character descriptions (costumes, props, colours). Never describe characters from memory.
3. `slides/projects/<source-project>/scenes.json` — mode patterns, base_scene chains, prompt style
4. `slides/projects/<source-project>/plan.md` — character table and scene map

Always do a cost estimate before generating. Pricing (2K resolution):

| Mode | Model | Cost |
|---|---|---|
| text-to-image | nano-banana-pro | $0.14 |
| edit | nano-banana-pro | $0.14 |
| edit-ultra | nano-banana-pro | $0.15 |
| edit | nano-banana-2 | $0.105 |
| edit-fast | nano-banana-2 | $0.045 |

Rule of thumb: character refs ($0.14 each, generated once) + scenes (~$0.08–$0.14 each). A 12-scene deck with 5 characters ≈ **$1.50–$2.00 total**.

### Approval Gate — Required Before Any Generation

After writing or updating `scenes.json` for any project, **always** output both tables below and the cost estimate, then **stop and wait for explicit user approval** before running `generate_characters.py` or `generate_scenes.py`.

**Scene dependency table** (one row per scene):

| Scene | Type | Depends On | Model |
|---|---|---|---|
| scene-N/Na | reuse / edit / edit-fast / text-to-image / composite | base scene or source (with project if cross-project) + pip sources | nano-banana-2 / nano-banana-pro / — |

**Character table** (one row per character):

| ID | Type | Model |
|---|---|---|
| char-id | new / copied / char_project | nano-banana-pro / — |

**Cost estimate table:**

| Item | Count | Unit | Subtotal |
|---|---|---|---|
| New character refs | N | $0.14 | $X |
| Edit scenes | N | $0.105 | $X |
| Edit-fast scenes | N | $0.045 | $X |
| Reuse / composite | N | free | $0.00 |
| **Total** | | | **$X** |

Do not run any generation command until the user responds with approval.

### Before Any Regeneration Run

1. **Character + prompt sync**: After updating character reference PNGs, search every `scenes.json` (including dependent projects using `char_project`) for stale inline costume descriptions and update them before calling `generate_scenes.py`. Mismatched prompts produce wrong images at full cost.
2. **Check balance first**: Run the balance check command before any generation run.
3. **Sample before full run**: After major prompt changes, generate 2–3 representative scenes first (`generate_scenes.py <project> scene-X/Xa scene-Y/Yb`) to confirm output quality before committing to the full run.

### Run Commands

```bash
# Generate character reference sheets (once per project)
python3 slides/_scripts/generate_characters.py <project>

# Regenerate a single character only
python3 slides/_scripts/generate_characters.py <project> <character-id>

# Generate all scene images
python3 slides/_scripts/generate_scenes.py <project>

# Regenerate specific scenes
python3 slides/_scripts/generate_scenes.py <project> --redo scene-3/3c scene-4/4a

# Generate specific scenes only (no --redo)
python3 slides/_scripts/generate_scenes.py <project> scene-1/1a scene-1/1b

# Assemble PPTX
python3 slides/_scripts/build_pptx.py <project>

# Custom PPTX filename
python3 slides/_scripts/build_pptx.py <project> --out MyDeck_v2.pptx

# Check WaveSpeed balance
python3 -c "
import requests, os
from dotenv import load_dotenv
load_dotenv('.env')
r = requests.get('https://api.wavespeed.ai/api/v3/balance', headers={'Authorization': f'Bearer {os.environ[\"WAVESPEEDAI_API_KEY\"]}'})
print(r.json()['data']['balance'])
"
```

### scenes.json Schema

```json
{
  "id": "scene-2/2a",
  "title": "Short description",
  "mode": "text-to-image | edit | edit-fast | composite | reuse",
  "model": "nano-banana-pro | nano-banana-2",
  "resolution": "2k",
  "chars": ["character-id"],
  "base_scene": "scene-1/1a",
  "base_project": "deliverance",
  "prompt": "...",
  "pip": { "source": "scene-1/1c", "position": "center-right", "scale": 0.28, "border": true },
  "overlay": { "asset": "stop-sign", "position": "center", "scale": 0.45, "opacity": 0.88 },
  "layout": "3-panel-vertical",
  "sources": ["projects/deliverance/scenes/scene-4/4a/output.png"],
  "source": "scene-4/4c"
}
```

**Mode decision rules:**
- `text-to-image` + `nano-banana-pro` — no prior image; character appearance described inline in prompt
- `edit` + `nano-banana-2` — placing characters into a new scene; pass refs via `chars[]`; do NOT re-describe characters already passed via refs
- `edit-fast` + `nano-banana-2` — minor modification to a previous scene; use `base_scene`
- `composite` — pure PIL stitch, no API call; use `layout` + `sources`; layouts: `3-panel-vertical`, `3-panel-horizontal`, `2-panel-vertical`, `2-panel-horizontal`; `sources` paths are relative to `slides/`
- `reuse` — copy another scene's output unchanged; use `source`

`chars` resolves from the current project first, then falls back to `char_project` set in `project.json`. `base_scene` similarly respects `base_project` for cross-project edits.

**Content filter rule:** Passing a child character reference image + a distress/conflict prompt triggers WaveSpeed safety filters. Use `text-to-image` (no `chars[]`) for scenes involving fear, conflict, or physical contact, describing the character inline instead.

**Sequential scenes in the same setting** must be chained via `base_scene`, not generated independently, to maintain consistent location and crowd across slides.

### PIL Post-Processing

`pip` (picture-in-picture) and `overlay` fields are applied locally after the API call. Graphic assets live in `slides/_assets/`. The `composite` mode uses PIL only, with no API call.

Valid `position` values for both `pip` and `overlay`: `center`, `center-right`, `center-left`, `top-right`, `top-left`, `bottom-right`, `bottom-left`.

### WaveSpeed API

- Env var: `WAVESPEEDAI_API_KEY` (in `.env`)
- Balance: `GET /api/v3/balance`
- Fetch an existing prediction: `GET /api/v3/predictions/<task-id>/result` — use this to recover outputs without re-generating
- SSL errors on large base64 POSTs are transient; the client retries 3× with backoff automatically

### build_pptx.py Behaviour

- Prefers `output.png`, falls back to `draft.png` automatically
- Resolves `reuse` mode scenes by following the `source` pointer in scenes.json
- `slides.json` controls slide order, theme labels, and optional CTA text slides:
  - `"cta": null` — image slide only
  - `"cta": "Question?\n\nAnswer!"` — image slide + white CTA slide; use `\n\n` for paragraph breaks

### project.json (optional)

Place in the project root to inherit characters from another project:

```json
{ "name": "My Project Name", "char_project": "deliverance" }
```

When `char_project` is set, character refs not found locally are resolved from that project's `characters/` folder.

### Prompt Templates

`slides/_templates/character-prompt.md` and `slides/_templates/scene-prompt.md` contain canonical style guides for writing prompts. Read these when starting a new project.

---

## TOD Content Generation

Use the `tod-generate` skill (`/tod-generate`) for weekly content. Content lives under `content/teens/` and `content/preteens/`. Rotation schedule is in `rotation.json`.

---

## Environment

- Python 3.14, `python3` command
- Dependencies: `requests`, `python-pptx`, `Pillow`, `python-dotenv`
- Credentials in `.env` at project root: `WAVESPEEDAI_API_KEY`, `NOCODB_*`, Telegram bot tokens
- Generated images and `.pptx` files are gitignored (reproducible artifacts)
