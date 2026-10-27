/* Booking service for the Talent360 × Eddekhar landing page.
 *
 * STATUS: documented stub. The routes, validation, slot rules, anti-spam and
 * double-booking checks are implemented; Google Calendar, email and CRM calls
 * activate once the environment variables in .env.example are set.
 *
 * Routes (mounted under /api, same origin as the page):
 *   GET  /api/slots?date=YYYY-MM-DD      busy intervals on the consultant's calendar
 *   POST /api/book                        create the event + Meet link, email, CRM
 *   POST /api/booking/:id/phone           add the optional phone after confirmation
 *   GET  /api/booking/:id/cancel?token=   cancel (link in the confirmation email)
 *   GET  /api/booking/:id/reschedule?token=  redirects to the page with the booking id
 *   POST /api/lead-magnet                 email capture for gated PDFs
 */
"use strict";

const http = require("http");
const crypto = require("crypto");
const { google } = require("googleapis");
const nodemailer = require("nodemailer");

const env = process.env;
// Everything (calendar, sender, team copies) runs from the Business Growth mailbox unless overridden.
const BG = "business-growth@talent-360.me";
const CAL_OWNER = env.CONSULTANT_EMAIL || BG;
const FROM = env.MAIL_FROM || `Talent360 <${env.SMTP_USER || BG}>`;
const TEAM = env.TEAM_EMAIL || BG;
const PORT = Number(env.PORT || 8080);
const TZ = "Asia/Riyadh";
const OFFSET_MIN = 180;
const RULES = { days: [0, 1, 2, 3, 4], startMin: 600, endMin: 960, len: 30, buffer: 15, noticeH: 24, horizonDays: 21 };

/* ---------- Google Calendar (service account with domain-wide delegation) ---------- */
function calendarClient() {
  if (!env.GOOGLE_SERVICE_ACCOUNT_JSON) return null;
  const creds = JSON.parse(env.GOOGLE_SERVICE_ACCOUNT_JSON);
  const auth = new google.auth.JWT({
    email: creds.client_email, key: creds.private_key,
    scopes: ["https://www.googleapis.com/auth/calendar"],
    subject: CAL_OWNER, // impersonate the Business Growth mailbox so events and Meet links live on its calendar
  });
  return google.calendar({ version: "v3", auth });
}
const cal = calendarClient();

/* ---------- Google Apps Script bridge (preferred): runs inside business-growth@'s own account ----------
   See backend/apps-script/. Set APPS_SCRIPT_URL + APPS_SCRIPT_SECRET; then no service account or SMTP is needed. */
const GAS = env.APPS_SCRIPT_URL || "";
async function gas(action, payload) {
  const r = await fetch(GAS, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, redirect: "follow",
    body: JSON.stringify(Object.assign({ action, key: env.APPS_SCRIPT_SECRET || "" }, payload)) });
  const text = await r.text();
  let j; try { j = JSON.parse(text); } catch (e) { throw new Error("apps script: non-JSON reply (" + r.status + "): " + text.slice(0, 160)); }
  if (j.error) throw new Error("apps script: " + j.error);
  return j;
}
let gasStatus = GAS ? "checking" : "not configured";
if (GAS) gas("ping", {}).then((j) => { gasStatus = "ok as " + j.account; console.log("[apps-script]", gasStatus); })
  .catch((e) => { gasStatus = e.message; console.error("[apps-script]", e.message); });
const CAL_ID = env.CONSULTANT_CALENDAR_ID || "primary";

async function busyBetween(timeMin, timeMax) {
  if (!cal && GAS) return (await gas("busy", { timeMin, timeMax })).busy || [];
  if (!cal) return []; // stub mode: everything free
  const r = await cal.freebusy.query({ requestBody: { timeMin, timeMax, timeZone: TZ, items: [{ id: CAL_ID }] } });
  return (r.data.calendars[CAL_ID] && r.data.calendars[CAL_ID].busy) || [];
}

/* ---------- Slot rules (mirror the front end; the server is the authority) ---------- */
function riyadhDow(date) { return new Date(date.getTime() + OFFSET_MIN * 60000).getUTCDay(); }
function riyadhMinutes(date) { const r = new Date(date.getTime() + OFFSET_MIN * 60000); return r.getUTCHours() * 60 + r.getUTCMinutes(); }
function isValidSlot(start, end) {
  if (isNaN(start) || isNaN(end)) return false;
  if (end - start !== RULES.len * 60000) return false;
  if (RULES.days.indexOf(riyadhDow(start)) === -1) return false;
  const m = riyadhMinutes(start);
  if (m < RULES.startMin || m + RULES.len > RULES.endMin) return false;
  if ((m - RULES.startMin) % (RULES.len + RULES.buffer) !== 0) return false;
  if (start.getTime() < Date.now() + RULES.noticeH * 3600000) return false;
  if (start.getTime() > Date.now() + RULES.horizonDays * 86400000) return false;
  return true;
}

/* ---------- Anti-spam: per-IP rate limit ---------- */
const hits = new Map();
function rateLimited(ip, limit = 8, windowMs = 10 * 60000) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < windowMs);
  list.push(now); hits.set(ip, list);
  return list.length > limit;
}

/* ---------- Double-booking guard: in-process lock + calendar re-check ---------- */
const locks = new Set();

/* ---------- Signed links for cancel / reschedule / phone ---------- */
function sign(id) { return crypto.createHmac("sha256", env.LINK_SECRET || "dev-secret").update(id).digest("base64url").slice(0, 32); }
function verify(id, token) { const a = Buffer.from(sign(id)); const b = Buffer.from(String(token || "")); return a.length === b.length && crypto.timingSafeEqual(a, b); }

/* ---------- Email (bilingual) ---------- */
const smtp = env.SMTP_HOST && env.SMTP_PASS ? nodemailer.createTransport({ host: env.SMTP_HOST, port: Number(env.SMTP_PORT || 587), secure: Number(env.SMTP_PORT) === 465, auth: { user: env.SMTP_USER || BG, pass: env.SMTP_PASS } }) : null;
if (smtp) smtp.verify().then(() => console.log("[mail] SMTP ready as", env.SMTP_USER || BG)).catch((e) => console.error("[mail] SMTP login failed:", e.message));
// With no SMTP, mail goes out through the Apps Script bridge from business-growth@'s Gmail.
const mailer = smtp || (GAS ? { sendMail: (m) => {
  const a = (m.attachments || [])[0];
  return gas("mail", { to: m.to, subject: m.subject, text: m.text, replyTo: m.replyTo, fromName: "Talent360",
    attachment: a ? { name: a.filename, type: "application/pdf", data: require("fs").readFileSync(a.path).toString("base64") } : null });
} } : null);
function fmt(date, lang) {
  return new Intl.DateTimeFormat(lang === "ar" ? "ar-SA-u-ca-gregory-nu-latn" : "en-GB", { timeZone: TZ, dateStyle: "full", timeStyle: "short" }).format(date);
}
async function sendConfirmation(b) {
  if (!mailer) return;
  const when = fmt(new Date(b.start), b.lang);
  const cancel = `${env.PUBLIC_BASE_URL}/api/booking/${b.id}/cancel?token=${b.token}`;
  const resched = `${env.PUBLIC_BASE_URL}/api/booking/${b.id}/reschedule?token=${b.token}`;
  const ar = `تم تأكيد جلستك المجانية مع موارد ومهارات\n\nالموعد: ${when} (بتوقيت الرياض)\nرابط الاجتماع: ${b.meetUrl || "يُرسل لاحقًا"}${env.CONSULTANT_NAME_AR ? "\nالمستشار: " + env.CONSULTANT_NAME_AR : ""}\nخصم إدخار 10% مطبق تلقائيًا.\n\nإعادة الجدولة: ${resched}\nالإلغاء: ${cancel}`;
  const en = `Your free session with Talent360 is confirmed\n\nWhen: ${when} (Riyadh time)\nMeeting link: ${b.meetUrl || "to follow"}${env.CONSULTANT_NAME_EN ? "\nConsultant: " + env.CONSULTANT_NAME_EN : ""}\n10% Eddekhar discount applied automatically.\n\nReschedule: ${resched}\nCancel: ${cancel}`;
  await mailer.sendMail({
    from: FROM, to: b.email,
    subject: b.lang === "ar" ? "تأكيد جلسة الفحص المجاني | موارد ومهارات × إدخار" : "Your free HR check is booked | Talent360 × Eddekhar",
    text: b.lang === "ar" ? ar + "\n\n— — —\n\n" + en : en + "\n\n— — —\n\n" + ar,
  });
  // Reminders: Google Calendar sends the invite reminders (24h email + 1h popup) set on the event below.
}
async function notifyTeam(b) {
  if (!mailer) return;
  await mailer.sendMail({
    from: FROM, to: TEAM, replyTo: b.email,
    subject: `[Eddekhar booking] ${b.focusLabel} · ${b.company} · ${fmt(new Date(b.start), "en")}`,
    text: [`New booking from the Eddekhar landing page.`, ``,
      `When: ${fmt(new Date(b.start), "en")} (Riyadh time)`, `Focus: ${b.focusLabel}`,
      `Name: ${b.name}`, `Company: ${b.company}`, `Email: ${b.email}`, `Language: ${b.lang}`,
      `Meet: ${b.meetUrl || (cal || GAS ? "not created" : "calendar not connected: send an invite by hand")}`,
      `UTM: ${Object.entries(b.utm || {}).map(([k, v]) => k + "=" + v).join(", ") || "none"}`].join("\n"),
  });
}

/* ---------- Lead magnets: email the file, tell the team, log to CRM ----------
   Put each PDF at backend/files/<tool>-<lang>.pdf or <tool>.pdf (e.g. labour_law_eg-ar.pdf, elite_case_pdf.pdf).
   If a file is missing the visitor gets a "coming shortly" email and the team is asked to send it by hand.
   bulk_payroll_eg downloads in the browser, so it only notifies the team. */
const LEAD_TITLES = {
  compare_pdf: ["مقارنة الـ Offshoring بالكيان الخاص في مصر", "Offshoring vs your own Egypt entity"],
  elite_case_pdf: ["دراسة حالة Elite كاملة", "The full Elite case study"],
  bulk_payroll_eg: ["كشف الرواتب الكامل", "Full payroll sheet"],
  labour_law_eg: ["دليل قانون العمل المصري الجديد 14/2025", "Egypt's new Labour Law 14/2025: employer guide"],
  labour_law_sa: ["دليل نظام العمل السعودي بعد تعديلات 2025", "Saudi Labour Law after the 2025 amendments"],
};
async function sendLeadMagnet(body) {
  const tool = String(body.tool || "").replace(/[^\w-]/g, "");
  const lang = body.lang === "en" ? "en" : "ar";
  const title = (LEAD_TITLES[tool] || [tool, tool])[lang === "ar" ? 0 : 1];
  // Prefer a language-specific file (files/<tool>-<lang>.pdf), then files/<tool>.pdf.
  const path = require("path"), fs = require("fs");
  const file = [tool + "-" + lang + ".pdf", tool + ".pdf"].map((f) => path.join(__dirname, "files", f)).find((f) => fs.existsSync(f));
  const hasFile = Boolean(file);
  console.log("[lead-magnet]", tool, body.email, hasFile ? "file" : "no-file");
  const crm = { source: "eddekhar_landing", tags: ["Eddekhar referral", "lead_magnet:" + tool, "lang:" + lang], email: body.email, utm: body.utm,
    note: `Eddekhar referral. Requested "${title}" from the landing page.` };
  if (env.CRM_WEBHOOK_URL) fetch(env.CRM_WEBHOOK_URL, { method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + (env.CRM_API_KEY || "") }, body: JSON.stringify(crm) }).catch((e) => console.error("[crm]", e.message));
  else console.log("[crm stub]", JSON.stringify(crm));
  if (!mailer) return;
  const jobs = [];
  if (tool !== "bulk_payroll_eg") {
    const ar = hasFile ? `مرفق لك: ${title}.\n\nإذا أردت مناقشة النتائج مع مستشار، احجز فحصك المجاني: ${env.PUBLIC_BASE_URL}/ar/#book\n\nموارد ومهارات by Talent360`
                       : `شكرًا لطلبك: ${title}.\nسيرسله لك فريق موارد ومهارات خلال يوم عمل.\n\nموارد ومهارات by Talent360`;
    const en = hasFile ? `Attached: ${title}.\n\nWant to talk it through with a consultant? Book your free check: ${env.PUBLIC_BASE_URL}/en/#book\n\nTalent360`
                       : `Thanks for requesting: ${title}.\nThe Talent360 team will send it within one working day.\n\nTalent360`;
    jobs.push(mailer.sendMail({
      from: FROM, to: body.email,
      subject: title + (lang === "ar" ? " | موارد ومهارات" : " | Talent360"),
      text: lang === "ar" ? ar : en,
      attachments: hasFile ? [{ filename: path.basename(file), path: file }] : [],
    }));
  }
  jobs.push(mailer.sendMail({
    from: FROM, to: TEAM,
    subject: `[Eddekhar lead] ${title} requested by ${body.email}`,
    text: `${body.email} requested "${title}" (${tool}) from the Eddekhar landing page (${lang}).` + (hasFile || tool === "bulk_payroll_eg" ? "" : "\nNo file is configured for this tool yet: please send it by hand."),
  }));
  await Promise.allSettled(jobs);
}

/* ---------- CRM (Talent360 CRM on Railway) ---------- */
async function pushToCrm(b) {
  const note = [
    `Eddekhar referral. Booked ${b.focusLabel} for ${fmt(new Date(b.start), "en")} Riyadh time.`,
    `Contact: ${b.name}, ${b.company}, ${b.email}${b.phone ? ", " + b.phone : ""}.`,
    `Language: ${b.lang === "ar" ? "Arabic" : "English"}. Offer: 10% off all services.`,
  ].join(" ");
  const payload = {
    source: "eddekhar_landing", tags: ["Eddekhar referral", "focus:" + b.focus, "lang:" + b.lang],
    name: b.name, email: b.email, company: b.company, phone: b.phone || null,
    meeting: { start: b.start, end: b.end, meetUrl: b.meetUrl, eventId: b.eventId },
    utm: b.utm, page: b.page, referrer: b.referrer, consent: { pdpl: true, at: b.createdAt }, note,
  };
  if (!env.CRM_WEBHOOK_URL) { console.log("[crm stub]", JSON.stringify(payload)); return; }
  await fetch(env.CRM_WEBHOOK_URL, { method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + (env.CRM_API_KEY || "") }, body: JSON.stringify(payload) });
}

/* ---------- Storage (swap for the CRM or a DB; in-memory is for the stub only) ---------- */
const bookings = new Map();

const FOCUS = { hr: "HR Health Check", team: "Team & Workforce Check", unsure: "Not sure (decide in first 5 min)" };
const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
// Company emails only (mirrors the page): personal mailboxes are refused.
const FREE_MAIL = new Set(["gmail.com", "googlemail.com", "msn.com", "ymail.com", "rocketmail.com", "icloud.com", "me.com", "mac.com", "aol.com",
  "proton.me", "protonmail.com", "pm.me", "mail.com", "email.com", "zoho.com", "zohomail.com", "tutanota.com", "tuta.io", "fastmail.com",
  "hey.com", "inbox.com", "gmx.com", "mail.ru", "qq.com", "163.com", "126.com", "maktoob.com", "windowslive.com"]);
function isPersonal(email) {
  const d = String(email).trim().toLowerCase().split("@")[1] || "";
  return FREE_MAIL.has(d) || /^(yahoo|hotmail|outlook|live|gmx|yandex)\.[a-z.]+$/.test(d);
}

async function book(body, ip) {
  if (body.website) return [200, { id: "ok" }]; // honeypot: pretend success
  if (rateLimited(ip)) return [429, { error: "rate_limited" }];
  const name = String(body.name || "").trim().slice(0, 120);
  const email = String(body.email || "").trim().slice(0, 160);
  const company = String(body.company || "").trim().slice(0, 160);
  const focus = FOCUS[body.focus] ? body.focus : "unsure";
  const lang = body.lang === "en" ? "en" : "ar";
  if (!name || !emailRe.test(email) || !company || body.consent !== true) return [400, { error: "invalid_fields" }];
  if (isPersonal(email)) return [400, { error: "personal_email" }];
  const start = new Date(body.start), end = new Date(body.end);
  if (!isValidSlot(start, end)) return [400, { error: "invalid_slot" }];

  const key = start.toISOString();
  if (locks.has(key)) return [409, { error: "slot_taken" }];
  locks.add(key);
  try {
    const busy = await busyBetween(new Date(start.getTime() - RULES.buffer * 60000).toISOString(), new Date(end.getTime() + RULES.buffer * 60000).toISOString());
    const clash = [...bookings.values()].some((x) => Date.parse(x.start) < end.getTime() + RULES.buffer * 60000 && Date.parse(x.end) > start.getTime() - RULES.buffer * 60000);
    if (busy.length || clash) return [409, { error: "slot_taken" }];

    const id = crypto.randomUUID();
    const b = { id, token: sign(id), name, email, company, focus, focusLabel: FOCUS[focus], lang, start: start.toISOString(), end: end.toISOString(),
      utm: body.utm || {}, page: String(body.page || "").slice(0, 500), referrer: String(body.referrer || "").slice(0, 500), createdAt: new Date().toISOString() };

    if (cal) {
      const ev = await cal.events.insert({
        calendarId: CAL_ID, conferenceDataVersion: 1, sendUpdates: "all",
        requestBody: {
          summary: `${FOCUS[focus]} · ${company} (Eddekhar)`,
          description: `Eddekhar referral. ${name}, ${company}. Language: ${lang}. 10% discount applies.`,
          start: { dateTime: b.start, timeZone: TZ }, end: { dateTime: b.end, timeZone: TZ },
          attendees: [{ email }],
          conferenceData: { createRequest: { requestId: id, conferenceSolutionKey: { type: "hangoutsMeet" } } },
          reminders: { useDefault: false, overrides: [{ method: "email", minutes: 1440 }, { method: "popup", minutes: 60 }] },
          extendedProperties: { private: { bookingId: id, source: "eddekhar_landing" } },
        },
      });
      b.eventId = ev.data.id;
      b.meetUrl = ev.data.hangoutLink || null;
    } else if (GAS) {
      const ev = await gas("event", { summary: `${FOCUS[focus]} · ${company} (Eddekhar)`,
        description: `Eddekhar referral. ${name}, ${company}. Language: ${lang}. 10% discount applies.`,
        start: b.start, end: b.end, attendee: email, requestId: id });
      b.eventId = ev.eventId; b.meetUrl = ev.meetUrl || null;
    }
    bookings.set(id, b);
    const sent = await Promise.allSettled([sendConfirmation(b), notifyTeam(b), pushToCrm(b)]);
    sent.forEach((r, i) => { if (r.status === "rejected") console.error(["[mail] confirmation", "[mail] team", "[crm]"][i], r.reason && r.reason.message); });
    return [200, { id, token: b.token, meetUrl: b.meetUrl || null, calendar: !!(cal || GAS), mailed: !!mailer }];
  } finally { locks.delete(key); }
}

/* ---------- Static site: serves the built pages from ../dist ---------- */
const DIST = require("path").join(__dirname, "..", "dist");
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json", ".svg": "image/svg+xml",
  ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".ico": "image/x-icon", ".pdf": "application/pdf", ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml", ".woff2": "font/woff2" };
function serveStatic(pathname, res) {
  const path = require("path"), fs = require("fs");
  let rel = decodeURIComponent(pathname);
  if (rel.endsWith("/")) rel += "index.html";
  const file = path.normalize(path.join(DIST, rel));
  if (!file.startsWith(DIST)) return send(res, 404, { error: "not_found" });
  fs.stat(file, (err, st) => {
    if (!err && st.isDirectory()) { res.writeHead(301, { Location: pathname + "/" }); return res.end(); }
    if (err) { res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" }); return res.end('<p>Not found. <a href="/">Home</a></p>'); }
    const ext = path.extname(file).toLowerCase();
    res.writeHead(200, { "Content-Type": TYPES[ext] || "application/octet-stream",
      "Cache-Control": ext === ".html" ? "no-cache" : "public, max-age=86400" });
    fs.createReadStream(file).pipe(res);
  });
}

/* ---------- HTTP ---------- */
function send(res, code, obj) { res.writeHead(code, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }); res.end(JSON.stringify(obj)); }
function readJson(req) {
  return new Promise((ok) => { let d = ""; req.on("data", (c) => { d += c; if (d.length > 20000) req.destroy(); }); req.on("end", () => { try { ok(JSON.parse(d || "{}")); } catch (e) { ok({}); } }); });
}

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  const ip = (req.headers["x-forwarded-for"] || req.socket.remoteAddress || "").split(",")[0].trim();
  try {
    if (req.method === "GET" && url.pathname === "/api/slots") {
      const d = url.searchParams.get("date");
      if (!/^\d{4}-\d{2}-\d{2}$/.test(d || "")) return send(res, 400, { error: "invalid_date" });
      const dayStart = new Date(Date.parse(d + "T00:00:00Z") - OFFSET_MIN * 60000);
      const busy = await busyBetween(dayStart.toISOString(), new Date(dayStart.getTime() + 86400000).toISOString());
      // Pad busy blocks by the buffer so a slot never sits right against another meeting
      return send(res, 200, { timezone: TZ, busy: busy.map((b) => ({ start: new Date(Date.parse(b.start) - RULES.buffer * 60000).toISOString(), end: new Date(Date.parse(b.end) + RULES.buffer * 60000).toISOString() })) });
    }
    if (req.method === "POST" && url.pathname === "/api/book") { const [c, o] = await book(await readJson(req), ip); return send(res, c, o); }
    let m;
    if (req.method === "POST" && (m = url.pathname.match(/^\/api\/booking\/([\w-]+)\/phone$/))) {
      const body = await readJson(req); const b = bookings.get(m[1]);
      if (!b || !verify(b.id, body.token)) return send(res, 404, { error: "not_found" });
      b.phone = String(body.phone || "").replace(/[^\d+\s-]/g, "").slice(0, 20);
      await pushToCrm(b).catch(() => {});
      return send(res, 200, { ok: true, mailed: !!mailer });
    }
    if (req.method === "GET" && (m = url.pathname.match(/^\/api\/booking\/([\w-]+)\/(cancel|reschedule)$/))) {
      const b = bookings.get(m[1]);
      if (!b || !verify(b.id, url.searchParams.get("token"))) return send(res, 404, { error: "not_found" });
      if (cal && b.eventId) await cal.events.delete({ calendarId: CAL_ID, eventId: b.eventId, sendUpdates: "all" });
      else if (GAS && b.eventId) await gas("cancel", { eventId: b.eventId });
      bookings.delete(b.id);
      const back = `${env.PUBLIC_BASE_URL}/${b.lang}/${m[2] === "reschedule" ? "?rebook=1" : "?cancelled=1"}#book`;
      res.writeHead(302, { Location: back }); return res.end();
    }
    if (req.method === "GET" && url.pathname === "/api/health") {
      return send(res, 200, { calendar: !!(cal || GAS), mail: !!mailer, appsScript: gasStatus, calendarOwner: CAL_OWNER, mailFrom: FROM, team: TEAM });
    }
    if (req.method === "POST" && url.pathname === "/api/lead-magnet") {
      const body = await readJson(req);
      if (body.website) return send(res, 200, { ok: true });
      if (rateLimited(ip, 10) || !emailRe.test(String(body.email || ""))) return send(res, 400, { error: "invalid" });
      if (isPersonal(body.email)) return send(res, 400, { error: "personal_email" });
      await sendLeadMagnet(body);
      return send(res, 200, { ok: true, mailed: !!mailer });
    }
    if (req.method === "GET" || req.method === "HEAD") return serveStatic(url.pathname, res);
    send(res, 404, { error: "not_found" });
  } catch (err) {
    console.error(err);
    send(res, 500, { error: "server_error" });
  }
}).listen(PORT, () => console.log("site + booking api on :" + PORT + (cal || GAS ? "" : " (stub mode: no Google credentials)")));
