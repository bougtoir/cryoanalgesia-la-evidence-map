#!/usr/bin/env python3
"""Domain + comparator classification for the stage-3 corpus -> candidates_classified.csv"""
import csv,re
cand=[r for r in csv.DictReader(open("/home/ubuntu/pm_work/post_osf/stage2.csv")) if r["stage2_decision"]=="candidate"]
TITLE_CRYO_ANALG=re.compile(
 r"(cryoanalgesia|cryoanesthesia|cryoanaesthesia|cryoneurolysis|cryoneurotomy|"
 r"cryoablation.*(pain|analges|nerve|intercostal|genicular|neuroma|post-?thorac|pectus|thorac|post-?surg|post-?operat)|"
 r"cryo.*(pain management|analgesia|anesthesia|anaesthesia|nerve block)|"
 r"(ice|cold|cooling|vapocoolant|ethyl chloride|precool|pre-cool).*(analgesia|anesthesia|anaesthesia|injection pain|venipuncture|cannulation|puncture|biopsy|procedure|injection|block|pain)|"
 r"(analgesia|anesthesia|anaesthesia|pain).*(ice|cold|cooling|vapocoolant|ethyl chloride|precool|pre-cool))",re.I)
DROP=re.compile(r"(denture|orthodontic bracket|cryosurgery|keratosis|wart|verruca|mollusc|condylom|leishman|papilloma|granuloma|keloid|angioma|leiomyoma|retinopathy|mucositis|frostbite|cryolipolysis|fat|ovarian|oocyte|embryo|sperm|cryopreserv|tumou?r|fibroadenoma|renal|prostate|hepatic|lung nodule|atrial|ventricular|mycetoma|endobronchial|desmoid|chondroblastoma|osteoblastoma|osteoid|plantar fibroma|sport|athletic|exercise|muscle soreness|doms|dysmenorrhea|veterinary|rat\b|mice|mouse|porcine)",re.I)
# general-anesthesia ethyl chloride (inhaled GA, not peripheral cryoanalgesia)
GA_ETHYL=re.compile(r"(ethyl chloride (anesthesia|anaesthesia)|anaesthesia with.*ethyl chloride|general an[aé]sthesia.*ethyl chloride)",re.I)
DOMAINS=[
 ("thoracic_chestwall",re.compile(r"(thorac|intercostal|rib|chest|pectus|nuss|sternotomy|vats|pleur|mastectomy|rib fracture|lung resection)",re.I)),
 ("dental_oral",re.compile(r"(dental|dentistry|oral|tooth|teeth|palatal|endodont|pulp|alveolar|molar|incisor|extraction|periodont|tonsillectomy|tonsill)",re.I)),
 ("vascular_access",re.compile(r"(venipuncture|venepuncture|cannulation|intravenous|vascular access|phlebotomy|heel ?stick|heelstick|arterial puncture|immuni[sz]ation|vaccin|injection pain|blood draw|venous)",re.I)),
 ("orthopedic_msk",re.compile(r"(arthroplasty|orthopedic|orthopaedic|knee|hip|spine|spinal|genicular|musculoskeletal|amputation|fracture(?!.*rib)|bone|joint|tka|tkr|facet|zygapophys|back pain|lumbar)",re.I)),
 ("derm_office",re.compile(r"(dermat|skin|laser|hair removal|biopsy|botulinum|botox|hyperhidrosis|minor (surgery|procedure)|office|implant|etonogestrel|nexplanon|goserelin|skin graft|donor site|skin test|intradermal|subcutaneous)",re.I)),
 ("chronic_pain_neurolysis",re.compile(r"(neuralgia|neuropathic|chronic pain|intractable|neuroma|post-?herpetic|phantom|occipital|ilioinguinal|iliohypogastric|genitofemoral|pudendal|facet|suprascapular|intercostal neuralgia|pain syndrome|sacroiliac|cervicogenic|trigeminal|temporomandibular|phantom limb|coccyg|cancer pain|metasta)",re.I)),
 ("periop_other",re.compile(r"(herniorrhaphy|hernia|surgery|surgical|operative|postoperative|abdominal|cardiac surgery|tonsillectomy|ocular|corneal|phaco|cataract|eye|endometrial|menorrhagia|labor|labour|episiotomy|sting|envenomation|burn)",re.I)),
]
LA_PAT=re.compile(r"(lidocaine|lignocaine|bupivacaine|ropivacaine|levobupivacaine|mepivacaine|prilocaine|articaine|benzocaine|emla|eutectic|tetracaine|chloroprocaine|procaine|dyclonine|local anaesthet|local anesthet|topical anaesthet|topical anesthet|epidural|spinal an|subarachnoid|intercostal (nerve )?block|paravertebral|nerve block|serratus|plane block|field block|infiltration (of|with) (lidocaine|local)|regional an|patient-controlled epidural|pca epidural|peripheral nerve block)",re.I)
SHAM_PAT=re.compile(r"(sham|placebo|usual care|standard care|conventional (analgesia|pain management)|opioid|morphine|control group|no (analgesia|treatment)|oral analges|acetaminophen|paracetamol|nsaid|indomethacin|diclofenac|ketorolac|nitrous oxide|tens\b|transcutaneous|pento?zocine|pentazocine|fentanyl|patient-controlled analgesia|pcia|sedation|nitrous|midazolam|external-beam|radiation therapy|radiofrequency|pulsed radiofrequency|prf\b|pregabalin|hot water|warming|no pretreatment|nothing\b|uncooled|room temperature)",re.I)
res=[]
for r in cand:
    t=r["title"] or "";a=r["abstract"] or ""
    if not TITLE_CRYO_ANALG.search(t):continue
    if DROP.search(t) and not re.search(r"(analges|pain|anesth|anaesth|block)",t,re.I):continue
    if GA_ETHYL.search(t):continue
    text=t+" "+a
    dom="other_procedural"
    for d,pat in DOMAINS:
        if pat.search(text):dom=d;break
    la=LA_PAT.search(text);sh=SHAM_PAT.search(text)
    if la: comp="LA_comparator_signal"
    elif sh: comp="indirect_comparator_signal"
    else: comp="noncomparative_signal"
    res.append({**r,"domain":dom,"comparator_signal":comp})
with open("/home/ubuntu/pm_work/post_osf/candidates_classified.csv","w",newline="") as f:
    fields=list(res[0].keys())
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(res)
from collections import Counter
print(len(res),Counter((r["domain"],r["comparator_signal"]) for r in res))
