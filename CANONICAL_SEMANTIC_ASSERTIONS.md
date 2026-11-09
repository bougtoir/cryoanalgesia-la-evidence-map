# Canonical semantic assertions — RECONCILED

Generated programmatically from PRIMARY_STUDY_MAP.csv / TIER_A_COMPLETE.csv / CANONICAL_COUNTS_FINAL_RECONCILED.json.

| Assertion | Count checked | Failures | Result | Examples |
|---|---|---|---|---|
| Tier A => LA_comparator_yes_no == yes | 125 | 0 | PASS | — |
| Tier A => comparator_type compatible with direct LA comparison | 125 | 0 | PASS | — |
| LA_comparator_yes_no==yes AND comparator_type contains 'direct'/'LA-based' => Tier A | 125 | 0 | PASS | — |
| Tier B/C => comparator_type does not claim direct LA comparator | 303 | 0 | PASS | — |
| clinical_domain does not contradict procedure_context | 428 | 0 | PASS | — |
| no excluded sensory-testing record in PRIMARY_STUDY_MAP | 428 | 0 | PASS | — |
| no review/protocol in PRIMARY_STUDY_MAP | 428 | 0 | PASS | — |
| no review/protocol in TIER_A_COMPLETE | 124 | 0 | PASS | — |
| TIER_A_COMPLETE rows == Tier A cohort-primary rows | 124 | 0 | PASS | — |
| no stale old-domain token contradicting clinical_domain in any semantic field | 428 | 0 | PASS | — |

OVERALL: ALL PASS