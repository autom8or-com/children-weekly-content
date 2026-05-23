#!/usr/bin/env node
/**
 * TOD Presentation Sunday — Word Document Builder
 * Builds a single combined document: group assignments table + full guideline.
 *
 * Usage:
 *   node build_presentation.js <spec.json> <output.docx>
 *
 * Spec JSON shape:
 * {
 *   "title": "PRESENTATION SUNDAY",
 *   "passage": "Acts 22", "extra": "Psalms 19:7-11",
 *   "date": "2026-05-24", "cohort": "TEENS",
 *   "church": "RCCG Tabernacle of David (TOD)",
 *   "groups": [
 *     {
 *       "topic_title": "...", "summary": "...", "verses": "Acts 22:1-11",
 *       "questions": ["...", "...", "...", "..."],
 *       "principle": "...",
 *       "members": ["Member 1", "Member 2", "Member 3"]
 *     },
 *     ...2 groups total
 *   ],
 *   "closing_remarks": "...",
 *   "discussion_questions": ["...", "...", "..."]
 * }
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageNumber, LevelFormat, PageBreak,
} = require("docx");

const spec    = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const outPath = process.argv[3];
const docType = (process.argv[4] || "GUIDELINE").toUpperCase();

const NAVY  = "1A376E";
const GOLD  = "B88600";
const WHITE = "FFFFFF";
const GREY  = "888888";
const LIGHT = "EEF2FF";
const DARKGREY = "555555";

const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const allBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };

function rule() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "CCCCCC", space: 1 } },
    spacing: { before: 40, after: 60 },
    children: [],
  });
}

function sectionHeading(text) {
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), bold: true, color: NAVY, size: 22, font: "Calibri" })],
    spacing: { before: 200, after: 80 },
  });
}

function label(text) {
  return new Paragraph({
    children: [new TextRun({ text, bold: true, size: 20, font: "Calibri", color: DARKGREY })],
    spacing: { before: 120, after: 40 },
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, size: 20, font: "Calibri", color: opts.color })],
    spacing: { before: 20, after: 40 },
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, size: 20, font: "Calibri" })],
    spacing: { before: 20, after: 20 },
  });
}

function numbered(text) {
  return new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    children: [new TextRun({ text, size: 20, font: "Calibri" })],
    spacing: { before: 20, after: 20 },
  });
}

// ── Combined document (group assignments table + full guideline) ──────────────

function buildCombined() {
  const passage = spec.extra ? `${spec.passage}  +  ${spec.extra}` : spec.passage;

  // Group assignments table
  const tableHeaderRow = new TableRow({
    tableHeader: true,
    children: ["Group", "Members", "Assigned Topic", "Verses"].map(h => new TableCell({
      borders: allBorders,
      shading: { fill: NAVY, type: ShadingType.CLEAR },
      margins: { top: 100, bottom: 100, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: WHITE, size: 18, font: "Calibri" })] })],
    })),
  });

  const tableDataRows = (spec.groups || []).map((g, i) => new TableRow({
    children: [
      `Group ${i + 1}`,
      (g.members || []).join(", "),
      g.topic_title,
      g.verses || "",
    ].map((text, colIdx) => new TableCell({
      borders: allBorders,
      shading: { fill: i % 2 === 0 ? LIGHT : WHITE, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      width: { size: [700, 2800, 3000, 1800][colIdx], type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, size: 18, font: "Calibri" })] })],
    })),
  }));

  const children = [
    // Church header
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: (spec.church || "").toUpperCase(), bold: true, color: NAVY, size: 18, font: "Calibri" })],
      spacing: { after: 0 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: spec.title, bold: true, color: NAVY, size: 32, font: "Calibri" })],
      spacing: { before: 40, after: 40 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: passage, bold: true, color: GOLD, size: 22, font: "Calibri" })],
      spacing: { after: 40 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `Sunday ${spec.date}  |  ${spec.cohort}`, color: GREY, size: 18, font: "Calibri" })],
      spacing: { after: 80 },
    }),
    rule(),

    // Group assignments table
    sectionHeading("Group Assignments"),
    new Table({
      width: { size: 9000, type: WidthType.DXA },
      columnWidths: [700, 2800, 3000, 1800],
      rows: [tableHeaderRow, ...tableDataRows],
    }),
    new Paragraph({ children: [], spacing: { before: 80 } }),
    rule(),

    // Important dates
    sectionHeading("Important Dates"),
    body(`Presentation Date:      Sunday ${spec.date}`),
    body(`Preparation Deadline:   Saturday before Sunday (morning of)`),
    body(`Deadline to Contact Facilitator:  By Thursday if you have questions`),
    new Paragraph({ children: [], spacing: { before: 80 } }),

    // Format options
    sectionHeading("4 Presentation Format Options — Choose One"),
    ...[
      ["FORMAT 1: STORYTELLING", "Retell your section in your own words. Make it engaging and clear. Help the audience feel the story. End by connecting to the biblical principle."],
      ["FORMAT 2: CHARACTER ANALYSIS", "Focus on the main character(s) in your section. Analyze WHY they made their choices. Explore their motivations, fears, doubts, or faith. Connect their story to the biblical principle."],
      ["FORMAT 3: PRINCIPLE & APPLICATION", "Identify the biblical principle from your section. Explain what God is teaching through this event. Give a modern teen scenario that shows this principle in action. Help the audience see how it applies to their lives."],
      ["FORMAT 4: Q&A STYLE", "Prepare 2-3 thought-provoking questions about your section. Ask the class to discuss/answer. Guide the discussion toward discovering the biblical principle. Summarize the key truth at the end."],
    ].flatMap(([name, desc]) => [
      new Paragraph({
        children: [
          new TextRun({ text: `${name}: `, bold: true, size: 20, font: "Calibri" }),
          new TextRun({ text: desc, size: 20, font: "Calibri" }),
        ],
        numbering: { reference: "bullets", level: 0 },
        spacing: { before: 40, after: 40 },
      }),
    ]),
    new Paragraph({ children: [], spacing: { before: 80 } }),

    // Expectations
    sectionHeading("What Every Group Must Do"),
    ...[
      "All group members participate — everyone speaks",
      "Quote or reference the Bible passage",
      "Show preparation — it's clear you read and understood your section",
      "Stay within 2-3 minutes",
      "Connect your section to its biblical principle",
    ].map(e => bullet(e)),

    new Paragraph({ children: [new PageBreak()] }),

    // Per-group pages
    ...(spec.groups || []).flatMap((group, i) => [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: `GROUP ${i + 1}`, bold: true, color: WHITE, size: 28, font: "Calibri" })],
        shading: { fill: NAVY, type: ShadingType.CLEAR },
        spacing: { before: 0, after: 0 },
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: group.topic_title, bold: true, color: NAVY, size: 24, font: "Calibri" })],
        spacing: { before: 100, after: 40 },
      }),
      body(`Verses: ${group.verses}`, { color: GOLD }),
      body(`Presentation time: 2-3 minutes  |  Choose your own format`),
      new Paragraph({ children: [], spacing: { before: 60 } }),

      label("WHAT HAPPENS IN THIS SECTION:"),
      body(group.summary),

      label("KEY QUESTIONS YOUR GROUP SHOULD EXPLORE:"),
      ...(group.questions || []).map(q => numbered(q)),

      label("THE BIBLICAL PRINCIPLE:"),
      body(group.principle),

      label("PREPARATION STEPS:"),
      ...[
        "Read the passage together (out loud or silently)",
        "Discuss the key questions as a group",
        "Choose your presentation format",
        "Write out your presentation and practise it",
        "Aim for 2-3 minutes — time yourselves",
        "Arrive early on Sunday ready to present",
      ].map(s => numbered(s)),

      ...(i < (spec.groups || []).length - 1 ? [new Paragraph({ children: [new PageBreak()] })] : []),
    ]),

    new Paragraph({ children: [new PageBreak()] }),

    // Facilitator closing remarks
    sectionHeading("Facilitator: Closing Remarks  (5 minutes)"),
    body(spec.closing_remarks),

    new Paragraph({ children: [], spacing: { before: 80 } }),
    sectionHeading("Facilitator: Discussion Questions  (10 minutes)"),
    ...(spec.discussion_questions || []).map(q => numbered(q)),
  ];

  return new Document({
    numbering: {
      config: [
        {
          reference: "bullets",
          levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
        },
        {
          reference: "numbers",
          levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
        },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 900, bottom: 900, left: 1080, right: 1080 },
        },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            children: [new TextRun({ text: `TOD ${spec.cohort}  |  Presentation Sunday  |  ${spec.passage}`, color: GREY, size: 16, font: "Calibri" })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Page ", color: GREY, size: 16, font: "Calibri" }),
              new TextRun({ children: [PageNumber.CURRENT], color: GREY, size: 16, font: "Calibri" }),
            ],
          })],
        }),
      },
      children,
    }],
  });
}

// ── Run ────────────────────────────────────────────────────────────────────────

const doc = buildCombined();
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log(`Saved: ${outPath}`);
});
