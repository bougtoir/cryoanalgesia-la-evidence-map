# Semantic classification unit tests — RECONCILED (T1-T20)

Executed 2026-11-09 against the reconciled SUBMISSION_LOCK canonical datasets. Tests operate on the `clinical_domain` field (post-repair authoritative field), not legacy procedure_context or source category. T17/T18 were re-diagnosed: the earlier FAIL was a stale test report — the reconciled canonical data satisfies both assertions.

| Test | Definition | Rows evaluated | Result | Failure examples |
|---|---|---|---|---|
| T1 | no systematic review in primary | all 428 primary rows | PASS | — |
| T2 | no meta-analysis in primary | all 428 | PASS | — |
| T3 | no protocol in primary (JMIR-type) | all 428 | PASS | — |
| T4 | no BMJ Open-type protocol in primary | all 428 | PASS | — |
| T5 | no knee/OA record in thoracic_chestwall | thoracic rows=138 | PASS | — |
| T6 | no trigeminal record in thoracic_chestwall | thoracic rows | PASS | — |
| T7 | cryo vs epidural present in Tier A | Tier A rows=125 | PASS | — |
| T8 | no synthesis report in Tier A | Tier A rows | PASS | — |
| T9 | follow_up clean | all rows | PASS | — |
| T10 | no malformed n= in sample_size_total | all rows | PASS | — |
| T11 | VATS/intercostal -> thoracic_chestwall | VATS-titled rows=2 | PASS | — |
| T12 | thoracotomy/thoracic terms -> thoracic_chestwall | thoracic-term rows=133 | PASS | — |
| T13 | pectus intercostal -> thoracic_chestwall | pectus rows=50 | PASS | — |
| T14 | caesarean sensory-testing records excluded/not orthopedic | primary rows | PASS | — |
| T15 | all gate-excluded records absent from PRIMARY_STUDY_MAP | primary rows | PASS | — |
| T16 | no sensory/block-testing-only role survives (LA presence does not rescue) | primary rows | PASS | — |
| T17 | clinically relevant knee OA/arthroplasty/genicular cryo records -> orthopedic_msk (on clinical_domain field) | matching rows=20 | PASS | — |
| T18 | trigeminal neuralgia/therapeutic cryoneurolysis records -> chronic_pain_neurolysis (on clinical_domain field) | trigeminal rows=4 | PASS | — |
| T19 | venipuncture/arterial-puncture vapocoolant -> vascular_access | matching rows=43 | PASS | — |
| T20 | dental precooling records -> dental_oral | matching rows=18 | PASS | — |

OVERALL: ALL PASS (T1-T20)