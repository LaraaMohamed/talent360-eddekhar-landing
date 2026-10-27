# Moving to Railway

The repo deploys to Railway from `Dockerfile` and `railway.json`. One service runs everything: the static Arabic and English pages, the booking API and the guide downloads. The server is always on, so the calendar no longer waits for a cold start.

## 1. Create the service (about 5 minutes)

1. Go to railway.com and sign in with GitHub. Choose the **Hobby** plan ($5 a month, which covers this site).
2. **New Project → Deploy from GitHub repo → `LaraaMohamed/talent360-eddekhar-landing`**, branch `main`.
3. Railway finds `railway.json` and builds with the Dockerfile. Leave the build and start commands empty.
4. Open the service. Under **Settings → Networking**, click **Generate Domain**. You get a domain like `talent360-eddekhar-production.up.railway.app`.
5. Optional: add `eddekhar.talent-360.me` as a custom domain there, then add the CNAME record Railway shows at your DNS provider.
6. Under **Settings → Region**, pick a European region (closest to Riyadh and Cairo).

## 2. Variables (Service → Variables → Raw editor)

Copy the two secret values from Render (**Dashboard → talent360-eddekhar → Environment**). Fill in your Railway domain, then paste:

```
PUBLIC_BASE_URL=https://<your Railway domain or custom domain>
APPS_SCRIPT_URL=<copy from Render>
APPS_SCRIPT_SECRET=<copy from Render>
BUSY_CALENDARS=darkawi@talent-360.me
CONSULTANT_CALENDAR_ID=darkawi@talent-360.me
BOOKING_GUESTS=business-growth@talent-360.me
TEAM_EMAIL=business-growth@talent-360.me
MAIL_FROM=Talent360 <business-growth@talent-360.me>
LINK_SECRET=<copy from Render, so cancel links already sent keep working>
```

Copy any other variables you set on Render too, such as `SEND_VISITOR_EMAIL`, `CRM_WEBHOOK_URL` and `CRM_API_KEY`. Railway redeploys by itself after you save.

## 3. Check it

- Open `https://<railway domain>/api/health`. It should show `"appsScript": "ok as business-growth@talent-360.me"` and `"calendar": true`.
- Open `/ar/`, go to the booking section and check the times load.

## 4. Switch over

- Share the new link instead of the onrender.com one.
- In GitHub, disable the **Keep booking server warm** workflow (Actions → workflow → ⋯ → Disable). Railway doesn't sleep.
- Keep Render for a few days as a backup, then suspend it.
- PDF guides link to the booking page. Tell Claude the final domain, and it will rebuild the guides to point there.
