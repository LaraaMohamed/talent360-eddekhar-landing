/* Talent360 × Eddekhar landing page behaviour.
   No dependencies. Works without the booking API (falls back to locally
   generated slots and a clearly labelled preview confirmation). */
(function () {
  "use strict";

  var doc = document.documentElement;
  var LANG = doc.lang === "en" ? "en" : "ar";
  var T = JSON.parse(document.getElementById("i18n").textContent);
  var CFG = window.T360_CONFIG || {};
  var API = CFG.apiBase || "/api";
  var TZ = "Asia/Riyadh";
  var RIYADH_OFFSET_MIN = 180; // GMT+3, no DST

  function store(kind, key, val) {
    try {
      var s = kind === "local" ? window.localStorage : window.sessionStorage;
      if (val === undefined) return s.getItem(key);
      s.setItem(key, val);
    } catch (e) { return null; }
  }

  /* ---------- Analytics: dataLayer events ---------- */
  window.dataLayer = window.dataLayer || [];
  function track(event, data) {
    var payload = Object.assign({ event: event, lang: LANG }, data || {});
    window.dataLayer.push(payload);
    if (CFG.debug) console.log("[track]", payload);
  }

  /* ---------- UTM capture (stored for the session, sent with the booking) ---------- */
  var utm = {};
  (function () {
    var p = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (k) {
      if (p.get(k)) utm[k] = p.get(k);
    });
    if (Object.keys(utm).length) store("session", "t360_utm", JSON.stringify(utm));
    else { try { utm = JSON.parse(store("session", "t360_utm") || "{}") || {}; } catch (e) { utm = {}; } }
    if (!utm.utm_source) { utm.utm_source = "eddekhar"; utm.utm_medium = "partner"; utm.inferred = "true"; }
    // Keep UTMs on the language toggle so attribution survives the switch
    var qs = new URLSearchParams();
    Object.keys(utm).forEach(function (k) { if (k.indexOf("utm_") === 0) qs.set(k, utm[k]); });
    document.querySelectorAll("[data-lang-link]").forEach(function (a) {
      a.setAttribute("href", a.getAttribute("href").split("?")[0] + "?" + qs.toString());
    });
  })();

  /* ---------- Language memory ---------- */
  store("local", "t360_lang", LANG);
  document.querySelectorAll("[data-lang-link]").forEach(function (a) {
    a.addEventListener("click", function () {
      store("local", "t360_lang", a.getAttribute("hreflang").slice(0, 2));
      track("language_toggle", { to: a.getAttribute("hreflang") });
    });
  });

  /* ---------- Theme toggle ---------- */
  var themeBtn = document.getElementById("theme-toggle");
  var saved = store("local", "t360_theme");
  if (saved) doc.setAttribute("data-theme", saved);
  function currentTheme() {
    var t = doc.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function paintThemeBtn() {
    if (!themeBtn) return;
    var dark = currentTheme() === "dark";
    themeBtn.setAttribute("aria-pressed", String(dark));
    themeBtn.setAttribute("aria-label", dark ? T.themeLight : T.themeDark);
    themeBtn.innerHTML = dark
      ? '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
      : '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  }
  if (themeBtn) {
    paintThemeBtn();
    themeBtn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      doc.setAttribute("data-theme", next);
      store("local", "t360_theme", next);
      paintThemeBtn();
    });
  }

  /* ---------- CTA tracking + focus preselect ---------- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-cta]");
    if (!a) return;
    track("cta_click", { cta: a.getAttribute("data-cta") });
    var focus = a.getAttribute("data-focus");
    if (focus) {
      var r = document.querySelector('input[name="focus"][value="' + focus + '"]');
      if (r) { r.checked = true; r.dispatchEvent(new Event("change", { bubbles: true })); }
    }
  });

  /* ---------- Marquee pause control ---------- */
  var mq = document.querySelector(".marquee");
  var mqBtn = document.getElementById("marquee-toggle");
  if (mq && mqBtn) {
    mqBtn.addEventListener("click", function () {
      var paused = mq.classList.toggle("paused");
      mqBtn.textContent = paused ? T.marqueePlay : T.marqueePause;
      mqBtn.setAttribute("aria-pressed", String(paused));
    });
  }

  /* ---------- Sticky mobile CTA after hero ---------- */
  var sticky = document.querySelector(".sticky-cta");
  var hero = document.querySelector(".hero");
  var booking = document.getElementById("book");
  if (sticky && hero && "IntersectionObserver" in window) {
    var heroGone = false, bookingVisible = false;
    function paint() { sticky.classList.toggle("show", heroGone && !bookingVisible); sticky.setAttribute("aria-hidden", String(!(heroGone && !bookingVisible))); }
    new IntersectionObserver(function (en) { heroGone = !en[0].isIntersecting; paint(); }).observe(hero);
    if (booking) new IntersectionObserver(function (en) { bookingVisible = en[0].isIntersecting; paint(); }, { threshold: 0.15 }).observe(booking);
  }

  /* ---------- Scroll depth ---------- */
  var depths = [25, 50, 75, 100], sent = {};
  window.addEventListener("scroll", function () {
    var h = document.documentElement.scrollHeight - innerHeight;
    if (h <= 0) return;
    var pct = (scrollY / h) * 100;
    depths.forEach(function (d) { if (pct >= d - 1 && !sent[d]) { sent[d] = 1; track("scroll_depth", { percent: d }); } });
  }, { passive: true });

  /* ---------- Ecosystem tabs ---------- */
  document.querySelectorAll("[role=tablist]").forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll("[role=tab]"));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var dir = (e.key === "ArrowRight") ? 1 : (e.key === "ArrowLeft") ? -1 : 0;
        if (!dir) return;
        if (doc.dir === "rtl") dir = -dir;
        var n = tabs[(i + dir + tabs.length) % tabs.length];
        n.focus(); select(n);
      });
    });
  });

  /* ---------- Expert flip card ---------- */
  document.querySelectorAll("[data-flip]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var card = btn.closest(".flip");
      var flipped = card.classList.toggle("is-flipped");
      card.querySelector(".flip-front").setAttribute("aria-hidden", String(flipped));
      card.querySelector(".flip-back").setAttribute("aria-hidden", String(!flipped));
      card.querySelector(flipped ? ".flip-back [data-flip]" : ".flip-front [data-flip]").focus();
    });
  });

  /* =========================================================
     BOOKING
     Rules: Sun–Thu, 10:00–16:00 Riyadh, 30-min sessions,
     15-min buffer, 24h minimum notice.
     ========================================================= */
  var form = document.getElementById("booking-form");
  if (!form) return;

  var RULES = { days: [0, 1, 2, 3, 4], startMin: 600, endMin: 960, len: 30, buffer: 15, noticeH: 24, horizon: 10 };
  var state = { focus: null, day: null, slot: null, showLocal: false, booking: null };
  var daysEl = document.getElementById("bk-days");
  var slotsEl = document.getElementById("bk-slots");
  var errEl = document.getElementById("bk-error");
  var submitBtn = document.getElementById("bk-submit");
  var summaryEl = document.getElementById("bk-summary");
  var tzBtn = document.getElementById("bk-tz");
  var tzLbl = document.getElementById("bk-tz-label");
  var locale = LANG === "ar" ? "ar-SA-u-ca-gregory-nu-latn" : "en-GB";

  function riyadhParts(date) {
    // A Date shifted so its UTC fields read as Riyadh wall time
    return new Date(date.getTime() + RIYADH_OFFSET_MIN * 60000);
  }
  function utcFromRiyadh(y, m, d, minutes) {
    return new Date(Date.UTC(y, m, d, 0, minutes) - RIYADH_OFFSET_MIN * 60000);
  }
  function fmtTime(date, local) {
    return new Intl.DateTimeFormat(locale, { hour: "2-digit", minute: "2-digit", hour12: false, timeZone: local ? undefined : TZ }).format(date);
  }
  function fmtDay(date, opts) {
    return new Intl.DateTimeFormat(locale, Object.assign({ timeZone: TZ }, opts)).format(date);
  }

  function workingDays() {
    var out = [], now = new Date();
    var r = riyadhParts(now);
    var y = r.getUTCFullYear(), m = r.getUTCMonth(), d = r.getUTCDate();
    for (var i = 0; out.length < RULES.horizon && i < 30; i++) {
      var noon = utcFromRiyadh(y, m, d + i, 720);
      var dow = riyadhParts(noon).getUTCDay();
      if (RULES.days.indexOf(dow) === -1) continue;
      var slots = slotsFor(y, m, d + i);
      if (slots.length) out.push({ key: noon.toISOString().slice(0, 10), noon: noon, ymd: [y, m, d + i], slots: slots });
    }
    return out;
  }
  function slotsFor(y, m, d) {
    var res = [], earliest = Date.now() + RULES.noticeH * 3600000;
    for (var t = RULES.startMin; t + RULES.len <= RULES.endMin; t += RULES.len + RULES.buffer) {
      var start = utcFromRiyadh(y, m, d, t);
      if (start.getTime() >= earliest) res.push({ start: start, end: new Date(start.getTime() + RULES.len * 60000), busy: false });
    }
    return res;
  }

  var DAYS = workingDays();

  var PAGE = 5, prevBtn = document.getElementById("bk-prev"), nextBtn = document.getElementById("bk-next");
  var monthEl = document.getElementById("bk-month"), slotsTitle = document.getElementById("bk-slots-title");
  state.page = 0;
  if (prevBtn) prevBtn.addEventListener("click", function () { if (state.page > 0) { state.page--; renderDays(); } });
  if (nextBtn) nextBtn.addEventListener("click", function () { if ((state.page + 1) * PAGE < DAYS.length) { state.page++; renderDays(); } });

  function renderDays() {
    daysEl.innerHTML = "";
    var first = state.page * PAGE, shown = DAYS.slice(first, first + PAGE);
    if (monthEl && shown.length) {
      var m1 = fmtDay(shown[0].noon, { month: "long", year: "numeric" }), m2 = fmtDay(shown[shown.length - 1].noon, { month: "long", year: "numeric" });
      monthEl.textContent = m1 === m2 ? m1 : fmtDay(shown[0].noon, { month: "long" }) + " – " + m2;
    }
    if (prevBtn) prevBtn.disabled = state.page === 0;
    if (nextBtn) nextBtn.disabled = first + PAGE >= DAYS.length;
    if (slotsTitle && DAYS[state.day]) slotsTitle.textContent = T.slotsFor + " · " + fmtDay(DAYS[state.day].noon, { weekday: "long", day: "numeric", month: "long" });
    shown.forEach(function (day, k) {
      var idx = first + k;
      var b = document.createElement("button");
      b.type = "button"; b.className = "day";
      b.setAttribute("aria-pressed", String(state.day === idx));
      b.setAttribute("aria-label", fmtDay(day.noon, { weekday: "long", day: "numeric", month: "long" }));
      b.innerHTML = '<span class="dow">' + fmtDay(day.noon, { weekday: "short" }) + '</span><span class="dnum">' +
        fmtDay(day.noon, { day: "numeric" }) + "</span>";
      b.addEventListener("click", function () { state.day = idx; state.slot = null; renderDays(); loadSlots(); validate(); });
      daysEl.appendChild(b);
    });
  }

  function loadSlots() {
    var day = DAYS[state.day];
    slotsEl.innerHTML = '<p class="slot-empty">' + T.loading + "</p>";
    // Ask the backend which slots are free on the consultant's calendar
    fetch(API + "/slots?date=" + day.key + "&lang=" + LANG, { headers: { Accept: "application/json" } })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (data) {
        var busy = (data.busy || []).map(function (b) { return [Date.parse(b.start), Date.parse(b.end)]; });
        day.slots.forEach(function (s) {
          s.busy = busy.some(function (b) { return s.start.getTime() < b[1] && s.end.getTime() > b[0]; });
        });
        renderSlots();
      })
      .catch(function () { state.preview = true; renderSlots(); });
  }

  function renderSlots() {
    var day = DAYS[state.day];
    slotsEl.innerHTML = "";
    if (!day) return;
    var any = false;
    day.slots.forEach(function (s, i) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "slot";
      b.textContent = fmtTime(s.start, state.showLocal);
      b.disabled = s.busy;
      if (!s.busy) any = true;
      b.setAttribute("aria-pressed", String(state.slot === i));
      b.setAttribute("aria-label", fmtTime(s.start, state.showLocal) + (s.busy ? " — " + T.taken : ""));
      b.addEventListener("click", function () {
        state.slot = i; renderSlots(); validate();
        track("slot_selected", { date: day.key, time: fmtTime(s.start, false) });
      });
      slotsEl.appendChild(b);
    });
    if (!any) slotsEl.innerHTML = '<p class="slot-empty">' + T.noSlots + "</p>";
  }

  tzBtn.addEventListener("click", function () {
    state.showLocal = !state.showLocal;
    var localTz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    tzLbl.textContent = state.showLocal ? T.tzLocal.replace("{tz}", localTz) : T.tzRiyadh;
    tzBtn.textContent = state.showLocal ? T.showRiyadh : T.showLocal;
    renderSlots();
  });

  form.addEventListener("change", function (e) {
    if (e.target.name === "focus") { state.focus = e.target.value; validate(); }
  });
  form.addEventListener("input", validate);

  /* ---------- Work email only: personal mailboxes are rejected ---------- */
  var FREE_MAIL = ["gmail.com", "googlemail.com", "msn.com", "ymail.com", "rocketmail.com", "icloud.com", "me.com", "mac.com", "aol.com",
    "proton.me", "protonmail.com", "pm.me", "mail.com", "email.com", "zoho.com", "zohomail.com", "tutanota.com", "tuta.io", "fastmail.com",
    "hey.com", "inbox.com", "gmx.com", "mail.ru", "qq.com", "163.com", "126.com", "maktoob.com", "windowslive.com"];
  function emailState(v) {
    v = String(v || "").trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return "invalid";
    var d = v.split("@")[1];
    if (FREE_MAIL.indexOf(d) > -1 || /^(yahoo|hotmail|outlook|live|gmx|yandex)\.[a-z.]+$/.test(d)) return "personal";
    return "ok";
  }
  function emailMsg(st) { return st === "personal" ? T.emailPersonal : T.emailInvalid; }

  function chosen() {
    var d = DAYS[state.day];
    return d && state.slot !== null ? d.slots[state.slot] : null;
  }

  function validate() {
    var s = chosen();
    if (s) {
      summaryEl.hidden = false;
      var focusLbl = state.focus ? T.focus[state.focus] : T.focus.unsure;
      summaryEl.textContent = T.summary
        .replace("{focus}", focusLbl)
        .replace("{date}", fmtDay(s.start, { weekday: "long", day: "numeric", month: "long" }))
        .replace("{time}", fmtTime(s.start, false));
    } else summaryEl.hidden = true;
    var ok = !!s && form.name.value.trim() && emailState(form.email.value) === "ok" && form.company.value.trim() && form.consent.checked;
    submitBtn.disabled = !ok;
    return ok;
  }

  form.email.addEventListener("blur", function () {
    var es = emailState(form.email.value);
    errEl.textContent = form.email.value.trim() && es !== "ok" ? emailMsg(es) : "";
  });
  form.email.addEventListener("input", function () { if (emailState(form.email.value) === "ok") errEl.textContent = ""; });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    errEl.textContent = "";
    if (!validate()) { var es = emailState(form.email.value); errEl.textContent = es !== "ok" && form.email.value.trim() ? emailMsg(es) : T.fixFields; return; }
    var s = chosen();
    var payload = {
      focus: state.focus || "unsure",
      start: s.start.toISOString(), end: s.end.toISOString(), timezone: TZ,
      name: form.name.value.trim(), email: form.email.value.trim(), company: form.company.value.trim(),
      consent: true, website: form.website.value, // honeypot
      lang: LANG, utm: utm, page: location.href, referrer: document.referrer || ""
    };
    submitBtn.disabled = true; submitBtn.textContent = T.booking;
    fetch(API + "/book", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); })
      .then(function (res) { confirmed(s, res, false); })
      .catch(function (err) {
        if (err && err.error === "slot_taken") {
          errEl.textContent = T.slotTaken; DAYS[state.day].slots[state.slot].busy = true; state.slot = null; renderSlots();
          submitBtn.textContent = T.submit; validate(); return;
        }
        if (err && err.error === "personal_email") { errEl.textContent = T.emailPersonal; submitBtn.textContent = T.submit; validate(); return; }
        if (err && err.error) { errEl.textContent = T.genericError; submitBtn.textContent = T.submit; validate(); return; }
        // No backend reachable: preview mode
        confirmed(s, { id: "preview", meetUrl: null, preview: true }, true);
      });
  });

  function icsDate(d) { return d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""); }

  function confirmed(s, res, preview) {
    state.booking = res;
    track("booking_confirmed", { focus: state.focus || "unsure", preview: !!preview });
    var title = T.eventTitle;
    var details = T.eventDetails + (res.meetUrl ? "\n" + res.meetUrl : "");
    var gcal = "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + encodeURIComponent(title) +
      "&dates=" + icsDate(s.start) + "/" + icsDate(s.end) + "&details=" + encodeURIComponent(details) + "&ctz=" + TZ;
    var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Talent360//Eddekhar//" + LANG.toUpperCase(), "BEGIN:VEVENT",
      "UID:" + (res.id || Date.now()) + "@talent-360.me", "DTSTAMP:" + icsDate(new Date()), "DTSTART:" + icsDate(s.start), "DTEND:" + icsDate(s.end),
      "SUMMARY:" + title, "DESCRIPTION:" + details.replace(/\n/g, "\\n"), res.meetUrl ? "LOCATION:" + res.meetUrl : "", "END:VEVENT", "END:VCALENDAR"]
      .filter(Boolean).join("\r\n");
    var icsUrl = URL.createObjectURL(new Blob([ics], { type: "text/calendar" }));
    var meet = res.meetUrl
      ? '<a href="' + res.meetUrl + '" rel="noopener">' + res.meetUrl.replace(/^https?:\/\//, "") + "</a>"
      : T.meetByEmail;

    var box = document.getElementById("booker");
    box.innerHTML =
      '<div class="confirm" tabindex="-1" id="bk-confirm">' +
      '<div class="ok"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg></div>' +
      "<h3>" + T.confirmedTitle + "</h3>" +
      
      "<dl><dt>" + T.date + "</dt><dd>" + fmtDay(s.start, { weekday: "long", day: "numeric", month: "long", year: "numeric" }) + "</dd>" +
      "<dt>" + T.time + "</dt><dd>" + fmtTime(s.start, false) + " – " + fmtTime(s.end, false) + " " + T.riyadhShort + "</dd>" +
      "<dt>" + T.meet + "</dt><dd>" + meet + "</dd>" +
      "<dt>" + T.discount + "</dt><dd>" + T.discountVal + "</dd></dl>" +
      '<div class="actions"><a class="btn btn-primary btn-sm" href="' + gcal + '" target="_blank" rel="noopener">' + T.addGoogle + "</a>" +
      '<a class="btn btn-secondary btn-sm" href="' + icsUrl + '" download="talent360-hr-check.ics">' + T.addIcs + "</a></div>" +
      '<form id="phone-form" class="phone-row" novalidate><div class="field"><label for="bk-phone">' + T.phoneLabel + "</label>" +
      '<input id="bk-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="+966 5x xxx xxxx"></div>' +
      '<button class="btn btn-secondary btn-sm" type="submit">' + T.phoneSave + '</button></form><p class="form-error" id="phone-msg" role="status"></p>' +
      '<div class="unlocked"><strong>' + T.unlockedTitle + "</strong><ul>" + T.unlockedItems.map(function (i) { return "<li>" + i + "</li>"; }).join("") + "</ul></div>" +
      "</div>";
    document.getElementById("bk-confirm").focus();
    store("local", "t360_unlocked", "1");
    document.getElementById("phone-form").addEventListener("submit", function (e) {
      e.preventDefault();
      var v = document.getElementById("bk-phone").value.trim();
      var msg = document.getElementById("phone-msg");
      if (!/^\+?[0-9\s-]{8,16}$/.test(v)) { msg.style.color = ""; msg.textContent = T.phoneInvalid; return; }
      fetch(API + "/booking/" + encodeURIComponent(res.id) + "/phone", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ phone: v, token: res.token }) })
        .catch(function () {}).then(function () { msg.style.color = "var(--accent-ink)"; msg.textContent = T.phoneSaved; });
    });
  }

  renderDays();
  if (DAYS.length) { state.day = 0; renderDays(); loadSlots(); }
  validate();

  /* ---------- Egypt salary calculator: Gross <-> Net (2026) ----------
     Social insurance: Law 148/2019, employee share 11% of the insured wage,
     insured wage limits from 1/1/2026: min 2,700, max 16,700 EGP.
     Income tax: Law 91/2005 as amended, 2026 brackets, 20,000 EGP exemption. */
  var afterGate = {}; // tool -> action to run once the visitor has given an email
  var sc = document.getElementById("salcalc");
  if (sc) {
    var INS_MIN = 2700, INS_MAX = 16700, INS_RATE = 0.11, ER_RATE = 0.1875, EXEMPTION = 20000;
    var scMode = "g2n", scIns = "auto", scUsed = false, scLast = null;
    var $ = function (id) { return document.getElementById(id); };
    var egp = function (v) { return new Intl.NumberFormat("en-EG", { maximumFractionDigits: 0 }).format(Math.round(v)); };
    function autoInsurance(g) {
      if (g <= 0) return { amount: 0, wage: 0 };
      var w = Math.min(Math.max(g, INS_MIN), INS_MAX);
      return { amount: w * INS_RATE, wage: w };
    }
    function annualTax(t) { return taxSlices(t).reduce(function (a, x) { return a + x.tax; }, 0); }
    function taxSlices(t) {
      if (t <= 0) return [];
      var b;
      if (t <= 600000) b = [[40000, 0], [55000, .10], [70000, .15], [200000, .20], [400000, .225], [Infinity, .25]];
      else if (t <= 700000) b = [[55000, .10], [70000, .15], [200000, .20], [400000, .225], [Infinity, .25]];
      else if (t <= 800000) b = [[70000, .15], [200000, .20], [400000, .225], [Infinity, .25]];
      else if (t <= 900000) b = [[200000, .20], [400000, .225], [Infinity, .25]];
      else if (t <= 1200000) b = [[400000, .225], [Infinity, .25]];
      else b = [[1200000, .25], [Infinity, .275]];
      var out = [], prev = 0;
      for (var i = 0; i < b.length; i++) {
        var slice = Math.min(t, b[i][0]) - prev;
        if (slice > 0) out.push({ from: prev, to: Math.min(t, b[i][0]), rate: b[i][1], tax: slice * b[i][1] });
        prev = b[i][0];
        if (t <= b[i][0]) break;
      }
      return out;
    }
    function fromGross(g, manual) {
      var ins = scIns === "auto" ? autoInsurance(g) : { amount: manual, wage: null };
      var tax = annualTax((g - ins.amount) * 12 - EXEMPTION) / 12;
      var erIns = ins.wage === null ? null : ins.wage * ER_RATE;
      return { gross: g, insurance: ins.amount, wage: ins.wage, tax: tax, net: g - ins.amount - tax,
        taxable: (g - ins.amount) * 12 - EXEMPTION, erIns: erIns, cost: erIns === null ? null : g + erIns };
    }
    function fromNet(net, manual) {
      // Gross-up by bisection: tax is progressive and insurance is capped.
      var lo = net, hi = net * 2.2 + 60000;
      for (var i = 0; i < 70; i++) {
        var mid = (lo + hi) / 2;
        if (fromGross(mid, manual).net < net) lo = mid; else hi = mid;
      }
      return fromGross((lo + hi) / 2, manual);
    }
    function scRun() {
      var amt = parseFloat($("sc-amount").value) || 0, manual = parseFloat($("sc-manual").value) || 0;
      var out = $("sc-out"), err = $("sc-err"), empty = $("sc-empty");
      if (amt <= 0) { out.hidden = true; err.hidden = true; empty.hidden = false; return; }
      empty.hidden = true;
      if (scMode === "g2n" && scIns === "manual" && manual >= amt) { out.hidden = true; err.hidden = false; return; }
      err.hidden = true;
      var r = scMode === "g2n" ? fromGross(amt, manual) : fromNet(amt, manual);
      $("sc-big").textContent = egp(scMode === "g2n" ? r.net : r.gross);
      var pct = function (v) { return r.gross > 0 ? Math.max(0, v / r.gross * 100) + "%" : "0%"; };
      $("sc-b-net").style.width = pct(r.net); $("sc-b-ins").style.width = pct(r.insurance); $("sc-b-tax").style.width = pct(r.tax);
      $("sc-r-gross").textContent = egp(r.gross);
      $("sc-wage-row").hidden = r.wage === null;
      if (r.wage !== null) $("sc-r-wage").textContent = egp(r.wage);
      $("sc-ins-pct").hidden = r.wage === null;
      $("sc-r-ins").textContent = "− " + egp(r.insurance);
      $("sc-r-tax").textContent = "− " + egp(r.tax);
      $("sc-r-net").textContent = egp(r.net);
      $("sc-r-annual").textContent = egp(r.net * 12) + " EGP";
      var sl = taxSlices(r.taxable);
      $("sc-r-eff").textContent = (r.gross > 0 ? (r.tax / r.gross * 100) : 0).toFixed(1) + "%";
      $("sc-r-marg").textContent = sl.length ? (sl[sl.length - 1].rate * 100).toFixed(1).replace(".0", "") + "%" : "0%";
      $("sc-br-body").innerHTML = sl.map(function (x) {
        return "<tr><td dir=\"ltr\">" + egp(x.from) + " – " + egp(x.to) + "</td><td dir=\"ltr\">" + (x.rate * 100).toFixed(1).replace(".0", "") + "%</td><td dir=\"ltr\">" + egp(x.tax) + "</td></tr>";
      }).join("");
      $("sc-br-none").hidden = sl.some(function (x) { return x.tax > 0; });
      $("sc-er").hidden = r.cost === null;
      if (r.cost !== null) {
        $("sc-r-erins").textContent = "+ " + egp(r.erIns);
        $("sc-r-ercost").textContent = egp(r.cost);
        $("sc-r-erannual").textContent = egp(r.cost * 12) + " EGP";
      }
      scLast = r;
      out.hidden = false;
      if (!scUsed) { scUsed = true; track("tool_used", { tool: "salary_calculator_eg" }); }
    }
    function press(sel, attr, val) {
      sc.querySelectorAll(sel).forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute(attr) === val)); });
    }
    sc.querySelectorAll("[data-scmode]").forEach(function (b) {
      b.addEventListener("click", function () {
        scMode = b.getAttribute("data-scmode"); press("[data-scmode]", "data-scmode", scMode);
        var l = $("sc-amount-label"), o = $("sc-out-label");
        l.textContent = l.getAttribute(scMode === "g2n" ? "data-g" : "data-n");
        o.textContent = o.getAttribute(scMode === "g2n" ? "data-n" : "data-g");
        scRun();
      });
    });
    sc.querySelectorAll("[data-scins]").forEach(function (b) {
      b.addEventListener("click", function () {
        scIns = b.getAttribute("data-scins"); press("[data-scins]", "data-scins", scIns);
        $("sc-manual").hidden = scIns !== "manual"; $("sc-note").hidden = scIns !== "auto";
        scRun();
      });
    });
    $("sc-amount").addEventListener("input", scRun);
    $("sc-manual").addEventListener("input", scRun);
    scRun();

    // Copy a plain-text breakdown for an offer letter.
    $("sc-copy").addEventListener("click", function () {
      if (!scLast) return;
      var btn = this, l = JSON.parse(btn.getAttribute("data-l")), r = scLast;
      var lines = [l[0] + ": " + egp(r.gross) + " EGP", l[1] + ": " + egp(r.insurance) + " EGP", l[2] + ": " + egp(r.tax) + " EGP", l[3] + ": " + egp(r.net) + " EGP"];
      if (r.cost !== null) lines.push(l[4] + ": " + egp(r.erIns) + " EGP", l[5] + ": " + egp(r.cost) + " EGP");
      var done = function () { var t = btn.textContent; btn.textContent = btn.getAttribute("data-done"); setTimeout(function () { btn.textContent = t; }, 2500); };
      if (navigator.clipboard) navigator.clipboard.writeText(lines.join("\n")).then(done, function () {}); 
      track("tool_used", { tool: "salary_calculator_eg", action: "copy_offer" });
    });

    // Bulk payroll: parse pasted rows or a CSV on the device, preview a few,
    // and hand over the full sheet once an email is given.
    var bulkRows = [], bulkUsed = false;
    var digits = function (v) { return v.replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); }).replace(/[۰-۹]/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹".indexOf(d); }); };
    function bulkParse(text) {
      var rows = [], skipped = 0;
      digits(text).split(/\r?\n/).forEach(function (line) {
        line = line.trim();
        if (!line) return;
        var m = line.match(/^(.*?)[\s,;\t"]*("?)([0-9][0-9,]*(?:\.[0-9]+)?)\2[\s,;"]*$/);
        if (!m) { skipped++; return; }
        var g = parseFloat(m[3].replace(/,/g, ""));
        if (!(g > 0)) { skipped++; return; }
        var name = m[1].replace(/^["\s]+|[",;\t\s]+$/g, "") || ("#" + (rows.length + 1));
        var saved = scIns; scIns = "auto"; var r = fromGross(g, 0); scIns = saved;
        r.name = name; rows.push(r);
      });
      return { rows: rows, skipped: skipped };
    }
    function bulkRun() {
      var p = bulkParse($("sc-bulk-ta").value);
      bulkRows = p.rows;
      var has = bulkRows.length > 0;
      $("sc-bulk-empty").hidden = has; $("sc-bulk-res").hidden = !has;
      if (!has) return;
      var sum = function (k) { return bulkRows.reduce(function (a, r) { return a + r[k]; }, 0); };
      $("sc-t-n").textContent = bulkRows.length;
      $("sc-t-g").textContent = egp(sum("gross"));
      $("sc-t-net").textContent = egp(sum("net"));
      $("sc-t-c").textContent = egp(sum("cost"));
      var esc = function (t) { var d = document.createElement("i"); d.textContent = t; return d.innerHTML; };
      $("sc-prev-body").innerHTML = bulkRows.slice(0, 3).map(function (r) {
        return "<tr><td>" + esc(r.name) + "</td><td dir=\"ltr\">" + egp(r.gross) + "</td><td dir=\"ltr\">" + egp(r.net) + "</td><td dir=\"ltr\">" + egp(r.cost) + "</td></tr>";
      }).join("");
      var more = $("sc-bulk-more"), skip = $("sc-bulk-skip");
      more.hidden = bulkRows.length <= 3; more.textContent = more.getAttribute("data-t").replace("{n}", bulkRows.length - 3);
      skip.hidden = !p.skipped; skip.textContent = skip.getAttribute("data-t").replace("{n}", p.skipped);
      if (!bulkUsed) { bulkUsed = true; track("tool_used", { tool: "bulk_payroll_eg" }); }
    }
    $("sc-bulk-ta").addEventListener("input", bulkRun);
    $("sc-bulk-file").addEventListener("change", function () {
      var f = this.files && this.files[0];
      if (!f) return;
      var rd = new FileReader();
      rd.onload = function () { $("sc-bulk-ta").value = String(rd.result); bulkRun(); };
      rd.readAsText(f);
    });
    afterGate.bulk_payroll_eg = function () {
      if (!bulkRows.length) return;
      var head = JSON.parse($("sc-bulk-dl").getAttribute("data-head"));
      var q = function (v) { v = String(v); return /[",\n]/.test(v) ? "\"" + v.replace(/"/g, "\"\"") + "\"" : v; };
      var n = function (v) { return Math.round(v); };
      var csv = [head.map(q).join(",")].concat(bulkRows.map(function (r) {
        return [q(r.name), n(r.gross), n(r.wage), n(r.insurance), n(r.tax), n(r.net), n(r.erIns), n(r.cost)].join(",");
      })).join("\r\n");
      var url = URL.createObjectURL(new Blob(["\ufeff" + csv], { type: "text/csv;charset=utf-8" }));
      var a = document.createElement("a"); a.href = url; a.download = "talent360-egypt-payroll-2026.csv";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    };
  }

  /* ---------- Lead-magnet gate (progressive profiling) ---------- */
  var modal = document.getElementById("gate-modal");
  if (modal && modal.showModal) {
    var gateTitle = document.getElementById("gate-title");
    var gateForm = document.getElementById("gate-form");
    var gateMsg = document.getElementById("gate-msg");
    document.querySelectorAll("[data-tool]").forEach(function (b) {
      b.addEventListener("click", function () {
        var tool = b.getAttribute("data-tool");
        track("tool_used", { tool: tool, action: "open_gate" });
        gateTitle.textContent = b.getAttribute("data-title");
        gateForm.tool.value = tool; gateMsg.textContent = "";
        if (store("session", "t360_email")) gateForm.email.value = store("session", "t360_email");
        modal.showModal();
      });
    });
    document.getElementById("gate-close").addEventListener("click", function () { modal.close(); });
    gateForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = gateForm.email.value.trim();
      var est = emailState(email);
      gateMsg.style.color = "";
      if (est !== "ok") { gateMsg.textContent = emailMsg(est); return; }
      store("session", "t360_email", email);
      fetch(API + "/lead-magnet", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, tool: gateForm.tool.value, lang: LANG, utm: utm, website: gateForm.website.value }) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j, offline: r.status === 404 || r.status === 405 }; }); },
              function () { return { offline: true }; })
        .then(function (res) {
          var tool = gateForm.tool.value, after = afterGate[tool];
          if (!res.offline && !res.ok) {
            gateMsg.textContent = res.j && res.j.error === "personal_email" ? T.emailPersonal : T.gateFail; return;
          }
          track("lead_magnet_requested", { tool: tool, preview: !!res.offline });
          if (after) after();
          gateMsg.style.color = "var(--accent-ink)";
          gateMsg.textContent = after ? T.bulkSent : T.gateSent;
        });
    });
  }
})();
