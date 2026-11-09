#!/usr/bin/env python3
"""Gates 5-7 canonical outputs: MASTER_RECORDS update, PRIMARY_STUDY_MAP, TIER_A, counts, PRISMA."""
import csv,json
from collections import Counter
W="/home/ubuntu/pm_work/post_osf/"
OUT="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_rebuild/"
mrec={r["record_id"]:r for r in csv.DictReader(open(W+"MASTER_RECORDS.csv"))}
stage2={r["record_id"]:r for r in csv.DictReader(open(W+"stage2.csv"))}
tscreen={l.split("|")[0] for l in []}
tset={r["record_id"] for r in []}
title_dec={}
with open(W+"title_screen_ids.txt","w") as _:pass
# title_screen.csv keyed by record_id
title_dec={r["record_id"]:r for r in csv.DictReader(open(W+"title_screen.csv"))}
prim={r["study_id"]:r for r in csv.DictReader(open(W+"primary_final.csv"))}
synth={r["record_id"]:r for r in csv.DictReader(open(OUT+"SYNTHESIS_REPORTS.csv"))}
proto={r["record_id"]:r for r in csv.DictReader(open(OUT+"PROTOCOLS_ONGOING.csv"))}
for rid,r in mrec.items():
    if rid in prim:
        p=prim[rid];r["screening_status"]="included_primary_tier_"+p["tier"];r["exclusion_reason"]="";r["fulltext_status"]="abstract_and_metadata_verified"
    elif rid in synth:
        r["screening_status"]="synthesis_report_tracked";r["exclusion_reason"]="not a primary study";r["fulltext_status"]="abstract_and_metadata_verified"
    elif rid in proto:
        r["screening_status"]="protocol_ongoing_tracked";r["exclusion_reason"]="protocol/registration not primary evidence";r["fulltext_status"]="abstract_and_metadata_verified"
    elif rid in stage2:
        s2=stage2[rid]
        if s2["stage2_decision"]=="candidate":
            r["screening_status"]="excluded_eligibility";r["exclusion_reason"]=r["exclusion_reason"] or "out of scope at eligibility review (wrong publication type, non-analgesic cryo use, or non-clinical)";r["fulltext_status"]="abstract_verified"
        else:
            r["screening_status"]="excluded_abstract";r["exclusion_reason"]=s2["stage2_reason"];r["fulltext_status"]="abstract_screened"
    elif rid in title_dec:
        r["screening_status"]="excluded_title";r["exclusion_reason"]=title_dec[rid].get("reason","title off-topic");r["fulltext_status"]="title_screened"
    else:
        r["screening_status"]=r["screening_status"] or "excluded_title";r["fulltext_status"]=r["fulltext_status"] or "title_screened"
with open(OUT+"MASTER_RECORDS.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(mrec.values())[0].keys());w.writeheader();w.writerows(mrec.values())
# PRIMARY_STUDY_MAP: canonical cols + identifiers
cols=["study_id","cohort_id","primary_citation","linked_secondary_citations","country","year","domain","design","sample_size_total","cryo_n","comparator_n","cryo_modality","comparator_type","LA_comparator_yes_no","LA_type","adjunct_design_yes_no","tier","primary_outcome","outcome_timepoint","effect_direction","effect_estimate","CI","p_value","persistent_pain_definition","opioid_outcome","functional_outcome","adverse_events","follow_up","overlap_notes","interpretation_allowed","interpretation_not_allowed"]
extra=["title","doi","pmid","journal"]
with open(OUT+"PRIMARY_STUDY_MAP.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols+extra)
    w.writeheader()
    for r in prim.values():
        rr={k:r.get(k,"") for k in cols+extra}
        rr["journal"]=mrec[r["study_id"]]["journal"]
        w.writerow(rr)
ta=[r for r in prim.values() if r["tier"]=="A"]
with open(OUT+"TIER_A_COMPLETE.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols+extra);w.writeheader()
    for r in ta:
        rr={k:r.get(k,"") for k in cols+extra};rr["journal"]=mrec[r["study_id"]]["journal"];w.writerow(rr)
cc={"records_identified_total":18105,"records_pubmed":9509,"records_openalex":6239,"records_ctgov":357,"records_crossref":2000,
"records_after_dedup":len(mrec),"title_screened":len(mrec),"title_excluded":sum(1 for r in mrec.values() if r["screening_status"]=="excluded_title"),
"abstract_assessed":len(stage2),"abstract_excluded":sum(1 for r in stage2.values() if r["stage2_decision"]!="candidate"),
"eligibility_assessed":sum(1 for r in stage2.values() if r["stage2_decision"]=="candidate"),
"primary_study_reports":len(prim),"tier_A":len(ta),"tier_B":sum(1 for r in prim.values() if r["tier"]=="B"),
"tier_C":sum(1 for r in prim.values() if r["tier"]=="C"),
"synthesis_reports":len(synth),"protocols_ongoing":len(proto),
"language_policy":"English-only (prospective, declared)",
"searched_databases":["PubMed","OpenAlex","ClinicalTrials.gov","Crossref"],
"blocked_sources":"OpenAlex OA6-OA8 quota; CENTRAL/WHO ICTRP/Embase/Scopus/WoS not accessible"}
json.dump(cc,open(OUT+"CANONICAL_COUNTS.json","w"),indent=1)
with open(OUT+"CANONICAL_COUNTS.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["quantity","value"]);[w.writerow([k,v]) for k,v in cc.items()]
dom=Counter(r["domain"] for r in prim.values());ti=Counter(r["tier"] for r in prim.values())
pflow=[("Identification","records identified from databases",cc["records_identified_total"]),
("Identification","PubMed",cc["records_pubmed"]),("Identification","OpenAlex",cc["records_openalex"]),
("Identification","ClinicalTrials.gov",cc["records_ctgov"]),("Identification","Crossref",cc["records_crossref"]),
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
print(json.dumps({k:(v if not isinstance(v,list) else v) for k,v in cc.items()},indent=0)[:800])
print(dom)
EOF=1
