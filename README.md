# SEHE — Sir Edmund Hillary Explorer website build

Working repository for the Sir Edmund Hillary Explorer (Pounamu Tourism Group)
site rebuild: seven self-contained HTML tour pages, the Journeys index, the
homepage, the brochure-collection page, per-page booking widgets, a Cloudflare
Worker that feeds live departure availability from Checkfront (plus a new-item
watchdog), and the switch-over / lead-capture kits.

## Current state (31 Jul 2026)
All pages LIVE on their real URLs, homepage included (root domain).
`LATEST/` holds every paste-ready deliverable under a STABLE filename —
Ben pastes only from there (`tools/make-latest.py` regenerates it).

| Page | Master file | Notes |
|---|---|---|
| Homepage (/) | `SEHE-homepage_v33.txt` | departure board + brochure-collection band; v33 on /v2 for testing; old homepage parked at /home-old (noindex) |
| Journeys | `SEHE-journeys-page_v22.txt` | single-widget page (hero + FAQ + contact folded in) |
| Brochure collection | `SEHE-brochure-collection_v2.txt` | single main widget; stale tablet duplicate deleted |
| 7 tour pages | `SEHE-*-tour_v*.txt` (one per page) | pasted as Block A + native Duda form + Block B — see `switchover/` |

- Tour pages carry the Checkfront split-item fix (`302,374` / `289,392`) and
  the static 5-star Trustpilot strip (Ben's call, 4.7-TrustScore facts noted
  in the changelogs). Winter 2026 is sold out and presented as such.
- `worker/sehe-worker_LIVE-auto.js` is the paste-ready Worker
  (`sehe-next-departures` on Cloudflare — same single worker for the feed,
  `/lead`, `/items-audit`). `worker/worker.js` is identical plus test exports;
  `node worker/worker.test.mjs` must stay green (48 tests).
- `tools/make-blocks.py` regenerates the Block A/B pairs from the masters
  (byte-verified split; Block A swaps the HTML form for the docking note).
- Phase 2 (direct lead capture + UTM persistence) is built and parked:
  `leadform/ENABLE-DIRECT-LEADS.md`.

## Rules of the road
1. Bump the version on every change (filename + header + changelog).
2. Every render is enhance-only: missing data must never wipe baked HTML.
3. Never let `<` touch a word inside inline scripts (Duda's publisher strips
   tag-like tokens and corrupts the block).
4. Secrets (Checkfront, Zapier hooks) live only in Cloudflare Worker secrets.

## History note (12 Jul 2026)
The original session history (~100 commits, 9 Jun–8 Jul 2026) lived only in an
ephemeral container and was lost when it recycled; the GitHub remote had never
received a successful push (write access was blocked). Rebuilt from Ben's
re-uploaded masters, cross-checked against the published preview pages. The
authoritative deliverables also exist in Ben's chat downloads.

Resolved same day: the Claude GitHub App is now installed on the repo, pushes
work, and this GitHub repository is the durable record going forward — every
change is committed and pushed immediately.
