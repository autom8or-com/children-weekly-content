# Lesson Brief — Robert the Prodigal Student

## 1. Identity
- slug:             robert-prodigal-student
- series / part:    Parables of Jesus · Part 1 (the Prodigal Son, retold)
- passage:          Luke 15:11-32 (NIV)
- sunday / date:    TBD
- audience / tone:  Pre-teens graduating primary → secondary school in Lagos. Nigerian, modern dress, relatable urban context. Conversational, storybook-comic tone — the parable is told in panels with baked-in text bubbles like a real comic strip.

## 2. Lesson (the teaching spine)
- theme (one line):     Decision time — choose Jesus over the world's parties; repentance brings you home
- memory verse:         "But we had to celebrate and be glad, because this brother of yours was dead and is alive again; he was lost and is found." — Luke 15:32 (NIV)
- bible text:           Luke 15:11-32 (full passage, two-column layout on the bible-text slide)
- objectives:
    - Tell the Prodigal Son story in their own words, panel by panel
    - Identify the 3 conditions of the lost son (without senses, dead while alive, lost)
    - Apply the 5 lessons to their own transition from primary to secondary school
    - Make a personal decision to defy worldly school parties and belong to Jesus
- big questions:
    - What does it mean to be "lost" when your parents are right there?
    - What does repentance actually look like in school life?
    - Why does heaven throw a party when one person repents?
- angela study title:   Robert the Prodigal Student
- application:          Choosing Jesus over the world's parties at your new school — and the A-B-C rescue plan when you slip
- teaching points:      # one block per point Nicolas will document in her diary
    - point:         Without his senses
      teacher_note:  You need to be consistent in your prayer and devotions so you have prayer and wisdom stored up for many days. So you can know bad friends and avoid them.
      angela_line:   "He ate with pigs because he lost his senses — if you don't pray daily, you'll lose yours too."
      scripture:     Luke 15:17
      pull_slide:    scene-2/2a (pigs)
    - point:         Dead while alive
      teacher_note:  As far as I am separated from God through sin and disobedience, I am dead alive. Everyday in school, if I disobey God I will be dead while alive.
      angela_line:   "Every time you disobey God, you're alive on the outside but dead on the inside."
      scripture:     Luke 15:24
      pull_slide:    scene-2/2a (pigs, alone)
    - point:         Lost
      teacher_note:  His parents did not hear from him. His life was hidden from his parents. As I go to school I must be brave to tell my parents about my problems.
      angela_line:   "If your parents haven't heard from you in a while — that's the lost condition."
      scripture:     Luke 15:24
      pull_slide:    scene-1/1b (far country)
    - point:         Repentant
      teacher_note:  He confessed his sin. Whenever you spot you have started little little disobediences, run back to God and repent. Tell your parents too. They will be happy for and pray for you.
      angela_line:   "Repentance isn't just a feeling — it's the decision to run back, even when you're dirty."
      scripture:     Luke 15:21
      pull_slide:    scene-2/2b (father runs)
    - point:         Heaven throws a party
      teacher_note:  Every time I bring a sinner to repentance, I cause a party in heaven. So as you go you must decide not to follow bad friends, not to be disobedient to your parents, observe your devotions daily, and be repentant when you sin. Most of all, tell others about it. Then you will be causing joy in heaven.
      angela_line:   "When one of you decides for Jesus — heaven throws a feast. You matter that much."
      scripture:     Luke 15:10
      pull_slide:    scene-2/2b (father runs)

## 3. Cast
- robert  : new            # 12-year-old Lagos pre-teen, the "prodigal student" — pre-teen-friendly, modern dress
- father  : new            # Nigerian dad in his 40s, warm and dignified, the kind who runs not walks
- nicolas : new            # 12-13 year-old Lagos girl, the diary narrator (replaces Angela from earlier decks)
- bad-friends / party crowd : inline   # only described inline in panel 2, no ref sheet needed
- pigs : inline                       # only described inline in panel 3, no ref sheet needed

## 4. Continuity
- base projects:    none — fresh cast, fresh story, no cross-project reuse

## 5. Story beats  (ordered → become illustrations + story slides)
# COMIC RULE for this project: every panel has a header banner at the top + 1-2 baked-in
# speech bubbles (≤6 words each) so the story reads as a real conversational comic strip.
# The story-card body around the image narrates AROUND the dialogue, not over it.
- 1: HE WANTED HIS SHARE    — Robert, age 12, demands his share of the family money from Father in their Lagos living room. Father, heartbroken, hands it over.
- 2: THE FAR COUNTRY        — Robert at a loud Lagos party with older bad friends, money flying, drinks in hand. He's smiling but out of place.
- 3: HE ENDED UP WITH PIGS  — Robert alone, dirty, hungry, sitting in a muddy pig pen at the edge of a remote village. No bubble — visual silence, the lowest point.
- 4: FATHER RAN TO HIM      — Father RUNNING down the road toward Robert, arms wide open, big relieved smile. Robert walks toward him, humble, head down.

## 6. Deck sections  (include / drop; order runs top → bottom)
- open:       [ {include:welcome}, {include:let-us-pray}, {include:house-rules} ]
- preamble:   [ topic, objectives, memory-verse, bible-text, big-questions ]
- per-story:  story-card ×4 (one per §5 beat, panel image + 1-line narration)
              + section-header "THE FULL STORY" → composite (4-panel wide strip) as one big story-card
- angela:     [ section-header "NICOLAS'S DIARY" (thumbs of 4 comic panels),
                diary-card ×5 (one per §2 teaching point, image pulled from pull_slide) ]
- wrap:       [ application, summary, goodbye ]

## 7. Constraints
- scene budget:     4 panel scenes + 1 composite (PIL-only)  →  4 API calls
- cost ceiling:     ≤ $1.20
- provider:         kie.ai (default)
- sensitivities:    pre-teen safe. Panel 3 (pigs) uses text-to-image to avoid child-ref + distress filter. No gore, no injuries. Pigs are friendly-looking cartoon pigs, not filthy realistic ones. Robert's sadness is shown through posture, not tears.
- art direction:    storybook flat digital art, clean bold black outlines, warm vibrant colours — same line weight and palette across all 4 panels. Lagos-modern dress (t-shirts, jeans, sneakers), not biblical robes.

## 8. Delivery
- format:           .pptx (native render via deck_render.py) + per-scene PNGs
- destination:      slides/projects/robert-prodigal-student/output/
- deadline:         TBD
