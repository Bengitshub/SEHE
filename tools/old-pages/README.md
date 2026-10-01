# Old-design page builders (Sep 2026 rebuild)

These scripts generate the eight rebuilt page masters in the repo root:

| Builder | Master it writes |
|---|---|
| `build_reviews.py` | `SEHE-reviews-page_v7.txt` |
| `build_contact.py` | `SEHE-contact-page_v9.txt` |
| `build_about.py` | `SEHE-about-page_v7.txt` |
| `build_faq.py` | `SEHE-faq-page_v8.txt` |
| `build_gallery.py` | `SEHE-gallery-page_v7.txt` |
| `build_trust.py` | `SEHE-himalayan-trust-page_v5.txt` |
| `build_legal.py` | `SEHE-privacy-policy-page_v5.txt` and `SEHE-terms-page_v5.txt` |

The masters are what gets pasted into Duda (through `LATEST/`). The builders are
here so the masters can be rebuilt and checked, not because you must use them.

## Requirements

Python 3.9 or later. Standard library only; nothing to install.

## Rebuild and check (from the repo root)

```sh
python3 tools/old-pages/build_faq.py          # or any builder
git status                                     # the master must show no change
python3 tools/old-pages/verify.py SEHE-faq-page_v8.txt --verbatim-file tools/old-pages/out/verbatim-faq.txt
```

As of 1 Oct 2026, every builder rebuilds its master **byte for byte**, and
`verify.py` passes on all eight. The `verify.py` arguments per page:

| Master | Verbatim file | Extra flags |
|---|---|---|
| Reviews | `tools/old-pages/data/verbatim-reviews.txt` | `--allow-image-host=i.vimeocdn.com` |
| Contact | `tools/old-pages/data/verbatim-contact.txt` | |
| About | `tools/old-pages/out/verbatim-about.txt` | |
| FAQ | `tools/old-pages/out/verbatim-faq.txt` | |
| Gallery | `tools/old-pages/out/verbatim-gallery.txt` | |
| Himalayan Trust | `tools/old-pages/out/verbatim-trust.txt` | `--allow-amount=$3` (the Trust's own "$3 a day") |
| Privacy | `tools/old-pages/out/verbatim-privacy-policy.txt` | |
| Terms | `tools/old-pages/out/verbatim-terms-and-conditions.txt` | |

The `out/` files are written by the builders (git ignores the folder).

## What `verify.py` checks

- No `<` or `&` inside inline scripts, and **no `>` or `<` anywhere inside `<style>`**. Duda's publisher rewrites `>` as `&gt;`, and the browser then drops the whole CSS rule.
- No schema, no tracking code, and no departure data or Worker URL in these pages.
- No hard-coded TrustScore, rating or review count, and no extra Trustpilot bootstrap.
- Every image is on the Duda CDN and has alt text. Phone and email links are well-formed, and new-tab links carry `rel="noopener"`.
- No "small group" or "rail touring" wording, and no prices.
- Every CSS selector is scoped to the page's `.sehe-pg-…` wrapper.
- Every locked passage (reviews, FAQ answers, legal text, the Trust's words, photo titles) is present, word for word.

## Inputs

- **Live text** comes from the redacted snapshots in `backups/2026-09-25-old-pages/`. About also checks a few facts against the homepage and Journeys in `backups/2026-09-06-live-site/pages/`.
- **`data/`:**
  - the Duda widget data for the FAQ list, Gallery photos and About images, exported from the live pages;
  - `terms-edits.json`, Kirsty's approved Terms edits;
  - the hand-made checklists for Reviews and Contact.
- **Approved copy** (round 3, and Kirsty's 26 Sep answers) is written into the builders as constants, with comments saying where each piece came from.

## Changing a page

1. Edit the copy in the builder.
2. Bump the version, which means changing it in three places:
   - the `VERSION vN` line;
   - a new changelog entry;
   - the output filename (`SEHE-<page>_vN+1.txt`) and the `END OF FILE` line.
3. Run the builder, then `git rm` the old master.
4. Run `verify.py`.
5. Run `python3 tools/make-latest.py`.
6. Commit, then paste the new `LATEST/` file into Duda (see the runbook).

Locked wording (FAQ answers, legal text, reviews, the Trust's words, photo titles) changes only with written approval. Approved changes go in as explicit, checked edits:

- the FAQ: `ANSWER_EDITS` in `build_faq.py`;
- the Terms and Privacy: the `edits` lists in `build_legal.py` and `data/terms-edits.json`.

Each edit must match exactly once, and the build proves the result is the live text plus those edits and nothing else.

If someone edits a master by hand instead, the builder will no longer reproduce it. Either carry the change into the builder, or keep editing that master by hand from then on.
