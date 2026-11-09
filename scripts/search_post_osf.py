#!/usr/bin/env python3
"""Post-OSF-registration search rebuild (registered sources: PubMed, CENTRAL, Scopus, CT.gov).
Runs 2026-11-09. CENTRAL blocked (Cloudflare Turnstile) -> documented, not silently substituted."""
import json, time, urllib.parse, urllib.request, hashlib, csv, os, sys

BASE = "/home/ubuntu/pm_work/post_osf"
RAW = f"{BASE}/raw"; EXP = f"{BASE}/exports"
os.makedirs(RAW, exist_ok=True); os.makedirs(EXP, exist_ok=True)
SEARCH_DATE = "2026-11-09"
UA = {"User-Agent": "pain-medicine-scoping-review/2.0 (mailto:bougtoir@gmail.com)"}
SCOPUS_KEY = os.environ["SCOPUS_API_KEY"]

def get(url, retries=4, headers=None):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={**UA, **(headers or {})})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == retries - 1: raise
            time.sleep(4 * (i + 1))

def save_raw(name, data):
    p = f"{RAW}/{name}"
    with open(p, "wb") as f: f.write(data)
    return {"file": os.path.relpath(p, BASE), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

manifest = []

CRYO = ('("cryoanalgesia"[tiab] OR "cryoanesthesia"[tiab] OR "cryoanaesthesia"[tiab] '
        'OR "cryoneurolysis"[tiab] OR "cryoneurotomy"[tiab] OR "cryoablation"[tiab] '
        'OR "cryotherapy"[tiab] OR "vapocoolant"[tiab] OR "ethyl chloride"[tiab] '
        'OR "ice massage"[tiab] OR "cold spray"[tiab] OR "precooling"[tiab] '
        'OR "pre-cooling"[tiab] OR "ice pack"[tiab] OR "ice application"[tiab])')
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
    "Q8_broad_block": f'{CRYO} AND ("nerve block"[tiab] OR epidural[tiab] OR "regional anesthesia"[tiab] OR "regional anaesthesia"[tiab])',
}

def pubmed_search(qname, query):
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed"
           f"&term={urllib.parse.quote(query)}&retmax=10000&retmode=json&datetype=pdat")
    data = get(url)
    meta = save_raw(f"pubmed_{qname}_esearch.json", data)
    j = json.loads(data)
    ids = j["esearchresult"].get("idlist", [])
    recs = []
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
                         "journal": r.get("source","")})
        time.sleep(0.4)
    out = f"{EXP}/pubmed_{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"MEDLINE via PubMed","platform":"NCBI E-utilities","date":SEARCH_DATE,
                     "query_id":qname,"query":query,"filters":"none (English eligibility at screening per protocol)",
                     "date_restriction":"none","raw_hits":j["esearchresult"]["count"],
                     "exported_records":len(recs),"export_file":os.path.relpath(out,BASE),**meta})
    print(f"PubMed {qname}: hits={j['esearchresult']['count']} exported={len(recs)}",flush=True)
    return recs

# ---------------- Scopus ----------------
SCRYO = ('TITLE-ABS-KEY(cryoanalgesia OR cryoanesthesia OR cryoanaesthesia OR cryoneurolysis '
         'OR cryoneurotomy OR cryoablation OR cryotherapy OR vapocoolant OR "ethyl chloride" '
         'OR "ice massage" OR "cold spray" OR precooling OR "pre-cooling" OR "ice pack" OR "ice application")')
SLA = ('TITLE-ABS-KEY("local anesthetic" OR "local anesthesia" OR "local anaesthetic" OR "local anaesthesia" '
       'OR lidocaine OR mepivacaine OR bupivacaine OR ropivacaine OR levobupivacaine OR articaine '
       'OR prilocaine OR benzocaine OR EMLA OR "eutectic mixture" OR "nerve block" OR epidural '
       'OR "regional anesthesia" OR "regional anaesthesia" OR "topical anesthetic" OR "topical anaesthetic" '
       'OR "intercostal block")')
SPAIN = 'TITLE-ABS-KEY(analgesia OR analgesic OR pain OR anesthesia OR anaesthesia)'
SCOPUS_QUERIES = {
    "S1_core_cryo_x_LA": f"{SCRYO} AND {SLA}",
    "S2_core_cryo_x_pain": f"{SCRYO} AND {SPAIN}",
    "S3_dental": f'{SCRYO} AND TITLE-ABS-KEY(dental OR dentistry OR oral OR palatal OR "inferior alveolar" OR tooth OR endodontic)',
    "S4_vascular": f'{SCRYO} AND TITLE-ABS-KEY(venipuncture OR cannulation OR intravenous OR "vascular access" OR venepuncture OR phlebotomy)',
    "S5_thoracic": f'{SCRYO} AND TITLE-ABS-KEY(thoracotomy OR thoracic OR intercostal OR "rib fracture" OR "rib fractures" OR VATS OR pectus OR "chest wall" OR Nuss OR sternotomy)',
    "S6_orthopedic": f'{SCRYO} AND TITLE-ABS-KEY(arthroplasty OR orthopedic OR orthopaedic OR "total knee" OR "total hip" OR knee OR genicular OR spine OR musculoskeletal)',
    "S7_derm_office": f'{SCRYO} AND TITLE-ABS-KEY(dermatology OR dermatologic OR laser OR "hair removal" OR "minor surgery" OR "office-based" OR "skin biopsy" OR implant)',
    "S8_broad_block": f'{SCRYO} AND TITLE-ABS-KEY("nerve block" OR epidural OR "regional anesthesia" OR "regional anaesthesia")',
}

SCOPUS_PAGE_CAP = 4950  # apiKey (no insttoken) caps start+count at 5000

def scopus_total(query):
    url = ("https://api.elsevier.com/content/search/scopus?query=" + urllib.parse.quote(query) +
           f"&start=0&count=1&view=STANDARD&apiKey={SCOPUS_KEY}")
    for attempt in range(4):
        try:
            j = json.loads(get(url))
            return int(j["search-results"]["opensearch:totalResults"])
        except Exception:
            if attempt == 3: raise
            time.sleep(3 * (attempt + 1))

def scopus_fetch(qname, query):
    """Fetch all records for one query whose total <= SCOPUS_PAGE_CAP."""
    recs = []; start = 0; total = None
    while True:
        url = ("https://api.elsevier.com/content/search/scopus?query=" + urllib.parse.quote(query) +
               f"&start={start}&count=25&view=STANDARD&apiKey={SCOPUS_KEY}")
        data = None
        for attempt in range(4):
            try:
                data = get(url); break
            except urllib.error.HTTPError as ex:
                if attempt == 3: raise
                time.sleep(5 * (attempt + 1))
        save_raw(f"scopus_{qname}_p{start}.json", data)
        j = json.loads(data); sr = j["search-results"]
        total = int(sr["opensearch:totalResults"])
        entries = sr.get("entry", [])
        if not entries: break
        for e in entries:
            if e.get("error"): continue
            recs.append({"scopus_eid": e.get("eid",""), "title": e.get("dc:title",""),
                         "authors": e.get("dc:creator",""), "year": (e.get("prism:coverDate","") or "")[:4],
                         "doi": e.get("prism:doi",""), "journal": e.get("prism:publicationName",""),
                         "pubtype": e.get("subtypeDescription","")})
        start += len(entries)
        if start >= total or start >= SCOPUS_PAGE_CAP: break
        time.sleep(0.3)
    return total, recs

def scopus_partitions(query):
    """Return list of (suffix, partition_query) each with total <= cap."""
    total = scopus_total(query)
    if total <= SCOPUS_PAGE_CAP:
        return [("", query, total)]
    # partition by publication year; widen/narrow ranges adaptively
    parts = []
    lo, hi = 1800, 2027
    def probe(q):
        return scopus_total(q)
    # binary-split year ranges until each <= cap
    stack = [(lo, hi)]
    while stack:
        y0, y1 = stack.pop()
        if y0 > lo:
            pq = f"({query}) AND PUBYEAR > {y0 - 1} AND PUBYEAR < {y1}"
            sfx = f"_y{y0}to{y1-1}"
        else:
            pq = f"({query}) AND PUBYEAR < {y1}"
            sfx = f"_ybef{y1}"
        t = probe(pq)
        if t <= SCOPUS_PAGE_CAP:
            parts.append((sfx, pq, t)); continue
        # need further split
        if y1 - y0 <= 1:
            # single year still too big: split by halves via month is not supported; bisect days not possible -> split year anyway by accepting >cap is impossible, so split finer by quarters using PUBYEAR only can't. Fall back: split by single year and then by alphabetical title? Instead split y0==y1-1 into two via PUBYEAR = y0 and PUBYEAR = y1-1? covered. Here means single-year >cap: split via ISSN? Use publication date year+month unsupported. Raise with clear error to handle manually.
            raise RuntimeError(f"partition too large: {pq} -> {t}")
        mid = (y0 + y1) // 2
        stack.append((mid, y1)); stack.append((y0, mid))
    parts.sort(key=lambda p: p[0])
    return parts

def scopus_search(qname, query):
    parts = scopus_partitions(query)
    recs = []; grand_total = 0; part_desc = []
    for sfx, pq, t in parts:
        pt, pr = scopus_fetch(f"{qname}{sfx}", pq)
        grand_total += t; recs.extend(pr)
        part_desc.append(f"{sfx or '_all'}: query=({pq}) hits={t} exported={len(pr)}")
        time.sleep(0.4)
    out = f"{EXP}/scopus_{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"Scopus","platform":"Elsevier Scopus Search API (apiKey)","date":SEARCH_DATE,
                     "query_id":qname,"query":query,
                     "filters":"none (English eligibility at screening per protocol)",
                     "date_restriction":"none; queries exceeding the apiKey 5000-result page cap were partitioned by PUBYEAR ranges (see partition_detail)",
                     "partition_detail":" | ".join(part_desc) if len(part_desc)>1 else "",
                     "raw_hits":grand_total,
                     "exported_records":len(recs),"export_file":os.path.relpath(out,BASE)})
    print(f"Scopus {qname}: hits={grand_total} exported={len(recs)} partitions={len(parts)}",flush=True)
    return recs

# ---------------- CT.gov ----------------
CT_TERMS = {
    "T1_cryoanalgesia": "cryoanalgesia",
    "T2_cryoneurolysis": "cryoneurolysis",
    "T3_cryoablation_pain": "cryoablation AND pain",
    "T4_cryoablation_analgesia": "cryoablation AND analgesia",
    "T5_vapocoolant": "vapocoolant",
    "T6_ethyl_chloride": '"ethyl chloride" spray',
    "T7_cryoanesthesia": "cryoanesthesia OR cryoanaesthesia",
}
def ctgov_search(qname, term):
    recs=[];tok=None
    while True:
        url=(f"https://clinicaltrials.gov/api/v2/studies?query.term={urllib.parse.quote(term)}"
             f"&pageSize=100&format=json" + (f"&pageToken={tok}" if tok else ""))
        data=get(url); save_raw(f"ctgov_{qname}{'_'+str(len(recs)) if tok else ''}.json",data)
        j=json.loads(data)
        for st in j.get("studies",[]):
            p=st.get("protocolSection",{})
            idm=p.get("identificationModule",{});dm=p.get("designModule",{})
            stat=p.get("statusModule",{})
            recs.append({"nct":idm.get("nctId",""),"title":idm.get("briefTitle",""),
                "authors":"","year":(stat.get("startDateStruct",{}).get("date","") or "")[:4],
                "doi":"","journal":"ClinicalTrials.gov","status":stat.get("overallStatus",""),
                "enrollment":(dm.get("enrollmentInfo") or {}).get("count","")})
        tok=j.get("nextPageToken")
        if not tok:break
        time.sleep(0.3)
    out=f"{EXP}/ctgov_{qname}.json"
    with open(out,"w") as f:json.dump(recs,f,indent=1)
    manifest.append({"source":"ClinicalTrials.gov","platform":"CT.gov API v2","date":SEARCH_DATE,
        "query_id":qname,"query":term,"filters":"none","date_restriction":"none",
        "raw_hits":len(recs),"exported_records":len(recs),"export_file":os.path.relpath(out,BASE)})
    print(f"CT.gov {qname}: {len(recs)}",flush=True)
    return recs

which = sys.argv[1] if len(sys.argv)>1 else "all"
if which in ("all","pubmed"):
    for qn,q in PUBMED_QUERIES.items():
        pubmed_search(qn,q); time.sleep(0.4)
if which in ("all","scopus"):
    for qn,q in SCOPUS_QUERIES.items():
        scopus_search(qn,q); time.sleep(0.5)
if which in ("all","ctgov"):
    for qn,q in CT_TERMS.items():
        ctgov_search(qn,q); time.sleep(0.4)
with open(f"{BASE}/SEARCH_EXPORT_MANIFEST_partial.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["source","platform","date","query_id","query","filters","date_restriction","partition_detail","raw_hits","exported_records","export_file","file","bytes","sha256"],extrasaction="ignore")
    w.writeheader();w.writerows(manifest)
print("manifest rows:",len(manifest))
