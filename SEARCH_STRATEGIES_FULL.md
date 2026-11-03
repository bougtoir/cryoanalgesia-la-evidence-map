# SEARCH_STRATEGIES_FULL — cryoanalgesia vs local-anesthetic scoping review

Search date: **2026-11-03** (single dated search; no separate update search).

## Sources actually searched

| Source | Platform | Access | Status |
|--------|----------|--------|--------|
| MEDLINE | PubMed — NCBI E-utilities (esearch/esummary) | open | EXECUTED |
| OpenAlex | OpenAlex REST API, `title_and_abstract.search` field filter | open index | EXECUTED (queries OA1–OA5 complete; OA6–OA8 blocked by shared-IP daily-budget 429 — see deviations) |
| Cochrane CENTRAL | cochranelibrary.com | requires interactive web session; programmatic access blocked (HTTP 419) | NOT EXECUTED — documented gap; mitigation below |
| Scopus / Web of Science | — | no institutional subscription exists | NOT SEARCHED — OpenAlex used as the declared open-index substitute; never represented as Scopus/WoS |
| Embase | — | no genuine Embase/Ovid access exists | NOT SEARCHED — absence declared in Methods and limitations |
| ClinicalTrials.gov | API v2 | open | EXECUTED |
| WHO ICTRP | trialsearch.who.int | web portal reachable but no scriptable API (HTTP 404/000 on API endpoints) | NOT EXECUTED — documented gap; registry coverage via ClinicalTrials.gov + trial reports via PubMed/OpenAlex |
| Crossref | REST API `query.bibliographic` | open | EXECUTED (supplementary; substitutes for OpenAlex OA6–OA8) |

Mitigation for CENTRAL/ICTRP: CENTRAL contents are largely trial reports also indexed in MEDLINE/PubMed and OpenAlex, and registrations in ClinicalTrials.gov; the residual risk of missing small journal-only CENTRAL records is acknowledged as a limitation.

## Language policy (frozen, single policy)
English-language full reports only (single-reviewer workflow without translation resources). Applied identically in OSF protocol, Methods, supplement, and PRISMA exclusion reasons.

## Exact search strings and yields

### Q1_core_cryo_x_LA — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 785; Exported: 785
- Query: `CRYO=(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR ethyl chloride OR ice massage OR cold spray OR precooling OR pre-cooling OR ice pack OR ice application)[tiab] AND LA=(local anesthetic OR local anesthesia OR local anaesthetic OR local anaesthesia OR lidocaine OR mepivacaine OR bupivacaine OR ropivacaine OR levobupivacaine OR articaine OR prilocaine OR benzocaine OR EMLA OR eutectic mixture OR nerve block(s) OR epidural OR regional anesthesia/anaesthesia OR topical anesthetic/anaesthetic OR intercostal block)[tiab]`

### Q2_core_cryo_x_pain — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 3415; Exported: 3415
- Query: `CRYO AND (analgesia OR analgesic OR pain OR anesthesia OR anaesthesia)[tiab]`

### Q3_dental — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 883; Exported: 883
- Query: `CRYO AND (dental OR dentistry OR oral OR palatal OR inferior alveolar OR tooth OR endodontic)[tiab]`

### Q4_vascular — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 360; Exported: 360
- Query: `CRYO AND (venipuncture OR cannulation OR intravenous OR vascular access OR venepuncture OR phlebotomy)[tiab]`

### Q5_thoracic — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 542; Exported: 542
- Query: `CRYO AND (thoracotomy OR thoracic OR intercostal OR rib fracture(s) OR VATS OR pectus OR chest wall OR Nuss OR sternotomy)[tiab]`

### Q6_orthopedic — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 796; Exported: 796
- Query: `CRYO AND (arthroplasty OR orthopedic OR orthopaedic OR total knee OR total hip OR knee OR genicular OR spine OR musculoskeletal)[tiab]`

### Q7_derm_office — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 2437; Exported: 2437
- Query: `CRYO AND (dermatology OR dermatologic OR laser OR hair removal OR minor surgery OR office-based OR skin biopsy OR implant)[tiab]`

### Q8_ctgov_style_broad — MEDLINE/PubMed (NCBI E-utilities esearch+esummary)
- Date: 2026-11-03
- Filters: none; Language: all (English policy applied at screening); Date restriction: none
- Raw hits: 291; Exported: 291
- Query: `CRYO AND (nerve block OR epidural OR regional anesthesia OR regional anaesthesia)[tiab]`

### OA1_core_cryo_x_LA — OpenAlex (OpenAlex API filter=title_and_abstract.search (open index; declared substitute for Scopus/WoS — no subscription access))
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all (English applied at screening); Date restriction: none
- Raw hits: 1426; Exported: 1426
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND ("local anesthetic" OR "local anesthesia" OR "local anaesthesia" OR lidocaine OR bupivacaine OR ropivacaine OR mepivacaine OR EMLA OR "nerve block" OR epidural OR "regional anesthesia" OR "regional anaesthesia" OR "topical anesthetic" OR "topical anaesthetic" OR benzocaine)`

### OA2_thoracic — OpenAlex (OpenAlex API filter=title_and_abstract.search (open index; declared substitute for Scopus/WoS — no subscription access))
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all (English applied at screening); Date restriction: none
- Raw hits: 1061; Exported: 1061
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (thoracotomy OR thoracic OR intercostal OR "rib fracture" OR "rib fractures" OR pectus OR Nuss OR "chest wall" OR VATS OR sternotomy)`

### OA3_dental — OpenAlex (OpenAlex API filter=title_and_abstract.search (open index; declared substitute for Scopus/WoS — no subscription access))
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all (English applied at screening); Date restriction: none
- Raw hits: 2081; Exported: 2081
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (dental OR dentistry OR oral OR tooth OR palatal OR endodontic OR "inferior alveolar")`

### OA4_vascular — OpenAlex (OpenAlex API filter=title_and_abstract.search (open index; declared substitute for Scopus/WoS — no subscription access))
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all (English applied at screening); Date restriction: none
- Raw hits: 744; Exported: 744
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (venipuncture OR venepuncture OR cannulation OR intravenous OR "vascular access" OR phlebotomy)`

### OA5_orthopedic — OpenAlex (OpenAlex API filter=title_and_abstract.search (open index; declared substitute for Scopus/WoS — no subscription access))
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all (English applied at screening); Date restriction: none
- Raw hits: 927; Exported: 927
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (arthroplasty OR orthopedic OR orthopaedic OR "total knee" OR "total hip" OR genicular OR musculoskeletal)`

### OA6_derm_office — OpenAlex (OpenAlex API filter=title_and_abstract.search)
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all; Date restriction: none
- Raw hits: BLOCKED — OpenAlex shared-IP daily budget exhausted (HTTP 429); coverage substituted by Crossref queries CR1–CR2; Exported: 0
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (dermatology OR dermatologic OR laser OR "hair removal" OR "skin biopsy" OR "minor surgery")`

### OA7_periop — OpenAlex (OpenAlex API filter=title_and_abstract.search)
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all; Date restriction: none
- Raw hits: BLOCKED — OpenAlex shared-IP daily budget exhausted (HTTP 429); coverage substituted by Crossref queries CR1–CR2; Exported: 0
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (postoperative OR perioperative OR postsurgical) AND ("nerve block" OR epidural OR "local anesthetic" OR "regional anesthesia")`

### OA8_chronic_pain — OpenAlex (OpenAlex API filter=title_and_abstract.search)
- Date: 2026-11-03
- Filters: title_and_abstract field search; Language: all; Date restriction: none
- Raw hits: BLOCKED — OpenAlex shared-IP daily budget exhausted (HTTP 429); coverage substituted by Crossref queries CR1–CR2; Exported: 0
- Query: `(cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy) AND (neuropathic OR "chronic pain")`

### ctgov_cryoanalgesia — ClinicalTrials.gov (API v2)
- Date: 2026-11-03
- Filters: none; Language: n/a; Date restriction: none
- Raw hits: 49; Exported: 49
- Query: `cryoanalgesia`

### ctgov_cryoneurolysis — ClinicalTrials.gov (API v2)
- Date: 2026-11-03
- Filters: none; Language: n/a; Date restriction: none
- Raw hits: 62; Exported: 62
- Query: `cryoneurolysis`

### ctgov_cryoablation_AND_analgesia — ClinicalTrials.gov (API v2)
- Date: 2026-11-03
- Filters: none; Language: n/a; Date restriction: none
- Raw hits: 41; Exported: 41
- Query: `cryoablation AND analgesia`

### ctgov_cryoablation_AND_pain — ClinicalTrials.gov (API v2)
- Date: 2026-11-03
- Filters: none; Language: n/a; Date restriction: none
- Raw hits: 126; Exported: 126
- Query: `cryoablation AND pain`

### ctgov_vapocoolant — ClinicalTrials.gov (API v2)
- Date: 2026-11-03
- Filters: none; Language: n/a; Date restriction: none
- Raw hits: 34; Exported: 34
- Query: `vapocoolant`

### ctgov_ethyl_chloride_spray — ClinicalTrials.gov (API v2)
- Date: 2026-11-03
- Filters: none; Language: n/a; Date restriction: none
- Raw hits: 45; Exported: 45
- Query: `ethyl chloride spray`

### CR1_cryo_x_LA — Crossref (Crossref REST API (supplementary; substitutes for OpenAlex OA6–OA8 blocked by shared-IP 429))
- Date: 2026-11-03
- Filters: top-1000 relevance-ranked export; Language: all; Date restriction: none
- Raw hits: see query page; Exported: 1000
- Query: `cryoanalgesia cryoanesthesia cryoneurolysis vapocoolant "local anesthetic" lidocaine bupivacaine ropivacaine "nerve block" epidural`

### CR2_cryo_pain_domains — Crossref (Crossref REST API (supplementary; substitutes for OpenAlex OA6–OA8 blocked by shared-IP 429))
- Date: 2026-11-03
- Filters: top-1000 relevance-ranked export; Language: all; Date restriction: none
- Raw hits: see query page; Exported: 1000
- Query: `cryoablation cryoneurolysis intercostal pectus rib fracture dermatology laser neuropathic "chronic pain"`

## PubMed controlled vocabulary
Free-text Title/Abstract terms were used as printed above; PubMed automatically maps via Automatic Term Mapping (MeSH where applicable). No MeSH-only query was run; ATM behavior is documented here as the controlled-vocabulary pathway.

## Raw exports
All raw JSON snapshots and page-level exports are under `raw/` with the machine-readable `SEARCH_EXPORT_MANIFEST.csv` (file, bytes, sha256 recorded at fetch time).