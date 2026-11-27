"""Recompute the reported counts (PRISMA arithmetic, report/cohort units, Tier A/B/C, Table 1 domain x tier, Tier A effect directions, opioid and persistent-pain counts) from the CSV/JSON files in this repository only.
Usage: python3 scripts/verify_counts.py  (run from repository root; Python 3 standard library only)"""
import csv,json,sys,collections,os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
cc=json.load(open(D+'CANONICAL_COUNTS_FINAL_RECONCILED.json'))
p=list(csv.DictReader(open(D+'PRIMARY_STUDY_MAP.csv')))
pr=[r for r in p if r['study_id']==r['cohort_id']]
taf=list(csv.DictReader(open(D+'TIER_A_COMPLETE.csv')))
syn=sum(1 for _ in csv.DictReader(open(D+'SYNTHESIS_REPORTS.csv'))); prot=sum(1 for _ in csv.DictReader(open(D+'PROTOCOLS_ONGOING.csv')))
tier=collections.Counter(r['evidence_tier'] for r in pr); ed=collections.Counter(r['effect_direction'] for r in taf)
ta=[r for r in pr if r['evidence_tier']=='A']
res=[]
def chk(n,a,b): res.append((n,a,b,a==b))
for k,v in [('primary_study_reports',len(p)),('unique_cohorts',len(pr)),('tier_A',tier['A']),('tier_B',tier['B']),('tier_C',tier['C']),('synthesis_reports',syn),('protocols_ongoing',prot),('linked_secondary_reports',len(p)-len(pr))]:
    chk('CSV vs canonical JSON: '+k,v,cc[k])
chk('PRISMA 1231=662+428+101+40',cc['eligibility_excluded']+len(p)+syn+prot,cc['eligibility_assessed'])
chk('TIER_A_COMPLETE rows == Tier A cohorts',len(taf),tier['A'])
chk('randomized_primary (study_design == RCT, all reports)',sum(r['study_design']=='RCT' for r in p),cc['randomized_primary'])
print('Tier A effect directions (computed, descriptive):', dict(ed))
print('Tier A opioid outcome reported:', sum(r['opioid_outcome']=='reported' for r in ta))
print('Tier A explicit persistent-pain definition:', sum(r['persistent_pain_definition'] not in ('','NR') for r in ta))
ct=collections.Counter((r['clinical_domain'],r['evidence_tier']) for r in pr)
print('Table 1 (unique cohorts by domain and tier):')
for d in sorted({r['clinical_domain'] for r in pr}):
    print(f"  {d}: A {ct[(d,'A')]}, B {ct[(d,'B')]}, C {ct[(d,'C')]}, total {sum(ct[(d,t)] for t in 'ABC')}")
yr=collections.Counter(int(r['year']) for r in p if r['year'].isdigit())
print('Reports published before 1980 (not shown in year figure):',sum(v for y,v in yr.items() if y<1980))
bad=0
for n,a,b,ok in res:
    bad+=not ok; print(f'{"PASS" if ok else "FAIL"}  {n}: {a}' + ('' if ok else f' (expected {b})'))
print('Overall:', 'PASS' if not bad else 'FAIL'); sys.exit(bad>0)
