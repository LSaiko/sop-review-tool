# Tests

Two tiers — one needs no API key, one does.

## Offline smoke test (no API key)

Locks in the robustness fixes (XML-escaping, empty-findings guard, `.docx`
tables, response-shape validation, non-UTF-8 handling) and confirms a PDF
renders. Run on every change.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python tests/smoke_test.py
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
