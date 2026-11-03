#!/usr/bin/env python3
"""Dedup all_records.json -> MASTER_RECORDS.csv (Gate 4 step 1)."""
import json,csv,re,hashlib
recs=[]
ar=json.load(open("/home/ubuntu/pm_work/all_records.json"))
for src in ("pubmed","openalex","crossref","ctgov"):
    for r in ar[src]:
        r["_src"]=src
        recs.append(r)
def norm(t):
    t=(t or "").lower()
    t=re.sub(r"[^a-z0-9 ]"," ",t)
    return re.sub(r"\s+"," ",t).strip()
groups={};order=[]
for r in recs:
    key=None
    if r.get("doi"): key="doi:"+r["doi"].lower().strip()
    elif r.get("pmid"): key="pmid:"+str(r["pmid"])
    elif r.get("nct"): key="nct:"+r["nct"]
    else: key="t:"+norm(r.get("title",""))[:120]
    if key in groups:
        groups[key]["sources"].add(r["_src"]);groups[key]["queries"].add(r.get("query_id",""))
    else:
        g={"key":key,"rep":r,"sources":{r["_src"]},"queries":{r.get("query_id","")}}
        groups[key]=g;order.append(key)
# second pass: fuzzy title merge across different keys (same normalized title)
title_map={}
for k in order:
    nt=norm(groups[k]["rep"].get("title",""))[:100]
    if not nt:continue
    if nt in title_map:
        title_map[nt]["members"].append(k)
        for m in groups[k]["sources"]:title_map[nt]["members_src"].add(m)
    else:
        title_map[nt]={"members":[k],"members_src":set(groups[k]["sources"])}
seen=set();rows=[];dupn=0
def first(a,b): return a or b or ""
for nt,g in title_map.items():
    members=[k for k in g["members"] if k not in seen]
    if not members:continue
    seen.update(members)
    rep=None
    for pref in ("pubmed","openalex","crossref","ctgov"):
        for k in members:
            if groups[k]["rep"]["_src"]==pref: rep=groups[k]["rep"];break
        if rep:break
    if rep is None: rep=groups[members[0]]["rep"]
    srcs=set();queries=set()
    for k in members:
        srcs|=groups[k]["sources"];queries|=groups[k]["queries"]
    if len(members)>1:dupn+=len(members)-1
    rid="R"+hashlib.md5("|".join(sorted(members)).encode()).hexdigest()[:10]
    rows.append({"record_id":rid,"title":rep.get("title",""),
      "authors":rep.get("authors",""),"year":rep.get("year",""),
      "doi":rep.get("doi",""),"pmid":rep.get("pmid",""),"nct":rep.get("nct",""),
      "journal":rep.get("source",""),
      "source_database":"|".join(sorted(srcs)),"queries":"|".join(sorted(q for q in queries if q)),
      "duplicate_group":"|".join(sorted(members)),
      "screening_status":"pending","exclusion_reason":"","fulltext_status":""})
rows.sort(key=lambda r:(r["year"],r["title"]))
with open("/home/ubuntu/pm_work/MASTER_RECORDS.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
print("raw",len(recs),"unique",len(rows),"dupes_removed",len(recs)-len(rows))
