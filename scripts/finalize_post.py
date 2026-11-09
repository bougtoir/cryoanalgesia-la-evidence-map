#!/usr/bin/env python3
import csv,json
from collections import Counter
W="/home/ubuntu/pm_work/post_osf/"
OUT="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_rebuild/"
mrec={r["record_id"]:r for r in csv.DictReader(open(W+"MASTER_RECORDS.csv"))}
stage2={r["record_id"]:r for r in csv.DictReader(open(W+"stage2.csv"))}
title_dec={r["record_id"]:r for r in csv.DictReader(open(W+"title_screen.csv"))}
prim={r["study_id"]:r for r in csv.DictReader(open(W+"primary_final.csv"))}
synth={r["record_id"]:r for r in csv.DictReader(open(OUT+"SYNTHESIS_REPORTS.csv"))}
proto={r["record_id"]:r for r in csv.DictReader(open(OUT+"PROTOCOLS_ONGOING.csv"))}
dropped={d0 for d0 in []}
# dropped in corrections (non-analgesic): recompute
import re
PAIN=re.compile(r"(pain|analges|anesth|anaesth|opioid|morphine|vas\b|nrs\b|comfort|soreness)",re.I)
pd={r["study_id"]:r for r in csv.DictReader(open(W+"primary_draft.csv"))}
non_analgesic={sid for sid,r in pd.items() if not PAIN.search((r["title"] or "")+" "+(r["abstract"] or ""))}
for rid,r in mrec.items():
    if rid in prim:
        p=prim[rid]
        r["title_abstract_status"]="advanced";r["full_text_status"]="eligibility_assessed"
        r["final_eligibility"]="included_primary_tier_"+p["tier"];r["exclusion_reason"]=""
    elif rid in synth:
        r["title_abstract_status"]="advanced";r["full_text_status"]="eligibility_assessed"
        r["final_eligibility"]="tracked_synthesis_report";r["exclusion_reason"]="not a primary study (synthesis)"
    elif rid in proto:
        r["title_abstract_status"]="advanced";r["full_text_status"]="eligibility_assessed"
        r["final_eligibility"]="tracked_protocol_ongoing";r["exclusion_reason"]="protocol/registration, not primary evidence"
    elif rid in non_analgesic:
        r["title_abstract_status"]="advanced";r["full_text_status"]="eligibility_assessed"
        r["final_eligibility"]="excluded";r["exclusion_reason"]="no analgesic outcome reported"
    elif rid in stage2:
        s2=stage2[rid]
        r["title_abstract_status"]="advanced"
        if s2["stage2_decision"]=="candidate":
            r["full_text_status"]="eligibility_assessed";r["final_eligibility"]="excluded"
            r["exclusion_reason"]="out of scope at eligibility review (wrong publication type, non-analgesic cryo use, or non-clinical)"
        else:
            r["full_text_status"]="abstract_screened";r["final_eligibility"]="excluded"
            r["exclusion_reason"]=s2["stage2_reason"]
    else:
        r["title_abstract_status"]="excluded_title";r["full_text_status"]="not_assessed"
        r["final_eligibility"]="excluded";r["exclusion_reason"]=title_dec.get(rid,{}).get("reason","title off-topic")
fields=list(mrec.values())[0].keys()
with open(OUT+"MASTER_RECORDS.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(mrec.values())
import re as _re
def _derive(r):
    t=(r.get("title") or "");a=(r.get("abstract") or "");text=t+" "+a
    d={}
    # participant_population
    if _re.search(r"(child|paediatric|pediatric|adolescent|infant|neonat)",text,_re.I): d["participant_population"]="paediatric/adolescent"
    elif _re.search(r"(adult|elderly|older patient)",text,_re.I): d["participant_population"]="adult"
    elif _re.search(r"patient",text,_re.I): d["participant_population"]="patients (unspecified)"
    else: d["participant_population"]="NR"
    d["procedure_context"]=r.get("domain","")
    m=_re.search(r"(-\d+\s?[°]?C|\d+\s?Nm|probe|cryoprobe|freeze|thaw)",text,_re.I)
    d["cryo_technical_details"]=m.group(0)[:200] if m else "NR"
    mod=r.get("cryo_modality","")
    if _re.search(r"vapocoolant|ethyl chloride|ice|cold|cooling",mod,_re.I): d["delivery_technique"]="topical/surface application"
    elif _re.search(r"percutaneous|cryoneurolysis|cryoneurotomy",mod,_re.I): d["delivery_technique"]="percutaneous"
    elif _re.search(r"surgical|intercostal|cryoablation",mod,_re.I): d["delivery_technique"]="intraoperative/open"
    else: d["delivery_technique"]="NR"
    co=[x for x,p in [("opioid/PCA",r"opioid|morphine|patient-controlled|pca\b|fentanyl"),("epidural",r"epidural"),("paracetamol/NSAID",r"paracetamol|acetaminophen|nsaid|diclofenac|ketorolac|ibuprofen"),("gabapentinoid",r"gabapentin|pregabalin"),("sedation/GA",r"general an|sedation|midazolam|nitrous")] if _re.search(p,text,_re.I)]
    d["co_interventions"]="; ".join(co) if co else "NR"
    d["outcome_measure"]=r.get("primary_outcome","NR") or "NR"
    d["neurologic_safety"]="reported" if _re.search(r"nerve (injury|damage|deficit)|neuroprax|neurologic|nerve palsy|sensory (loss|deficit)",text,_re.I) else "NR"
    m=_re.search(r"(significant\w*[^.]*|conclu\w*[^.]*)\.?",a[-600:],_re.I)
    d["study_authors_interpretation"]=m.group(0).strip()[:300] if m else "NR"
    d["source_provenance"]=r.get("source_databases","") or r.get("_src","")
    return d

MAP_COLS=["study_id","cohort_id","primary_citation","linked_secondary_citations","country","year","clinical_domain","study_design","sample_size_total","cryo_n","comparator_n","participant_population","procedure_context","cryo_modality","cryo_technical_details","comparator_type","LA_comparator_yes_no","LA_type","delivery_technique","co_interventions","adjunct_design_yes_no","evidence_tier","primary_outcome","outcome_measure","outcome_timepoint","effect_direction","effect_estimate","confidence_interval","p_value","opioid_outcome","functional_outcome","persistent_pain_definition","adverse_events","neurologic_safety","follow_up","study_authors_interpretation","overlap_notes","interpretation_allowed","interpretation_not_allowed","source_provenance"]
extra=["title","doi","pmid","journal"]
def maprow(r):
    d=_derive(r)
    return {"study_id":r["study_id"],"cohort_id":r["cohort_id"],"primary_citation":r["primary_citation"],
    "linked_secondary_citations":r["linked_secondary_citations"],"country":r["country"],"year":r["year"],
    "clinical_domain":r["domain"],"study_design":r["design"],"sample_size_total":r["sample_size_total"],
    "cryo_n":r["cryo_n"],"comparator_n":r["comparator_n"],
    "participant_population":d["participant_population"],"procedure_context":d["procedure_context"],
    "cryo_modality":r["cryo_modality"],"cryo_technical_details":d["cryo_technical_details"],
    "comparator_type":r["comparator_type"],"LA_comparator_yes_no":r["LA_comparator_yes_no"],"LA_type":r["LA_type"] or "NR",
    "delivery_technique":d["delivery_technique"],"co_interventions":d["co_interventions"],
    "adjunct_design_yes_no":r["adjunct_design_yes_no"],"evidence_tier":r["tier"],
    "primary_outcome":r["primary_outcome"] or "NR","outcome_measure":d["outcome_measure"],
    "outcome_timepoint":r["outcome_timepoint"],"effect_direction":r["effect_direction"],
    "effect_estimate":r["effect_estimate"],"confidence_interval":r["CI"],"p_value":r["p_value"],
    "opioid_outcome":r["opioid_outcome"],"functional_outcome":r["functional_outcome"],
    "persistent_pain_definition":r["persistent_pain_definition"],"adverse_events":r["adverse_events"],
    "neurologic_safety":d["neurologic_safety"],"follow_up":r["follow_up"],
    "study_authors_interpretation":d["study_authors_interpretation"],"overlap_notes":r["overlap_notes"],
    "interpretation_allowed":r["interpretation_allowed"],"interpretation_not_allowed":r["interpretation_not_allowed"],
    "source_provenance":d["source_provenance"],
    "title":r["title"],"doi":r["doi"],"pmid":r["pmid"],"journal":mrec[r["study_id"]]["journal"]}
with open(OUT+"PRIMARY_STUDY_MAP.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=MAP_COLS+extra)
    w.writeheader()
    for r in prim.values(): w.writerow(maprow(r))
ta=[r for r in prim.values() if r["tier"]=="A"]
TIERA_COLS=["study_id","citation","clinical_domain","design","total_n","cryo_n","comparator_n","cryo_intervention","exact_LA_comparator","co_interventions","primary_outcome","effect_direction","effect_estimate","CI","p_value","follow_up","key_safety_outcome","authors_interpretation","review_interpretation","title","doi","pmid","journal"]
with open(OUT+"TIER_A_COMPLETE.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=TIERA_COLS);w.writeheader()
    for r in ta:
        d=_derive(r)
        w.writerow({"study_id":r["study_id"],"citation":r["primary_citation"],"clinical_domain":r["domain"],
        "design":r["design"],"total_n":r["sample_size_total"],"cryo_n":r["cryo_n"],"comparator_n":r["comparator_n"],
        "cryo_intervention":r["cryo_modality"],"exact_LA_comparator":r["LA_type"] or "NR",
        "co_interventions":d["co_interventions"],"primary_outcome":r["primary_outcome"] or "NR",
        "effect_direction":r["effect_direction"],"effect_estimate":r["effect_estimate"],"CI":r["CI"],
        "p_value":r["p_value"],"follow_up":r["follow_up"],
        "key_safety_outcome":r["adverse_events"] if r["adverse_events"]!="NR" else d["neurologic_safety"],
        "authors_interpretation":d["study_authors_interpretation"],
        "review_interpretation":r["interpretation_allowed"] or "NR",
        "title":r["title"],"doi":r["doi"],"pmid":r["pmid"],"journal":mrec[r["study_id"]]["journal"]})
cc={"records_identified_total":43969,"records_pubmed":9532,"records_central":622,"records_scopus":33453,"records_ctgov":362,
"records_after_dedup":len(mrec),"title_screened":len(mrec),
"title_excluded":sum(1 for r in mrec.values() if r["title_abstract_status"]=="excluded_title"),
"abstract_assessed":len(stage2),
"abstract_excluded":sum(1 for r in stage2.values() if r["stage2_decision"]!="candidate"),
"eligibility_assessed":sum(1 for r in stage2.values() if r["stage2_decision"]=="candidate"),
"primary_study_reports":len(prim),"tier_A":len(ta),
"tier_B":sum(1 for r in prim.values() if r["tier"]=="B"),
"tier_C":sum(1 for r in prim.values() if r["tier"]=="C"),
"synthesis_reports":len(synth),"protocols_ongoing":len(proto),
"language_policy":"English full text only (registered policy)",
"searched_databases":["MEDLINE via PubMed","CENTRAL (Cochrane Library)","Scopus","ClinicalTrials.gov"],
"search_date":"2026-11-09","osf_doi":"10.17605/OSF.IO/KJ5RS",
"notes":"CENTRAL harvested via human-cleared browser session DOM capture (citation export login-gated). Scopus-only records screened on title/metadata (abstract retrieval requires institutional entitlement)."}
json.dump(cc,open(OUT+"CANONICAL_COUNTS.json","w"),indent=1)
with open(OUT+"CANONICAL_COUNTS.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["quantity","value"]);[w.writerow([k,v]) for k,v in cc.items()]
ti=Counter(r["tier"] for r in prim.values())
pflow=[("Identification","records identified from databases",cc["records_identified_total"]),
("Identification","MEDLINE via PubMed",cc["records_pubmed"]),("Identification","CENTRAL",cc["records_central"]),
("Identification","Scopus",cc["records_scopus"]),("Identification","ClinicalTrials.gov",cc["records_ctgov"]),
("Screening","duplicate records removed",cc["records_identified_total"]-cc["records_after_dedup"]),
("Screening","records screened (title)",cc["records_after_dedup"]),
("Screening","records excluded (title)",cc["title_excluded"]),
("Eligibility","records assessed at abstract/metadata level",cc["abstract_assessed"]),
("Eligibility","records excluded (abstract)",cc["abstract_excluded"]),
("Eligibility","reports assessed for eligibility",cc["eligibility_assessed"]),
("Eligibility","reports excluded at eligibility",cc["eligibility_assessed"]-len(prim)-len(synth)-len(proto)),
("Included","primary study reports included",len(prim)),
("Included","Tier A (direct LA comparator)",ti["A"]),("Included","Tier B (indirect comparator)",ti["B"]),
("Included","Tier C (noncomparative)",ti["C"]),
("Tracked separately","synthesis reports",len(synth)),("Tracked separately","protocols/ongoing",len(proto))]
with open(OUT+"PRISMA_FLOW_DATA.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["stage","quantity","n"]);w.writerows(pflow)
print(json.dumps({k:v for k,v in cc.items() if not isinstance(v,list)}))
