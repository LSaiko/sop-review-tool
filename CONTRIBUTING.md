# Contributing to sop-review-tool

Thank you for improving this tool. This guide covers the most common contribution types: adding a new SOP type, extending the checklist, adjusting device-class stringency, and general code changes.

---

## Setup

```bash
git clone https://github.com/LSaiko/sop-review-tool.git
cd sop-review-tool
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
```

---

## Adding a New SOP Type

All SOP types and their checklist items live in `sop_review.py` inside the `TYPE_SPECIFIC_CHECKLIST` dictionary. To add a new type (e.g., `sterilization`):

### 1. Add checklist items to `TYPE_SPECIFIC_CHECKLIST`

```python
TYPE_SPECIFIC_CHECKLIST: dict[str, list[dict]] = {
    # ... existing types ...
    "sterilization": [
        {
            "id": "ST01",
            "item": "Sterilization Method Specification",
            "description": "Method (EtO, steam, radiation) and cycle parameters defined",
            "regulation": "21 CFR 820.75",
        },
        {
            "id": "ST02",
            "item": "Bioburden Limit",
            "description": "Pre-sterilization bioburden acceptance limit stated",
            "regulation": "21 CFR 820.75(a)",
        },
        # Add as many items as the regulation requires
    ],
}
```

**Item ID convention:** Use a short uppercase prefix + two-digit number.
Use a prefix that doesn't conflict with existing ones (`U`, `M`, `C`, `CL`, `I`, `CP`).

### 2. Register the type in `parse_args()`

```python
parser.add_argument(
    "--sop-type",
    required=True,
    choices=[
        "manufacturing", "calibration", "cleaning",
        "inspection", "complaint", "sterilization",  # ← add here
    ],
    help="SOP type: manufacturing | calibration | ... | sterilization",
)
```

### 3. Add a reference SOP to `examples/`

Create a realistic sample SOP file at:
```
examples/acme_<product>_<type>_sop.txt
```

Follow the format of the existing example SOPs:
- Use the standard SOP header (Document Number, Title, Revision, Effective Date)
- Include all 11 universal sections (Purpose → Approval Signatures)
- Include all your new type-specific sections
- Add a revision history table

### 4. Generate a review output and add it to `validation/`

Run the tool against your new SOP:
```bash
python sop_review.py \
  --file examples/your_new_sop.txt \
  --sop-type sterilization \
  --device-class III \
  --output validation/your_new_sop_review.pdf \
  --json-output validation/your_new_sop_findings.json
```

Create a corresponding `validation/your_new_sop_review_output.md` following
the format of the existing review output files.

### 5. Update the README

Add your new SOP type to the **Supported SOP Types** table in `README.md`:
```markdown
| `sterilization` | Sterilization Method, Bioburden Limit, ... |
```

Add a card to the **Example Reports** gallery HTML table if you have a reference SOP.

---

## Adding or Modifying Checklist Items

To add a new item to an existing SOP type:

```python
# In TYPE_SPECIFIC_CHECKLIST["cleaning"]
{
    "id": "CL05",
    "item": "Endotoxin / Pyrogen Control",
    "description": "Endotoxin limits and testing method for water-contact surfaces",
    "regulation": "21 CFR 820.70(e)",
},
```

To modify a universal checklist item, edit the corresponding entry in
`UNIVERSAL_CHECKLIST`. Note that universal items apply to **all** SOP types,
so any change affects every review.

---

## Adjusting Device-Class Stringency Notes

The `CLASS_NOTES` dictionary injects a one-sentence context note into the
Claude prompt for each device class. Edit these in `sop_review.py`:

```python
CLASS_NOTES: dict[str, str] = {
    "I":   "Class I device: ...",
    "II":  "Class II device: ...",
    "III": "Class III device: ...",
}
```

Keep notes concise — they are injected directly into the prompt. Avoid
language that would instruct Claude to ignore checklist items or assign
blanket PRESENT statuses.

---

## Modifying the PDF Report

The PDF is built with ReportLab in `generate_pdf_report()`. Key functions:

| Function | What it controls |
|---|---|
| `_make_styles()` | All paragraph styles (fonts, sizes, colors) |
| `_scorecard_table()` | Summary scorecard (PRESENT / INCOMPLETE / MISSING counts) |
| `_findings_table()` | Per-item findings table with evidence and recommendations |
| `generate_pdf_report()` | Page layout, header, badge, rationale, footer |

Color constants are at the top of the PDF section:
```python
STATUS_COLORS  = { "PRESENT": ..., "INCOMPLETE": ..., "MISSING": ... }
OVERALL_COLORS = { "READY FOR QA REVIEW": ..., "NEEDS REVISION": ..., "MAJOR GAPS": ... }
```

---

## Code Style

- Follow existing docstring format (Google-style Args / Returns / Raises).
- All public functions must have docstrings.
- Run a linter before submitting (`ruff check sop_review.py` or `flake8`).
- Do not commit generated `*_report.pdf` or `findings.json` files — these are in `.gitignore`.

---

## Submitting Changes

1. Create a branch: `git checkout -b feat/add-sterilization-sop-type`
2. Make your changes and test with a real SOP file.
3. Update `CHANGELOG.md` under `[Unreleased]`.
4. Open a pull request with a clear description of what changed and why.

---

## Important Reminder

This tool performs **preliminary** assessment only. Any new checklist items or
SOP types you add should be reviewed against current FDA guidance and validated
against known-compliant reference documents before being relied upon in a
regulated environment.
