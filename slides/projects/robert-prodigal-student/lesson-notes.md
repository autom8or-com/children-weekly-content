# Lesson Notes — Robert the Prodigal Student

> **Audience:** Pre-teens graduating primary → secondary in Lagos.
> **Passage:** Luke 15:11–32 (NIV) — the Prodigal Son, retold in a modern Nigerian setting.
> **Tone:** Storybook-comic, conversational, fully baked-in text bubbles.
> **Topic title (Angela/Nicolas's diary headline):** *Robert the Prodigal Student*

---

## 1. The Theme (one line)

**Decision time — choose Jesus over the world's parties; repentance brings you home.**

This is the moment in the school year when your kids are about to step out of the safe primary-school bubble into a new world of secondary school. New friends. New parties. New pressure. The Prodigal Son story lands differently here: Robert is THEIR age, in THEIR world, and the choices he made are the exact choices they will be tempted to make.

**Anchor verse:** *Luke 15:32* — "But we had to celebrate and be glad, because this brother of yours was dead and is alive again; he was lost and is found."

**The call to action:** Before they step into SS1, decide now: *I belong to Jesus. No matter what.*

---

## 2. The Teaching Points (Nicolas's diary → 5 diary cards)

These are the 5 lessons the children will leave with. Each one is a diary card. The body and `teacher_note` are taken **directly** from the brief — do not rewrite them.

### 2.1 Without his senses *(Luke 15:17)*
**Angela/Nicolas line:** "He ate with pigs because he lost his senses — if you don't pray daily, you'll lose yours too."
**Teacher note:** You need to be consistent in your prayer and devotions so you have prayer and wisdom stored up for many days. So you can know bad friends and avoid them.
**Pull slide:** `scene-2/2a` (pigs)

### 2.2 Dead while alive *(Luke 15:24)*
**Angela/Nicolas line:** "Every time you disobey God, you're alive on the outside but dead on the inside."
**Teacher note:** As far as I am separated from God through sin and disobedience, I am dead alive. Everyday in school, if I disobey God I will be dead while alive.
**Pull slide:** `scene-2/2a` (pigs, alone)

### 2.3 Lost *(Luke 15:24)*
**Angela/Nicolas line:** "If your parents haven't heard from you in a while — that's the lost condition."
**Teacher note:** His parents did not hear from him. His life was hidden from his parents. As I go to school I must be brave to tell my parents about my problems.
**Pull slide:** `scene-1/1b` (far country)

### 2.4 Repentant *(Luke 15:21)*
**Angela/Nicolas line:** "Repentance isn't just a feeling — it's the decision to run back, even when you're dirty."
**Teacher note:** He confessed his sin. Whenever you spot you have started little little disobediences, run back to God and repent. Tell your parents too. They will be happy for and pray for you.
**Pull slide:** `scene-2/2b` (father runs)

### 2.5 Heaven throws a party *(Luke 15:10)*
**Angela/Nicolas line:** "When one of you decides for Jesus — heaven throws a feast. You matter that much."
**Teacher note:** Every time I bring a sinner to repentance, I cause a party in heaven. So as you go you must decide not to follow bad friends, not to be disobedient to your parents, observe your devotions daily, and be repentant when you sin. Most of all, tell others about it. Then you will be causing joy in heaven.
**Pull slide:** `scene-2/2b` (father runs / feast)

---

## 3. The Story Beats (4 comic panels)

| # | Header | Story |
|---|---|---|
| 1 | **HE WANTED HIS SHARE** | Robert, 12, demands his share of the family money from Father in their Lagos living room. Father, heartbroken, hands it over. |
| 2 | **THE FAR COUNTRY** | Robert at a loud Lagos party with older bad friends, money flying, drinks in hand. Smiling but out of place. |
| 3 | **HE ENDED UP WITH PIGS** | Robert alone, dirty, hungry, in a muddy pig pen. Lowest point. No bubble — visual silence. |
| 4 | **FATHER RAN TO HIM** | Father RUNNING toward Robert, arms wide open, big smile. Reunion. |

Each panel has a header banner + 1–2 baked-in speech bubbles (≤ 6 words each). The story is told through the bubbles; the story-card body narrates AROUND the dialogue, not over it.

---

## 4. The Cast

| ID | Role | Look | Where they appear |
|---|---|---|---|
| `robert` | The Prodigal Student — 12-yr-old Lagos pre-teen | Medium-dark chocolate-brown skin, short black hair, navy graphic t-shirt, jeans, white-and-red sneakers | Panels 1, 2, 3, 4 (all 4) |
| `father` | The forgiving dad — 40s Nigerian man | Dark brown skin, short black hair with grey at the temples, light blue rolled-sleeve shirt, dark trousers | Panels 1 + 4 |
| `nicolas` | The diary narrator — 13-yr-old Lagos girl | Medium-dark skin, long dark braids, white shirt, green-navy plaid skirt, gold cross pendant, holds a small Bible | Diary cards (5) — ref is ready for future expansions |

The bad-friends crowd and the pigs are **inline** — no character refs. They're described in the panel prompts only.

---

## 5. The Cast is Open

This brief leaves the cast open. If you ever want to:
- Add the older brother (resentful) for a follow-up lesson on jealousy
- Add a "new school friend" cast to mirror the secondary-school transition
- Add a "big sister" cast to anchor Nicolas

…just append to `characters.json` and the same pipeline picks it up.

---

## 6. How to Run

```bash
# Step 1 — character references (3 chars × $0.14 = $0.42)
python3 slides/_scripts/generate_characters.py robert-prodigal-student

# Step 2 — 4 panel scenes + 1 composite (PIL-only) — see cost table
python3 slides/_scripts/generate_scenes.py robert-prodigal-student

# Step 3 — assemble PPTX
python3 slides/_scripts/build_pptx.py robert-prodigal-student
```

For a single panel re-roll, use `--redo scene-2/2a` (etc).
For sample-2-first, run the first 2 panels: `python3 slides/_scripts/generate_scenes.py robert-prodigal-student scene-1/1a scene-1/1b`.
