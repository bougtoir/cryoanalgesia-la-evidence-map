#!/usr/bin/env python3
import csv,matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from collections import Counter
OUT="/home/ubuntu/repos/wip/manuscript/pain_medicine/Pain_Medicine_post_OSF_rebuild/"
fl=[r for r in csv.DictReader(open(OUT+"PRISMA_FLOW_DATA.csv"))]
d={r["quantity"]:int(r["n"]) for r in fl}
fig,ax=plt.subplots(figsize=(8.5,7.5));ax.axis("off")
def box(x,y,w,h,txt,fs=9):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02",fc="#eef3f8",ec="#335",lw=1))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=fs)
def arrow(x1,y1,x2,y2):ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="->",mutation_scale=14,color="#335"))
box(0.05,0.88,0.5,0.09,f'Records identified (n = {d["records identified from databases"]:,})\nPubMed n={d["MEDLINE via PubMed"]:,}; CENTRAL n={d["CENTRAL"]:,}; Scopus n={d["Scopus"]:,}; CT.gov n={d["ClinicalTrials.gov"]:,}')
box(0.62,0.88,0.33,0.09,f'Duplicate records removed\n(n = {d["duplicate records removed"]:,})')
box(0.05,0.70,0.5,0.09,f'Records screened at title level\n(n = {d["records screened (title)"]:,})')
box(0.62,0.70,0.33,0.09,f'Records excluded at title level\n(n = {d["records excluded (title)"]:,})')
box(0.05,0.52,0.5,0.09,f'Records assessed at abstract/metadata level\n(n = {d["records assessed at abstract/metadata level"]:,})')
box(0.62,0.52,0.33,0.09,f'Records excluded at abstract level\n(n = {d["records excluded (abstract)"]:,})')
box(0.05,0.34,0.5,0.09,f'Reports assessed for eligibility\n(n = {d["reports assessed for eligibility"]:,})')
box(0.62,0.34,0.33,0.09,f'Reports excluded at eligibility\n(n = {d["reports excluded at eligibility"]:,})')
box(0.05,0.14,0.5,0.12,f'Primary study reports included (n = {d["primary study reports included"]:,})\nTier A direct LA comparator n = {d["Tier A (direct LA comparator)"]}\nTier B indirect comparator n = {d["Tier B (indirect comparator)"]}\nTier C noncomparative n = {d["Tier C (noncomparative)"]}')
box(0.62,0.14,0.33,0.12,f'Tracked separately\nSynthesis reports n = {d["synthesis reports"]}\nProtocols/ongoing n = {d["protocols/ongoing"]}')
for y1,y2 in [(0.88,0.79),(0.70,0.61),(0.52,0.43),(0.34,0.26)]:arrow(0.30,y1,0.30,y2)
for y in [0.925,0.745,0.565,0.385,0.20]:arrow(0.55,y,0.62,y)
ax.set_xlim(0,1);ax.set_ylim(0.1,1)
plt.tight_layout();plt.savefig(OUT+"PRISMA_FLOW_FINAL.png",dpi=300);plt.close()
# Figure 2: domain x tier stacked bars
prim=list(csv.DictReader(open(OUT+"PRIMARY_STUDY_MAP.csv")))
doms=["thoracic_chestwall","vascular_access","dental_oral","orthopedic_msk","chronic_pain_neurolysis","derm_office","periop_other","other_procedural"]
cnt=Counter((r["clinical_domain"],r["evidence_tier"]) for r in prim)
A=[cnt[(d,"A")] for d in doms];B=[cnt[(d,"B")] for d in doms];C=[cnt[(d,"C")] for d in doms]
fig,ax=plt.subplots(figsize=(8,4.8))
x=range(len(doms))
ax.bar(x,A,label="Tier A (direct LA comparator)",color="#2b6cb0")
ax.bar(x,B,bottom=A,label="Tier B (indirect comparator)",color="#90cdf4")
ax.bar(x,C,bottom=[a+b for a,b in zip(A,B)],label="Tier C (noncomparative)",color="#cbd5e0")
ax.set_xticks(list(x));ax.set_xticklabels(["Thoracic/\nchest wall","Vascular\naccess","Dental/\noral","Orthopedic/\nMSK","Chronic pain\nneurolysis","Derm/\noffice","Periop\nother","Other\nprocedural"],fontsize=9)
ax.set_ylabel("Primary study reports (n)");ax.legend(fontsize=8)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout();plt.savefig(OUT+"Figure2_domain_tier.png",dpi=300);plt.close()
# Figure 3: publication year histogram by tier
years={}
for r in prim:
    try:y=int(r["year"])
    except:continue
    years.setdefault(y,Counter())[r["evidence_tier"]]+=1
ys=sorted(years);ys=[y for y in ys if y>=1980]
fig,ax=plt.subplots(figsize=(8,4.8))
A=[years[y]["A"] for y in ys];B=[years[y]["B"] for y in ys];C=[years[y]["C"] for y in ys]
ax.bar(ys,A,label="Tier A",color="#2b6cb0")
ax.bar(ys,B,bottom=A,label="Tier B",color="#90cdf4")
ax.bar(ys,C,bottom=[a+b for a,b in zip(A,B)],label="Tier C",color="#cbd5e0")
ax.set_xlabel("Publication year");ax.set_ylabel("Primary study reports (n)");ax.legend(fontsize=8)
ax.spines[["top","right"]].set_visible(False)
plt.tight_layout();plt.savefig(OUT+"Figure3_year_tier.png",dpi=300);plt.close()
print("figs done")
