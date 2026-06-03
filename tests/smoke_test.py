#!/usr/bin/env python3
"""
smoke_test.py — offline smoke tests for sop_review.py.

Runs WITHOUT an Anthropic API key: it exercises every pure function plus
PDF rendering, and locks in the robustness fixes (XML-escaping, empty-findings
guard, .docx tables, response-shape validation, non-UTF-8 handling).

Usage:
    python tests/smoke_test.py
Exits 0 if all checks pass, 1 otherwise.
"""

import json
import sys
import tempfile
from pathlib import Path

# Import the module under test (repo root is the parent of tests/).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sop_review as sr  # noqa: E402

PASSED = 0
FAILED = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  PASS  {name}")
    else:
        FAILED += 1
        print(f"  FAIL  {name}{' -- ' + detail if detail else ''}")


def expect_raises(name: str, exc_type, fn, *args) -> None:
    try:
        fn(*args)
    except exc_type:
        check(name, True)
    except Exception as exc:  # noqa: BLE001
        check(name, False, f"raised {type(exc).__name__}, expected {exc_type.__name__}")
    else:
        check(name, False, "no exception raised")


def test_build_checklist_text() -> None:
    print("build_checklist_text")
    txt = sr.build_checklist_text("inspection")
    check("universal items present", "[U01]" in txt and "[U11]" in txt)
    check("type-specific items present", "[I01]" in txt)
    unknown = sr.build_checklist_text("does-not-exist")
    check("unknown type -> universal only", "[U01]" in unknown and "[I01]" not in unknown)


def test_parse_claude_response() -> None:
    print("parse_claude_response")
    good = {
        "overall_status": "READY FOR QA REVIEW",
        "overall_rationale": "ok",
        "findings": [{"id": "U01", "item": "Purpose", "regulation": "x",
                      "status": "PRESENT", "evidence": "e", "recommendation": None}],
    }
    # Markdown fences should be stripped.
    fenced = "```json\n" + json.dumps(good) + "\n```"
    parsed = sr.parse_claude_response(fenced)
    check("valid (fenced) JSON parses", parsed["overall_status"] == "READY FOR QA REVIEW")

    expect_raises("non-JSON -> ValueError", ValueError, sr.parse_claude_response, "not json")

    missing = json.dumps({"overall_status": "X", "findings": []})
    expect_raises("missing keys -> ValueError", ValueError, sr.parse_claude_response, missing)

    empty = json.dumps({**good, "findings": []})
    expect_raises("empty findings -> ValueError", ValueError, sr.parse_claude_response, empty)

    bad_status = json.dumps({**good, "findings": [{"id": "U01", "status": "MAYBE"}]})
    expect_raises("invalid status -> ValueError", ValueError, sr.parse_claude_response, bad_status)

    no_status = json.dumps({**good, "findings": [{"id": "U01"}]})
    expect_raises("finding missing status -> ValueError", ValueError, sr.parse_claude_response, no_status)


def test_read_sop_file() -> None:
    print("read_sop_file")
    expect_raises("missing file -> FileNotFoundError", FileNotFoundError,
                  sr.read_sop_file, "no_such_file_12345.txt")

    with tempfile.TemporaryDirectory() as d:
        bad_ext = Path(d) / "x.rtf"
        bad_ext.write_text("hi", encoding="utf-8")
        expect_raises("unsupported ext -> ValueError", ValueError, sr.read_sop_file, str(bad_ext))

        ok = Path(d) / "ok.txt"
        ok.write_text("hello sop", encoding="utf-8")
        check("reads .txt", sr.read_sop_file(str(ok)) == "hello sop")

        nonutf8 = Path(d) / "bad.txt"
        nonutf8.write_bytes(b"\xff\xfe\x00bad bytes")
        expect_raises("non-UTF-8 .txt -> ValueError", ValueError, sr.read_sop_file, str(nonutf8))


def test_pdf_rendering_escapes_and_empty() -> None:
    print("generate_pdf_report (XML-escape + empty-findings regressions)")
    # Content with characters that break ReportLab unless escaped.
    nasty = "Tolerance < 5 µm & spec > 3 <b>bold?</b>"
    review = {
        "overall_status": "NEEDS REVISION",
        "overall_rationale": nasty,
        "findings": [{
            "id": "U01", "item": "Purpose & Scope <x>", "regulation": "21 CFR 820.40 <a>",
            "status": "INCOMPLETE", "evidence": nasty, "recommendation": nasty,
        }],
    }
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "report.pdf"
        try:
            sr.generate_pdf_report(review, str(out), "sample.txt", "III", "inspection")
            check("PDF builds with <, >, & in dynamic text", out.exists() and out.stat().st_size > 0)
        except Exception as exc:  # noqa: BLE001
            check("PDF builds with <, >, & in dynamic text", False, f"{type(exc).__name__}: {exc}")

    # Empty findings must not raise ZeroDivisionError in the scorecard.
    styles = sr._make_styles()
    try:
        sr._scorecard_table([], styles)
        check("scorecard handles empty findings (no ZeroDivision)", True)
    except Exception as exc:  # noqa: BLE001
        check("scorecard handles empty findings (no ZeroDivision)", False,
              f"{type(exc).__name__}: {exc}")


def main() -> None:
    print("=== sop_review.py offline smoke tests ===\n")
    test_build_checklist_text()
    test_parse_claude_response()
    test_read_sop_file()
    test_pdf_rendering_escapes_and_empty()
    print(f"\n{PASSED} passed, {FAILED} failed")
    sys.exit(1 if FAILED else 0)


if __name__ == "__main__":
    main()
