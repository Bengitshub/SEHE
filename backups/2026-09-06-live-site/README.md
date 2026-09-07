# Live-site hardcopy — 2026-09-07 01:56 UTC

Frozen backup of siredmundhillaryexplorer.com taken from the OUTSIDE (fetched
as a browser would) at the moment stamped above. Nothing in this folder is
ever edited; a new backup gets a new dated folder. The git tag
`backup-2026-09-06-live` pins this exact commit forever.

| Folder | Contents |
|---|---|
| `pages/` | The full HTML of every page exactly as Duda served it (page shell + our widgets + Duda runtime). One file per URL. |
| `widgets/` | Just the SEHE widget code from each page (what you would paste into a Duda HTML widget to rebuild it). |
| `paste-sources/` | The clean paste-ready sources (`LATEST/`) as they stood at this moment. |
| `worker/` | The Cloudflare Worker code as deployed. |

## State captured
- Homepage root v27 (v38 on /v2, noindex); Journeys v22; Brochure Collection v2.
- Tour pages: Block A v21/v20/v23/v13/v13/v24/v15; Block B v28/v26/-/v19/v19/v30/v21.
- Booking: **Checkfront widget** on six tour pages; **new-app embed** on Winter 2026.

## Restore any page
Paste the matching file from `widgets/` (tour pages: widget 1 = Block A,
widget 2 = Block B, with the native Duda brochure form row between them) or
the clean source from `paste-sources/`. Secrets (Checkfront key, Zapier
hooks) are not in this repo; they live only in Cloudflare Worker settings.

## Redaction note
Duda's runtime ships a Mapbox token (`rtCommonProps["common.mapbox.token"]`, Duda's own, for its map widgets) on every page; GitHub's secret scanner flags it, so it is replaced with `pk.REDACTED-DUDA-MAPBOX-TOKEN` in `pages/`. It is not part of the SEHE widget code and is not needed to restore any page.
