# SEHE — Performance Max campaign: "PMax — Journeys"
_Generated 2026-08-23 by `build-campaign.py`. Every count below is machine-checked._

**Final URL:** https://siredmundhillaryexplorer.com/journeys

## 1. Campaign settings
| Setting | Value | Why |
|---|---|---|
| Objective | Leads | Brochure form + phone are the site's conversion paths |
| Campaign type | Performance Max | — |
| Bidding | **Maximise conversions** (no target CPA at launch) | Let it learn first; add tCPA after ~30 conversions |
| Budget | **NZ$70/day** to start (raise once conversion data flows) | PMax wants roughly 3x expected cost-per-lead of headroom |
| Locations | New Zealand + Australia (Presence: people IN the targets) | Matches guest base; add US/UK/CA as a second campaign later |
| Language | English | — |
| **Final URL expansion** | **OFF** | The whole point is landing on /journeys; expansion would scatter traffic (and can surface /v2 or /home-old) |
| Auto-tagging | ON (account level) | — |
| Final URL suffix | `utm_source=google&utm_medium=cpc&utm_campaign=pmax_journeys` | Lands in the Phase-2 lead-capture UTM fields when enabled |

## 2. Conversion tracking — set up BEFORE launch
1. **Brochure lead (primary).** In GA4 on the Duda site: mark a page-view of
   `/brochure-collection` *arriving from a journey/tour/homepage form* as key event
   `brochure_lead` (simplest robust proxy: destination page-view key event), then
   **import it into Google Ads** as a primary conversion.
2. **Phone call (primary).** Google Ads call asset on +64 3 974 1812 with call
   reporting ON (60s threshold), plus GA4 `tel:` click event imported as secondary.
3. **Booking (secondary, value).** Checkfront booking-complete → GA4 purchase event
   (Checkfront's GA integration), imported with value. Keep secondary until volume proves it.

## 3. Asset group: "Journeys — All" (one group at launch)
One asset group concentrates learning. Split (Winter / Spring-Summer / Pinnacle)
only after conversions flow.

**Business name** — `Sir Ed Hillary Explorer` (23/25)
> The full name "Sir Edmund Hillary Explorer" is 27 characters and does not fit
> Google's 25-char field. If the Ads account has a verified business name that
> renders differently, prefer that.

### Headlines (12 of 15)
| Text | Chars |
|---|---|
| `Fully Guided NZ Rail Journeys` | 29/30 |
| `The South Island by Rail` | 24/30 |
| `Rail & Coach, Fully Guided` | 26/30 |
| `NZ's Leading Tour Operator` | 26/30 |
| `Compare All Seven Journeys` | 26/30 |
| `Now Booking to April 2028` | 25/30 |
| `TranzAlpine & Milford Sound` | 27/30 |
| `11 to 15 Day Guided Tours` | 25/30 |
| `Award-Winning NZ Tours` | 22/30 |
| `Winter & Summer Departures` | 26/30 |
| `Christchurch Departures` | 23/30 |
| `Free Brochure Collection` | 24/30 |

### Long headlines (5 of 5)
| Text | Chars |
|---|---|
| `Seven fully guided South Island journeys by rail and coach, now booking to April 2028` | 85/90 |
| `New Zealand's Leading Tour Operator 2022-2025 at the World Travel Awards` | 72/90 |
| `The TranzAlpine, Milford Sound, Queenstown and Aoraki Mt Cook, fully guided` | 75/90 |
| `Rail and coach touring for travellers who like their adventure comfortable` | 74/90 |
| `Free brochure collection: itineraries, inclusions, pricing and departure dates` | 78/90 |

### Descriptions (first is the required short one)
| Text | Chars |
|---|---|
| `Fully guided South Island journeys by rail & coach.` | 51/60 |
| `Seven journeys, 11 to 15 days, departing Christchurch. Compare them all on one page.` | 84/90 |
| `4-star-plus hotels, rail, coach and most meals included. A team that answers the phone.` | 87/90 |
| `World Travel Awards winner 2022-2025. Rated 'Excellent' on Trustpilot.` | 70/90 |
| `Spring/summer and winter departures, now booking through to April 2028.` | 71/90 |

### Images (from `creatives/google-journeys/`)
| Slot | Files |
|---|---|
| Landscape 1.91:1 (1200x628) | `sehe-journeys-a-land.jpg`, `sehe-journeys-b-land.jpg`, `sehe-journeys-c-land.jpg` |
| Square 1:1 (1200x1200) | `sehe-journeys-a-sq.jpg`, `sehe-journeys-b-sq.jpg`, `sehe-journeys-c-sq.jpg` |
| Portrait 4:5 (960x1200) | `sehe-journeys-a-port.jpg`, `sehe-journeys-b-port.jpg`, `sehe-journeys-c-port.jpg` |
| Logo 1:1 (1200x1200) | `sehe-journeys-logo-1x1.png` |
| Logo 4:1 (1200x300) | `sehe-journeys-logo-4x1.png` |

### Video
None yet — **upload a 15-60s cut of the site film to the SEHE YouTube channel**
and attach it; until then Google auto-generates slideshows from the images
(acceptable, not great). The site's Vimeo film (1046997096) is the source; a
horizontal 30s cut + a 15s vertical cut cover PMax and Demand Gen both.

### Call to action
`Learn more` (best fit for a comparison landing page; "Book now" overpromises the click).

## 4. Assets (extensions)
**Sitelinks** (all four required surfaces)
| Text | Desc 1 | Desc 2 | Final URL |
|---|---|---|---|
| `14-Day Spring/Summer` (20/25) | Our signature journey (21/35) | Milford, Queenstown & Aoraki (28/35) | https://siredmundhillaryexplorer.com/2026-2027-spring/summer-tour-14-days |
| `Winter Editions` (15/25) | The Alps under deep snow (24/35) | 12 days, Jul & Aug departures (29/35) | https://siredmundhillaryexplorer.com/2027-winter-edition-tours |
| `The Pinnacle Tour` (17/25) | Hosted by Peter Hillary (23/35) | One departure, January 2027 (27/35) | https://siredmundhillaryexplorer.com/pinnacle-tour-2027 |
| `Brochure Collection` (19/25) | Every journey, free PDFs (24/35) | Itineraries, pricing and dates (30/35) | https://siredmundhillaryexplorer.com/brochure-collection |

**Callouts:** `Fully Guided` (12) · `100% NZ Owned` (13) · `4-Star-Plus Hotels` (18) · `Most Meals Included` (19) · `Award-Winning Service` (21) · `Phone Us 7 Days` (15)

**Structured snippet** — header `Tours`: `14-Day Spring/Summer`, `11-Day Spring/Summer`, `12-Day Winter Edition`, `The Pinnacle Tour`

**Call asset:** +64 3 974 1812 (call reporting ON)

## 5. Audience signal (signal, not targeting — PMax expands from it)
- **Search themes (20 of 25):** new zealand rail tours, south island train tours, tranzalpine tour package, escorted tours new zealand, guided tours south island, new zealand coach tours, milford sound tour from christchurch, queenstown rail tour, scenic train trips new zealand, new zealand winter tours, senior tours new zealand, fully escorted nz holidays, south island itinerary 14 days, luxury train tours new zealand, guided rail holidays, new zealand tours for over 50s, aoraki mt cook tours, tekapo stargazing tour, coastal pacific train tour, new zealand tour packages from australia
- **Your data:** brochure-lead list + site visitors (add the GA4/Ads remarketing tag list when available)
- **Interests/in-market:** Escorted tours, Rail travel, New Zealand travel, Luxury travel
- **Demographics:** 45+ skew (do NOT hard-exclude under-45 — signal only; PMax decides)

## 6. Exclusions & hygiene
- Brand exclusions: add "sir edmund hillary explorer" brand list if brand search
  is (or becomes) its own campaign; otherwise PMax will absorb cheap brand clicks
  and flatter its own numbers.
- Account negatives: jobs, everest, "hillary clinton", school/college names.
- Placement exclusions: review the placement report weekly for the first month.

## 7. Launch checklist
1. Conversion actions live and firing (section 2) — test the brochure form end-to-end.
2. Upload the 11 image/logo assets; paste text assets (use `pmax-text-assets.csv`).
3. Final URL expansion OFF; URL suffix set; locations/language set.
4. Call asset verified; sitelinks/callouts/snippets attached.
5. YouTube video uploaded and attached (or accept auto-gen for week 1).
6. Confirm WTA + Trustpilot marks are cleared for paid use (concept C runs them).
7. Launch Mon-Tue morning NZT; leave untouched for 2 weeks (learning phase) apart
   from placement-report checks; first judgement at 30 days / ~30 conversions.

## 8. Refresh cadence
- Concept B images carry real dates (16 Nov 2026 / 30 Nov 2026 / 10 Jul 2027):
  regenerate via `creatives/google-journeys/build.py` when one passes or sells out.
- "April 2028" horizon (headline + long headline + description + images) holds
  until the 2028/29 season releases — then regenerate everything in one pass.
