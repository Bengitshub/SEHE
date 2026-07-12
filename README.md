# SEHE — Sir Edmund Hillary Explorer website build

Working repository for the Sir Edmund Hillary Explorer (Pounamu Tourism Group)
tour-page rebuild: seven self-contained HTML landing pages, a Journeys index,
a homepage, per-page booking widgets, a Cloudflare Worker that feeds live
departure availability from Checkfront, and the switch-over / lead-capture kits.

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
