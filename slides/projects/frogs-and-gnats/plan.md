# Frogs and Gnats — Plan

**Passage:** Exodus 8:1–19 (NIV) — the second and third plagues.
**Sequel to:** `river-turns-to-blood` (first plague). Same cast, same storybook style.
**Theme:** Stubbornness — Pharaoh's hardened heart and its consequences.
**Audience / tone:** Pre-K storybook, gentle. Frogs = cute cartoon style. Gnats = dense dark buzzing swarms.

## Characters

| ID | Type | Source | Notes |
|---|---|---|---|
| moses-b | char_project | character-variants | Young, dark brown skin, clean-shaven, white tunic + emerald green mantle, glowing staff |
| aaron-a | char_project | character-variants | Young, dark brown skin, yellow priestly robe, gemstone breastplate, golden headband, rod |
| god-a | copied | god-helps-me-do-hard-things | Elderly, long white hair/beard, glowing white robes, golden light, golden throne. Appears ONLY inside the memory bubble |
| Pharaoh / officials / magicians / villagers | base image | rttb + gods-power | Inherited from base scenes; no ref sheet |

## Memory Bubble Format (God speaking to Moses)

God's instruction is drawn **inside an AI-generated cloud-shaped memory/thought bubble** floating above Moses — connected to him by small thought-bubble circles, with the `god-a` figure rendered inside it and a small speech bubble carrying God's words. **No PIL pip.** The bubble is produced entirely by the edit prompt (pattern from rttb scene-1/1d), passing `god-a` as a character ref so the divine figure is visually consistent with prior projects.

The chain enforced across each pair of slides: **God spoke → Moses heard (memory bubble) → Moses told Aaron (speech bubble) → Aaron acted (next slide).**

## Continuity Strategy (why scenes look right)

- **Don't strip the base; disturb it as little as possible.** The instruction frames (1a, 2a) keep the *full* rttb `scene-2/2a` cast (Pharaoh + officials + Moses + Aaron) and only *add* the God bubble + Moses's relay speech. Action frames chain off them, so Pharaoh and the court persist down the whole Nile sequence.
- **Never reposition a character in a cross-edit** — moving a figure forces a redraw, which drifts appearance (aged faces, wrong skin, lost staff). Pin roles explicitly instead ("it is AARON who acts, not Moses").
- **Anchor youth with refs.** When a Nile/edit frame drifts Moses elderly, re-pass `moses-b`/`aaron-a` refs to re-anchor the young, clean-shaven look (no repositioning).
- Palace scenes anchor to `gods-power scene-2/2a` (cleanest direct ref application), not to downstream edits.

## Scene Map

### Scene 1: The Frog Plague (Exodus 8:1–15)

| ID | Title | Mode | Base | Refs | Slide |
|---|---|---|---|---|---|
| 1/1a | God warns Moses; Moses relays to Aaron (Nile) | edit | rttb 2/2a | moses-b, aaron-a, god-a | 1 |
| 1/1b | Aaron stretches rod — frogs rise | edit | 1/1a | — | 2 |
| 1/1c | Frogs swarm and cover the land | edit | 1/1b | — | 3 |
| 1/1d | Frogs invade the palace — Pharaoh horrified | edit | gods-power 2/2a | — | 4 |
| 1/1e | Magicians also make frogs — worse! | edit | rttb 2/2f | moses-b, aaron-a | 5 |
| 1/1f | Pharaoh begs: Pray to the Lord! | edit | gods-power 2/2b | moses-b, aaron-a | 6 |
| 1/1g | Moses prays — frogs die in smelly heaps | edit | 1/1c | — | 7 |
| 1/1h | Pharaoh sees relief, hardens his heart | edit | 1/1f | — | 8 + CTA |

### Scene 2: The Gnat Plague (Exodus 8:16–19)

| ID | Title | Mode | Base | Refs | Slide |
|---|---|---|---|---|---|
| 2/2a | God instructs Moses; Moses relays to Aaron (gnats) | edit | rttb 2/2a | moses-b, aaron-a, god-a | 9 |
| 2/2b | Aaron strikes the dust — gnats swarm | edit | 2/2a | moses-b, aaron-a | 10 |
| 2/2c | Magicians try and fail — finger of God! | edit | gods-power 2/2a | moses-b, aaron-a | 11 + CTA |
| 2/2d | Pharaoh still hard — trouble upon trouble | edit | 2/2c | — | 12 + CTA |

**Total:** 12 image slides + 3 CTA slides = 15 deck slides.

## Lessons (CTA slides)

1. **v9, v12–15** — Many want God's blessings without repentance. Pharaoh asked Moses to pray, then hardened his heart the moment relief came.
2. **v18** — Human power has limits. Magicians could copy blood and frogs but could not produce gnats.
3. **v19** — Some acknowledge God only when disaster forces them ("the finger of God"). Choose him now.
4. **Overall** — Stubbornness brings trouble upon trouble, one plague upon another.

## Run Commands

```bash
# Characters: none to generate (moses-b/aaron-a inherited; god-a copied into characters/)

# Check balance
python3 -c "import requests,os;from dotenv import load_dotenv;load_dotenv('.env');print(requests.get('https://api.kie.ai/api/v1/chat/credit',headers={'Authorization':f'Bearer {os.environ[\"KIE_API_KEY\"]}'}).json()['data'])"

# Generate all scenes (skips existing; --redo to force; existing output.png is auto-backed-up to _backups/<ts>/)
python3 slides/_scripts/generate_scenes.py frogs-and-gnats

# Assemble deck
python3 slides/_scripts/build_pptx.py frogs-and-gnats
```
