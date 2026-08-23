#!/usr/bin/env python3
"""Performance Max campaign pack — /journeys. Single source of truth.

Every text asset lives HERE, is validated against Google's hard character
limits (len() — Google counts spaces), and the script emits:

    PMAX-CAMPAIGN.md   the full build sheet a human follows in Google Ads
    pmax-text-assets.csv   the text assets, one per row, for fast copy-paste

Copy rules honoured (Paul): "fully guided ... by rail & coach" (never bare
"rail touring" as the whole product), no "small groups", no exclamation
marks (Google disallows them in headlines), claims match the live site
(11-15 days, 4-star-plus hotels, most meals, WTA 2022-2025, April 2028
horizon). Re-run after any copy change: python3 build-campaign.py
"""
import csv
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))

FINAL_URL = 'https://siredmundhillaryexplorer.com/journeys'

# ---- text assets (limit, text) ----------------------------------------------
BUSINESS_NAME = 'Sir Ed Hillary Explorer'          # 25-char limit; full brand name is 27

HEADLINES = [  # 3-15 allowed, 30 chars max
    'Fully Guided NZ Rail Journeys',
    'The South Island by Rail',
    'Rail & Coach, Fully Guided',
    "NZ's Leading Tour Operator",
    'Compare All Seven Journeys',
    'Now Booking to April 2028',
    'TranzAlpine & Milford Sound',
    '11 to 15 Day Guided Tours',
    'Award-Winning NZ Tours',
    'Winter & Summer Departures',
    'Christchurch Departures',
    'Free Brochure Collection',
]

LONG_HEADLINES = [  # 1-5 allowed, 90 chars max
    'Seven fully guided South Island journeys by rail and coach, now booking to April 2028',
    "New Zealand's Leading Tour Operator 2022-2025 at the World Travel Awards",
    'The TranzAlpine, Milford Sound, Queenstown and Aoraki Mt Cook, fully guided',
    'Rail and coach touring for travellers who like their adventure comfortable',
    'Free brochure collection: itineraries, inclusions, pricing and departure dates',
]

DESCRIPTIONS_SHORT = [  # first description: 60 chars max
    'Fully guided South Island journeys by rail & coach.',
]
DESCRIPTIONS = [  # up to 4 more, 90 chars max
    'Seven journeys, 11 to 15 days, departing Christchurch. Compare them all on one page.',
    '4-star-plus hotels, rail, coach and most meals included. A team that answers the phone.',
    "World Travel Awards winner 2022-2025. Rated 'Excellent' on Trustpilot.",
    'Spring/summer and winter departures, now booking through to April 2028.',
]

SITELINKS = [  # text 25 max, each description 35 max
    ('14-Day Spring/Summer', 'Our signature journey', 'Milford, Queenstown & Aoraki'),
    ('Winter Editions', 'The Alps under deep snow', '12 days, Jul & Aug departures'),
    ('The Pinnacle Tour', 'Hosted by Peter Hillary', 'One departure, January 2027'),
    ('Brochure Collection', 'Every journey, free PDFs', 'Itineraries, pricing and dates'),
]

CALLOUTS = [  # 25 chars max
    'Fully Guided',
    '100% NZ Owned',
    '4-Star-Plus Hotels',
    'Most Meals Included',
    'Award-Winning Service',
    'Phone Us 7 Days',
]

SNIPPET_HEADER = 'Tours'
SNIPPETS = [  # 25 chars max each
    '14-Day Spring/Summer',
    '11-Day Spring/Summer',
    '12-Day Winter Edition',
    'The Pinnacle Tour',
]

SEARCH_THEMES = [  # up to 25
    'new zealand rail tours', 'south island train tours', 'tranzalpine tour package',
    'escorted tours new zealand', 'guided tours south island', 'new zealand coach tours',
    'milford sound tour from christchurch', 'queenstown rail tour', 'scenic train trips new zealand',
    'new zealand winter tours', 'senior tours new zealand', 'fully escorted nz holidays',
    'south island itinerary 14 days', 'luxury train tours new zealand', 'guided rail holidays',
    'new zealand tours for over 50s', 'aoraki mt cook tours', 'tekapo stargazing tour',
    'coastal pacific train tour', 'new zealand tour packages from australia',
]

IMAGES = {
    'Landscape 1.91:1 (1200x628)': ['sehe-journeys-a-land.jpg', 'sehe-journeys-b-land.jpg', 'sehe-journeys-c-land.jpg'],
    'Square 1:1 (1200x1200)':      ['sehe-journeys-a-sq.jpg', 'sehe-journeys-b-sq.jpg', 'sehe-journeys-c-sq.jpg'],
    'Portrait 4:5 (960x1200)':     ['sehe-journeys-a-port.jpg', 'sehe-journeys-b-port.jpg', 'sehe-journeys-c-port.jpg'],
    'Logo 1:1 (1200x1200)':        ['sehe-journeys-logo-1x1.png'],
    'Logo 4:1 (1200x300)':         ['sehe-journeys-logo-4x1.png'],
}

# ---- validation --------------------------------------------------------------
errors = []

def check(kind, text, limit):
    if len(text) > limit:
        errors.append(f'{kind} OVER by {len(text)-limit}: "{text}" ({len(text)}/{limit})')
    return f'{len(text):>2}/{limit}'

check('business name', BUSINESS_NAME, 25)
assert 3 <= len(HEADLINES) <= 15 and 1 <= len(LONG_HEADLINES) <= 5
assert len(DESCRIPTIONS_SHORT) == 1 and len(DESCRIPTIONS) <= 4
for t in HEADLINES: check('headline', t, 30)
for t in LONG_HEADLINES: check('long headline', t, 90)
for t in DESCRIPTIONS_SHORT: check('short description', t, 60)
for t in DESCRIPTIONS: check('description', t, 90)
for s, d1, d2 in SITELINKS:
    check('sitelink text', s, 25); check('sitelink d1', d1, 35); check('sitelink d2', d2, 35)
for t in CALLOUTS: check('callout', t, 25)
check('snippet header', SNIPPET_HEADER, 25)
for t in SNIPPETS: check('snippet', t, 25)
assert len(SEARCH_THEMES) <= 25
for t in HEADLINES + LONG_HEADLINES + DESCRIPTIONS_SHORT + DESCRIPTIONS:
    assert '!' not in t, f'exclamation mark (disallowed): {t}'
    assert 'small group' not in t.lower(), f'banned claim: {t}'
for f in [x for v in IMAGES.values() for x in v]:
    assert os.path.exists(os.path.join(HERE, '..', f)), f'missing image {f}'
if errors:
    print('\n'.join(errors)); raise SystemExit('CHARACTER LIMITS EXCEEDED')

# ---- emit the build sheet ----------------------------------------------------
def rows(items, limit):
    return '\n'.join(f'| `{t}` | {len(t)}/{limit} |' for t in items)

md = f'''# SEHE — Performance Max campaign: "PMax — Journeys"
_Generated {date.today().isoformat()} by `build-campaign.py`. Every count below is machine-checked._

**Final URL:** {FINAL_URL}

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

**Business name** — `{BUSINESS_NAME}` ({len(BUSINESS_NAME)}/25)
> The full name "Sir Edmund Hillary Explorer" is 27 characters and does not fit
> Google's 25-char field. If the Ads account has a verified business name that
> renders differently, prefer that.

### Headlines ({len(HEADLINES)} of 15)
| Text | Chars |
|---|---|
{rows(HEADLINES, 30)}

### Long headlines ({len(LONG_HEADLINES)} of 5)
| Text | Chars |
|---|---|
{rows(LONG_HEADLINES, 90)}

### Descriptions (first is the required short one)
| Text | Chars |
|---|---|
{rows(DESCRIPTIONS_SHORT, 60)}
{rows(DESCRIPTIONS, 90)}

### Images (from `creatives/google-journeys/`)
| Slot | Files |
|---|---|
''' + '\n'.join(f'| {k} | {", ".join(f"`{x}`" for x in v)} |' for k, v in IMAGES.items()) + f'''

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
''' + '\n'.join(
    f'| `{s}` ({len(s)}/25) | {d1} ({len(d1)}/35) | {d2} ({len(d2)}/35) | '
    + {'14-Day Spring/Summer': 'https://siredmundhillaryexplorer.com/2026-2027-spring/summer-tour-14-days',
       'Winter Editions': 'https://siredmundhillaryexplorer.com/2027-winter-edition-tours',
       'The Pinnacle Tour': 'https://siredmundhillaryexplorer.com/pinnacle-tour-2027',
       'Brochure Collection': 'https://siredmundhillaryexplorer.com/brochure-collection'}[s] + ' |'
    for s, d1, d2 in SITELINKS) + f'''

**Callouts:** ''' + ' · '.join(f'`{c}` ({len(c)})' for c in CALLOUTS) + f'''

**Structured snippet** — header `{SNIPPET_HEADER}`: ''' + ', '.join(f'`{s}`' for s in SNIPPETS) + f'''

**Call asset:** +64 3 974 1812 (call reporting ON)

## 5. Audience signal (signal, not targeting — PMax expands from it)
- **Search themes ({len(SEARCH_THEMES)} of 25):** ''' + ', '.join(SEARCH_THEMES) + '''
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
'''

open(os.path.join(HERE, 'PMAX-CAMPAIGN.md'), 'w', encoding='utf-8').write(md)

with open(os.path.join(HERE, 'pmax-text-assets.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['type', 'text', 'chars', 'limit'])
    w.writerow(['business_name', BUSINESS_NAME, len(BUSINESS_NAME), 25])
    for t in HEADLINES: w.writerow(['headline', t, len(t), 30])
    for t in LONG_HEADLINES: w.writerow(['long_headline', t, len(t), 90])
    for t in DESCRIPTIONS_SHORT: w.writerow(['description_short', t, len(t), 60])
    for t in DESCRIPTIONS: w.writerow(['description', t, len(t), 90])
    for s, d1, d2 in SITELINKS:
        w.writerow(['sitelink', s, len(s), 25]); w.writerow(['sitelink_desc', d1, len(d1), 35]); w.writerow(['sitelink_desc', d2, len(d2), 35])
    for t in CALLOUTS: w.writerow(['callout', t, len(t), 25])
    for t in SNIPPETS: w.writerow(['snippet', t, len(t), 25])
    for t in SEARCH_THEMES: w.writerow(['search_theme', t, len(t), ''])

print('ALL CHARACTER LIMITS PASS')
print(f'headlines {len(HEADLINES)}/15, long {len(LONG_HEADLINES)}/5, descriptions {1+len(DESCRIPTIONS)}/5, '
      f'sitelinks {len(SITELINKS)}, callouts {len(CALLOUTS)}, snippets {len(SNIPPETS)}, themes {len(SEARCH_THEMES)}/25')
print('wrote PMAX-CAMPAIGN.md + pmax-text-assets.csv')
