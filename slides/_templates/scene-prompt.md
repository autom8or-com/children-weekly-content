# Scene Prompt Template
# Usage: Fill in all [BRACKETS] and save as scenes/scene-N/Na/prompt.md

## Scene: [e.g. scene-1/1a]
## Title: [Short scene description]

---

## Mode Decision
- TEXT-TO-IMAGE → use when: no prior scene exists to build from; character refs injected via `images[]`
- EDIT (scene-to-scene) → use when: continuing/modifying a previous scene image
- EDIT (character ref) → use when: placing established characters into a new scene layout

## WaveSpeed Mode: [text-to-image | edit | edit-fast | edit-ultra]
## Model: [nano-banana-pro | nano-banana-2]
## Endpoint: /api/v1/model/google/[model]/[mode]
## Cost: [$X per image at chosen resolution]

---

## Reference Images (if edit mode)
```json
"images": [
  "characters/angela/reference.png",
  "characters/jesus/reference.png"
]
```
> For text-to-image: embed character descriptions inline in the prompt text.
> For edit mode: pass reference images via `images[]`, describe desired changes in prompt.

---

## Prompt

[SCENE PROMPT TEXT]

---

## API Payload
```json
{
  "images": [],
  "prompt": "[SCENE PROMPT]",
  "aspect_ratio": "16:9",
  "resolution": "2k",
  "output_format": "png",
  "enable_sync_mode": true
}
```

## Output
Save generated image as: `scenes/scene-N/Na/output.png`
Use as reference for: [next scene if applicable, e.g. "scene-3/3d uses this as base"]
