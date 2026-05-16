#!/usr/bin/env node
/**
 * TOD Game Sunday — Word Document Builder
 * Usage: node build_game.js <spec.json> <output.docx>
 *
 * Spec JSON shape:
 * {
 *   "title": "GAME SUNDAY",
 *   "passage": "Acts 20", "extra": "Psalms 19:7-11",
 *   "date": "2026-05-10", "cohort": "TEENS",
 *   "church": "RCCG Tabernacle of David (TOD)",
 *   "principle": "...",
 *   "sections": [{ "title": "...", "verses": "Acts 20:1-6" }, ...x5],
 *   "round1": [{ "section": "1", "phrase": "...", "reference": "..." }, ...x5],
 *   "round2": [{ "section": "1", "question": "...", "answer": "..." }, ...x5],
 *   "round3": [{ "section": "1", "statement": "...", "answer": "TRUE|FALSE", "explanation": "..." }, ...x5],
 *   "closing": "..."
 * }
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
  WidthType, ShadingType, VerticalAlign, PageNumber, LevelFormat,
} = require("docx");

const spec = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const outputPath = process.argv[3];

// ── Colours ──────────────────────────────────────────────────────────────────
const NAVY  = "1A376E";
const GOLD  = "B88600";
const LIGHT = "EEF2FF";
const WHITE = "FFFFFF";
const GREY  = "666666";

// ── Helpers ───────────────────────────────────────────────────────────────────
const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const allBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const cellPad = { top: 100, bottom: 100, left: 140, right: 140 };

function spacer(pts = 6) {
  return new Paragraph({ children: [new TextRun("")], spacing: { before: pts * 20, after: 0 } });
}

function rule() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "CCCCCC", space: 1 } },
    spacing: { before: 40, after: 40 },
    children: [],
  });
}

function sectionHeading(text) {
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), bold: true, color: NAVY, size: 24, font: "Calibri" })],
    spacing: { before: 200, after: 80 },
  });
}

function bodyText(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, size: 20, font: "Calibri", bold: opts.bold, color: opts.color })],
    spacing: { before: 20, after: 60 },
  });
}

function headerRow(cells) {
  return new TableRow({
    tableHeader: true,
    children: cells.map((text, i) => new TableCell({
      borders: allBorders,
      shading: { fill: NAVY, type: ShadingType.CLEAR },
      margins: cellPad,
      children: [new Paragraph({
        children: [new TextRun({ text, bold: true, color: WHITE, size: 18, font: "Calibri" })],
      })],
    })),
  });
}

function dataRow(cells, rowIndex) {
  const fill = rowIndex % 2 === 0 ? LIGHT : WHITE;
  return new TableRow({
    children: cells.map(text => new TableCell({
      borders: allBorders,
      shading: { fill, type: ShadingType.CLEAR },
      margins: cellPad,
      children: [new Paragraph({
        children: [new TextRun({ text: String(text), size: 18, font: "Calibri" })],
      })],
    })),
  });
}

function makeTable(headers, rows, columnWidths) {
  const totalWidth = columnWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths,
    rows: [
      headerRow(headers),
      ...rows.map((row, i) => dataRow(row, i)),
    ],
  });
}

// ── Document header ───────────────────────────────────────────────────────────
function docHeader() {
  const passage = spec.extra ? `${spec.passage}  +  ${spec.extra}` : spec.passage;
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: (spec.church || "RCCG TABERNACLE OF DAVID (TOD)").toUpperCase(), bold: true, color: NAVY, size: 20, font: "Calibri" })],
      spacing: { after: 0 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: spec.title, bold: true, color: NAVY, size: 36, font: "Calibri" })],
      spacing: { before: 40, after: 40 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: passage, bold: true, color: GOLD, size: 26, font: "Calibri" })],
      spacing: { after: 40 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `${spec.date}  |  ${spec.cohort}`, color: GREY, size: 18, font: "Calibri" })],
      spacing: { after: 80 },
    }),
    rule(),
  ];
}

// ── Build document ────────────────────────────────────────────────────────────
const children = [
  ...docHeader(),

  // Principle
  sectionHeading("Overarching Biblical Principle"),
  bodyText(spec.principle, { bold: false }),
  spacer(8),

  // Narrative sections
  sectionHeading("5 Narrative Sections"),
  ...(spec.sections || []).map((s, i) => new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    children: [
      new TextRun({ text: `${s.title}  `, bold: true, size: 20, font: "Calibri" }),
      new TextRun({ text: s.verses, color: GREY, size: 20, font: "Calibri" }),
    ],
    spacing: { before: 20, after: 20 },
  })),
  spacer(12),

  // Round 1
  sectionHeading("Round 1: Find & Quote  (15 minutes)"),
  bodyText("Teams race to find the phrase and quote the exact verse reference.", { color: GREY }),
  makeTable(
    ["Section", "Phrase to Find", "Reference"],
    (spec.round1 || []).map(r => [r.section, r.phrase, r.reference]),
    [700, 5600, 1460]
  ),
  spacer(12),

  // Round 2
  sectionHeading("Round 2: Comprehension  (15 minutes)"),
  bodyText("One deep question per section. Teams discuss, then answer.", { color: GREY }),
  makeTable(
    ["Section", "Question", "Biblical Answer Guide"],
    (spec.round2 || []).map(r => [r.section, r.question, r.answer]),
    [700, 3500, 3560]
  ),
  spacer(12),

  // Round 3
  sectionHeading("Round 3: Binary Jump  (15 minutes)"),
  bodyText("Everyone jumps RIGHT (True) or LEFT (False).", { color: GREY }),
  makeTable(
    ["Section", "Statement", "Answer", "Explanation"],
    (spec.round3 || []).map(r => [r.section, r.statement, r.answer, r.explanation]),
    [700, 3600, 900, 2560]
  ),
  spacer(12),

  // Closing
  sectionHeading("Final Discussion & Closing  (2 minutes)"),
  bodyText(spec.closing),
];

const doc = new Document({
  numbering: {
    config: [{
      reference: "numbers",
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, bottom: 1080, left: 1260, right: 1260 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: `TOD Teens Church  |  Game Sunday  |  ${spec.passage}`, color: GREY, size: 16, font: "Calibri" })],
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

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outputPath, buf);
  console.log(`Saved: ${outputPath}`);
});
