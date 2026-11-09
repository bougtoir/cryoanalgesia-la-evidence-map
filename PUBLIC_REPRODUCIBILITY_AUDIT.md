# Public reproducibility audit (repaired)

Fresh-clone recompute from the files in this repository (2026-11-09):
- PRIMARY_STUDY_MAP rows: 437 == canonical 437 ✓
- unique cohorts: 431 == 431 ✓ (6 linked secondary reports retained)
- Tier A/B/C on cohort-primary rows: 139/153/139 ✓
- synthesis 100, protocols 39 ✓
- PRISMA: 1231 = 655 + 437 + 100 + 39 ✓
- domains: {'other_procedural': 37, 'chronic_pain_neurolysis': 65, 'orthopedic_msk': 63, 'thoracic_chestwall': 92, 'periop_other': 73, 'vascular_access': 54, 'dental_oral': 29, 'derm_office': 24}

Repair provenance: raw acquisition (43,969 / 23,502 / 4,359 / 1,231) is frozen from the registered 2026-11-09 search; repaired counts emerge from re-verified publication type, eligibility, domain, cohort, and tier logic (see audit CSVs and SEMANTIC_CLASSIFICATION_TESTS.md).
