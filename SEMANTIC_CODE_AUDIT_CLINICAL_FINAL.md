# SEMANTIC CODE AUDIT — clinical final (GATE C14)

Pipeline audited bidirectionally: eligibility → domain → tier → cohort → counts → manuscript → tables → figures → PRISMA.

- Eligibility: 437 → 430 retained. Exclusions: sensory/block-testing cold (3), non-analgesic cryoablation cardiac (2), no patient cohort AI eval (1), Delphi consensus (1). Evidence text and role labels in CLINICAL_SEMANTIC_ELIGIBILITY_AUDIT.csv for all 437.
- Domain: hierarchical rules obstetric→thoracic→ortho→vascular→chronic→dental→derm→periop→other; 143 reassignments + 3 manual adjudications documented in CLINICAL_DOMAIN_REAUDIT.csv; negative controls: 3 hits, all adjudicated.
- Tier: recomputed only after eligibility/domain fixes; Tier A requires LA-arm term (incl. epidural, nerve block, paravertebral, plane block, infiltration, topical LA) within 200 chars of an explicit comparative cue; non-LA comparators → B; noncomparative → C. 75 records changed tier.
- Cohort: conservative surname+domain+Jaccard≥0.35+≤5y merges recomputed after domain changes; 8 linked secondaries; 430 reports → 422 unique cohorts.
- Counts: CANONICAL_COUNTS_FINAL.json; PRISMA closes: 1,231 = 662 + 430 + 100 + 39; cohorts 422 = 430−8; tiers 131+145+146=422.
- Extraction: field validators re-run on all 430 rows (n, CI, p, follow-up); malformed → NR (documented).
- Manuscript: all numbers rendered from CANONICAL_COUNTS_FINAL.json and the regenerated tables; Table 1 sums to cohort-primary totals; obstetric_periop included.
- Tests: T1–T20 PASS.
