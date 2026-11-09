#!/usr/bin/env python3
"""GATE 4 (part 1): merge 4-source exports -> MASTER_RECORDS.csv + DUPLICATE_MAP.csv.
Schema per post-OSF spec: per-source flags, duplicate_group_id, retained_record,
title_abstract_status, full_text_status, final_eligibility, exclusion_reason, notes.
Dedup keys: DOI > PMID > NCT > exact normalized title; then fuzzy title+first-author+year.
"""
import json, csv, re, os, hashlib
from collections import defaultdict

BASE = "/home/ubuntu/pm_work/post_osf"; EXP = f"{BASE}/exports"

def norm(t):
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def first_author(a):
    a = (a or "").strip()
    return a.split(";")[0].split(",")[0].strip().lower()[:30] if a else ""

recs = []
# PubMed
for fn in sorted(os.listdir(EXP)):
    if fn.startswith("pubmed_"):
        for r in json.load(open(f"{EXP}/{fn}")):
            r = dict(r); r["_src"] = "PubMed"; r["_qid"] = fn[7:-5]; recs.append(r)
    elif fn.startswith("scopus_"):
        for r in json.load(open(f"{EXP}/{fn}")):
            r = dict(r); r["_src"] = "Scopus"; r["_qid"] = fn[7:-5]; recs.append(r)
    elif fn.startswith("central_"):
        for r in json.load(open(f"{EXP}/{fn}")):
            r = dict(r); r["_src"] = "CENTRAL"; r["_qid"] = fn[8:-5]
            y = re.search(r",\s*(\d{4})[ ,|]", r.get("metadata","")) or re.search(r"(\d{4})", r.get("metadata",""))
            r["year"] = y.group(1) if y else ""
            recs.append(r)
    elif fn.startswith("ctgov_"):
        for r in json.load(open(f"{EXP}/{fn}")):
            r = dict(r); r["_src"] = "ClinicalTrials"; r["_qid"] = fn[6:-5]; recs.append(r)
print("raw records:", len(recs))

# ---- group by exact keys ----
groups = {}
for r in recs:
    keys = []
    if r.get("doi"): keys.append("doi:" + r["doi"].lower().strip())
    if r.get("pmid"): keys.append("pmid:" + str(r["pmid"]))
    if r.get("nct"): keys.append("nct:" + r["nct"])
    if r.get("cn_doi"): keys.append("doi:" + r["cn_doi"].lower().strip())
    keys.append("t:" + norm(r.get("title", ""))[:120])
    placed = None
    for k in keys:
        if k in groups:
            placed = groups[k]; break
    if placed is None:
        placed = {"members": [], "keys": set()}
        groups[keys[0]] = placed
    placed["members"].append(r)
    placed["keys"].update(keys)
    for k in keys:
        groups[k] = placed  # union all keys
uniq = {id(g): g for g in groups.values()}
group_list = list(uniq.values())
print("groups after exact keys:", len(group_list))

# ---- fuzzy merge: normalized title prefix + first author + year ----
seen_gid = set()
merged = []
used = set()
by_sig = defaultdict(list)
for i, g in enumerate(group_list):
    rep = g["members"][0]
    nt = norm(rep.get("title",""))[:90]
    fa = first_author(rep.get("authors",""))
    yr = str(rep.get("year",""))[:4]
    by_sig[(nt, fa, yr)].append(i)
for sig, idxs in by_sig.items():
    rep_g = group_list[idxs[0]]
    if len(idxs) > 1:
        for j in idxs[1:]:
            rep_g["members"] += group_list[j]["members"]
            rep_g["keys"] |= group_list[j]["keys"]
            used.add(j)
    merged.append(rep_g)
print("groups after fuzzy merge:", len(merged))

# ---- assign ids, representative record, duplicate map ----
SRC_PREF = ["PubMed", "CENTRAL", "Scopus", "ClinicalTrials"]
master = []; dupmap = []
for i, g in enumerate(merged):
    srcs = sorted({m["_src"] for m in g["members"]}, key=SRC_PREF.index)
    rep = next((m for s in SRC_PREF for m in g["members"] if m["_src"] == s), g["members"][0])
    gid = f"DG{i:05d}"
    rid = "R" + hashlib.md5(gid.encode()).hexdigest()[:10]
    queries = sorted({m["_qid"] for m in g["members"]})
    dup_members = [m for m in g["members"]]
    master.append(dict(
        record_id=rid, duplicate_group_id=gid, retained_record=1,
        title=rep.get("title",""), authors=rep.get("authors",""), year=rep.get("year",""),
        doi=rep.get("doi","") or rep.get("cn_doi",""), pmid=rep.get("pmid",""),
        nct=rep.get("nct",""), scopus_eid=rep.get("scopus_eid",""),
        journal=rep.get("journal","") or rep.get("metadata","")[:80],
        pubtype=rep.get("pubtype","") or rep.get("status",""),
        source_PubMed=int("PubMed" in srcs), source_CENTRAL=int("CENTRAL" in srcs),
        source_Scopus=int("Scopus" in srcs), source_ClinicalTrials=int("ClinicalTrials" in srcs),
        source_databases="|".join(srcs), queries="|".join(queries),
        n_duplicate_records=len(dup_members),
        title_abstract_status="pending", full_text_status="", final_eligibility="",
        exclusion_reason="", notes=""))
    for j, m in enumerate(dup_members):
        dupmap.append(dict(duplicate_group_id=gid, record_id=rid,
            member_index=j, retained_record=int(m is rep),
            source=m["_src"], query_id=m["_qid"],
            title=m.get("title",""), authors=m.get("authors",""),
            year=m.get("year",""), doi=m.get("doi","") or m.get("cn_doi",""),
            pmid=m.get("pmid",""), nct=m.get("nct",""), scopus_eid=m.get("scopus_eid","")))

master.sort(key=lambda r: (r["year"], r["title"]))
fields = list(master[0].keys())
with open(f"{BASE}/MASTER_RECORDS.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(master)
with open(f"{BASE}/DUPLICATE_MAP.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(dupmap[0].keys())); w.writeheader(); w.writerows(dupmap)
multi = sum(1 for m in master if m["n_duplicate_records"] > 1)
print("master:", len(master), "| multi-source groups:", multi,
      "| duplicate rows:", sum(m["n_duplicate_records"] - 1 for m in master))
