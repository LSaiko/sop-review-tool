# Example SOP Review Output — Stryker Mako / IGS Complaint Handling SOP

**SOP File:** `examples/stryker_mako_igs_complaint_handling_sop.txt`  
**Document Number:** SOP-QA-CX-091, Rev. D  
**Review Date:** 2026-05-11  
**Device Class:** III (Mako SmartRobotics — PMA P150002; IGS Navigation — 510(k) K201847)  
**SOP Type:** `complaint`  
**Model:** `claude-sonnet-4-6`  
**CLI Command:**

```bash
python sop_review.py \
  --file examples/stryker_mako_igs_complaint_handling_sop.txt \
  --sop-type complaint \
  --device-class III \
  --output validation/mako_igs_complaint_review_report.pdf
```

---

## Overall GMP Readiness

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│             READY FOR QA REVIEW                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Rationale:** SOP-QA-CX-091 is an exceptionally thorough complaint handling procedure that addresses all 15 checklist items. The MDR reportability decision framework (three-question screen, five-day report trigger, risk management file cross-reference) is especially strong for a Class III dual-product SOP. The CAPA linkage threshold (≥3 complaints within 12 months) reflects mature PMS program design. No MISSING items; one INCOMPLETE notation on CP02 relates to Appendix A being a separate attachment rather than embedded — a minor structural observation only.

---

## Summary Scorecard

| Total Items | PRESENT | INCOMPLETE | MISSING | Pass Rate |
|:-----------:|:-------:|:----------:|:-------:|:---------:|
| 15 | 14 | 1 | 0 | **93%** |

---

## Detailed Compliance Findings

### Universal Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| U01 | Purpose Statement | 21 CFR 820.40 | **PRESENT** | *"This procedure establishes the requirements for receiving, documenting, investigating, and determining Medical Device Report (MDR) reportability for customer complaints related to the Stryker Mako SmartRobotics Surgical System and Stryker Navigation System 2.0 (IGS)."* Specific to process, devices, and regulatory framework. | — |
| U02 | Scope | 21 CFR 820.40 | **PRESENT** | Scope defines complaint using the 21 CFR 820.3(b) regulatory definition verbatim, lists both device families with their regulatory identifiers (PMA P150002, 510(k) K201847), identifies all complaint source types, and explicitly excludes internal NCRs, supplier complaints, and pre-market feedback with cross-references to applicable SOPs. | — |
| U03 | Responsibilities | 21 CFR 820.20(b) | **PRESENT** | Five roles defined: Complaint Intake Coordinator (receipt, logging, acknowledgment, assignment), Product Line QA Engineer (investigation, MDR assessment), QA Manager (MDR final determination, submission, trend monitoring), and Field Service Engineer (field documentation). Timelines embedded within each responsibility. | — |
| U04 | References | 21 CFR 820.40 | **PRESENT** | Comprehensive — regulatory citations (21 CFR 820.198 subsections, 21 CFR 803.50, 803.53), FDA guidance documents (MDR guidance 2016, Recalls guidance), standards (ISO 13485:2016 Sec 8.2.2, ISO 14971:2019), MedWatch 3500A, and 6 internal documents. Two device-specific Risk Management Files cited. | — |
| U05 | Definitions / Abbreviations | 21 CFR 820.3 | **PRESENT** | 10 terms defined including regulatory definitions for "MDR-Reportable Event" and "Malfunction" sourced directly from 21 CFR 803.50(a) and 21 CFR 803.3 respectively — best practice for a complaint SOP subject to FDA inspection. | — |
| U06 | Materials and Equipment List | 21 CFR 820.70(g) | **PRESENT** | Section 6 lists the Pilgrim SmartSolve CMS (with access path), FDA MedWatch Online Reporting System, all forms (QA-CX-091, QA-MDR-003, MedWatch 3500A), MDR decision tree reference, and both device Risk Management Files. Appropriate for an administrative/quality process SOP. | — |
| U07 | Safety Precautions / PPE Requirements | 21 CFR 820.70(e) | **PRESENT** | Section 7 addresses HIPAA confidentiality requirements (patient PHI, 21 CFR 803.9 citations), returned device quarantine procedure with cross-reference to SOP-QC-NCR-001, and prohibition on repair/disposal without QA Manager approval — appropriate hazard identification for a complaint handling SOP where "safety" pertains to data integrity and evidence preservation rather than physical hazards. | — |
| U08 | Step-by-Step Procedure | 21 CFR 820.40 | **PRESENT** | Six numbered steps with sub-steps: complaint receipt/logging (with 9 required data elements enumerated), triage/assignment (with MDR clock trigger conditions), technical investigation (RCA methodology, returned device testing), MDR reportability assessment (three-question screen), complaint closure (30-day timeline, extension conditions), and complainant response. Timelines embedded throughout. | — |
| U09 | Documentation / Forms / Records | 21 CFR 820.180 | **PRESENT** | Section 9 documents: Complaint Record (SmartSolve), MDR Reportability Assessment form, MDR Submission (MedWatch 3500A copy), acknowledgment/closure letters, and CAPA records. Two separate retention periods correctly differentiated: 21 CFR 820.198(f) for complaint records (device life + 2 years, minimum 5 years) and 21 CFR 803.18 for MDR submissions (minimum 2 years from submission date). | — |
| U10 | Revision History Table | 21 CFR 820.40(b) | **PRESENT** | Complete four-revision history (Rev A through D) with specific change summaries. Rev D notes are particularly strong — cites the ISO 13485:2016 alignment basis and specifies the CAPA threshold change (Step 5.3). Rev C appropriately references the FDA 2022 Q&A guidance driving the five-day MDR update. | — |
| U11 | Approval Signatures Block | 21 CFR 820.40(a) | **PRESENT** | Three-role signature block: Prepared By (VP Quality Assurance), Reviewed By (Regulatory Affairs Specialist), Approved By (Chief Quality Officer). Appropriate C-suite level authority for a complaint/MDR procedure on dual Class III / Class II products. | — |

### Complaint-Specific Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| CP01 | Complaint Intake / Acknowledgment | 21 CFR 820.198(a) | **PRESENT** | *"CIC opens a new Complaint Record in Pilgrim SmartSolve (Form QA-CX-091) within 24 hours of receiving the contact."* Acknowledgment timeline: 2 business days. Dedicated complaint mailbox and phone extension defined. Nine required data elements enumerated in Step 1.3. | — |
| CP02 | MDR / Reportability Determination | 21 CFR 803 / 820.198(d) | **INCOMPLETE** | Step 4 contains a strong three-question MDR screen (Q1: malfunction, Q2: severity potential, Q3: serious injury/death) with the correct logic gate (Q3=Yes OR Q1+Q2=Yes → reportable). Five-day report trigger is addressed in Step 2.3. However, the Appendix A MDR Decision Tree is described as a *"separate attachment in EDMS"* rather than embedded in this SOP. During an inspection, the SOP itself should be self-contained or Appendix A should be formally incorporated by reference with its document number and revision. | Assign a controlled document number to the Appendix A decision tree (e.g., QA-MDR-DT-001 Rev A) and add that citation to the References section. Alternatively, embed the decision tree directly in the SOP as a formal Appendix A section. This closes the gap for standalone SOP completeness under 21 CFR 820.198(d). |
| CP03 | Root Cause Analysis Requirement | 21 CFR 820.198(e) | **PRESENT** | Step 3.3: *"Conduct Root Cause Analysis (RCA) using at minimum a fishbone/Ishikawa diagram or 5-Why analysis. Document RCA findings in the Complaint Record."* Step 3.4 provides a defined taxonomy of root cause categories (6 categories including NDF/UTR). | — |
| CP04 | CAPA Linkage | 21 CFR 820.100 | **PRESENT** | Step 5.3: *"If a systemic issue is identified (same root cause in ≥3 complaints within 12 months), initiate CAPA per SOP-QA-CAPA-007; link CAPA number to the Complaint Record in SmartSolve."* The quantitative threshold (≥3 / 12 months) and SmartSolve linkage requirement are specific and auditable. QA Manager is identified as the CAPA monitor. | — |

---

## Reviewer Notes (Human Supplement)

1. **CP02 — Appendix A** — The Appendix A decision tree is described as already existing in EDMS. The simplest remediation is adding its document number and revision to the References section (e.g., "QA-MDR-DT-001 Rev A: MDR Reportability Decision Tree"). This is a documentation housekeeping item, not a substantive gap.

2. **Five-day MDR clock** — Step 2.3 correctly triggers the five-day clock assessment but phrases it as "notify QA Manager to assess." For a Class III device, consider adding an explicit hold-time requirement: QA Manager must respond within 24 hours to the five-day trigger assessment, to ensure the 5-day window is not inadvertently missed.

3. **HIPAA / 21 CFR 803.9 alignment** — Section 7.1 correctly cites 21 CFR 803.9 for MDR patient confidentiality. Confirm the HIPAA cross-reference (SOP-IT-SEC-003) is current and that it addresses the specific PHI masking format required by FDA's Electronic Submissions System for MedWatch 3500A.

4. **Dual-device scope complexity** — This SOP covers both a Class III PMA device (Mako) and a Class II 510(k) device (IGS Navigation). The MDR investigation steps (Step 3.2 functional testing protocols) reference separate test protocols (TP-MAK-FT-001 and TP-IGS-FT-001). Confirm both protocols are current-revision and included in the next SOP revision's References section update.

---

## AI-Assisted Review Conclusion

**AI Preliminary Assessment:** READY FOR QA REVIEW (1 INCOMPLETE — minor structural item)  
**Estimated Remediation Effort:** Minimal — CP02 gap is a cross-reference citation addition; no substantive content changes required  
**Human Reviewer Concurrence:** ☐ Concur  ☐ Concur with comments  ☐ Do not concur

Human Reviewer: ___________________________  Date: ___________

---

*Generated by claude-sonnet-4-6 | Anthropic API | For quality review use only — not a substitute for qualified regulatory counsel.*
