# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [1.3.0] — 2026-05-16

### Fixed
- **UTC timestamp bug** — `datetime.now()` in PDF report header now uses
  `datetime.now(timezone.utc)` so the "Date Generated" field is always true UTC,
  not local machine time.
- **`--help` no longer hides valid choices** — Removed `metavar="CLASS"` and
  `metavar="TYPE"` from `--device-class` and `--sop-type` so argparse displays
  the actual valid values in `--help` output.
- **PDF error handling** — `pdfplumber.open()` is now wrapped in a `try/except`
  that catches password-protected, corrupt, and invalid PDF files and surfaces a
  clear, actionable error message instead of a raw traceback.

### Changed
- **`max_tokens` raised from 4096 → 8192** — Prevents JSON truncation on
  Class III SOPs with 15 checklist items and long evidence quotes.
- **QMSR limitation note updated** — README now correctly states the QMSR
  took effect February 2, 2026 (was phrased as a future event) and advises
  users to perform a manual QMSR gap assessment alongside AI output.

### Added
- **Retry logic with exponential backoff** — `call_claude()` retries up to
  3 times (5 s → 10 s → 20 s) on transient `anthropic.APIError` before
  failing, making the tool resilient to momentary network or API hiccups.
- **`--json-output PATH` flag** — Optionally saves the raw Claude JSON
  response alongside the PDF report. Useful for programmatic downstream
  integration with QMS databases or audit logging systems.
- **`.gitignore`** — Protects against accidental commits of generated reports,
  `.env` files (API keys), virtual environments, and `__pycache__`.
- **`CHANGELOG.md`** (this file) — Documents version history.
- **`CONTRIBUTING.md`** — Guide for adding new SOP types, checklist items,
  and device-class stringency notes.

### Removed
- **Unused `TA_LEFT` import** — `TA_LEFT` was imported from `reportlab.lib.enums`
  but never referenced in the codebase.
- **Dead `"body"` ParagraphStyle** — Defined in `_make_styles()` but never
  used in the PDF story builder.

### Documentation
- Updated module-level docstring and `read_sop_file()` docstring to reflect
  `.pdf` input support (added in v1.2.0 but not reflected in docstrings).

---

## [1.2.0] — 2026-05-15

### Added
- **PDF input support** — `read_sop_file()` now handles `.pdf` files using
  `pdfplumber` with `layout=True` for structure-preserving text extraction.
  Scanned/image-only PDFs raise a clear error directing the user to OCR.
- `pdfplumber>=0.11.0` added to `requirements.txt`.
- PDF usage example added to CLI `--help` epilog and README quickstart.
- Scanned-PDF limitation added to README limitations table.

---

## [1.1.0] — 2026-05-14

### Added
- **3 additional Stryker reference SOPs** in `examples/`:
  - `stryker_igs_optical_tracker_calibration_sop.txt` (calibration, Class II)
  - `stryker_mako_instrument_cleaning_sop.txt` (cleaning, Class III)
  - `stryker_mako_igs_complaint_handling_sop.txt` (complaint, Class III)
- **3 corresponding review output files** in `validation/`:
  - `igs_calibration_review_output.md` — 13/15 PRESENT, NEEDS REVISION
  - `mako_cleaning_review_output.md` — 12/15 PRESENT, NEEDS REVISION
  - `mako_igs_complaint_review_output.md` — 14/15 PRESENT, READY FOR QA REVIEW
- **README example gallery** — 4-card HTML showcase at top of README with
  color-coded GMP readiness badges and links to full review outputs.
- Repository structure table updated in README.

---

## [1.0.0] — 2026-05-14 — Initial Release

### Added
- `sop_review.py` — AI-powered CLI tool using Claude (`claude-sonnet-4-6`)
  as a senior FDA compliance specialist persona.
- **21 CFR 820 checklist** — 11 universal items + type-specific additions for
  5 SOP categories: `manufacturing`, `calibration`, `cleaning`, `inspection`,
  `complaint`.
- **Device class stringency** — Class I / II / III adjusts review rigor.
- **Color-coded PDF report** — Green (PRESENT) / Amber (INCOMPLETE) /
  Red (MISSING) with overall GMP readiness badge and summary scorecard.
- `.txt` and `.docx` input support.
- `sample_sop.txt` — Demo cleaning SOP with intentional gaps (U10, CL03).
- `sop_review_report.pdf` — Pre-generated example PDF from `sample_sop.txt`.
- `examples/stryker_mako_inspection_sop.txt` — Fully-compliant Class III
  reference SOP (Mako RIO incoming inspection, SOP-QC-MAK-042 Rev C).
- `validation/validation_report.md` — Tool validation methodology and results.
- `validation/stryker_mako_review_output.md` — Example review output (15/15 PRESENT).
- `requirements.txt` — `anthropic`, `reportlab`, `python-docx`.
- `README.md` — Full setup, CLI reference, checklist coverage, and disclaimer.
