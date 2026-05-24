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
| edit | nano-banana-2 | $0.105 |
| edit-fast | nano-banana-2 | $0.045 |

### Run Commands

```bash
# Generate character reference sheets (once per project)
python3 slides/_scripts/generate_characters.py <project>

# Generate all scene images
python3 slides/_scripts/generate_scenes.py <project>

# Regenerate specific scenes
python3 slides/_scripts/generate_scenes.py <project> --redo scene-3/3c scene-4/4a

# Generate specific scenes only (no --redo)
python3 slides/_scripts/generate_scenes.py <project> scene-1/1a scene-1/1b

# Assemble PPTX
python3 slides/_scripts/build_pptx.py <project>

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
- `composite` — pure PIL stitch, no API call; use `layout` + `sources`
- `reuse` — copy another scene's output unchanged; use `source`

**Content filter rule:** Passing a child character reference image + a distress/conflict prompt triggers WaveSpeed safety filters. Use `text-to-image` (no `chars[]`) for scenes involving fear, conflict, or physical contact, describing the character inline instead.

**Sequential scenes in the same setting** must be chained via `base_scene`, not generated independently, to maintain consistent location and crowd across slides.

### PIL Post-Processing

`pip` (picture-in-picture) and `overlay` fields are applied locally after the API call. Graphic assets live in `slides/_assets/`. The `composite` mode uses PIL only, with no API call.

### WaveSpeed API

- Env var: `WAVESPEEDAI_API_KEY` (in `.env`)
- Balance: `GET /api/v3/balance`
- Fetch an existing prediction: `GET /api/v3/predictions/<task-id>/result` — use this to recover outputs without re-generating
- SSL errors on large base64 POSTs are transient; the client retries 3× with backoff automatically

### build_pptx.py Behaviour

- Prefers `output.png`, falls back to `draft.png` automatically
- Resolves `reuse` mode scenes by following the `source` pointer in scenes.json
- `slides.json` controls slide order, theme labels, and optional CTA text slides

---

## TOD Content Generation

Use the `tod-generate` skill (`/tod-generate`) for weekly content. Content lives under `content/teens/` and `content/preteens/`. Rotation schedule is in `rotation.json`.

---

## Environment

- Python 3.14, `python3` command
- Dependencies: `requests`, `python-pptx`, `Pillow`, `python-dotenv`
- Credentials in `.env` at project root: `WAVESPEEDAI_API_KEY`, `NOCODB_*`, Telegram bot tokens
- Generated images and `.pptx` files are gitignored (reproducible artifacts)
