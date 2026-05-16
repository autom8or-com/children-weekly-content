#!/usr/bin/env node
/**
 * TOD Quiz Sunday — Word Document Builder
 * Builds ONE variant document OR the unified answer keys document.
 *
 * Usage:
 *   node build_quiz.js <spec.json> <output.docx> [variant]
 *   variant: A | B | C | KEYS   (default: A)
 *
 * Spec JSON shape:
 * {
 *   "title": "QUIZ SUNDAY",
 *   "passage": "Acts 21", "extra": "Psalms 19:7-11",
 *   "date": "2026-05-17", "cohort": "TEENS",
 *   "church": "RCCG Tabernacle of David (TOD)",
 *   "variant_a": [
 *     { "question": "...", "options": { "A": "...", "B": "...", "C": "...", "D": "..." }, "correct": "B" },
 *     ...30 items
 *   ],
 *   "variant_b": [ ...30 different items ],
 *   "variant_c": [ ...30 different items ]
 * }
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageNumber, LevelFormat,
} = require("docx");

const spec    = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const outPath = process.argv[3];
const variant = (process.argv[4] || "A").toUpperCase();

const NAVY  = "1A376E";
const GOLD  = "B88600";
const WHITE = "FFFFFF";
const GREY  = "888888";
const LIGHT = "F4F6FF";

const thinBorder = { style: BorderStyle.SINGLE, size: 1, color: "DDDDDD" };
const allBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };
const noBorder   = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders  = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function rule() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "CCCCCC", space: 1 } },
    spacing: { before: 40, after: 40 },
    children: [],
  });
}

function sectionHeading(text) {
  return new Paragraph({
    children: [new TextRun({ text: text.toUpperCase(), bold: true, color: NAVY, size: 22, font: "Calibri" })],
    spacing: { before: 200, after: 80 },
  });
}

// ── Variant document ──────────────────────────────────────────────────────────

function buildVariantDoc(variantLetter) {
  const key = `variant_${variantLetter.toLowerCase()}`;
  const questions = spec[key] || [];
  const passage   = spec.extra ? `${spec.passage}  +  ${spec.extra}` : spec.passage;

  // Header block
  const headerBlock = [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: (spec.church || "").toUpperCase(), bold: true, color: NAVY, size: 18, font: "Calibri" })],
      spacing: { after: 0 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `${spec.title} — VARIANT ${variantLetter}`, bold: true, color: NAVY, size: 32, font: "Calibri" })],
      spacing: { before: 40, after: 40 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: passage, bold: true, color: GOLD, size: 22, font: "Calibri" })],
      spacing: { after: 60 },
    }),
    // Name / date line
    new Paragraph({
      children: [
        new TextRun({ text: "Name: ________________________________    Date: _____________    Score: _____ / 30", size: 18, font: "Calibri" }),
      ],
      spacing: { after: 40 },
    }),
    new Paragraph({
      children: [new TextRun({ text: "Instructions: Answer all 30 questions. You may reference the Bible passage provided.", size: 16, font: "Calibri", color: GREY })],
      spacing: { after: 20 },
    }),
    rule(),
  ];

  // Split questions into two columns of 15 each
  const col1 = questions.slice(0, 15);   // Q1-Q15
  const col2 = questions.slice(15, 30);  // Q16-Q30
  const rows = Math.max(col1.length, col2.length);

  function questionCell(q, qNum) {
    if (!q) return new TableCell({ borders: noBorders, children: [new Paragraph({ children: [] })] });

    const optionLetters = ["A", "B", "C", "D"];
    return new TableCell({
      borders: allBorders,
      shading: { fill: qNum % 2 === 0 ? LIGHT : WHITE, type: ShadingType.CLEAR },
      margins: { top: 120, bottom: 120, left: 160, right: 160 },
      width: { size: 4500, type: WidthType.DXA },
      children: [
        new Paragraph({
          children: [new TextRun({ text: `${qNum}. ${q.question}`, bold: true, size: 18, font: "Calibri" })],
          spacing: { after: 40 },
        }),
        ...optionLetters.map(letter => new Paragraph({
          children: [new TextRun({ text: `    ${letter})  ${q.options[letter]}`, size: 17, font: "Calibri" })],
          spacing: { before: 10, after: 10 },
        })),
        new Paragraph({
          children: [new TextRun({ text: `[Variant: ${variantLetter}]`, size: 14, font: "Calibri", color: "BBBBBB" })],
          spacing: { before: 30, after: 0 },
        }),
      ],
    });
  }

  const tableRows = [];
  for (let i = 0; i < rows; i++) {
    tableRows.push(new TableRow({
      children: [
        questionCell(col1[i], i + 1),
        new TableCell({ borders: noBorders, width: { size: 200, type: WidthType.DXA }, children: [new Paragraph({ children: [] })] }),
        questionCell(col2[i], i + 16),
      ],
    }));
  }

  const questionsTable = new Table({
    width: { size: 9200, type: WidthType.DXA },
    columnWidths: [4500, 200, 4500],
    rows: tableRows,
  });

  return new Document({
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
            children: [new TextRun({ text: `TOD Teens Church  |  Quiz Sunday  |  ${spec.passage}  |  Variant ${variantLetter}`, color: GREY, size: 16, font: "Calibri" })],
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
      children: [...headerBlock, questionsTable],
    }],
  });
}

// ── Answer keys document ──────────────────────────────────────────────────────

function buildKeysDoc() {
  const passage = spec.extra ? `${spec.passage}  +  ${spec.extra}` : spec.passage;

  const children = [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: (spec.church || "").toUpperCase(), bold: true, color: NAVY, size: 18, font: "Calibri" })],
      spacing: { after: 0 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: `${spec.title} — ANSWER KEYS`, bold: true, color: NAVY, size: 32, font: "Calibri" })],
      spacing: { before: 40, after: 40 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: passage, bold: true, color: GOLD, size: 22, font: "Calibri" })],
      spacing: { after: 60 },
    }),
    new Paragraph({
      children: [new TextRun({ text: "FACILITATOR ONLY — Do not distribute to students.", bold: true, color: "CC0000", size: 20, font: "Calibri" })],
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
    }),
    rule(),
  ];

  for (const variantLetter of ["A", "B", "C"]) {
    const questions = spec[`variant_${variantLetter.toLowerCase()}`] || [];
    children.push(sectionHeading(`Variant ${variantLetter}`));

    // 3-column answer grid
    const cols = [[], [], []];
    questions.forEach((q, i) => cols[i % 3].push(`Q${i + 1}:  ${q.correct}`));

    const maxRows = Math.max(...cols.map(c => c.length));
    const gridRows = [];
    for (let r = 0; r < maxRows; r++) {
      gridRows.push(new TableRow({
        children: cols.map(col => new TableCell({
          borders: allBorders,
          shading: { fill: r % 2 === 0 ? LIGHT : WHITE, type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          width: { size: 3000, type: WidthType.DXA },
          children: [new Paragraph({
            children: [new TextRun({ text: col[r] || "", size: 20, font: "Calibri" })],
          })],
        })),
      }));
    }

    children.push(
      new Table({ width: { size: 9000, type: WidthType.DXA }, columnWidths: [3000, 3000, 3000], rows: gridRows }),
      new Paragraph({ children: [], spacing: { before: 120, after: 0 } })
    );
  }

  return new Document({
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 900, bottom: 900, left: 1080, right: 1080 },
        },
      },
      children,
    }],
  });
}

// ── Run ────────────────────────────────────────────────────────────────────────

const doc = variant === "KEYS" ? buildKeysDoc() : buildVariantDoc(variant);
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outPath, buf);
  console.log(`Saved: ${outPath}`);
});
