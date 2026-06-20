# God's Power — Plan

## Characters

| ID | Type | Source | Notes |
|---|---|---|---|
| moses-b | char_project | character-variants | White tunic, emerald green mantle, glowing staff |
| aaron-a | char_project | character-variants | Yellow priestly robe, gemstone breastplate, golden headband |
| god-a | base image only | god-helps-me-do-hard-things | Not generated as new ref — appears in inherited base scenes |

## Scene Map

### Scene 1: Moses Thinks He Cannot Do It

| ID | Title | Base |
|---|---|---|
| scene-1/1a | God tells Moses: I have made you like God to Pharaoh | ghmdht scene-2/2b |
| scene-1/1b | God appoints Aaron as prophet | ghmdht scene-2/2b |
| scene-1/1c | God, Moses, and Aaron — cloud vision (reuse) | ghmdht scene-2/2c |
| scene-1/1d | Moses (80) and Aaron (83) — old but ready! | ghmdht scene-2/2a |
| scene-1/1e | God commands: Throw your staff before Pharaoh | ghmdht scene-2/2b |
| scene-1/1f | Moses and Aaron fly to the Israelites — Aaron in priestly cloak | titl scene-2/2d |

### Scene 2: God Demonstrates His Power

| ID | Title | Base |
|---|---|---|
| scene-2/2a | Moses declares: Let my people go! — magicians flank Pharaoh | titl scene-1/1a |
| scene-2/2b | Pharaoh rises: Show me a sign! | scene-2/2a (this project) |
| scene-2/2c | Aaron's staff becomes an upright cobra | scene-2/2b (this project) |
| scene-2/2d | Pharaoh signals — magicians step forward | scene-2/2c (this project) |
| scene-2/2e | Magicians' staffs become snakes too | scene-2/2d (this project) |
| scene-2/2f | Aaron's snake swallows them all! | scene-2/2e (this project) |
| scene-2/2g | Pharaoh furious: Get out! Get out!! | scene-2/2f (this project) |

## Run Commands

```bash
# Characters (skip — all refs inherited from character-variants)
# python3 slides/_scripts/generate_characters.py gods-power

# Generate all scenes
python3 slides/_scripts/generate_scenes.py gods-power

# Assemble deck
python3 slides/_scripts/build_pptx.py gods-power
```
