#!/usr/bin/env python3
import csv,json,time,urllib.parse,urllib.request,re
keep=[r[0] for r in csv.reader(open("/home/ubuntu/pm_work/post_osf/title_screen.csv")) if r[0]!="record_id" and r[1]=="advance_to_abstract"]
rows={r["record_id"]:r for r in csv.DictReader(open("/home/ubuntu/pm_work/post_osf/MASTER_RECORDS.csv"))}
pmids=[rows[r]["pmid"] for r in keep if rows[r]["pmid"]]
print("pmids to fetch",len(pmids))
UA={"User-Agent":"pain-medicine-scoping-review/1.0"}
def get(u,retries=4):
    for i in range(retries):
        try:
            req=urllib.request.Request(u,headers=UA)
            with urllib.request.urlopen(req,timeout=60) as r:return r.read().decode("utf-8","replace")
        except Exception as e:
            print("retry",i,e);time.sleep(4*(i+1))
    raise RuntimeError(u)
out={}
for i in range(0,len(pmids),200):
    batch=pmids[i:i+200]
    u=("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed"
       f"&id={','.join(batch)}&retmode=xml")
    xml=get(u)
    open(f"/home/ubuntu/pm_work/post_osf/raw/abstracts_{i}.xml","w").write(xml)
    # parse simple
    for art in re.finditer(r"<PubmedArticle>(.*?)</PubmedArticle>",xml,re.S):
        a=art.group(1)
        pmid=re.search(r"<PMID[^>]*>(\d+)</PMID>",a)
        abstr=" ".join(re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>",a,re.S))
        abstr=re.sub(r"<[^>]+>"," ",abstr)
        pt=re.findall(r"<PublicationType[^>]*>(.*?)</PublicationType>",a)
        if pmid:out[pmid.group(1)]={"abstract":re.sub(r"\s+"," ",abstr).strip(),"pubtypes":pt}
    time.sleep(0.5)
json.dump(out,open("/home/ubuntu/pm_work/post_osf/abstracts.json","w"))
print("fetched",len(out))
