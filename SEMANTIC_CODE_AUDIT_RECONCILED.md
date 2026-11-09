# Semantic code audit — RECONCILED

Scope: SUBMISSION_LOCK reconciliation scripts (`~/pm_work/post_osf/reconcile_final.py`, `tests_reconciled.py`, `make_figs_lock.py`, `~/pm_work/build_docs_lock.py`).

## Findings
1. **Field authority**: `clinical_domain` is the sole domain field; `procedure_context` previously stored stale pre-repair domain tokens (135 contradictions) — now replaced with `clinical_domain`. No record retains a domain-token procedure_context that differs from clinical_domain (assertion-verified).
2. **Tier/comparator consistency**: 32 flagged records adjudicated from source abstracts; after adjudication `evidence_tier`, `comparator_type`, `LA_comparator_yes_no`, `LA_type` form coherent tuples — verified by bidirectional assertions (Tier A ⟺ LA_comparator=yes + LA-based comparator_type).
3. **Tests**: T1–T20 PASS (generated file SEMANTIC_CLASSIFICATION_TESTS_RECONCILED.md). T1 initially failed on real data (narrative review R2703fc3a9f) — record moved to SYNTHESIS_REPORTS and rerun passes. T19 regex was over-broad ("intravenous" matched thoracic IV-analgesia arms) — pattern narrowed to access-procedure terms and rerun.
4. **Assertions**: all PASS (CANONICAL_SEMANTIC_ASSERTIONS.md). One assertion-implementation bug found and fixed: `"direct comparator" in s` matched the substring inside `"indirect comparator"`; replaced with `(?<!in)direct comparator`.
5. **Counts**: all derived from reconciled rows — 428 reports / 420 cohorts / A 124 / B 152 / C 144 / synth 101 / proto 40. No count is preserved or hardcoded.
6. **Frozen elements untouched**: search yields, dedup, pubtype repair, eligibility exclusions (662), protocol/OSF text, acquisition ledger.
7. **Residual limitation**: comparator semantics for un-flagged B/C rows were corrected en masse in the earlier C-pass; this pass re-adjudicated the 32 contradicted rows plus test-discovered escapees. Stratified manual re-abstraction of all 428 remains a scoping-review limitation (single reviewer + AI clerical), disclosed in the manuscript.

Verdict: code produces the stated outputs; tests and assertions consume live data.
