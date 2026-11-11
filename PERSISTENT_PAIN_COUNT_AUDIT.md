# Persistent-pain count audit (Gate S14)

Bug: manuscript read "Among the 124 Tier A reports ... an explicit persistent-pain outcome definition appeared in 125."

Root cause (generator, not data): `persist_A` counted non-empty `persistent_pain_definition` strings — including the literal "NR" placeholder — over all 125 report-level Tier A rows, while the sentence's denominator was the 124 cohort-primary rows. Two unit errors compounded: wrong numerator rule (non-empty ≠ defined) and wrong denominator (reports vs cohorts).

Correct estimand: unique-cohort level.
- Denominator: 124 cohort-primary Tier A cohorts (TIER_A_COMPLETE.csv rows = 124).
- Numerator: cohort-primary Tier A rows whose `persistent_pain_definition` field is neither empty nor "NR" = 10 (verbatim entries: phantom-pain persistence note, LANSS at 2 weeks, neuropathic-pain outcomes at 8 weeks/6 months, etc.).
- Source field: `persistent_pain_definition` in PRIMARY_STUDY_MAP.csv (verbatim, may contain "NR").
- Linked-secondary treatment: linked secondary reports are never counted (cohort-primary filter `cohort_id == study_id`).
- Opioid outcomes likewise recomputed at cohort-primary level: 41 of 124.

Final manuscript wording (regenerated): "Opioid outcomes were reported in 41 Tier A cohorts; an explicit persistent-pain outcome definition appeared in 10."

Data frozen: no classification changed; this was a derived-output bug only.
