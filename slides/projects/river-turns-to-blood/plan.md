# River Turns to Blood — Plan

**Passage:** Exodus 7:14–25 (NIV) — the first plague.
**Sequel to:** `gods-power` (staff-to-snake). Same cast, same storybook style.
**Audience / tone:** Pre-K storybook, gentle. Blood = smooth deep-red water, no gore.

## Characters

| ID | Type | Source | Notes |
|---|---|---|---|
| moses-b | char_project | character-variants | White tunic, emerald green mantle, glowing staff |
| aaron-a | char_project | character-variants | Yellow priestly robe, gemstone breastplate, golden headband, rod |
| god-a | base image only | gods-power desert scenes | Appears in inherited base scenes (golden divine light); not generated |
| Pharaoh / officials / magicians / villagers | described inline | — | No reference; carried by consistent inline description |

## Theme 1 — God Instructs Moses and Aaron (vv 14–19)

| ID | Title | Base |
|---|---|---|
| scene-1/1a | Pharaoh still says no — go to him at the river | gods-power scene-1/1a |
| scene-1/1b | Take the staff that became a snake | gods-power scene-1/1e (+moses-b) |
| scene-1/1c | God's message: Let my people go! | gods-power scene-1/1a |
| scene-1/1d | A warning: the river will turn to blood (vision cloud) | gods-power scene-1/1a |
| scene-1/1e | Aaron, stretch your staff over all Egypt's waters | gods-power scene-1/1b (+aaron-a) |

## Theme 2 — The River Turns to Blood (vv 20–25)

| ID | Title | Base |
|---|---|---|
| scene-2/2a | Morning at the Nile — facing Pharaoh & officials | moses-b + aaron-a (new Nile setting) |
| scene-2/2b | Aaron raises the staff and strikes the water | scene-2/2a |
| scene-2/2c | The whole river turns to blood | scene-2/2b |
| scene-2/2d | The fish die and the river stinks | scene-2/2c |
| scene-2/2e | No water to drink — shock on the riverbank | scene-2/2c |
| scene-2/2f | Pharaoh's magicians copy it by their secret arts | scene-2/2c |
| scene-2/2g | Pharaoh's heart stays hard — he turns to his palace | scene-2/2c |
| scene-2/2h | The Egyptians dig for water — seven days pass | scene-2/2e |

## Continuity notes

- Theme 1 edits the actual `gods-power` desert "God speaks" outputs (1a/1b/1e) — God, Moses, Aaron, golden divine light all carry over; only the speech bubble changes (plus the 1d vision cloud).
- Theme 2 is a new Nile-riverbank setting (no prior asset). Moses & Aaron stay consistent via refs; the red river chains forward via `base_scene` so location/crowd stay fixed across 2a→2h.
- Pharaoh's costume is described identically everywhere to match his `gods-power` palace look.

## Pre-generation setup (worktree)

The new kie.ai pipeline lives in this worktree, but base-image artifacts are gitignored and live in the main checkout. Before generating, copy them in:

```bash
# Moses/Aaron character refs
mkdir -p slides/projects/character-variants/characters/{moses-b,aaron-a}
cp /Users/HP/children-content/slides/projects/character-variants/characters/moses-b/reference.png \
   slides/projects/character-variants/characters/moses-b/
cp /Users/HP/children-content/slides/projects/character-variants/characters/aaron-a/reference.png \
   slides/projects/character-variants/characters/aaron-a/

# gods-power base scene outputs used by Theme 1 (1a, 1b, 1e)
for s in 1a 1b 1e; do
  mkdir -p slides/projects/gods-power/scenes/scene-1/$s
  cp /Users/HP/children-content/slides/projects/gods-power/scenes/scene-1/$s/output.png \
     slides/projects/gods-power/scenes/scene-1/$s/
done
```

## Run commands

```bash
# Characters: none to generate (all inherited from character-variants)

# Generate all scenes
python3 slides/_scripts/generate_scenes.py river-turns-to-blood

# Sample first (recommended after prompt changes)
python3 slides/_scripts/generate_scenes.py river-turns-to-blood scene-1/1a scene-2/2a scene-2/2c

# Assemble deck
python3 slides/_scripts/build_pptx.py river-turns-to-blood
```
