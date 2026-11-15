#!/usr/bin/env python3
"""Refresh an indoor UAV evidence base from OpenAlex."""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timezone

DB = Path("database.json")
QUERIES = [
    '"UAV" indoor warehouse',
    '"unmanned aerial vehicle" indoor inspection',
    '"indoor drone" warehouse',
    '"UAV" factory indoor navigation',
    '"drone" warehouse inventory inspection',
    '"UAV" rack inspection',
    '"indoor aerial robot" industrial',
]
AIRCRAFT = re.compile(r"\b(drone|uav|uas|unmanned aerial vehicle|unmanned aerial system|aerial robot)\b", re.I)
INDOOR = re.compile(r"\b(indoor|indoors|warehouse|distribution cent(?:re|er)|factory|manufacturing facility|enclosed (?:space|environment)|racking|rack inspection|gps-denied|indoor navigation)\b", re.I)
DIRECT = re.compile(r"warehouse|distribution cent(?:re|er)|racking|rack inspection|inventory|stocktaking", re.I)

def abstract_from_inverted(inv):
    if not inv: return ""
    words = {}
    for word, positions in inv.items():
        for pos in positions: words[pos] = word
    return " ".join(words[k] for k in sorted(words))

def fetch(query):
    params = urllib.parse.urlencode({"search": query, "per-page": 100, "sort": "publication_date:desc"})
    req = urllib.request.Request("https://api.openalex.org/works?" + params,
        headers={"User-Agent": "VerityIndoorUAVResearch/1.1 (academic literature discovery)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response).get("results", [])

def main():
    data = json.loads(DB.read_text()) if DB.exists() else {"records": []}
    existing = {r.get("doi") or r.get("url") or r.get("title") for r in data.get("records", [])}
    added = 0
    for query in QUERIES:
        try: works = fetch(query)
        except Exception as exc:
            print(f"OpenAlex query failed ({query}): {exc}")
            continue
        for work in works:
            title = work.get("title") or ""
            abstract = abstract_from_inverted(work.get("abstract_inverted_index"))
            keywords = [k.get("display_name") for k in (work.get("keywords") or [])[:20]]
            venue = ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or "OpenAlex"
            doi = work.get("doi")
            url = doi or work.get("id") or ""
            searchable = " ".join([title, abstract, " ".join(keywords)])
            # Both UAV/drone terminology AND positive indoor evidence are mandatory.
            if not AIRCRAFT.search(searchable) or not INDOOR.search(searchable): continue
            key = doi or url or title
            if key in existing: continue
            data.setdefault("records", []).append({
                "title": title, "date": work.get("publication_date") or str(work.get("publication_year") or ""),
                "year": work.get("publication_year"), "keywords": keywords,
                "summary": abstract[:2200] or "Abstract not available in OpenAlex; review the source.",
                "url": url, "doi": doi, "source": venue,
                "indoor_evidence": INDOOR.findall(searchable)[:15],
                "screening_status": "Needs human review",
                "indoor_relevance": "Directly relevant" if DIRECT.search(searchable) else "Related indoor application"
            })
            existing.add(key); added += 1
        time.sleep(1)
    data["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data["screening_criteria"] = {
        "aircraft_required": "UAV, UAS, unmanned aerial vehicle/system, drone, or aerial robot",
        "indoor_required": "Indoor, warehouse, factory, enclosed facility, racking, or indoor navigation evidence",
        "outdoor_only": "Excluded",
        "review_note": "Automated screening is preliminary; verify each source and its indoor use before citing."
    }
    DB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} new indoor UAV records. Total records: {len(data.get('records', []))}")

if __name__ == "__main__": main()
