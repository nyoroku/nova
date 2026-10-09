# Nova production release — 9 October 2026

The activities release is live at [Nova boat rides](https://www.novaboatridesnaivasha.co.ke/boat-rides/).

Application commit: `d2ce3537517ae6dd9cc36dd88723126bee7992a1`, pushed to both `main` and `codex/nova-activities` in [nyoroku/nova](https://github.com/nyoroku/nova/commit/d2ce3537517ae6dd9cc36dd88723126bee7992a1). This report and the implementation status were updated after the application release.

## Release

- PythonAnywhere account: `novaboats`; web app: `www.novaboatridesnaivasha.co.ke`.
- Application directory: `/home/novaboats/nova`; existing Python 3.12 virtual environment retained. Its Django runtime is 6.1.1.
- The server could not resolve GitHub's hostname. An incremental Git bundle containing the already-pushed commits was uploaded using PythonAnywhere's authenticated API, verified against the existing repository, and used for a fast-forward update. No credentials were placed in the bundle or repository.
- Thirteen migrations applied successfully to the existing live SQLite database. The local database was not uploaded.
- Existing activity photos were optimized and static assets collected. Existing `/static/` and `/media/` mappings were retained.
- Production debug mode was disabled using a server-only `.env` file. The existing HTTPS setting was retained. The web app reloaded successfully.

## Preservation and verification

- All four pre-release enquiries are still present, with every original stored field unchanged.
- Nineteen rates and five external-fee records remain. The catalogue now has ten activities and ten booking options: eight activities public, two drafts.
- All 51 automated Django tests passed on the server, with no system-check issues or pending migrations.
- Eighteen live routes returned HTTP 200, including all eight public activity pages, the enquiry page, price hub, service hub and sitemap. HTML pages each have one H1 and valid JSON-LD.
- Both draft activity URLs return HTTP 404 and are excluded from the sitemap.
- The private 60-minute option returns KES 4,500 for three adults. The selected option, party size and date carry into the enquiry form.
- The checked page's local static and media assets returned HTTP 200. Browser verification confirmed eight catalogue cards, no broken loaded images, and no horizontal overflow at the mobile viewport.
- No synthetic enquiry was submitted to the live database. Lead submission and idempotency were verified by automated tests.

## Recovery material

Backups are retained outside the served application at `/home/novaboats/nova-activity-release-20261009/backup/`:

- `db.sqlite3`: consistent pre-migration SQLite backup.
- `application-and-media.tar.gz`: pre-release code, configuration and media.
- `repository.bundle`: pre-release Git history.
- `working-tree-status.txt`: inventory of pre-release manual edits.

The old manually modified checkout was also preserved in a Git stash named `Nova pre-activities deployment 2026-10-09`. Full database rollback requires the backup and care to retain any enquiries received after release; reversing schema changes alone is insufficient for the data migrations.

## Remaining product work

Sunrise and Full Lake Explorer need verified operating facts and photos before publication. Existing activities still need the editorial/operational verification and gallery completion listed in `NOVA_ACTIVITY_FACT_MATRIX.md` and the Google readiness export. Google activity submission, live analytics configuration, real-device checks and field Core Web Vitals remain separate unfinished work. No paid provider or Google listing was activated by this release.
