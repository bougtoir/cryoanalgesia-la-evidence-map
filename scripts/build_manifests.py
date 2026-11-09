#!/usr/bin/env python3
"""Assemble GATE 2 outputs: SEARCH_YIELDS.csv, SEARCH_EXPORT_MANIFEST.csv,
SEARCH_STRATEGIES_FULL.md from the four frozen sources' logs/exports/raw."""
import csv, json, os, re, hashlib, ast, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
SEARCH_DATE = "2026-11-09"
# Constants extracted WITHOUT executing the search modules (their top-level code runs queries).
def _literal_assign(path, names):
    tree = ast.parse(open(path).read())
    out = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") in names:
            try:
                out[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:
                pass
        if isinstance(n, ast.AnnAssign) and getattr(n.target, "id", "") in names:
            try:
                out[n.target.id] = ast.literal_eval(n.value)
            except Exception:
                pass
    return out
_src = open(f"{_HERE}/search_post_osf.py").read()
# f-strings need evaluation with the CRYO/LA/PAIN/SCRYO/SLA/SPAIN constants
_consts = _literal_assign(f"{_HERE}/search_post_osf.py",
    {"CRYO","LA","PAIN","SCRYO","SLA","SPAIN"})
_env = dict(_consts)
class _Ev(ast.NodeVisitor):
    def __init__(self): self.out={}
    def visit_Assign(self, n):
        t=getattr(n.targets[0],"id","")
        if t in {"PUBMED_QUERIES","SCOPUS_QUERIES","CT_TERMS"}:
            try: self.out[t]=eval(compile(ast.Expression(n.value),"<a>","eval"),{"__builtins__":{}},_env)
            except Exception as e: print("eval fail",t,e)
_ev=_Ev(); _ev.visit(ast.parse(_src))
PUBMED_QUERIES=_ev.out["PUBMED_QUERIES"]; SCOPUS_QUERIES=_ev.out["SCOPUS_QUERIES"]; CT_TERMS=_ev.out["CT_TERMS"]
CENTRAL_QUERIES=_literal_assign(f"{_HERE}/central_harvest.py",{"QUERIES"})["QUERIES"]

BASE = "/home/ubuntu/pm_work/post_osf"
RAW, EXP = f"{BASE}/raw", f"{BASE}/exports"
log = open(f"{BASE}/search.log").read()
clog = open(f"{BASE}/central.log").read()

def ledger_for(prefix):
    """sha256/size ledger over raw files starting with prefix"""
    out = []
    for fn in sorted(os.listdir(RAW)):
        if fn.startswith(prefix):
            b = open(f"{RAW}/{fn}", 'rb').read()
            out.append(f"{fn}:{len(b)}:{hashlib.sha256(b).hexdigest()[:16]}")
    return out

rows = []
# PubMed
for qid, q in PUBMED_QUERIES.items():
    m = re.search(rf"PubMed {qid}: hits=(\d+) exported=(\d+)", log)
    rows.append(dict(source="MEDLINE via PubMed", platform="NCBI E-utilities", date=SEARCH_DATE,
        query_id=qid, query=q, filters="none (English eligibility at screening per protocol)",
        date_restriction="none", partition_detail="", raw_hits=int(m.group(1)),
        exported_records=int(m.group(2)), export_file=f"exports/pubmed_{qid}.json",
        raw_files=";".join(ledger_for(f"pubmed_{qid}"))))
# Scopus (hits/partitions from log; partition queries from raw filenames)
for qid, q in SCOPUS_QUERIES.items():
    m = re.search(rf"Scopus {qid}: hits=(\d+) exported=(\d+) partitions=(\d+)", log)
    parts = sorted(set(re.match(rf"scopus_{re.escape(qid)}(_[^_][^_]*)?_", fn).group(1) or ""
                       for fn in os.listdir(RAW) if fn.startswith(f"scopus_{qid}")))
    pd = "partitions by PUBYEAR: " + ",".join(p.strip("_") for p in parts if p) if len(parts) > 1 else ""
    rows.append(dict(source="Scopus", platform="Elsevier Scopus Search API (apiKey)", date=SEARCH_DATE,
        query_id=qid, query=q, filters="none (English eligibility at screening per protocol)",
        date_restriction="none; queries over the 5000-result apiKey page cap were partitioned by PUBYEAR (see partition_detail)",
        partition_detail=pd, raw_hits=int(m.group(1)), exported_records=int(m.group(2)),
        export_file=f"exports/scopus_{qid}.json", raw_files=";".join(ledger_for(f"scopus_{qid}"))))
# CENTRAL
for qid, q in CENTRAL_QUERIES.items():
    m = re.search(rf"CENTRAL {qid}: hits=(\d+) exported=(\d+)", clog)
    rows.append(dict(source="CENTRAL", platform="Cochrane Library web, human-cleared session, DOM capture (citation export login-gated)",
        date=SEARCH_DATE, query_id=qid, query=q,
        filters="field=Title Abstract Keyword (searchBy=1); word variations searched (site default)",
        date_restriction="none", partition_detail="", raw_hits=int(m.group(1)),
        exported_records=int(m.group(2)), export_file=f"exports/central_{qid}.json",
        raw_files=";".join(ledger_for(f"central_{qid}"))))
# CT.gov
ctm = list(csv.DictReader(open(f"{BASE}/SEARCH_EXPORT_MANIFEST_partial.csv")))
for r in ctm:
    rows.append(dict(source="ClinicalTrials.gov", platform="CT.gov API v2", date=SEARCH_DATE,
        query_id=r["query_id"], query=r["query"], filters="none", date_restriction="none",
        partition_detail="", raw_hits=int(r["raw_hits"]), exported_records=int(r["exported_records"]),
        export_file=r["export_file"], raw_files=";".join(ledger_for(f"ctgov_{r['query_id']}"))))

fields = ["source","platform","date","query_id","query","filters","date_restriction",
          "partition_detail","raw_hits","exported_records","export_file","raw_files"]
with open(f"{BASE}/SEARCH_EXPORT_MANIFEST.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
with open(f"{BASE}/SEARCH_YIELDS.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["source","query_id","raw_hits","exported_records"])
    for r in rows: w.writerow([r["source"], r["query_id"], r["raw_hits"], r["exported_records"]])
for r in rows:
    print(r["source"], r["query_id"], r["raw_hits"], r["exported_records"])
print("TOTAL raw:", sum(r["raw_hits"] for r in rows), "exported:", sum(r["exported_records"] for r in rows))
