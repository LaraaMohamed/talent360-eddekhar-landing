# Talent360 × Eddekhar landing page

Bilingual (Arabic default, English) landing page for Eddekhar clients to book a free HR Health Check with 10% off.

## Build

```
python3 build.py           # production site in dist/ (ar/, en/, assets/)
python3 build.py preview   # flat preview in preview/
```

Content lives in `content.py`, markup in `template.py`, styles and scripts in `assets/`.

## Deploy

**Render (live, dynamic):** `render.yaml` runs `backend/server.js`, which serves the built pages from `dist/` and the
booking and lead-magnet API on the same domain. Every push to `main` redeploys. Email needs `SMTP_HOST`, `SMTP_USER` and
`SMTP_PASS` set in the Render service's Environment tab; calendar invites need `GOOGLE_SERVICE_ACCOUNT_JSON` (see `backend/.env.example`).
Until SMTP is set, every booking and download request is still emailed to the team through FormSubmit (set `TEAM_INBOX` in `build.py`).

**GitHub Pages (static mirror):** `.github/workflows/pages.yml` publishes `dist/` on every push. Forms there use the FormSubmit relay only.

## Lead-magnet guides

`guides/guides.py` + `guides/render.js` generate the Egypt and Saudi labour-law PDFs
(`cd guides && python3 guides.py && node render.js`). The backend emails `backend/files/<tool>-<lang>.pdf`.
