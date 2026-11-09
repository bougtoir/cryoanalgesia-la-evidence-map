#!/usr/bin/env python3
"""Gates 5-7: build canonical datasets from classified candidates."""
import csv,re,json
res=[r for r in csv.DictReader(open("/home/ubuntu/pm_work/post_osf/candidates_classified.csv"))]
def get_n(a):
    m=re.search(r"(?:n\s*=\s*|(\d+)\s*(?:patients|participants|subjects|children|adults|cases))",a or "")
    if m:return m.group(0).replace("n = ","").replace("n= ","").strip() if m.group(0).startswith("n") else m.group(1)
    m2=re.findall(r"(\d+)\s+(?:patients|participants|subjects|children|adults)",a or "")
    return m2[0] if m2 else "NR"
def pv(a):
    m=re.search(r"p\s*[<=]\s*0?\.\d+",a or "")
    return m.group(0) if m else "NR"
primary=[];synth=[];proto=[];drop=[]
for r in res:
    pt=r["pubtype_tag"]
    if pt in ("synthesis_SR_MA","narrative_review"):
        synth.append(r);continue
    if pt.startswith("protocol") or r.get("nct"):
        proto.append(r);continue
    if pt=="case_report":
        drop.append((r,"case report <3 patients"));continue
    if pt=="other" and not re.search(r"(patient|cases|series|trial|study)",(r["abstract"] or ""),re.I):
        drop.append((r,"non-primary publication / unclear"));continue
    comp=r["comparator_signal"]
    if pt=="case_series" or comp=="noncomparative_signal":tier="C"
    elif comp=="LA_comparator_signal":tier="A"
    else:tier="B"
    a=r["abstract"] or ""
    primary.append({"study_id":r["record_id"],"cohort_id":r["record_id"],
      "primary_citation":(r["authors"].split(";")[0]+" "+r["year"]+" "+r["journal"]).strip(),
      "linked_secondary_citations":"","country":"","year":r["year"],"domain":r["domain"],
      "design":pt,"sample_size_total":get_n(a),"cryo_n":"NR","comparator_n":"NR",
      "cryo_modality":"","comparator_type":comp,"LA_comparator_yes_no":"yes" if comp=="LA_comparator_signal" else "no",
      "LA_type":"","adjunct_design_yes_no":"NR","tier":tier,
      "primary_outcome":"","outcome_timepoint":"","effect_direction":"","effect_estimate":"",
      "CI":"","p_value":pv(a),"persistent_pain_definition":"","opioid_outcome":"","functional_outcome":"",
      "adverse_events":"","follow_up":"","overlap_notes":"","interpretation_allowed":"","interpretation_not_allowed":"",
      "title":r["title"],"abstract":a,"doi":r["doi"],"pmid":r["pmid"]})
out="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_rebuild/"
cols=["study_id","cohort_id","primary_citation","linked_secondary_citations","country","year","domain","design","sample_size_total","cryo_n","comparator_n","cryo_modality","comparator_type","LA_comparator_yes_no","LA_type","adjunct_design_yes_no","tier","primary_outcome","outcome_timepoint","effect_direction","effect_estimate","CI","p_value","persistent_pain_definition","opioid_outcome","functional_outcome","adverse_events","follow_up","overlap_notes","interpretation_allowed","interpretation_not_allowed"]
with open("/home/ubuntu/pm_work/post_osf/primary_draft.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols+["comparator_signal","title","abstract","doi","pmid"]);w.writeheader();w.writerows(primary)
with open(out+"SYNTHESIS_REPORTS.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["record_id","title","authors","year","journal","pubtype_tag","domain","comparator_signal","doi","pmid"])
    w.writeheader();w.writerows([{k:r.get(k,"") for k in w.fieldnames} for r in synth])
with open(out+"PROTOCOLS_ONGOING.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["record_id","nct","title","authors","year","journal","pubtype_tag","domain","comparator_signal","doi","pmid","status","enrollment"])
    w.writeheader();w.writerows([{k:r.get(k,"") for k in w.fieldnames} for r in proto])
print("primary",len(primary),"synth",len(synth),"proto",len(proto),"drop",len(drop))
from collections import Counter
print(Counter((p["domain"],p["tier"]) for p in primary))
