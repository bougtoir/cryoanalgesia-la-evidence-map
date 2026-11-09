#!/usr/bin/env python3
"""Gate 4: title-level screening with controlled exclusion reasons."""
import csv,re
rows=list(csv.DictReader(open("/home/ubuntu/pm_work/MASTER_RECORDS.csv")))

CRYO_PAT=re.compile(r"cryo|vapocoolant|ethyl chloride|ice (pack|massage|application)|precool|pre-cool|cold (spray|therapy)|cooling",re.I)
# records must still match a cryo term (all queries had one, but crossref is fuzzy)
NONHUMAN=re.compile(r"\b(rats?|mice|mouse|porcine|swine|piglet|canine|dog\b|feline|cat\b|equine|horse|bovine|ovine|rabbit|zebrafish|drosophila|veterinary|animal model|sprague|wistar|macaque|sheep|goat|guinea pig|hamster)\b",re.I)
WRONG_INTERV=re.compile(r"(tumou?r ablation|tumor cryoablation|cryopreservation|vitrification|cryolipolysis|fat (freezing|reduction)|frostbite|cold injury|cold-water|whole[- ]body cry|cryoglobulin|cryo-?em\b|electron microscopy|cryosurgery of|cryoablation of (hepatic|liver|renal|kidney|lung|prostate|breast|bone|soft[- ]tissue|thyroid|adrenal|cardiac|atrial|ventricular|fibroepithelial|chondroblastoma|osteoblastoma|osteoid|desmoid|plantar fibroma)|cryoablation for (hepatic|renal|lung|prostate|breast|cardiac|ventricular|atrial|desmoid|chondroblastoma|osteoblastoma|osteoid|fibroepithelial)|atrial fibrillation|ventricular tachycardia|arrhythmia|av nodal|accessory pathway|endobronchial cryo|cryoprobe.*(biopsy|lung)|mucositis|oral cryotherapy|cryotherapy for (warts?|verruca|mollusc|actinic|seborrheic|leishman|leiomyom|papilloma|lichen|granuloma|keloid|angioma|retinoblastoma|retinopathy|cervic|hpv|condylom|genital|wart)|wart|verruca|molluscum|actinic keratosis|seborrheic|pyogenic granuloma|cherry angioma|keloid|cryopencil|cryosurgical treatment of|bone tumou?rs?|chondroblastoma|osteoblastoma|osteoid osteoma|desmoid|fibroepithelial|renal tum|prostate canc|breast (lesion|tumo|fibr)|fibroadenoma|liver tum|hepatocell|ovarian (tissue|cyst)|oocyte|sperm|semen|embryo|cryostorage|cryostatic|cryotherapy.*(knee arthroplasty|orthopedic surge|muscle|sport|athlet|recovery|delayed onset|doms|inflammation)|sports? medicine|athletic|exercise recovery|muscle soreness)",re.I)
WRONG_PUBTYPE=re.compile(r"^(editorial|comment|letter to|erratum|correction|reply|news|ecomment)",re.I)
NONCLINICAL=re.compile(r"(crystallography|x-ray|protein structure|enzyme|crystal structure|phantom|in vitro|bench[- ]top|materials science|hydrogel|nanoparticle|gene expression|histolog|cell culture|phylogen|cryopreserv|freeze-dry|lyophil|physics|engineering|simulat|computational model|thermal conduct|cryogenics|spaceflight|cryo-sem|cryo-tem)",re.I)
NO_CLIN_PAIN=re.compile(r"(cosmetic|body contour|apoptosis|mechanism of action only|device validation|bench test|thermal imaging study|temperature measurement only)",re.I)

keep,excl=[],[]
for r in rows:
    t=r["title"] or ""
    if not CRYO_PAT.search(t):
        excl.append((r,"wrong intervention (no cryoanalgesic modality signal)"));continue
    if NONHUMAN.search(t):
        excl.append((r,"nonhuman"));continue
    if WRONG_INTERV.search(t):
        excl.append((r,"wrong intervention (non-analgesic cryo application)"));continue
    if NONCLINICAL.search(t) and not re.search(r"(pain|analges|anesth|block|patient)",t,re.I):
        excl.append((r,"non-clinical / bench research"));continue
    if WRONG_PUBTYPE.search(t):
        excl.append((r,"wrong publication type (title-level)"));continue
    keep.append(r)

with open("/home/ubuntu/pm_work/title_screen.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["record_id","decision","reason"])
    for r in keep:w.writerow([r["record_id"],"advance_to_abstract",""])
    for r,why in excl:w.writerow([r["record_id"],"excluded_title",why])
print("advance",len(keep),"excluded",len(excl))
