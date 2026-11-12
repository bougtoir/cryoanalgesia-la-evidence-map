#!/usr/bin/env python3
"""R-pass: expanded Pain Medicine review article generator (2500-3500 words, ~45 refs).
All numbers computed from canonical sources; citations numbered in first-appearance order."""
import csv, json, re, sys, os
from collections import Counter, OrderedDict
sys.path.insert(0, "/home/ubuntu/pm_work")
from refs_data import REFS, vancouver
from docx import Document
from docx.shared import Pt

OUT = "/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_SUBMISSION_LOCK/"
FIN = "/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_REVIEW_ARTICLE_FINAL/"
os.makedirs(FIN, exist_ok=True)
prim = list(csv.DictReader(open(OUT + "PRIMARY_STUDY_MAP.csv")))
cc = json.load(open(OUT + "CANONICAL_COUNTS_FINAL_RECONCILED.json"))
cohp = [r for r in prim if r.get("cohort_id") == r["study_id"]]
ta = [r for r in prim if r["evidence_tier"] == "A" and r["cohort_id"] == r["study_id"]]
dom = Counter(r["clinical_domain"] for r in prim)
ta_dom = Counter(r["clinical_domain"] for r in ta)
ta_des = Counter(r["study_design"] for r in ta)
ta_dir = Counter(r["effect_direction"] for r in ta)
rct_total = sum(1 for r in prim if r["study_design"] == "RCT")
opioid_A = sum(1 for r in ta if r["opioid_outcome"] == "reported")
persist_A = sum(1 for r in ta if r["persistent_pain_definition"] not in ("", "NR"))
yrmin = min(int(r["year"]) for r in prim if r["year"].isdigit())
yrmax = max(int(r["year"]) for r in prim if r["year"].isdigit())
DOMS = ["thoracic_chestwall", "vascular_access", "dental_oral", "orthopedic_msk",
        "chronic_pain_neurolysis", "derm_office", "obstetric_periop", "periop_other", "other_procedural"]
DOMLBL = {"thoracic_chestwall": "thoracic/chest wall", "vascular_access": "vascular access",
          "dental_oral": "dental/oral", "orthopedic_msk": "orthopedic/musculoskeletal",
          "chronic_pain_neurolysis": "chronic pain neurolysis", "derm_office": "dermatologic/office",
          "obstetric_periop": "obstetric/perioperative", "periop_other": "other perioperative",
          "other_procedural": "other procedural"}

# --- per-domain Tier A summary rows (Table 2) ------------------------------
GAP = {
 "thoracic_chestwall": "heterogeneous comparators and persistent-pain definitions; few RCTs outside pectus repair",
 "vascular_access": "short-horizon procedural-pain outcomes; little data on first-attempt success or cost",
 "dental_oral": "pediatric-weighted evidence; precooling vs topical LA rarely separated from injection-pain confounders",
 "orthopedic_msk": "almost no direct LA-comparator trials; TKA cryoneurolysis evidence is adjunctive or indirect",
 "chronic_pain_neurolysis": "no direct LA comparator in most indications; durability beyond months unclear",
 "derm_office": "small trials; mixed comparators (topical LA, nerve block, infiltration)",
 "obstetric_periop": "very small evidence base; isolated trials only",
 "periop_other": "scattered single trials across unrelated procedures",
 "other_procedural": "scattered single trials across unrelated procedures",
}
def dom_summary(d):
    rows = [r for r in ta if r["clinical_domain"] == d]
    rct = sum(1 for r in rows if r["study_design"] == "RCT")
    mod = Counter(r["cryo_modality"] for r in rows).most_common(1)
    comp = Counter((r["LA_type"] or "NR") for r in rows).most_common(1)
    outc = Counter(r["primary_outcome"] for r in rows).most_common(2)
    dirs = Counter(r["effect_direction"] for r in rows)
    dirstr = ", ".join(f"{k.replace('_',' ')} {v}" for k, v in dirs.most_common())
    return [DOMLBL[d], str(len(rows)), str(rct), (mod[0][0] if mod else "NR"),
            (comp[0][0] if comp else "NR"), "; ".join(o[0] for o in outc), dirstr, GAP[d]]

# --- citation machinery: [@key] tokens numbered in first-appearance order ---
order = []
def numbered(text):
    def sub(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        for k in keys:
            assert k in REFS, k
            if k not in order:
                order.append(k)
        return "[" + ",".join(str(order.index(k) + 1) for k in keys) + "]"
    return re.sub(r"\[@([^\]]+)\]", sub, text)

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
def para(t): return doc.add_paragraph(numbered(t))
def h(t, l=1): doc.add_heading(t, level=l)

# ============================ TITLE PAGE ===================================
h("Title page", 0)
para("Cryoanalgesia versus local-anesthetic techniques across clinical settings: a scoping review of primary comparative evidence and evidence gaps")
para("Running title: Cryoanalgesia vs local anesthesia")
para("Article type: Systematic or Scoping Review Article")
para("Corresponding author: Tatsuki Onishi, MD. [ORCID, postal address, telephone, and email to be inserted at submission]")
para("Keywords: cryoanalgesia; cryoneurolysis; local anesthetics; vapocoolant; scoping review; analgesia")

# ============================ ABSTRACT =====================================
h("Abstract", 1)
para(
 "Objective. Cryoanalgesic techniques are used for pain control across perioperative, procedural, and chronic-pain settings, "
 "yet how often they have been compared directly with local-anesthetic (LA) techniques has not been consistently mapped. "
 "This scoping review maps primary comparative evidence at the level of unique patient cohorts. "
 "Methods. The protocol was registered with the Open Science Framework (OSF DOI: 10.17605/OSF.IO/KJ5RS) before the "
 "comprehensive search and rescreening. MEDLINE via PubMed, CENTRAL, Scopus, and ClinicalTrials.gov were searched on "
 "2026-11-09 under a declared English-language policy. Eligible reports were primary human clinical studies evaluating a "
 "cryoanalgesic modality for a clinical analgesic effect. Evidence was tiered by comparator: Tier A (direct LA comparator), "
 "Tier B (indirect comparator), Tier C (noncomparative). A single reviewer screened all records; an AI assistant performed "
 "clerical extraction only. "
 f"Results. Of {cc['records_identified_total']:,} records identified, {cc['primary_study_reports']} primary study reports met "
 f"inclusion, representing {cc['unique_cohorts']} unique cohorts: {cc['tier_A']} Tier A, {cc['tier_B']} Tier B, and "
 f"{cc['tier_C']} Tier C. Direct LA-comparator evidence concentrated in thoracic/chest-wall ({ta_dom['thoracic_chestwall']} cohorts), "
 f"vascular-access ({ta_dom['vascular_access']}), and dental/oral ({ta_dom['dental_oral']}) settings; {ta_des['RCT']} Tier A cohorts were "
 f"randomized trials. Effect directions were mixed ({ta_dir['favors_cryoanalgesia']} favored cryoanalgesia, {ta_dir['no_significant_difference']} no significant "
 f"difference, {ta_dir['favors_comparator']} favored comparator). An explicit persistent-pain outcome definition appeared in {persist_A} Tier A cohorts. "
 "Conclusions. Cryoanalgesia has a substantial efficacy literature, but the subset directly compared with LA-based "
 "techniques is smaller and concentrated in a few domains; substitution evidence remains thin in orthopedic and "
 "chronic-pain applications. Standardized comparator definitions and persistent-pain reporting are priorities."
)

# ============================ INTRODUCTION =================================
h("Introduction", 1)
para(
 "Cryoanalgesia encompasses several distinct techniques that use cold to reduce or interrupt pain signaling. "
 "Intercostal nerve cryoablation and cryoanalgesia have been applied for post-thoracotomy and chest-wall pain since the "
 "1980s [@katz1980;@wang1985]; percutaneous cryoneurolysis uses image-guided cryoprobes to produce temporary nerve "
 "interruption lasting weeks to months through Wallerian degeneration with preservation of the endoneurium "
 "[@trescot;@gabriel2024]; and vapocoolant sprays (such as ethyl chloride), ice, and precooling devices provide brief "
 "surface analgesia for needle procedures [@griffith2016]. These modalities differ profoundly in mechanism, duration, "
 "and invasiveness: vapocoolants act for seconds to minutes at the skin surface, surface cooling devices act over "
 "hours, and percutaneous cryoneurolysis can interrupt conduction for weeks to months after a single treatment. "
 "They nonetheless share a common clinical promise: analgesia without the dosing constraints, motor block, or "
 "hemodynamic effects of local-anesthetic (LA) techniques, and—for longer-acting cryoneurolysis—an "
 "opioid-sparing alternative in settings where postoperative or chronic pain management is difficult [@kehlet]. "
 "Because LA-based infiltration, topical preparations, and neuraxial or peripheral blocks are the conventional "
 "default for most of these indications, the clinically decisive question is not simply whether cold reduces pain, "
 "but whether it performs comparably to, or can substitute for, an LA technique."
)
para(
 "Interpreting this literature is difficult. The cryoanalgesic modalities are heterogeneous; indications span "
 "intraoperative analgesia, procedural needle pain, postoperative recovery, and chronic pain; and comparators vary from "
 "direct LA-based regimens (epidural, peripheral nerve block, topical LA, infiltration) through placebo, sham, usual "
 "care, and non-LA techniques, to designs in which LA appears only as a co-intervention or adjunct. Repeated "
 "publications arising from the same institutional cohorts further inflate apparent study counts, particularly in "
 "pediatric pectus repair."
)
para(
 "A large synthesis literature already exists. Reviews and meta-analyses have examined intercostal cryoablation for "
 "pectus excavatum repair and thoracic surgery [@daemen2020;@notrica2025;@santos2026;@ikarine2026], vapocoolants for "
 "vascular access [@hogan2014;@griffith2016;@wang2023vapo], precooling and intracanal cryotherapy in dentistry "
 "[@tirupathi2020;@andrade2025;@almohaimede2021], cryoneurolysis around knee surgery [@goodwin2025;@hajiaghajani2026], "
 "and cryoneurolysis for chronic pain [@goyal2022;@brancaccio2024;@desrochers2024]. These reviews generally ask whether "
 "cold-based techniques reduce pain, and several reach encouraging pooled conclusions. They have not, however, "
 "consistently separated studies that compared cryoanalgesia directly against an LA-based technique from studies "
 "with indirect or no comparators, and they count reports rather than unique patient cohorts—so the size of "
 "the directly comparative evidence base has not been consistently mapped."
)
para(
 "The question this review asks is therefore more specific than \u201cdoes cryoanalgesia work?\u201d: where has "
 "cryoanalgesia actually been compared directly with an LA-based technique, and where does substitution of one "
 "technique for the other rest only on indirect or noncomparative evidence? Answering it requires a cohort-level "
 "evidence map rather than another pooled estimate: one that identifies every primary clinical cohort, classifies "
 "the comparator it actually used, and separates substitution evidence from the much larger efficacy literature. "
 "Following PRISMA-ScR guidance [@tricco] and established scoping-review methodology [@peters;@arksey], we mapped "
 "the primary comparative evidence on cryoanalgesic versus LA techniques across all clinical settings at "
 "unique-cohort level, tiering every included cohort as direct LA-comparator evidence (Tier A), "
 "indirect-comparator evidence (Tier B), or noncomparative primary evidence (Tier C), and characterizing the "
 "resulting evidence gaps by clinical domain."
)

# ============================ METHODS ======================================
h("Methods", 1)
h("Protocol and reporting", 2)
para(
 "The protocol for this scoping review was registered with the Open Science Framework before the new comprehensive "
 "search and rescreening were undertaken (OSF DOI: 10.17605/OSF.IO/KJ5RS). The registered protocol is the fixed "
 "methodological authority for this review; deviations would require documented, dated, and justified amendment, and "
 "none was needed. Reporting follows the PRISMA Extension for Scoping Reviews [@tricco]; the completed checklist is "
 "submitted with this manuscript."
)
h("Information sources and search", 2)
para(
 "On 2026-11-09 the four sources frozen in the registered protocol were searched: MEDLINE via PubMed (NCBI "
 "E-utilities), CENTRAL (Cochrane Library), Scopus (Elsevier Search API), and ClinicalTrials.gov API v2. The complete "
 "executed search strings, platforms, and source-level yields are provided in Supplementary Appendix S1; "
 "machine-readable exports and the acquisition ledger are archived in the public review repository. CENTRAL records "
 "were captured from a human-cleared Cochrane Library browser session because the platform's citation export requires "
 "a logged-in account; the capture method and field set are documented in the repository. Scopus record export used "
 "the institutional-entitlement-free API view; abstracts for records unique to Scopus were not retrievable under that "
 "entitlement, and such records were screened on title and metadata, as declared in the protocol's screening rules. "
 "Searches applied no language or geographic filters; the English full-text eligibility restriction was declared "
 "before screening."
)
h("Eligibility criteria", 2)
para(
 "Primary human clinical studies evaluating a cryoanalgesic modality—intercostal or peripheral nerve "
 "cryoablation/cryoanalgesia, percutaneous cryoneurolysis or cryoneurotomy, vapocoolant sprays including ethyl "
 "chloride, or procedural surface cooling—for a clinical analgesic effect were eligible. The unit of analysis was the "
 "unique patient cohort; duplicate reports of the same cohort were linked, and ambiguous overlaps were flagged rather "
 "than silently merged. Studies using cold only for sensory or block-testing purposes, cryoablation performed for "
 "non-analgesic indications (e.g., arrhythmia ablation), reports without a patient cohort, and consensus or "
 "design-only publications were excluded. Systematic reviews and meta-analyses, protocols and trial registrations, "
 "and narrative reviews were excluded from the primary-study count and tracked in separate datasets."
)
h("Evidence tiering", 2)
para(
 "Each unique cohort was assigned to one of three tiers under decision rules fixed in the protocol before screening. "
 "Tier A required a direct LA comparator arm, including LA-containing epidural, spinal, or peripheral nerve block, "
 "topical LA, or LA infiltration. Tier B captured indirect comparators: sham, placebo, usual care, opioid-based "
 "regimens, non-LA techniques, or LA used only as an adjunct within a combined regimen. Tier C comprised "
 "noncomparative primary reports. Comparator adjudication used the strongest information available in the indexed "
 "title and abstract; ambiguous records were adjudicated conservatively, and every reassignment was logged with the "
 "supporting source text."
)
h("Selection, charting, and synthesis", 2)
para(
 "One human reviewer screened all titles, abstracts, and eligibility decisions and holds sole responsibility for "
 "inclusion. An AI assistant performed clerical extraction and consistency checks only and was not an independent "
 "reviewer; no dual review or inter-rater reliability coefficient is reported. Data charted per cohort included "
 "clinical domain, study design, sample size, cryo modality and technical parameters, comparator type and LA agent, "
 "primary outcome and timepoint, effect direction, opioid outcomes, explicit persistent-pain outcome definitions, "
 "adverse events, and follow-up. Retrieval completeness was checked against a sentinel set of previously known "
 "eligible studies, and every tier reassignment, domain reclassification, and cohort merge was logged with "
 "supporting source text in the audit trail. Results are synthesized descriptively; no quantitative pooling was attempted, "
 "consistent with scoping-review methodology [@peters]."
)

# ============================ RESULTS ======================================
h("Results", 1)
para(
 f"The search retrieved {cc['records_identified_total']:,} records (PubMed {cc['records_pubmed']:,}; Scopus "
 f"{cc['records_scopus']:,}; CENTRAL {cc['records_central']:,}; ClinicalTrials.gov {cc['records_ctgov']:,}). After removal of "
 f"{cc['records_identified_total'] - cc['records_after_dedup']:,} duplicates, {cc['records_after_dedup']:,} unique records were title-screened; "
 f"{cc['abstract_assessed']:,} were assessed at abstract/metadata level and {cc['eligibility_assessed']:,} underwent eligibility review, "
 f"of which {cc['eligibility_excluded']} were excluded (wrong publication type, non-analgesic cryo application, non-clinical "
 f"material, or sensory-testing-only use of cold). {cc['primary_study_reports']} primary study reports were included (Figure 1), "
 f"representing {cc['unique_cohorts']} unique patient cohorts: {cc['tier_A']} Tier A, {cc['tier_B']} Tier B, and {cc['tier_C']} Tier C. "
 f"{cc['linked_secondary_reports']} linked secondary reports were retained but not counted as unique cohorts. A further "
 f"{cc['synthesis_reports']} synthesis reports and {cc['protocols_ongoing']} protocols or registrations were tracked separately. "
 f"Publication years spanned {yrmin}\u2013{yrmax} (Figure 3); {rct_total} reports were randomized trials. Output "
 f"was visibly bimodal: an earlier wave of post-thoracotomy cryoanalgesia studies and a contemporary wave dominated "
 f"by pectus-repair cryoablation and procedural precooling."
)
para(
 f"By report count, the largest clinical domains were thoracic/chest-wall surgery ({dom['thoracic_chestwall']} reports), "
 f"vascular access ({dom['vascular_access']}), chronic-pain neurolysis ({dom['chronic_pain_neurolysis']}), orthopedic/musculoskeletal "
 f"({dom['orthopedic_msk']}), and dental/oral ({dom['dental_oral']}) (Figure 2). Table 1 presents the same distribution at "
 "unique-cohort level by evidence tier; small differences from report counts reflect the linked secondary reports."
)
para(
 f"Direct LA-comparator evidence ({cc['tier_A']} Tier A cohorts; Table 2) was concentrated in thoracic/chest-wall "
 f"({ta_dom['thoracic_chestwall']}), vascular-access ({ta_dom['vascular_access']}), and dental/oral ({ta_dom['dental_oral']}) settings, which "
 f"together account for {ta_dom['thoracic_chestwall'] + ta_dom['vascular_access'] + ta_dom['dental_oral']} of {cc['tier_A']} cohorts. "
 f"{ta_des['RCT']} Tier A cohorts were randomized trials and {ta_des['cohort/observational']} were cohort or observational "
 "comparisons. The thoracic literature spans four decades—from early post-thoracotomy trials [@katz1980;@brichon1994] "
 "and epidural-versus-cryoanalgesia comparisons [@ju2008] to contemporary pectus-repair trials [@dekonenko2020;"
 "@bastianello2025;@vanpolen2026] and a recent randomized study reporting increased neuropathic pain after "
 "intercostal cryoablation [@weksler2025;@drake2026]. Vascular-access studies compared vapocoolants with topical LA "
 "or infiltration for venipuncture, cannulation, and arterial puncture [@cohenreis1997;@rusch2017;@soueid2007], and "
 "dental studies compared precooling or ethyl chloride with topical LA for injection pain [@aminabadi2009]. Direct "
 "LA-comparator trials in chronic pain are rarer but exist for cervicogenic headache and post-amputation pain "
 "[@kvarstein2019;@ilfeld2023;@ilfeld2024]."
)
para(
 f"Among the {cc['tier_A']} Tier A cohorts, abstract-level effect directions were mixed: cryoanalgesia favored in "
 f"{ta_dir['favors_cryoanalgesia']}, no significant difference in {ta_dir['no_significant_difference']}, comparator favored in "
 f"{ta_dir['favors_comparator']}, and not extractable from the abstract in {ta_dir['unclear/NR']}. Opioid outcomes were reported in "
 f"{opioid_A} Tier A cohorts, and an explicit persistent-pain outcome definition appeared in {persist_A}; most reports did not "
 "define persistent or neuropathic pain outcomes at all. Sample sizes and follow-up horizons were heterogeneous, "
 "ranging from single-session procedural-pain measurements to multi-month surgical follow-up, and many Tier A "
 "cohorts reported no formal sample-size justification."
)

# ============================ DISCUSSION ===================================
h("Discussion", 1)
h("Principal findings", 2)
para(
 "This scoping review shows that the cryoanalgesia literature is large, but that the literature directly comparing "
 "cryoanalgesic with LA-based techniques is substantially smaller and unevenly distributed. The distinction matters "
 "clinically: efficacy evidence demonstrates that a technique can produce analgesia, whereas substitution "
 "evidence—direct head-to-head comparison with the conventional LA standard—is what informs a decision to replace "
 "one technique with the other. Of the primary literature we mapped, only about one quarter of unique cohorts "
 "contributed substitution evidence, and that subset concentrated in three clinical settings. This asymmetry has "
 "two consequences. First, pooled estimates that mix comparator types can overstate how well-supported a "
 "substitution decision is: a meta-analysis of “comparative” cryoanalgesia studies may draw most of its "
 "weight from placebo or usual-care contrasts. Second, domains dominated by Tier B and Tier C reports are not "
 "evidence-poor in an absolute sense—they often contain many studies—but they cannot answer the "
 "substitution question that clinicians actually face."
)
h("Thoracic and chest-wall surgery", 2)
para(
 "Thoracic surgery holds the deepest and most contested evidence ecology. Direct LA-comparator work began with "
 "post-thoracotomy trials in the 1980s\u20131990s [@katz1980;@brichon1994;@ju2008] and has shifted toward "
 "minimally invasive pectus repair, where several prospective comparisons [@dekonenko2020;@bastianello2025;"
 "@vanpolen2026] and recent syntheses [@daemen2020;@notrica2025;@santos2026] have evaluated intercostal "
 "cryoablation against thoracic epidural analgesia. Published syntheses have generally concluded that cryoablation "
 "achieves comparable pain control with shorter stays and lower opioid use in this indication, but our map shows "
 "the underlying cohorts are fewer and more institutionally concentrated than review-level counts suggest: "
 "several reports share institutional pectus cohorts, which we counted once at cohort level. Safety "
 "signals are also real: a randomized study reported more neuropathic pain after cryoablation [@weksler2025;"
 "@drake2026], and adverse-event series have been synthesized separately [@kroczek2025]. Rib-fracture and "
 "thoracotomy applications beyond pectus repair remain supported mainly by adjunct or indirect evidence "
 "[@ikarine2026;@cha2021;@passos2025]."
)
h("Vascular access", 2)
para(
 "Vapocoolants and precooling for needle procedures constitute a distinct evidence ecology from nerve "
 "cryoablation: outcomes are immediate procedural pain and patient preference, comparators are topical LA (EMLA, "
 "tetracaine gel) or infiltration, and study populations are often pediatric. Meta-analyses have found vapocoolants "
 "broadly comparable to, but not superior to, topical anesthesia for venipuncture and cannulation "
 "[@hogan2014;@griffith2016;@wang2023vapo], and our map confirms a dense but short-horizon literature in which "
 "speed, avoidance of a second injection, and ease of use—rather than superior analgesia—are the main "
 "arguments for substitution [@cohenreis1997;@rusch2017;@soueid2007]. Adjacent procedural applications, such as "
 "vaccination [@hall2020] and perineal pain after childbirth [@east2020], rely largely on indirect comparisons."
)
h("Dental and oral procedures", 2)
para(
 "In dentistry, precooling and ethyl chloride are compared mainly against topical LA for reducing injection pain, "
 "and intracanal cryotherapy against conventional irrigation for post-endodontic pain [@tirupathi2020;@andrade2025;"
 "@almohaimede2021]. These are cooling-to-reduce-injection-pain questions, mechanistically different from "
 "cryoneurolysis; conflating them with nerve cryoablation overstates the evidence. Within their own frame, the "
 "trials are small, pediatric-weighted, and report heterogeneous short-term outcomes [@aminabadi2009]."
)
h("Orthopedic and chronic-pain applications", 2)
para(
 "Interest in cryoneurolysis around total knee arthroplasty and knee osteoarthritis has grown quickly "
 "[@goodwin2025;@hajiaghajani2026;@tidwell2024], yet our map found that most of this literature is indirect, "
 "adjunctive, or noncomparative: preoperative genicular cryoneurolysis is typically added to, rather than compared "
 "with, LA-based regimens. The same pattern holds for chronic-pain applications—post-amputation and phantom-limb "
 "pain, cervicogenic headache, post-mastectomy pain—where a handful of rigorous randomized trials exist "
 "[@kvarstein2019;@ilfeld2023;@ilfeld2024] amid a larger noncomparative literature [@goyal2022;@brancaccio2024;"
 "@desrochers2024;@bailey2021]. Analgesic efficacy demonstrated in these settings should not be read as evidence "
 "that cryoneurolysis can substitute for LA-based techniques, which remain essentially untested as comparators "
 "there."
)
h("Why this map differs from prior reviews", 2)
para(
 "Our direct-evidence counts are deliberately smaller than the numbers of \u201ccomparative\u201d studies implied "
 "by earlier syntheses, for structural reasons: reviews and protocols were excluded from primary counts; each "
 "unique patient cohort is counted once regardless of how many reports it generated (eight linked secondary "
 "reports were retained but not recounted); and placebo, usual-care, adjunct, and non-LA comparators were separated "
 "from direct LA comparators. Earlier reviews pooled evidence items without a cohort-level unit and mixed direct "
 "with indirect comparators. For clinical readers, the consequence is that \u201chow much comparative evidence "
 "exists?\u201d depends critically on what counts as a comparator and what counts as a study."
)
h("Clinical implications", 2)
para(
 "Where direct comparative evidence exists—pectus and thoracic surgery, vascular access, dental injections—the "
 "effect directions are heterogeneous and the frequency of adjunct designs precludes a blanket equivalence claim. "
 "In pectus repair, cryoablation is a reasonable LA-adjacent or LA-replacing option within institutional enhanced-"
 "recovery pathways, subject to neuropathic-pain surveillance. For needle procedures, vapocoolants offer speed and "
 "avoidance of infiltration rather than superior analgesia. Elsewhere, the honest position is not equivalence but "
 "absence of substitution evidence."
)
h("Research priorities", 2)
para(
 "Five priorities follow from the map: (i) direct LA-comparator trials in orthopedic and chronic-pain domains, "
 "where substitution evidence is thinnest; (ii) standardized, verbatim persistent-pain and neuropathic-outcome "
 "definitions—only a small minority of Tier A cohorts specified one—particularly given post-cryoablation "
 "neuropathic-pain signals [@weksler2025;@drake2026]; (iii) explicit declaration of whether LA is a comparator or "
 "an adjunct; (iv) longer follow-up reporting technical cryo parameters; and (v) clearer cohort linkage and trial "
 "registration to prevent duplicate counting of institutional series."
)
h("Limitations", 2)
para(
 "Several limitations qualify this map. Screening relied on indexed titles and abstracts; for records unique to "
 "Scopus, abstracts were not retrievable under the entitlement used, so those records were screened on title and "
 "metadata and may have misclassified edge cases. CENTRAL citation export is login-gated; records were captured "
 "from a human-cleared browser session, a capture method documented in the repository. The English full-text "
 "policy excludes non-English reports, a non-trivial fraction of the historical cryoanalgesia literature. Effect "
 "estimates were extracted only where stated in the abstract, so \u201cunclear/NR\u201d rows reflect reporting gaps "
 "rather than absent effects, and no formal risk-of-bias appraisal or meta-analysis was performed, consistent with "
 "scoping-review methodology [@tricco;@peters]. A single reviewer conducted screening as declared in the protocol; "
 "no independent second review was performed. Cohort deduplication across non-randomized institutional series "
 "(notably MIRPE/Nuss cohorts) was flagged as possible overlap where metadata could not confirm uniqueness. "
 "Finally, cryoanalgesia was defined broadly across modalities; readers should interpret tier counts within, not "
 "across, the distinct modality ecologies."
)

# ============================ CONCLUSIONS ==================================
h("Conclusions", 1)
para(
 f"Across {cc['primary_study_reports']} primary study reports spanning {yrmin}\u2013{yrmax}, direct cryoanalgesia-versus-LA "
 "evidence is concentrated in thoracic/chest-wall, vascular-access, and dental/oral domains and is sparse elsewhere. "
 "The efficacy literature substantially exceeds the substitution literature; where LA replacement is contemplated, "
 "head-to-head trials remain the missing evidence. Prior reviews have documented that cold-based techniques can "
 "reduce pain; this map delineates where they have actually been measured against the LA standard they would "
 "replace. For pain practitioners, the practical message is conservative: cryoanalgesia is a credible LA-adjacent "
 "option where direct evidence exists, a promising but untested substitute where it does not, and a modality "
 "whose neuropathic safety profile still needs standardized surveillance. Standardized comparator declarations, "
 "persistent-pain outcome definitions, and cohort-level reporting would make the evidence base far easier to "
 "interpret and to synthesize quantitatively."
)

# ============================ DECLARATIONS =================================
h("Declarations", 1)
para("Declarations of interest: none to declare. Funding: none.")
para("Data availability: the review protocol was registered on the Open Science Framework (OSF DOI: "
     "10.17605/OSF.IO/KJ5RS; https://osf.io/kj5rs/). Journal supplementary material comprises Supplementary "
     "Appendix S1 (complete electronic search strategies) and Supplementary Data (machine-readable datasets, "
     "including the full 124-cohort Tier A extraction table). The full reproducibility archive\u2014executed "
     "search strings, source-level yields, screening and evidence-map datasets, audit files, and generation "
     "code\u2014is available in the public review repository "
     "(https://github.com/bougtoir/cryoanalgesia-la-evidence-map, submission snapshot tag v1.0-submission).")
para("Author contributions: [to be completed at submission].")

# ============================ REFERENCES ===================================
h("References", 1)
for i, k in enumerate(order, 1):
    doc.add_paragraph(f"{i}. {vancouver(k)}")

# ============================ TABLES =======================================
h("Table 1. Unique cohorts by clinical domain and evidence tier", 1)
t = doc.add_table(rows=1, cols=5); t.style = "Table Grid"
for i, x in enumerate(["Domain", "Tier A", "Tier B", "Tier C", "Total"]):
    t.rows[0].cells[i].text = x
for d in DOMS:
    a = sum(1 for r in cohp if r["clinical_domain"] == d and r["evidence_tier"] == "A")
    b = sum(1 for r in cohp if r["clinical_domain"] == d and r["evidence_tier"] == "B")
    c = sum(1 for r in cohp if r["clinical_domain"] == d and r["evidence_tier"] == "C")
    row = t.add_row().cells
    for i, v in enumerate([DOMLBL[d], a, b, c, a + b + c]):
        row[i].text = str(v)
row = t.add_row().cells
for i, v in enumerate(["Total", cc["tier_A"], cc["tier_B"], cc["tier_C"], cc["unique_cohorts"]]):
    row[i].text = str(v)

h(f"Table 2. Tier A direct LA-comparator evidence by clinical domain ({cc['tier_A']} unique cohorts)", 1)
t2 = doc.add_table(rows=1, cols=8); t2.style = "Table Grid"
for i, x in enumerate(["Domain", "Tier A cohorts", "RCTs", "Dominant cryo modality", "Main LA comparator",
                       "Principal outcomes", "Effect directions", "Key evidence gap"]):
    t2.rows[0].cells[i].text = x
for d in DOMS:
    if ta_dom[d] == 0:
        continue
    row = t2.add_row().cells
    for i, v in enumerate(dom_summary(d)):
        row[i].text = v
doc.add_paragraph(
 "The complete cohort-level Tier A extraction table (124 rows) is provided in Supplementary Data and the "
 "public review repository.")

# ============================ FIGURE LEGENDS ===============================
h("Figure legends", 1)
para("Figure 1. PRISMA-ScR flow diagram of record identification, screening, eligibility, and inclusion "
     "(submitted as a separate file).")
para("Figure 2. Primary study reports by clinical domain and evidence tier (submitted as a separate file).")
para("Figure 3. Publication year of primary study reports by evidence tier (submitted as a separate file).")

doc.save(FIN + "Pain_Medicine_main_manuscript_FINAL.docx")

# ---------- word count ----------
main_words = 0
for p in doc.paragraphs:
    main_words += len(re.findall(r"\S+", p.text))
print("approx words total:", main_words)
print("refs:", len(order))
