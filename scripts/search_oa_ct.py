#!/usr/bin/env python3
import json,time,urllib.parse,urllib.request,hashlib,csv,os
BASE="/home/ubuntu/pm_work";RAW=f"{BASE}/raw";EXP=f"{BASE}/exports"
SEARCH_DATE="2026-11-03"
UA={"User-Agent":"pain-medicine-scoping-review/1.0 (contact: bougtoir@gmail.com)"}
def get(url,retries=5):
    for i in range(retries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=60) as r: return r.read()
        except Exception as e:
            print("retry",i,url[:90],e);time.sleep(4*(i+1))
    raise RuntimeError(url)
def save_raw(n,d):
    p=f"{RAW}/{n}";open(p,"wb").write(d)
    return {"file":p,"bytes":len(d),"sha256":hashlib.sha256(d).hexdigest()}
manifest=[]
def openalex_search(qname,search_str):
    recs=[];total=None;pages=0
    while pages<10:
        u=("https://api.openalex.org/works?per_page=200"
           f"&search={urllib.parse.quote(search_str)}&page={pages+1}"
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
        pages+=1
        if not j["results"] or pages*200>=total:break
        time.sleep(0.5)
    out=f"{EXP}/openalex_{qname}.json";json.dump(recs,open(out,"w"),indent=1)
    manifest.append({"source":"OpenAlex","platform":"OpenAlex API (open index; declared substitute for Scopus/WoS — no subscription access)",
      "date":SEARCH_DATE,"query_id":qname,"query":search_str,"filters":"none",
      "language":"all (English applied at screening)","date_restriction":"none",
      "raw_hits":total,"exported_records":len(recs),"export_file":out})
    print("OA",qname,total,len(recs));return recs
CRYO_OA='cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage"'
LA_OA='"local anesthetic" OR "local anesthesia" OR lidocaine OR bupivacaine OR ropivacaine OR mepivacaine OR EMLA OR "nerve block" OR epidural OR "regional anesthesia" OR "topical anesthetic" OR benzocaine'
all_oa=[]
for qn,q in {"OA1_core":f'({CRYO_OA}) AND ({LA_OA})',"OA2_cryo_pain":f'({CRYO_OA}) AND (analgesia OR pain OR anesthesia)'}.items():
    recs=openalex_search(qn,q)
    for r in recs:r["query_id"]=qn
    all_oa+=recs;time.sleep(0.4)
all_ct=[]
for term in ["cryoanalgesia","cryoneurolysis","cryoablation AND analgesia","cryoablation AND pain","vapocoolant","ethyl chloride spray"]:
    qname="ctgov_"+term.replace(" ","_").replace('"','')
    recs=[];token=None;pages=0
    while True:
        u=("https://clinicaltrials.gov/api/v2/studies"
           f"?query.term={urllib.parse.quote(term)}&pageSize=100&format=json"
           +(f"&pageToken={token}" if token else ""))
        data=get(u);save_raw(f"{qname}_p{pages}.json",data)
        j=json.loads(data)
        for s in j.get("studies",[]):
            p=s["protocolSection"];idm=p["identificationModule"]
            st=p.get("statusModule",{});dm=p.get("designModule",{})
            recs.append({"nct":idm.get("nctId"),"title":idm.get("briefTitle",""),
              "year":(st.get("startDateStruct",{}).get("date","")[:4]),
              "status":st.get("overallStatus",""),"design":dm.get("studyType",""),
              "enrollment":(dm.get("enrollmentInfo") or {}).get("count")})
        token=j.get("nextPageToken");pages+=1
        if not token:break
        time.sleep(0.4)
    out=f"{EXP}/{qname}.json";json.dump(recs,open(out,"w"),indent=1)
    manifest.append({"source":"ClinicalTrials.gov","platform":"API v2","date":SEARCH_DATE,
      "query_id":qname,"query":term,"filters":"none","language":"n/a","date_restriction":"none",
      "raw_hits":len(recs),"exported_records":len(recs),"export_file":out})
    print("CT",term,len(recs))
    for r in recs:r["query_id"]=qn
    all_ct+=recs;time.sleep(0.3)
json.dump({"manifest":manifest},open(f"{BASE}/oa_ct_manifest.json","w"),indent=1)
json.dump({"openalex":all_oa,"ctgov":all_ct},open(f"{BASE}/oa_ct_records.json","w"),indent=1)
print("DONE",len(all_oa),len(all_ct))
