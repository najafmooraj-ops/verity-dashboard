#!/usr/bin/env python3
"""Refresh the indoor UAV evidence base from OpenAlex."""
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

DB = Path("database.json")
QUERIES = [
    '"indoor drone" warehouse',
    '"UAV" indoor warehouse inspection',
    '"drone" racking inspection',
    '"indoor UAV" industrial inspection',
    '"drone" indoor navigation inventory',
]
AIRCRAFT = re.compile(r"\b(drone|uav|unmanned aerial|aerial robot)\b", re.I)
INDOOR = re.compile(r"\b(indoor|warehouse|distribution cent(?:re|er)|factory|manufacturing|enclosed|racking|rack inspection|gps-denied|indoor navigation)\b", re.I)
DIRECT = re.compile(r"warehouse|racking|rack inspection|inventory|distribution cent(?:re|er)", re.I)

def abstract_from_inverted(inv):
    if not inv:
        return ""
    words = {}
    for word, positions in inv.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words[k] for k in sorted(words))

def fetch(query):
    params = urllib.parse.urlencode({"search": query, "per-page": 50, "sort": "publication_date:desc"})
    url = "https://api.openalex.org/works?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "VerityIndoorUAVResearch/1.0 (academic literature discovery)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response).get("results", [])

def main():
    data = json.loads(DB.read_text()) if DB.exists() else {"records": []}
    existing = {r.get("doi") or r.get("url") or r.get("title") for r in data.get("records", [])}
    added = 0
    for query in QUERIES:
        try:
            works = fetch(query)
        except Exception as exc:
            print(f"OpenAlex query failed ({query}): {exc}")
            continue
        for work in works:
            title = work.get("title") or ""
            abstract = abstract_from_inverted(work.get("abstract_inverted_index"))
            venue = ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or "OpenAlex"
            doi = work.get("doi")
            url = doi or work.get("id") or ""
            text = " ".join([title, abstract])
            if not AIRCRAFT.search(text) or not INDOOR.search(text):
                continue
            key = doi or url or title
            if key in existing:
                continue
            data.setdefault("records", []).append({
                "title": title,
                "date": work.get("publication_date") or str(work.get("publication_year") or ""),
                "year": work.get("publication_year"),
                "keywords": [k.get("display_name") for k in (work.get("keywords") or [])[:12]],
                "summary": abstract[:1600] or "Abstract not available in OpenAlex; review the source.",
                "url": url,
                "doi": doi,
                "source": venue,
                "indoor_evidence": INDOOR.findall(text)[:12],
                "screening_status": "Needs human review",
                "indoor_relevance": "Directly relevant" if DIRECT.search(text) else "Related indoor application",
            })
            existing.add(key)
            added += 1
        time.sleep(1)
    data["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    DB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(f"Added {added} new indoor UAV records. Total records: {len(data.get('records', []))}")

if __name__ == "__main__":
    main()
