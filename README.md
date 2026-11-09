# cryoanalgesia-la-evidence-map
Reproduction assets for a scoping review mapping primary comparative evidence of cryoanalgesic vs local-anesthetic techniques. Unit of analysis: unique patient cohort.

Post-OSF-registration rebuild (OSF DOI 10.17605/OSF.IO/KJ5RS). Sources searched 2026-11-09: MEDLINE via PubMed, CENTRAL (Cochrane Library), Scopus, ClinicalTrials.gov.

- `CANONICAL_COUNTS.*` — single source of all reported numbers (43,969 records -> 23,502 unique -> 429 primary study reports: Tier A 143 / B 176 / C 110; 27 synthesis, 26 protocols).
- `PRIMARY_STUDY_MAP.csv`, `TIER_A_COMPLETE.csv`, `SYNTHESIS_REPORTS.csv`, `PROTOCOLS_ONGOING.csv`, `MASTER_RECORDS.csv`, `DUPLICATE_MAP.csv` — full datasets.
- `SEARCH_STRATEGIES_FULL.md`, `SEARCH_YIELDS.csv`, `SEARCH_EXPORT_MANIFEST.csv`, `CENTRAL_EXPORT_MANIFEST.csv`, `SENTINEL_RETRIEVAL_TEST.csv`, `DATA_ACQUISITION_LEDGER.csv` — search documentation.
- `PRISMA_FLOW_DATA.csv`, `PRISMA_FLOW_FINAL.png`, `Figure2_domain_tier.png`, `Figure3_year_tier.png` — figures and flow data.
- `scripts/` — post-OSF pipeline (search_post_osf, central_harvest, dedup_post, sentinel_test, screening/classification, finalize, figure/document builders), plus intermediate datasets.
- `phase_a_legacy/` — earlier pre-registration pipeline (PubMed/OpenAlex/Crossref/CT.gov), retained for audit history.
