# Hostile semantic review — RECONCILED (SUBMISSION_LOCK)

Simulated reviewers: regional anesthesiologist, thoracic anesthesiologist, pain physician, scoping-review methodologist, hostile data auditor. Executed 2026-11-09 against reconciled data.

## Questions and answers
- **Does Tier A mean the same thing in every file?** Yes. Tier A = direct interpretable LA-based comparator; enforced bidirectionally: A ⇒ LA_comparator=yes + LA-based comparator_type; LA=yes + direct comparator ⇒ A. 124 cohort-primary rows in TIER_A_COMPLETE exactly equal Tier A cohort-primary rows in PRIMARY_STUDY_MAP.
- **Can a row be LA=yes but Tier B/C without an explicit reason?** No. After adjudication all 32 flagged records were resolved: LA present only as background (epidural methadone all-arms in Roxburgh 1987), screening (diagnostic blocks in spasticity cohorts), adjunct (ESP block before cryo in Zacha 2023), constant-across-arms topical LA (split-mouth precooling), or non-analyzable mixed conventional care (Rim 2024) → comparator fields rewritten to reflect the true role.
- **Does comparator_type agree with tier?** Yes — verified by assertion; 143 rows whose text literally said "indirect comparator" were initially flagged by a substring bug in the assertion itself (fixed).
- **Does clinical_domain agree with actual procedure?** Yes — procedure_context no longer stores a contradicting domain token (135 corrected; 0 residual).
- **Are old pre-repair fields still present?** No contradicting semantic field survives; procedure_context now mirrors clinical_domain.
- **Do QC documents report real test results?** Yes — FINAL_QC_REPORT_RECONCILED.md quotes the generated test/assertion artifacts; no hand-typed "all PASS".
- **Specific records (Gate F4):** Roxburgh 1987 = B (epidural background); Rim 2024 = B (mixed conventional care, epidural option not analyzable); Mawhorter 2004 = B (placebo; EMLA background only); Soueid 2007 = **A** (Ametop arm is a direct topical-LA comparator); Cadaval Gallardo 2020 = C (no epidural given; single-arm); Zacha 2023 = **B** (adjunct ESP-block comparison, not cryo-vs-LA).

## Remaining issues
- No unresolved HIGH or MEDIUM issue. LOW residual: comparator roles for un-flagged B rows were assigned by rule + targeted adjudication rather than full-text review of all 428 (disclosed limitation); historical/epidural comparators marked LA_type="epidural analgesia (…historical)" to keep semantics explicit.

Verdict: no unresolved high/medium issue.
