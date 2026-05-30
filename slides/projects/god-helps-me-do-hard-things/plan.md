# God Helps Me Do Hard Things

## Theme
Both Moses and Angela faced tasks they felt too weak for. God helped both of them. He will help us too.

## Characters

| ID | Description | Source |
|---|---|---|
| god-a | Kindly elderly God, seated on golden throne | New — generate |
| god-b | Kindly elderly God, standing/active pose | New — generate |
| moses-a | Moses in bright emerald green robe, gold sash | `char_project`: character-variants |
| aaron-a | Aaron in priestly breastplate + golden headband (prophet variant) | `char_project`: character-variants |
| aaron-b | Aaron in simple yellow robe (everyday variant) | `char_project`: character-variants |
| angela | Toddler girl, chocolate skin, pink pinafore | Copied from deliverance/characters/ |

Note: infog-a is generated as `scene-util/infog-a` (text-to-image), not a character ref.

## Scene Map

### Utility Scenes (not in slides.json)

| Scene | Mode | Depends On | Description |
|---|---|---|---|
| scene-util/infog-a | text-to-image | — | Hand infographic — Hebrews 13:5, finger labels |

### Scene 1: Moses Thinks He Cannot Do It

| Scene | Mode | Depends On | Model |
|---|---|---|---|
| scene-1/1a | reuse | titl `scene-2/2b` | — |
| scene-1/1b | edit | scene-1/1a | nano-banana-2 |
| scene-1/1c | edit + scene_ref | scene-1/1b + ref: titl `scene-1/1b` | nano-banana-2 |
| scene-1/1d | edit-fast | scene-1/1c | nano-banana-2 |

**CTA:** "Moses thought he could not do it."

### Scene 2: God Encourages Moses

| Scene | Mode | Depends On | Model |
|---|---|---|---|
| scene-2/2a | edit | titl `scene-2/2b` | nano-banana-2 |
| scene-2/2b | edit + god-a | scene-2/2a | nano-banana-2 |
| scene-2/2c | edit + scene_ref | scene-2/2b + ref: titl `scene-1/1a` | nano-banana-2 |
| scene-2/2d | edit-fast | scene-2/2c | nano-banana-2 |

**CTA:** "God promised to help Moses."

### Scene 3: Angela Thinks She Cannot Do It

| Scene | Mode | Depends On | Model |
|---|---|---|---|
| scene-3/3a | edit | titl `scene-3/3b` | nano-banana-2 |
| scene-3/3b | edit-fast | scene-3/3a | nano-banana-2 |
| scene-3/3c | edit-fast | scene-3/3b | nano-banana-2 |
| scene-3/3d | edit-fast | scene-3/3c | nano-banana-2 |
| scene-3/3e | edit + 2× scene_refs | scene-3/3d + refs: scene-util/infog-a, titl `scene-4/4d` | nano-banana-2 |
| scene-3/3f | edit-fast | scene-3/3e | nano-banana-2 |
| scene-3/3g | edit-fast | scene-3/3f | nano-banana-2 |

**CTA:** "Angela thought she could not do it."

## Cost Estimate

| Item | Count | Unit | Subtotal |
|---|---|---|---|
| New character refs (god-a, god-b) | 2 | $0.14 | $0.28 |
| text-to-image scene (infog-a) | 1 | $0.14 | $0.14 |
| Edit scenes (1b, 1c, 2a, 2b, 2c, 3a, 3e) | 7 | $0.105 | $0.735 |
| Edit-fast scenes (1d, 2d, 3b, 3c, 3d, 3f, 3g) | 7 | $0.045 | $0.315 |
| Reuse (1a) | 1 | free | $0.00 |
| **Total** | | | **~$1.47** |

## Run Order

```bash
# 1. Check balance
python3 -c "
import requests, os
from dotenv import load_dotenv
load_dotenv('.env')
r = requests.get('https://api.wavespeed.ai/api/v3/balance', headers={'Authorization': f'Bearer {os.environ[\"WAVESPEEDAI_API_KEY\"]}'})
print(r.json()['data']['balance'])
"

# 2. Generate new characters (god-a, god-b only)
python3 slides/_scripts/generate_characters.py god-helps-me-do-hard-things

# 3. Sample before full run
python3 slides/_scripts/generate_scenes.py god-helps-me-do-hard-things scene-util/infog-a scene-2/2b

# 4. Full scene generation
python3 slides/_scripts/generate_scenes.py god-helps-me-do-hard-things

# 5. Build PPTX
python3 slides/_scripts/build_pptx.py god-helps-me-do-hard-things
```
