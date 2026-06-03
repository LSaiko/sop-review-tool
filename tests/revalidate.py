#!/usr/bin/env python3
"""
revalidate.py — online re-validation harness for sop_review.py.

Runs the full CLI (real Anthropic API call with the configured model, currently
claude-opus-4-8) against every bundled example SOP, then compares the result to
the documented claude-sonnet-4-6 baseline. Use this to re-establish the
VALIDATED status after a model upgrade (see validation/validation_report.md).

Requires ANTHROPIC_API_KEY in the environment.

Usage:
    python tests/revalidate.py [--out results]
Exits 0 if every case ran and parsed; 1 if any case errored. Differences from
the baseline are reported as DRIFT (informational), not failures — a human
reviewer signs off on whether the new model's findings are acceptable.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (sop file, sop-type, device-class, baseline overall_status, baseline PRESENT/total)
CASES = [
    ("sample_sop.txt", "cleaning", "II", "NEEDS REVISION", "13/15"),
    ("examples/acme_orthonav_inspection_sop.txt", "inspection", "III", "READY FOR QA REVIEW", "15/15"),
    ("examples/acme_igs_optical_tracker_calibration_sop.txt", "calibration", "II", "NEEDS REVISION", "13/15"),
    ("examples/acme_orthonav_instrument_cleaning_sop.txt", "cleaning", "III", "NEEDS REVISION", "12/15"),
    ("examples/acme_orthonav_igs_complaint_handling_sop.txt", "complaint", "III", "READY FOR QA REVIEW", "14/15"),
]


def run_case(sop: str, sop_type: str, device_class: str, out_dir: Path) -> dict | None:
    stem = Path(sop).stem
    json_out = out_dir / f"{stem}.json"
    pdf_out = out_dir / f"{stem}.pdf"
    cmd = [
        sys.executable, str(ROOT / "sop_review.py"),
        "--file", str(ROOT / sop),
        "--sop-type", sop_type,
        "--device-class", device_class,
        "--output", str(pdf_out),
        "--json-output", str(json_out),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  ERROR running {sop}:\n{proc.stderr.strip()}")
        return None
    try:
        return json.loads(json_out.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"  ERROR reading JSON for {sop}: {exc}")
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Re-validate sop_review.py against example SOPs.")
    ap.add_argument("--out", default="results", help="Directory for JSON/PDF outputs")
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        sys.exit(1)

    out_dir = (ROOT / "tests" / args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    errors = 0
    drifts = 0
    print(f"=== Re-validation run (model from sop_review.py) → {out_dir} ===\n")
    for sop, sop_type, dclass, base_status, base_score in CASES:
        print(f"* {sop}  [{sop_type}, Class {dclass}]")
        data = run_case(sop, sop_type, dclass, out_dir)
        if data is None:
            errors += 1
            continue
        findings = data["findings"]
        present = sum(1 for f in findings if f["status"] == "PRESENT")
        score = f"{present}/{len(findings)}"
        status = data["overall_status"]
        drift = (status != base_status) or (score != base_score)
        if drift:
            drifts += 1
        tag = "DRIFT" if drift else "match"
        print(f"    new: {status} ({score})   baseline: {base_status} ({base_score})   [{tag}]\n")

    print(f"Done. {len(CASES) - errors}/{len(CASES)} cases ran; "
          f"{drifts} differ from baseline (review required); {errors} errored.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
