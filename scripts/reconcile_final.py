import csv,json,collections,re,os
FIN="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_FINAL/"
REP="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_rebuild_REPAIRED/"
LOCK="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_SUBMISSION_LOCK/"
os.makedirs(LOCK,exist_ok=True)
prim=list(csv.DictReader(open(FIN+"PRIMARY_STUDY_MAP.csv")))
st2={r["record_id"]:r for r in csv.DictReader(open("stage2.csv"))}
DOM_TOKENS={"thoracic_chestwall","dental_oral","vascular_access","orthopedic_msk","chronic_pain_neurolysis","derm_office","periop_other","other_procedural","obstetric_periop"}

# ================= F2: domain / procedure_context reconciliation =================
dom_rows=[]
for r in prim:
    old=r["procedure_context"] or ""
    contra = old in DOM_TOKENS and old!=r["clinical_domain"]
    empty = old==""
    if contra or empty:
        new=r["clinical_domain"]
        action="replaced stale domain-token procedure_context with reconciled clinical_domain" if contra else "filled empty procedure_context with clinical_domain"
    else:
        new=old;action="retained (no contradiction)"
    if contra or empty:
        dom_rows.append({"record_id":r["study_id"],"citation":r["primary_citation"],"clinical_domain":r["clinical_domain"],
            "old_procedure_context":old,"new_procedure_context":new,"contradiction_yes_no":"yes" if contra else "no",
            "action":action,"rationale":"old value was a pre-repair domain label inconsistent with the re-audited clinical_domain" if contra else "empty"})
    r["procedure_context"]=new
with open(LOCK+"DOMAIN_CONTEXT_RECONCILIATION_AUDIT.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(dom_rows[0].keys()));w.writeheader();w.writerows(dom_rows)
print("F2 contradictions fixed:",sum(x["contradiction_yes_no"]=="yes" for x in dom_rows),"filled:",sum(x["contradiction_yes_no"]=="no" for x in dom_rows))

# ================= F3/F4: bidirectional tier/comparator adjudication =================
# (new_tier, comparator_type, LA_yes, LA_type, verified_design, verified_role, rationale)
ADJ={
"R1a58f5705c":("C","none (single-arm observational cohort)","no","NR","prospective observational cohort","diagnostic LA nerve block was eligibility screening, not a comparator arm","single-arm cohort; block used to select candidates — not an analyzable LA contrast","observational cohort study; positive response to diagnostic nerve block required for enrolment"),
"R1f0f3bd730":("B","control group receiving identical care (epidural methadone in both arms)","no","NR","prospective randomized blinded trial","control arm; LA epidural methadone was background care common to both groups","epidural methadone was protocolized for ALL patients — not a randomized contrast","all patients received methadone via lumbar epidural; cryo vs non-cryo control"),
"R1f50ba970e":("B","standard of care without cryo (no blocks, no epidural)","no","NR","retrospective cohort comparison","non-cryo control receiving standard care without LA blocks","control explicitly excluded intercostal/serratus blocks and epidural — LA is not the comparator","control group did not include intercostal or serratus blocks or immediate postoperative epidural"),
"R39233e542d":("B","control group (no ice); spinal anesthesia background in both arms","no","NR","prospective RCT","control arm; spinal anesthesia identical in both groups","LA spinal anesthesia was the common anesthetic technique, not the studied contrast","all patients underwent cesarean under spinal anesthesia; randomized to ice vs control"),
"R554ba757b1":("C","none (single-arm case series)","no","NR","retrospective case series","noncomparative; epidural explicitly not given to any patient","no comparator arm; 'no patients received epidural anesthesia'","retrospective analysis of 21 patients; no patients received epidural anesthesia"),
"R666ef4069d":("A","LA-based technique (local infiltration, direct comparator); also non-LA ShotBlocker arm","yes","local infiltration (LA)","3-arm RCT (vapocoolant vs ShotBlocker vs LA infiltration)","arm","local infiltration arm is a direct LA-based contrast for needle-associated pain","Group C received local infiltration before spinal anaesthesia — a genuine LA-based analgesic arm"),
"R7351a70374":("B","non-treated control group","no","NR","two-group comparative study","non-cryo control arm","control was simply untreated; 'local anesthetic effect' in text describes the ice mechanism, not an LA arm","group I ice vs group II control; no LA comparator"),
"R8b33ccb2a7":("B","placebo spray (cold saline) and untreated arm","no","NR","randomized controlled self-controlled trial","placebo/untreated arms; EMLA cited only as prior pediatric evidence","EMLA was background literature, not a study arm","randomized trial of topical FM vs cold saline placebo"),
"R8cd511412a":("B","adjunct comparison (ESP block + cryo vs cryo + IV analgesia)","no","NR","controlled comparative study (26 vs 10)","adjunct-structure comparison; ESP block tests the added value of a block ON TOP of cryo","comparison isolates the ESP adjunct, not cryo vs LA — both groups received cryoanalgesia","intervention = cryoablation + ESP block; control = cryoablation + IV multimodal analgesia"),
"R8da57dbee1":("C","none (descriptive convenience sample)","no","NR","descriptive physiologic study","noncomparative; nerve block presence differed descriptively only","descriptive temperature data; block vs no-block not a powered treatment contrast","convenience sample; data presented, not statistically analyzed"),
"R9326d5e533":("C","none (case series)","no","NR","prospective case series","diagnostic LA blocks were candidacy screening, not a comparator","noncomparative; LA blocks used to determine appropriateness for treatment","eight patients; all first underwent diagnostic nerve blocks with LA"),
"R9ab39ed3f5":("B","conventional pain management (IV-PCA or thoracic epidural; composition not analyzable)","no","NR","randomized single-blind trial","conventional-care arm; epidural mentioned as one of several conventional options — not a clean LA-only contrast","group N received 'conventional pain management' mixing IV-PCA and epidural options — not an interpretable direct LA contrast","randomly assigned to cryoanalgesia (n=24) or noncryoanalgesia conventional management (n=24)"),
"Ra257d1434b":("B","within-patient adjunct comparison (precool+topical lidocaine vs topical lidocaine alone)","no","NR","split-mouth interventional study","adjunct comparison; topical lidocaine applied identically to both sides","LA is constant across arms; the contrast is precooling vs none — adjunct, not LA substitution","one side precooled with ice plus topical lidocaine; other side topical lidocaine only"),
"Rc1eb87e894":("C","none (3-case report)","no","NR","case series","noncomparative","3-case descriptive report","report of 3 cases of ultrasound-guided percutaneous cryoneurolysis"),
"Rc68d3b9d41":("C","none (single-arm retrospective review)","no","NR","retrospective chart review","noncomparative; epidural/PCA patients were EXCLUDED","patients receiving epidural or PCA excluded by design — no comparator","patients receiving epidural analgesia or patient-controlled analgesia were excluded"),
"Rcff0974212":("A","LA-based technique (Ametop/tetracaine topical anesthetic, direct comparator) plus no-analgesia arm","yes","topical LA (tetracaine gel, Ametop)","3-group comparative study (EC vs Ametop vs none)","arm","Ametop topical anesthetic arm is a direct LA-based contrast","venipuncture performed with no analgesia (NO), ethyl chloride (EC), or topical anesthetic Ametop (TA)"),
"Rf5f2fc211f":("B","placebo spray","no","NR","randomized double-blind placebo-controlled trial","placebo arm","comparator was placebo spray, not LA","vapocoolant spray (n=38) or placebo spray (n=34)"),
"Rf709115dfc":("A","LA-based technique (benzocaine gel, direct comparator)","yes","topical LA (benzocaine gel)","split-mouth comparative study","arm","benzocaine gel control side is a direct topical-LA contrast for needle pain","benzocaine gel applied on control side; refrigerated cartridge on experimental side"),
"Rf7d6b6db92":("C","none (retrospective case series)","no","NR","retrospective case series","noncomparative; successful intercostal LA block was eligibility criterion","retrospective review of cryoanalgesia after successful intercostal blockade — block is screening, not comparator","patients who received percutaneous cryoanalgesia following successful intercostal nerve blockade"),
# X2: Tier A records whose stale comparator fields disagreed
"R074af0228d":("A","LA-based technique (thoracic epidural analgesia, historical cohort comparator)","yes","epidural analgesia (thoracic epidural, historical cohort)","retrospective cohort vs prior TE cohort","historical comparator arm","explicit comparison of Cryo cohort vs previous 62-patient thoracic epidural cohort — analyzable LA contrast","compared Cryo cohort with previous cohort of 62 patients who underwent TE and MIRPE"),
"R0eebc3be03":("B","placebo spray","no","NR","randomized placebo-controlled trial","placebo arm","comparator was water-spray placebo; 'ideal local anesthesia' phrasing is aspirational, not an arm","group A vapocoolant vs group B water spray placebo"),
"R1f08988e8f":("A","LA-based technique (10% lignocaine spray, direct comparator)","yes","topical LA (lignocaine spray 10%)","comparative study","arm","title-level direct comparison of lignocaine spray vs ice-bag cryoanalgesia","compare the effectiveness of 10% lignocaine spray and cryoanalgesia (ice bag)"),
"R55b8b51789":("B","control (no cold spray); local anesthesia identical in both arms","no","NR","RCT","adjunct comparison; LA given to all — contrast is cold spray adjunct vs none","LA was standard care in both groups; studied contrast is the added cold spray","cold spray applied before local anesthesia vs control; both received LA"),
"R603908c76f":("B","control (no precooling); LA administration common to all","no","NR","RCT 3-arm","adjunct comparison; LA is the procedure in all arms","contrast is popsicle precooling vs none during LA administration — LA is constant","control no precooling vs popsicle precooling groups during LA administration"),
"R7630e97b84":("B","placebo spray","no","NR","self-controlled RCT","placebo arm","vapocoolant vs placebo before the LA injection — LA injection is the stimulus, not a comparator","vapocoolant or placebo prior to initial intradermal anaesthetic injection"),
"R8a3b574d2b":("B","topical anesthesia alone (adjunct comparison)","no","NR","RCT","adjunct comparison; topical anesthesia common base in both arms","contrast is cryotherapy adjunct vs no adjunct; topical LA present identically in both groups","topical anesthesia with cryotherapy vs topical anesthesia alone"),
"R939be6a7b8":("B","sham treatment","no","NR","prospective randomized blinded trial","sham arm","comparator was sham cryo; herniorrhaphy under LA is background","cryoanalgesia vs sham treatment after mesh repair under local anesthesia"),
"Ra91051123f":("B","placebo spray","no","NR","single-blind randomized placebo-controlled trial","placebo arm","comparator was placebo spray","ethyl chloride spray vs placebo spray before arterial puncture"),
"Rc65340598e":("B","cohort comparison (diagnostic block vs no block)","no","NR","retrospective cohort comparison","predictive-workflow comparison; the block is a diagnostic step, not a therapeutic LA comparator","compares outcomes by whether a pre-cryoneurolysis diagnostic block was performed","patients categorized by whether a pre-cryoneurolysis diagnostic block was performed"),
"Rcd6cbea867":("A","LA-based technique (topical anesthesia, direct comparator)","yes","topical LA (ophthalmic topical anesthesia)","randomized comparative study","arm","randomized cryoanalgesia vs topical anesthesia for phacoemulsification","82 patients randomized to phacoemulsification under cryoanalgesia or topical anesthesia"),
"Rcd77c831af":("B","honey and no-treatment control arms","no","NR","RCT 3-arm","non-LA comparator arms","comparators were honey and untreated control — no LA arm","ethyl chloride vs honey vs control for dental injection pain"),
"Redfdf5062f":("B","TENS and conventional-method arms","no","NR","RCT 3-arm","non-LA comparator arms","comparators were TENS and conventional method — no LA arm","TENS vs vibrational precooling vs conventional method during LA administration"),
}
tier_rows=[]
changed=0
for r in prim:
    sid=r["study_id"]
    if sid in ADJ:
        nt,ct,ly,lt,vd,vr,rat,src=ADJ[sid]
        ch = (nt!=r["evidence_tier"]) or (ct!=r["comparator_type"]) or (ly!=r["LA_comparator_yes_no"]) or (lt!=r["LA_type"])
        if ch:changed+=1
        tier_rows.append({"record_id":sid,"citation":r["primary_citation"],"current_tier":r["evidence_tier"],
            "old_comparator_type":r["comparator_type"],"old_LA_comparator_yes_no":r["LA_comparator_yes_no"],"old_LA_type":r["LA_type"],
            "verified_design":vd,"verified_comparator_role":vr,"true_direct_LA_comparator_yes_no":ly,
            "new_tier":nt,"new_comparator_type":ct,"new_LA_comparator_yes_no":ly,"new_LA_type":lt,
            "rationale":rat,"source_text":src,"changed_yes_no":"yes" if ch else "no"})
        r["evidence_tier"]=nt;r["comparator_type"]=ct;r["LA_comparator_yes_no"]=ly;r["LA_type"]=lt
# assertion: no remaining unexplained flag combos after adjudication
for r in prim:
    if r["evidence_tier"]=="A":
        assert r["LA_comparator_yes_no"]=="yes",r["study_id"]
        assert "LA" in r["comparator_type"],r["study_id"]
    else:
        assert not (r["LA_comparator_yes_no"]=="yes" and "direct" in r["comparator_type"]),r["study_id"]
with open(LOCK+"TIER_COMPARATOR_RECONCILIATION_AUDIT.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(tier_rows[0].keys()));w.writeheader();w.writerows(tier_rows)
print("F3 flagged rows:",len(tier_rows),"changed:",changed)

# ================= pubtype escapees found by reconciled T1/T19 tests =================
# R2703fc3a9f: self-declared "This narrative review summarizes..." -> belongs to SYNTHESIS_REPORTS
# Rd82babbea1: "design of a prospective ... randomized controlled trial" design publication, no results -> PROTOCOLS_ONGOING
move_synth=[r for r in prim if r["study_id"]=="R2703fc3a9f"]
move_proto=[r for r in prim if r["study_id"]=="Rd82babbea1"]
prim=[r for r in prim if r["study_id"] not in {"R2703fc3a9f","Rd82babbea1"}]
synths=list(csv.DictReader(open(FIN+"SYNTHESIS_REPORTS.csv")))
protos=list(csv.DictReader(open(FIN+"PROTOCOLS_ONGOING.csv")))
for r in move_synth:
    synths.append({"record_id":r["study_id"],"title":r["title"],"authors":r["primary_citation"],"year":r["year"],"journal":r["journal"],"pubtype_tag":"narrative review (caught by reconciled T1)","domain":r["clinical_domain"],"comparator_signal":"","doi":r["doi"],"pmid":r["pmid"]})
for r in move_proto:
    protos.append({"record_id":r["study_id"],"nct":"","title":r["title"],"authors":r["primary_citation"],"year":r["year"],"journal":r["journal"],"pubtype_tag":"trial design publication (no results; caught at reconciliation)","domain":r["clinical_domain"],"comparator_signal":"","doi":r["doi"],"pmid":r["pmid"],"status":"design publication","enrollment":"NR"})
with open(LOCK+"SYNTHESIS_REPORTS.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(synths[0].keys()));w.writeheader();w.writerows(synths)
with open(LOCK+"PROTOCOLS_ONGOING.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(protos[0].keys()));w.writeheader();w.writerows(protos)
print("moved to synth:",len(move_synth),"to proto:",len(move_proto))

# write reconciled PRIMARY_STUDY_MAP
with open(LOCK+"PRIMARY_STUDY_MAP.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(prim[0].keys()));w.writeheader();w.writerows(prim)

# ================= F5: rebuild TIER_A_COMPLETE =================
ta=[r for r in prim if r["evidence_tier"]=="A" and r["cohort_id"]==r["study_id"]]
oldt={r["study_id"]:r for r in csv.DictReader(open(FIN+"TIER_A_COMPLETE.csv"))}
tafields=list(oldt[next(iter(oldt))].keys())
with open(LOCK+"TIER_A_COMPLETE.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=tafields);w.writeheader()
    for r in ta:
        o=oldt.get(r["study_id"],{})
        row=dict(o) if o else {k:"NR" for k in tafields}
        row["study_id"]=r["study_id"];row["citation"]=r["primary_citation"]
        row["clinical_domain"]=r["clinical_domain"];row["design"]=r["study_design"]
        row["exact_LA_comparator"]=r["LA_type"]
        row["title"]=r["title"];row["doi"]=r["doi"];row["pmid"]=r["pmid"];row["journal"]=r["journal"]
        w.writerow(row)
for r in ta:
    assert r["LA_comparator_yes_no"]=="yes"
print("Tier A rows:",len(ta))

# ================= F7: reconciled counts =================
coh=[r for r in prim if r["cohort_id"]==r["study_id"]]
tc=collections.Counter(r["evidence_tier"] for r in coh)
dom=collections.Counter(r["clinical_domain"] for r in prim)
sec=json.load(open("clin_pass1.json"))["sec"]
new={"records_identified_total":43969,"records_pubmed":9532,"records_central":622,"records_scopus":33453,"records_ctgov":362,"records_after_dedup":23502,"title_screened":23502,"title_excluded":19143,"abstract_assessed":4359,"abstract_excluded":3128,"eligibility_assessed":1231,"eligibility_excluded":1231-len(prim)-len(synths)-len(protos),"primary_study_reports":len(prim),"unique_cohorts":len(coh),"tier_A":tc["A"],"tier_B":tc["B"],"tier_C":tc["C"],"synthesis_reports":len(synths),"protocols_ongoing":len(protos),"randomized_primary":sum(r["study_design"]=="RCT" for r in prim),"cohort_observational_primary":sum(r["study_design"]=="cohort/observational" for r in prim),"linked_secondary_reports":len(sec),"sensory_testing_excluded":3,"non_analgesic_cryoablation_excluded":2,"non_patient_or_consensus_excluded":2,"clinical_domain_counts":dict(dom),"language_policy":"English full text only (registered policy)","search_date":"2026-11-09","osf_doi":"10.17605/OSF.IO/KJ5RS","notes":"SUBMISSION_LOCK reconciliation: 2 publication-type escapees moved (narrative review R2703fc3a9f -> synthesis; trial-design publication Rd82babbea1 -> protocols); bidirectional tier/comparator adjudication of 32 flagged records (3 promoted to A [Soueid Ametop, refrigerated-cartridge vs benzocaine, ShotBlocker LA-infiltration arm]; 11 demoted A->B [placebo/sham/adjunct/non-LA comparators]; 1 B->C; 1 C->B); procedure_context reconciled to clinical_domain (135 stale domain-token values); search-stage counts frozen."}
assert new["eligibility_assessed"]==new["eligibility_excluded"]+new["primary_study_reports"]+new["synthesis_reports"]+new["protocols_ongoing"]
assert new["unique_cohorts"]==new["primary_study_reports"]-new["linked_secondary_reports"]==tc["A"]+tc["B"]+tc["C"]
json.dump(new,open(LOCK+"CANONICAL_COUNTS_FINAL_RECONCILED.json","w"),indent=1)
with open(LOCK+"CANONICAL_COUNTS_FINAL_RECONCILED.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["metric","value"]);[w.writerow([k,json.dumps(v) if isinstance(v,dict) else v]) for k,v in new.items()]
rows=[("records identified from databases",43969),("MEDLINE via PubMed",9532),("CENTRAL",622),("Scopus",33453),("ClinicalTrials.gov",362),("duplicate records removed",43969-23502),("records screened (title)",23502),("records excluded at title",19143),("reports assessed at abstract/metadata",4359),("reports excluded at abstract",3128),("reports assessed for eligibility",1231),("reports excluded at eligibility",new["eligibility_excluded"]),("primary study reports included",len(prim)),("unique cohorts",len(coh)),("linked secondary reports",len(sec)),("Tier A (direct LA comparator)",tc["A"]),("Tier B (indirect comparator)",tc["B"]),("Tier C (noncomparative)",tc["C"]),("synthesis reports",len(synths)),("protocols/ongoing",len(protos))]
with open(LOCK+"PRISMA_FLOW_DATA_FINAL_RECONCILED.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["quantity","n"]);w.writerows(rows)
print(json.dumps({k:new[k] for k in ["eligibility_excluded","primary_study_reports","unique_cohorts","tier_A","tier_B","tier_C","randomized_primary","clinical_domain_counts"]},indent=1))
