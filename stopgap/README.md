# Site-wide Head HTML and the departures stopgap

| File | What it is |
|---|---|
| `SEHE-head-html-REWRITE.txt` | The whole of Duda's **Head HTML** field (Site Settings → Head HTML), as published on 20 Sep 2026. It holds every tracking tag and the temporary hide-departures block. |
| `SEHE-hide-departures.txt` | The hide-departures block on its own, with a longer explanation. It is for reference only: the block is already inside the Head HTML above, so never paste it a second time. |

**Checked 1 Oct 2026:** the live site serves exactly this Head HTML (allowing for Duda's own re-formatting).

## What the Head HTML loads

| Tag | ID |
|---|---|
| Google Tag Manager | `GTM-TPSTZ264` |
| Google Analytics 4 | `G-GKR67569LP` |
| AdRoll | advertiser `E2XDEAS5ERHYVMCPAM3XX7`, pixel `V2TMPMEBHFGSHGD5DQQTZD` |
| Microsoft Clarity | `yefix0e9cy` |
| Trustpilot | the widget bootstrap, loaded once |

The file's header mentions "the note at the bottom about the second GA4 property"; that note was never added, so here it is, with the other tags the site loads from outside this field:

- **Duda injects its own GA4 property, `G-KESV7YYW1G`**, so two GA4 properties run side by side. Kirsty is to confirm which one the business reports from.
- **GTM tag 14 also configures `G-GKR67569LP`**, so page views may be counted twice. Check in GA4 DebugView.
- **Duda's Body End HTML** holds the Google Ads tag `AW-16523865426`, a Meta Pixel block with an empty ID, ActiveCampaign site tracking and tawk.to. The booking app uses its own Google Ads tag, `AW-18077303178`.

## Rules for editing the Head HTML

1. A paste **replaces the whole field**. Copy the whole file, from the downloaded file or GitHub's Raw view.
2. **No `<` and no `&` anywhere inside an inline script.** Duda escapes both in the head, which is why the AdRoll pixel never fired before 20 Sep 2026. Use `forEach` instead of `for` loops, and nested `if`s instead of `&&`.
3. **No `>` inside `<style>`** (repo rule 5).
4. After publishing, open the page source and check:
   - the header comment with `rewritten 20 Sep 2026` is there;
   - there is no `&lt;` or `&amp;` between that comment and `END temporary departure block`;
   - `s.adroll.com` and `clarity.ms` load (browser dev tools, Network tab).

## The temporary hide-departures block

**Why it's there.** Bookings moved from Checkfront to The Creator's booking app in September 2026, but the Worker's feed still reads Checkfront, so departure dates and counts can be wrong. On 18 Sep 2026 Kirsty asked for "Next departure" and "All departure dates" to be removed in the meantime.

**What it hides:**

- the "Next Departure" strips on every tour card;
- the "All departure dates" month lists (Journeys and the Brochure Collection);
- departure counts, such as "11 Departures" in the tour-page heroes;
- the homepage departure board and next-departure lines.

**What it keeps on purpose:** every sold-out marker (hiding those would make a sold-out tour look bookable), and all other content: prices, durations, routes, buttons and the booking app.

**Status on 1 Oct 2026: keep it.** The Worker's feed now marks every Winter 2027, Pinnacle 2027 and 2027/28 date as sold out, because Checkfront no longer offers them. This block is what stops those false labels from showing.

## Removing the block later

Only after the Worker reads the new booking app and its feed has been checked (`worker/README.md`):

1. In Duda, open Site Settings → Head HTML.
2. Delete everything from `<!-- ═══ TEMPORARY: hide unverifiable departure data` down to `<!-- ═══ END temporary departure block ═══ -->`, both lines included.
3. Publish. Check that the homepage, Journeys and one tour page show the right dates.
4. Make the same deletion in `SEHE-head-html-REWRITE.txt` and commit it, so this folder still matches the live site.
