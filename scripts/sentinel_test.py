#!/usr/bin/env python3
"""GATE 3: sentinel retrieval test. Sentinel set = 4 named studies + all legacy
Tier A direct-comparator studies. Checks presence in each source's raw exports."""
import csv, json, os, re
BASE = "/home/ubuntu/pm_work/post_osf"; EXP = f"{BASE}/exports"
LEG = "/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_submission_rebuild"

def norm(t):
    t = (t or "").lower(); t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

# index raw exports
idx = {"PubMed": set(), "CENTRAL": set(), "Scopus": set(), "ClinicalTrials": set()}
idx_pm = {"PubMed": set(), "CENTRAL": set(), "Scopus": set(), "ClinicalTrials": set()}
idx_doi = {"PubMed": set(), "CENTRAL": set(), "Scopus": set(), "ClinicalTrials": set()}
for fn in sorted(os.listdir(EXP)):
    src = {"pubmed": "PubMed", "scopus": "Scopus", "central": "CENTRAL", "ctgov": "ClinicalTrials"}[fn.split("_")[0]]
    for r in json.load(open(f"{EXP}/{fn}")):
        idx[src].add(norm(r.get("title", ""))[:110])
        if r.get("pmid"): idx_pm[src].add(str(r["pmid"]))
        d = (r.get("doi") or r.get("cn_doi") or "").lower()
        if d: idx_doi[src].add(d)

sents = []
named = [
    ("S-COPPER", "Bastianello M et al. Paediatr Anaesth. 2025;35:347-358 (COPPER RCT)",
     "10.1111/pan.15090", "40035332", "Cryoanalgesia for Pain Management After Pectus Excavatum Repair (COPPER) in Adolescents: A Randomized Controlled Trial."),
    ("S-EJPS2024", "van Braak H et al. Eur J Pediatr Surg. 2024;34:488-492", "", "38242172", ""),
    ("S-JPS2020", "Dekonenko C et al. J Pediatr Surg. 2020;55:1444-1447", "", "31699436", ""),
    ("S-EJPSRCT", "Rim GM et al. Eur J Pediatr Surg. 2024;34:338-345", "", "37364610", ""),
]
# pull titles for named PMIDs from PubMed export
pm_title = {}
for fn in os.listdir(EXP):
    if fn.startswith("pubmed_"):
        for r in json.load(open(f"{EXP}/{fn}")):
            pm_title[str(r.get("pmid"))] = r.get("title", "")
for sid, cite, doi, pm, t in named:
    sents.append((sid, cite, doi, pm, pm_title.get(pm, t), "eligible_central"))
tier_a = list(csv.DictReader(open(f"{LEG}/TIER_A_COMPLETE.csv")))
for r in tier_a:
    sents.append((r["study_id"], r["primary_citation"], r["doi"], r["pmid"],
                  r["title"], "eligible_tierA_comparator"))

rows = []
fails = []
for sid, cite, doi, pm, title, exp in sents:
    nt = norm(title)[:110]
    got = {}
    route = []
    for src in idx:
        hit = False
        if pm and pm in idx_pm[src]: hit = True; route.append(f"{src}:PMID")
        if doi and doi.lower() in idx_doi[src]: hit = True; route.append(f"{src}:DOI")
        if nt and nt in idx[src]: hit = True; route.append(f"{src}:title")
        got[src] = hit
    ok = "pass" if any(got.values()) else "FAIL"
    if ok == "FAIL" and "central" in exp: fails.append(sid)
    rows.append(dict(sentinel_id=sid, citation=cite, **{"DOI/PMID": f"{doi}/{pm}".strip("/")},
        expected_eligibility=exp,
        PubMed_retrieved=int(got["PubMed"]), CENTRAL_retrieved=int(got["CENTRAL"]),
        Scopus_retrieved=int(got["Scopus"]), ClinicalTrials_retrieved=int(got["ClinicalTrials"]),
        retrieval_route="|".join(sorted(set(r.split(":")[0] for r in route))) or "none",
        notes="|".join(route), pass_fail=ok))
fields = ["sentinel_id","citation","DOI/PMID","expected_eligibility","PubMed_retrieved",
          "CENTRAL_retrieved","Scopus_retrieved","ClinicalTrials_retrieved",
          "retrieval_route","notes","pass_fail"]
with open(f"{BASE}/SENTINEL_RETRIEVAL_TEST.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
print("sentinels:", len(rows), "pass:", sum(1 for r in rows if r["pass_fail"]=="pass"),
      "fail:", len(fails), fails[:20])
per_src = {s: sum(1 for r in rows if r[s+"_retrieved"]) for s in
           ["PubMed","CENTRAL","Scopus","ClinicalTrials"]}
print(per_src)
