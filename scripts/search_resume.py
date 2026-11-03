#!/usr/bin/env python3
"""Resume: OpenAlex + ClinicalTrials.gov only; merges PubMed exports already on disk."""
import json, time, urllib.parse, urllib.request, hashlib, csv, os
BASE="/home/ubuntu/pm_work"; RAW=f"{BASE}/raw"; EXP=f"{BASE}/exports"
SEARCH_DATE="2026-11-03"
UA={"User-Agent":"pain-medicine-scoping-review/1.0 (mailto:bougtoir@gmail.com)"}
def get(url,retries=3):
    for i in range(retries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=60) as r: return r.read()
        except Exception:
            if i==retries-1: raise
            time.sleep(3*(i+1))
def save_raw(name,data):
    p=f"{RAW}/{name}"
    with open(p,"wb") as f: f.write(data)
    return {"file":p,"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
manifest=[]
# rebuild pubmed manifest rows from existing exports
PUBMED_QUERIES=["Q1_core_cryo_x_LA","Q2_core_cryo_x_pain","Q3_dental","Q4_vascular","Q5_thoracic","Q6_orthopedic","Q7_derm_office","Q8_ctgov_style_broad"]
QSTR={
"Q1_core_cryo_x_LA":"CRYO block AND LA block (see SEARCH_STRATEGIES_FULL.md)",
"Q2_core_cryo_x_pain":"CRYO block AND (analgesia OR analgesic OR pain OR anesthesia OR anaesthesia)[tiab]",
"Q3_dental":"CRYO block AND (dental OR dentistry OR oral OR palatal OR inferior alveolar OR tooth OR endodontic)[tiab]",
"Q4_vascular":"CRYO block AND (venipuncture OR cannulation OR intravenous OR vascular access OR venepuncture OR phlebotomy)[tiab]",
"Q5_thoracic":"CRYO block AND (thoracotomy OR thoracic OR intercostal OR rib fracture(s) OR VATS OR pectus OR chest wall OR Nuss OR sternotomy)[tiab]",
"Q6_orthopedic":"CRYO block AND (arthroplasty OR orthopedic OR orthopaedic OR total knee OR total hip OR knee OR genicular OR spine OR musculoskeletal)[tiab]",
"Q7_derm_office":"CRYO block AND (dermatology OR dermatologic OR laser OR hair removal OR minor surgery OR office-based OR skin biopsy OR implant)[tiab]",
"Q8_ctgov_style_broad":"CRYO block AND (nerve block OR epidural OR regional anesthesia OR regional anaesthesia)[tiab]"}
for qn in PUBMED_QUERIES:
    p=f"{EXP}/pubmed_{qn}.json"
    if not os.path.exists(p): print("MISSING",p); continue
    recs=json.load(open(p))
    manifest.append({"source":"MEDLINE/PubMed","platform":"NCBI E-utilities","date":SEARCH_DATE,
      "query_id":qn,"query":QSTR[qn],"filters":"none","language":"all (English applied at screening)",
      "date_restriction":"none","raw_hits":len(recs),"exported_records":len(recs),"export_file":p})
    print("pubmed manifest",qn,len(recs))
def openalex_search(qname,search_str):
    recs=[];cursor="*";total=None;pages=0
    while cursor and pages<10:
        u=("https://api.openalex.org/works?per_page=200"
           f"&search={urllib.parse.quote(search_str)}&cursor={urllib.parse.quote(cursor)}"
           "&mailto=bougtoir@gmail.com")
        data=get(u);save_raw(f"openalex_{qname}_p{pages}.json",data)
        j=json.loads(data);total=j["meta"]["count"]
        for w in j["results"]:
            doi=(w.get("doi") or "").replace("https://doi.org/","")
            authors="; ".join(a["author"]["display_name"] for a in w.get("authorships",[]))
            recs.append({"openalex_id":w["id"],"title":w.get("title") or "",
              "authors":authors,"year":str(w.get("publication_year") or ""),
              "doi":doi,"pmid":(w.get("ids",{}).get("pmid") or "").rsplit("/",1)[-1],
              "source":(((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")})
        cursor=j["meta"].get("next_cursor");pages+=1
        if not j["results"]: break
        time.sleep(0.5)
    out=f"{EXP}/openalex_{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"OpenAlex","platform":"OpenAlex API (open index; declared substitute for Scopus/WoS — no subscription access)",
      "date":SEARCH_DATE,"query_id":qname,"query":search_str,"filters":"none",
      "language":"all (English applied at screening)","date_restriction":"none",
      "raw_hits":total,"exported_records":len(recs),"export_file":out})
    print(f"OpenAlex {qname}: {total} -> {len(recs)}")
    return recs
CRYO_OA='cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage"'
LA_OA='"local anesthetic" OR "local anesthesia" OR lidocaine OR bupivacaine OR ropivacaine OR mepivacaine OR EMLA OR "nerve block" OR epidural OR "regional anesthesia" OR "topical anesthetic" OR benzocaine'
OA={"OA1_core":f'({CRYO_OA}) AND ({LA_OA})',"OA2_cryo_pain":f'({CRYO_OA}) AND (analgesia OR pain OR anesthesia)'}
all_oa=[]
for qn,q in OA.items():
    recs=openalex_search(qn,q)
    for r in recs: r["query_id"]=qn
    all_oa+=recs; time.sleep(0.4)
all_ct=[]
for term in ["cryoanalgesia","cryoneurolysis","cryoablation AND analgesia","cryoablation AND pain","vapocoolant","ethyl chloride spray"]:
    qname="ctgov_"+term.replace(" ","_").replace('"','')
    url=("https://clinicaltrials.gov/api/v2/studies"
         f"?query.term={urllib.parse.quote(term)}&pageSize=100&format=json")
    recs=[];token=None;pages=0
    while True:
        u=url+(f"&pageToken={token}" if token else "")
        data=get(u);save_raw(f"{qname}_p{pages}.json",data)
        j=json.loads(data)
        for s in j.get("studies",[]):
            p=s["protocolSection"];idm=p["identificationModule"]
            st=p.get("statusModule",{});dm=p.get("designModule",{})
            recs.append({"nct":idm.get("nctId"),"title":idm.get("briefTitle",""),
              "year":(st.get("startDateStruct",{}).get("date","")[:4]),
              "status":st.get("overallStatus",""),
              "design":dm.get("studyType",""),
              "enrollment":(dm.get("enrollmentInfo") or {}).get("count")})
        token=j.get("nextPageToken");pages+=1
        if not token: break
        time.sleep(0.4)
    out=f"{EXP}/{qname}.json"
    with open(out,"w") as f: json.dump(recs,f,indent=1)
    manifest.append({"source":"ClinicalTrials.gov","platform":"API v2","date":SEARCH_DATE,
      "query_id":qname,"query":term,"filters":"none","language":"n/a","date_restriction":"none",
      "raw_hits":len(recs),"exported_records":len(recs),"export_file":out})
    print(f"CT.gov {term}: {len(recs)}")
    for r in recs: r["query_id"]=qname
    all_ct+=recs; time.sleep(0.3)
with open(f"{BASE}/SEARCH_EXPORT_MANIFEST.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["source","platform","date","query_id","query","filters","language","date_restriction","raw_hits","exported_records","export_file"],extrasaction="ignore")
    w.writeheader();w.writerows(manifest)
all_pm=[]
for qn in PUBMED_QUERIES:
    p=f"{EXP}/pubmed_{qn}.json"
    if os.path.exists(p):
        for r in json.load(open(p)): r["query_id"]=qn
        all_pm+=json.load(open(p))
with open(f"{BASE}/all_records.json","w") as f:
    json.dump({"pubmed":all_pm,"openalex":all_oa,"ctgov":all_ct},f,indent=1)
print("DONE",len(all_pm),len(all_oa),len(all_ct))
