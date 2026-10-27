# Connect the booking page to business-growth@talent-360.me

The script runs inside the Business Growth Google account, so bookings land on **its** calendar (with a Google Meet link) and emails go out from **its** Gmail. No admin console, service account or app password.

1. Sign in to Google as **business-growth@talent-360.me** and open <https://script.google.com> → **New project**. Name it "Eddekhar booking".
2. Replace everything in `Code.gs` with [`Code.gs`](Code.gs) from this folder.
3. **Project Settings** (gear icon) → tick **Show "appsscript.json" manifest file**. Back in the editor, open `appsscript.json` and replace it with [`appsscript.json`](appsscript.json).
4. **Project Settings → Script properties → Add property**: name `KEY`, value a long random string (e.g. 40 letters and numbers). Keep it; Render needs the same value.
5. **Deploy → New deployment** → type **Web app** → *Execute as*: **Me** → *Who has access*: **Anyone** → **Deploy**. Click **Authorize access**, choose business-growth@, and allow (if Google says the app isn't verified: **Advanced → Go to Eddekhar booking**).
6. Copy the **Web app URL** (ends in `/exec`).
7. Render → talent360-eddekhar → **Environment**: add `APPS_SCRIPT_URL` = that URL and `APPS_SCRIPT_SECRET` = the `KEY` value. Save (the service restarts).
8. Ahmed's calendar: slots only show when **both** business-growth@ and Ahmed (`BUSY_CALENDARS`) are free, and Ahmed is invited to each booking (`BOOKING_GUESTS`). Inside the talent-360.me Workspace free/busy is shared by default; if Ahmed's busy times don't show, he opens Google Calendar → Settings → his calendar → *Share with specific people* → adds business-growth@talent-360.me with **See only free/busy**.
9. Open `https://talent360-eddekhar.onrender.com/api/health`. It should show `"appsScript": "ok as business-growth@talent-360.me"`, `"calendar": true`, `"mail": true`.

**Guides and files:** a visitor who asks for a guide gets an email from business-growth@ with a confirmation link; opening it verifies their company email and starts the download. The team gets a "verified and downloaded" email.

If you later edit the script, use **Deploy → Manage deployments → Edit → Version: New version** so the URL stays the same.
