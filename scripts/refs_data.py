# Reference pool for the expanded review article.
# key -> {"pmid": ...} for PubMed-verified, or {"crossref": (authors, title, journal, year, doi)}
import json

VER = json.load(open("/home/ubuntu/pm_work/refs_verified.json"))

REFS = {
    # methodology / background
    "tricco": {"pmid": "30178033"},
    "peters": {"pmid": "33570328"},
    "arksey": {"crossref": ("Arksey H, O'Malley L", "Scoping studies: towards a methodological framework", "Int J Soc Res Methodol", "2005", "8", "19-32", "10.1080/1364557032000119616")},
    "kehlet": {"pmid": "16698416"},
    "trescot": {"pmid": "16880882"},
    "gabriel2024": {"pmid": "38963513"},
    "wang1985": {"pmid": "2995903"},
    # syntheses
    "ernst1994": {"pmid": "8169463"},
    "hogan2014": {"pmid": "25168120"},
    "griffith2016": {"pmid": "27113639"},
    "wang2023vapo": {"pmid": "36780438"},
    "park2021": {"pmid": "34408872"},
    "daemen2020": {"pmid": "32929487"},
    "notrica2025": {"pmid": "40720602"},
    "santos2026": {"pmid": "42332433"},
    "ikarine2026": {"pmid": "41965210"},
    "kroczek2025": {"pmid": "41537297"},
    "tirupathi2020": {"pmid": "32617406"},
    "andrade2025": {"pmid": "40231138"},
    "almohaimede2021": {"pmid": "34831517"},
    "wang2024tonsil": {"pmid": "39069570"},
    "goodwin2025": {"pmid": "40613355"},
    "hajiaghajani2026": {"pmid": "40513900"},
    "goyal2022": {"pmid": "36111102"},
    "brancaccio2024": {"pmid": "39707720"},
    "hall2020": {"pmid": "33189429"},
    "east2020": {"pmid": "33034900"},
    "bailey2021": {"pmid": "32955997"},
    "tidwell2024": {"pmid": "38127092"},
    "cha2021": {"pmid": "34079913"},
    "passos2025": {"pmid": "40292042"},
    "desrochers2024": {"pmid": "39716781"},
    # primary landmark studies (all in TIER_A_COMPLETE)
    "katz1980": {"pmid": "6102235"},
    "brichon1994": {"pmid": "7811482"},
    "ju2008": {"pmid": "17870625"},
    "dekonenko2020": {"pmid": "31699436"},
    "bastianello2025": {"pmid": "40035332"},
    "weksler2025": {"pmid": "39522714"},
    "drake2026": {"pmid": "41199434"},
    "vanpolen2026": {"pmid": "42528259"},
    "ilfeld2022": {"pmid": "35929983"},
    "ilfeld2023": {"pmid": "36512721"},
    "ilfeld2024": {"pmid": "38478876"},
    "kvarstein2019": {"pmid": "31675351"},
    "cohenreis1997": {"pmid": "9374583"},
    "rusch2017": {"pmid": "27590462"},
    "soueid2007": {"pmid": "17572521"},
    "aminabadi2009": {"pmid": "19430625"},
}


def vancouver(key):
    """Return the Vancouver reference string for key."""
    r = REFS[key]
    if "crossref" in r:
        a, t, j, y, v, p, d = r["crossref"]
        return f"{a}. {t}. {j}. {y};{v}:{p}. doi:{d}"
    o = VER[r["pmid"]]
    s = f"{o['authors']}. {o['title']}. {o['journal']}. {o['year']}"
    if o["vol"]:
        s += f";{o['vol']}"
        if o["issue"]:
            s += f"({o['issue']})"
        if o["pages"]:
            s += f":{o['pages']}"
    s += "."
    if o["doi"]:
        s += f" doi:{o['doi']}."
    s += f" PMID:{r['pmid']}."
    return s
