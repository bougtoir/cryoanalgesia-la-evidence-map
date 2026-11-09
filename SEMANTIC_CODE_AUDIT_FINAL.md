# SEMANTIC CODE AUDIT — final (GATE R12)

Scope: classification/extraction computation path post-repair. Inputs frozen (raw exports, stage2, abstracts.json).

## Estimand checks
- Unit of analysis: report-level rows in PRIMARY_STUDY_MAP (437); unique cohorts via cohort_id collapse (431); 6 linked secondary reports retained but excluded from unique-cohort counts. Tier counts are computed on cohort-primary rows only (139/153/139 = 431).
- Denominators: eligibility_assessed 1,231 = 655 excluded + 437 primary + 100 synthesis + 39 protocols. Verified by assertion in rebuild_repaired.py and by the PRISMA check script.
- Direction: effect_direction derived from abstract text patterns only; 'unclear/NR' where no pattern matched — no invented estimates (pooled review-level values cannot appear since syntheses are excluded upstream).

## Semantic fixes applied (vs prior pipeline)
1. `tag_pubtype` order bug: abstract-level 'randomized' matched before review/protocol checks -> reviews/protocols labeled RCT. Repaired: synthesis/protocol/registry/editorial types resolved BEFORE RCT; PubMed publication types take precedence.
2. Domain: noisy single-keyword domain assignment replaced by score+targeted-override (knee/genicular/infrapatellar/saphenous->orthopedic_msk; trigeminal/neuralgia/neuroma->chronic_pain_neurolysis). 188 domain corrections recorded in DOMAIN_CLASSIFICATION_AUDIT.csv.
3. Cohort: same-surname+same-domain+title-similarity+<=5y clusters conservatively merged (6 groups, 6 secondaries); uncertainty flagged, not silently counted.
4. Extraction: validators reject bare 'n=', age/cost text in follow_up, and any non-numeric sample size; p-value must match explicit p<0.x pattern; unverifiable fields = NR. 2,281 field-level corrections in SEMANTIC_EXTRACTION_AUDIT.csv.

## Hand-checked stratified sample
5 Tier A / 5 Tier B / 5 Tier C / 5 synthesis / 5 protocol rows manually reviewed against titles + types: all classifications consistent with verified publication type and comparator semantics (e.g., 1- vs 2-minute cryo dosing correctly Tier B timing comparison, not Tier A).
