# Talent360 × Eddekhar landing page

Bilingual (Arabic default, English) landing page for Eddekhar clients to book a free HR Health Check with 10% off.

## Build

```
python3 build.py           # production site in dist/ (ar/, en/, assets/)
python3 build.py preview   # flat preview in preview/
```

Content lives in `content.py`, markup in `template.py`, styles and scripts in `assets/`.

## Deploy

Every push to `main` builds the site and publishes `dist/` to GitHub Pages (`.github/workflows/pages.yml`).
In the repo settings, set **Pages → Source** to **GitHub Actions** once.

GitHub Pages serves static files only. Booking, Google Calendar invites and lead-magnet emails need the
Node backend in `backend/` hosted separately (see `backend/.env.example` and `HANDOFF.md`), with
`apiBase` in the page config pointing at it. Until then the forms validate but nothing is sent.

## Lead-magnet guides

`guides/guides.py` + `guides/render.js` generate the Egypt and Saudi labour-law PDFs
(`cd guides && python3 guides.py && node render.js`). The backend emails `backend/files/<tool>-<lang>.pdf`.
