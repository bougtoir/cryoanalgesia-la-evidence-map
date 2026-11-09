#!/usr/bin/env python3
"""CENTRAL (Cochrane Library) harvest via CDP on the cleared Chrome profile.
Submits each query through the site's own basic-search form (Title Abstract
Keyword, searchBy=1), then parses rendered result items per page (DOM capture;
citation export is login-gated). Writes raw HTML + parsed JSON + manifest.
"""
import json, time, os, sys, hashlib, csv, datetime
import urllib.request, websocket

BASE = "/home/ubuntu/pm_work/post_osf"
RAW = f"{BASE}/raw"; EXP = f"{BASE}/exports"
os.makedirs(RAW, exist_ok=True); os.makedirs(EXP, exist_ok=True)
CDP = "http://localhost:9333/json"
SEARCH_DATE = "2026-11-09"

QUERIES = {
 "C1_core_cryo": 'cryoanalgesia OR "cryoneurolysis" OR "cryoneurotomy" OR "cryo nerve block" OR "cryogenic nerve block" OR "nerve cryoablation" OR "intercostal cryoanalgesia" OR "cryoablation of nerves"',
 "C2_cryo_x_pain": '(cryo* NEAR/3 (analgesia OR analgesic OR "nerve block" OR neurolysis OR "pain management" OR "postoperative pain"))',
 "C3_dental": '(cryoanalgesia OR cryoneurolysis OR cryoablation) AND (dental OR dentistry OR "third molar" OR tonsillectomy OR "oral surgery" OR alveolar)',
 "C4_vascular": '(cryoanalgesia OR cryoneurolysis) AND (vascular OR "varicose vein" OR endovenous OR amputation OR "limb ischemia")',
 "C5_thoracic": '(cryoanalgesia OR cryoneurolysis OR "intercostal cryo*") AND (thoracotomy OR thoracic OR thoracoscopy OR sternotomy OR pectus OR "rib fracture" OR Nuss OR mammary)',
 "C6_orthopedic": '(cryoanalgesia OR cryoneurolysis) AND (orthopedic OR "knee arthroplasty" OR "total knee" OR "total hip" OR arthroscopy OR spine OR laminectomy OR "joint replacement")',
 "C7_derm_neuro": '(cryoanalgesia OR cryoneurolysis OR cryoablation) AND (dermatolog* OR skin OR neuroma OR neuropathy OR "post-herpetic" OR postherpetic OR pudendal OR occipital OR supraorbital)',
 "C8_LA_x_cryo": '("local anesthe*" OR lidocaine OR bupivacaine OR ropivacaine OR "nerve block") AND (cryoanalgesia OR cryoneurolysis OR "cryo ablation" OR cryoablation)',
}

def ws_connect():
    tabs = json.load(urllib.request.urlopen(CDP))
    pg = [t for t in tabs if t['type'] == 'page' and 'cochranelibrary' in t.get('url', '')]
    if not pg:
        pg = [t for t in tabs if t['type'] == 'page']
    return websocket.create_connection(pg[0]['webSocketDebuggerUrl'], timeout=120, suppress_origin=True)

def new_ev(ws):
    mid = [0]
    def ev(expr, timeout=120):
        mid[0] += 1
        ws.send(json.dumps({'id': mid[0], 'method': 'Runtime.evaluate',
                            'params': {'expression': expr, 'returnByValue': True, 'awaitPromise': True}}))
        ws.settimeout(timeout)
        while True:
            m = json.loads(ws.recv())
            if m.get('id') == mid[0]:
                return m['result']['result'].get('value')
    return ev

def save_raw(name, data):
    p = f"{RAW}/{name}"
    b = data.encode() if isinstance(data, str) else data
    open(p, 'wb').write(b)
    return {"file": f"raw/{name}", "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

manifest = []
ws = ws_connect(); ev = new_ev(ws)

for qid, q in QUERIES.items():
    # submit via the site's own basic search form
    ev(f'''
      var f=[...document.querySelectorAll("form")].find(f=>f.action.includes('redirectSearchResult'));
      if(!f){{ location.href='https://www.cochranelibrary.com/advanced-search'; }}
      f.querySelector('[name=searchText]').value={json.dumps(q)};
      f.querySelector('[name=searchBy]').value='1';
      f.submit();''')
    # wait for results to render
    n_items = 0
    for _ in range(40):
        time.sleep(2)
        try:
            n_items = ev('document.querySelectorAll(".search-results-item").length') or 0
            if n_items: break
        except Exception:
            time.sleep(2)
            ws = ws_connect(); ev = new_ev(ws)
    hits_txt = ev('(document.querySelector(".results-number")||{textContent:""}).textContent.trim()') or ''
    body = ev('document.body.innerText') or ''
    import re
    m = re.search(r'(\d+)\s+Trials matching', body)
    total = int(m.group(1)) if m else (int(hits_txt) if hits_txt.isdigit() else None)
    # set 100 per page
    try:
        ev('''var s=document.querySelector('select#resultPerPage'); if(s){s.value='100'; s.dispatchEvent(new Event('change',{bubbles:true}));}''')
        time.sleep(6)
    except Exception:
        pass
    import math
    # get a pagination URL template (contains cur=N) and fetch all pages directly
    link_tmpl = ev('''
      (function(){
        var a=document.querySelector('.pagination-page-list-item a');
        if(!a) return null;
        var u=a.href.replace(/resultPerPage=\\d+/,'resultPerPage=100');
        return u;
      })()''')
    pages = max(1, math.ceil((total or 0) / 100)) if total else 1
    all_recs = []
    for page in range(1, pages + 1):
        if link_tmpl:
            url_page = re.sub(r'cur=\d+', f'cur={page}', link_tmpl)
            html = ev(f'''
              fetch({json.dumps(url_page)},{{credentials:'include'}})
                .then(r=>r.text())''') or ''
        else:
            html = ev('document.querySelector(".search-results")?document.querySelector(".search-results").outerHTML:document.body.innerHTML') or ''
        save_raw(f"central_{qid}_page{page}.html", html)
        recs = ev(f'''
          (function(){{
            var doc=new DOMParser().parseFromString({json.dumps(html)},'text/html');
            var src=doc.querySelector('.search-results')?doc:document;
            return [...src.querySelectorAll(".search-results-item")].map(it=>{{
              const d=[...it.querySelectorAll("[data-article-doi]")].map(x=>x.getAttribute("data-article-doi")).join(";");
              const t=(it.querySelector(".result-title a")||{{textContent:""}}).textContent.trim();
              const href=(it.querySelector(".result-title a")||{{href:""}}).href;
              const auth=(it.querySelector(".search-result-authors")||{{textContent:""}}).textContent.trim();
              const meta=(it.querySelector(".search-result-metadata-text")||{{textContent:""}}).textContent.trim().replace(/\\s+/g," ");
              const s=(it.querySelector(".external-database-reference")||{{textContent:""}}).textContent.trim();
              return {{cn_doi:d,title:t,authors:auth,metadata:meta,source_db:s,href:href}};
            }});
          }})()''') or []
        all_recs.extend(recs)
        time.sleep(1)
    # drop duplicates within a query (same CN DOI)
    seen = set(); ded = []
    for r in all_recs:
        k = r['cn_doi'] or r['title']
        if k in seen: continue
        seen.add(k); ded.append(r)
    all_recs = ded
    out = f"{EXP}/central_{qid}.json"
    json.dump(all_recs, open(out, "w"), indent=1)
    manifest.append({"source": "CENTRAL", "platform": "Cochrane Library web (cochranelibrary.com), cleared-session DOM capture; citation export is login-gated",
                     "date": SEARCH_DATE, "query_id": qid, "query": q,
                     "filters": "field=Title Abstract Keyword (searchBy=1); word variations searched (site default)",
                     "date_restriction": "none",
                     "raw_hits": total if total is not None else len(all_recs),
                     "exported_records": len(all_recs),
                     "export_file": os.path.relpath(out, BASE)})
    print(f"CENTRAL {qid}: hits={total} exported={len(all_recs)}", flush=True)

with open(f"{BASE}/CENTRAL_EXPORT_MANIFEST.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["source","platform","date","query_id","query","filters","date_restriction","partition_detail","raw_hits","exported_records","export_file"], extrasaction="ignore")
    w.writeheader(); w.writerows(manifest)
print("done", len(manifest))
