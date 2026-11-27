# cryoanalgesia-la-evidence-map
Reproduction assets for a scoping review mapping primary comparative evidence of cryoanalgesic vs local-anesthetic techniques. Unit of analysis: unique patient cohort.

Post-OSF-registration rebuild (OSF DOI 10.17605/OSF.IO/KJ5RS). Sources searched 2026-11-09: MEDLINE via PubMed, CENTRAL (Cochrane Library), Scopus, ClinicalTrials.gov.

- `CANONICAL_COUNTS_FINAL_RECONCILED.*` — single source of all reported numbers (43,969 records -> 23,502 unique -> 428 primary study reports / 420 unique cohorts: Tier A 124 / B 152 / C 144; 101 synthesis reports, 40 protocols/ongoing). `CANONICAL_COUNTS_FINAL.*` is the superseded pre-reconciliation set.
- `PRIMARY_STUDY_MAP.csv`, `TIER_A_COMPLETE.csv`, `SYNTHESIS_REPORTS.csv`, `PROTOCOLS_ONGOING.csv`, `MASTER_RECORDS.csv`, `DUPLICATE_MAP.csv` — full datasets.
- `SEARCH_STRATEGIES_FULL.md`, `SEARCH_YIELDS.csv`, `SEARCH_EXPORT_MANIFEST.csv`, `CENTRAL_EXPORT_MANIFEST.csv`, `SENTINEL_RETRIEVAL_TEST.csv`, `DATA_ACQUISITION_LEDGER.csv` — search documentation.
- `PRISMA_FLOW_DATA.csv`, `PRISMA_FLOW_FINAL.png`, `Figure2_domain_tier.png`, `Figure3_year_tier.png` — figures and flow data.
- `scripts/` — post-OSF pipeline (search_post_osf, central_harvest, dedup_post, sentinel_test, screening/classification, finalize, figure/document builders), plus intermediate datasets.
- `phase_a_legacy/` — earlier pre-registration pipeline (PubMed/OpenAlex/Crossref/CT.gov), retained for audit history.

## Verify the reported counts

`python3 scripts/verify_counts.py` (Python 3 standard library; run from the repository root) recomputes the PRISMA arithmetic, report and unique-cohort counts, Tier A/B/C, the domain-by-tier table, randomized reports, Tier A effect directions, opioid and persistent-pain counts from the CSV/JSON files in this repository and checks them against `CANONICAL_COUNTS_FINAL_RECONCILED.json`. The other scripts in `scripts/` document the original pipeline; they reference the author's workspace paths and external search APIs and are not intended to be re-run as-is.
