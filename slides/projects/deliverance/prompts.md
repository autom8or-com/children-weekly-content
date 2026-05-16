# Deliverance — Full Image Prompt Document
Generated for: Pre-K / Toddler Sunday School
Art Style: Storybook Illustration (flat digital, clean outlines, warm vibrant colors)
Aspect Ratio: 16:9 | Resolution: 2K (draft: 1K)

---

## HOW TO READ THIS DOCUMENT

Each prompt has:
- **Mode** — which WaveSpeed endpoint to call
- **Model** — nano-banana-pro or nano-banana-2
- **Refs** — which character reference images to pass as `images[]`
- **Base Scene** — for scene-continuations, the prior output image to pass instead
- **Prompt** — the actual generation prompt

Character reference images are generated first (Section 0), then referenced in all subsequent scenes.

---

## SECTION 0 — CHARACTER REFERENCE SHEETS
> Run once. Re-run only if a character's design needs to change.

### CHAR-001 · Angela
**Mode:** `text-to-image` | **Model:** `nano-banana-pro` | **Cost:** $0.14 (2K)
**Save to:** `characters/angela/reference.png`

```
Character reference sheet for consistent reuse across all scenes.
Angela is a chocolate brown-skinned African toddler girl, approximately 3 years old.
She has a round chubby face, wide expressive dark eyes full of life, and short natural
hair styled in two small neat puffs on either side of her head. She wears a bright
pink pinafore dress over a white long-sleeved shirt, with white sneakers. Her
expression is warm, curious, and joyful — a big friendly innocent smile.
Full body view, standing facing directly forward, arms relaxed at her sides.
Storybook illustration style, flat digital art, clean black outlines, warm vibrant
colors. Plain pure white background. No scene, no setting, no props.
```

---

### CHAR-002 · Jesus (Superman)
**Mode:** `text-to-image` | **Model:** `nano-banana-pro` | **Cost:** $0.14 (2K)
**Save to:** `characters/jesus/reference.png`

```
Character reference sheet for consistent reuse across all scenes.
Jesus is depicted as a superhero with a warm golden-brown skin tone, kind and wise
eyes, and short dark hair. He wears a bright royal blue Superman-style full bodysuit,
a flowing red cape behind him, red boots, and a red chest shield featuring a bold
golden letter "J" (not the Superman S — it is the letter J for Jesus). His build is
strong and heroic but his expression is gentle, approachable, and warmly smiling.
One hand raised in a friendly wave.
Full body view, standing facing directly forward.
Storybook illustration style, flat digital art, clean black outlines, warm vibrant
colors. Plain pure white background. No scene, no setting, no props.
```

---

### CHAR-003 · Moses
**Mode:** `text-to-image` | **Model:** `nano-banana-pro` | **Cost:** $0.14 (2K)
**Save to:** `characters/moses/reference.png`

```
Character reference sheet for consistent reuse across all scenes.
Moses is a youthful Nigerian man with chocolate brown skin, an athletic build, and
short cropped natural hair. He wears a bright emerald green Superman-style full
bodysuit with red boots and a red chest shield bearing a bold golden letter "M".
He holds a long sturdy wooden staff/rod upright in his right hand. His expression is
confident and purposeful — the look of someone who knows his mission.
Full body view, standing facing directly forward.
Storybook illustration style, flat digital art, clean black outlines, warm vibrant
colors. Plain pure white background. No scene, no setting.
```

---

### CHAR-004 · Aaron
**Mode:** `text-to-image` | **Model:** `nano-banana-pro` | **Cost:** $0.14 (2K)
**Save to:** `characters/aaron/reference.png`

```
Character reference sheet for consistent reuse across all scenes.
Aaron is a youthful Nigerian man with chocolate brown skin, an athletic build similar
to Moses, and short cropped natural hair. He wears a bright sunshine yellow
Superman-style full bodysuit with red boots and a red chest shield bearing a bold
golden letter "A". He holds a long sturdy wooden staff/rod upright in his left hand.
His expression is friendly, eager, and loyal — ready to act.
Full body view, standing facing directly forward.
Storybook illustration style, flat digital art, clean black outlines, warm vibrant
colors. Plain pure white background. No scene, no setting.
```

---

### CHAR-005 · The Serpent
**Mode:** `text-to-image` | **Model:** `nano-banana-pro` | **Cost:** $0.14 (2K)
**Save to:** `characters/serpent/reference.png`

```
Character reference sheet for consistent reuse across all scenes.
The Serpent is a gigantic cartoon snake — exaggeratedly enormous in scale, not
realistic. Bright emerald green body with slightly darker green diamond scale markings.
Large cartoonish yellow eyes with narrowed sinister pupils. A wide open mouth showing
comically oversized white fangs and a forked red tongue. Body loosely coiled.
Clearly cartoon-style — menacing in character but not realistically frightening for
young children. No additional characters or background.
Full body visible.
Storybook illustration style, flat digital art, clean black outlines, vibrant colors.
Plain pure white background.
```

---

**Section 0 Total: 5 images × $0.14 = $0.70**

---

## SECTION 1 — SCENE 1: What Is Deliverance?

### IMG-1A · Angela Chased by the Serpent
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/angela/reference.png`
- `characters/serpent/reference.png`

```
Using the provided reference images, compose a wide storybook scene.
The girl from the reference (chocolate brown-skinned toddler, pink pinafore dress,
two-puff natural hair) is running in full panic toward the LEFT of the frame — arms
flailing, tears streaming down her round chubby face, mouth open in a terrified cry.
Her legs show speed and urgency. Behind her from the RIGHT, the gigantic cartoon snake
from the reference (enormous emerald green, yellow cartoon eyes, wide grinning open
mouth) lunges forward in hot pursuit, body coiling and surging toward her.
Background: bright blue sky, simple flat green grass, clear daytime. Diagonal
composition lines drive the eye from right to left creating a feeling of speed and
panic. No graphic violence. Child-friendly storybook picture-book aesthetic.
Flat digital art, clean outlines, warm vibrant colors.
```

---

### IMG-1B · Jesus Rescues Angela; Snake Flees
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/angela/reference.png`
- `characters/jesus/reference.png`
- `characters/serpent/reference.png`

```
Using the provided reference images, compose a wide heroic rescue storybook scene.
Jesus from the reference (blue Superman suit, red flowing cape, golden "J" on chest
shield, warm golden-brown skin, kind strong face) swoops down dramatically from the
UPPER LEFT of the frame, arms outstretched, cradling Angela (from reference —
chocolate-skinned toddler, pink pinafore, two-puff hair) safely in his arms. Angela's
tears are drying, expression shifting from terror to relief — a small grateful smile
beginning to form as she looks up at Jesus. On the RIGHT side of the frame, the
enormous cartoon serpent (from reference — emerald green, yellow eyes) has turned
completely around and is fleeing in the opposite direction with a comically panicked
wide-eyed expression, body coiling backward rapidly. Bright sunny sky with warm golden
rays around Jesus. Dynamic action lines show movement. Child-friendly storybook
picture-book aesthetic. Flat digital art, clean outlines, warm vibrant colors.
```

---

**Section 1 Total: 2 images × $0.105 = $0.21 (final run)**

---

## SECTION 2 — SCENE 2: Heroes of Our Deliverance

### IMG-2A · God Sends Moses and Aaron
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/moses/reference.png`
- `characters/aaron/reference.png`

```
Using the provided reference images, compose a wide awe-inspiring storybook scene of
divine commissioning. From the UPPER CENTRE of the frame, brilliant golden beams of
light pour down from a glowing bright cloud — representing God's presence and voice —
shining directly onto two figures standing below. On the LEFT stands Moses (from
reference — emerald green Superman costume, golden M on chest, wooden staff held
upright, chocolate brown skin), gazing upward with an expression of wonder and
reverent awe. On the RIGHT stands Aaron (from reference — sunshine yellow Superman
costume, golden A on chest, wooden staff, chocolate brown skin), also gazing upward
with the same reverent awe. Both stand tall with expressions of readiness and holy
purpose. The ground beneath them is sandy with warm tones. The sky is brightened
by the divine golden light. Warm golden color palette. Reverent, majestic mood.
Storybook picture-book aesthetic. Flat digital art, clean outlines.
```

---

### IMG-2B · Moses and Aaron Before Pharaoh (Serpent Watching)
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/moses/reference.png`
- `characters/aaron/reference.png`
- `characters/serpent/reference.png`

```
Using the provided reference images, compose a wide tense confrontation scene inside
an ancient Egyptian palace. The palace background features tall ornate columns with
simplified Egyptian hieroglyph patterns, a red carpet runner on the floor, gold
decorative urns, and flickering torchlight. On the LEFT of the frame stand Moses
(emerald green Superman costume, golden M breastplate, wooden staff, confident upright
posture) and Aaron (yellow Superman costume, golden A breastplate, wooden staff) side
by side, facing right with bold and fearless expressions. On the RIGHT, Pharaoh sits
on a grand ornate golden throne — depicted as a cartoon older man in Egyptian regal
attire, golden crown, flowing golden robes, arms folded, stern and unimpressed
expression. In the BACKGROUND partially visible — curled lazily around the base of
one of the palace columns — is the enormous cartoon serpent from the reference
(emerald green, yellow sly eyes), watching the encounter with a smug expression.
Dramatic but child-friendly. Storybook picture-book aesthetic. Flat digital art,
clean outlines, vibrant colors with dramatic shadows.
```

---

### IMG-2C · The Israelites — A Sympathetic Scene of Oppression
**Mode:** `text-to-image` | **Model:** `nano-banana-pro` | **Cost:** $0.14 (2K)
**Refs:** None (no specific characters)

```
Storybook illustration, flat digital art style, clean outlines. Wide 16:9 scene
evoking deep sympathy and compassion. A group of people — children and adults,
warm chocolate and brown skin tones, dressed in simple rough worn cloth — are depicted
in oppressed conditions. Some are bent under the weight of heavy clay bricks stacked
on their backs. Some sit exhausted on dry ground, heads drooping, arms heavy with
tiredness. Some children sit with sad tearful eyes and dust-covered faces. The people
are clearly weary, burdened, and longing for relief. Egyptian overseer silhouettes
stand at the far edges of the frame — depicted simply as authority figures, no graphic
content. The color palette is intentionally muted and desaturated: warm earthy browns,
beige tones, grey shadows, dusty ochre — conveying sadness and heaviness. The
composition draws the eye to the tired faces and burdened figures at the centre.
No violence depicted. Emotionally resonant storybook aesthetic designed to stir
compassion in young hearts.
```

---

**Section 2 Total: 2 × $0.105 + 1 × $0.14 = $0.35**

---

## SECTION 3 — SCENE 3: Who Is the Victim?

### IMG-3A · Angela and the Crowd Pursued by Many Serpents
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/angela/reference.png`
- `characters/serpent/reference.png`

```
Using the provided reference images, compose a wide chaotic storybook scene showing
universal pursuit. A diverse crowd of people — children and adults, young and old,
warm brown and chocolate skin tones, varied clothing — all run in panic across the
frame from RIGHT to LEFT. Multiple giant cartoon serpents of different colors (emerald
green like the reference, plus red, purple, orange — each one enormous and
cartoonishly menacing) chase the crowd from behind and from the right edge. Angela
(from reference — chocolate-skinned toddler girl, pink pinafore dress, two-puff
natural hair, face showing fear and urgency) is clearly visible in the FOREGROUND of
the crowd, one of the most prominent fleeing figures. The composition is wide and
busy, showing that everyone — young and old — is caught up in this flight. The mood
is chaotic but the style remains clearly child-friendly cartoon. No graphic violence.
Storybook picture-book aesthetic. Flat digital art, clean outlines, vibrant but
slightly ominous colors.
```

---

### IMG-3B · Sin Entered the World Through the Serpent (Garden of Eden)
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/serpent/reference.png`

```
Using the provided serpent reference image, compose a wide lush storybook scene
depicting the garden of Eden. The garden is beautiful and vibrant — tall fruit trees
with leafy canopies, colorful tropical flowers in pink, yellow, and orange, bright
rich green grass, butterflies fluttering. It should feel like paradise at first
glance. At the CENTRE-RIGHT of the frame, the enormous cartoon serpent from the
reference (emerald green, yellow sly narrowed eyes) is coiled slyly around the trunk
of the largest fruit tree, its body winding upward. The serpent's head rests near a
cluster of bright red glistening fruit hanging from the tree, and it looks down with
a curved knowing smile — mischievous and deceptive. The area directly around the
serpent has subtly cooler and darker tones (deeper shadow, slightly more sinister
colors) contrasting the bright paradise elsewhere in the scene. No human figures in
this image. The serpent and the forbidden fruit are the sole narrative focus.
Storybook picture-book aesthetic. Flat digital art, clean outlines, lush vibrant
colors.
```

---

### IMG-3C · Jesus Flies In With the Bible Over the Fleeing Crowd
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Base Scene (images[0]):** `scenes/scene-3/3a/output.png` *(the crowd scene)*
**Additional Refs:** `characters/jesus/reference.png`

```
Using the provided crowd scene image as the base (people and serpents fleeing across
the frame), add Jesus entering dramatically into the scene. Jesus (from the reference
— bright blue Superman suit, red flowing cape, golden "J" on red chest shield,
golden-brown skin, determined and compassionate expression) flies into the frame from
the UPPER RIGHT, body angled forward in flight with one arm outstretched ahead and
the other hand holding a bright white glowing Bible — a golden cross on its cover,
light radiating from it. Strong golden radiant light emanates from Jesus outward
across the scene. Dynamic diagonal speed lines trail behind him showing his velocity
and power. Keep the panicked crowd and the serpents visible in the lower portion of
the frame exactly as they appear in the base image. The overall atmosphere begins
to shift from fearful to hopeful — warm golden light starts to fill the scene from
the direction Jesus comes from. Storybook illustration style, flat digital art, clean
outlines. Do not remove any existing elements from the base scene.
```

---

### IMG-3D · Serpents Gone — People Rejoice and Thank God
**Mode:** `edit-fast` | **Model:** `nano-banana-2` | **Cost:** $0.045 (2K)
**Base Scene (images[0]):** `scenes/scene-3/3c/output.png` *(Jesus arriving over crowd)*

```
Using the provided scene image of Jesus flying over the panicked crowd as the starting
point, apply the following specific changes:
1. REMOVE all serpents from the scene entirely — no snakes anywhere in the image.
2. STOP the crowd from running — every person is now still.
3. TRANSFORM all fearful expressions and poses into joyful, grateful ones:
   - Some people have both arms raised high in praise
   - Some are on their knees with heads bowed in prayer
   - Some are crying happy tears with wide smiles
   - Some are hugging each other in relief and joy
4. Angela (the chocolate-skinned toddler in the pink pinafore dress, visible in the
   foreground) should be shown with hands clasped together, looking upward at Jesus
   with the widest smile and relieved happy tears.
5. Jesus above remains the same — floating, smiling warmly, Bible still in hand.
6. FLOOD the entire scene with warm golden sunlight — replace all ominous tones with
   brightness, warmth, and celebration.
Keep all storybook illustration style, character designs, and scene layout from the
base image. Only the above elements should change.
```

---

**Section 3 Total: 3 × $0.105 + 1 × $0.045 = $0.36**

---

## SECTION 4 — SCENE 4: Why Does Jesus Set Us Free?

### IMG-4A · Angela Serves Water to Jesus in the Sitting Room
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/angela/reference.png`
- `characters/jesus/reference.png`

```
Using the provided reference images, compose a warm cozy domestic storybook scene.
Setting: a simple comfortable Nigerian home sitting room. Features: a colourful sofa
with patterned throw pillows, a vibrant patterned rug on the floor, curtains with
warm natural daylight streaming softly through the window, a small side table.
Jesus (from reference — blue Superman suit with red cape draped casually over the
back of the sofa, golden "J" on chest shield) sits comfortably on the sofa, relaxed,
hands resting on his knees, looking across toward Angela with a warm, grateful,
appreciating smile. Angela (from reference — chocolate-skinned toddler, pink pinafore
dress, two-puff natural hair) is walking carefully toward Jesus from the right, both
tiny hands wrapped around a small colourful plastic cup of water, her tongue slightly
out in concentration, her face full of proud loving eagerness not to spill a single
drop. The scene radiates warmth, love, and joyful service. Soft warm interior
lighting. Child-friendly storybook picture-book aesthetic. Flat digital art, clean
outlines.
```

---

### IMG-4B · Angela and Jesus Read the Bible Together in the Garden
**Mode:** `edit` | **Model:** `nano-banana-2` | **Cost:** $0.07 (1K draft) → $0.105 (2K final)
**Refs (images[]):**
- `characters/angela/reference.png`
- `characters/jesus/reference.png`

```
Using the provided reference images, compose a peaceful beautiful garden storybook
scene of learning and companionship. Setting: a lush garden with soft green grass,
colorful flowers in pink, yellow, and orange, and a large leafy tree at the centre.
Warm golden afternoon sunlight filters through the tree's canopy, casting dappled
light across the scene.
Jesus (from reference — blue Superman suit, red cape, golden "J" on chest) sits
cross-legged at the base of the tree, relaxed and attentive, one side open for
Angela. Angela (from reference — chocolate-skinned toddler, pink pinafore dress,
two-puff hair) sits snugly pressed against his side, both of them leaning slightly
together. Resting across both their laps is a large open Bible — white pages, golden
cross on the cover. Jesus points gently to a line on the page with one finger;
Angela looks up at him with wide bright curious eyes and a joyful smile, clearly
delighted by what she's hearing. The scene feels intimate, safe, and full of love.
Peaceful, nurturing mood. Child-friendly storybook picture-book aesthetic. Flat
digital art, clean outlines, warm golden light.
```

---

### IMG-4C · Angela Wears Her Own "A" Cape — Empowered
**Mode:** `edit-fast` | **Model:** `nano-banana-2` | **Cost:** $0.045 (2K)
**Base Scene (images[0]):** `scenes/scene-4/4b/output.png` *(garden reading scene)*

```
Using the provided garden scene of Angela and Jesus reading the Bible together as
the starting point, apply the following specific changes to Angela only:
1. ADD a small bright red Superman-style cape flowing behind Angela — matching the
   visual style and color of Jesus's cape but scaled to her toddler size.
2. ADD a small golden "A" badge/breastplate shield on the FRONT of her pink pinafore
   dress, over her chest — styled like Jesus's "J" shield but with the letter A.
3. CHANGE Angela's pose: she is now standing upright beside Jesus, hands on hips in
   a confident proud heroic stance, looking DIRECTLY AT THE VIEWER with the widest
   most joyful smile.
4. ADJUST Jesus: he is now standing beside Angela (slightly taller), one hand resting
   gently and proudly on her shoulder, his other hand giving a warm thumbs-up, smiling
   at her with deep pride and delight.
5. Keep the garden background, the golden afternoon light, the tree, the flowers —
   all exactly as in the base scene.
The overall mood should shift to joyful, victorious, celebratory, and empowering.
```

---

**Section 4 Total: 2 × $0.105 + 1 × $0.045 = $0.255**

---

## TOTAL COST SUMMARY

| Section | Images | Est. Cost |
|---|---|---|
| Section 0 — Character Refs | 5 | $0.70 |
| Section 1 — Scene 1 | 2 | $0.21 |
| Section 2 — Scene 2 | 3 | $0.35 |
| Section 3 — Scene 3 | 4 | $0.36 |
| Section 4 — Scene 4 | 3 | $0.255 |
| **TOTAL (final run)** | **17** | **~$1.875** |
| Draft run (1K) first | 11 scenes | ~$0.63 |

**Draft → Approve → Final workflow total: ~$2.50**

---

## GENERATION ORDER

Always run in this order (dependencies must exist before referencing):

```
0. Character refs (all 5) — independent, run in parallel
1. scene-2/2c              — no refs (pure text-to-image)
2. scene-1/1a, scene-1/1b, scene-2/2a, scene-2/2b, scene-3/3a, scene-3/3b, scene-4/4a, scene-4/4b — use char refs
3. scene-3/3c              — depends on scene-3/3a output
4. scene-3/3d              — depends on scene-3/3c output
5. scene-4/4c              — depends on scene-4/4b output
```
