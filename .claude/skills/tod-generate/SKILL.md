---
name: tod-generate
description: >
  Generates complete, print-ready Sunday activity Word documents (.docx) for RCCG Tabernacle
  of David (TOD) Teens Church — covering both Teens (ages 13-19) and Pre-Teens (ages 9-12).
  Produces fully filled-in Game sheets, three Quiz variants (A/B/C) with unified answer keys,
  or Presentation guidelines with group assignments — grounded in conservative biblical truth.
  Uploads each file to NocoDB storage and stores download links. Sends a Telegram notification
  with all download links when done. Resumes from a checkpoint if a previous run was interrupted.
  Invoke whenever Sunday content needs to be prepared: user says "generate Sunday content",
  "prepare this week's materials", "it's Friday", runs /tod-generate with or without a date,
  or asks for TOD church activity materials. Also fires on scheduled Friday routines.
---

# TOD Sunday Content Generator

All paths are relative to the project root: `/Users/HP/children-content/`
Scripts live in: `.claude/skills/tod-generate/scripts/`

---

## STEP 0 — Resume check

Load secrets from `.env` first (all subsequent scripts depend on them):
```bash
set -a && source .env && set +a
```

Then check for an existing checkpoint:

```bash
python3 .claude/skills/tod-generate/scripts/checkpoint.py status 2>/dev/null
```

**If a checkpoint exists for this Sunday** → print its status to the user, confirm which steps
are already done, and skip those steps below. Jump to the first step marked `pending`.

**If no checkpoint or different date** → proceed from Step 1 (a fresh checkpoint is created
at the end of Step 2 once we know the target date and passages).

---

## STEP 1 — Find the target Sunday

```bash
python3 -c "
from datetime import date, timedelta
today = date.today()
days = (6 - today.weekday()) % 7
days = 7 if days == 0 else days
print((today + timedelta(days=days)).strftime('%Y-%m-%d'))
"
```

If the user passed a specific date (e.g. `/tod-generate 2026-06-14`), use that instead.

---

## STEP 2 — Look up the rotation + init checkpoint

Read `config/rotation.json`. Find the entry where `"date"` matches the target Sunday.

Extract: `activity`, `teens.passage`, `teens.extra`, `preteens.passage`, `preteens.extra`

**If activity is SKIPPED or MESSAGE**:
> "This is a **[1st/MESSAGE] Sunday** — no activity content needed.
> Bible reading: Teens: [passage] + [extra] | Pre-Teens: [passage] + [extra]."
Stop here. No checkpoint needed.

**If activity is GAME, QUIZ, or PRESENTATION**, initialise the checkpoint:
```bash
python3 .claude/skills/tod-generate/scripts/checkpoint.py init \
  [DATE] [ACTIVITY] "[TEENS_PASSAGE]" "[PRETEENS_PASSAGE]"
```

Then mark rotation done:
```bash
python3 .claude/skills/tod-generate/scripts/checkpoint.py set rotation_lookup done
```

---

## STEP 3 — NocoDB table setup (already done — skip on all runs)

The `tod_content_library` table was created in the Pora Student base on 2026-05-07.
All credentials are in `.env` (sourced in Step 0):
- `NOCODB_BASE_URL=https://nocodb.aiautom8or.com`
- `NOCODB_BASE_ID=pi615b94l2p403o`
- `NOCODB_TABLE_ID=m0lpo3ciq9q35t1`

**Skip this step entirely.** `nocodb_upload.py` reads directly from these env vars.

> If the table is ever lost and needs to be recreated, see the git history of this SKILL.md
> for the original curl commands (Step 3 before 2026-05-07).

---

## STEP 4 — Generate & build Teens content

Skip any sub-step already marked `done` in the checkpoint.

Set the Node path once before running any scripts:
```bash
export NODE_PATH=$(npm root -g)
SKILL=".claude/skills/tod-generate/scripts"
OUTDIR="content/teens/[DATE]_[ACTIVITY]_[TEENS_PASSAGE_NO_SPACES]"
mkdir -p "$OUTDIR" /tmp/tod_specs/teens
```

### Conservative biblical framing — applies to all content
All answers must reflect clear, orthodox Christian truth. No ambiguous or relativistic framing.
Correct answers are definitively correct. Applications are practical and faith-affirming for teens.

---

### 4a — Write the JSON spec   (checkpoint: `teens_spec_written`)

Read the appropriate template from `templates/` then produce the JSON spec below.

**GAME** → write `/tmp/tod_specs/teens/game.json`:
```json
{
  "title": "GAME SUNDAY",
  "passage": "[Teens passage]",
  "extra": "Psalms 19:7-11",
  "date": "[DATE]",
  "cohort": "TEENS",
  "church": "RCCG Tabernacle of David (TOD)",
  "principle": "[Overarching biblical truth — 1-2 sentences]",
  "sections": [
    {"title": "[S1 title]", "verses": "[e.g. Acts 20:1-6]"},
    {"title": "[S2 title]", "verses": "..."},
    {"title": "[S3 title]", "verses": "..."},
    {"title": "[S4 title]", "verses": "..."},
    {"title": "[S5 title]", "verses": "..."}
  ],
  "round1": [
    {"section":"1","phrase":"[Near-exact Scripture quote]","reference":"[Book Ch:v]"},
    {"section":"2","phrase":"...","reference":"..."},
    {"section":"3","phrase":"...","reference":"..."},
    {"section":"4","phrase":"...","reference":"..."},
    {"section":"5","phrase":"...","reference":"..."}
  ],
  "round2": [
    {"section":"1","question":"[WHY/significance question]","answer":"[2-3 sentence biblical answer guide]"},
    {"section":"2","question":"...","answer":"..."},
    {"section":"3","question":"...","answer":"..."},
    {"section":"4","question":"...","answer":"..."},
    {"section":"5","question":"...","answer":"..."}
  ],
  "round3": [
    {"section":"1","statement":"[True/false statement]","answer":"TRUE","explanation":"[Why]"},
    {"section":"2","statement":"...","answer":"FALSE","explanation":"..."},
    {"section":"3","statement":"...","answer":"...","explanation":"..."},
    {"section":"4","statement":"...","answer":"...","explanation":"..."},
    {"section":"5","statement":"...","answer":"...","explanation":"..."}
  ],
  "closing": "[Complete personalized closing discussion statement]"
}
```

**QUIZ** → write `/tmp/tod_specs/teens/quiz.json`:
```json
{
  "title": "QUIZ SUNDAY",
  "passage": "[Teens passage]",
  "extra": "Psalms 19:7-11",
  "date": "[DATE]",
  "cohort": "TEENS",
  "church": "RCCG Tabernacle of David (TOD)",
  "variant_a": [
    {"question":"...","options":{"A":"...","B":"...","C":"...","D":"..."},"correct":"B"},
    "...29 more questions"
  ],
  "variant_b": ["...30 different questions"],
  "variant_c": ["...30 different questions"]
}
```
Difficulty rules: 9 Easy + 13 Moderate + 8 Hard = 30 per variant.
Section coverage: 6 questions × 5 sections = 30.
Correct answers: ~7-8 per letter (A/B/C/D) — do not cluster.
Variants must be genuinely different, not paraphrases.

**PRESENTATION** → write `/tmp/tod_specs/teens/presentation.json`:
```json
{
  "title": "PRESENTATION SUNDAY",
  "passage": "[Teens passage]",
  "extra": "Psalms 19:7-11",
  "date": "[DATE]",
  "cohort": "TEENS",
  "church": "RCCG Tabernacle of David (TOD)",
  "groups": [
    {
      "topic_title": "[Section 1 topic]",
      "summary": "[2-3 sentences]",
      "verses": "[e.g. Acts 22:1-11]",
      "questions": [
        "What happened? (narrative)",
        "Why did [key character] act this way? (motivation)",
        "What does this reveal about God or faith? (principle)",
        "How does this apply to your life as a teen? (application)"
      ],
      "principle": "[Spiritual truth — 1-2 sentences]",
      "members": ["Member 1","Member 2","Member 3"]
    },
    "...4 more groups"
  ],
  "closing_remarks": "[Pre-filled facilitator closing connecting all 5 sections]",
  "discussion_questions": ["...","...","..."]
}
```

After writing the spec, checkpoint it:
```bash
python3 $SKILL/checkpoint.py set teens_spec_written done
```

---

### 4b — Build Word documents   (checkpoint: `teens_docx_built`)

**GAME:**
```bash
node $SKILL/build_game.js /tmp/tod_specs/teens/game.json \
  "$OUTDIR/Game_Teens_[PASSAGE].docx"

python3 $SKILL/checkpoint.py add-file teens \
  "Game_Teens_[PASSAGE].docx" "$OUTDIR/Game_Teens_[PASSAGE].docx" GAME_SHEET
```

**QUIZ:**
```bash
for VARIANT in A B C; do
  node $SKILL/build_quiz.js /tmp/tod_specs/teens/quiz.json \
    "$OUTDIR/Quiz_Teens_Variant_${VARIANT}_[PASSAGE].docx" $VARIANT
  python3 $SKILL/checkpoint.py add-file teens \
    "Quiz_Teens_Variant_${VARIANT}_[PASSAGE].docx" \
    "$OUTDIR/Quiz_Teens_Variant_${VARIANT}_[PASSAGE].docx" "QUIZ_VARIANT_$VARIANT"
done
node $SKILL/build_quiz.js /tmp/tod_specs/teens/quiz.json \
  "$OUTDIR/Quiz_Teens_Answer_Keys_[PASSAGE].docx" KEYS
python3 $SKILL/checkpoint.py add-file teens \
  "Quiz_Teens_Answer_Keys_[PASSAGE].docx" \
  "$OUTDIR/Quiz_Teens_Answer_Keys_[PASSAGE].docx" QUIZ_ANSWER_KEYS
```

**PRESENTATION:**
```bash
node $SKILL/build_presentation.js /tmp/tod_specs/teens/presentation.json \
  "$OUTDIR/Presentation_Teens_Guideline_[PASSAGE].docx" GUIDELINE
python3 $SKILL/checkpoint.py add-file teens \
  "Presentation_Teens_Guideline_[PASSAGE].docx" \
  "$OUTDIR/Presentation_Teens_Guideline_[PASSAGE].docx" PRESENTATION_GUIDELINE

node $SKILL/build_presentation.js /tmp/tod_specs/teens/presentation.json \
  "$OUTDIR/Presentation_Teens_Group_Assignments_[PASSAGE].docx" GROUPS
python3 $SKILL/checkpoint.py add-file teens \
  "Presentation_Teens_Group_Assignments_[PASSAGE].docx" \
  "$OUTDIR/Presentation_Teens_Group_Assignments_[PASSAGE].docx" PRESENTATION_GROUPS
```

Checkpoint:
```bash
python3 $SKILL/checkpoint.py set teens_docx_built done
```

---

### 4c — Upload to NocoDB   (checkpoint: `teens_nocodb_uploaded`)

For every file registered in the checkpoint under `teens`, run:
```bash
RESULT=$(python3 $SKILL/nocodb_upload.py \
  --file        "[local_path]" \
  --sunday-date "[DATE]" \
  --cohort      TEENS \
  --activity    "[ACTIVITY]" \
  --passage     "[TEENS_PASSAGE]" \
  --file-type   "[file_type]" \
  --settings    config/settings.json)

URL=$(echo $RESULT | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['download_url'])")
RID=$(echo $RESULT | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['record_id'])")

python3 $SKILL/checkpoint.py set-url teens "[filename]" "$URL" "$RID"
```

After all teens files are uploaded:
```bash
python3 $SKILL/checkpoint.py set teens_nocodb_uploaded done
```

---

## STEP 5 — Generate & build Pre-Teens content

Repeat the same sub-steps (5a, 5b, 5c) as Step 4 with these differences:
- `"cohort": "PRE-TEENS"` in the JSON spec
- Spec files: `/tmp/tod_specs/preteens/`
- Output folder: `content/preteens/[DATE]_[ACTIVITY]_[PRETEENS_PASSAGE_NO_SPACES]/`
- File names: `Preteens` instead of `Teens`
- Checkpoint steps: `preteens_spec_written`, `preteens_docx_built`, `preteens_nocodb_uploaded`
- Upload flag: `--cohort PRE-TEENS`

**Language adjustments for ages 9-12:**
- Simpler vocabulary — no jargon without a plain-English explanation beside it
- Questions lean narrative over analytical
- Application examples from school, home, friendships
- Hard questions are still substantive, just in plainer language than the Teens version

---

## STEP 6 — Telegram notification   (checkpoint: `telegram_sent`)

Read `$TELEGRAM_GROUP_CHAT_ID` and `$TELEGRAM_TOPIC_ID` from the environment (sourced from
`.env` in Step 0).
Read `.claude/checkpoint.json` → collect all `download_url` values from `files.teens` and
`files.preteens`.

Build the file links block (one line per file):
```
• [Teens] Game_Teens_Acts20.docx → https://...
• [Teens] (answer keys, if QUIZ) → https://...
• [Pre-Teens] Game_Preteens_John7.docx → https://...
```

Fill `completion_message_template` from `config/settings.json → telegram.completion_message_template` with:
- `{date}` → Sunday date formatted as "10 May 2026"
- `{activity}` → e.g. "GAME"
- `{teens_passage}` → e.g. "Acts 20"
- `{preteens_passage}` → e.g. "John 7"
- `{file_links}` → the bullet list built above

Send using the Telegram MCP tool (`mcp__plugin_telegram_telegram__reply`):
- `chat_id`: `$TELEGRAM_GROUP_CHAT_ID`
- `reply_to`: `$TELEGRAM_TOPIC_ID` (routes message to the "Oworo Children's Content" forum topic)
- `text`: the filled template (Markdown enabled — template uses `*bold*` formatting)

If `TELEGRAM_GROUP_CHAT_ID` is empty, skip and print:
> "Telegram skipped — add TELEGRAM_GROUP_CHAT_ID to .env to enable."

After sending:
```bash
python3 .claude/skills/tod-generate/scripts/checkpoint.py set telegram_sent done
```

---

## STEP 7 — Final summary

```
✅  Sunday [DATE] — [ACTIVITY]

TEENS ([Passage] + Psalms 19:7-11)
  Files: [list .docx names]
  Folder: content/teens/[folder]/
  NocoDB: [N] records created

PRE-TEENS ([Passage] + Psalms 19:7-11)
  Files: [list .docx names]
  Folder: content/preteens/[folder]/
  NocoDB: [N] records created

📲  Telegram: [sent | skipped — no chat_id]

[PRESENTATION only]
📋  Reminder: Distribute Guideline docs to groups by [SUNDAY DATE − 7 days].
```

---

## One-time setup (already complete ✅)

All credentials are in `.env` — no further setup needed:
- `NOCODB_API_TOKEN`, `NOCODB_BASE_URL`, `NOCODB_BASE_ID`, `NOCODB_TABLE_ID`
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_GROUP_CHAT_ID`, `TELEGRAM_TOPIC_ID`

The NocoDB table `tod_content_library` exists in the Pora Student base at
`https://nocodb.aiautom8or.com` (table ID `m0lpo3ciq9q35t1`).

---

## Quality checks before finishing

- [ ] 5 narrative sections with titles and exact verse ranges
- [ ] Biblical answers reflect orthodox Christian understanding throughout
- [ ] Quiz variants are genuinely different (not paraphrases)
- [ ] Quiz correct answers spread across A/B/C/D
- [ ] Game phrases are near-exact Scripture quotes
- [ ] Presentation topics span all 5 sections
- [ ] Pre-Teens content uses noticeably simpler language
- [ ] All Word docs built without errors (check node output)
- [ ] All files uploaded to NocoDB (check checkpoint)
- [ ] Checkpoint shows all steps `done` before finishing
