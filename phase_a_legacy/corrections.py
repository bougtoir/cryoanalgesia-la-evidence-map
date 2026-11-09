#!/usr/bin/env python3
import csv,re
rows=[r for r in csv.DictReader(open("/home/ubuntu/pm_work/primary_draft.csv"))]
MOVE_SYNTH={"R8ca3355a97","R0ef9081b27","Rd3148cda08"}
DROP={"R0170c07727":"sensory-testing study; cryo used as test stimulus not analgesia",
"Rfb4d6200ff":"sensory block testing device comparison; not analgesic outcome",
"Rd40a667a42":"spasticity outcome, not pain/analgesia",
"R6c60257529":"spasticity outcome, not pain/analgesia",
"Rad6902bf0f":None}
TO_B={"R3d4fc87b5b","R553da25e61","Rb349821abb","R76f1428b87","Raea7c55c62","R976936849f",
"R3f77dcc853","R6b54978e95","R9d2313f3b5","Rfdbf8bcff3","R96f0b59e1f"}
TO_C={"Rd9d37aa81f","R820d76bee2"}
OVERLAP_NUSS=lambda t: bool(re.search(r"(nuss|pectus|mirpe|ravitch)",t or "",re.I)) and "cohort" in ""
MODAL=[("Intercostal nerve cryoablation/cryoanalgesia",r"intercostal|thoracoscop"),
("Percutaneous cryoneurolysis/cryoneurotomy",r"cryoneurolysis|cryoneurotomy|percutaneous cryo"),
("Surgical/open cryoablation of nerves",r"cryoablation"),
("Vapocoolant spray",r"vapocoolant|cooling spray|cold spray"),
("Ethyl chloride spray",r"ethyl chloride|ethyl vinyl chloride"),
("Ice/cold pack or massage",r"ice|cold pack|ice massage|ice pack|cooling|precool|pre-cool"),
("Cryoanesthesia (other)",r"cryoanesth|cryoanaesth|cryoanalgesia")]
LAT=[("lidocaine",r"lidocaine|lignocaine"),("bupivacaine",r"bupivacaine"),("ropivacaine",r"ropivacaine"),
("mepivacaine",r"mepivacaine"),("prilocaine",r"prilocaine"),("articaine",r"articaine"),
("EMLA (lidocaine-prilocaine)",r"emla|eutectic"),("benzocaine",r"benzocaine"),("tetracaine",r"tetracaine"),
("dyclonine",r"dyclonine"),("chloroprocaine",r"chloroprocaine"),("procaine",r"\bprocaine\b"),
("epidural analgesia (LA-containing)",r"epidural"),("spinal/subarachnoid (LA)",r"spinal an|subarachnoid"),
("nerve block (LA)",r"nerve block|paravertebral|serratus|plane block|field block|intercostal block"),
("topical LA (unspecified)",r"topical (anaesthet|anesthet)|local anaesthet|local anesthet")]
DIRY=[("favors_cryoanalgesia",r"(significant(ly)? (greater|better|lower|more effective|reduced)|superior|improved).{0,80}(cryo|vapocoolant|cold|cooling|ice|ethyl chloride)|cryo\w*.{0,60}(significant(ly)? (greater|better|lower|more effective|reduced)|superior|reduced|improv)"),
("favors_comparator",r"(lidocaine|emla|topical|epidural).{0,60}(better|superior|lower pain|more effective)|(worse|higher|increased|greater) (pain|score).{0,60}(cryo|vapocoolant|cold|ice|ethyl chloride)|(lignocaine|lidocaine) is a better"),
("no_significant_difference",r"no (significant )?(statistical )?(difference|differences)|comparable|equally effective|similar (efficacy|pain|effect)|non-?inferior|did not (differ|reduce)|no benefit|fails to (decrease|reduce)|equivalent")]
OUT=[("pain intensity (VAS/NRS)",r"vas|visual analog|numerical rating|nrs|pain score|pain intensity"),
("opioid consumption",r"opioid|morphine|ome|mme|narcotic"),
("procedural pain",r"procedural pain|injection pain|puncture pain|insertion pain"),
("persistent/neuropathic pain",r"persistent|chronic|neuropathic|postsurgical pain syndrome|postthoracotomy pain syndrome"),
("patient satisfaction/preference",r"satisf|preference|acceptab|comfort"),
("adverse events/safety",r"adverse|complication|neuroprax|nerve damage|safe")]
drop_rows=[]
for r in rows:
    t=(r["title"] or "");a=(r["abstract"] or "");text=t+" "+a
    sid=r["study_id"]
    if sid in MOVE_SYNTH:
        drop_rows.append((r,"synthesis/systematic review"));continue
    if sid in DROP and DROP[sid]:
        drop_rows.append((r,DROP[sid]));continue
    if sid=="Rad6902bf0f":
        r["overlap_notes"]="secondary psychometric analysis of a cryoneurolysis RCT cohort; linked to parent trial"
    if sid in TO_B:r["tier"]="B"
    if sid in TO_C:r["tier"]="C";r["interpretation_not_allowed"]="noncomparative evidence"
    for name,p in MODAL:
        if re.search(p,text,re.I):r["cryo_modality"]=name;break
    if not r["cryo_modality"]:r["cryo_modality"]="unspecified cryoanalgesic technique"
    la=[n for n,p in LAT if re.search(p,text,re.I)]
    r["LA_type"]="; ".join(la) if r["tier"]=="A" else ""
    if r["tier"]=="A":
        r["adjunct_design_yes_no"]="yes" if re.search(r"(plus|combined with|in addition|adjunct|along with|with or without)",t+a[:400],re.I) else "no"
    for n,p in OUT:
        if re.search(p,text,re.I):r["primary_outcome"]=n;break
    for n,p in DIRY:
        if re.search(p,a,re.I):r["effect_direction"]=n;break
    if not r["effect_direction"]:r["effect_direction"]="unclear/NR"
    tp=re.search(r"(\d+\s?(h|hr|hours|hours?|days?|weeks?|months?|year)s?)[^.\n]{0,40}",a,re.I)
    r["follow_up"]=tp.group(0)[:60] if tp else "NR"
    r["outcome_timepoint"]=r["follow_up"]
    r["opioid_outcome"]="reported" if re.search(r"opioid|morphine|\bome\b|\bmme\b|narcotic",a,re.I) else "NR"
    r["adverse_events"]="reported" if re.search(r"adverse|complication|nerve (injury|damage|deficit)|neuroprax|safety",a,re.I) else "NR"
    m=re.search(r"[^.]*(persistent|chronic postsurgical|neuropathic)[^.]*\.",a,re.I)
    if m:r["persistent_pain_definition"]=m.group(0).strip()[:300]
    if r["tier"]=="A" and not r["overlap_notes"] and re.search(r"(nuss|pectus|mirpe|ravitch)",t,re.I) and r["design"]!="RCT":
        r["overlap_notes"]="possible cohort overlap with other MIRPE/Nuss cryoablation cohort reports; unique-cohort status unconfirmed from metadata"
    r["interpretation_allowed"]="comparative signal reported in abstract" if r["tier"]=="A" else ("indirect comparator" if r["tier"]=="B" else "")
    if r["tier"]=="C":r["interpretation_not_allowed"]="noncomparative evidence"
    r["comparator_type"]={"A":"LA-based technique (direct comparator)","B":"indirect comparator (sham/placebo/usual/opioid/non-LA/adjunct)","C":"none" }[r["tier"]]
kept=[r for r in rows if r["study_id"] not in {d[0]["study_id"] for d in drop_rows}]
with open("/home/ubuntu/pm_work/primary_final.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(kept)
from collections import Counter
print("kept",len(kept),"dropped",len(drop_rows),Counter(r["tier"] for r in kept),Counter((r["domain"],r["tier"]) for r in kept))
