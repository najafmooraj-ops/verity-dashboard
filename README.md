# Verity / MIT Indoor UAV Research Dashboard

## Scope
Indoor applications of unmanned aerial vehicles (UAVs) only. The collector treats **drone** as a common synonym for UAV and searches both. A record must contain an aerial-vehicle term and positive evidence of an indoor environment (e.g. indoor navigation, warehouse, distribution centre, factory, enclosed space, or racking inspection). Outdoor-only applications are excluded.

Automated screening is a first-pass relevance filter, not a substitute for human review. Each record displays the indoor evidence used to include it.

## Publish publicly
1. In Netlify, choose **Add new site → Import an existing project** and connect this GitHub repository.
2. Set the publish directory to `.`; no build command is needed.
3. Publish. Netlify provides the public URL.
4. Ensure GitHub Actions are enabled. The workflow runs daily at 10:15 UTC and can be run manually from Actions.

When new works are found, GitHub Actions commits `database.json`. That commit triggers Netlify to redeploy the public dashboard. Your computer does not need to be on.

## Local preview
Run `python3 -m http.server 8000` in this folder and open `http://localhost:8000/drone_research_dashboard.html`.

## Notes
- OpenAlex is the automated scholarly source. Google Scholar and Litmaps remain manual discovery sources.
- A public dashboard means records are publicly viewable. Do not add confidential sponsor data or private notes.
- The GitHub repository itself can be private while the Netlify website is public.
- Review the indoor evidence before citing a record; keyword screening can produce false positives and false negatives.
