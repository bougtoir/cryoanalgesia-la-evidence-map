# FINAL QC REPORT — RECONCILED (SUBMISSION_LOCK)

Generated 2026-11-09 from actual machine output (SEMANTIC_CLASSIFICATION_TESTS_RECONCILED.md and CANONICAL_SEMANTIC_ASSERTIONS.md are the test artifacts; this report does not restate results by hand).

## Canonical counts (CANONICAL_COUNTS_FINAL_RECONCILED.json — sole source)
- Primary study reports: 428 | Unique cohorts: 420 (linked secondary reports: 8)
- Tier A 124 / Tier B 152 / Tier C 144 (cohort-primary rows)
- Synthesis reports: 101 | Protocols/ongoing: 40
- PRISMA: 1,231 eligibility-assessed = 662 excluded + 428 primary + 101 synthesis + 40 protocols (exact closure)
- Search stage frozen: 43,969 raw → 23,502 dedup → 4,359 abstract-assessed → 1,231 eligibility-assessed

## What this reconciliation pass changed
- F2 domain/context: 135 procedure_context values replaced (stale pre-repair domain tokens → reconciled clinical_domain). Zero unresolved contradictions.
- F3/F4 tier/comparator: 32 flagged records adjudicated against source abstracts; all 32 changed. 3 promoted to Tier A (Soueid ethyl chloride vs Ametop; refrigerated cartridge vs benzocaine; ShotBlocker trial's LA-infiltration arm), 11 demoted A→B (placebo/sham/adjunct/non-LA comparators), 1 B→C (single-arm SEF cohort), 1 C→B (ESP-block adjunct comparison), plus comparator_type/LA fields corrected on all.
- Publication-type escapees: narrative review R2703fc3a9f → SYNTHESIS_REPORTS; trial-design publication Rd82babbea1 → PROTOCOLS_ONGOING.
- Counts therefore changed from the FINAL candidate (430/422/A131/B145/C146/100/39) to 428/420/A124/B152/C144/101/40.

## Test execution (quoted from SEMANTIC_CLASSIFICATION_TESTS_RECONCILED.md)
```
ALL PASS (T1-T20)
```
All T1–T20 PASS, including T17 (knee OA → orthopedic_msk) and T18 (trigeminal → chronic_pain_neurolysis). The earlier FINAL report's T17/T18 FAIL was a stale test-report artifact; re-executing the tests on the `clinical_domain` field confirms the reconciled data satisfies both assertions.

## Canonical assertions (quoted from CANONICAL_SEMANTIC_ASSERTIONS.md)
```
ALL PASS
```
All assertions PASS: Tier A ⟺ direct LA comparator bidirectionally consistent; no review/protocol contamination; no stale domain tokens; TIER_A_COMPLETE exactly equals Tier A cohort-primary rows.

## QC verdict
ALL PASS. SUBMIT permitted.
