# Old-design pages rebuild: runbook (25 Sep 2026, updated after round-2 feedback and the Contact v8 fix)

This runbook covers eight rebuilt pages: Reviews, Contact, About, FAQ, Gallery, Himalayan Trust, Privacy Policy and Terms & Conditions.

- **Paste files:** always paste from `LATEST/`. They are regenerated with `python3 tools/make-latest.py`.
- **Masters:** one per page in the repo root:
  - `SEHE-reviews-page_v6.txt`
  - `SEHE-contact-page_v8.txt`
  - `SEHE-gallery-page_v6.txt`
  - `SEHE-about-page_v5.txt`
  - `SEHE-faq-page_v6.txt`
  - `SEHE-himalayan-trust-page_v5.txt`
  - `SEHE-privacy-policy-page_v3.txt`
  - `SEHE-terms-page_v3.txt`
- **Before snapshot:** the served HTML of every old page, from 25 Sep 2026, is in `backups/2026-09-25-old-pages/`.
- **Draft emails:** for Kirsty and Paul, in `notes/2026-09-25-emails.md`.

## Start here (if you are new to this project)

**What this is.** Eight old pages on siredmundhillaryexplorer.com (a Duda site) have new designs. Each page's code is ready to paste. Nothing is live yet.

- **Plan:** each page is built on a hidden copy first (`<slug>-new`) and published so Kirsty can preview it. It replaces the live page only after she approves.

**Who does what.**

| Person | Role |
|---|---|
| Ben | Builds Phase 1 (Reviews, Contact). Contract ends **31 Oct 2026**. |
| The Creator (Izaac and Joel) | May build Phase 2 (About, FAQ, Gallery, Himalayan Trust, Privacy, Terms). They also have their own work in the same Duda editor (see rule 3 in §0). |
| Kirsty | Approves every page before it goes live. Answers the content questions in §7. |
| Paul | Owns the legal and policy wording: Privacy, Terms, and FAQ payment and cancellation. |

**You need:**

- Duda editor access;
- this repo (or just the `LATEST/` folder);
- about 20–30 minutes per page.

No coding is needed. You paste whole files into Duda HTML widgets.

**The flow for every page:**

1. Duplicate → `-new`.
2. Hide it from the menu.
3. Paste.
4. Check with Izaac and Joel, then publish.
5. Send Kirsty the preview link.
6. After her OK, swap.

**About has one extra gate.** Its itinerary claims (A1 to A3 in §7) must be confirmed, qualified or removed **before `about-new` is published at all**, even as a preview. See Phase 2.

The details are in §0 to §4.

**Changing a page's content later.** Edit the page's master in the repo root, never `LATEST/`:

1. Bump the version in the file name, the header and the changelog.
2. Run `python3 tools/make-latest.py`.
3. Commit and push.

**House rules for the code** (README "Rules of the road"):

- No `<` or `&` inside inline `<script>` blocks, because Duda's publisher escapes them.
- **No `>` anywhere inside `<style>`, comments included** (found 25 Sep on the live `/reviews-new`). Duda publishes it as `&gt;`, and the browser then silently drops the whole rule. Write `.a .b`, never `.a > .b` or `:has(> …)`.
- **Only use markup already working in this site's Duda widgets.** Contact v7's definition list (`dl`/`dt`/`dd`) was the one tag set no working page used, and v7 vanished in the editor. `verify.py` now fails on both of these.
- Scripts only add to the page.
- All CSS stays under the page's `.sehe-pg-…` class.

## First manual fix: two tour pages are hidden from Google

Two tour pages are served with `<meta name="robots" content="noindex">`:

- `/2026-2027-spring/summer-tour-14-days` (14-Day 2026/27)
- `/2026-2027-spring/summer-tour-11-day-tours` (11-Day 2026/27)

They already had it in the 6 Sep backup (`backups/2026-09-06-live-site/pages/`), so they have probably been out of Google since the July switch-over. They are also missing from `/sitemap.xml`. These are main tour pages and PMax sitelink destinations.

1. In Duda, open each page, go to **Page settings → SEO**, and turn **"Hide from search engines" off**.
2. Check with Izaac and Joel (rule 3 in §0), then **Publish**.
3. In **Google Search Console → URL Inspection**, paste each full URL and click **Request indexing**.
4. Open https://www.siredmundhillaryexplorer.com/sitemap.xml and check both URLs are now listed.

**Leave `/brochure-collection` on noindex.** That is deliberate; see §6.

## Go-live plan: two phases, Kirsty previews first

**Phase 1: Reviews and Contact (Ben).**

Status 25 Sep: `reviews-new` and `about-new` are built and published. `reviews-new` needs **v6 pasted over v5** (the "Show 6 more reviews" fix, §3). `contact-new` needs **v8** (§3).

1. Build `reviews-new` and `contact-new` (§1 and §3). **Hide both from the menu.**
2. Check with Izaac and Joel that nothing of theirs is pending, then publish.
3. Email Kirsty the two preview links (draft in `notes/2026-09-25-emails.md`).
4. **Kirsty must not submit the contact form on the preview.** The form on `contact-new` is live (rule 7 in §0).
   - Alternative: agree **one** test submission on `contact-new` as the end-to-end test, and write down the date and time. Everyone then ignores that one conversion and inbox message.
5. When Kirsty approves, swap each page (§2). **Nothing is swapped before she approves.**

**Phase 2: About, FAQ, Gallery, Himalayan Trust, Privacy and Terms (Ben, or The Creator after 31 Oct).**

- The steps are the same as Phase 1: build `-new`, hide it from the menu, check with Izaac and Joel, publish, send Kirsty the preview links, and swap after she approves.
- **About is gated.** Do not publish `about-new` until Kirsty has answered A1 to A3 in §7: the Antarctic Centre visit, Marlborough, and the Hillary family guest speaker.
  - **Confirmed for every tour:** keep the sentence.
  - **True only for some tours:** qualify it in Kirsty's words.
  - **Not true, or no answer:** delete the sentence.

  §7 lists the exact sentences. Make the edits (see "Changing a page's content later"), then publish the preview and send it to Kirsty.
- **Her other questions don't block anything:** A4 (an updated route map), Gallery G2 to G4 (photo titles, the Milford spelling, photos of places no current tour visits) and FAQ F8 (hygiene). Those pages can go live, and the answers become small edits later.
- **Privacy and Terms.** The new pages carry the **current** wording exactly. If Paul changes any wording, edit the text inside `<div class="lg-doc">` in that page's HTML widget, and update the master to match. Never paste old wording back.

## 0. Rules for every page

1. **Build on a copy.** Duplicate the live page and name the copy `<slug>-new`. The live page stays untouched until the swap.
2. **Hide the copy from the menu.** Duda can add a duplicated page to the navigation. After duplicating, open the copy's **page settings** and hide it from navigation. Check the header menu **and** the footer menu.
3. **Publishing publishes everything.** In Duda, Publish pushes **every** pending edit on the site, not just your page.
   - **Before every publish:** check with Izaac and Joel that none of their unpublished work is sitting in the editor.
   - **Before touching Body End or the global header (§5):** tell them first.
4. **What a preview is.** A published `-new` page is noindex (Duda's default for new pages) and hidden from the menu, but anyone with the link can open it.
5. **Never create a redirect from `/<slug>` to `/<slug>-old`.** After renaming, open **Site Settings → URL Redirects** and delete any rule whose source is `/<slug>`. Duda may add one automatically when a page URL changes.
6. **Contact: copy the form, never move it.** Duplicating the page gives `contact-new` its own copy of the form. The original page, which becomes `contact-old`, keeps its form, so rollback stays possible.
7. **The form on `contact-new` is live.** A submission there:
   - reaches Kirsty's inbox and the Zapier lead Zap;
   - counts as the **"Contact Us Form Submitted"** conversion. GTM matches any URL containing `/contact`, and `/contact-new` contains it.

   So don't test it unless a test is agreed (see Phase 1).
8. **Removing noindex at the swap is a launch blocker**, except for Himalayan Trust, Privacy and Terms, which are noindex today (see §4).

## 1. The row every single-widget page needs

In the `-new` page:

1. Delete **every content row**. Leave the global header and footer alone.
2. Add an empty **1-column row** and set it to:
   - Full width: on.
   - Padding top and bottom: **0**.
   - Background: none.
3. Drag in an **HTML** widget, click **Edit HTML**, paste the whole `LATEST/<file>`, then click **Update**.

The CSS also sets the row padding to 0 in modern browsers. The editor setting covers older browsers. Duda's theme otherwise pads every row 120px top and bottom on desktop.

## 2. Preview, approval and swap

**Preview.**

1. Check with Izaac and Joel (rule 3), then **Publish**.
2. Open `https://www.siredmundhillaryexplorer.com/<slug>-new` on a phone and a desktop.
3. Send Kirsty the link.

**Swap. Only after Kirsty approves.**

1. **Old page → Page settings.**
   - Change the URL from `<slug>` to `<slug>-old`.
   - Turn **Hide from search engines** on.
   - Hide it from the navigation.
2. **Site Settings → URL Redirects.** Delete any rule from `/<slug>`.
3. **New page → Page settings.**
   - Change the URL from `<slug>-new` to `<slug>`.
   - Paste the SEO title and description from the table in §4.
   - Set **Hide from search engines**: **off** for Reviews, Contact, About, FAQ and Gallery. Keep it **on** for Himalayan Trust, Privacy and Terms.
4. **Site Navigation.** Duda menu items point to *pages*, not URLs, so the menu still points at the old page after the rename. In **both** the header and footer menus, show the new page in the old page's position with the same label.
5. **Publish** (after checking with Izaac and Joel). Then check the live URL on a phone and a desktop:
   - the menu link and the footer link;
   - that no redirect is in place (the URL stays `/<slug>`).

**Rollback** is the same steps in reverse:

1. New page → `<slug>-new`, with noindex on.
2. Old page → `<slug>`, with noindex off where it was indexed.
3. Restore the menus.
4. Delete any redirect from `/<slug>`.
5. Publish.

The old page is untouched throughout, so rollback takes about two minutes.

## 3. Page by page

### Reviews (`/reviews`): `LATEST/reviews-page.txt`

**Build.** Use the §1 row. **After publishing `/reviews-new`, check:**

- The Trustpilot Micro Combo shows in the hero. If it doesn't, the plain "Read our reviews on Trustpilot" link shows instead.
- **Show 6 more reviews** is a white button with a navy border and a **+**. Clicked, it opens, the + becomes **−**, and the label reads **Show fewer reviews**. (v5 showed it as plain text on the live page; v6 fixes that, so re-paste v6 into the same widget if `reviews-new` still has v5.)
- **The guest video.** It shows a poster with a play button and the title. Click it: the Vimeo player loads and should start. Vimeo blocks automated checks, so actual playback could not be tested here. Without JavaScript, or if Vimeo is blocked, the poster is a plain link to the video on Vimeo.

**The 12 selected reviews.** They come from the public Trustpilot profile on 25 Sep 2026, newest first, from Louise H. (Sep 2026) to David (Mar 2026). All are 5-star. The first 6 show and 6 sit behind "Show more".

- They are verbatim. Cuts are at whole sentences, marked "…". The month shown is the month the review was **posted** on Trustpilot.
- The brief's original set was a May snapshot; about 16 reviews are newer than it.

**To refresh the selected reviews later:**

1. Copy the reviews verbatim, cut only at whole sentences, and mark cuts with "…".
2. Keep name, country and the posting month.
3. Edit `TP` in the master, bump the version, then run `tools/make-latest.py`.

**Trustpilot plan.** The public profile shows **"Paid Trustpilot subscription"**. But on 25 Sep, Trustpilot's widget service answered "BusinessUnit does not have access to that trustbox" for the review-list TrustBoxes: Carousel, Slider, List and Grid. Only Micro, Mini, Starter and Review Collector worked.

- The Carousel may just need enabling in **Trustpilot Business → TrustBox library**, or it may need a higher tier.
- **Whoever holds the Trustpilot login should check this before anyone pays for an upgrade.**
- If a Carousel becomes available, its "Get code" snippet (business unit `67af6f95db89fc000f855205`) could show new reviews automatically.
- Until then, the live TrustBox shows the current score and count (TrustScore 4.7 from 88 reviews on 25 Sep), and the 12 selected reviews are fixed text.

### Contact (`/contact`): ONE HTML widget above the native form: `LATEST/contact-page.txt`

The whole page is one widget (v8). The native Duda form stays in its own row directly below the widget. On the published page, a small script moves the form into the right-hand column. **In the Duda editor the form stays below the widget; that is expected.**

**v7 vanished in the editor after Update; use v8.** v8 contains only markup already working in this site's other Duda widgets (see the house rules at the top). **What you should see in the editor after Update:** the photo banner, "Contact details" with the phone numbers, the awards line, "Helpful information" with three boxes, and the native form in its own row underneath.

**Build.**

1. Duplicate `/contact` → `contact-new`. Hide it from the menu (rule 2).
2. In `contact-new`, delete these three rows:
   - the photo banner row;
   - the "Contact Us" text row;
   - the Facebook/Instagram row.
3. In the form row, delete the **"Send us an enquiry" text** and the **Trustpilot widget**.
   - **Keep the form, and change none of its settings.** The button stays "Send".
   - Set this row's padding to 0.
4. Add **one** full-width row **directly above** the form row, with padding 0. Add **one** HTML widget and paste `LATEST/contact-page.txt`.

   There are no other rows to add. The widget holds the hero, the contact details, the form's column and "Helpful information". The site footer already carries the Pounamu line and social links, so the page doesn't repeat them.
5. Check with Izaac and Joel, then Publish. Open `/contact-new` on a desktop, where the form should sit to the right of the contact details, and on a phone, where it sits below them.

**If the form ever stays below the widget on the published page**, the page still works: the form simply shows under the contact details. The script leaves the form alone if the reCAPTCHA checkbox was already drawn, and it never changes the form itself.

**If the widget still shows nothing after Update**, one two-minute test tells us whether it's the code or the widget:

1. Open the same HTML widget, delete everything, type `<p>TEST</p>`, click **Update**.
2. If **TEST shows**, the widget is fine: open it again, delete `TEST`, paste `LATEST/contact-page.txt` again (select all in the file first, so nothing is cut off), click **Update**. If it vanishes again, write down exactly that ("TEST shows, contact-page.txt vanishes") and send it to whoever maintains this repo.
3. If **TEST does not show either**, the row or widget is the problem, not the code: delete that row, add a fresh full-width row directly above the form row, add a new HTML widget, and paste again.

**Check the form's settings in `contact-new`** against `/contact`. Look only; change nothing:

| Setting | Expected value |
|---|---|
| Email recipient(s) | Same as `/contact` |
| Subject | "SEHE Website Form Message" |
| Webhook / Zapier URL | Present and the same |
| reCAPTCHA | On (checkbox) |
| Success message | "Thank you for contacting us. We will get back to you as soon as possible" |
| Field labels | `%FIRSTNAME%`, `%EMAIL%`, `%ENQUIRY_MESSAGE%` |
| Button text | "Send" (keep it) |

**Tracking stays intact.** The public GTM container, checked 25 Sep 2026, has these triggers:

- *Phone Link Clicked* fires on any link containing `tel:`. Every number on the new page is a `tel:` link.
- *Contact Us Form Submitted* fires when `.dmform-success` containing "Thank you for contacting us" is fully on screen, on a URL containing `/contact`. The native form keeps both, which is also why a preview submission counts (rule 7).

**Labels (optional, manual step).** The labels `%FIRSTNAME%`, `%EMAIL%` and `%ENQUIRY_MESSAGE%` are the **keys the email and the Zapier webhook receive**, because Duda posts them as `label-dmform-N`. That's why the page shows "Your name", "Your email address" and "Your message" with **CSS only**, instead of renaming them.

- No script changes the form. The docking script only moves it into place.
- Until the labels are renamed, screen readers still announce the tokens, as on the live page today.

To rename them properly, in one sitting:

1. Open the Zap that starts from the Duda catch hook and note which fields it maps.
2. Rename the labels in Duda.
3. Re-map the Zap.
4. Delete the three `::before { content: 'Your …' }` lines in the Contact master, bump its version and paste the new `LATEST/contact-page.txt`.

**Chat button.** "Chat with us" appears only once tawk.to has loaded. tawk.to is already on every page, so no second chat system was added.

### About (`/about`): `LATEST/about-page.txt`

Use the §1 row. **Before you publish `about-new`, resolve A1 to A3 in §7** (see Phase 2). A4 doesn't block it.

**Left out** (see A4): three of the old carousel's seven slides.

- The **2025/26 Spring/Summer route map**, which is a past season.
- The Wharf photo, whose 640w file is an 880 KB PNG.
- The humpback whale photo, whose licence is unconfirmed.

### FAQ (`/f-a-q`): `LATEST/faq-page.txt`

Use the §1 row. Every question has its own link, and opening the link opens that answer. For example: `/f-a-q#faq-what-are-the-payment-terms`.

**Check the top of the page (v6).** The four section links and **Open all answers** are the same button: square-ish 6px corners, navy border. On a desktop they sit in one row, with Open all answers at the right. On a phone the section links form an even 2 × 2 grid, with Open all answers full width underneath.

### Gallery (`/gallery`): `LATEST/gallery-page.txt`

Use the §1 row. **v6 is photos first:** there is no caption under the photos.

- **Labels.** A navy label with a gold dash sits on 9 photos only, one per signature experience the current tours name: Queenstown, Aoraki Mt Cook, Kaikoura, Kingston Flyer, Rogers K92, TSS Earnslaw, Larnach Castle, Walter Peak, Taieri Gorge photostop. The label is the photo's own title, word for word.
- **Milford Sound** gets a label once Kirsty settles the spelling (G3). Then add `21: 'Milford Sounds cruise'` (or the corrected title) to `KEY` in the Gallery builder, bump the version and paste again.
- **Credits.** The two photographer credits stay on their photos.
- **Every other title** shows when a photo is opened, and screen readers still hear it.

Then test the lightbox:

- Click a photo to open it. The title (if it has one) shows under the photo with "Photo n of 32".
- The arrow keys move between photos.
- Esc closes it.

### Himalayan Trust (`/himalayan-trust`): `LATEST/himalayan-trust-page.txt`

Use the §1 row. The page is **noindex today; keep it**.

### Privacy Policy (`/privacy-policy`) and Terms (`/terms-and-conditions`)

Paste `LATEST/privacy-policy-page.txt` and `LATEST/terms-page.txt` into a §1 row each. Both pages are **noindex today; keep it**.

The documents copy the live wording word for word. The build refuses to write the file if a single character differs from the live page.

## 4. SEO title and description (Page settings → SEO)

| Page | Title | Description | Indexing |
|---|---|---|---|
| Reviews | Reviews \| Sir Edmund Hillary Explorer *(unchanged)* | Selected Trustpilot reviews, a guest video and earlier feedback from guests who have travelled New Zealand's South Island with the Sir Edmund Hillary Explorer. | index |
| Contact | Contact Us \| Sir Edmund Hillary Explorer | Talk to our New Zealand team about choosing a tour, travelling solo, room options or an existing booking. Phone +64 3 974 1812 or email info@pounamutourismgroup.com. *(replaces the old PO Box 11-11, Blenheim text)* | index |
| About | About \| Sir Edmund Hillary Explorer *(unchanged)* | *(keep current)* | index |
| FAQ | FAQ \| Sir Edmund Hillary Explorer *(unchanged)* | *(keep current)* | index |
| Gallery | Gallery \| Sir Edmund Hillary Explorer *(unchanged)* | *(keep current)* | index |
| Himalayan Trust | Himalayan Trust \| Sir Edmund Hillary Explorer | Sir Edmund Hillary's Himalayan Trust in its own words: its heritage, its work in the Everest region today, and how to donate directly to the Trust. | **noindex (as today)** |
| Privacy Policy | Privacy Policy \| Sir Edmund Hillary Explorer *(unchanged)* | *(keep current)* | **noindex (as today)** |
| Terms | Terms and Conditions \| Sir Edmund Hillary Explorer *(unchanged)* | *(keep current)* | **noindex (as today)** |

No page carries schema. Do not switch on the FAQ schema option or any review stars.

## 5. Manual clean-up outside the pages (exact code)

**Before A to C:** tell Izaac and Joel. These edits change the site-wide Body End HTML and the global header, and publishing pushes every pending edit (rule 3).

### A. Body End HTML (Site Settings): delete this block

It is the Trustpilot widget HTML pasted **inside a `<script>` tag**. It never displays, and it throws `SyntaxError: Unexpected token '<'` on **every page** (confirmed 25 Sep 2026):

```html
 <script>
    <!-- TrustBox widget - Micro Star -->
<div class="trustpilot-widget" data-locale="en-NZ" data-template-id="5419b732fbfb950b10de65e5" data-businessunit-id="67af6f95db89fc000f855205" data-style-height="24px" data-style-width="100%" data-theme="dark">
  <a href="https://nz.trustpilot.com/review/siredmundhillaryexplorer.com" target="_blank" rel="noopener">Trustpilot</a>
</div>
<!-- End TrustBox widget -->
 </script>
```

### B. Body End HTML: delete the last line

This is a second Trustpilot bootstrap. Head HTML already loads it once.

```html
<script type="text/javascript" src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async></script>
```

### C. Global header: delete the HTML widget called "TrustBox script"

It holds only another copy of the same bootstrap:

```html
<!-- TrustBox script --> <script type="text/javascript" src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async=""> </script> <!-- End TrustBox script -->
```

**After A to C, publish, then check:**

1. **On `/reviews-new`** (or `/reviews` after the swap):
   - Open DevTools → **Network** and filter on `tp.widget`. Reload. There should be **exactly one** `tp.widget.bootstrap.min.js` load.
   - The TrustBox in the hero renders.
2. **On one tour page** (e.g. `/pinnacle-tour-2027`), the Trustpilot TrustBox still renders. Tour pages carry their own bootstrap in the page widget, so **two loads there is expected**. Journeys likewise carries its own.

### D. Body End HTML: Meta pixel block with an empty ID

The block runs `fbq('init', '')` and has a `noscript` image with `tr?id=`. GTM already loads the Meta pixel (tag 16).

1. Check in Meta Pixel Helper that the GTM pixel fires on its own.
2. Then delete the block from `<!-- Facebook Pixel Code -->` to `<!-- End Facebook Pixel Code -->`.

Do **not** touch the Tawk.to, `AW-16523865426` gtag or ActiveCampaign (`vgo`) scripts.

### E. Footer menu

The footer menu (desktop and mobile) has no **Reviews** link, and its order differs from the header. Add Reviews after Journeys, to match the header: Home · About · Journeys · Reviews · Gallery · FAQ · Contact.

### F. Mobile header phone icon

It links to `tel:+64 3 974 1812`, with spaces. Change it to `tel:+6439741812` so every phone dials it cleanly.

## 6. Findings on other pages (report only; nothing changed)

### `/brochure-collection`: keep it noindex; watch the traffic that reaches it without a form

**Why it's noindex.** It is noindex on purpose. Every brochure form redirects there, and the Meta custom conversion **"Brochure Collection Page"** fires on URLs containing `brochure-collection`. The risk is visits that reach it **without** submitting a form.

**What fires on a page view of `/brochure-collection`.** Checked 25 Sep 2026 against the public GTM container `GTM-TPSTZ264` and the page source.

- **GTM**, all page views (no trigger is specific to this page):
  - tag 14, Google tag `G-GKR67569LP` (GA4 page_view);
  - tag 16, Meta Pixel base code (PageView);
  - tag 36, Microsoft Clarity;
  - tag 47, Microsoft UET page load (`97186072`);
  - the link-click and element-visibility listeners.
- **Head HTML:** GA4 `G-GKR67569LP` a second time, Duda's own GA4 `G-KESV7YYW1G`, AdRoll, and Clarity a second time.
- **Body End:** Google Ads tag `AW-16523865426` (config), a Meta Pixel block with an empty ID (PageView), ActiveCampaign site tracking, and tawk.to.
- **The gap:** nothing on the page tells "arrived after a form" apart from "arrived by a link". Any conversion defined as "URL contains brochure-collection" therefore counts every visit.

**Internal links to `/brochure-collection`.**

- **Live site:** none, apart from the page's own canonical tag. The Journeys cards' "Brochure" buttons go to each tour page's `#tour-brochure` form.
- **New pages:** the earlier versions had three direct links (the Reviews band, the Contact quick link and the Gallery band). They are removed in Reviews v4, Contact v4 and Gallery v3.

**PMax sitelinks: yes, they can count as brochure conversions.**

- The repo's own PMax plan (`creatives/google-journeys/pmax/PMAX-CAMPAIGN.md`) has a **"Brochure Collection" sitelink to `/brochure-collection`**.
- The same plan proposes the primary conversion `brochure_lead` as a **GA4 page view of `/brochure-collection`**, imported into Google Ads.
- The Creator's handover sheet has a **"Free Tour Brochures"** sitelink to the same URL.

So if either sitelink is live and the brochure conversion is URL-based, every sitelink click counts as a brochure lead, and PMax will learn to buy those clicks. Meta's "Brochure Collection Page" is URL-based. The Google Ads and GA4 definitions could not be checked, because I have no access to the accounts.

**Recommendation:**

- Move the brochure sitelink(s) off `/brochure-collection`, to `/journeys` or to a tour page's `#tour-brochure` form.
- Keep `/brochure-collection` reachable only through the forms.
- Later, count the form submission itself rather than the page visit.

**Also seen, unverified:** GA4 `G-GKR67569LP` is configured twice (Head HTML and GTM tag 14), and Clarity loads twice. Page views may be double-counted in GA4; check in GA4 DebugView.

### Other findings

- **Two old banner images** are PNG files named `.jpg`, and their 1280w and 1920w CDN sizes redirect in a loop. Neither is used by the new pages.
  - the `/contact` banner (L161 Milford Sound, **3.9 MB**);
  - the `/gallery` banner (Wharf, 880 KB).
- **Homepage v38 (on `/v2`).** The hero hard-codes the Trustpilot 5-star image with 'Rated "Excellent"'. This is the same honesty issue as the tour-page strips.
- **Journeys v22** loads its own Trustpilot bootstrap. It also says "small-group", against Paul's no-"small groups" rule.
- **Head HTML** contains a long explanatory comment ("What was fixed: …") that anyone can read in the page source. Tidying it is optional.

## 7. Content flags (Kirsty or the business to decide; nothing edited)

The wording on the new pages is exactly as it is live today, unless a master's changelog says otherwise. The items below look wrong or disagree with other pages. They are listed here, not changed. The emails in `notes/2026-09-25-emails.md` send Kirsty's and Paul's items.

### Reviews

- **R1 — Lisa Godwin.** Her review is on Trustpilot, posted July 2025. On the old page it appeared as direct guest feedback, with a travel date and a link to her Trustpilot profile. It is simply not in the new selected set, and it is left out of "Earlier guest feedback", which now has 16 entries.
- **R2 — Newer reviews.** About 16 reviews are newer than the brief's original May set. The selected set was replaced on 25 Sep with reviews up to September 2026 (§3, Reviews). Refresh it now and then.
- **R3 — Typos in the older testimonials**, such as "where wonderful", "every been on" and "Hilary". They are kept verbatim by rule.

### Contact

- **C1 — Form labels.** The labels `%FIRSTNAME%`, `%EMAIL%` and `%ENQUIRY_MESSAGE%` are the payload keys. Screen readers announce those tokens, as they do on the live page today. The fix is the label rename with the Zap check (§3, Contact).
- **C2 — Webhook URL in page source.** Duda's form puts its Zapier catch-hook URL in the public page source, so anyone could post to it. Consider a filter step in the Zap, for example: only continue when the subject is "SEHE Website Form Message".
- **C3 — Two email addresses.** The site uses info@pounamutourismgroup.com, but the Terms use info@siredmundhillaryexplorer.com. Confirm both inboxes are monitored.

### About (for Kirsty)

The About text was rewritten in the approved copy update (round 3, 25 Sep 2026). A1 to A3 quote the new wording.

**A1 to A3 block the About page.** `about-new` is not published until each one has been handled:

- **Confirmed for every tour:** keep.
- **True only for some:** qualify it in Kirsty's words.
- **Not true, or no answer:** delete the sentence.

All three sentences are in the second paragraph under "Our inspiration". To edit them:

- **Before building:** edit the master (`SEHE-about-page_v*.txt`: bump the version, run `tools/make-latest.py`).
- **Already pasted:** edit the text in the `about-new` HTML widget, then update the master to match.

- **A1 — International Antarctic Centre.** The page says: "In Christchurch, learn about his team's Antarctic expedition using converted farm tractors at the International Antarctic Centre." Is that visit still on every itinerary?
- **A2 — Marlborough.** The page says: "You will also travel through Marlborough, where Hillary trained for the air force during the Second World War and climbed Mt Tapuae-o-Uenuku." Is that still true of every tour?
- **A3 — Hillary family guest speaker.** The page says: "A guest speaker from the Hillary family shares personal stories and how the family continues his legacy." Is that on every departure? Other pages put it differently:
  - The live homepage says "a member of the Hillary family personally joins the tour for an evening at the Sir Edmund Hillary Alpine Centre".
  - Journeys shows a "Hillary Family Speaker" tile.
  - Peter Hillary hosts only the Pinnacle.
- **A4 — Photos left out.** Three items from the old carousel are not on the new page:
  - the 2025/26 route map, which is for a past season (**is there an updated map?**);
  - the Wharf photo, whose 640w file is an 880 KB PNG;
  - the humpback whale photo. Its file name (`australasia_new_zealand_kaikoura_gallery_…`) suggests a third-party library image, and the licence is unconfirmed.

### FAQ (answers verbatim; conflicts with other pages)

- **F1 — Mobility. URGENT for Paul.** Kirsty's ruling is "two flights of stairs", which is what the FAQ says. Terms clause 13 still says "15 steps … carry your own bags", and the Terms are the contract.
- **F2 — Payment methods.** The pages disagree:
  - The FAQ offers bank transfer (AU$, US$ and NZ$ accounts), Wise and PayPal.
  - Terms clause 2 says internet banking, with a 2% credit-card surcharge.
  - The Journeys FAQ says internet banking plus a 2% card fee, and leaves out the 40%-at-six-months stage.
- **F3 — When the operator cancels.** The FAQ says "100% refund". Terms clauses 3–4 say PTG first tries to reschedule or offer other dates. Terms item e) also says 100% refund.
- **F4 — Flights.** The FAQ says flights to and from the start and end points are not included. The homepage says the Pinnacle includes the flight to Auckland.
- **F5 — Meals.** One answer says "all breakfasts and a selection of additional meals". Another says "Most meals are included".
- **F6 — Seating (minor).** The FAQ page says some trains have allocated seating. The Journeys FAQ says seating "is not pre-allocated", but that answer is about the coach.
- **F7 — Dietary requirements.** The FAQ says to use the "pre-trip documentation". Terms clause 23 says "at the time of booking".
- **F8 — Hygiene answer (for Kirsty).** It mentions N95 masks and Rapid Antigen Tests. Is that still current?
- **F9 — Typo kept verbatim.** "Some train journeys feature allocated an allocated seating".
- **F10 — Physical payment address.** The address "Level 3, 111 Cashel Street, Christchurch" stays in the FAQ's payment answer. It is deliberately not shown on Contact, because it isn't a visitor location.

### Gallery (for Kirsty)

- **G1 — Intro sentence. RESOLVED (round 3, 25 Sep 2026).** The old intro said every photo came from passengers, but two are professional images (Rob Suisted, David Wall; both credited). The intro now reads "A closer look at the scenery and experiences along the way, including photographs shared by our guests."
- **G2 — Titles that look wrong.**
  - Two photos are titled "Mirror Lake aka Lake Matheson (by Fox Glacier)", but they look like the Mirror Lakes in the Eglinton Valley on the Milford Road.
  - The waterfall titled "Milford Sounds" looks like Thunder Creek Falls on the Haast Pass.
- **G3 — Spellings kept verbatim:** "Milford Sounds", "Milford Sounds cruise", "Queen Charlotte Sounds", and "Kaikoura" without a macron. Since v6 this also holds back the Milford Sound label: Milford is a signature experience, but a label reading "Milford Sounds" would put the misspelling on the page. Once Kirsty approves "Milford Sound", correct both titles and add the label.
- **G4 — Photos of places no current tour visits** (checked against the current tour pages' text on 25 Sep 2026): Queen Charlotte Sounds, Picton foreshore (also the page's banner photo), Arrowtown and "Moonshine tasting in Gore", plus the two G2 photos. They are still in the gallery, unlabelled. Keep them or remove them: Kirsty's call.

### Himalayan Trust (the Trust's own words)

- **H1 — Statistics kept as written.** Confirm these are current with the Trust:
  - "Over half the population lives on $3 a day or less"
  - "planted over 2.6 million tree seedlings over 30 years"
- **H2 — Caption dates differ from the photo file names.**
  - "Sotang, 2023" is on a file named "Nepal Monitoring 2022".
  - "Khunde Hospitals nurses, 2019" is on a file dated 2016_02_25.
- **H3 — Typos kept verbatim:** "we need you help"; "Khunde Hospitals nurses".

### Privacy Policy (no wording changes allowed; for Paul)

- **P1 — Checkfront.** Section 4 lists **Checkfront (Booking & Reservations System)**. Bookings now run through The Creator's booking app, so the policy should name the current processor.
- **P2 — Postal address.** The policy gives PO Box 39018, Harewood, Christchurch 8545. Everywhere else uses PO Box 19735, Woolston.
- **P3 — Cookie preferences.** The policy says "You can manage or withdraw your cookie preferences via our website settings". The site has no cookie-consent or settings tool, but it runs two GA4 properties, Google Ads, AdRoll, the Meta Pixel, Microsoft Clarity and ActiveCampaign tracking.
- **P4 — Under-13s.** Section 8 says the services "are not intended for individuals under the age of 13", but Terms clause 41 allows guests under 13 when accompanied.
- **P5 — Missing full stop.** Section 9's last sentence has no full stop. It is kept verbatim.

### Terms & Conditions (no wording changes allowed; for Paul)

- **T1 — Postcode.** Clause 1 gives "PO Box 19735, Woolston, Christchurch, **82415**". It should be 8241.
- **T2 — Email.** Clause 1 gives info@siredmundhillaryexplorer.com (see C3).
- **T3 — Privacy Officer address.** Clause 9 gives PO Box 39018, Harewood, Christchurch 8545 (see P2).
- **T4 — Clause numbering** jumps from 18 to 20, so there is no clause 19.
- **T5 — Missing link.** Clause 8 says the Privacy Policy "can be viewed here on this page", but there is no link.
- **T6 — Ferry.** Clause 36 mentions a Picton–Wellington ferry ticket. Is that still part of any tour?
- **T7 — Typos kept verbatim:**
  - "It You are responsible" (clause 10)
  - "a refund the Tour Package Price" (clause 18)
  - "PTG.." (clause 32)
  - "on behalf or a Guest … that that Guest" (clause 41)
  - "organisers ," (clause 44)
- See also F1, F2, F3 and F7.
