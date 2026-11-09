# Full search strategies — post-OSF rebuild

Protocol: OSF DOI 10.17605/OSF.IO/KJ5RS (registered 2026-11-06, before this search and rescreening).
Search date: 2026-11-09 (all sources). Language policy: English full text only, applied at screening; no language or geographic filters were applied to any search. No date restrictions were applied.

Registered sources (frozen): 1. MEDLINE via PubMed, 2. CENTRAL (Cochrane Library), 3. Scopus, 4. ClinicalTrials.gov. No other sources were searched.

Deduped contribution = number of unique post-dedup records in MASTER_RECORDS.csv whose query list includes the query id.

## MEDLINE via PubMed — platform: NCBI E-utilities

### Q1_core_cryo_x_LA

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND ("local anesthetic"[tiab] OR "local anesthesia"[tiab] OR "local anaesthetic"[tiab] OR "local anaesthesia"[tiab] OR lidocaine[tiab] OR mepivacaine[tiab] OR bupivacaine[tiab] OR ropivacaine[tiab] OR levobupivacaine[tiab] OR articaine[tiab] OR prilocaine[tiab] OR benzocaine[tiab] OR EMLA[tiab] OR "eutectic mixture"[tiab] OR "nerve block"[tiab] OR "nerve blocks"[tiab] OR epidural[tiab] OR "regional anesthesia"[tiab] OR "regional anaesthesia"[tiab] OR "topical anesthetic"[tiab] OR "topical anaesthetic"[tiab] OR "intercostal block"[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 789 | Exported: 789 | Deduped contribution: 786
- Export file: `exports/pubmed_Q1_core_cryo_x_LA.json`

### Q2_core_cryo_x_pain

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND (analgesia[tiab] OR analgesic[tiab] OR pain[tiab] OR anesthesia[tiab] OR anaesthesia[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 3425 | Exported: 3425 | Deduped contribution: 3402
- Export file: `exports/pubmed_Q2_core_cryo_x_pain.json`

### Q3_dental

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND (dental[tiab] OR dentistry[tiab] OR "oral"[tiab] OR palatal[tiab] OR "inferior alveolar"[tiab] OR tooth[tiab] OR endodontic[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 884 | Exported: 884 | Deduped contribution: 881
- Export file: `exports/pubmed_Q3_dental.json`

### Q4_vascular

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND (venipuncture[tiab] OR cannulation[tiab] OR "intravenous"[tiab] OR "vascular access"[tiab] OR venepuncture[tiab] OR phlebotomy[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 361 | Exported: 361 | Deduped contribution: 359
- Export file: `exports/pubmed_Q4_vascular.json`

### Q5_thoracic

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND (thoracotomy[tiab] OR thoracic[tiab] OR intercostal[tiab] OR "rib fracture"[tiab] OR "rib fractures"[tiab] OR VATS[tiab] OR pectus[tiab] OR "chest wall"[tiab] OR Nuss[tiab] OR sternotomy[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 545 | Exported: 545 | Deduped contribution: 543
- Export file: `exports/pubmed_Q5_thoracic.json`

### Q6_orthopedic

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND (arthroplasty[tiab] OR orthopedic[tiab] OR orthopaedic[tiab] OR "total knee"[tiab] OR "total hip"[tiab] OR knee[tiab] OR genicular[tiab] OR spine[tiab] OR musculoskeletal[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 798 | Exported: 798 | Deduped contribution: 791
- Export file: `exports/pubmed_Q6_orthopedic.json`

### Q7_derm_office

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND (dermatology[tiab] OR dermatologic[tiab] OR laser[tiab] OR "hair removal"[tiab] OR "minor surgery"[tiab] OR "office-based"[tiab] OR "skin biopsy"[tiab] OR implant[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 2438 | Exported: 2438 | Deduped contribution: 2400
- Export file: `exports/pubmed_Q7_derm_office.json`

### Q8_broad_block

```
("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab]) AND ("nerve block"[tiab] OR epidural[tiab] OR "regional anesthesia"[tiab] OR "regional anaesthesia"[tiab])
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 292 | Exported: 292 | Deduped contribution: 290
- Export file: `exports/pubmed_Q8_broad_block.json`

## Scopus — platform: Elsevier Scopus Search API (apiKey)

### S1_core_cryo_x_LA

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY("local anesthetic" OR "local anesthesia" OR "local anaesthetic" OR "local anaesthesia" OR lidocaine OR mepivacaine OR bupivacaine OR ropivacaine OR levobupivacaine OR articaine OR prilocaine OR benzocaine OR EMLA OR "eutectic mixture" OR "nerve block" OR epidural OR "regional anesthesia" OR "regional anaesthesia" OR "topical anesthetic" OR "topical anaesthetic" OR "intercostal block")
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 2839 | Exported: 2839 | Deduped contribution: 2812
- Export file: `exports/scopus_S1_core_cryo_x_LA.json`

### S2_core_cryo_x_pain

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY(analgesia OR analgesic OR pain OR anesthesia OR anaesthesia)
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 10936 | Exported: 10936 | Deduped contribution: 10790
- Export file: `exports/scopus_S2_core_cryo_x_pain.json`
- PUBYEAR partitioning (Scopus apiKey 5000-record cap): partitions by PUBYEAR: y1913to1969,y1970to1997,y1998to2011,y2012to2018,y2019to2026,ybef1913

### S3_dental

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY(dental OR dentistry OR oral OR palatal OR "inferior alveolar" OR tooth OR endodontic)
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 2387 | Exported: 2387 | Deduped contribution: 2362
- Export file: `exports/scopus_S3_dental.json`

### S4_vascular

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY(venipuncture OR cannulation OR intravenous OR "vascular access" OR venepuncture OR phlebotomy)
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 1389 | Exported: 1389 | Deduped contribution: 1380
- Export file: `exports/scopus_S4_vascular.json`

### S5_thoracic

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY(thoracotomy OR thoracic OR intercostal OR "rib fracture" OR "rib fractures" OR VATS OR pectus OR "chest wall" OR Nuss OR sternotomy)
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 2062 | Exported: 2062 | Deduped contribution: 2033
- Export file: `exports/scopus_S5_thoracic.json`

### S6_orthopedic

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY(arthroplasty OR orthopedic OR orthopaedic OR "total knee" OR "total hip" OR knee OR genicular OR spine OR musculoskeletal)
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 2831 | Exported: 2831 | Deduped contribution: 2804
- Export file: `exports/scopus_S6_orthopedic.json`

### S7_derm_office

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY(dermatology OR dermatologic OR laser OR "hair removal" OR "minor surgery" OR "office-based" OR "skin biopsy" OR implant)
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 9909 | Exported: 9909 | Deduped contribution: 9616
- Export file: `exports/scopus_S7_derm_office.json`
- PUBYEAR partitioning (Scopus apiKey 5000-record cap): partitions by PUBYEAR: y1913to1969,y1970to1997,y1998to2011,y2012to2018,y2019to2026,ybef1913

### S8_broad_block

```
TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application") AND TITLE-ABS-KEY("nerve block" OR epidural OR "regional anesthesia" OR "regional anaesthesia")
```
- Executed: 2026-11-09 | Filters: none (English eligibility at screening per protocol) | Date restriction: none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail) | Language: unfiltered at search, English-only at screening
- Raw hits: 1100 | Exported: 1100 | Deduped contribution: 1091
- Export file: `exports/scopus_S8_broad_block.json`

## CENTRAL — platform: Cochrane Library web, human-cleared session, DOM capture (citation export login-gated)

### C1_core_cryo

```
cryoanalgesia OR "cryoneurolysis" OR "cryoneurotomy" OR "cryo nerve block" OR "cryogenic nerve block" OR "nerve cryoablation" OR "intercostal cryoanalgesia" OR "cryoablation of nerves"
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 189 | Exported: 189 | Deduped contribution: 186
- Export file: `exports/central_C1_core_cryo.json`

### C2_cryo_x_pain

```
(cryo* NEAR/3 (analgesia OR analgesic OR "nerve block" OR neurolysis OR "pain management" OR "postoperative pain"))
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 183 | Exported: 183 | Deduped contribution: 178
- Export file: `exports/central_C2_cryo_x_pain.json`

### C3_dental

```
(cryoanalgesia OR cryoneurolysis OR cryoablation) AND (dental OR dentistry OR "third molar" OR tonsillectomy OR "oral surgery" OR alveolar)
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 4 | Exported: 4 | Deduped contribution: 4
- Export file: `exports/central_C3_dental.json`

### C4_vascular

```
(cryoanalgesia OR cryoneurolysis) AND (vascular OR "varicose vein" OR endovenous OR amputation OR "limb ischemia")
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 11 | Exported: 11 | Deduped contribution: 11
- Export file: `exports/central_C4_vascular.json`

### C5_thoracic

```
(cryoanalgesia OR cryoneurolysis OR "intercostal cryo*") AND (thoracotomy OR thoracic OR thoracoscopy OR sternotomy OR pectus OR "rib fracture" OR Nuss OR mammary)
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 77 | Exported: 77 | Deduped contribution: 76
- Export file: `exports/central_C5_thoracic.json`

### C6_orthopedic

```
(cryoanalgesia OR cryoneurolysis) AND (orthopedic OR "knee arthroplasty" OR "total knee" OR "total hip" OR arthroscopy OR spine OR laminectomy OR "joint replacement")
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 22 | Exported: 22 | Deduped contribution: 22
- Export file: `exports/central_C6_orthopedic.json`

### C7_derm_neuro

```
(cryoanalgesia OR cryoneurolysis OR cryoablation) AND (dermatolog* OR skin OR neuroma OR neuropathy OR "post-herpetic" OR postherpetic OR pudendal OR occipital OR supraorbital)
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 51 | Exported: 51 | Deduped contribution: 51
- Export file: `exports/central_C7_derm_neuro.json`

### C8_LA_x_cryo

```
("local anesthe*" OR lidocaine OR bupivacaine OR ropivacaine OR "nerve block") AND (cryoanalgesia OR cryoneurolysis OR "cryo ablation" OR cryoablation)
```
- Executed: 2026-11-09 | Filters: field=Title Abstract Keyword (searchBy=1); word variations searched (site default) | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 85 | Exported: 85 | Deduped contribution: 84
- Export file: `exports/central_C8_LA_x_cryo.json`

## ClinicalTrials.gov — platform: CT.gov API v2

### T1_cryoanalgesia

```
cryoanalgesia
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 50 | Exported: 50 | Deduped contribution: 50
- Export file: `exports/ctgov_T1_cryoanalgesia.json`

### T2_cryoneurolysis

```
cryoneurolysis
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 62 | Exported: 62 | Deduped contribution: 62
- Export file: `exports/ctgov_T2_cryoneurolysis.json`

### T3_cryoablation_pain

```
cryoablation AND pain
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 126 | Exported: 126 | Deduped contribution: 126
- Export file: `exports/ctgov_T3_cryoablation_pain.json`

### T4_cryoablation_analgesia

```
cryoablation AND analgesia
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 41 | Exported: 41 | Deduped contribution: 41
- Export file: `exports/ctgov_T4_cryoablation_analgesia.json`

### T5_vapocoolant

```
vapocoolant
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 34 | Exported: 34 | Deduped contribution: 34
- Export file: `exports/ctgov_T5_vapocoolant.json`

### T6_ethyl_chloride

```
"ethyl chloride" spray
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 44 | Exported: 44 | Deduped contribution: 44
- Export file: `exports/ctgov_T6_ethyl_chloride.json`

### T7_cryoanesthesia

```
cryoanesthesia OR cryoanaesthesia
```
- Executed: 2026-11-09 | Filters: none | Date restriction: none | Language: unfiltered at search, English-only at screening
- Raw hits: 5 | Exported: 5 | Deduped contribution: 5
- Export file: `exports/ctgov_T7_cryoanesthesia.json`

## CENTRAL retrieval method note

CENTRAL was searched via the Cochrane Library web UI basic-search portlet (field scope 'Title Abstract Keyword', word variations on) using a human-cleared browser session; result records were captured from the search-result DOM (title, authors, metadata, CN DOI / external database references) because citation export is login-gated. All page HTML is preserved under raw/central_*.

## Known acquisition anomalies

- Scopus S2 and S7 exceeded the apiKey 5000-record window and were fetched in PUBYEAR partitions (see partition_detail in SEARCH_EXPORT_MANIFEST.csv).
- During manifest rebuild a tooling bug briefly re-ran the PubMed queries once, overwriting that day's PubMed raw files in place. Queries, dates, and data were identical (idempotent re-fetch); no data loss, but the raw file mtimes for PubMed reflect the re-run. Recorded here for audit honesty.
- raw_truncated_s2/ holds partial pages from the first S2 attempt that hit the 5000-record cap before PUBYEAR partitioning was implemented; superseded by the complete partitioned export.