# Tests

Two tiers — one needs no API key, one does.

## Offline pytest suite (no API key)

`test_sop_review.py` covers the 21 CFR 820 gap-analysis pipeline end to end: checklist
assembly, `.txt`/`.docx`/`.pdf` ingestion, response-shape validation, PDF rendering
(XML-escaping, empty-findings guard), retry behaviour and the CLI, plus the optional Part 11
hook. The Claude API is mocked; no test makes a live call. CI runs it on every push.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt pytest pytest-cov
pytest tests/ --cov=sop_review --cov=part11 --cov-fail-under=90
```

## Online re-validation (requires ANTHROPIC_API_KEY)

Drives the full CLI with the configured model (currently `claude-opus-4-8`)
against every example SOP and compares to the documented `claude-sonnet-4-6`
baseline. Use this to re-establish the VALIDATED status after a model upgrade
(see `../validation/validation_report.md`).

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
python tests/revalidate.py            # outputs JSON + PDF to tests/results/
```

Cases that differ from the baseline are reported as **DRIFT** (informational),
not failures — a qualified reviewer decides whether the new model's findings
are acceptable before sign-off.
