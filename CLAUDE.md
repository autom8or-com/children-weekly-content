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

# Check kie.ai credit balance (default provider)
python3 -c "
import requests, os
from dotenv import load_dotenv
load_dotenv('.env')
r = requests.get('https://api.kie.ai/api/v1/chat/credit', headers={'Authorization': f'Bearer {os.environ[\"KIE_API_KEY\"]}'})
print(r.json()['data'])
"

# Check WaveSpeed balance (opt-in provider)
python3 -c "
import requests, os
from dotenv import load_dotenv
load_dotenv('.env')
r = requests.get('https://api.wavespeed.ai/api/v3/balance', headers={'Authorization': f'Bearer {os.environ[\"WAVESPEEDAI_API_KEY\"]}'})
print(r.json()['data']['balance'])
"
```

### Image Providers

The slides pipeline runs on two interchangeable providers behind one interface:

- **kie.ai** (default) — `KIE_API_KEY`. Job API: `POST /api/v1/jobs/createTask`, poll `GET /api/v1/jobs/recordInfo?taskId=`. Reference images must be URLs, so local refs are auto-uploaded via the base64 upload endpoint first. No separate `edit`/`edit-fast` endpoints — edit-vs-generate is inferred from whether refs are passed.
- **WaveSpeed** (opt-in) — `WAVESPEEDAI_API_KEY`. Inline base64 refs; per-mode endpoints.

Selection precedence: `--provider kie|wavespeed` flag → `"provider"` field in `project.json` → `IMAGE_PROVIDER` env → default `kie`. Model names (`nano-banana-pro`, `nano-banana-2`) and `scenes.json` are identical across providers.

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

**Dialogue-in-image rule (default clean, bubbles sparingly):** Illustrations default to CLEAN scene art — the slide's text card carries the words. But a baked-in speech/thought bubble (or a banner where a bubble won't fit) is allowed **only where a single spoken line IS the teaching** (a key warning, an ironic confession) — used sparingly, never on every scene, and never on impact/spectacle scenes (a plague striking, a crowd, a split-panel distinction), which stay wordless. When a bubble is used: keep it ≤6 words, quote the exact text in the prompt with "neat, correctly-spelled cartoon lettering" (models garble long text), and trim the story-card body so it narrates *around* the quote rather than echoing it.

**Sequential scenes in the same setting** must be chained via `base_scene`, not generated independently, to maintain consistent location and crowd across slides.

### PIL Post-Processing

`pip` (picture-in-picture) and `overlay` fields are applied locally after the API call. Graphic assets live in `slides/_assets/`. The `composite` mode uses PIL only, with no API call.

Valid `position` values for both `pip` and `overlay`: `center`, `center-right`, `center-left`, `top-right`, `top-left`, `bottom-right`, `bottom-left`.

### kie.ai API (default provider)

- Env var: `KIE_API_KEY` (in `.env`)
- Credit balance: `GET /api/v1/chat/credit`
- Submit: `POST /api/v1/jobs/createTask` with `{model, input:{prompt, image_input:[urls], aspect_ratio, resolution, output_format}}`
- Poll: `GET /api/v1/jobs/recordInfo?taskId=<id>` → `data.state` in {waiting, queuing, generating, success, fail}; on success parse `data.resultJson` (JSON string) → `resultUrls[0]`
- Local reference images are uploaded first via `POST https://kieai.redpandaai.co/api/file-base64-upload` (temp URL, auto-deleted ~3 days)
- Client retries POST/GET/upload 3× with backoff automatically

### WaveSpeed API (opt-in provider)

- Env var: `WAVESPEEDAI_API_KEY` (in `.env`)
- Balance: `GET /api/v3/balance`
- Fetch an existing prediction: `GET /api/v3/predictions/<task-id>/result` — use this to recover outputs without re-generating
- SSL errors on large base64 POSTs are transient; the client retries 3× with backoff automatically

### build_pptx.py Behaviour

`build_pptx.py` auto-detects two deck flavours from `slides.json`:

**Typed lesson deck** (any entry has a `"type"` key) — the storybook lesson format. Two render paths:
- **Native (default)** — `deck_render.py` builds real PowerPoint shapes + **editable text** boxes, with the illustration placed as a picture. Edit text afterward in PowerPoint or Canva. Close to the mock (exact palette/layout/fonts; uniform card corners, no divider bar). Requires Caveat + Patrick Hand fonts installed on whatever machine opens the file. Embedded illustrations are downscaled to 1600px JPEG (q88) on the way in to keep the `.pptx` light (~5–6MB vs ~95MB at full 2K); originals and `collections.zip` stay full-res. Tune via `IMG_MAX_W` / `IMG_QUALITY` in `deck_render.py`.
- **Screenshot (`--screenshot`)** — `deck_html.py` renders each slide to standalone 1920×1080 HTML (fonts via Google Fonts, images inlined as data URIs), `playwright-cli` (headless) screenshots it, placed full-bleed. Pixel-perfect to the mock but flat images (not editable). Needs `playwright-cli` + a Chromium + network for the web fonts.

Slide types and fields (`palette` ∈ `preamble|flies|livestock|boils|diary`; inline `**bold**` supported in any text):
- `title` / `goodbye` — `{eyebrow, title, subtitle?, date?, footer?, image?}` (goodbye = dark bg). `date: "auto"` fills today's date (e.g. "28th June 2026").
- `topic` — `{eyebrow?, title, image?}` standalone topic bookend (dark bg; eyebrow defaults to "✦ TOPIC ✦")
- `section-header` — `{palette, eyebrow, title, footer, thumbs?:[scene_id]}` (thumbs = decorative thumbnail row)
- `verse` — `{eyebrow, title, reference, image?}` (dark bg) · `prayer` — `{eyebrow, title, footer?, image?}`
- `house-rules` — `{palette?, chip?, title?, rules:[{emoji|icon, text}]}` (boilerplate; usually via the `house-rules` partial)
- `objectives` — `{palette?, chip?, title?, lead?, bullets:[{emoji, text}], image?}`
- `outlines` — `{palette?, chip?, title?, items:[{label, image?}]}` (agenda grid; thumbs are story scenes)
- `bible-text` — `{eyebrow?, reference, body:[paragraph…], columns?:1|2}` (long scripture; 2 columns if multi-paragraph)
- `application` — `{title?, intro:[line…], steps_lead?, steps?:[{letter, text}], image?}` — altar-call slide; `steps` defaults to the A-B-C of salvation
- `story-card` — `{palette, chip, title, body:[{text, strong?}], prompt?, image?}`
- `diary-card` — `{chip, title, body:[{text, strong?}], teacher_note?, signature, image?}` (Angela's voice; Odun authors the text). `teacher_note` is written to the slide's **speaker-notes pane** in the native deck (teacher sees it, kids don't; omitted from screenshot decks); set it to `null` to opt a card out. A diary-card with no `teacher_note` key triggers a build `[GUARD]` warning.
- `summary` — `{palette, chip, title, bullets:[{emoji, text}], prompt?, image?}`

`image` (and `thumbs[]`, `items[].image`, `rules[].icon`) is either a `scenes.json` scene id (→ its `output.png`/`draft.png`, or a `reuse` source) **or a static-asset path** ending in an image extension (e.g. `_assets/icons/mute.png`), resolved relative to `slides/`. Omit for text-only slides.

**Boilerplate partials** — repeating slides (weekly welcome, opening prayer, house rules) live once under `slides/_templates/partials/<name>.json`; a project references them in `slides.json` with `{"include": "<name>"}` (extra keys on the include override the partial). Available: `welcome`, `let-us-pray`, `house-rules`. The renderers (`deck_render.py` native + `deck_html.py` screenshot) are kept in lockstep — any new slide type must be added to **both**.

**Legacy image deck** (no `"type"`) — full-bleed scene image + optional CTA text slide. Preserves older projects (frogs-and-gnats, deliverance, etc.):
- Prefers `output.png`, falls back to `draft.png`; resolves `reuse` scenes via the `source` pointer
- `"cta": null` — image slide only · `"cta": "Q\n\nA"` — image slide + white CTA slide (`\n\n` = paragraph break)

### project.json (optional)

Place in the project root to inherit characters from another project:

```json
{ "name": "My Project Name", "char_project": "deliverance" }
```

When `char_project` is set, character refs not found locally are resolved from that project's `characters/` folder.

### Prompt Templates

`slides/_templates/character-prompt.md` and `slides/_templates/scene-prompt.md` contain canonical style guides for writing prompts. Read these when starting a new project.

**Starting a new lesson deck:** copy `slides/_templates/brief-template.md` to `slides/projects/<slug>/brief.md` and fill it (or paste a rough brief). The brief is the single story-agnostic intake "request"; it expands into `project.json`, `scenes.json`, `slides.json`, and `lesson-notes.md`. Then run the approval gate before generating.

**Angela's Diary authoring rule (don't drift):** the diary is defined **once** — in the brief's §2 teaching points (mirrored into `lesson-notes.md`). Each teaching point becomes **exactly one** `diary-card` whose body and `teacher_note` are **transcribed** from §2, never invented during `slides.json` authoring. Pull each card's picture from an existing story scene (the point's `pull_slide`), not a bespoke Angela portrait, unless §2 says otherwise. Never resolve an `OPEN DECISION` silently at build time — settle it with Odun first (`build_pptx.py` prints a `[GUARD]` warning if one survives, or if a diary-card is missing its `teacher_note`).

---

## TOD Content Generation

Use the `tod-generate` skill (`/tod-generate`) for weekly content. Content lives under `content/teens/` and `content/preteens/`. Rotation schedule is in `rotation.json`.

---

## Environment

- Python 3.14, `python3` command
- Dependencies: `requests`, `python-pptx`, `Pillow`, `python-dotenv`
- Credentials in `.env` at project root: `KIE_API_KEY`, `IMAGE_PROVIDER`, `WAVESPEEDAI_API_KEY`, `NOCODB_*`, Telegram bot tokens
- Generated images and `.pptx` files are gitignored (reproducible artifacts)
