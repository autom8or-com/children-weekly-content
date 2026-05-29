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

**If no entry is found for that date** → print:
> "No rotation entry for [DATE] — nothing to generate. Add this date to `config/rotation.json` to schedule content."

Stop here. Do not proceed.

Extract: `activity`, `teens.passage`, `teens.extra`, `preteens.passage`, `preteens.extra`

**If activity is SKIPPED or MESSAGE**, send a Telegram reading reminder then stop.

Build the message:
```
*No activity this Sunday ([formatted date])*

Bible reading for the week:
• Teens: [teens.passage] + [teens.extra]
• Pre-Teens: [preteens.passage] + [preteens.extra]
```

Send using the Telegram MCP tool (`mcp__plugin_telegram_telegram__reply`):
- `chat_id`: `$TELEGRAM_GROUP_CHAT_ID`
- `reply_to`: `$TELEGRAM_TOPIC_ID`
- `text`: the message above (Markdown enabled)

If `TELEGRAM_GROUP_CHAT_ID` is empty, skip the message and print the reading info to the console instead.

Stop here. No checkpoint needed.

**If activity is GAME**, initialise the checkpoint and proceed to Step 3.

**If activity is QUIZ**, also check the very next entry in the schedule:
- If that next entry's `activity` is `PRESENTATION`, store it as the **paired PRESENTATION**:
  `pres_date`, `pres_teens_passage`, `pres_preteens_passage`
- Announce: "QUIZ + PRESENTATION pair detected — generating both in one run."
- Generate QUIZ content (Steps 4–5), then immediately generate PRESENTATION content
  (Steps 4–5 again for the paired date) before sending the Telegram notification.
  The Telegram message covers both Sundays.

**If activity is PRESENTATION**, initialise the checkpoint and proceed to Step 3.

For any active activity, initialise the checkpoint:
```bash
python3 .claude/skills/tod-generate/scripts/checkpoint.py init \
  [DATE] [ACTIVITY] "[TEENS_PASSAGE]" "[PRETEENS_PASSAGE]"
```

Then mark rotation done:
```bash
python3 .claude/skills/tod-generate/scripts/checkpoint.py set rotation_lookup done
```

---

## STEP 3 — Generate & build Teens content

Skip any sub-step already marked `done` in the checkpoint.

Set the Node path once before running any scripts:
```bash
export NODE_PATH=$(npm root -g)
SKILL=".claude/skills/tod-generate/scripts"
OUTDIR="content/teens/[DATE]_[ACTIVITY]_[TEENS_PASSAGE_NO_SPACES]"
mkdir -p "$OUTDIR" /tmp/tod_specs/teens
```

> NocoDB credentials (`NOCODB_BASE_URL`, `NOCODB_BASE_ID`, `NOCODB_TABLE_ID`) are already in `.env`
> and sourced in Step 0. `nocodb_upload.py` reads them directly — no extra setup needed.
> To recreate the table if ever lost, see git history of this SKILL.md (before 2026-05-07).

### Conservative biblical framing — applies to all content
All answers must reflect clear, orthodox Christian truth. No ambiguous or relativistic framing.
Correct answers are definitively correct. Applications are practical and faith-affirming for teens.

---

### 3a — Write the JSON spec   (checkpoint: `teens_spec_written`)

Produce the JSON spec below for the active activity type.

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
      "topic_title": "[First half of passage — topic title]",
      "summary": "[2-3 sentences covering the first half of the chapter]",
      "verses": "[e.g. Acts 22:1-16]",
      "questions": [
        "What happened? (narrative)",
        "Why did [key character] act this way? (motivation)",
        "What does this reveal about God or faith? (principle)",
        "How does this apply to your life as a teen? (application)"
      ],
      "principle": "[Spiritual truth from first half — 1-2 sentences]",
      "members": ["Member 1","Member 2","Member 3"]
    },
    {
      "topic_title": "[Second half of passage — topic title]",
      "summary": "[2-3 sentences covering the second half of the chapter]",
      "verses": "[e.g. Acts 22:17-30]",
      "questions": [
        "What happened? (narrative)",
        "Why did [key character] act this way? (motivation)",
        "What does this reveal about God or faith? (principle)",
        "How does this apply to your life as a teen? (application)"
      ],
      "principle": "[Spiritual truth from second half — 1-2 sentences]",
      "members": ["Member 4","Member 5","Member 6"]
    }
  ],
  "closing_remarks": "[Pre-filled facilitator closing connecting both sections]",
  "discussion_questions": ["...","...","..."]
}
```
Split the chapter roughly in half by verse count. Group 1 covers the first half, Group 2 the second half.

After writing the spec, checkpoint it:
```bash
python3 $SKILL/checkpoint.py set teens_spec_written done
```

---

### 3b — Build Word documents   (checkpoint: `teens_docx_built`)

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
  "$OUTDIR/Presentation_Teens_[PASSAGE].docx"
python3 $SKILL/checkpoint.py add-file teens \
  "Presentation_Teens_[PASSAGE].docx" \
  "$OUTDIR/Presentation_Teens_[PASSAGE].docx" PRESENTATION
```

Checkpoint:
```bash
python3 $SKILL/checkpoint.py set teens_docx_built done
```

---

### 3c — Upload to NocoDB   (checkpoint: `teens_nocodb_uploaded`)

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

## STEP 4 — Generate & build Pre-Teens content

Repeat the same sub-steps (4a, 4b, 4c) as Step 3 with these differences:
- `"cohort": "PRE-TEENS"` in the JSON spec
- Spec files: `/tmp/tod_specs/preteens/`
- Output folder: `content/preteens/[DATE]_[ACTIVITY]_[PRETEENS_PASSAGE_NO_SPACES]/`
- File names: `Preteens` instead of `Teens`
- Checkpoint keys: `preteens_spec_written`, `preteens_docx_built`, `preteens_nocodb_uploaded`
- Upload flag: `--cohort PRE-TEENS`
- PRESENTATION: same 2-group structure, single combined .docx named `Presentation_Preteens_[PASSAGE].docx`

**Language adjustments for ages 9-12:**
- Simpler vocabulary — no jargon without a plain-English explanation beside it
- Questions lean narrative over analytical
- Application examples from school, home, friendships
- Hard questions are still substantive, just in plainer language than the Teens version

---

## STEP 5 — Telegram notification   (checkpoint: `telegram_sent`)

Read `$TELEGRAM_GROUP_CHAT_ID` and `$TELEGRAM_TOPIC_ID` from the environment (sourced from
`.env` in Step 0).
Read `.claude/checkpoint.json` → collect all `download_url` values from `files.teens` and
`files.preteens`.

Build the file links block (one line per file, all Sundays combined):
```
• [Teens – QUIZ] Quiz_Teens_Variant_A_Acts21.docx → https://...
• [Pre-Teens – QUIZ] Quiz_Preteens_Variant_A_John8.docx → https://...
• [Teens – PRESENTATION] Presentation_Teens_Acts22.docx → https://...
• [Pre-Teens – PRESENTATION] Presentation_Preteens_John9.docx → https://...
```

Fill `completion_message_template` from `config/settings.json → telegram.completion_message_template` with:
- `{date}` → primary Sunday date formatted as "24 May 2026"
- `{activity}` → for a single run: e.g. "GAME"; for a paired run: "QUIZ + PRESENTATION"
- `{teens_passage}` → primary Teens passage (e.g. "Acts 21")
- `{preteens_passage}` → primary Pre-Teens passage (e.g. "John 8")
- `{file_links}` → the bullet list built above (covers all generated files)

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

## STEP 6 — Final summary

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

[If QUIZ+PRESENTATION pair was generated, repeat the block above for the PRESENTATION date]

📲  Telegram: [sent | skipped — no chat_id]

[PRESENTATION only]
📋  Reminder: Distribute Presentation docs to groups by [PRESENTATION DATE − 7 days]
    (i.e. the Sunday before — quiz day — so groups have a full week to prepare).
```

---

## STEP 7 — Commit & push any changes

After the final summary, check for uncommitted changes and push them to the remote branch:

```bash
git status
```

If there are modified or untracked files (e.g. updated `package.json` from `npm install`):

```bash
# Stage only relevant files — never commit .env or node_modules
git add .claude/skills/tod-generate/scripts/package.json \
        .claude/skills/tod-generate/scripts/package-lock.json
# Add any other legitimately changed tracked files
git add -u

git commit -m "chore(tod-generate): pipeline run [DATE] — [ACTIVITY]"

git push -u origin <current-branch>
```

**If `git push` returns 403 ("Permission denied"):**
The cloud session's git token doesn't have write access. The fix is to run
`/web-setup` in your local terminal once — this syncs your `gh` CLI token to
your Claude account and the proxy picks it up automatically from the next session.
No env variable is needed for git; `GH_TOKEN` only affects the `gh` CLI, not `git push`.

After a successful push, create a draft PR if one doesn't already exist:
```bash
# The remote prints a PR URL on push — open it, or use the GitHub MCP tool
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

- [ ] 5 narrative sections with titles and exact verse ranges (GAME/QUIZ)
- [ ] Biblical answers reflect orthodox Christian understanding throughout
- [ ] Quiz variants are genuinely different (not paraphrases)
- [ ] Quiz correct answers spread across A/B/C/D
- [ ] Game phrases are near-exact Scripture quotes
- [ ] Presentation has exactly 2 groups — Group 1 covers first half, Group 2 second half
- [ ] Presentation builds a single combined .docx (group table + guideline in one file)
- [ ] Pre-Teens content uses noticeably simpler language
- [ ] All Word docs built without errors (check node output)
- [ ] All files uploaded to NocoDB (check checkpoint)
- [ ] Checkpoint shows all steps `done` before finishing
- [ ] If QUIZ+PRESENTATION pair: both Sundays fully generated before Telegram is sent
