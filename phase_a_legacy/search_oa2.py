#!/usr/bin/env python3
import json,time,urllib.parse,urllib.request,hashlib,csv,os
BASE="/home/ubuntu/pm_work";RAW=f"{BASE}/raw";EXP=f"{BASE}/exports"
SEARCH_DATE="2026-11-03"
UA={"User-Agent":"pain-medicine-scoping-review/1.0 (contact: bougtoir@gmail.com)"}
def get(url,retries=6):
    for i in range(retries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=60) as r: return r.read()
        except Exception as e:
            print(" retry",i,e);time.sleep(5*(i+1))
    raise RuntimeError(url)
def save_raw(n,d):
    p=f"{RAW}/{n}";open(p,"wb").write(d)
    return p
C='cryoanalgesia OR cryoanesthesia OR cryoneurolysis OR cryoablation OR vapocoolant OR "ethyl chloride" OR "ice massage" OR cryotherapy'
LA='"local anesthetic" OR "local anesthesia" OR "local anaesthesia" OR lidocaine OR bupivacaine OR ropivacaine OR mepivacaine OR EMLA OR "nerve block" OR epidural OR "regional anesthesia" OR "regional anaesthesia" OR "topical anesthetic" OR "topical anaesthetic" OR benzocaine'
QUERIES={
 "OA1_core_cryo_x_LA":f'({C}) AND ({LA})',
 "OA2_thoracic":f'({C}) AND (thoracotomy OR thoracic OR intercostal OR "rib fracture" OR "rib fractures" OR pectus OR Nuss OR "chest wall" OR VATS OR sternotomy)',
 "OA3_dental":f'({C}) AND (dental OR dentistry OR oral OR tooth OR palatal OR endodontic OR "inferior alveolar")',
 "OA4_vascular":f'({C}) AND (venipuncture OR venepuncture OR cannulation OR intravenous OR "vascular access" OR phlebotomy)',
 "OA5_orthopedic":f'({C}) AND (arthroplasty OR orthopedic OR orthopaedic OR "total knee" OR "total hip" OR genicular OR musculoskeletal)',
 "OA6_derm_office":f'({C}) AND (dermatology OR dermatologic OR laser OR "hair removal" OR "skin biopsy" OR "minor surgery" OR implant)',
 "OA7_periop":f'({C}) AND (postoperative OR perioperative OR postsurgical) AND ("nerve block" OR epidural OR "local anesthetic" OR "regional anesthesia")',
 "OA8_chronic_pain":f'({C}) AND (neuropathic OR "chronic pain")',
}
manifest=[];all_oa=[]
for qn,q in QUERIES.items():
    recs=[];total=None;page=0
    while page<25:
        u=("https://api.openalex.org/works?per_page=200"
           f"&filter=title_and_abstract.search:{urllib.parse.quote(q)}"
           f"&page={page+1}&mailto=bougtoir@gmail.com")
        data=get(u);save_raw(f"openalex_{qn}_p{page}.json",data)
        j=json.loads(data);total=j["meta"]["count"]
        for w in j["results"]:
            doi=(w.get("doi") or "").replace("https://doi.org/","")
            authors="; ".join(a["author"]["display_name"] for a in w.get("authorships",[]))
            recs.append({"openalex_id":w["id"],"title":w.get("title") or "",
              "authors":authors,"year":str(w.get("publication_year") or ""),
              "doi":doi,"pmid":(w.get("ids",{}).get("pmid") or "").rsplit("/",1)[-1],
              "source":(((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")})
        page+=1
        if not j["results"] or page*200>=total: break
        time.sleep(0.4)
    out=f"{EXP}/openalex_{qn}.json";json.dump(recs,open(out,"w"),indent=1)
    manifest.append({"source":"OpenAlex","platform":"OpenAlex API, filter=title_and_abstract.search (open index; declared substitute for Scopus/WoS — no subscription access)",
      "date":SEARCH_DATE,"query_id":qn,"query":q,"filters":"title_and_abstract field search",
      "language":"all (English applied at screening)","date_restriction":"none",
      "raw_hits":total,"exported_records":len(recs),"export_file":out})
    print("OA",qn,total,len(recs))
    for r in recs:r["query_id"]=qn
    all_oa+=recs;time.sleep(0.3)
# merge with existing manifest + records
mrows=list(csv.DictReader(open(f"{BASE}/SEARCH_EXPORT_MANIFEST.csv")))
mrows+=manifest
with open(f"{BASE}/SEARCH_EXPORT_MANIFEST.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["source","platform","date","query_id","query","filters","language","date_restriction","raw_hits","exported_records","export_file"])
    w.writeheader();w.writerows(mrows)
pubmed=[]
for qn in ["Q1_core_cryo_x_LA","Q2_core_cryo_x_pain","Q3_dental","Q4_vascular","Q5_thoracic","Q6_orthopedic","Q7_derm_office","Q8_ctgov_style_broad"]:
    p=f"{EXP}/pubmed_{qn}.json"
    for r in json.load(open(p)): r["query_id"]=qn
    pubmed+=json.load(open(p))
ct=json.load(open(f"{BASE}/oa_ct_records.json"))["ctgov"]
json.dump({"pubmed":pubmed,"openalex":all_oa,"ctgov":ct},open(f"{BASE}/all_records.json","w"),indent=1)
print("DONE",len(pubmed),len(all_oa),len(ct))
