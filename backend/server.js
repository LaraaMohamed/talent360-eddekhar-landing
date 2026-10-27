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
 *   POST /api/lead-magnet                 checks the company email (format, not personal, domain has MX), returns a download link, alerts the team
 */
"use strict";

const http = require("http");
const crypto = require("crypto");
const { google } = require("googleapis");
const nodemailer = require("nodemailer");

const env = process.env;
// On Railway, fall back to the service's public domain when PUBLIC_BASE_URL is not set.
if (!env.PUBLIC_BASE_URL && env.RAILWAY_PUBLIC_DOMAIN) env.PUBLIC_BASE_URL = "https://" + env.RAILWAY_PUBLIC_DOMAIN;
// Everything (calendar, sender, team copies) runs from the Business Growth mailbox unless overridden.
const BG = "business-growth@talent-360.me";
const CAL_OWNER = env.CONSULTANT_EMAIL || BG;
const FROM = env.MAIL_FROM || `Talent360 <${env.SMTP_USER || BG}>`;
const TEAM = env.TEAM_EMAIL || BG;
// Calendars that must all be free for a slot to show, and people invited to every booking.
const AHMED = "darkawi@talent-360.me"; // Ahmed Al-Darkawi: the consultant whose calendar takes the bookings
const BUSY_CALS = (env.BUSY_CALENDARS || AHMED).split(",").map((x) => x.trim()).filter(Boolean);
const GUESTS = (env.BOOKING_GUESTS || "").split(",").map((x) => x.trim()).filter(Boolean);
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
// Each call has a timeout and retries transient failures (network, 5xx, Google rate limits) with backoff.
async function gas(action, payload, tries = 3) {
  let last;
  for (let i = 0; i < tries; i++) {
    try {
      const r = await fetch(GAS, { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8" }, redirect: "follow",
        signal: AbortSignal.timeout(30000), body: JSON.stringify(Object.assign({ action, key: env.APPS_SCRIPT_SECRET || "" }, payload)) });
      const text = await r.text();
      let j; try { j = JSON.parse(text); } catch (e) { throw Object.assign(new Error("apps script: non-JSON reply (" + r.status + "): " + text.slice(0, 160)), { retry: r.status >= 500 || r.status === 429 }); }
      if (j.error) throw Object.assign(new Error("apps script: " + j.error), { retry: !!j.retryable, code: j.error });
      return j;
    } catch (e) {
      last = e;
      const retry = e.retry || e.name === "TimeoutError" || e.name === "AbortError" || /fetch failed|ECONNRESET|ETIMEDOUT|EAI_AGAIN/i.test(e.message);
      if (!retry || i === tries - 1) break;
      await new Promise((ok) => setTimeout(ok, 1000 * Math.pow(3, i)));
    }
  }
  throw last;
}
let gasStatus = GAS ? "checking" : "not configured";
if (GAS) gas("ping", {}).then((j) => { gasStatus = "ok as " + j.account; console.log("[apps-script]", gasStatus); })
  .catch((e) => { gasStatus = e.message; console.error("[apps-script]", e.message); });
// Re-check the bridge every 30 minutes so /api/health shows its real state.
if (GAS) setInterval(() => gas("ping", {}, 1).then((j) => { gasStatus = "ok as " + j.account; }).catch((e) => { gasStatus = e.message; console.error("[apps-script] ping", e.message); }), 30 * 60000).unref();

/* Calendar events that failed to create are retried in the background (2, 5, 15, 30, 60, 120 min).
   The booking is already recorded and the team already notified; Google sends the client the invite once it exists.
   The queue lives in memory, so a restart drops it: the team email says when an invite still has to be sent by hand. */
const RETRY_MIN = [2, 5, 15, 30, 60, 120];
function queueEvent(b, payload, attempt = 0) {
  if (attempt >= RETRY_MIN.length) {
    console.error("[calendar] gave up on", b.id);
    if (mailer) mailer.sendMail({ from: FROM, to: TEAM, subject: `[Eddekhar booking] Calendar invite NOT created for ${b.company}`,
      text: `Please send the invite by hand.\n${b.name} <${b.email}>, ${b.company}\n${fmt(new Date(b.start), "en")} Riyadh time` }).catch(() => {});
    return;
  }
  setTimeout(async () => {
    try {
      const ev = await gas("event", payload);
      b.eventId = ev.eventId; b.meetUrl = ev.meetUrl || null;
      refreshBusy().catch(() => {});
      console.log("[calendar] created late for", b.id);
      if (mailer) mailer.sendMail({ from: FROM, to: TEAM, subject: `[Eddekhar booking] Calendar invite created for ${b.company}`,
        text: `The invite for ${b.name} <${b.email}> is now on the calendar.\nMeet: ${b.meetUrl || "(none)"}` }).catch(() => {});
    } catch (e) {
      if (e.code === "slot_taken") return console.error("[calendar] slot taken before late retry for", b.id);
      console.error("[calendar] retry", attempt + 1, "failed:", e.message);
      queueEvent(b, payload, attempt + 1);
    }
  }, RETRY_MIN[attempt] * 60000).unref();
}
const CAL_ID = env.CONSULTANT_CALENDAR_ID || AHMED;

async function busyBetween(timeMin, timeMax) {
  if (!cal && GAS) {
    try { return (await gas("busy", { timeMin, timeMax, calendars: BUSY_CALS })).busy || []; }
    // Keep the booking page working; the bridge re-checks free/busy under a lock before creating the event.
    catch (e) { console.error("[apps-script] busy:", e.message); return []; }
  }
  if (!cal) return []; // stub mode: everything free
  const r = await cal.freebusy.query({ requestBody: { timeMin, timeMax, timeZone: TZ, items: [{ id: CAL_ID }] } });
  return (r.data.calendars[CAL_ID] && r.data.calendars[CAL_ID].busy) || [];
}

// Free/busy for the whole booking horizon, fetched in one call and kept warm, so the calendar shows slots instantly.
// Bookings still re-check live free/busy (and the bridge re-checks under a lock), so a stale cache can never double-book.
const BUSY_TTL = 3 * 60000;
let busyCache = null, busyLoading = null;
function refreshBusy() {
  if (busyLoading) return busyLoading;
  const from = new Date(Date.now() - 86400000), to = new Date(Date.now() + (RULES.horizonDays + 2) * 86400000);
  busyLoading = busyBetween(from.toISOString(), to.toISOString())
    .then((busy) => { busyCache = { at: Date.now(), from: from.getTime(), to: to.getTime(), busy }; return busyCache; })
    .finally(() => { busyLoading = null; });
  return busyLoading;
}
async function busyForDay(a, z) {
  let c = busyCache;
  if (!c || a < c.from || z > c.to) c = await refreshBusy();
  else if (Date.now() - c.at > BUSY_TTL) refreshBusy().catch(() => {}); // serve now, refresh in the background
  return c.busy.filter((b) => Date.parse(b.end) > a && Date.parse(b.start) < z);
}
setInterval(() => refreshBusy().catch(() => {}), BUSY_TTL).unref();
refreshBusy().catch(() => {});

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
  return gas("mail", { to: m.to, subject: m.subject, text: m.text, html: m.html, replyTo: m.replyTo, fromName: "Talent360",
    attachment: a ? { name: a.filename, type: "application/pdf", data: require("fs").readFileSync(a.path).toString("base64") } : null });
} } : null);
function fmt(date, lang) {
  return new Intl.DateTimeFormat(lang === "ar" ? "ar-SA-u-ca-gregory-nu-latn" : "en-GB", { timeZone: TZ, dateStyle: "full", timeStyle: "short" }).format(date);
}
async function sendConfirmation(b) {
  if (!mailer) return;
  const ar = b.lang === "ar", when = fmt(new Date(b.start), b.lang);
  const cancel = `${env.PUBLIC_BASE_URL}/api/booking/${b.id}/cancel?token=${b.token}`;
  const resched = `${env.PUBLIC_BASE_URL}/api/booking/${b.id}/reschedule?token=${b.token}`;
  const meet = b.meetUrl ? `<a href="${esc(b.meetUrl)}" style="color:#168C7C">${esc(b.meetUrl)}</a>` : esc(ar ? "يصلك مع دعوة التقويم" : "Sent with your calendar invite");
  const consultant = ar ? env.CONSULTANT_NAME_AR : env.CONSULTANT_NAME_EN;
  const html = emailHtml(b.lang, {
    title: ar ? `شكرًا ${b.name}، تم تأكيد جلستك` : `Thank you ${b.name}, your session is confirmed`,
    paras: ar ? ["يسعدنا لقاؤك. ستراجع مع مستشارنا وضع شركتك في 30 دقيقة، وتستلم بعدها ثلاث أولويات مكتوبة وقائمة أسعارك بخصم إدخار."]
              : ["We look forward to meeting you. In 30 minutes you'll review your company's situation with our consultant, then receive three written priorities and your price list with the Eddekhar discount."],
    rows: [[ar ? "الموعد" : "When", esc(when) + (ar ? " (بتوقيت الرياض)" : " (Riyadh time)")], [ar ? "الفحص" : "Check", esc(b.focusLabel)], [ar ? "رابط الاجتماع" : "Meeting link", meet]]
      .concat(consultant ? [[ar ? "المستشار" : "Consultant", esc(consultant)]] : []),
    note: ar ? `تحتاج تغيير الموعد؟ <a href="${resched}" style="color:#168C7C">أعد الجدولة</a> أو <a href="${cancel}" style="color:#168C7C">ألغِ الحجز</a>.`
             : `Need to change it? <a href="${resched}" style="color:#168C7C">Reschedule</a> or <a href="${cancel}" style="color:#168C7C">cancel</a>.`,
    cta: ar ? "تعرّف على خدماتنا" : "Explore our services", ctaUrl: `${env.PUBLIC_BASE_URL}/${b.lang}/#help`,
  });
  const text = ar ? `تم تأكيد جلستك المجانية مع موارد ومهارات\n\nالموعد: ${when} (بتوقيت الرياض)\nرابط الاجتماع: ${b.meetUrl || "يصلك مع دعوة التقويم"}\nخصم إدخار 10% مطبق تلقائيًا.\n\nإعادة الجدولة: ${resched}\nالإلغاء: ${cancel}`
                  : `Your free session with Talent360 is confirmed\n\nWhen: ${when} (Riyadh time)\nMeeting link: ${b.meetUrl || "sent with your calendar invite"}\n10% Eddekhar discount applied automatically.\n\nReschedule: ${resched}\nCancel: ${cancel}`;
  await mailer.sendMail({ from: FROM, to: b.email, replyTo: TEAM,
    subject: ar ? "تم تأكيد جلستك المجانية | موارد ومهارات × إدخار" : "Your free HR check is confirmed | Talent360 × Eddekhar", text, html });
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
  benefits_eg: ["دليل مزايا الموظفين في مصر 2026", "Employee benefits in Egypt, 2026"],
  hcm_guide: ["إدارة الموارد البشرية بالكامل أم موظف داخلي؟", "HCM vs an in-house HR hire"],
};
/* ---------- Branded HTML email (table layout, inline styles, works in Gmail and Outlook) ---------- */
const esc = (x) => String(x).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
function emailHtml(lang, o) {
  const ar = lang === "ar", dir = ar ? "rtl" : "ltr", al = ar ? "right" : "left";
  const base = env.PUBLIC_BASE_URL || "https://talent360-eddekhar.onrender.com";
  const font = ar ? "Tahoma,Arial,sans-serif" : "Arial,Helvetica,sans-serif";
  const rows = (o.rows || []).map(([k, v]) => `<tr><td style="padding:9px 14px;border-bottom:1px solid #EDF2F6;color:#5A6785;font-size:14px;width:38%">${esc(k)}</td><td style="padding:9px 14px;border-bottom:1px solid #EDF2F6;color:#0E183C;font-weight:bold;font-size:14px">${v}</td></tr>`).join("");
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#EEF6F6">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#EEF6F6"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" dir="${dir}" style="max-width:600px;width:100%;background:#ffffff;border-radius:18px;overflow:hidden;font-family:${font};text-align:${al}">
 <tr><td style="background:#0E183C;padding:22px 28px"><img src="${base}/assets/img/brand/mawared-mark-white.png" alt="${ar ? "موارد ومهارات" : "Talent360"}" height="40" style="display:block;height:40px;border:0"></td></tr>
 <tr><td style="background:#1FC9B1;height:4px;line-height:4px;font-size:0">&nbsp;</td></tr>
 <tr><td style="padding:30px 28px 8px"><h1 style="margin:0 0 12px;font-size:22px;line-height:1.4;color:#0E183C">${esc(o.title)}</h1>
  ${o.paras.map((x) => `<p style="margin:0 0 14px;font-size:15px;line-height:1.75;color:#26324D">${x}</p>`).join("")}</td></tr>
 ${rows ? `<tr><td style="padding:4px 28px 14px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #DCE7EE;border-radius:12px;border-collapse:separate">${rows}</table></td></tr>` : ""}
 ${o.note ? `<tr><td style="padding:0 28px 14px"><div style="background:#E3F6F3;border-radius:12px;padding:12px 16px;font-size:14px;line-height:1.7;color:#0E183C">${o.note}</div></td></tr>` : ""}
 <tr><td style="padding:6px 28px 26px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#4E7A3D;border-radius:14px"><tr><td style="padding:18px 20px;color:#ffffff">
  <div style="font-size:26px;font-weight:bold;line-height:1">10%</div>
  <div style="font-size:14px;line-height:1.6;margin:6px 0 14px">${ar ? "خصم على كل خدمات موارد ومهارات لعملاء إدخار، يُطبَّق تلقائيًا." : "Off every Talent360 service for Eddekhar clients, applied automatically."}</div>
  <a href="${o.ctaUrl}" style="display:inline-block;background:#1FC9B1;color:#0E183C;font-weight:bold;font-size:15px;text-decoration:none;padding:12px 24px;border-radius:999px">${esc(o.cta)}</a>
 </td></tr></table></td></tr>
 <tr><td style="padding:18px 28px;background:#F6FAFC;border-top:1px solid #E3EBF1;font-size:12px;line-height:1.8;color:#5A6785">
  ${ar ? "فريق موارد ومهارات" : "The Talent360 team"} · <a href="mailto:business-growth@talent-360.me" style="color:#168C7C">business-growth@talent-360.me</a> · <span dir="ltr">+966 592060727</span><br>
  ${ar ? "الرياض · القاهرة" : "Riyadh · Cairo"} · <a href="https://talent-360.me" style="color:#168C7C">talent-360.me</a><br>
  ${ar ? "بالشراكة مع إدخار" : "In partnership with Eddekhar"}
 </td></tr>
</table></td></tr></table></body></html>`;
}

/* Lead magnets: the guide goes straight to the company inbox as an attachment, with a thank-you and a CTA.
   Only the inbox owner receives it, so the company address is verified by delivery. */
function leadFile(tool, lang) {
  const path = require("path"), fs = require("fs");
  return [tool + "-" + lang + ".pdf", tool + ".pdf"].map((f) => path.join(__dirname, "files", f)).find((f) => fs.existsSync(f)) || null;
}
// Until a mailbox is connected, the page hands the guide over directly through a short-lived signed link.
function guideLink(tool, lang) {
  const p = Buffer.from(JSON.stringify({ t: tool, l: lang, x: Date.now() + 3600000 })).toString("base64url");
  return "/api/guide?t=" + p + "." + sign("guide:" + p);
}
function readGuideLink(tok) {
  const [p, sig] = String(tok || "").split(".");
  if (!p || !sig || !verify("guide:" + p, sig)) return null;
  try { const o = JSON.parse(Buffer.from(p, "base64url").toString()); return o.x > Date.now() ? o : null; } catch (e) { return null; }
}
async function sendLeadMagnet(body) {
  const tool = String(body.tool || "").replace(/[^\w-]/g, "");
  const lang = body.lang === "en" ? "en" : "ar", ar = lang === "ar";
  const title = (LEAD_TITLES[tool] || [tool, tool])[ar ? 0 : 1];
  const email = String(body.email).trim().slice(0, 160);
  const file = leadFile(tool, lang);
  console.log("[lead-magnet]", tool, email, file ? "file" : "no-file");
  const crm = { source: "eddekhar_landing", tags: ["Eddekhar referral", "lead_magnet:" + tool, "lang:" + lang], email, utm: body.utm,
    note: `Eddekhar referral. Requested "${title}" from the landing page${file ? "; the guide was emailed to their company inbox" : ""}.` };
  if (env.CRM_WEBHOOK_URL) fetch(env.CRM_WEBHOOK_URL, { method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + (env.CRM_API_KEY || "") }, body: JSON.stringify(crm) }).catch((e) => console.error("[crm]", e.message));
  else console.log("[crm stub]", JSON.stringify(crm));
  // Visitor emails are switched off until a dedicated sending domain is set up (protects talent-360.me's reputation).
  // The visitor gets an instant download; the team still gets an internal alert. Set SEND_VISITOR_EMAIL=true to email the guide again.
  if (!mailer || !SEND_VISITOR_EMAIL) {
    if (mailer) mailer.sendMail({ from: FROM, to: TEAM, replyTo: email, subject: `[Eddekhar lead] ${title} downloaded by ${email}`,
      text: `${email} downloaded "${title}" (${tool}) from the Eddekhar landing page (${lang}).` + (file ? "" : "\nNo file is configured for this tool yet: please send it by hand.") })
      .catch((e) => console.error("[mail] team", e.message));
    return { sent: false, teamNotified: !!mailer, download: file ? guideLink(tool, lang) : null };
  }
  const book = `${env.PUBLIC_BASE_URL}/${lang}/#book`;
  const html = emailHtml(lang, {
    title: ar ? "شكرًا لاهتمامك، دليلك مرفق" : "Thank you, your guide is attached",
    paras: file ? (ar
      ? [`يسعدنا أن نرسل لك <b>${esc(title)}</b> مرفقًا بهذه الرسالة.`, "أعددنا الدليل ليكون مرجعًا عمليًا لصاحب العمل: الأحكام بأرقام المواد، وأمثلة محسوبة، وقائمة تحقق تراجع بها وضع شركتك.", "وإذا أردت أن نطبّق ما فيه على شركتك تحديدًا، يراجع معك أحد مستشارينا العقود والرواتب والتأمينات في جلسة مجانية مدتها 30 دقيقة، وتخرج منها بثلاث أولويات مكتوبة."]
      : [`We're pleased to send you <b>${esc(title)}</b>, attached to this email.`, "It is built as a practical employer reference: rules with their article numbers, worked examples and a checklist to review where your company stands.", "If you'd like to apply it to your company, one of our consultants will review your contracts, payroll and insurance with you in a free 30-minute session, and you'll leave with three written priorities."])
      : (ar ? [`شكرًا لطلبك <b>${esc(title)}</b>.`, "سيرسله لك فريقنا خلال يوم عمل واحد."] : [`Thank you for requesting <b>${esc(title)}</b>.`, "Our team will send it to you within one working day."]),
    cta: ar ? "احجز فحصك المجاني" : "Book your free HR check", ctaUrl: book,
  });
  const text = ar ? `شكرًا لاهتمامك. مرفق لك: ${title}.\n\nاحجز فحصك المجاني (30 دقيقة) مع خصم إدخار 10%: ${book}\n\nفريق موارد ومهارات\nbusiness-growth@talent-360.me`
                  : `Thank you for your interest. Attached: ${title}.\n\nBook your free 30-minute HR check, with the 10% Eddekhar discount: ${book}\n\nThe Talent360 team\nbusiness-growth@talent-360.me`;
  await mailer.sendMail({ from: FROM, to: email, replyTo: TEAM, subject: ar ? `${title} | موارد ومهارات` : `${title} | Talent360`, text, html,
    attachments: file ? [{ filename: require("path").basename(file), path: file }] : [] });
  mailer.sendMail({ from: FROM, to: TEAM, replyTo: email, subject: `[Eddekhar lead] ${title} sent to ${email}`,
    text: `${email} requested "${title}" (${tool}) from the Eddekhar landing page (${lang}).` + (file ? " The guide was emailed to them." : "\nNo file is configured for this tool yet: please send it by hand.") })
    .catch((e) => console.error("[mail] team", e.message));
  return { sent: true };
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
const SEND_VISITOR_EMAIL = env.SEND_VISITOR_EMAIL === "true";
// A real company email must be on a domain that receives mail (has MX records). DNS outages don't block visitors.
const dnsP = require("dns").promises, mxCache = new Map();
async function receivesMail(email) {
  const d = String(email).trim().toLowerCase().split("@")[1] || "";
  if (mxCache.has(d)) return mxCache.get(d);
  const ok = await Promise.race([
    dnsP.resolveMx(d).then((r) => r.some((x) => x.exchange && x.exchange !== "."), (e) => (e.code === "ENOTFOUND" || e.code === "ENODATA" ? false : true)),
    new Promise((r) => setTimeout(() => r(true), 4000)),
  ]);
  // If even a known domain fails, the server's DNS is down: let the visitor through rather than block everyone.
  if (!ok && !(await dnsP.resolveMx("gmail.com").then(() => true, () => false))) return true;
  mxCache.set(d, ok);
  return ok;
}
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
      refreshBusy().catch(() => {});
      b.meetUrl = ev.data.hangoutLink || null;
    } else if (GAS) {
      const payload = { summary: `${FOCUS[focus]} · ${company} (Eddekhar)`,
        description: `Eddekhar referral. ${name}, ${company}. Language: ${lang}. 10% discount applies.`,
        start: b.start, end: b.end, attendee: email, guests: GUESTS, requestId: id, calendarId: CAL_ID };
      try {
        const ev = await gas("event", payload);
        b.eventId = ev.eventId; b.meetUrl = ev.meetUrl || null;
        refreshBusy().catch(() => {});
      } catch (e) {
        if (e.code === "slot_taken") return [409, { error: "slot_taken" }];
        console.error("[calendar] event failed, queued for retry:", e.message);
        queueEvent(b, payload);
      }
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
      const busy = await busyForDay(dayStart.getTime(), dayStart.getTime() + 86400000);
      // Pad busy blocks by the buffer so a slot never sits right against another meeting
      return send(res, 200, { timezone: TZ, busy: busy.map((b) => ({ start: new Date(Date.parse(b.start) - RULES.buffer * 60000).toISOString(), end: new Date(Date.parse(b.end) + RULES.buffer * 60000).toISOString() })) });
    }
    if (req.method === "POST" && url.pathname === "/api/book") { const [c, o] = await book(await readJson(req), ip); return send(res, c, o); }
    let m;
    if (req.method === "POST" && (m = url.pathname.match(/^\/api\/booking\/([\w-]+)\/phone$/))) {
      // The signed token proves the booking; the booking itself may be gone from memory after a restart,
      // so the phone is always mailed to the team with whatever details the page sent along.
      const body = await readJson(req);
      if (!verify(m[1], body.token)) return send(res, 404, { error: "not_found" });
      const phone = String(body.phone || "").replace(/[^\d+\s-]/g, "").slice(0, 20);
      const clip = (v) => String(v || "").slice(0, 160);
      const b = bookings.get(m[1]) || { id: m[1], name: clip(body.name), email: clip(body.email), company: clip(body.company), start: clip(body.start) };
      b.phone = phone;
      if (bookings.has(m[1])) await pushToCrm(b).catch(() => {});
      if (mailer) mailer.sendMail({ from: FROM, to: TEAM, replyTo: emailRe.test(b.email) ? b.email : undefined,
        subject: `[Eddekhar booking] Phone for ${b.company || b.name || m[1]}`,
        text: `${b.name || "(name)"}, ${b.company || "(company)"}, ${b.email || "(email)"}\nPhone: ${phone}${b.start ? "\nSession: " + b.start : ""}` })
        .catch((e) => console.error("[mail] phone", e.message));
      return send(res, 200, { ok: true, mailed: !!mailer });
    }
    if (req.method === "GET" && (m = url.pathname.match(/^\/api\/booking\/([\w-]+)\/(cancel|reschedule)$/))) {
      const b = bookings.get(m[1]);
      if (!b || !verify(b.id, url.searchParams.get("token"))) return send(res, 404, { error: "not_found" });
      if (cal && b.eventId) await cal.events.delete({ calendarId: CAL_ID, eventId: b.eventId, sendUpdates: "all" });
      else if (GAS && b.eventId) await gas("cancel", { eventId: b.eventId, calendarId: CAL_ID });
      refreshBusy().catch(() => {});
      bookings.delete(b.id);
      const back = `${env.PUBLIC_BASE_URL}/${b.lang}/${m[2] === "reschedule" ? "?rebook=1" : "?cancelled=1"}#book`;
      res.writeHead(302, { Location: back }); return res.end();
    }
    if (req.method === "GET" && url.pathname === "/api/guide") {
      const o = readGuideLink(url.searchParams.get("t")); const f = o && leadFile(o.t, o.l);
      if (!f) return send(res, 410, { error: "expired" });
      res.writeHead(200, { "Content-Type": "application/pdf", "Content-Disposition": `attachment; filename="${require("path").basename(f)}"`, "Cache-Control": "no-store" });
      return require("fs").createReadStream(f).pipe(res);
    }
    if (req.method === "GET" && url.pathname === "/api/health") {
      return send(res, 200, { calendar: !!(cal || GAS), mail: !!mailer, appsScript: gasStatus, busyCalendars: BUSY_CALS, guests: GUESTS, calendarOwner: CAL_OWNER, mailFrom: FROM, team: TEAM });
    }
    if (req.method === "POST" && url.pathname === "/api/lead-magnet") {
      const body = await readJson(req);
      if (body.website) return send(res, 200, { ok: true });
      if (rateLimited(ip, 10) || !emailRe.test(String(body.email || ""))) return send(res, 400, { error: "invalid" });
      if (isPersonal(body.email)) return send(res, 400, { error: "personal_email" });
      if (!(await receivesMail(body.email))) return send(res, 400, { error: "no_mail_domain" });
      const r = await sendLeadMagnet(body);
      return send(res, 200, Object.assign({ ok: true, mailed: !!mailer }, r));
    }
    if (req.method === "GET" || req.method === "HEAD") return serveStatic(url.pathname, res);
    send(res, 404, { error: "not_found" });
  } catch (err) {
    console.error(err);
    send(res, 500, { error: "server_error" });
  }
}).listen(PORT, () => console.log("site + booking api on :" + PORT + (cal || GAS ? "" : " (stub mode: no Google credentials)")));
