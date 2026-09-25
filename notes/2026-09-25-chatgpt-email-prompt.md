You are helping Ben write emails about work on the Sir Edmund Hillary Explorer website (siredmundhillaryexplorer.com, a Duda site run by Pounamu Tourism Group). Write the emails only. Do not commit, push, open pull requests or issues, or edit any file.

SOURCES: GitHub repo Bengitshub/SEHE, branch claude/gracious-clarke-v52v6s (NOT main)
Read these first. They are the source of truth: if this prompt and the repo disagree, follow the repo and tell me.
1. notes/2026-09-25-old-pages-rebuild-runbook.md: "Start here", the check-over table, the go-live plan, §0 rules, §2 swap, §3 page notes, §4 SEO table, §5 clean-up A to F, §7 content questions.
2. notes/2026-09-25-emails.md: the current drafts to Kirsty and Paul.
3. LATEST/_READ-ME-FIRST.txt, and README.md ("Rules of the road").
4. The branch's commit messages from 25 Sep 2026, which explain each change.

PEOPLE
- Ben: sends every email. Contractor; his contract ends 31 October 2026.
- Kirsty: approves every page before it goes live, and answers the content questions.
- Paul: owns the legal and policy wording (Privacy Policy, Terms, and the FAQ's payment and cancellation answers).
- Aaron: manages the site and does the switch-over, same as always. After 31 October, page changes go to him.
- Izaac and Joel (The Creator): have their own work in the same Duda editor. They confirmed nothing was waiting on 25 Sep.

WHAT HAPPENED (checked on the live site, 25 Sep 2026)
- Eight old-design pages now have new designs, each built on a hidden preview page that search engines are told to ignore. The live pages are untouched. Previews: reviews-new, contact-new, about-new, faq-new, gallery-new, himalayan-trust-new, privacy-policy-new, terms-new, each at https://www.siredmundhillaryexplorer.com/ followed by that name.
- Every preview was checked on desktop and phone: the code is complete, there are no leftover old sections, and none appears in any menu.
- About is on hold. It must not go live, or be shared, until Kirsty answers questions A1 to A3 (runbook §7).
- Contact: the first attempts vanished in the editor because the copied code was cut off at line 150. The page was rebuilt from a fresh copy of /contact. Its form is the real Duda form, with the same recipient, webhook and subject as the live page, and on the published page it sits beside the contact details. It is a live form: a message sent from the preview reaches the inbox and the Zap, and counts as a conversion.
- Duda rewrites one CSS character (">") when it publishes, which broke the "Show 6 more reviews" button on the first Reviews preview. Every page file now avoids it, and Reviews is fixed.
- FAQ: the buttons at the top now match. Gallery: photos first, with 10 small labels on signature tour experiences, and "Milford Sounds" corrected to "Milford Sound" (Ben confirmed).
- The two 2026/27 spring/summer tour pages (14-day and 11-day) had been hidden from Google. That is fixed, and both are back in the sitemap.
- Not done yet: the site-wide clean-up in runbook §5, items A to F. A to C remove broken or duplicate Trustpilot code from the Body End HTML and the global header (A causes a script error on every page). D removes a Facebook Pixel block with an empty ID. E adds Reviews to the footer menu. F fixes the mobile header phone link.

WRITE THESE FOUR EMAILS
1. To Kirsty: previews and questions. Base it on draft 1 in notes/2026-09-25-emails.md: the seven preview links (not About); please don't send a message through the Contact preview's form; nothing goes live until she approves; then her questions (About 1 to 4, Gallery 5 and 6, FAQ 7). Tell her About follows once she answers About 1 to 3.
2. To Paul: legal and policy fixes. Use draft 2 in notes/2026-09-25-emails.md, tightened only. Keep all 14 items and their item codes.
3. To Aaron: switch-over handover. Cover:
   - which previews are ready, each with its preview link and the live page it replaces; About is held;
   - swap each page only after Kirsty approves it, following runbook §2, and paste the SEO title and description from §4;
   - exact addresses: faq-new becomes f-a-q, terms-new becomes terms-and-conditions, privacy-policy-new becomes privacy-policy, and the rest simply drop "-new";
   - "Hide from search engines": off for Reviews, Contact, About, FAQ and Gallery; keep it on for Himalayan Trust, Privacy and Terms;
   - after each rename, delete any URL redirect whose source is the page's live address (Duda may add one automatically), and point the header and footer menu items at the new page;
   - publishing pushes every pending edit, so check with Izaac and Joel first;
   - Contact: in the editor the form sits in its own row below the new section, which is expected; never change or move the form; no test messages unless one is agreed;
   - the §5 clean-up (A to F), with a heads-up to Izaac and Joel before A to C;
   - two lessons for any future edit: copy the whole file from the downloaded file or GitHub's Raw view, never from a preview (the Contact, Reviews and Privacy files end with an "END OF FILE" line, which must be the last line in Duda's code box); and edit the masters in the repo, not LATEST/ (runbook "Changing a page's content later");
   - rollback takes about two minutes, because the old pages are never changed (§2);
   - where everything is: the repo, the branch and the runbook path.
4. To Izaac and Joel: a short FYI. Eight hidden preview pages were published on 25 Sep (list them); the two 2026/27 tour pages are visible to Google again; Aaron will do the switch-overs after Kirsty approves; the §5 clean-up will touch the Body End HTML and the global header, and they will hear before anything there is published. Thank them for confirming nothing was waiting.

STYLE
- From Ben: friendly and plain, New Zealand English, short paragraphs and lists.
- No em dashes. Use commas, colons or full stops instead.
- Kirsty's and Paul's emails: no technical jargon, no file paths, no version numbers. Aaron's email may use file paths and runbook section numbers.
- Put each preview link on its own line, as a full URL.
- Don't describe the tours as "small group" or "rail touring".
- Never include webhook or Zapier URLs, API keys, tokens, hidden form values or anything else secret from the repo.
- Don't invent facts. If you're unsure of something, write [CHECK: what to confirm].

OUTPUT
For each email: To, Subject, then the body. After the four emails, list anything in the repo that contradicted this prompt or looked out of date.
