#!/usr/bin/env python3
"""Gate 2 search rebuild: PubMed (E-utilities), OpenAlex, ClinicalTrials.gov v2.
Saves raw exports + machine-readable manifest + yields CSV. Search date fixed."""
import json, time, urllib.parse, urllib.request, hashlib, csv, os, sys

BASE = "/home/ubuntu/pm_work"
RAW = f"{BASE}/raw"; EXP = f"{BASE}/exports"
os.makedirs(RAW, exist_ok=True); os.makedirs(EXP, exist_ok=True)
SEARCH_DATE = "2026-11-03"
UA = {"User-Agent": "pain-medicine-scoping-review/1.0 (mailto:bougtoir@gmail.com)"}

def get(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == retries - 1: raise
            time.sleep(3 * (i + 1))

def save_raw(name, data):
    p = f"{RAW}/{name}"
    with open(p, "wb") as f: f.write(data)
    return {"file": p, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

# ---------------- PubMed ----------------
CRYO = ('("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoneurolysis"[tiab] '
        'OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] OR "cryotherapy"[tiab] '
        'OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] OR "ice massage"[tiab] '
        'OR "cold spray"[tiab] OR "precooling"[tiab] OR "pre-cooling"[tiab] '
        'OR "ice pack"[tiab] OR "ice application"[tiab])')
LA = ('("local anesthetic"[tiab] OR "local anesthesia"[tiab] OR "local anaesthetic"[tiab] '
      'OR "local anaesthesia"[tiab] OR lidocaine[tiab] OR mepivacaine[tiab] '
      'OR bupivacaine[tiab] OR ropivacaine[tiab] OR levobupivacaine[tiab] '
      'OR articaine[tiab] OR prilocaine[tiab] OR benzocaine[tiab] OR EMLA[tiab] '
      'OR "eutectic mixture"[tiab] OR "nerve block"[tiab] OR "nerve blocks"[tiab] '
      'OR epidural[tiab] OR "regional anesthesia"[tiab] OR "regional anaesthesia"[tiab] '
      'OR "topical anesthetic"[tiab] OR "topical anaesthetic"[tiab] OR "intercostal block"[tiab])')
PAIN = '(analgesia[tiab] OR analgesic[tiab] OR pain[tiab] OR anesthesia[tiab] OR anaesthesia[tiab])'

PUBMED_QUERIES = {
    "Q1_core_cryo_x_LA": f"{CRYO} AND {LA}",
    "Q2_core_cryo_x_pain": f"{CRYO} AND {PAIN}",
    "Q3_dental": f'{CRYO} AND (dental[tiab] OR dentistry[tiab] OR "oral"[tiab] OR palatal[tiab] OR "inferior alveolar"[tiab] OR tooth[tiab] OR endodontic[tiab])',
    "Q4_vascular": f'{CRYO} AND (venipuncture[tiab] OR cannulation[tiab] OR "intravenous"[tiab] OR "vascular access"[tiab] OR venepuncture[tiab] OR phlebotomy[tiab])',
    "Q5_thoracic": f'{CRYO} AND (thoracotomy[tiab] OR thoracic[tiab] OR intercostal[tiab] OR "rib fracture"[tiab] OR "rib fractures"[tiab] OR VATS[tiab] OR pectus[tiab] OR "chest wall"[tiab] OR Nuss[tiab] OR sternotomy[tiab])',
    "Q6_orthopedic": f'{CRYO} AND (arthroplasty[tiab] OR orthopedic[tiab] OR orthopaedic[tiab] OR "total knee"[tiab] OR "total hip"[tiab] OR knee[tiab] OR genicular[tiab] OR spine[tiab] OR musculoskeletal[tiab])',
    "Q7_derm_office": f'{CRYO} AND (dermatology[tiab] OR dermatologic[tiab] OR laser[tiab] OR "hair removal"[tiab] OR "minor surgery"[tiab] OR "office-based"[tiab] OR "skin biopsy"[tiab] OR implant[tiab])',
    "Q8_ctgov_style_broad": f'{CRYO} AND ("nerve block"[tiab] OR epidural[tiab] OR "regional anesth*"[tiab])',
}
PUBMED_QUERIES["Q8_ctgov_style_broad"] = f'{CRYO} AND ("nerve block"[tiab] OR epidural[tiab] OR "regional anesthesia"[tiab] OR "regional anaesthesia"[tiab])'

manifest, yields = [], []

def pubmed_search(qname, query):
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed"
           f"&term={urllib.parse.quote(query)}&retmax=10000&retmode=json&datetype=pdat")
    data = get(url)
    meta = save_raw(f"pubmed_{qname}_esearch.json", data)
    j = json.loads(data)
    ids = j["esearchresult"].get("idlist", [])
    recs = []
    if ids:
        # fetch summaries in batches of 200
        for i in range(0, len(ids), 200):
            batch = ",".join(ids[i:i+200])
            s = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed"
                    f"&id={batch}&retmode=json")
            save_raw(f"pubmed_{qname}_esummary_{i}.json", s)
            sj = json.loads(s)
            for pid in sj["result"]["uids"]:
                r = sj["result"][pid]
                recs.append({"pmid": pid, "title": r.get("title",""),
                             "authors": "; ".join(a["name"] for a in r.get("authors",[])),
                             "year": (r.get("pubdate","")[:4]),
                             "doi": next((i2["value"] for i2 in r.get("articleids",[]) if i2["idtype"]=="doi"), ""),
                             "source": r.get("source","")})
            time.sleep(0.5)
    out = f"{EXP}/pubmed_{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"MEDLINE/PubMed","platform":"NCBI E-utilities","date":SEARCH_DATE,
                     "query_id":qname,"query":query,"filters":"none","language":"all (English policy applied at screening)",
                     "date_restriction":"none","raw_hits":j["esearchresult"]["count"],
                     "exported_records":len(recs),"export_file":out,**meta})
    print(f"PubMed {qname}: count={j['esearchresult']['count']} exported={len(recs)}")
    return recs

all_pm = []
for qn,q in PUBMED_QUERIES.items():
    recs = pubmed_search(qn,q)
    for r in recs: r["query_id"]=qn
    all_pm += recs
    time.sleep(0.4)

# ---------------- OpenAlex ----------------
def openalex_search(qname, search_str):
    url = ("https://api.openalex.org/works?filter=type:article|review&per_page=200"
           f"&search={urllib.parse.quote(search_str)}&mailto=bougtoir@gmail.com")
    # cursor pagination up to 5 pages
    url = ("https://api.openalex.org/works?per_page=200&cursor=*"
           f"&search={urllib.parse.quote(search_str)}&mailto=bougtoir@gmail.com")
    recs=[]; cursor="*"; total=None; pages=0
    while cursor and pages<10:
        u = ("https://api.openalex.org/works?per_page=200"
             f"&search={urllib.parse.quote(search_str)}&cursor={urllib.parse.quote(cursor)}"
             "&mailto=bougtoir@gmail.com")
        data=get(u); save_raw(f"openalex_{qname}_p{pages}.json",data)
        j=json.loads(data); total=j["meta"]["count"]
        for w in j["results"]:
            doi=(w.get("doi") or "").replace("https://doi.org/","")
            authors="; ".join(a["author"]["display_name"] for a in w.get("authorships",[]))
            recs.append({"openalex_id":w["id"],"title":w.get("title") or "",
                         "authors":authors,"year":str(w.get("publication_year") or ""),
                         "doi":doi,"pmid":(w.get("ids",{}).get("pmid") or "").rsplit("/",1)[-1],
                         "source":(((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")})
        cursor=j["meta"].get("next_cursor"); pages+=1
        if not j["results"]: break
        time.sleep(0.5)
    out=f"{EXP}/openalex_{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"OpenAlex","platform":"OpenAlex API (open index; declared substitute for Scopus/WoS — no subscription access)",
                     "date":SEARCH_DATE,"query_id":qname,"query":search_str,
                     "filters":"none","language":"all (English policy applied at screening)",
                     "date_restriction":"none","raw_hits":total,"exported_records":len(recs),
                     "export_file":out})
    print(f"OpenAlex {qname}: count={total} exported={len(recs)}")
    return recs

CRYO_OA = 'cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage"'
LA_OA = '"local anesthetic" OR "local anesthesia" OR lidocaine OR bupivacaine OR ropivacaine OR mepivacaine OR EMLA OR "nerve block" OR epidural OR "regional anesthesia" OR "topical anesthetic" OR benzocaine'
OPENALEX_QUERIES = {
    "OA1_core": f'({CRYO_OA}) AND ({LA_OA})',
    "OA2_cryo_pain": f'({CRYO_OA}) AND (analgesia OR pain OR anesthesia)',
}
all_oa=[]
for qn,q in OPENALEX_QUERIES.items():
    recs=openalex_search(qn,q)
    for r in recs: r["query_id"]=qn
    all_oa+=recs
    time.sleep(0.4)

# ---------------- ClinicalTrials.gov ----------------
CT_TERMS = ["cryoanalgesia","cryoneurolysis","cryoablation AND analgesia","cryoablation AND pain","vapocoolant","ethyl chloride spray"]
all_ct=[]
for term in CT_TERMS:
    qname="ctgov_"+term.replace(" ","_").replace('"','')
    url=("https://clinicaltrials.gov/api/v2/studies"
         f"?query.term={urllib.parse.quote(term)}&pageSize=100&format=json")
    recs=[]; token=None; total=None; pages=0
    while True:
        u=url+(f"&pageToken={token}" if token else "")
        data=get(u); save_raw(f"{qname}_p{pages}.json",data)
        j=json.loads(data)
        for s in j.get("studies",[]):
            p=s["protocolSection"]; idm=p["identificationModule"]
            st=p.get("statusModule",{}); dm=p.get("designModule",{})
            recs.append({"nct":idm.get("nctId"),"title":idm.get("briefTitle",""),
                         "year":(st.get("startDateStruct",{}).get("date","")[:4]),
                         "status":st.get("overallStatus",""),
                         "design":", ".join(dm.get("studyType","").split()+dm.get("phases",[])),
                         "enrollment":dm.get("enrollmentInfo",{}).get("count")})
        token=j.get("nextPageToken"); pages+=1
        if not token: break
        time.sleep(0.4)
    out=f"{EXP}/{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"ClinicalTrials.gov","platform":"API v2","date":SEARCH_DATE,
                     "query_id":qname,"query":term,"filters":"none","language":"n/a",
                     "date_restriction":"none","raw_hits":len(recs),"exported_records":len(recs),
                     "export_file":out})
    print(f"CT.gov {term}: {len(recs)}")
    for r in recs: r["query_id"]=qname
    all_ct+=recs
    time.sleep(0.3)

with open(f"{BASE}/SEARCH_EXPORT_MANIFEST.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["source","platform","date","query_id","query","filters","language","date_restriction","raw_hits","exported_records","export_file","file","bytes","sha256"],extrasaction="ignore")
    w.writeheader(); w.writerows(manifest)
with open(f"{BASE}/all_records.json","w") as f:
    json.dump({"pubmed":all_pm,"openalex":all_oa,"ctgov":all_ct},f,indent=1)
print("DONE", len(all_pm), len(all_oa), len(all_ct))
