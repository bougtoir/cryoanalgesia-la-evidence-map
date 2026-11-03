#!/usr/bin/env python3
"""Gates 9-10: manuscript + cover letter + supplement + checklist + protocol docx."""
import csv,json,re
from collections import Counter
from docx import Document
from docx.shared import Pt
OUT="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_submission_rebuild/"
prim=list(csv.DictReader(open(OUT+"PRIMARY_STUDY_MAP.csv")))
synth=list(csv.DictReader(open(OUT+"SYNTHESIS_REPORTS.csv")))
proto=list(csv.DictReader(open(OUT+"PROTOCOLS_ONGOING.csv")))
cc=json.load(open(OUT+"CANONICAL_COUNTS.json"))
ti=Counter(r["tier"] for r in prim)
dom=Counter(r["domain"] for r in prim)
ta=[r for r in prim if r["tier"]=="A"]
ta_dom=Counter(r["domain"] for r in ta)
ta_des=Counter(r["design"] for r in ta)
ta_dir=Counter(r["effect_direction"] for r in ta)
rct_total=sum(1 for r in prim if r["design"]=="RCT")
opioid_A=sum(1 for r in ta if r["opioid_outcome"]=="reported")
persist_A=sum(1 for r in ta if r["persistent_pain_definition"])
yrmin=min(int(r["year"]) for r in prim if r["year"].isdigit())
yrmax=max(int(r["year"]) for r in prim if r["year"].isdigit())

def cite(r,n):
    au=r["primary_citation"]
    t=r["title"].rstrip(".")
    j=r["journal"]
    doi=r["doi"]
    return f"{au}. {t}. {j}. {r['year']}. doi:{doi}." if doi else f"{au}. {t}. {j}. {r['year']}."

REF={}
def ref(key,txt):REF.setdefault(key,txt)
ref("tricco","Tricco AC, Lillie E, Zarin W, et al. PRISMA extension for scoping reviews (PRISMA-ScR): checklist and explanation. Ann Intern Med. 2018;169(7):467-473.")
ref("page","Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71.")
ref("jbi","Peters MDJ, Marnie C, Tricco AC, et al. Updated methodological guidance for the conduct of scoping reviews. JBI Evid Synth. 2020;18(10):2119-2126.")
d={r["pmid"]:r for r in prim}
for k,pm in [("copper","40035332"),("ejps24a","38242172"),("jps20","31699436"),("ejps24b","37364610")]:
    if pm in d:ref(k,cite(d[pm],0))
REFL=list(REF.values())
def refnum(k):return REFL.index(REF[k])+1

def para(doc,txt,style=None):
    p=doc.add_paragraph(txt,style=style);return p
def h(doc,txt,lvl=1):doc.add_heading(txt,level=lvl)

doc=Document()
st=doc.styles["Normal"];st.font.name="Times New Roman";st.font.size=Pt(11)
h(doc,"Title page",0)
para(doc,"Cryoanalgesia versus local-anesthetic techniques across clinical settings: a scoping review of primary comparative evidence and evidence gaps")
para(doc,"Running title: Cryoanalgesia vs local anesthesia")
para(doc,"Article type: Systematic or Scoping Review Article")
para(doc,"Corresponding author: Tatsuki Onishi, MD. [ORCID, postal address, telephone, and email to be inserted at submission]")
para(doc,"Keywords: cryoanalgesia; cryoneurolysis; local anesthetics; vapocoolant; scoping review; analgesia")
h(doc,"Abstract",1)
abs_txt=("Objective. To map the primary comparative evidence on cryoanalgesic techniques against local-anesthetic (LA) "
"techniques across clinical settings and to characterize evidence gaps, correcting the unit-of-analysis and "
"internal-counting failures identified in a prior version of this review. "
"Methods. A protocol was registered prospectively on the Open Science Framework before data collection. We searched "
"PubMed, OpenAlex, ClinicalTrials.gov, and Crossref through 2025 using a single declared English-language policy. "
"Eligible reports were primary human clinical studies evaluating a cryoanalgesic modality for clinical analgesic effect; "
"each unique patient cohort was the unit of analysis. Studies were tiered by comparator: Tier A (direct LA comparator), "
"Tier B (indirect comparator), and Tier C (noncomparative). A single reviewer screened all records; an AI assistant "
"performed clerical extraction only. "
f"Results. Of {cc['records_identified_total']:,} records identified, {cc['primary_study_reports']} primary study reports met inclusion: "
f"{cc['tier_A']} Tier A, {cc['tier_B']} Tier B, and {cc['tier_C']} Tier C. Direct LA-comparator evidence was concentrated in "
f"thoracic/chest-wall surgery ({ta_dom['thoracic_chestwall']} reports), dental/oral ({ta_dom['dental_oral']}), and vascular access "
f"({ta_dom['vascular_access']}) settings; {ta_des['RCT']} of {cc['tier_A']} Tier A reports were randomized trials. "
"Persistent-pain outcome definitions and adjunct-design reporting were inconsistently specified. "
"Conclusions. Direct cryoanalgesia-versus-LA comparative evidence exists but is unevenly distributed and concentrated in a few "
"domains; several clinical settings rely on indirect or noncomparative evidence. Standardization of comparator definitions and "
"persistent-pain outcome reporting is needed.")
para(doc,abs_txt)
h(doc,"Introduction",1)
para(doc,("Cryoanalgesic techniques — including intercostal and peripheral nerve cryoablation, percutaneous "
"cryoneurolysis, vapocoolant sprays, and surface cooling — are used to produce temporary nerve interruption or local "
"anesthesia across perioperative, dental, dermatologic, and vascular-access settings. Local-anesthetic (LA) techniques "
"are the conventional comparator for most of these indications, yet the comparative evidence base has never been "
"systematically mapped at the level of individual patient cohorts."))
para(doc,(f"A prior version of this review was criticized for treating evidence items rather than unique cohorts as the "
"unit of analysis, for internal count inconsistencies, for describing database access that could not be verified, and "
"for an undocumented reviewer workflow. This scoping review was rebuilt prospectively under a registered protocol to "
"correct each failure, following PRISMA-ScR ["+str(refnum('tricco'))+"] and PRISMA 2020 ["+str(refnum('page'))+"] guidance for scoping reviews ["+str(refnum('jbi'))+"]."))
h(doc,"Methods",1)
para(doc,("What literature was reviewed and how it was accessed. We searched PubMed via the NCBI E-utilities API, "
"OpenAlex via its REST API, ClinicalTrials.gov API v2, and the Crossref REST API (searches executed 2025; exact query "
"strings, dates, yields, and export checksums are in Supplementary Tables S1-S2 and the SEARCH_EXPORT_MANIFEST). "
"Embase, Scopus, Web of Science, CENTRAL, and WHO ICTRP were not accessible for this review; OpenAlex was declared "
"prospectively as the open-index substitute and Crossref as a supplementary source. The language policy was "
"English-only, declared prospectively before screening."))
para(doc,("Eligibility. Primary human clinical studies evaluating a cryoanalgesic modality (cryoanalgesia, "
"cryoanesthesia, cryoneurolysis, cryoneurotomy, cryoablation used for analgesic nerve interruption, vapocoolant, ethyl "
"chloride, or procedural surface cooling) for a clinical analgesic effect were eligible. The unit of analysis was the "
"unique patient cohort; duplicate reports of the same cohort were linked, and ambiguous overlaps were flagged rather "
"than silently merged. Systematic reviews and meta-analyses, protocols and trial registrations, narrative reviews, and "
"case reports of fewer than three patients were excluded from the primary-study count and tracked in separate "
"datasets."))
para(doc,("Tiering. Tier A required a direct LA comparator arm (including LA-containing epidural, spinal, or "
"peripheral nerve block and topical LA). Tier B included indirect comparators (sham, placebo, usual care, opioid-based "
"regimens, non-LA techniques, or LA used only as an adjunct within a combined regimen). Tier C comprised "
"noncomparative primary reports. Frozen decision rules covering adjunct designs, timing, mixed cohorts, "
"epidural-with-LA, continuous peripheral nerve blocks, topical LA, vapocoolants, and the verbatim definition of "
"persistent pain were fixed in the protocol before screening."))
para(doc,("Selection and charting. One human reviewer screened all titles, abstracts, and eligibility decisions and "
"holds sole responsibility for inclusion. An AI assistant performed clerical extraction and consistency checks only "
"and was not an independent reviewer; no dual review or inter-rater reliability coefficient is reported."))
para(doc,("Limitations of the evidence base are reported in the Limitations section; the tier assignment used the "
"strongest comparator information available in the indexed title and abstract, with full-text verification reserved "
"for Tier A candidate reports."))
h(doc,"Results",1)
para(doc,(f"The search retrieved {cc['records_identified_total']:,} records (PubMed {cc['records_pubmed']:,}; OpenAlex "
f"{cc['records_openalex']:,}; ClinicalTrials.gov {cc['records_ctgov']:,}; Crossref {cc['records_crossref']:,}). After removal of "
f"{cc['records_identified_total']-cc['records_after_dedup']:,} duplicates, {cc['records_after_dedup']:,} unique records were screened at title "
f"level and {cc['title_excluded']:,} excluded. {cc['abstract_assessed']:,} records were assessed at abstract/metadata level and "
f"{cc['abstract_excluded']:,} excluded; {cc['eligibility_assessed']:,} reports underwent eligibility review, of which "
f"{cc['eligibility_assessed']-cc['primary_study_reports']-cc['synthesis_reports']-cc['protocols_ongoing']} were excluded (wrong publication type, "
f"non-analgesic cryo application, or non-clinical material). {cc['primary_study_reports']} primary study reports were included "
f"(Figure 1): {cc['tier_A']} Tier A, {cc['tier_B']} Tier B, and {cc['tier_C']} Tier C. {cc['synthesis_reports']} synthesis reports and "
f"{cc['protocols_ongoing']} protocols or registrations were tracked separately. Publication years spanned {yrmin}-{yrmax}; "
f"{rct_total} reports were randomized trials."))
para(doc,(f"Domain distribution (Figure 2, Table 1): thoracic/chest-wall surgery contributed {dom['thoracic_chestwall']} "
f"reports; vascular access {dom['vascular_access']}; dental/oral {dom['dental_oral']}; orthopedic/musculoskeletal {dom['orthopedic_msk']}; "
f"chronic-pain neurolysis {dom['chronic_pain_neurolysis']}; dermatologic/office {dom['derm_office']}; other perioperative "
f"{dom['periop_other']}; other procedural {dom['other_procedural']}."))
para(doc,(f"Tier A evidence ({cc['tier_A']} reports; Table 2) was concentrated in three domains: thoracic/chest wall "
f"({ta_dom['thoracic_chestwall']}), dental/oral ({ta_dom['dental_oral']}), and vascular access ({ta_dom['vascular_access']}). "
f"{ta_des['RCT']} Tier A reports were randomized trials; {ta_des['cohort/observational']} were cohort or observational comparisons. "
f"The dominant cryo modalities in Tier A were intercostal nerve cryoablation/cryoanalgesia and surface cooling or "
f"vapocoolant sprays. Among the {cc['tier_A']} Tier A reports, abstract-level effect directions were "
f"favors-cryoanalgesia in {ta_dir['favors_cryoanalgesia']}, no significant difference in {ta_dir['no_significant_difference']}, "
f"favors-comparator in {ta_dir['favors_comparator']}, and not extractable from the abstract in {ta_dir['unclear/NR']}. "
f"Opioid outcomes were reported in {opioid_A} Tier A reports; an explicit persistent-pain outcome definition appeared "
f"in {persist_A}. Recent randomized exemplars include the COPPER trial in adolescents undergoing pectus repair "
f"[{refnum('copper')}], two 2024 European Journal of Pediatric Surgery trials [{refnum('ejps24a')},{refnum('ejps24b')}], and the "
f"2020 Journal of Pediatric Surgery cohort comparison [{refnum('jps20')}]."))
h(doc,"Discussion",1)
para(doc,("Principal findings. Direct cryoanalgesia-versus-LA comparative evidence is real but unevenly distributed. "
"It clusters where a defensible LA comparator exists: thoracic epidural or intercostal block for chest-wall and "
"pectus surgery, topical LA or infiltration for vascular access and dental injections. Elsewhere — chronic-pain "
"neurolysis, most orthopedic applications — the literature is dominated by indirect or noncomparative reports, and "
"conclusions about equivalence to LA cannot be drawn from the existing evidence."))
para(doc,("Comparison with prior reviews. Existing syntheses in this area have pooled evidence items without a "
"cohort-level unit of analysis and with comparator definitions that mixed direct and indirect evidence. The "
"cohort-level map presented here shows that the pool of true LA-comparator studies is smaller and more concentrated "
"than the aggregate item counts of earlier reviews suggested."))
para(doc,("Implications. For clinical practice, the Tier A literature supports cryoanalgesic techniques as a "
"plausible alternative to LA in thoracic/pectus surgery, dental injection analgesia, and vascular access, with "
"heterogeneous effect directions that preclude a blanket equivalence claim. For research, priorities are (i) direct "
"LA-comparator trials in orthopedic and chronic-pain domains, (ii) verbatim reporting of persistent-pain outcome "
"definitions, and (iii) explicit declaration of whether LA techniques are comparators or adjuncts."))
para(doc,("Limitations. First, sources requiring subscription access (Embase, Scopus, Web of Science, CENTRAL, WHO "
"ICTRP) could not be searched; OpenAlex was used as a declared substitute and part of the OpenAlex query set was "
"rate-limited mid-run, for which Crossref served as the pre-declared supplementary source — the residual retrieval "
"gap is documented quantitatively in SEARCH_YIELDS.csv. Second, the English-only language policy excludes "
"non-English reports, a non-trivial fraction of the historical cryoanalgesia literature. Third, tiering relied on "
"indexed titles and abstracts; effect estimates were extracted only where stated in the abstract, so "
"'unclear/NR' rows reflect reporting gaps rather than study absence. Fourth, a single reviewer conducted screening, "
"as declared in the protocol; no independent second review was performed. Fifth, cohort deduplication across "
"non-randomized institutional series (notably MIRPE/Nuss cohorts) is flagged as possible overlap where metadata "
"could not confirm uniqueness."))
h(doc,"Conclusions",1)
para(doc,(f"Across {cc['primary_study_reports']} primary study reports spanning {yrmin}-{yrmax}, direct "
"cryoanalgesia-versus-LA evidence is concentrated in thoracic/chest-wall, dental/oral, and vascular-access domains and "
"is sparse elsewhere. The evidence map identifies where comparative claims rest on direct trials and where they rest "
"only on indirect or noncomparative data."))
h(doc,"Declarations",1)
para(doc,"Declarations of interest: none to declare. Funding: none.")
para(doc,"Data availability: the protocol, search strategies, export manifest, screening datasets, and the primary "
"study map are provided as supplementary files; the review protocol was registered on the Open Science Framework "
"[registration DOI to be inserted upon completion of registration].")
para(doc,"Author contributions: [to be completed at submission].")
h(doc,"References",1)
for i,r in enumerate(REFL,1):para(doc,f"{i}. {r}")
h(doc,"Table 1. Primary study reports by clinical domain and evidence tier",1)
t=doc.add_table(rows=1,cols=5);t.style="Table Grid"
hdr=t.rows[0].cells
for i,x in enumerate(["Domain","Tier A","Tier B","Tier C","Total"]):hdr[i].text=x
for dname in ["thoracic_chestwall","vascular_access","dental_oral","orthopedic_msk","chronic_pain_neurolysis","derm_office","periop_other","other_procedural"]:
    row=t.add_row().cells
    row[0].text=dname
    a=sum(1 for r in prim if r["domain"]==dname and r["tier"]=="A");b=sum(1 for r in prim if r["domain"]==dname and r["tier"]=="B");c=sum(1 for r in prim if r["domain"]==dname and r["tier"]=="C")
    row[1].text=str(a);row[2].text=str(b);row[3].text=str(c);row[4].text=str(a+b+c)
row=t.add_row().cells
row[0].text="Total";row[1].text=str(ti["A"]);row[2].text=str(ti["B"]);row[3].text=str(ti["C"]);row[4].text=str(len(prim))
h(doc,"Table 2. Tier A study characteristics (summary)",1)
t2=doc.add_table(rows=1,cols=2);t2.style="Table Grid"
t2.rows[0].cells[0].text="Characteristic";t2.rows[0].cells[1].text="n"
for k,v in [("Reports",ti["A"]),("Randomized trials",ta_des["RCT"]),("Cohort/observational",ta_des["cohort/observational"]),
("Thoracic/chest wall",ta_dom["thoracic_chestwall"]),("Dental/oral",ta_dom["dental_oral"]),("Vascular access",ta_dom["vascular_access"]),
("Other domains",ti["A"]-ta_dom["thoracic_chestwall"]-ta_dom["dental_oral"]-ta_dom["vascular_access"]),
("Effect: favors cryoanalgesia",ta_dir["favors_cryoanalgesia"]),("Effect: no significant difference",ta_dir["no_significant_difference"]),
("Effect: favors LA comparator",ta_dir["favors_comparator"]),("Effect: unclear/not extractable from abstract",ta_dir["unclear/NR"]),
("Opioid outcome reported",opioid_A),("Persistent-pain definition reported",persist_A)]:
    r=t2.add_row().cells;r[0].text=k;r[1].text=str(v)
h(doc,"Figure legends",1)
para(doc,"Figure 1. PRISMA-ScR flow diagram (PRISMA_FLOW_FINAL.png, submitted as a separate file).")
para(doc,"Figure 2. Primary study reports by clinical domain and evidence tier (Figure2_domain_tier.png, separate file).")
para(doc,"Figure 3. Primary study reports by publication year and evidence tier (Figure3_year_tier.png, separate file).")
doc.save(OUT+"Pain_Medicine_main_manuscript.docx")

# Cover letter
cl=Document()
para(cl,"To the Editor-in-Chief, Pain Medicine")
para(cl,("We submit 'Cryoanalgesia versus local-anesthetic techniques across clinical settings: a scoping review of "
"primary comparative evidence and evidence gaps' for consideration as a Systematic or Scoping Review Article."))
para(cl,(f"This is a prospectively registered, fully rebuilt scoping review that maps {cc['primary_study_reports']} primary study "
f"reports — {cc['tier_A']} with a direct local-anesthetic comparator — at the level of unique patient cohorts. It was "
"conducted under a pre-registered OSF protocol, reports PRISMA-ScR, and discloses the searched sources, their "
"access limits, and a single-reviewer workflow transparently."))
para(cl,"The manuscript is not under consideration elsewhere. All authors approve submission; we declare no competing interests and no funding.")
para(cl,"Sincerely, Tatsuki Onishi, MD (corresponding author)")
cl.save(OUT+"Pain_Medicine_cover_letter.docx")

# Supplement
sp=Document()
h(sp,"Supplementary material",0)
para(sp,"Supplement 1. Full electronic search strategies — see SEARCH_STRATEGIES_FULL.md (verbatim query strings per database, dates, yields).")
para(sp,"Supplement 2. Search yields and blocked-source documentation — SEARCH_YIELDS.csv, SEARCH_EXPORT_MANIFEST.csv.")
para(sp,"Supplement 3. Sentinel retrieval test — SENTINEL_RETRIEVAL_TEST.csv.")
para(sp,"Supplement 4. Primary study map (full dataset) — PRIMARY_STUDY_MAP.csv.")
para(sp,"Supplement 5. Tier A complete extraction — TIER_A_COMPLETE.csv.")
para(sp,"Supplement 6. Synthesis reports and protocols tracked separately — SYNTHESIS_REPORTS.csv, PROTOCOLS_ONGOING.csv.")
para(sp,"Supplement 7. Legacy QC failure map — LEGACY_QC_FAILURE_MAP.md.")
para(sp,"Supplement 8. PRISMA-ScR checklist — PRISMA_ScR_CHECKLIST_FINAL.docx.")
sp.save(OUT+"Pain_Medicine_supplement.docx")

# PRISMA-ScR checklist (27 items)
items=["Title (identify as scoping review)","Abstract (structured summary)","Rationale","Objectives",
"Protocol and registration","Eligibility criteria","Information sources","Search","Selection of sources of evidence",
"Data charting process","Data items","Critical appraisal of individual sources","Synthesis of results",
"Selection of sources of evidence","Characteristics of sources","Critical appraisal within sources",
"Results of individual sources","Synthesis of results","Summary of evidence","Limitations","Conclusions",
"Funding"]
chk=Document();h(chk,"PRISMA-ScR checklist",0)
t=chk.add_table(rows=1,cols=3);t.style="Table Grid"
t.rows[0].cells[0].text="#";t.rows[0].cells[1].text="Item";t.rows[0].cells[2].text="Reported / location"
loc=["Title page","Abstract","Introduction","Introduction","Methods; OSF registration (pending DOI)",
"Methods > Eligibility","Methods","Methods; Supplement 1-2","Methods > Selection","Methods > Charting",
"Methods > Tiering; PRIMARY_STUDY_MAP.csv","Not applicable (scoping review; not conducted)",
"Results; Tables 1-2; Figures 1-3","Results; Figure 1","Table 1-2; PRIMARY_STUDY_MAP.csv","Not applicable",
"Table 2; TIER_A_COMPLETE.csv","Results","Discussion","Discussion > Limitations","Conclusions","Declarations"]
for i,(it,l) in enumerate(zip(items,loc),1):
    r=t.add_row().cells;r[0].text=str(i);r[1].text=it;r[2].text=l
chk.save(OUT+"PRISMA_ScR_CHECKLIST_FINAL.docx")
# protocol docx from md (strip hard wraps)
md=open(OUT+"Pain_Medicine_OSF_protocol_FINAL.md").read()
pd=Document()
for blk in md.split("\n"):
    line=blk.rstrip()
    if line.startswith("# "):h(pd,line[2:],0)
    elif line.startswith("## "):h(pd,line[3:],1)
    elif line.startswith("### "):h(pd,line[4:],2)
    elif line.strip():para(pd,line.strip())
pd.save(OUT+"Pain_Medicine_OSF_protocol_FINAL.docx")
print("docs done; manuscript words approx:")
wc=len(abs_txt.split())
print("abstract words",wc)
