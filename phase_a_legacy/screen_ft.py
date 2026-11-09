#!/usr/bin/env python3
"""Stage-3 (full-text-proxy) screening: cryo must be THE analgesic intervention studied."""
import csv,re
cand=[r for r in csv.DictReader(open("/home/ubuntu/pm_work/stage2.csv")) if r["stage2_decision"]=="candidate"]
TITLE_CRYO_ANALG=re.compile(
 r"(cryoanalgesia|cryoanesthesia|cryoanaesthesia|cryoneurolysis|cryoneurotomy|"
 r"cryoablation.*(pain|analges|nerve|intercostal|genicular|neuroma|post-?thorac|pectus|thorac|post-?surg|post-?operat)|"
 r"cryo.*(pain management|analgesia|anesthesia|anaesthesia|nerve block)|"
 r"(ice|cold|cooling|vapocoolant|ethyl chloride|precool|pre-cool).*(analgesia|anesthesia|anaesthesia|injection pain|venipuncture|cannulation|puncture|biopsy|procedure|injection|block|pain)|"
 r"(analgesia|anesthesia|anaesthesia|pain).*(ice|cold|cooling|vapocoolant|ethyl chloride|precool|pre-cool))",re.I)
# exclusion: cryo used for something else (nerve injury Rx without analgesia measured is still analgesic often; keep)
DROP=re.compile(r"(denture|orthodontic bracket|cryosurgery|keratosis|wart|verruca|mollusc|condylom|leishman|papilloma|granuloma|keloid|angioma|leiomyoma|retinopathy|mucositis|frostbite|cryolipolysis|fat|ovarian|oocyte|embryo|sperm|cryopreserv|tumou?r|fibroadenoma|renal|prostate|hepatic|lung nodule|atrial|ventricular|mycetoma|endobronchial|desmoid|chondroblastoma|osteoblastoma|osteoid|plantar fibroma|sport|athletic|exercise|muscle soreness|doms|dysmenorrhea|veterinary|rat|mouse|porcine)",re.I)
kept=[]
for r in cand:
    t=r["title"] or "";a=r["abstract"] or ""
    if not TITLE_CRYO_ANALG.search(t):
        continue
    if DROP.search(t) and not re.search(r"(analges|pain|anesth|anaesth|block)",t,re.I):
        continue
    kept.append(r)
print("kept",len(kept))
for r in kept:
    print(r["record_id"],"|",r["year"],"|",r["pubtype_tag"],"|",(r["title"] or "")[:130])
