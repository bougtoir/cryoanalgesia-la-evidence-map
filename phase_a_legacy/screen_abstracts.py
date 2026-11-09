#!/usr/bin/env python3
"""Stage-2 screening on title+abstract; publication-type tagging."""
import csv,json,re
rows={r["record_id"]:r for r in csv.DictReader(open("/home/ubuntu/pm_work/MASTER_RECORDS.csv"))}
keep_ids=[r[0] for r in csv.reader(open("/home/ubuntu/pm_work/title_screen.csv")) if r[0]!="record_id" and r[1]=="advance_to_abstract"]
abs_=json.load(open("/home/ubuntu/pm_work/abstracts.json"))

PAIN=re.compile(r"(pain|analges|anesth|anaesth|block|vas|nrs|opioid|morphine|comfort|postoperative|sore)",re.I)
CLINICAL=re.compile(r"(patient|randomi|trial|cohort|prospective|retrospective|case series|cases|children|adult|surg|procedur|clinic|hospital|volunteer|participants|undergoing)",re.I)
NONHUMAN2=re.compile(r"\b(rats?|mice|mouse|porcine|swine|canine|feline|rabbit|wistar|sprague|animal)\b",re.I)
WRONG2=re.compile(r"(tumou?r|fibroadenoma|renal|prostate|cervical cancer|hepatic|lung nodule|cardiac ablation|atrial|ventricular|mycetoma|wart|verruca|mollusc|condylom|leishman|actinic|seborrheic|papilloma|granuloma|keloid|angioma|retinopathy|mucositis|oral cryotherapy|frostbite|cryolipolysis|fat reduction|muscle soreness|delayed onset|doms|exercise|sport|athletic|recovery after (exercise|sport)|ovarian|oocyte|embryo|sperm|cryopreserv|physiotherapy|subacromial|trigger point|dysmenorrhea)",re.I)
ANALGESIC_NEED=re.compile(r"(analges|pain|anesth|anaesth|block|comfort during|procedural)",re.I)

def tag_pubtype(r,abstract,pts):
    t=(r["title"] or "").lower();a=(abstract or "").lower();pt=" ".join(pts).lower()
    if r.get("nct") or "nct0" in (r.get("doi","")):return "protocol/registration"
    if "randomized" in pt or "randomised" in pt or "randomized" in a or "randomised" in a or "rct" in t:return "RCT"
    if "meta-analysis" in pt or "meta-analysis" in t or "meta analysis" in t or "systematic review" in pt or "systematic review" in t or "cochrane" in t:return "synthesis_SR_MA"
    if "review" in pt and "journal" not in pt:return "narrative_review"
    if re.search(r"\breview\b",t) and "case" not in t:return "narrative_review"
    if "protocol" in t or "study protocol" in a:return "protocol"
    if "case report" in pt or "case rep" in t:return "case_report"
    if re.search(r"case series|series of \d+|\bwe report\b",t+" "+a):return "case_series"
    if re.search(r"cohort|prospective|retrospective|observational|registry|series",pt+a):return "cohort/observational"
    if "comparative study" in pt or "clinical trial" in pt:return "comparative/RCT?"
    return "other"

out=[]
for rid in keep_ids:
    r=rows[rid]
    pm=r["pmid"]
    abstract=abs_.get(pm,{}).get("abstract","") if pm else ""
    pts=abs_.get(pm,{}).get("pubtypes",[]) if pm else []
    text=(r["title"] or "")+" "+abstract
    reason=None
    if NONHUMAN2.search(text) and not re.search(r"(patient|human|volunteer)",text,re.I):
        reason="nonhuman"
    elif WRONG2.search(text):
        reason="wrong intervention (non-analgesic application)"
    elif not ANALGESIC_NEED.search(text):
        reason="no clinical analgesic outcome (abstract-level)"
    elif not CLINICAL.search(text):
        reason="non-clinical record"
    pt=tag_pubtype(r,abstract,pts)
    out.append({**r,"abstract":abstract[:4000],"pubtype_tag":pt,"stage2_decision":"candidate" if reason is None else "excluded_abstract","stage2_reason":reason or ""})

with open("/home/ubuntu/pm_work/stage2.csv","w",newline="") as f:
    fields=list(out[0].keys())
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
cand=[o for o in out if o["stage2_decision"]=="candidate"]
print("candidates",len(cand),"excluded2",len(out)-len(cand))
from collections import Counter
print(Counter(o["pubtype_tag"] for o in cand))
print(Counter(o["stage2_reason"] for o in out if o["stage2_decision"]!="candidate"))
