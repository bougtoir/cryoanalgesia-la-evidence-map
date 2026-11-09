# Public reproducibility audit — RECONCILED

Date: 2026-11-09. Method: fresh `git clone https://github.com/bougtoir/cryoanalgesia-la-evidence-map` into a clean directory; all values recomputed from cloned files only (no private inputs).

## Recomputed from clone
- PRIMARY_STUDY_MAP.csv rows: 428 primary reports; cohort-primary rows 420
- Tier A 124 / Tier B 152 / Tier C 144 (cohort-primary)
- Domain counts: thoracic_chestwall 138, vascular_access 57, chronic_pain_neurolysis 54, orthopedic_msk 46, dental_oral 36, periop_other 36, other_procedural 32, derm_office 19, obstetric_periop 10
- All equal CANONICAL_COUNTS_FINAL_RECONCILED.json values.
- Semantic assertions rerun on clone: Tier A ⇒ LA_comparator=yes + LA-based comparator_type (0 violations); no LA=yes outside Tier A (0); no procedure_context ≠ clinical_domain (0). PASS.
- PRISMA arithmetic: 1,231 = 662 + 428 + 101 + 40 (exact closure).
- Scripts in scripts/ (reconcile_final.py, tests_reconciled.py, make_figs_lock.py, build_docs_lock.py) are the exact generators.

Verdict: public clone reproduces all final canonical values.
