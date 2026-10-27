/**
 * Talent360 × Eddekhar booking bridge. Runs inside business-growth@talent-360.me's own Google account,
 * so the calendar and Gmail it uses are that mailbox's. No service account, no app password.
 *
 * Setup (once, signed in as business-growth@talent-360.me):
 *  1. script.google.com → New project → paste this file as Code.gs.
 *  2. Project Settings → tick "Show appsscript.json" → replace it with appsscript.json from this folder.
 *  3. Project Settings → Script properties → add KEY = a long random string (same value as APPS_SCRIPT_SECRET on Render).
 *  4. Deploy → New deployment → Web app → Execute as: Me, Who has access: Anyone → Deploy → allow access.
 *  5. Copy the Web app URL into APPS_SCRIPT_URL on Render.
 */
var TZ = "Asia/Riyadh";

function doPost(e) {
  var b;
  try { b = JSON.parse(e.postData.contents); } catch (x) { return out({ error: "bad_json" }); }
  var key = PropertiesService.getScriptProperties().getProperty("KEY");
  if (!key || b.key !== key) return out({ error: "forbidden" });
  try {
    switch (b.action) {
      case "ping": return out({ ok: true, account: Session.getEffectiveUser().getEmail() });
      case "busy": return out({ busy: busy(b.timeMin, b.timeMax) });
      case "event": return out(createEvent(b));
      case "cancel": Calendar.Events.remove("primary", b.eventId, { sendUpdates: "all" }); return out({ ok: true });
      case "mail": return out(mail(b));
    }
    return out({ error: "unknown_action" });
  } catch (err) {
    console.error(err);
    return out({ error: String(err && err.message || err) });
  }
}

function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

// Busy intervals on the primary calendar (timed events the owner hasn't declined).
function busy(timeMin, timeMax) {
  return CalendarApp.getDefaultCalendar().getEvents(new Date(timeMin), new Date(timeMax))
    .filter(function (ev) { return !ev.isAllDayEvent() && ev.getMyStatus() !== CalendarApp.GuestStatus.NO; })
    .map(function (ev) { return { start: ev.getStartTime().toISOString(), end: ev.getEndTime().toISOString() }; });
}

// Event with a Google Meet link; Google emails the invite to the client.
function createEvent(b) {
  var ev = Calendar.Events.insert({
    summary: b.summary, description: b.description,
    start: { dateTime: b.start, timeZone: TZ }, end: { dateTime: b.end, timeZone: TZ },
    attendees: [{ email: b.attendee }],
    conferenceData: { createRequest: { requestId: b.requestId, conferenceSolutionKey: { type: "hangoutsMeet" } } },
    reminders: { useDefault: false, overrides: [{ method: "email", minutes: 1440 }, { method: "popup", minutes: 60 }] },
  }, "primary", { conferenceDataVersion: 1, sendUpdates: "all" });
  return { eventId: ev.id, meetUrl: ev.hangoutLink || null };
}

// Plain-text email from this mailbox, optional PDF attachment (base64).
function mail(b) {
  var opts = { name: b.fromName || "Talent360" };
  if (b.replyTo) opts.replyTo = b.replyTo;
  if (b.attachment) opts.attachments = [Utilities.newBlob(Utilities.base64Decode(b.attachment.data), b.attachment.type || "application/pdf", b.attachment.name)];
  GmailApp.sendEmail(b.to, b.subject, b.text, opts);
  return { ok: true };
}
