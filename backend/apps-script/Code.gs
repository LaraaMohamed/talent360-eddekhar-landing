/**
 * Talent360 × Eddekhar booking bridge. Runs inside business-growth@talent-360.me's own Google account,
 * so it uses that mailbox's Gmail and its edit access to Ahmed Al-Darkawi's calendar (darkawi@talent-360.me).
 *
 * Setup (once, signed in as business-growth@talent-360.me): see README.md in this folder.
 *  - Script property KEY = the same value as APPS_SCRIPT_SECRET on Render.
 *  - Run setup() once from the editor: approves permissions, installs the daily health check, creates the log sheet.
 *  - Deploy → Web app → Execute as: Me, Who has access: Anyone. The URL goes into APPS_SCRIPT_URL on Render.
 *
 * Hardening: every Google call retries with backoff on transient errors; event creation runs under a script
 * lock with a free/busy re-check and an idempotency key (no double bookings, no duplicates on retries);
 * mail checks the daily quota first; every failure is logged to a Google Sheet and alerts business-growth@
 * (at most once an hour per kind of error); a daily trigger checks calendar and mail access.
 */
var TZ = "Asia/Riyadh";
var DEFAULT_CAL = "darkawi@talent-360.me";
var ALERT_TO = "business-growth@talent-360.me";
var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function doPost(e) {
  var b;
  try { b = JSON.parse(e.postData.contents); } catch (x) { return out({ error: "bad_json" }); }
  var key = prop("KEY");
  if (!key || b.key !== key) return out({ error: "forbidden" });
  try {
    switch (b.action) {
      case "ping": return out({ ok: true, account: Session.getEffectiveUser().getEmail(), mailQuota: MailApp.getRemainingDailyQuota() });
      case "busy": return out({ busy: busy(b.timeMin, b.timeMax, b.calendars) });
      case "event": return out(createEvent(b));
      case "cancel": return out(cancelEvent(b));
      case "mail": return out(mail(b));
    }
    return out({ error: "unknown_action" });
  } catch (err) {
    var msg = String(err && err.message || err);
    logError(b.action, msg, { start: b.start, to: b.to || b.attendee });
    return out({ error: msg, retryable: isTransient(msg) });
  }
}

// Plain GET answers a health probe (no data, no key needed), handy for an uptime monitor.
function doGet() { return out({ ok: true, service: "talent360-booking-bridge" }); }

function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function prop(k) { return PropertiesService.getScriptProperties().getProperty(k); }

/* ---------- Retries ---------- */
function isTransient(msg) {
  return /rate limit|too many|quota|backend error|internal error|service (invoked|unavailable|error)|timed? ?out|try again|503|500|server error|unavailable/i.test(String(msg));
}
function withRetry(fn, label) {
  var last;
  for (var i = 0; i < 5; i++) {
    try { return fn(); } catch (err) {
      last = err;
      if (!isTransient(err && err.message || err)) throw err;
      Utilities.sleep(Math.min(8000, 400 * Math.pow(2, i)) + Math.floor(Math.random() * 300));
    }
  }
  throw new Error((label || "call") + " failed after retries: " + (last && last.message || last));
}

/* ---------- Validation ---------- */
function isoDate(s, name) {
  var d = new Date(s);
  if (!s || isNaN(d.getTime())) throw new Error("invalid_" + name);
  return d;
}
function calId(id) {
  id = String(id || DEFAULT_CAL).trim();
  if (id !== "primary" && !EMAIL_RE.test(id) && id.indexOf("@group.calendar.google.com") < 0) throw new Error("invalid_calendar");
  return id;
}

/* ---------- Free/busy ---------- */
function busy(timeMin, timeMax, calendars) {
  var a = isoDate(timeMin, "timeMin"), z = isoDate(timeMax, "timeMax");
  if (z <= a) throw new Error("invalid_range");
  var ids = (calendars && calendars.length ? calendars : [DEFAULT_CAL]).map(calId);
  var r = withRetry(function () {
    return Calendar.Freebusy.query({ timeMin: a.toISOString(), timeMax: z.toISOString(), timeZone: TZ, items: ids.map(function (id) { return { id: id }; }) });
  }, "freebusy");
  var all = [];
  Object.keys(r.calendars || {}).forEach(function (id) {
    var c = r.calendars[id];
    // An unreadable calendar must not look "free": surface it so the server can stop offering slots.
    if (c.errors && c.errors.length) throw new Error("freebusy unavailable for " + id + ": " + JSON.stringify(c.errors));
    (c.busy || []).forEach(function (x) { all.push({ start: x.start, end: x.end }); });
  });
  return all;
}

/* ---------- Booking event (lock + re-check + idempotency) ---------- */
function createEvent(b) {
  var start = isoDate(b.start, "start"), end = isoDate(b.end, "end");
  if (end <= start) throw new Error("invalid_range");
  if (!EMAIL_RE.test(String(b.attendee || ""))) throw new Error("invalid_attendee");
  if (!b.requestId) throw new Error("missing_request_id");
  var cal = calId(b.calendarId);
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(25000)) throw new Error("busy, try again");
  try {
    // Same booking retried by the server: return the event we already made.
    var existing = withRetry(function () {
      return Calendar.Events.list(cal, { privateExtendedProperty: "bookingId=" + b.requestId, maxResults: 1, showDeleted: false });
    }, "lookup");
    if (existing.items && existing.items.length) return { eventId: existing.items[0].id, meetUrl: existing.items[0].hangoutLink || null, reused: true };

    var clash = withRetry(function () {
      return Calendar.Freebusy.query({ timeMin: start.toISOString(), timeMax: end.toISOString(), timeZone: TZ, items: [{ id: cal }] });
    }, "recheck");
    var c = clash.calendars && clash.calendars[cal];
    if (c && c.busy && c.busy.length) return { error: "slot_taken" };

    var guests = (b.guests || []).filter(function (g) { return EMAIL_RE.test(g); });
    var ev = withRetry(function () {
      return Calendar.Events.insert({
        summary: String(b.summary || "Talent360 session").slice(0, 200), description: String(b.description || "").slice(0, 4000),
        start: { dateTime: start.toISOString(), timeZone: TZ }, end: { dateTime: end.toISOString(), timeZone: TZ },
        attendees: [{ email: b.attendee }].concat(guests.map(function (g) { return { email: g }; })),
        conferenceData: { createRequest: { requestId: b.requestId, conferenceSolutionKey: { type: "hangoutsMeet" } } },
        reminders: { useDefault: false, overrides: [{ method: "email", minutes: 1440 }, { method: "popup", minutes: 60 }] },
        extendedProperties: { private: { bookingId: String(b.requestId), source: "eddekhar_landing" } },
      }, cal, { conferenceDataVersion: 1, sendUpdates: "all" });
    }, "insert");
    return { eventId: ev.id, meetUrl: ev.hangoutLink || null };
  } finally {
    lock.releaseLock();
  }
}

function cancelEvent(b) {
  if (!b.eventId) throw new Error("missing_event_id");
  var cal = calId(b.calendarId);
  try {
    withRetry(function () { Calendar.Events.remove(cal, b.eventId, { sendUpdates: "all" }); }, "cancel");
  } catch (err) {
    if (/not found|deleted|410|404/i.test(String(err.message))) return { ok: true, already: true };
    throw err;
  }
  return { ok: true };
}

/* ---------- Mail (quota-aware) ---------- */
function mail(b) {
  if (!EMAIL_RE.test(String(b.to || ""))) throw new Error("invalid_to");
  if (!b.subject || !(b.text || b.html)) throw new Error("invalid_mail");
  var left = MailApp.getRemainingDailyQuota();
  if (left < 1) { alert("mail_quota", "Daily Gmail sending quota is used up. Site emails pause until it resets; the site falls back to direct downloads."); return { error: "mail_quota", retryable: true }; }
  var opts = { name: b.fromName || "Talent360" };
  if (b.replyTo && EMAIL_RE.test(b.replyTo)) opts.replyTo = b.replyTo;
  if (b.html) opts.htmlBody = b.html;
  if (b.attachment && b.attachment.data) opts.attachments = [Utilities.newBlob(Utilities.base64Decode(b.attachment.data), b.attachment.type || "application/pdf", b.attachment.name || "guide.pdf")];
  withRetry(function () { GmailApp.sendEmail(b.to, String(b.subject).slice(0, 250), b.text || "", opts); }, "mail");
  if (left < 20) alert("mail_quota_low", "Only " + (left - 1) + " emails left in today's Gmail quota for the booking bridge.");
  return { ok: true, quotaLeft: left - 1 };
}

/* ---------- Error log sheet + throttled alerts ---------- */
function logSheet() {
  var id = prop("LOG_SHEET_ID"), ss = null;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
  if (!ss) {
    ss = SpreadsheetApp.create("Talent360 booking bridge log");
    ss.getSheets()[0].appendRow(["Time (UTC)", "Action", "Error", "Details"]);
    PropertiesService.getScriptProperties().setProperty("LOG_SHEET_ID", ss.getId());
  }
  return ss.getSheets()[0];
}
function logError(action, msg, details) {
  try { logSheet().appendRow([new Date().toISOString(), action || "", String(msg).slice(0, 500), JSON.stringify(details || {}).slice(0, 500)]); } catch (e) { console.error(e); }
  if (!isTransient(msg) || /failed after retries/.test(msg)) alert(action + ":" + String(msg).slice(0, 40), "Action: " + action + "\nError: " + msg + "\nDetails: " + JSON.stringify(details || {}));
}
function alert(kind, body) {
  var cache = CacheService.getScriptCache(), k = "alert:" + kind;
  if (cache.get(k)) return; // at most one alert per kind per hour
  cache.put(k, "1", 3600);
  try {
    var id = prop("LOG_SHEET_ID");
    MailApp.sendEmail(ALERT_TO, "[Talent360 booking bridge] " + kind, body + (id ? "\n\nLog: https://docs.google.com/spreadsheets/d/" + id : ""));
  } catch (e) { console.error("alert failed", e); }
}

/* ---------- Health check (daily trigger) and one-time setup ---------- */
function healthCheck() {
  var problems = [];
  try { var now = new Date(); busy(now.toISOString(), new Date(now.getTime() + 86400000).toISOString(), [DEFAULT_CAL]); }
  catch (e) { problems.push("Cannot read " + DEFAULT_CAL + " free/busy: " + e.message); }
  try { if (MailApp.getRemainingDailyQuota() < 10) problems.push("Gmail quota nearly used up: " + MailApp.getRemainingDailyQuota() + " left"); }
  catch (e) { problems.push("Cannot read mail quota: " + e.message); }
  if (!prop("KEY")) problems.push("Script property KEY is missing.");
  if (problems.length) { logError("healthCheck", problems.join(" | "), {}); alert("health", problems.join("\n")); }
  console.log(problems.length ? problems.join("\n") : "healthy");
  return problems;
}

function setup() {
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === "healthCheck") ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger("healthCheck").timeBased().everyDays(1).atHour(8).inTimezone(TZ).create();
  logSheet();
  var p = healthCheck();
  console.log("setup done as " + Session.getEffectiveUser().getEmail() + (p.length ? " with problems: " + p.join(" | ") : ", all healthy"));
}
