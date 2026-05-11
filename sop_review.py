#!/usr/bin/env python3
"""
sop_review.py — AI-powered SOP compliance review tool for 21 CFR 820.

Submits a Standard Operating Procedure text to Claude and generates a
color-coded PDF report indicating compliance status for each checklist item.

Usage:
    python sop_review.py --file sample_sop.txt --sop-type cleaning --device-class II
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic
import pdfplumber
from docx import Document
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# 21 CFR 820 COMPLIANCE CHECKLIST
# ---------------------------------------------------------------------------

UNIVERSAL_CHECKLIST: list[dict] = [
    {
        "id": "U01",
        "item": "Purpose Statement",
        "description": "1–2 sentences, specific to process",
        "regulation": "21 CFR 820.40",
    },
    {
        "id": "U02",
        "item": "Scope",
        "description": "What processes, equipment, and personnel are covered",
        "regulation": "21 CFR 820.40",
    },
    {
        "id": "U03",
        "item": "Responsibilities",
        "description": "Who performs, who reviews, who approves",
        "regulation": "21 CFR 820.20(b)",
    },
    {
        "id": "U04",
        "item": "References",
        "description": "Regulatory, standards, and related documents cited",
        "regulation": "21 CFR 820.40",
    },
    {
        "id": "U05",
        "item": "Definitions / Abbreviations",
        "description": "Key terms and acronyms defined",
        "regulation": "21 CFR 820.3",
    },
    {
        "id": "U06",
        "item": "Materials and Equipment List",
        "description": "All materials, reagents, and equipment enumerated",
        "regulation": "21 CFR 820.70(g)",
    },
    {
        "id": "U07",
        "item": "Safety Precautions / PPE Requirements",
        "description": "Hazards identified, appropriate PPE specified",
        "regulation": "21 CFR 820.70(e)",
    },
    {
        "id": "U08",
        "item": "Step-by-Step Procedure",
        "description": "Numbered steps using action-verb format",
        "regulation": "21 CFR 820.40",
    },
    {
        "id": "U09",
        "item": "Documentation / Forms / Records",
        "description": "Forms to complete and records to retain specified",
        "regulation": "21 CFR 820.180",
    },
    {
        "id": "U10",
        "item": "Revision History Table",
        "description": "Version, date, author, and change summary tracked",
        "regulation": "21 CFR 820.40(b)",
    },
    {
        "id": "U11",
        "item": "Approval Signatures Block",
        "description": "Signature lines for author, reviewer, and approver",
        "regulation": "21 CFR 820.40(a)",
    },
]

TYPE_SPECIFIC_CHECKLIST: dict[str, list[dict]] = {
    "manufacturing": [
        {
            "id": "M01",
            "item": "Environmental Conditions",
            "description": "Cleanroom class, temperature, and humidity limits specified",
            "regulation": "21 CFR 820.70(c)",
        },
        {
            "id": "M02",
            "item": "In-Process Inspection Checkpoints",
            "description": "Inspection hold points identified within the process",
            "regulation": "21 CFR 820.70(a)",
        },
        {
            "id": "M03",
            "item": "Non-Conformance Reporting Procedure",
            "description": "Steps to identify, segregate, and report non-conforming product",
            "regulation": "21 CFR 820.90",
        },
        {
            "id": "M04",
            "item": "Equipment Qualification Reference",
            "description": "IQ/OQ/PQ documentation or reference cited",
            "regulation": "21 CFR 820.70(g)",
        },
    ],
    "calibration": [
        {
            "id": "C01",
            "item": "Calibration Interval Justification",
            "description": "Frequency of calibration and rationale documented",
            "regulation": "21 CFR 820.72(a)",
        },
        {
            "id": "C02",
            "item": "NIST Traceability Statement",
            "description": "Traceable to national or international standards stated",
            "regulation": "21 CFR 820.72(b)",
        },
        {
            "id": "C03",
            "item": "Out-of-Calibration Response Procedure",
            "description": "Actions when equipment fails calibration defined",
            "regulation": "21 CFR 820.72(a)",
        },
        {
            "id": "C04",
            "item": "Calibration Label Requirements",
            "description": "Label contents and placement requirements specified",
            "regulation": "21 CFR 820.72(b)",
        },
    ],
    "cleaning": [
        {
            "id": "CL01",
            "item": "Cleaning Agent Specifications",
            "description": "Approved cleaning agents, concentrations, and contact times",
            "regulation": "21 CFR 820.70(e)",
        },
        {
            "id": "CL02",
            "item": "Rinse / Residue Verification",
            "description": "Method to verify removal of cleaning agent residue",
            "regulation": "21 CFR 820.70(e)",
        },
        {
            "id": "CL03",
            "item": "Non-Conformance Reporting Procedure",
            "description": "Steps for reporting cleaning failures or deviations",
            "regulation": "21 CFR 820.90",
        },
        {
            "id": "CL04",
            "item": "Cleaning Frequency / Schedule",
            "description": "When and how often cleaning must occur",
            "regulation": "21 CFR 820.70(f)",
        },
    ],
    "inspection": [
        {
            "id": "I01",
            "item": "Acceptance Criteria",
            "description": "Quantitative pass/fail criteria for each inspection attribute",
            "regulation": "21 CFR 820.80(d)",
        },
        {
            "id": "I02",
            "item": "Sampling Plan Reference",
            "description": "AQL level, sampling standard (e.g., ANSI/ASQ Z1.4) cited",
            "regulation": "21 CFR 820.80(c)",
        },
        {
            "id": "I03",
            "item": "Inspection Equipment / Gauges",
            "description": "Measurement instruments and calibration requirements",
            "regulation": "21 CFR 820.72",
        },
        {
            "id": "I04",
            "item": "Disposition Authority",
            "description": "Who is authorized to accept or reject product",
            "regulation": "21 CFR 820.80(a)",
        },
    ],
    "complaint": [
        {
            "id": "CP01",
            "item": "Complaint Intake / Acknowledgment",
            "description": "Timelines and method for acknowledging complaints",
            "regulation": "21 CFR 820.198(a)",
        },
        {
            "id": "CP02",
            "item": "MDR / Reportability Determination",
            "description": "Decision tree or criteria for MDR filing",
            "regulation": "21 CFR 803 / 820.198(d)",
        },
        {
            "id": "CP03",
            "item": "Root Cause Analysis Requirement",
            "description": "Requirement and method for investigating root cause",
            "regulation": "21 CFR 820.198(e)",
        },
        {
            "id": "CP04",
            "item": "CAPA Linkage",
            "description": "Connection to CAPA process if systemic issue identified",
            "regulation": "21 CFR 820.100",
        },
    ],
}

# Device class stringency notes injected into the prompt
CLASS_NOTES: dict[str, str] = {
    "I": (
        "Class I device: General controls apply. "
        "Flag missing items but note that some documentation requirements may be reduced under exemptions."
    ),
    "II": (
        "Class II device: General and special controls apply. "
        "All universal checklist items are mandatory. Treat INCOMPLETE as equivalent to MISSING for scoring."
    ),
    "III": (
        "Class III device: General controls, special controls, and PMA requirements apply. "
        "Apply the highest level of scrutiny. Any gap in documentation is a critical deficiency."
    ),
}

# ---------------------------------------------------------------------------
# FILE READING
# ---------------------------------------------------------------------------


def read_sop_file(file_path: str) -> str:
    """Read SOP content from a .txt or .docx file.

    Args:
        file_path: Absolute or relative path to the SOP file.

    Returns:
        Plain-text content of the SOP.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is unsupported.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"SOP file not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix == ".txt":
        return path.read_text(encoding="utf-8")
    elif suffix == ".docx":
        doc = Document(str(path))
        return "\n".join(para.text for para in doc.paragraphs)
    elif suffix == ".pdf":
        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text(layout=True)
                if text:
                    pages.append(text)
        if not pages:
            raise ValueError(f"No extractable text found in '{file_path}'. The PDF may be scanned/image-only.")
        return "\n\n".join(pages)
    else:
        raise ValueError(f"Unsupported file type '{suffix}'. Use .txt, .docx, or .pdf.")


# ---------------------------------------------------------------------------
# CLAUDE API CALL
# ---------------------------------------------------------------------------


def build_checklist_text(sop_type: str) -> str:
    """Combine universal and type-specific checklist items into a numbered list.

    Args:
        sop_type: One of the supported SOP type keys.

    Returns:
        Formatted checklist string for inclusion in the Claude prompt.
    """
    items = UNIVERSAL_CHECKLIST + TYPE_SPECIFIC_CHECKLIST.get(sop_type, [])
    lines = []
    for item in items:
        lines.append(
            f"[{item['id']}] {item['item']} ({item['regulation']}): {item['description']}"
        )
    return "\n".join(lines)


def call_claude(sop_text: str, sop_type: str, device_class: str) -> str:
    """Send the SOP text and checklist to Claude for compliance review.

    Args:
        sop_text: Full plain-text content of the SOP document.
        sop_type: SOP category (manufacturing, calibration, cleaning, etc.).
        device_class: FDA device class — "I", "II", or "III".

    Returns:
        Raw text response from Claude containing the structured review.

    Raises:
        anthropic.APIError: On any API-level failure.
    """
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    checklist_text = build_checklist_text(sop_type)
    class_note = CLASS_NOTES[device_class]

    system_prompt = (
        "You are a senior FDA compliance specialist with 15 years of medical device "
        "quality system experience. You review SOPs against 21 CFR Part 820 requirements. "
        "Be specific, cite regulation sections, and provide actionable recommendations. "
        "Always respond in the exact JSON format requested — no preamble, no markdown fences."
    )

    user_prompt = f"""Review the following Standard Operating Procedure against the 21 CFR 820 compliance checklist.

DEVICE CLASS: {device_class}
NOTE: {class_note}

SOP TYPE: {sop_type.upper()}

--- SOP TEXT START ---
{sop_text}
--- SOP TEXT END ---

CHECKLIST ITEMS TO EVALUATE:
{checklist_text}

INSTRUCTIONS:
For each checklist item, evaluate whether it is PRESENT, INCOMPLETE, or MISSING in the SOP.
- PRESENT: The requirement is clearly and adequately addressed.
- INCOMPLETE: The requirement is partially addressed but lacks required detail.
- MISSING: The requirement is entirely absent from the SOP.

Respond ONLY with a valid JSON object in this exact structure:
{{
  "overall_status": "READY FOR QA REVIEW" | "NEEDS REVISION" | "MAJOR GAPS",
  "overall_rationale": "<1-2 sentence summary of why you assigned this status>",
  "findings": [
    {{
      "id": "<checklist item ID>",
      "item": "<checklist item name>",
      "regulation": "<regulation section>",
      "status": "PRESENT" | "INCOMPLETE" | "MISSING",
      "evidence": "<quote from SOP that satisfies this item, or 'Not found in SOP'>",
      "recommendation": "<1-2 sentence actionable recommendation, or null if PRESENT>"
    }}
  ]
}}

Do not include any text outside the JSON object."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text


def parse_claude_response(raw: str) -> dict:
    """Parse and validate the JSON response from Claude.

    Args:
        raw: Raw text returned by the Claude API call.

    Returns:
        Parsed Python dict containing overall_status and findings list.

    Raises:
        ValueError: If the response cannot be parsed as valid JSON.
    """
    # Strip any accidental markdown fences
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Claude returned non-JSON output. Raw response:\n{raw}\n\nError: {exc}"
        ) from exc

    required_keys = {"overall_status", "overall_rationale", "findings"}
    if not required_keys.issubset(data.keys()):
        raise ValueError(
            f"Claude response missing required keys. Got: {list(data.keys())}"
        )

    return data


# ---------------------------------------------------------------------------
# PDF REPORT GENERATION
# ---------------------------------------------------------------------------

STATUS_COLORS: dict[str, colors.Color] = {
    "PRESENT": colors.HexColor("#27AE60"),       # green
    "INCOMPLETE": colors.HexColor("#F39C12"),    # amber
    "MISSING": colors.HexColor("#E74C3C"),       # red
}

OVERALL_COLORS: dict[str, colors.Color] = {
    "READY FOR QA REVIEW": colors.HexColor("#27AE60"),
    "NEEDS REVISION": colors.HexColor("#F39C12"),
    "MAJOR GAPS": colors.HexColor("#E74C3C"),
}


def _make_styles() -> dict:
    """Build a dictionary of ReportLab paragraph styles used in the report."""
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontSize=22,
            textColor=colors.HexColor("#1A252F"),
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#5D6D7E"),
            spaceAfter=4,
        ),
        "heading": ParagraphStyle(
            "SectionHeading",
            parent=base["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#1A252F"),
            spaceBefore=14,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
        ),
        "cell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontSize=8,
            leading=11,
            wordWrap="LTR",
        ),
        "cell_bold": ParagraphStyle(
            "TableCellBold",
            parent=base["Normal"],
            fontSize=8,
            leading=11,
            fontName="Helvetica-Bold",
        ),
        "badge": ParagraphStyle(
            "Badge",
            parent=base["Normal"],
            fontSize=18,
            fontName="Helvetica-Bold",
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontSize=7,
            textColor=colors.HexColor("#95A5A6"),
            alignment=TA_CENTER,
        ),
        "rationale": ParagraphStyle(
            "Rationale",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#2C3E50"),
            backColor=colors.HexColor("#EBF5FB"),
            borderPadding=(6, 6, 6, 6),
        ),
    }
    return styles


def _scorecard_table(findings: list[dict], styles: dict) -> Table:
    """Build the summary scorecard table showing pass/fail counts by status.

    Args:
        findings: List of finding dicts from Claude's response.
        styles: Dict of paragraph styles.

    Returns:
        A ReportLab Table object ready to add to the story.
    """
    total = len(findings)
    present = sum(1 for f in findings if f["status"] == "PRESENT")
    incomplete = sum(1 for f in findings if f["status"] == "INCOMPLETE")
    missing = sum(1 for f in findings if f["status"] == "MISSING")

    data = [
        [
            Paragraph("<b>Total Items</b>", styles["cell_bold"]),
            Paragraph("<b>PRESENT</b>", styles["cell_bold"]),
            Paragraph("<b>INCOMPLETE</b>", styles["cell_bold"]),
            Paragraph("<b>MISSING</b>", styles["cell_bold"]),
            Paragraph("<b>Pass Rate</b>", styles["cell_bold"]),
        ],
        [
            Paragraph(str(total), styles["cell"]),
            Paragraph(str(present), styles["cell"]),
            Paragraph(str(incomplete), styles["cell"]),
            Paragraph(str(missing), styles["cell"]),
            Paragraph(f"{present / total * 100:.0f}%", styles["cell"]),
        ],
    ]

    col_width = (7.5 * inch) / 5
    tbl = Table(data, colWidths=[col_width] * 5)
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A252F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (1, 1), (1, 1), colors.HexColor("#D5F5E3")),
                ("BACKGROUND", (2, 1), (2, 1), colors.HexColor("#FDEBD0")),
                ("BACKGROUND", (3, 1), (3, 1), colors.HexColor("#FADBD8")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return tbl


def _findings_table(findings: list[dict], styles: dict) -> Table:
    """Build the detailed findings table.

    Args:
        findings: List of finding dicts from Claude's response.
        styles: Dict of paragraph styles.

    Returns:
        A ReportLab Table object.
    """
    header = [
        Paragraph("<b>ID</b>", styles["cell_bold"]),
        Paragraph("<b>Checklist Item</b>", styles["cell_bold"]),
        Paragraph("<b>Reg. Section</b>", styles["cell_bold"]),
        Paragraph("<b>Status</b>", styles["cell_bold"]),
        Paragraph("<b>Evidence / Gap</b>", styles["cell_bold"]),
        Paragraph("<b>Recommendation</b>", styles["cell_bold"]),
    ]
    rows = [header]
    row_styles: list[tuple] = []

    for i, finding in enumerate(findings, start=1):
        status = finding.get("status", "MISSING")
        status_color = STATUS_COLORS.get(status, colors.grey)
        bg_color = {
            "PRESENT": colors.HexColor("#EAFAF1"),
            "INCOMPLETE": colors.HexColor("#FEF9E7"),
            "MISSING": colors.HexColor("#FDEDEC"),
        }.get(status, colors.white)

        evidence = finding.get("evidence") or "Not found in SOP"
        recommendation = finding.get("recommendation") or "—"

        row_styles.append(("BACKGROUND", (0, i), (-1, i), bg_color))
        row_styles.append(
            ("BACKGROUND", (3, i), (3, i), status_color)
        )
        row_styles.append(("TEXTCOLOR", (3, i), (3, i), colors.white))

        row = [
            Paragraph(finding.get("id", ""), styles["cell_bold"]),
            Paragraph(finding.get("item", ""), styles["cell"]),
            Paragraph(finding.get("regulation", ""), styles["cell"]),
            Paragraph(f"<b>{status}</b>", styles["cell_bold"]),
            Paragraph(evidence[:300] + ("…" if len(evidence) > 300 else ""), styles["cell"]),
            Paragraph(recommendation, styles["cell"]),
        ]
        rows.append(row)

    col_widths = [0.5 * inch, 1.4 * inch, 1.1 * inch, 0.9 * inch, 2.0 * inch, 1.6 * inch]
    tbl = Table(rows, colWidths=col_widths, repeatRows=1)

    base_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A252F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BDC3C7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (3, 1), (3, -1), "CENTER"),
    ]
    tbl.setStyle(TableStyle(base_style + row_styles))
    return tbl


def generate_pdf_report(
    review_data: dict,
    output_path: str,
    sop_filename: str,
    device_class: str,
    sop_type: str,
) -> None:
    """Render the compliance review results as a professional PDF report.

    Args:
        review_data: Parsed dict from Claude containing overall_status and findings.
        output_path: File path where the PDF will be saved.
        sop_filename: Original SOP file name (shown in the report header).
        device_class: FDA device class I / II / III.
        sop_type: SOP category label.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = _make_styles()
    story = []

    # ---- HEADER ----
    story.append(Paragraph("SOP Compliance Review Report", styles["title"]))
    story.append(
        Paragraph(
            f"21 CFR Part 820 — Quality System Regulation",
            styles["subtitle"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A252F")))
    story.append(Spacer(1, 8))

    # Metadata table
    meta_data = [
        ["Date Generated:", datetime.now().strftime("%B %d, %Y  %H:%M UTC")],
        ["SOP File:", sop_filename],
        ["Device Class:", f"Class {device_class}"],
        ["SOP Type:", sop_type.capitalize()],
    ]
    meta_tbl = Table(meta_data, colWidths=[1.5 * inch, 5.5 * inch])
    meta_tbl.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1A252F")),
                ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#5D6D7E")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(meta_tbl)
    story.append(Spacer(1, 14))

    # ---- OVERALL GMP READINESS BADGE ----
    overall_status = review_data["overall_status"]
    badge_color = OVERALL_COLORS.get(overall_status, colors.grey)

    story.append(Paragraph("Overall GMP Readiness", styles["heading"]))

    badge_data = [[Paragraph(overall_status, styles["badge"])]]
    badge_tbl = Table(badge_data, colWidths=[7.5 * inch])
    badge_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), badge_color),
                ("TOPPADDING", (0, 0), (0, 0), 14),
                ("BOTTOMPADDING", (0, 0), (0, 0), 14),
                ("ROUNDEDCORNERS", [6]),
            ]
        )
    )
    story.append(badge_tbl)
    story.append(Spacer(1, 8))

    # Rationale
    rationale_para = Paragraph(
        f"<b>Rationale:</b> {review_data.get('overall_rationale', '')}",
        styles["rationale"],
    )
    story.append(rationale_para)
    story.append(Spacer(1, 14))

    # ---- SCORECARD ----
    story.append(Paragraph("Summary Scorecard", styles["heading"]))
    story.append(_scorecard_table(review_data["findings"], styles))
    story.append(Spacer(1, 14))

    # ---- DETAILED FINDINGS ----
    story.append(PageBreak())
    story.append(Paragraph("Detailed Compliance Findings", styles["heading"]))
    story.append(Spacer(1, 6))
    story.append(_findings_table(review_data["findings"], styles))

    # ---- FOOTER ----
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#BDC3C7")))
    story.append(Spacer(1, 4))
    story.append(
        Paragraph(
            "Generated by Claude claude-sonnet-4-6 | Anthropic API | "
            "For quality review use only — not a substitute for qualified regulatory counsel.",
            styles["footer"],
        )
    )

    doc.build(story)


# ---------------------------------------------------------------------------
# CLI ENTRY POINT
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Namespace containing all parsed argument values.
    """
    parser = argparse.ArgumentParser(
        prog="sop_review.py",
        description="AI-powered 21 CFR 820 SOP compliance review tool (powered by Claude).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sop_review.py --file sample_sop.txt --sop-type cleaning --device-class II
  python sop_review.py --file my_mfg_sop.docx --sop-type manufacturing --device-class III --output report.pdf
  python sop_review.py --file stryker_mako_sop.pdf --sop-type inspection --device-class III --output mako_report.pdf
        """,
    )
    parser.add_argument(
        "--file",
        required=True,
        metavar="PATH",
        help="Path to the SOP file (.txt, .docx, or .pdf)",
    )
    parser.add_argument(
        "--output",
        default="./sop_review_report.pdf",
        metavar="PATH",
        help="Output path for the PDF report (default: ./sop_review_report.pdf)",
    )
    parser.add_argument(
        "--device-class",
        required=True,
        choices=["I", "II", "III"],
        metavar="CLASS",
        help="FDA device class: I, II, or III",
    )
    parser.add_argument(
        "--sop-type",
        required=True,
        choices=["manufacturing", "calibration", "cleaning", "inspection", "complaint"],
        metavar="TYPE",
        help="SOP type: manufacturing | calibration | cleaning | inspection | complaint",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point — orchestrates file reading, API call, and PDF generation."""
    args = parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "ERROR: ANTHROPIC_API_KEY environment variable is not set.\n"
            "Set it with: export ANTHROPIC_API_KEY='sk-ant-...'",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"[1/4] Reading SOP file: {args.file}")
    try:
        sop_text = read_sop_file(args.file)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"[2/4] Sending to Claude (model: claude-sonnet-4-6) "
        f"— SOP type: {args.sop_type}, Device class: {args.device_class}"
    )
    try:
        raw_response = call_claude(sop_text, args.sop_type, args.device_class)
    except Exception as exc:
        print(f"ERROR: Claude API call failed — {exc}", file=sys.stderr)
        sys.exit(1)

    print("[3/4] Parsing Claude response...")
    try:
        review_data = parse_claude_response(raw_response)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    findings = review_data["findings"]
    present_count = sum(1 for f in findings if f["status"] == "PRESENT")
    print(
        f"      Overall status: {review_data['overall_status']} "
        f"({present_count}/{len(findings)} items PRESENT)"
    )

    print(f"[4/4] Generating PDF report: {args.output}")
    generate_pdf_report(
        review_data=review_data,
        output_path=args.output,
        sop_filename=Path(args.file).name,
        device_class=args.device_class,
        sop_type=args.sop_type,
    )

    print(f"\nDone. Report saved to: {args.output}")


if __name__ == "__main__":
    main()
