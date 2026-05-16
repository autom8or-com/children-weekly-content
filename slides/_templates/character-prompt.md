# Character Reference Prompt Template
# Usage: Fill in all [BRACKETS] and save as characters/<id>/prompt.md

## Character ID: [angela | jesus | moses | aaron | serpent]
## WaveSpeed Mode: text-to-image
## Model: nano-banana-pro
## Endpoint: /api/v1/model/google/nano-banana-pro/text-to-image
## Cost: $0.14/image (2K)

---

## Prompt

Character reference sheet. [FULL CHARACTER DESCRIPTION]. 
Storybook illustration style, flat digital art, clean outlines, warm vibrant colors. 
Full body view, standing facing forward, plain white or very light background. 
No scene, no action — pure character reference for consistent reuse. 
Expressive face showing [DOMINANT EMOTION/PERSONALITY]. 
16:9 canvas with the character centered.

---

## API Payload Template
```json
{
  "prompt": "[PASTE PROMPT ABOVE]",
  "aspect_ratio": "16:9",
  "resolution": "2k",
  "output_format": "png",
  "enable_sync_mode": true
}
```

## Output
Save generated image as: `characters/[id]/reference.png`
