# Old-design pages rebuild: runbook (25 Sep 2026)

This runbook covers the eight pages rebuilt under Brief v2: Reviews, Contact, About, FAQ, Gallery, Himalayan Trust, Privacy Policy and Terms & Conditions.

- **Paste files:** always paste from `LATEST/`, regenerated with `python3 tools/make-latest.py`.
- **Masters:** the masters are `SEHE-<page>-page_v1.txt` in the repo root.
- **Before snapshot:** the served HTML of every old page is saved in `backups/2026-09-25-old-pages/`.

## 0. Rules for every page

1. **Build on a copy.** Duplicate the live page and name the copy `<slug>-new`. The live page stays untouched until the swap.
2. **Nothing is live until the swap.**
   - Duda gives a new page **noindex** by default.
   - The copy is not in the menu.
   - Publishing the site while a `-new` page exists is safe.
3. **Never create a redirect from `/<slug>` to `/<slug>-old`.** After renaming, open **Site Settings → URL Redirects** and delete any rule whose source is `/<slug>`. Duda may add one automatically when a page URL changes.
4. **Contact: copy the form, never move it.** Duplicating the page gives `contact-new` its own copy of the form. The original page, which becomes `contact-old`, keeps its form, so rollback stays possible.
5. **Do not send test submissions to the live inbox.** They reach Kirsty's inbox and the Zapier lead Zap. If an end-to-end test is wanted, agree it with Kirsty first.
6. **Removing noindex at the swap is a launch blocker**, except for the three pages that are noindex today (see the table).

## 1. The row every single-widget page needs

In the `-new` page:

1. Delete **every content row**. Leave the global header and footer alone.
2. Add an empty **1-column row** and set it to:
   - Full width: on.
   - Padding top and bottom: **0**.
   - Background: none.
3. Drag in an **HTML** widget, click **Edit HTML**, paste the whole `LATEST/<file>`, then click **Update**.

The CSS also sets the row padding to 0 in modern browsers. The editor setting covers older browsers without `:has()` support.

## 2. The swap (launch), per page

1. **Old page → Page settings.**
   - Change the URL from `<slug>` to `<slug>-old`.
   - Turn **Hide from search engines** on.
   - Remove it from the navigation.
2. **Site Settings → URL Redirects.** Delete any rule from `/<slug>`.
3. **New page → Page settings.**
   - Change the URL from `<slug>-new` to `<slug>`.
   - Paste the SEO title and description from the table in §4.
   - Set **Hide from search engines**: **off** for Reviews, Contact, About, FAQ and Gallery.
   - Keep it **on** for Himalayan Trust, Privacy and Terms, as today.
4. **Site Navigation.** Duda menu items point to *pages*, not URLs, so the menu still points at the old page after the rename.
   - Show the new page in the old page's position, with the same label.
   - Check both the header menu and the footer menu.
5. **Publish.** Then check the live URL on a phone and a desktop:
   - the menu link and the footer link;
   - that no redirect is in place (the URL stays `/<slug>`).

**Rollback** is the same steps in reverse:

1. New page → `<slug>-new`, with noindex on.
2. Old page → `<slug>`, with noindex off where it was indexed.
3. Restore the menu.
4. Delete any redirect from `/<slug>`.
5. Publish.

The old page is untouched throughout, so rollback takes about two minutes.

## 3. Page by page

### Reviews (`/reviews`) — `LATEST/reviews-page.txt`

**Build.** Use the §1 row. **After publishing `/reviews-new`, check:**

- The Trustpilot Micro Combo shows in the hero. If it doesn't, the plain "Read our reviews on Trustpilot" link shows instead.
- **Show 6 more reviews** opens.
- The guest video plays. Click play once: Vimeo blocks automated playback checks, so it could not be tested here.

**Trustpilot plan limit.** This Trustpilot account cannot use review-list TrustBoxes. Trustpilot's data service answers "BusinessUnit does not have access to that trustbox" for Carousel, Slider, List and Grid. Only Micro, Mini, Starter and Review Collector are available. So new reviews do **not** appear on the page automatically:

- The live TrustBox always shows the current score and count.
- The 12 selected reviews are fixed text.

**To refresh the selected reviews:**

1. Copy the reviews verbatim, cut only at whole sentences, and mark cuts with "…".
2. Keep name, country and review month.
3. Edit `TP` in the master, bump the version, then run `tools/make-latest.py`.

**Alternative:** upgrade the Trustpilot plan and paste the Carousel TrustBox "Get code" snippet, business unit `67af6f95db89fc000f855205`.

### Contact (`/contact`) — three HTML widgets plus the native form

**Build.**

1. Duplicate `/contact` → `contact-new`.
2. In `contact-new`, delete these three rows:
   - the photo banner row;
   - the "Contact Us" text row;
   - the Facebook/Instagram row.
3. In the form row, delete the **"Send us an enquiry" text** and the **Trustpilot widget**. **Keep the form.**
4. Drag an **HTML** widget onto the **left edge of the form**. Duda creates a left column.
   - Paste `LATEST/contact-page-blockB-details.txt`.
   - Set the row padding to 0.
5. Add a full-width row **above** it (padding 0) and paste `LATEST/contact-page-blockA-hero.txt`. Block A carries the CSS for the whole page, so it must stay on the page.
6. Add a full-width row **below** it and paste `LATEST/contact-page-blockC-more.txt`.

**Check the form's settings in `contact-new`** against `/contact`. Look only; change nothing:

| Setting | Expected value |
|---|---|
| Email recipient(s) | Same as `/contact` |
| Subject | "SEHE Website Form Message" |
| Webhook / Zapier URL | Present and the same |
| reCAPTCHA | On (checkbox) |
| Success message | "Thank you for contacting us. We will get back to you as soon as possible" |
| Field labels | `%FIRSTNAME%`, `%EMAIL%`, `%ENQUIRY_MESSAGE%` |

**Tracking stays intact.** The public GTM container, checked 25 Sep 2026, has these triggers:

- *Phone Link Clicked* fires on any link containing `tel:`. Every number on the new page is a `tel:` link.
- *Contact Us Form Submitted* fires when `.dmform-success` containing "Thank you for contacting us" is fully on screen, on a URL containing `/contact`. The native form keeps both.

**Labels (optional, manual step for Ben).** The labels `%FIRSTNAME%`, `%EMAIL%` and `%ENQUIRY_MESSAGE%` are the **keys the email and the Zapier webhook receive**, because Duda posts them as `label-dmform-N`. That's why the page shows "Your name", "Your email address" and "Your message" with CSS and `aria-label` instead of renaming them.

To rename them properly, in one sitting:

1. Open the Zap that starts from the Duda catch hook and note which fields it maps.
2. Rename the labels in Duda.
3. Re-map the Zap.
4. Delete the three `::before { content: "Your …" }` lines in Block A.

**Chat button.** "Start a live chat" only appears once tawk.to has loaded. tawk.to is already on every page; no second chat system was added.

### About (`/about`) — `LATEST/about-page.txt`

Use the §1 row.

**Flagged for Kirsty, not edited.** The live text says:

1. "In Christchurch, learn more about his team's expedition … at the International Antarctic Centre". Is that visit still part of every itinerary?
2. "You will also travel through Marlborough, where Edmund was trained for the air force … Mt Tapuae-o-Uenuku". Is Marlborough still on every tour?
3. "A guest speaker from the Hillary family will also give you an insight …". Is this true of every departure? The live homepage says "a member of the Hillary family personally joins the tour for an evening at the Sir Edmund Hillary Alpine Centre".

**Left out.** The old carousel's first slide is a **2025/26 Spring/Summer route map**, a past season. Kirsty should send an updated map if one exists.

### FAQ (`/f-a-q`) — `LATEST/faq-page.txt`

Use the §1 row. Every question has its own link, and opening the link opens that answer. For example: `/f-a-q#faq-what-are-the-payment-terms`.

### Gallery (`/gallery`) — `LATEST/gallery-page.txt`

Use the §1 row, then test the lightbox:

- Click a photo to open it.
- The arrow keys move between photos.
- Esc closes it.

### Himalayan Trust (`/himalayan-trust`) — `LATEST/himalayan-trust-page.txt`

Use the §1 row. The page is **noindex today; keep it**.

### Privacy Policy (`/privacy-policy`) and Terms (`/terms-and-conditions`)

Paste `LATEST/privacy-policy-page.txt` and `LATEST/terms-page.txt` into a §1 row. Both pages are **noindex today; keep it** unless Ben decides otherwise.

The documents are word-for-word copies. The build refuses to write the file if a single character differs from the live page.

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

## 5. Manual clean-up outside the pages (Ben; exact code)

### A. Body End HTML (Site Settings) — delete this block

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

### B. Body End HTML — delete the last line

This is a second Trustpilot bootstrap. Head HTML already loads it once.

```html
<script type="text/javascript" src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async></script>
```

### C. Global header — delete the HTML widget called "TrustBox script"

It holds only another copy of the same bootstrap:

```html
<!-- TrustBox script --> <script type="text/javascript" src="//widget.trustpilot.com/bootstrap/v5/tp.widget.bootstrap.min.js" async=""> </script> <!-- End TrustBox script -->
```

After A–C, the bootstrap loads once, from Head HTML. On the live Journeys page it currently appears four times.

### D. Body End HTML — Meta pixel block with an empty ID

The block runs `fbq('init', '')` and has a `noscript` image with `tr?id=`. GTM already loads the Meta pixel (tag 16).

1. Check in Meta Pixel Helper that the GTM pixel fires on its own.
2. Then delete the block from `<!-- Facebook Pixel Code -->` to `<!-- End Facebook Pixel Code -->`.

Do **not** touch the Tawk.to, `AW-16523865426` gtag or ActiveCampaign (`vgo`) scripts.

### E. Footer menu

The footer menu (desktop and mobile) has no **Reviews** link, and its order differs from the header. Add Reviews after Journeys, matching the header: Home · About · Journeys · Reviews · Gallery · FAQ · Contact.

### F. Mobile header phone icon

It links to `tel:+64 3 974 1812`, with spaces. Change it to `tel:+6439741812` so every phone dials it cleanly.

## 6. Found on out-of-scope pages (report only; nothing changed)

- **noindex on key pages.** The tour pages `/2026-2027-spring/summer-tour-14-days` and `/2026-2027-spring/summer-tour-11-day-tours`, and `/brochure-collection`, are served with `<meta name="robots" content="noindex">`. They are also missing from `/sitemap.xml`. These pages are PMax sitelinks and main menu destinations. Check whether this is intentional.
- **Two old banner images** are PNG files named `.jpg`, and their 1280w and 1920w CDN sizes redirect in a loop:
  - the `/contact` banner (L161 Milford Sound, **3.9 MB**);
  - the `/gallery` banner (Wharf, 880 KB).

  The new pages don't use them.
- **Homepage v38 (on `/v2`).** The hero hard-codes the Trustpilot 5-star image with 'Rated "Excellent"'. This is the same honesty issue as the tour-page strips.
- **Journeys v22** loads its own Trustpilot bootstrap. It also says "small-group", against Paul's no-"small groups" rule.
- **Head HTML** contains a long explanatory comment ("What was fixed: …") that anyone can read in the page source. Optional tidy.

## 7. Content flags (Kirsty or the business to decide; nothing edited)

Collected in the final report of 25 Sep 2026, and also listed in each master's header.
