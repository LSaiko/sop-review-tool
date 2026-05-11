# SOP Compliance Review Tool

An AI-powered CLI tool for **preliminary assessment** of Standard Operating Procedures against the **21 CFR Part 820** Quality System Regulation. Generates color-coded PDF reports to support — not replace — qualified human review.

> **Important:** This tool is for preliminary, first-pass gap analysis only. All findings must be validated and finalized by a qualified Regulatory Affairs or Quality Assurance professional before any action is taken.

---

## What This Tool Does

Medical device SOPs must conform to 21 CFR Part 820 (FDA Quality System Regulation) before they can be used in regulated manufacturing, inspection, or complaint-handling environments. Manual review is time-consuming and error-prone, especially for high-document-volume QMS environments (e.g., Stryker IGS, Mako Robotic Surgical System).

This tool uses **Claude** (`claude-sonnet-4-6`) as a senior FDA compliance specialist persona to:

1. Parse a submitted SOP (`.txt` or `.docx`)
2. Evaluate it against a tiered 21 CFR 820 checklist (universal + SOP-type-specific items)
3. Rate each checklist item `PRESENT` / `INCOMPLETE` / `MISSING`
4. Generate a professional color-coded PDF report with evidence quotes and actionable recommendations

### Training & Continuous Improvement

The tool is designed to improve over time. By feeding **existing approved and audited SOPs** (e.g., cleared Stryker IGS / Mako documents) as training examples, reviewers can:

- Calibrate Claude's assessment against known-good documents
- Identify acceptable baseline language patterns for specific SOP types
- Establish what "PRESENT" looks like for your organization's QMS style guide
- Build institutional knowledge of review parameters directly into the prompt engineering layer

See [`examples/`](./examples/) for reference SOPs and [`validation/`](./validation/) for benchmark output reports.

---

## Features

| Feature | Detail |
|---|---|
| **AI Review Engine** | Claude evaluates each SOP section as a senior FDA compliance specialist |
| **21 CFR 820 Checklist** | 11 universal items + type-specific additions per SOP category |
| **Device Class Stringency** | Class I / II / III adjusts review rigor and scoring thresholds |
| **Color-coded PDF Report** | Green (PRESENT) / Amber (INCOMPLETE) / Red (MISSING) with overall GMP readiness badge |
| **Structured JSON Extraction** | Claude returns structured data — no hallucinated prose, parseable output |
| **Input Formats** | `.txt`, `.docx`, and `.pdf` supported (text-based PDFs; scanned/image PDFs are not supported) |
| **Extensible Checklists** | Add organization-specific checklist items directly in `sop_review.py` |

---

## Supported SOP Types

| Type | Type-Specific Checklist Additions |
|---|---|
| `manufacturing` | Environmental Conditions, In-Process Inspection, NCR Procedure, Equipment Qualification |
| `calibration` | Calibration Interval, NIST Traceability, Out-of-Calibration Response, Label Requirements |
| `cleaning` | Cleaning Agent Specifications, Rinse/Residue Verification, NCR Procedure, Cleaning Schedule |
| `inspection` | Acceptance Criteria, Sampling Plan, Inspection Equipment, Disposition Authority |
| `complaint` | Complaint Intake/Acknowledgment, MDR Reportability, Root Cause Analysis, CAPA Linkage |

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/LSaiko/sop-review-tool.git
cd sop-review-tool
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows PowerShell
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key

Get your key from [console.anthropic.com](https://console.anthropic.com).

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### 5. Run a review

```bash
# Review the bundled sample SOP (intentional gaps for demo)
python sop_review.py \
  --file sample_sop.txt \
  --sop-type cleaning \
  --device-class II \
  --output demo_report.pdf

# Review a Stryker Mako-style inspection SOP (Class III)
python sop_review.py \
  --file examples/stryker_mako_inspection_sop.txt \
  --sop-type inspection \
  --device-class III \
  --output mako_review_report.pdf

# Review a PDF SOP directly
python sop_review.py \
  --file my_sop.pdf \
  --sop-type manufacturing \
  --device-class II \
  --output my_sop_report.pdf
```

> **PDF note:** The tool uses `pdfplumber` for text extraction. Text-based (digitally created) PDFs work well. Scanned or image-only PDFs are not supported — convert them with OCR software first.

---

## CLI Reference

```
python sop_review.py --file PATH --device-class {I,II,III} --sop-type TYPE [--output PATH]
```

| Argument | Required | Values | Description |
|---|---|---|---|
| `--file` | Yes | path | SOP file (`.txt`, `.docx`, or `.pdf`) |
| `--device-class` | Yes | `I` `II` `III` | FDA device class — adjusts review stringency |
| `--sop-type` | Yes | `manufacturing` `calibration` `cleaning` `inspection` `complaint` | Loads the appropriate checklist |
| `--output` | No | path | PDF output path (default: `./sop_review_report.pdf`) |

---

## PDF Report Structure

Each generated report contains:

1. **Header** — date, SOP filename, device class, SOP type
2. **Overall GMP Readiness Badge** — `READY FOR QA REVIEW` / `NEEDS REVISION` / `MAJOR GAPS`
3. **Summary Scorecard** — pass/fail counts and pass-rate percentage at a glance
4. **Detailed Findings Table** — every checklist item with:
   - Status (color-coded)
   - Evidence quote from the SOP
   - Actionable recommendation (when not PRESENT)
5. **Footer** — model attribution and quality-use disclaimer

---

## 21 CFR 820 Checklist Coverage

### Universal (all SOP types — 21 CFR 820.40)
- `U01` Purpose Statement
- `U02` Scope
- `U03` Responsibilities (21 CFR 820.20(b))
- `U04` References
- `U05` Definitions / Abbreviations (21 CFR 820.3)
- `U06` Materials and Equipment List (21 CFR 820.70(g))
- `U07` Safety Precautions / PPE Requirements (21 CFR 820.70(e))
- `U08` Step-by-Step Procedure
- `U09` Documentation / Forms / Records (21 CFR 820.180)
- `U10` Revision History Table (21 CFR 820.40(b))
- `U11` Approval Signatures Block (21 CFR 820.40(a))

### Manufacturing additions — 21 CFR 820.70 / 820.90
`M01` Environmental Conditions · `M02` In-Process Inspection · `M03` NCR Procedure · `M04` Equipment Qualification

### Calibration additions — 21 CFR 820.72
`C01` Calibration Interval · `C02` NIST Traceability · `C03` Out-of-Calibration Response · `C04` Calibration Labels

### Cleaning additions — 21 CFR 820.70 / 820.90
`CL01` Cleaning Agent Specs · `CL02` Rinse/Residue Verification · `CL03` NCR Procedure · `CL04` Cleaning Schedule

### Inspection additions — 21 CFR 820.80
`I01` Acceptance Criteria · `I02` Sampling Plan · `I03` Inspection Equipment · `I04` Disposition Authority

### Complaint additions — 21 CFR 820.198 / 21 CFR 803
`CP01` Complaint Intake · `CP02` MDR Reportability · `CP03` Root Cause Analysis · `CP04` CAPA Linkage

---

## Repository Structure

```
sop-review-tool/
├── sop_review.py                          # Main CLI application
├── sample_sop.txt                         # Demo SOP with intentional gaps (cleaning, Class II)
├── requirements.txt                       # Python dependencies
├── README.md                              # This file
├── sop_review_report.pdf                  # Example output from sample_sop.txt
│
├── examples/
│   └── stryker_mako_inspection_sop.txt    # Reference SOP: Mako RIO robotic system (Class III)
│
└── validation/
    ├── validation_report.md               # Tool validation: methodology, test cases, results
    └── stryker_mako_review_output.md      # Example review output for the Mako inspection SOP
```

---

## Architecture

```
sop_review.py
├── read_sop_file()          — .txt / .docx ingestion
├── build_checklist_text()   — assembles prompt checklist (universal + type-specific)
├── call_claude()            — Anthropic API call → structured JSON
├── parse_claude_response()  — validates and parses Claude output
└── generate_pdf_report()    — ReportLab PDF builder
    ├── _make_styles()
    ├── _scorecard_table()
    └── _findings_table()
```

**Model:** `claude-sonnet-4-6`  
**System prompt:** Senior FDA compliance specialist persona (15 years QMS experience)  
**Output format:** Structured JSON with per-item `status`, `evidence` quote, and `recommendation`  
**PDF parsing:** `pdfplumber` with layout-preserving text extraction (`layout=True`)

---

## Limitations & Important Caveats

| Limitation | Detail |
|---|---|
| **Preliminary only** | Claude may miss context-dependent requirements. Human sign-off is always required. |
| **Static checklist** | The checklist reflects 21 CFR Part 820 as of 2024. FDA may issue new guidance at any time. |
| **No 21 CFR Part 4 / QSR-to-QMSR transition** | The tool does not yet cover the updated QMSR (Quality Management System Regulation) effective February 2026. |
| **English-language SOPs only** | Multi-language documents are not tested. |
| **Text-based PDFs only** | Scanned / image-only PDFs will raise an error. Use OCR (e.g., Adobe Acrobat, Tesseract) to convert to searchable PDF before submitting. |
| **No cross-document validation** | Referenced SOPs and forms are not fetched or verified. |

---

## Disclaimer

This tool is intended to assist quality professionals in identifying potential gaps in SOP documentation during initial review. It does **not** constitute legal or regulatory advice and is **not** a substitute for review by a qualified Regulatory Affairs or Quality Assurance specialist.

All AI-generated findings must be validated against current FDA guidance, applicable standards, and your organization's document control procedures before any corrective action is taken.

---

## License

MIT — free to use and adapt for portfolio, internal quality tooling, or commercial projects.
