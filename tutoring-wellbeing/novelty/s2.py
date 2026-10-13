import json, time, urllib.request, urllib.error, urllib.parse
BASE = "https://api.semanticscholar.org/graph/v1"
def get(path, tries=8):
    url = BASE + path
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "novelty-scan/0.1"})
            with urllib.request.urlopen(req, timeout=60) as r:
                time.sleep(1.1); return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(min(60, 3 * 2 ** i)); continue
            raise
    raise RuntimeError("failed " + url)
def search(q, n=8, fields="paperId,title,year,citationCount,externalIds"):
    return get(f"/paper/search?limit={n}&fields={fields}&query=" + urllib.parse.quote(q))["data"]
def citations(pid, fields="paperId,title,year,abstract,externalIds,venue"):
    out, off = [], 0
    while True:
        d = get(f"/paper/{pid}/citations?limit=1000&offset={off}&fields={fields}")
        out += [x["citingPaper"] for x in d.get("data", [])]
        if "next" not in d: return out
        off = d["next"]
