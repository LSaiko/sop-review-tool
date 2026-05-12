# Example SOP Review Output — Stryker IGS Optical Tracker Calibration SOP

**SOP File:** `examples/stryker_igs_optical_tracker_calibration_sop.txt`  
**Document Number:** SOP-CAL-IGS-018, Rev. B  
**Review Date:** 2026-05-11  
**Device Class:** II (Stryker Navigation System 2.0 — 510(k) K201847)  
**SOP Type:** `calibration`  
**Model:** `claude-sonnet-4-6`  
**CLI Command:**

```bash
python sop_review.py \
  --file examples/stryker_igs_optical_tracker_calibration_sop.txt \
  --sop-type calibration \
  --device-class II \
  --output validation/igs_calibration_review_report.pdf
```

---

## Overall GMP Readiness

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│               NEEDS REVISION                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Rationale:** The SOP is well-structured and provides strong calibration methodology with NIST-traceable references and quantitative acceptance criteria. However, two items require remediation before QA sign-off: the Calibration Interval Justification (C01) lacks explicit frequency documentation in the procedure body (interval is stated in the disposition step but not formally justified), and the Materials and Equipment list (U06) references calibration due dates by external SOP rather than stating them explicitly, which may be insufficient for a standalone audit trail. All other 13 items are fully present.

---

## Summary Scorecard

| Total Items | PRESENT | INCOMPLETE | MISSING | Pass Rate |
|:-----------:|:-------:|:----------:|:-------:|:---------:|
| 15 | 13 | 2 | 0 | **87%** |

---

## Detailed Compliance Findings

### Universal Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| U01 | Purpose Statement | 21 CFR 820.40 | **PRESENT** | *"This procedure establishes the calibration requirements for the Stryker Navigation System 2.0 Optical Tracking Camera (OTC)... Calibration ensures positional accuracy meets the ≤1.0 mm root mean square (RMS) spatial error specification required for safe navigated surgical guidance."* | — |
| U02 | Scope | 21 CFR 820.40 | **PRESENT** | Scope identifies specific model series (NAV-OTC-200), trigger conditions (commissioning, periodic, post-repair), and explicit exclusions (Nav 1.x, fluoroscopic C-arm, software-only upgrades). | — |
| U03 | Responsibilities | 21 CFR 820.20(b) | **PRESENT** | Biomedical Engineer (performs), BME Supervisor (reviews/countersigns, disposition), and QA Manager (approves, audits) all defined with distinct obligations including escalation path for out-of-tolerance findings. | — |
| U04 | References | 21 CFR 820.40 | **PRESENT** | Regulatory references (21 CFR 820.72, 820.75), three applicable standards (ANSI/NCSL Z540-1, ISO 10360-2, ASTM F2554-10), and five internal controlled documents including the Stryker NavCalibrate User Guide and Service Manual. | — |
| U05 | Definitions / Abbreviations | 21 CFR 820.3 | **PRESENT** | 10 terms defined including AUC, CASS, RMS, and TRE — all acronyms used in the procedure body are present in Section 5. | — |
| U06 | Materials and Equipment List | 21 CFR 820.70(g) | **INCOMPLETE** | *"Stryker NavCalibration Reference Frame Kit (Part No. NAV-REF-KIT-001) Traceable to NIST via calibration certificate on file (BME Lab binder CAL-REF-IGS); recalibration interval: 12 months"* — Equipment is listed with cal tags and traceability statements, but the specific calibration due dates for each item are referenced by binder location rather than stated or tracked on the form. | Add a column to Form CAL-IGS-018 that captures the calibration due date for each reference standard used in that specific calibration event, ensuring a standalone audit-ready record. |
| U07 | Safety Precautions / PPE Requirements | 21 CFR 820.70(e) | **PRESENT** | Section 7 covers ESD wrist strap for electronic components, nitrile gloves for reference sphere handling (with rationale re: oil contamination), IR Class 1M safety note, and environmental requirements with documented thresholds (18–24 °C, 30–70% RH). | — |
| U08 | Step-by-Step Procedure | 21 CFR 820.40 | **PRESENT** | Eight numbered steps in action-verb format: environmental check, equipment verification, physical inspection, volumetric accuracy (NavCalibrate guided), point accuracy (sphere test), reference bar verification, disposition, and documentation. Acceptance criteria stated inline at each measurement step. | — |
| U09 | Documentation / Forms / Records | 21 CFR 820.180 | **PRESENT** | Section 9 specifies Form CAL-IGS-018, NavCalibrate PDF certificate with archive path, NCR form, and calibration label specification (Section 9.4). Retention stated as "minimum device useful life + 2 years, not less than 5 years." | — |
| U10 | Revision History Table | 21 CFR 820.40(b) | **PRESENT** | Complete revision history table with Revision letter, Date, Author (with role), and specific Change Summary for both Rev A and Rev B. Rev B references corrective action CAR-2024-019. | — |
| U11 | Approval Signatures Block | 21 CFR 820.40(a) | **PRESENT** | Signature block with Prepared By (BME Supervisor), Reviewed By (Regulatory Affairs), and Approved By (Director of Quality Assurance). | — |

### Calibration-Specific Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| C01 | Calibration Interval Justification | 21 CFR 820.72(a) | **INCOMPLETE** | Calibration interval (12 months) is stated in Step 7.1 ("Record next calibration due date (12 months from today)") but the SOP body does not contain a formal justification for why 12 months is the appropriate interval (e.g., reference to manufacturer recommendation, usage frequency analysis, or historical drift data). | Add a statement in Section 9 or a dedicated sub-section citing the basis for the 12-month interval: manufacturer's recommended service interval per NAV-SM-200, or internal usage analysis. This is required to demonstrate interval rationale under 21 CFR 820.72(a). |
| C02 | NIST Traceability Statement | 21 CFR 820.72(b) | **PRESENT** | *"all calibration reference standards (Section 6.1) have current, valid NIST-traceable calibration certificates... Record certificate numbers on Form CAL-IGS-018, Section 2."* NIST certificate numbers are captured on the record at each calibration event. | — |
| C03 | Out-of-Calibration Response Procedure | 21 CFR 820.72(a) | **PRESENT** | Step 7.2 defines out-of-calibration response: remove from service immediately, affix red "OUT OF SERVICE" label, notify BME Supervisor within 1 hour, initiate NCR, and assess impact on procedures performed since last passing calibration. Impact assessment requirement is especially strong for a Class II surgical navigation device. | — |
| C04 | Calibration Label Requirements | 21 CFR 820.72(b) | **PRESENT** | Section 9.4 specifies label contents (CALIBRATED text, serial number, calibration date, next due date, calibrated by), font size (minimum 8-pt), color (green with black print), and sourcing from approved supplier. | — |

---

## Reviewer Notes (Human Supplement)

1. **C01 interval basis** — The 12-month interval is consistent with Stryker's recommended service interval in the NAV-SM-200 Service Manual. Adding a one-line citation to Section 9 ("Interval established per manufacturer service documentation NAV-SM-200, Section 4.2") would close this finding with minimal revision effort.

2. **U06 equipment due dates** — The current approach (reference to binder) is administratively acceptable but creates a gap if the binder is not co-located with the record during an audit. A simple fix: add a "Cal Due Date" column to Form CAL-IGS-018 Section 2.

3. **Environmental condition documentation** — The SOP requires temperature and humidity to be recorded at start AND end of calibration (Step 1.1, Step 8.1 by implication). Verify that Form CAL-IGS-018 has two time-stamped rows for environmental data, not just one.

---

## AI-Assisted Review Conclusion

**AI Preliminary Assessment:** NEEDS REVISION (2 INCOMPLETE items)  
**Estimated Remediation Effort:** Low — both findings addressable with a Rev C minor update (< 1 page of changes)  
**Human Reviewer Concurrence:** ☐ Concur  ☐ Concur with comments  ☐ Do not concur

Human Reviewer: ___________________________  Date: ___________

---

*Generated by claude-sonnet-4-6 | Anthropic API | For quality review use only — not a substitute for qualified regulatory counsel.*
