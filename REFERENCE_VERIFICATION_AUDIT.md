# Reference verification audit (R12)

Method: every reference was resolved against PubMed (NCBI E-utilities esummary) or Crossref at generation time. 44 references total: 43 resolved by PMID, 1 (Arksey & O'Malley) by Crossref DOI 10.1080/1364557032000119616.

Verification items per reference: title, authors (first 6 + et al), journal abbreviation, year, volume/issue/pages, DOI, PMID — all populated from the API response, not from memory. Machine-checkable record: /home/ubuntu/pm_work/refs_verified.json + refs_data.py.

Sample spot checks performed manually:
- Tricco 2018 = Ann Intern Med 169:467-473, doi:10.7326/M18-0850 ✓ (PRISMA-ScR checklist citation — claim supported)
- Katz 1980 = Lancet 1:512-3, "Cryoanalgesia for post-thoracotomy pain" ✓ (early thoracic direct-comparator trial — in TIER_A_COMPLETE)
- Cohen Reis 1997 = Pediatrics 100:E5, vapocoolant vs EMLA RCT, favors_comparator per dataset ✓
- Drake 2026 = Ann Surg 283:943-949, neuropathic-pain RCT ✓ (safety claim supported)
- Kehlet 2006 = Lancet 367:1618-25 ✓ (persistent postsurgical pain context)

Fabrication risk: none — every ref was API-verified. Two candidate PMIDs initially guessed wrong (Peters JBI, Trescot, Foster OSF) were caught and corrected before inclusion; Foster OSF was dropped entirely rather than cited unverified.
