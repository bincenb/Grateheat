"""Forward-citation novelty scan.

For each anchor paper, pull the complete list of citing works from the
OpenCitations Index (v2), fetch title + abstract from Crossref, and flag any
citing work that mentions tutoring/shadow education AND a wellbeing outcome
AND a large-scale assessment. Flagged works are reviewed by hand.
"""
import json, re, time, urllib.parse, urllib.request, urllib.error

ANCHORS = {
    "10.1186/s40536-024-00228-5": "Karakus et al. 2024, tutoring and math in PISA 2022",
    "10.3389/fpsyg.2022.860179": "Liang et al. 2022, shadow education and wellbeing, PISA 2018 Hong Kong",
    "10.3390/ijerph18031222": "Taiwan 2021, shadow education and mental health",
    "10.3390/bs15070885": "China 2025, shadow education duration and depression",
    "10.1111/ejed.12413": "Zhang & Bray 2020, comparative research on shadow education (review)",
    "10.1108/s1479-353920180000020004": "Global patterns of shadow education use (cross-national)",
    "10.1146/annurev-soc-081715-074341": "Park et al. 2016, learning beyond the school walls (review)",
}

UA = {"User-Agent": "novelty-scan/0.1"}

def get_json(url, tries=6):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 * (i + 1))
        except Exception:
            time.sleep(2 * (i + 1))
    return None

def citing_dois(doi):
    d = get_json(f"https://api.opencitations.net/index/v2/citations/doi:{doi}") or []
    out = []
    for row in d:
        m = re.search(r"doi:(\S+)", row.get("citing", ""))
        if m:
            out.append(m.group(1).lower())
    return out

def crossref(doi):
    d = get_json("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if not d:
        return {"doi": doi, "title": "", "abstract": "", "year": None}
    m = d["message"]
    abstract = re.sub(r"<[^>]+>", " ", m.get("abstract", "") or "")
    year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return {"doi": doi, "title": (m.get("title") or [""])[0], "abstract": abstract, "year": year,
            "venue": (m.get("container-title") or [""])[0]}

TUTOR = re.compile(r"tutor|shadow educ|cram|supplementary (education|lesson|instruction)|out-of-school (lesson|class)|additional instruction|hagwon|juku|buxiban", re.I)
WELL = re.compile(r"well-?being|anxiety|life satisfaction|stress|depress|mental health|happiness|emotion|burnout|distress", re.I)
LSA = re.compile(r"\bPISA\b|\bTIMSS\b|cross-national|cross-country|international large-scale", re.I)

def main():
    seen, rows = {}, []
    for doi, label in ANCHORS.items():
        cites = citing_dois(doi)
        print(f"{doi}  {label}: {len(cites)} citing works")
        for c in cites:
            if c not in seen:
                seen[c] = crossref(c)
                time.sleep(0.2)
            rows.append((doi, c))
    flagged = []
    for c, m in seen.items():
        text = f"{m['title']} {m['abstract']}"
        t, w, l = bool(TUTOR.search(text)), bool(WELL.search(text)), bool(LSA.search(text))
        m.update(tutor=t, wellbeing=w, lsa=l, has_abstract=bool(m["abstract"].strip()))
        if t and w:
            flagged.append(m)
    json.dump({"anchors": ANCHORS, "edges": rows, "works": seen}, open("scan_results.json", "w"), indent=1)
    print(f"\nUnique citing works scanned: {len(seen)}  (with abstract: {sum(m['has_abstract'] for m in seen.values())})")
    print(f"Flagged (tutoring AND wellbeing terms): {len(flagged)}\n")
    for m in sorted(flagged, key=lambda m: (not m["lsa"], -(m["year"] or 0))):
        print(f"[{'LSA' if m['lsa'] else '   '}] {m['year']} {m['doi']} | {m['title'][:120]}")

if __name__ == "__main__":
    main()
