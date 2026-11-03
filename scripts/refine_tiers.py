#!/usr/bin/env python3
import csv,re
rows=[r for r in csv.DictReader(open("/home/ubuntu/pm_work/primary_draft.csv"))]
LA=re.compile(r"(lidocaine|lignocaine|bupivacaine|ropivacaine|levobupivacaine|mepivacaine|prilocaine|articaine|benzocaine|emla|eutectic|tetracaine|chloroprocaine|procaine|dyclonine|local anaesthet|local anesthet|topical anaesthet|topical anesthet|epidural|spinal an|subarachnoid|intercostal (nerve )?block|paravertebral|nerve block|serratus|plane block|field block|regional an|patient-controlled epidural|pca epidural|peripheral nerve block)",re.I)
CUE=re.compile(r"(vs\.?|versus|compared|comparative|comparison|randomi|allocated|assign|arm|group [a-z1-4]|received|either|treated with|controlled|prospective|crossover|cross-over)",re.I)
def near(text,pat,cue,win=220):
    for m in pat.finditer(text):
        s=max(0,m.start()-win);e=min(len(text),m.end()+win)
        if cue.search(text[s:e]):return True
    return False
for r in rows:
    text=(r["title"] or "")+" "+(r["abstract"] or "")
    if r["tier"]=="C":continue
    if r["design"]=="case_series":r["tier"]="C";r["interpretation_not_allowed"]="noncomparative";continue
    if near(text,LA,CUE):r["tier"]="A"
    else:
        IND=re.compile(r"(sham|placebo|usual care|standard care|conventional (analgesia|pain management)|opioid|morphine|control group|no (analgesia|treatment)|oral analges|acetaminophen|paracetamol|nsaid|indomethacin|diclofenac|ketorolac|nitrous oxide|tens\b|transcutaneous|fentanyl|patient-controlled analgesia|pcia|sedation|midazolam|radiofrequency|pregabalin|no pretreatment|uncooled)",re.I)
        r["tier"]="B" if (near(text,IND,CUE) or r["comparator_signal"]!="noncomparative_signal") else "C"
    if r["tier"]=="C" and not r["interpretation_not_allowed"]:r["interpretation_not_allowed"]="noncomparative evidence"
from collections import Counter
print(len(rows),Counter((r["domain"],r["tier"]) for r in rows))
with open("/home/ubuntu/pm_work/primary_draft.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
