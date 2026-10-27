# Talent360 × Eddekhar landing page: handoff note

Last updated: 26 October 2026 (v2, profile theme)

## What is in this folder

| Path | What it is |
|---|---|
| `dist/` | Deploy-ready static site: `ar/` (default), `en/`, each with a `case-studies/` page, `assets/`, `robots.txt`, `llms.txt`, `sitemap.xml`, and a root `index.html` that sends visitors to their saved language. |
| `backend/` | Booking API (Node 18+): slots from Ahmed's Google Calendar free/busy, event + Google Meet creation, bilingual confirmation email, CRM push, honeypot, rate limit, double-booking guard, signed cancel/reschedule links. Runs in stub mode until `.env` is filled in. |
| `content.py` | Every word on both pages (Arabic first, English mirror). Edit copy here, then rebuild. |
| `build.py` | `python3 build.py` rebuilds `dist/`. `REVIEW = False` (current) hides the internal review markers; set it to `True` to show them. Set `BASE` to the final hosting URL. |
| `assets/` | CSS, JS, logos, client logos and photos used by both pages. |

The page is fully functional without the backend: if `/api` is unreachable, the booking widget generates slots locally and shows a clearly labelled "preview mode" confirmation.

## How the structure maps to eddekhar.com/en

The page follows Eddekhar's section order and trust rhythm, with Talent360's identity:

1. Announcement bar (Eddekhar: "Discounts at 2,500+ stores") → Eddekhar-client offer bar
2. Sticky header with co-brand lockup, AR/EN toggle, primary CTA
3. Hero with two CTAs and a tick-mark trust line, plus the stats row
4. "Trusted by leading Saudi companies" marquee → "شركات تثق بتالنت 360"
5. One-line value statement
6. Two-sided value cards → four service cards (How we help)
7. Products → the two free checks (the offer)
8. Contact form → moved up as the inline booking block (the conversion point)
9. "Get started in three simple steps" with visuals → 3 steps with output mock-ups
10. Partners and integrations tabs → Saudi platforms we handle (GOSI, Qiwa, Mudad, Nitaqat, Muqeem, Ajeer) and markets. Text only, explicitly labelled as platforms, not partnerships.
11. Elite case study, then the 12-pillar comparison (Talent360 vs own entity vs EOR)
12. Blog → free tools / lead magnets (cost-of-a-bad-hire calculator works ungated)
13. Shariah expert flip card + compliance seal + regulator licence → "what to expect" list + company legal details + PDPL statement + process promises + Eddekhar partnership line
14. Five FAQs → eight FAQs
15. Final CTA band, then footer with legal entity details

## Brand decisions (v2, rebuilt on the Company Profile 2026)

- Brand name in Arabic is **موارد ومهارات** (or "موارد ومهارات by Talent360"); in Latin script it is **Talent360**. Never write تالنت 360 in Arabic.

- The whole page now follows the profile's look: light mint gradients, teal contour waves, navy `#0E183C` headings, teal `#1FC9B1` rules and accents, cream `#FFF5CB` cards, warm white `#FFFCF8` stat cards, teal service tiles with numbered circles. No navy-filled sections.
- Several sections use the profile's own artwork, re-rendered from the PDF without its text so the page sets live, bilingual text on top: the cover (hero), the "Numbers that speak for themselves" cubes slide (Arabic and English versions), the "Let's partner for growth" puzzle stack, and the large "T" shape behind "Connect with us". The consultant photo is from the "Why choose Talent 360" slide.
- Fonts match the profile: Almarai (Arabic), Unbounded Medium headings and Montserrat body (English), `display=swap`.
- Eddekhar green `#608E4D` is used only for the offer tag, the 10% panel and tick marks. Eddekhar logos are used unmodified, on a light chip where needed.
- In dark mode the Talent360 wordmark switches to a reversed (white) version.

## Open placeholders (confirm before launch)

None of these show on the page: `REVIEW` is now `False`, so the yellow review tags, empty legal rows and draft placeholders are hidden. Set `REVIEW = True` in `build.py` to see them marked on the page again.

1. **Logos**
   - Amanah Al Riyadh: logo supplied and now in the client strip.
   - Client logos were cropped from the company profile PDF (the Canva "HCM Model Cheat Sheet" one-pager could not be reached this session). Replace with original vector files if available.
   - Magnetic and OMQ: naming approval still needed.
2. **Photos**: the hero uses the company profile cover artwork, and the trust section uses the profile's consultant photo. Swap in a real Talent360 team or consultant photo if available. Ahmed's photo is missing (initials avatar for now). Elite visuals need permission.
3. **Stats**: page shows the five figures from the 2026 profile slide: 30+ industries, 80+ consultants, 4,500+ consultation hours, 5,500+ hired candidates, 300+ clients. Lara to confirm.
4. **Elite**: written permission to name, show the logo and quote; confirm the basis of the ~40% saving; supply an approved pull-quote (placeholder shown in review mode only).
5. **Comparison PDF figures**: the page is qualitative only. Approve the numbers before the gated PDF goes out. The EOR column wording should get a quick legal read.
6. ~~**Ahmed Darkawi** card~~: removed from the page at the user's request (2026-10-26). The FAQ and the trust intro still name Ahmed as the session lead; confirm that wording.
7. **Legal details**: commercial registration number, VAT number, full Riyadh address, (privacy policy is now a pop-up with the PDPL sentence, per the user; no URL needed), licences if any. No ISO or licence badges are shown because none were provided.
8. **Lead magnets**: only the cost-of-a-bad-hire calculator is interactive. The other seven open an email gate that posts to `/api/lead-magnet`, which logs the request but does not yet send a file. Decide launch scope and supply the PDFs.
9. **Hosting**: canonical URLs assume `https://talent-360.me/eddekhar/`. Change `BASE` in `build.py` if it will live at `eddekhar.talent-360.me`.
10. **Eddekhar's written approval** of the page before launch.
11. **Legal copy review**: the FAQ answer on whether offshoring is legal, and the "we are the employer" statements, should be checked by Talent360's legal adviser.
12. **Testimonials**: block omitted, per the rule. The profile's only quote is unattributed.
13. **FAQ count**: the brief listed nine questions and asked for six to eight. "How long to start hiring?" was left out because no confirmed timing exists.
14. **Social links**: LinkedIn, Instagram and Facebook URLs are inferred from the handles in the profile (Talent 360 ME / talent360me). Please verify.

## Backend setup

1. `cd backend && npm install`
2. Copy `.env.example` to `.env` and fill in:
   - Google Workspace service account with domain-wide delegation and the Calendar scope, impersonating Ahmed (`CONSULTANT_EMAIL`).
   - SMTP for bilingual confirmation emails (Brevo or Google Workspace SMTP both work).
   - `CRM_WEBHOOK_URL` and `CRM_API_KEY` for the Talent360 CRM on Railway. Each lead is tagged `Eddekhar referral`, `focus:<hr|team|unsure>`, `lang:<ar|en>`, and carries UTMs, PDPL consent time and a call-ready note.
   - `LINK_SECRET` for signed cancel/reschedule links.
3. Serve `dist/` and proxy `/api/*` to the Node service on the same origin.
4. Replace the in-memory `bookings` map with the CRM or a database before production (it resets on restart).

Slot rules (enforced on both client and server): Sunday to Thursday, 30-minute sessions from 10:00 with a 15-minute buffer (10:00, 10:45, 11:30, 12:15, 13:00, 13:45, 14:30, 15:15), last session ends 15:45, 24-hour minimum notice, Riyadh time (GMT+3), visitor can switch to their own time zone.

## Tracking

Events pushed to `window.dataLayer`: `cta_click` (with `cta` id), `slot_selected`, `booking_confirmed`, `tool_used`, `lead_magnet_requested`, `language_toggle`, `scroll_depth` (25/50/75/100). Connect GTM or GA4 to read them. UTMs from the Eddekhar catalogue link are kept for the session, carried on the language toggle, and sent with every booking.

## Tested

- 360px, 768px and 1280px, light and dark, Arabic and English: no horizontal scroll (the day picker scrolls sideways by design).
- Full booking flow in Arabic and English against the stub API: focus preselected from a service card, slot chosen, three fields, confirmation, optional phone saved, CRM payload logged with UTMs.
- Reduced motion stops the logo marquee and lays logos out as a static wall; hovering or focusing the strip also pauses it (the visible pause button was removed at the client's request).

## Egypt salary calculator (added 2026-10-27)
- Replaces the "HR prompt pack" tool card. It runs live in the tools section (`#salcalc`) and has no email gate.
- The formulas and limits were supplied by the user and are not independently verified:
  - Social insurance: Law 148/2019, an 11% employee share of the insured wage, with an insured wage between EGP 2,700 and 16,700 from 1 January 2026.
  - Income tax: Law 91/2005 as amended, the 2026 brackets and a EGP 20,000 personal exemption.
- Have Talent360's payroll lead confirm the figures before launch, and update them each January.
- The logic is in `assets/js/main.js` (search for "Egypt salary calculator"), and the copy is under the `sc_*` keys in `content.py`.

## More lead magnets (added 2026-10-27)
- Salary calculator now also shows the employer cost: employer social insurance share = 18.75% of the insured wage (Law 148/2019, still the governing law in 2026; 11%/18.75% and the 2,700/16,700 limits match Atlas HXM citing PwC, and Tawzef). Still worth a payroll sign-off.
- Effective tax rate, top bracket, a bracket-by-bracket tax table, and a "copy offer-letter breakdown" button.
- Bulk payroll sheet: visitors paste name + gross (or upload a CSV). Totals and a 3-row preview are free; the full CSV downloads after they give a work email (gate tool id `bulk_payroll_eg`). The data never leaves the browser; the backend only receives the email.
- Elite case study is now a gated download (tool id `elite_case_pdf`): a card in the tools grid and a button on the case-study page. **Open: the Elite case study PDF itself is needed** so the backend `/lead-magnet` handler can email it. Elite's written permission is still required before launch.

## Email (updated 2026-10-27)
- The preview has no mail server, so gated forms now say plainly "preview: no email was sent" instead of a fake "sent" message.
- Real sending happens in `backend/server.js` (`sendLeadMagnet`): needs SMTP_* (any SMTP, e.g. Brevo or Google Workspace) and TEAM_EMAIL set, and the PDFs placed in `backend/files/<tool>.pdf`. Missing PDF = visitor gets a "the team will send it within one working day" email and the team is notified.
- Only company emails are accepted (page and server): Gmail, Hotmail/Outlook/Live, Yahoo, iCloud, Proton, GMX, Yandex, AOL, Zoho and similar are refused.

## Labour law guides (added 2026-10-27)
- Two gated PDFs in the tools section: `labour_law_eg` (Egypt Labour Law 14/2025 + 2026 employee benefits table, 3 pages) and `labour_law_sa` (Saudi Labour Law after the Feb 2025 amendments, 2 pages), each in AR and EN.
- Source: `guides/guides.py` (content + sources) and `guides/render.js` (Playwright → A4 PDF). Rebuild: `cd guides && python3 guides.py && node render.js`.
- The backend attaches `backend/files/<tool>-<lang>.pdf`, falling back to `<tool>.pdf`.
- Each guide lists its sources at the end. Before launch, have someone on the HR/legal team re-check article numbers, the EGP 7,000 private-sector minimum wage and the GOSI rates against the official texts.
- The cost-of-a-bad-hire calculator was removed (user request, 2026-10-27).
