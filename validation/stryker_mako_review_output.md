# Example SOP Review Output — Stryker Mako RIO Inspection SOP

**SOP File:** `examples/stryker_mako_inspection_sop.txt`  
**Document Number:** SOP-QC-MAK-042, Rev. C  
**Review Date:** 2026-05-11  
**Device Class:** III (Mako RIO Robotic Surgical System — 510(k) K163360 / PMA P150002)  
**SOP Type:** `inspection`  
**Model:** `claude-sonnet-4-6`  
**CLI Command:**

```bash
python sop_review.py \
  --file examples/stryker_mako_inspection_sop.txt \
  --sop-type inspection \
  --device-class III \
  --output validation/stryker_mako_review_report.pdf
```

> **Note:** This document reproduces the structured findings that the tool generates in PDF form. It is provided as a readable reference alongside the PDF report. For audit use, reference the signed PDF report.

---

## Overall GMP Readiness

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│             READY FOR QA REVIEW                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Rationale:** The SOP comprehensively addresses all 15 checklist items (11 universal + 4 inspection-specific) with specific regulatory citations, quantitative acceptance criteria, ANSI/ASQ Z1.4 sampling plan references, and a complete revision history and approval block. No critical gaps were identified. The document is appropriate for a Class III device under 21 CFR Part 820.

---

## Summary Scorecard

| Total Items | PRESENT | INCOMPLETE | MISSING | Pass Rate |
|:-----------:|:-------:|:----------:|:-------:|:---------:|
| 15 | 15 | 0 | 0 | **100%** |

---

## Detailed Compliance Findings

### Universal Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| U01 | Purpose Statement | 21 CFR 820.40 | **PRESENT** | *"This procedure defines the incoming inspection requirements for Mako RIO Robotic Intelligent Orthopaedic (RIO) robotic arm subassembly components received from contract manufacturers, to verify dimensional conformance, surface integrity, and labeling accuracy prior to acceptance into inventory..."* | — |
| U02 | Scope | 21 CFR 820.40 | **PRESENT** | *"This SOP applies to all incoming lots of the following Mako RIO subassembly components: Robotic arm link castings (Part Nos. MK-ARM-101 through MK-ARM-106), Force/torque sensor modules (Part No. MK-FTS-220), End-effector coupling assemblies (Part No. MK-EFC-310)..."* Scope explicitly states what is excluded (SOP-QC-MAK-055). | — |
| U03 | Responsibilities | 21 CFR 820.20(b) | **PRESENT** | Distinct responsibilities defined for QC Inspection Technician, QC Engineer, QA Manager, and Receiving/Materials Management — including who performs, who reviews, who approves, and escalation path for borderline findings. | — |
| U04 | References | 21 CFR 820.40 | **PRESENT** | References section includes regulatory citations (21 CFR 820.50, 820.80, 820.72, 21 CFR 803), standards (ANSI/ASQ Z1.4, ISO 13485, ASME B46.1, ASME Y14.5), and 7 internal controlled documents including drawings and material specifications. | — |
| U05 | Definitions / Abbreviations | 21 CFR 820.3 | **PRESENT** | 15 terms defined including AQL, CMM, CoC, DHR, GD&T, NCR — all acronyms used in the procedure body are accounted for in Section 5. | — |
| U06 | Materials and Equipment List | 21 CFR 820.70(g) | **PRESENT** | Section 6 enumerates all calibrated instruments with specific calibration tag IDs (e.g., MIT-0042, STR-0019), as well as reference documents, consumables, and supplies. Calibration currency requirement explicitly stated ("do NOT use equipment with expired calibration"). | — |
| U07 | Safety Precautions / PPE Requirements | 21 CFR 820.70(e) | **PRESENT** | Section 7 specifies required PPE (gloves, safety glasses, steel-toed shoes) with rationale, handling precautions for heavy and sensitive components, and chemical hazard for IPA including SDS reference. | — |
| U08 | Step-by-Step Procedure | 21 CFR 820.40 | **PRESENT** | Eight numbered steps in action-verb format cover: quarantine verification, document/lot check, AQL sample selection, visual/surface inspection, CMM dimensional inspection, FTS functional check, disposition decision, and documentation filing. Steps reference specific forms and calibration requirements inline. | — |
| U09 | Documentation / Forms / Records | 21 CFR 820.180 | **PRESENT** | Section 9 specifies Form QC-IIR-042 (IIR), NCR Form QC-NCR-001, CMM data file archiving location, and CoC/packing slip retention. Retention period stated as "device useful life + 2 years" per 21 CFR 820.180. | — |
| U10 | Revision History Table | 21 CFR 820.40(b) | **PRESENT** | Section 10 contains a complete revision history table with Revision letter, Date, Author (with role), and Change Summary for all three revisions (A, B, C). Change summaries are specific and reference DRB action items where applicable. | — |
| U11 | Approval Signatures Block | 21 CFR 820.40(a) | **PRESENT** | Signature block includes Prepared By (QC Manager), Reviewed By (Regulatory Affairs Specialist), and Approved By (VP Quality Assurance) with signature lines and date fields. Roles are appropriate for a Class III device SOP. | — |

### Inspection-Specific Checklist Items

| ID | Checklist Item | Reg. Section | Status | Evidence | Recommendation |
|---|---|---|---|---|---|
| I01 | Acceptance Criteria | 21 CFR 820.80(d) | **PRESENT** | Quantitative accept/reject criteria specified throughout: Ra ≤ 0.8 µm for surface finish (Step 4.2), >0.1 mm depth = reject for scratches on product-contact surfaces (Step 4.1c), ±1.5% deviation limit for FTS functional check (Step 6.3), AQL 1.0 for critical dimensions and AQL 4.0 for cosmetic (Step 3.2). Critical feature out-of-tolerance = automatic reject stated explicitly (Step 5.5). All criteria reference CAC-MAK-042, Rev. C as the governing document. | — |
| I02 | Sampling Plan Reference | 21 CFR 820.80(c) | **PRESENT** | *"Using ANSI/ASQ Z1.4, Inspection Level II, AQL 1.0 for critical dimensions and AQL 4.0 for visual/cosmetic attributes"* — standard, level, and AQL values all specified. Sampling method (systematic random, k-th unit formula) also described (Step 3.3). | — |
| I03 | Inspection Equipment / Gauges | 21 CFR 820.72 | **PRESENT** | Section 6.1 lists all measurement instruments with serial numbers, calibration tag IDs, and requirement to verify current calibration before use. CMM program file name specified (MAK_ARM_101_Rev_C.prg). | — |
| I04 | Disposition Authority | 21 CFR 820.80(a) | **PRESENT** | Step 7.2 and 7.3 explicitly define disposition authority: QC Engineer signs to authorize release (Accept) and initiates NCR for rejections. QA Manager authorizes deviations or concessions. Rejected lots go to NCR/DRB process per SOP-QC-NCR-001. | — |

---

## Reviewer Notes (Human Supplement — Not AI Generated)

The following observations were added by the human QA reviewer after receiving the AI report:

1. **Step 6 scope gate** — The FTS functional check (Step 6) includes a clear "skip if not MK-FTS-220" instruction. Claude correctly identified all FTS items as PRESENT. Confirm this gate is also represented in Form QC-IIR-042 (Section 5 should have N/A fields for non-FTS lots).

2. **QMSR transition** — This SOP cites 21 CFR Part 820 in its pre-2026 form. As the QMSR (21 CFR Part 820, as amended) takes effect February 2, 2026, the references section should be reviewed against the new ISO 13485-aligned structure before the next scheduled revision.

3. **Drawing revision alignment** — The SOP references DWG-MAK-ARM-101-C. Confirm the drawing revision (Rev C) is still the current released revision in your EDMS before approving this SOP revision.

4. **ERP system reference** — Step 1.3 references "the ERP system" without naming the specific system or transaction code. Consider adding the ERP system name and PO lookup transaction for procedural clarity, especially during onboarding of new technicians.

---

## AI-Assisted Review Conclusion

The Stryker Mako RIO Inspection SOP (SOP-QC-MAK-042, Rev. C) is a well-structured, comprehensive document that addresses all 21 CFR Part 820 checklist requirements evaluated by this tool. It is appropriate as a **reference/training SOP** to calibrate the tool's assessment of what a high-quality Class III device inspection SOP looks like.

**AI Preliminary Assessment:** READY FOR QA REVIEW  
**Human Reviewer Concurrence:** ☐ Concur  ☐ Concur with comments  ☐ Do not concur

Human Reviewer: ___________________________  Date: ___________

---

*Generated by claude-sonnet-4-6 | Anthropic API | For quality review use only — not a substitute for qualified regulatory counsel.*
