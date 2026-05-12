# Example SOP Review Output — Stryker Mako Instrument Cleaning SOP

**SOP File:** `examples/stryker_mako_instrument_cleaning_sop.txt`  
**Document Number:** SOP-CLEAN-MAK-033, Rev. A  
**Review Date:** 2026-05-11  
**Device Class:** III (Mako SmartRobotics Accessories — PMA P150002)  
**SOP Type:** `cleaning`  
**Model:** `claude-sonnet-4-6`  
**CLI Command:**

```bash
python sop_review.py \
  --file examples/stryker_mako_instrument_cleaning_sop.txt \
  --sop-type cleaning \
  --device-class III \
  --output validation/mako_cleaning_review_report.pdf
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

**Rationale:** This is a comprehensive, well-written cleaning SOP with strong cleaning agent specifications, detailed washer-disinfector cycle parameters (A0 ≥ 600), and thorough visual inspection criteria. However, two items prevent immediate QA sign-off: the Revision History Table (U10) is explicitly absent (initial release acknowledged in the document footer), and Non-Conformance Reporting (CL03) while referenced, lacks the specific steps for reporting a cleaning deviation or failure as a standalone procedure within this SOP. For a Class III device, both are mandatory. All other 13 items are fully present with high-quality content.

---

## Summary Scorecard

| Total Items | PRESENT | INCOMPLETE | MISSING | Pass Rate |
|:-----------:|:-------:|:----------:|:-------:|:---------:|
| 15 | 12 | 1 | 2 | **80%** |

---

## Detailed Compliance Findings

### Universal Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| U01 | Purpose Statement | 21 CFR 820.40 | **PRESENT** | *"This procedure establishes the manual and automated cleaning requirements for reusable Mako SmartRobotics surgical instruments prior to sterilization, to remove biological soil, lubricant residue, and bone cement particulates that could compromise sterility assurance or cause instrument malfunction..."* Clear, specific, and process-tied. | — |
| U02 | Scope | 21 CFR 820.40 | **PRESENT** | Scope enumerates specific component catalog numbers (Catalog No. 7,207-052 series), lists four component types, and explicitly excludes single-use components, the robotic arm itself, and implant trials with cross-references to applicable SOPs. | — |
| U03 | Responsibilities | 21 CFR 820.20(b) | **PRESENT** | Four roles defined: CSP Tech (performs, logs), CSP Supervisor (reviews, approves, initiates NCR), BME (washer-disinfector maintenance), QA Manager (approves SOP). Escalation paths and timelines defined. | — |
| U04 | References | 21 CFR 820.40 | **PRESENT** | Regulatory (21 CFR 820.70(e)(f), 820.90, 820.180), standards (AAMI TIR30, ISO 15883-1, AAMI ST79, AORN Guidelines 2024), and 6 internal documents including the manufacturer IFU (IFU-MAK-INST-001) and Cleaning Validation Report (CVR-MAK-033-A). | — |
| U05 | Definitions / Abbreviations | 21 CFR 820.3 | **PRESENT** | 11 terms defined. Notably includes a definition of A0 Value with the acceptance threshold (≥600) embedded in the definition — strong practice for a cleaning SOP where A0 is the primary disinfection metric. | — |
| U06 | Materials and Equipment List | 21 CFR 820.70(g) | **PRESENT** | Section 6 details cleaning agents with approved dilution ratios and temperature ranges (Prolystica 1:64 at 45–55°C), automated equipment with unit IDs (WD-03), manual cleaning tools color-coded for Mako dedication (RED), RO water quality requirement (≤5 µS/cm), and consumables. | — |
| U07 | Safety Precautions / PPE Requirements | 21 CFR 820.70(e) | **PRESENT** | Decontamination zone and clean assembly zone PPE specified separately. Chemical hazard (enzymatic detergent), sharps safety for burr edges (dedicated grip tool), and first aid for detergent eye contact all addressed. SDS reference included. | — |
| U08 | Step-by-Step Procedure | 21 CFR 820.40 | **PRESENT** | Eight numbered steps with sub-steps in action-verb format: point-of-use pre-treatment, receive and sort, manual pre-clean (enzymatic), automated WD cycle (with parameters), post-wash visual inspection, lubrication, packaging, and documentation. Inline references to forms and cross-SOPs are consistent throughout. | — |
| U09 | Documentation / Forms / Records | 21 CFR 820.180 | **PRESENT** | Section 9 specifies Form CS-CL-033 (cleaning log), WD-03 cycle printout attachment requirement, NCR form, and CVR-MAK-033-A. Retention stated per 21 CFR 820.180 ("device useful life + 2 years"). | — |
| U10 | Revision History Table | 21 CFR 820.40(b) | **MISSING** | The SOP footer explicitly states: *"NOTE: Revision history not yet established (initial release)."* For a Class III device, a revision history table is mandatory even for Rev A — it must show at minimum the initial release entry. | Add a revision history table with a single Rev A entry: date, author, and "Initial release" as the change summary. This is a quick, straightforward fix. |
| U11 | Approval Signatures Block | 21 CFR 820.40(a) | **PRESENT** | Three-role signature block: Prepared By (CSP Supervisor), Reviewed By (Regulatory Affairs), Approved By (VP Quality Assurance). Appropriate authority levels for a Class III cleaning SOP. | — |

### Cleaning-Specific Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| CL01 | Cleaning Agent Specifications | 21 CFR 820.70(e) | **PRESENT** | *"Enzymatic detergent: Prolystica 2X Concentrate (diluted 1:64 in RO water, 45–55 °C), approved per IFU-MAK-INST-001, Section 6"* — concentration, temperature, and regulatory basis (manufacturer IFU) all stated. Washer-disinfector Cycle 4 parameters fully documented (pre-wash, wash, thermal rinse A0 ≥ 600, drying). | — |
| CL02 | Rinse / Residue Verification | 21 CFR 820.70(e) | **PRESENT** | Step 3.5: minimum 1 minute flowing RO water rinse with 3 complete passes; Step 4.3 thermal rinse at 90 °C with A0 ≥ 600 verified by cycle printout; Step 5.1 post-wash visual inspection under minimum 1,000 lux with lumen patency check. Multi-layered verification approach appropriate for Class III. | — |
| CL03 | Non-Conformance Reporting Procedure | 21 CFR 820.90 | **INCOMPLETE** | The SOP references SOP-QC-NCR-001 for NCR initiation in several steps (Step 2.3, Step 5.2, Section 9) and states "QC NCR is initiated per SOP-QC-NCR-001 for any rejected instrument" — but does not contain within this SOP the specific steps a CSP Tech must take when a cleaning deviation occurs (e.g., WD cycle A0 failure), including who to notify, how to quarantine the lot, and required documentation actions. The full deviation response flow is not self-contained. | Add a sub-step within Step 4 (or a dedicated Step 4.5) that provides inline instructions for WD cycle failure response: (1) mark instruments as "NOT CLEAN — DO NOT STERILIZE," (2) return to quarantine, (3) notify CSP Supervisor, (4) initiate NCR in SmartSolve, (5) repeat cleaning from Step 3. For Class III, the NCR trigger and response cannot be by-reference only. |
| CL04 | Cleaning Frequency / Schedule | 21 CFR 820.70(f) | **PRESENT** | The Cleaning Frequency Schedule table (preceding Approval Signatures) defines four trigger events with specific frequencies: after each surgical case, end-of-day if unused, after repair, and for loaner sets. The loaner set clause ("regardless of supplier-provided cleaning status") shows strong contamination control awareness. | — |

---

## Reviewer Notes (Human Supplement)

1. **U10 — Quick fix** — Adding the Rev A revision history row takes under 5 minutes. Recommend combining this with any other minor updates into a Rev B rather than a standalone revision solely for this item.

2. **CL03 — WD deviation response** — The current text handles instrument rejection well but the washer-disinfector cycle failure scenario (Step 4.4 mentions "instruments are NOT clean; repeat from Step 3") does not specify NCR initiation for the cycle failure itself. WD cycle deviations on a validated process for Class III devices must be documented as NCRs, not just silent repeats.

3. **Cleaning validation cross-reference** — CVR-MAK-033-A is referenced but not described. Consider adding a note in Section 9 that the CVR is reviewed each time this SOP is revised, to ensure the SOP continues to reflect validated parameters.

4. **Loaner instruments** — The frequency schedule addresses loaners. Confirm the loaner instrument quarantine and receipt inspection steps are aligned with SOP-QC-MAK-010 (Approved Supplier List) for third-party loaner sets.

---

## AI-Assisted Review Conclusion

**AI Preliminary Assessment:** NEEDS REVISION (1 MISSING, 1 INCOMPLETE)  
**Estimated Remediation Effort:** Low — U10 is a table insertion; CL03 requires a 3–5 line inline procedure addition in Step 4  
**Human Reviewer Concurrence:** ☐ Concur  ☐ Concur with comments  ☐ Do not concur

Human Reviewer: ___________________________  Date: ___________

---

*Generated by claude-sonnet-4-6 | Anthropic API | For quality review use only — not a substitute for qualified regulatory counsel.*
