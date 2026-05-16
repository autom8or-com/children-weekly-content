# Graph Report - /Users/HP/children-content/.claude/skills/tod-generate  (2026-05-09)

## Corpus Check
- Corpus is ~6,268 words - fits in a single context window. You may not need a graph.

## Summary
- 82 nodes · 158 edges · 8 communities detected
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Checkpoint State Machine|Checkpoint State Machine]]
- [[_COMMUNITY_Activity Types & Document Builders|Activity Types & Document Builders]]
- [[_COMMUNITY_Biblical Framing & Church Config|Biblical Framing & Church Config]]
- [[_COMMUNITY_Presentation Doc Builder|Presentation Doc Builder]]
- [[_COMMUNITY_Game Doc Builder|Game Doc Builder]]
- [[_COMMUNITY_Secrets, NocoDB & Resume Logic|Secrets, NocoDB & Resume Logic]]
- [[_COMMUNITY_NocoDB Upload Pipeline|NocoDB Upload Pipeline]]
- [[_COMMUNITY_Quiz Doc Builder|Quiz Doc Builder]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 10 edges
2. `TOD Sunday Content Generator Skill` - 10 edges
3. `_load()` - 8 edges
4. `_save()` - 7 edges
5. `Step 2 — Rotation Lookup and Checkpoint Init` - 7 edges
6. `Step 4 — Generate and Build Teens Content` - 7 edges
7. `checkpoint.py Script` - 7 edges
8. `buildGuideline()` - 5 edges
9. `cmd_init()` - 5 edges
10. `cmd_set()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `TOD Sunday Content Generator Skill` --references--> `Step 0 — Resume Check`  [EXTRACTED]
  SKILL.md → SKILL.md  _Bridges community 2 → community 5_
- `TOD Sunday Content Generator Skill` --references--> `Step 2 — Rotation Lookup and Checkpoint Init`  [EXTRACTED]
  SKILL.md → SKILL.md  _Bridges community 2 → community 1_
- `Step 2 — Rotation Lookup and Checkpoint Init` --calls--> `checkpoint.py Script`  [EXTRACTED]
  SKILL.md → SKILL.md  _Bridges community 1 → community 5_

## Hyperedges (group relationships)
- **TOD Content Generation Pipeline** — skill_md_step0_resume_check, skill_md_step1_find_target_sunday, skill_md_step2_rotation_lookup, skill_md_step4_teens_content, skill_md_step5_preteens_content, skill_md_step6_telegram_notification, skill_md_step7_final_summary [EXTRACTED 1.00]
- **Word Document Build Scripts** — skill_md_build_game_js, skill_md_build_quiz_js, skill_md_build_presentation_js [EXTRACTED 1.00]
- **Activity Types Handled** — skill_md_activity_game, skill_md_activity_quiz, skill_md_activity_presentation, skill_md_activity_skipped [EXTRACTED 1.00]
- **Church Cohorts** — skill_md_teens_cohort, skill_md_preteens_cohort [EXTRACTED 1.00]
- **Configuration Files** — skill_md_rotation_json, skill_md_settings_json, skill_md_env_file [EXTRACTED 1.00]

## Communities

### Community 0 - "Checkpoint State Machine"
Cohesion: 0.48
Nodes (12): cmd_add_file(), cmd_clear(), cmd_get(), cmd_init(), cmd_set(), cmd_set_url(), cmd_show(), cmd_status() (+4 more)

### Community 1 - "Activity Types & Document Builders"
Cohesion: 0.23
Nodes (12): GAME Activity Type, PRESENTATION Activity Type, QUIZ Activity Type, SKIPPED/MESSAGE Activity Type, build_game.js Script, build_presentation.js Script, build_quiz.js Script, Rationale: Quiz Difficulty and Answer Distribution Rules (+4 more)

### Community 2 - "Biblical Framing & Church Config"
Cohesion: 0.23
Nodes (12): Conservative Biblical Framing Principle, Pre-Teens Cohort (Ages 9-12), Quality Checks Checklist, Rationale: Simpler Language for Pre-Teens, RCCG Tabernacle of David (TOD) Teens Church, Step 1 — Find Target Sunday, Step 3 — NocoDB Table Setup (Already Done), Step 4 — Generate and Build Teens Content (+4 more)

### Community 3 - "Presentation Doc Builder"
Cohesion: 0.44
Nodes (8): body(), buildGroups(), buildGuideline(), bullet(), label(), numbered(), rule(), sectionHeading()

### Community 4 - "Game Doc Builder"
Cohesion: 0.4
Nodes (8): bodyText(), dataRow(), docHeader(), headerRow(), makeTable(), rule(), sectionHeading(), spacer()

### Community 5 - "Secrets, NocoDB & Resume Logic"
Cohesion: 0.29
Nodes (10): checkpoint.py Script, .env Secrets File, NocoDB tod_content_library Table, nocodb_upload.py Script, Rationale: Resume from Checkpoint on Interruption, config/settings.json Config File, Step 0 — Resume Check, Step 4c — Upload Teens Files to NocoDB (+2 more)

### Community 6 - "NocoDB Upload Pipeline"
Cohesion: 0.46
Nodes (6): create_record(), load_settings(), main(), Create a record in the content library table. Returns the record ID., Upload file to NocoDB storage. Returns the download URL., upload_file()

### Community 7 - "Quiz Doc Builder"
Cohesion: 0.73
Nodes (4): buildKeysDoc(), buildVariantDoc(), rule(), sectionHeading()

## Knowledge Gaps
- **12 isolated node(s):** `Upload file to NocoDB storage. Returns the download URL.`, `Create a record in the content library table. Returns the record ID.`, `Step 1 — Find Target Sunday`, `Step 3 — NocoDB Table Setup (Already Done)`, `Step 7 — Final Summary` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TOD Sunday Content Generator Skill` connect `Biblical Framing & Church Config` to `Activity Types & Document Builders`, `Secrets, NocoDB & Resume Logic`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `Step 2 — Rotation Lookup and Checkpoint Init` connect `Activity Types & Document Builders` to `Biblical Framing & Church Config`, `Secrets, NocoDB & Resume Logic`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Step 4 — Generate and Build Teens Content` connect `Biblical Framing & Church Config` to `Activity Types & Document Builders`, `Secrets, NocoDB & Resume Logic`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **What connects `Upload file to NocoDB storage. Returns the download URL.`, `Create a record in the content library table. Returns the record ID.`, `Step 1 — Find Target Sunday` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._