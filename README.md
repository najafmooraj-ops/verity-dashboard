# Verity × MIT — Indoor UAV Research Dashboard

A public-facing research dashboard focused on indoor UAV (unmanned aerial vehicle) and drone applications in warehouses and industrial facilities.

## Scope and screening
The collector searches both **drone** and **UAV** terminology. Records need an aircraft term and positive indoor-context evidence (for example, indoor navigation, warehouse, factory, enclosed space, or racking inspection). Outdoor-only applications are excluded from the visible research library. Automated keyword screening is a first-pass filter, not a substitute for human review.

## Files
- `index.html`: responsive dashboard and searchable indoor research library
- `database.json`: literature records shown by the dashboard
- `drone_scraper.py`: OpenAlex literature collector
- `.github/workflows/refresh-literature.yml`: scheduled refresh workflow
- `netlify.toml`: Netlify publish configuration

## Automatic refresh
GitHub Actions runs daily at 10:15 UTC (and can be run manually from the Actions tab). The workflow queries OpenAlex, screens for indoor UAV context, and commits new records to `database.json`. A Netlify site connected to this repository will redeploy after each database commit.

## Publish with Netlify
1. In Netlify, select **Add new site → Import an existing project**.
2. Connect GitHub and select `najafmooraj-ops/verity-dashboard`.
3. Leave the build command blank and use `.` as the publish directory.
4. Deploy. Netlify will provide a public site URL.

## Local preview
Run `python3 -m http.server 8000` from the repository root and open `http://localhost:8000`.

## Important notes
- The current seed database contains one clearly indoor warehouse/racking record. The previously discussed 73-record local database has not yet been uploaded; upload the latest `database.json` to restore and re-screen that fuller collection.
- Google Scholar and Litmaps remain useful complementary manual discovery sources; this automated collector currently uses OpenAlex.
- Review the source and indoor evidence before citing a study. Keyword screening can produce false positives and false negatives.
- This repository is currently **public**. Do not commit confidential sponsor information or private notes. If you want the source private, change repository visibility in GitHub Settings before connecting Netlify.
