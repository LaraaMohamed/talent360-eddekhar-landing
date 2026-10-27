import re
import hashlib, os
# -*- coding: utf-8 -*-
"""Page template (v2): each section is built on a layout from the Talent 360 Company Profile 2026."""
import json
from html import escape as e
from content import C
_HERE = os.path.dirname(os.path.abspath(__file__))


def _ver(rel):
    """Cache-busting version from the file's contents, so every CSS/JS change reaches browsers."""
    with open(os.path.join(_HERE, "assets", rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]


# Hidden sections: flip to True to show them again (their copy stays in content.py).
SHOW_ECOSYSTEM = False  # "We work every day with the systems your company uses" (GOSI, Qiwa, Mudad...)

from build import BASE, REVIEW, UPDATED, PRIVACY_URL, TEAM_INBOX, SOCIAL, TICK, ARROW, ICONS, CLIENTS, CLIENT_SIZES, pending, jsonld

ICO = {
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>',
    "rocket": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l4-4M14 4c3-1 6-1 6-1s0 3-1 6l-6 6-5-5z"/><path d="M9 10l-4 1-2 3 4 1M14 15l-1 4-3 2-1-4"/><circle cx="15.5" cy="8.5" r="1.5"/></svg>',
    "team": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="7" r="3"/><path d="M6 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="4.5" cy="9.5" r="2"/><circle cx="19.5" cy="9.5" r="2"/><path d="M1.5 18c0-2 1.3-3.5 3-3.5M22.5 18c0-2-1.3-3.5-3-3.5"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M8 14h2M14 14h2M8 17h2"/></svg>',
    "video": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="6" width="13" height="12" rx="3"/><path d="M15.5 10.5l6-3.5v10l-6-3.5"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 15h6M9 18h4"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v6c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
    "coins": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v5c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 15v2c0 1.7 2.7 3 6 3s6-1.3 6-3v-5c0-1.7-2.7-3-6-3"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
    "gov": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10l9-6 9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 21h18"/></svg>',
    "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8M15 7h6v6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.5 3.8 9s-1.3 6.5-3.8 9M12 3C9.5 5.5 8.2 8.5 8.2 12s1.3 6.5 3.8 9"/></svg>',
}
PILL_ICONS = ["team", "gov", "coins", "eye", "lock", "trend"]

# Teal arc from the profile's values slide
ARC = '<svg class="arc" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 110 C 300 10, 900 10, 1200 110" fill="none" stroke="#1FC9B1" stroke-width="5" stroke-linecap="round" opacity=".55"/></svg>'


def _render(lang, mode):
    L = C[lang]
    rtl = L["dir"] == "rtl"
    other = "en" if lang == "ar" else "ar"
    if mode == "preview":
        A = "assets/"
        other_href = "en.html" if lang == "ar" else "index.html"
    else:
        A = "../assets/"
        other_href = "../%s/" % other
    url = BASE + lang + "/"
    edd_logo = A + "img/brand/eddekhar-%s.svg" % lang
    t360 = A + "img/brand/mawared-mark.webp"
    t360w = A + "img/brand/mawared-mark-white.webp"
    by_t360 = ('<span class="mm-by" dir="ltr"><span>by</span><img class="logo-light" src="' + A + 'img/brand/talent360-lockup.png" alt="Talent360" width="124" height="20"></span>')
    privacy = PRIVACY_URL

    def cta(label, key, cls="btn btn-primary", href="#book", focus=None, arrow=True):
        f = ' data-focus="%s"' % focus if focus else ""
        return '<a class="%s" href="%s" data-cta="%s"%s>%s%s</a>' % (cls, href, key, f, e(label), (" " + ARROW) if arrow else "")

    def head(label, h, answer, hid, center=False, extra=""):
        return ('<div class="section-head%s"><span class="label">%s</span><h2 id="%s">%s%s</h2><hr class="rule" aria-hidden="true">%s</div>'
                % (" center" if center else "", e(label), hid, e(h), extra, ('<p class="answer">%s</p>' % e(answer)) if answer else ""))

    lockup = ('<div class="lockup"><a class="mm-logo" href="https://talent-360.me" aria-label="%s" target="_blank" rel="noopener"><img class="logo-light" src="%s" alt="%s" width="86" height="44">' + by_t360 + '</a>'
              '<span class="x" aria-hidden="true">×</span><a class="edd-chip" href="https://eddekhar.com" aria-label="%s" rel="noopener"><img src="%s" alt="%s" width="138" height="44"></a>'
              '</div>') % (e(L["t360_alt"]), t360, e(L["t360_alt"]), e(L["edd_alt"]), edd_logo, e(L["edd_alt"]))

    AR_CLIENT_NAMES = {"alinma": "مصرف الإنماء", "amanah": "أمانة منطقة الرياض"}

    def tiles_html(hidden):
        out = []
        for f, name, approval in CLIENTS:
            ah = ' aria-hidden="true"' if hidden else ""
            if f is None:
                out.append('<li class="logo-tile missing"%s>%s</li>' % (ah, L["amanah_missing"].replace("\n", "<br>")))
                continue
            w, h = CLIENT_SIZES[f]
            out.append('<li class="logo-tile"%s%s><img src="%simg/clients/%s.webp" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">%s</li>'
                       % (ah, "" if hidden else ' tabindex="0"', A, f, "" if hidden else e(AR_CLIENT_NAMES.get(f, name) if rtl else name), w, h,
                          pending(L, "اعتماد الاسم" if rtl else "Name approval") if (approval and not hidden) else ""))
        return "".join(out)

    services = "".join(
        '<a class="tile tile-%d" href="#book" data-cta="service_%s" data-focus="%s"><span class="tile-ico">%s</span><h3>%s</h3><p>%s</p><span class="more">%s %s</span><span class="num" aria-hidden="true">%d</span></a>'
        % (i + 1, k, focus, ICONS[k], e(t), e(d), e(L["svc_link"]), ARROW, i + 1)
        for i, (k, focus, t, d) in enumerate(L["services"]))

    def cream(icon, h, items, ideal, label, focus, key):
        return ('<article class="cream"><span class="circle" aria-hidden="true">%s</span><span class="free">%s</span><h3>%s</h3>'
                '<h4>%s</h4><ul>%s</ul><h4>%s</h4><p class="ideal">%s</p>%s</article>'
                % (ICO[icon], e(L["free"]), e(h), e(L["deliver_h"]), "".join("<li>%s<span>%s</span></li>" % (TICK, e(i)) for i in items),
                   e(L["ideal_h"]), e(ideal), cta(label, key, focus=focus)))

    chips = "".join('<div class="chip"><input type="radio" name="focus" id="f-%s" value="%s"><label for="f-%s">%s</label></div>' % (k, k, k, e(v)) for k, v in L["focus"].items())

    mocks = [
        '<div class="mock" aria-hidden="true"><div class="mock-h"><span>%s</span><span>%s</span></div><div class="mini-days">%s</div><div class="mini-slots"><span>10:00</span><span class="on">10:45</span><span>11:30</span><span>12:15</span><span>13:00</span><span>13:45</span></div></div>'
        % (e(L["mock1_h"]), "الرياض" if L["dir"] == "rtl" else "GMT+3", "".join('<span%s>%s</span>' % (' class="on"' if i == 1 else "", d) for i, d in enumerate(L["mock1_days"]))),
        '<div class="mock" aria-hidden="true"><div class="mock-h"><span>%s</span><span style="color:#1FC9B1">●</span></div><div class="call"><span class="av">%s</span><div><strong>%s</strong><br><span>%s</span></div></div><div class="bar"><i style="inline-size:60%%"></i></div></div>'
        % (e(L["mock2_h"]), "م" if L["dir"] == "rtl" else "T", e(L["mock2_who"]), e(L["mock2_meta"])),
        '<div class="mock" aria-hidden="true"><div class="mock-h"><span>%s</span><span class="tag10">-10%%</span></div><ol>%s</ol><div class="mock-h" style="margin:0"><span>%s</span><span style="color:#608E4D">✓</span></div></div>'
        % (e(L["mock3_h"]), "".join("<li>%s</li>" % e(i) for i in L["mock3_items"]), e(L["mock3_price"])),
    ]
    step_icons = ["calendar", "video", "doc"]
    steps = "".join('<li class="step"><div class="step-dot">%s<b>%d</b></div><h3>%s</h3><p>%s</p>%s</li>'
                    % (ICO[step_icons[i]], i + 1, e(t), e(d), mocks[i]) for i, (t, d) in enumerate(L["steps"]))

    eco_tabs = "".join('<button class="tab" role="tab" id="tab-%s" aria-controls="eco-%s" aria-selected="%s" tabindex="%s">%s</button>'
                       % (k, k, "true" if i == 0 else "false", "0" if i == 0 else "-1", e(l)) for i, (k, l) in enumerate(L["eco_tabs"]))
    eco_panels = ""
    for key, _ in L["eco_tabs"]:
        cells = "".join('<div class="eco"><span class="mark" aria-hidden="true">%s</span><div><strong>%s</strong><span>%s</span></div></div>' % (e(a[:2] if not rtl else a[:1]), e(a), e(b)) for a, b in L["eco_" + key])
        eco_panels += '<div id="eco-%s"><div class="eco-grid">%s</div></div>' % (key, cells)
    eco_section = ('<section id="ecosystem" class="alt" aria-labelledby="eco-h">\n <div class="container">\n  %s\n  <div class="eco-panel">%s</div>\n </div>\n</section>'
                   % (head(L['eco_eyebrow'], L['eco_h'], L['eco_answer'], 'eco-h'), eco_panels)) if SHOW_ECOSYSTEM else ""

    pills = "".join('<li class="pill"><span class="pdot">%s</span><span class="ptext">%s%s</span></li>'
                    % (ICO[PILL_ICONS[i % 6]], e(f), pending(L, "تأكيد الأساس" if rtl else "Confirm basis") if "40" in f else "")
                    for i, f in enumerate(L["elite_facts"]))

    cmp_head = "".join('<th scope="col"%s>%s</th>' % (' class="hl"' if i == 1 else "", e(c)) for i, c in enumerate(L["cmp_cols"][:3]))
    cmp_body = "".join('<tr><th scope="row">%s</th><td class="hl">%s</td><td>%s</td></tr>' % tuple(e(x) for x in r[:3]) for i, r in enumerate(L["cmp_rows"][:3]))
    cmp_locked = "".join('<tr><th scope="row">%s</th><td class="hl">%s</td><td>%s</td></tr>' % tuple(e(x) for x in r[:3]) for r in L["cmp_rows"][3:6])

    tools = ""
    for key, kind, title, desc in L["tools"]:
        if key == "salary_calc":
            btn = '<a class="btn btn-secondary btn-sm" href="#%s" data-cta="tool_%s">%s</a>' % ("badhire-h" if key == "bad_hire" else "salcalc-h", key, e(L["tool_try"]))
        else:
            btn = '<button class="btn btn-secondary btn-sm" type="button" data-tool="%s" data-title="%s">%s</button>' % (key, e(title), e(L["tool_get"]))
        tools += '<article class="tool-card"><span class="kind">%s</span><h3>%s</h3><p>%s</p>%s</article>' % (e(kind), e(title), e(desc), btn)

    def fact_val(v):  # empty values only appear in review builds
        if not v:
            return '<span class="pending" style="display:inline-block">%s</span>' % e(L["pending_val"])
        return ('<bdi dir="ltr">%s</bdi>' % e(v)) if (v.startswith("+") or "@" in v) else e(v)
    facts = "".join('<li><span>%s</span><span>%s</span></li>' % (e(k), fact_val(v)) for k, v in L["facts"] if v or REVIEW)
    faqs = "".join('<details><summary>%s</summary><div><p>%s</p></div></details>' % (e(q), e(a)) for q, a in L["faqs"])
    socials = "".join('<a href="%s" rel="noopener" aria-label="%s"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></a>' % (u, n, p.replace('fill="currentColor"', 'fill="#fff"').replace('stroke="currentColor"', 'stroke="#fff"')) for n, u, p in SOCIAL)
    offer = '<div class="offer-panel"><span class="big">%s</span><span><span class="lbl">%s</span><small>%s</small></span></div>' % (e(L["offer_big"]), e(L["offer_lbl"]), e(L["offer_small"]))
    trust = '<ul class="trust-line">%s</ul>' % "".join("<li>%s%s</li>" % (TICK, e(t)) for t in L["trust"])
    # card boxes on the profile slide, in px of the 1440x810 artwork: industries, consultants, hours, hires, clients
    boxes = {"en": [(952, 167), (330, 386), (1078, 392), (418, 599), (1038, 601)],
             "ar": [(622, 153), (0, 372), (748, 379), (88, 586), (708, 588)]}[lang]
    stat_cards = "".join('<li class="stat-card" style="--x:%.3f%%;--y:%.3f%%"><strong><bdi>%s</bdi></strong><span>%s</span></li>' % (x / 14.4, y / 8.1, e(n), e(l)) for (n, l), (x, y) in zip(L["stats"], boxes))

    alt_links = '<link rel="alternate" hreflang="ar-SA" href="%sar/"><link rel="alternate" hreflang="en-SA" href="%sen/"><link rel="alternate" hreflang="x-default" href="%sar/">' % (BASE, BASE, BASE)
    fonts = "family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700" if rtl else "family=Montserrat:wght@400;500;600;700&family=Unbounded:wght@400;500;600"
    hero_img = A + "img/hero-top-1600.webp"
    metric_aside = "من 0 إلى 25" if rtl else "0 → 25"

    return f"""<!doctype html>
<html lang="{lang}" dir="{L['dir']}" data-review="{'true' if REVIEW else 'false'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(L['title'])}</title>
<meta name="description" content="{e(L['description'])}">
<link rel="canonical" href="{url}">
{alt_links}
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#E8F9F8">
<meta property="og:type" content="website"><meta property="og:locale" content="{L['locale']}">
<meta property="og:title" content="{e(L['title'])}"><meta property="og:description" content="{e(L['description'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/img/cover-1600.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{A}img/brand/talent360-logo.png">
<meta name="color-scheme" content="light">
<link rel="preload" as="image" href="{hero_img}" imagesrcset="{A}img/hero-top-900.webp 900w, {hero_img} 1600w" imagesizes="100vw" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap">
<link rel="stylesheet" href="{A}css/main.css?v={_ver('css/main.css')}">
<script type="application/ld+json">{jsonld(lang, L, url)}</script>
</head>
<body>
<a class="skip" href="#main">{e(L['skip'])}</a>
<div class="announce"><a href="#book" data-cta="announcement"><span class="tag">{e(L['announce_tag'])}</span><span class="a-long">{e(L['announce'])}</span><span class="a-short">{e(L['announce_short'])}</span><span class="a-cta">{e(L['announce_cta'])} {ARROW}</span></a></div>

<header class="site-header">
 <div class="container header-inner">
  {lockup}
  <nav class="main-nav" aria-label="{e(L['nav_label'])}"><ul>{''.join('<li><a href="%s">%s</a></li>' % (h, e(t)) for h, t in L['nav'])}</ul></nav>
  <div class="header-actions">
   <a class="icon-btn" href="{other_href}" hreflang="{C[other]['hreflang']}" lang="{other}" data-lang-link aria-label="{e(L['other_lang_label'])}">{e(L['other_lang'])}</a>
   {cta(L['header_cta'], 'header', 'btn btn-primary btn-sm header-cta', arrow=False)}
   <button class="icon-btn menu-btn" type="button" aria-controls="side-nav" aria-expanded="false" aria-label="{'القائمة' if rtl else 'Menu'}"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10"/></svg></button>
  </div>
 </div>
</header>
<div class="drawer" id="side-nav" hidden>
 <div class="drawer-scrim" data-close></div>
 <aside class="drawer-panel" role="dialog" aria-modal="true" aria-label="{e(L['nav_label'])}">
  <div class="drawer-top">{lockup}<button class="icon-btn drawer-close" type="button" data-close aria-label="{'إغلاق القائمة' if rtl else 'Close menu'}"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
  <nav aria-label="{e(L['nav_label'])}"><ul class="drawer-links">{''.join('<li><a href="%s" data-close>%s<span aria-hidden="true">%s</span></a></li>' % (h, e(t), '‹' if rtl else '›') for h, t in L['nav'])}</ul></nav>
  <div class="drawer-foot">
   {cta(L['header_cta'], 'drawer', 'btn btn-primary btn-block', arrow=False).replace('<a ', '<a data-close ', 1)}
   <a class="drawer-lang" href="{other_href}" hreflang="{C[other]['hreflang']}" lang="{other}" data-lang-link>{'English' if rtl else 'العربية'}</a>
  </div>
 </aside>
</div>

<main id="main">
<!-- Hero: the profile cover -->
<section class="hero" aria-labelledby="h1">
 <div class="hero-stage">
  <picture><source media="(max-width: 700px)" srcset="{A}img/cover-mobile.webp" width="880" height="510"><img class="hero-photo" src="{A}img/hero-top-1600.webp" srcset="{A}img/hero-top-900.webp 900w, {A}img/hero-top-1600.webp 1600w" sizes="100vw" width="1600" height="611" alt="{e(L['hero_img_alt'])}" fetchpriority="high"></picture>
  <div class="hero-scrim" aria-hidden="true"></div>
  <div class="container hero-copy">
   <h1 id="h1">{e(L['h1']).replace(e(L['h1_hl']), '<span class="hl">%s</span>' % e(L['h1_hl']))}</h1>
   <p class="tagline">{e(L['tagline'])}</p>
   <p class="sub">{e(L['hero_sub']).replace('10%', '<mark class="hl-offer">10%</mark>', 1)}</p>
   <div class="hero-ctas">{cta(L['cta_primary'], 'hero_primary', 'btn btn-primary btn-lg', focus='hr')}{cta(L['cta_secondary'], 'hero_secondary', 'btn btn-glass btn-lg', href='#compare', arrow=False)}</div>
  </div>
 </div>
 <ul class="hstats" aria-label="{'أرقام' if rtl else 'Key figures'}">
  <li class="hs-offer"><span class="hs-num"><bdi>{e(L['fc_offer'][0])}</bdi></span><span class="hs-lbl">{e(L['fc_offer'][1])}</span></li>
  <li><span class="hs-num"><bdi>{e(L['fc_b'][0])}</bdi></span><span class="hs-lbl">{e(L['fc_b'][1])}</span></li>
  <li><span class="hs-num"><bdi>{e(L['fc_a'][0])}</bdi></span><span class="hs-lbl">{e(L['fc_a'][1])}</span></li>
  <li><span class="hs-num"><bdi>{e(L['fc_trust'][0])}</bdi></span><span class="hs-lbl">{e(L['fc_trust'][1])}</span></li>
 </ul>
</section>

<!-- Trusted by: the profile's white client panel -->
<section class="trusted alt" aria-labelledby="trusted-h">
 <div class="container">
  <h2 id="trusted-h">{e(L['trusted_h'])}</h2><hr class="rule" aria-hidden="true">
  <div class="logo-panel">
   <div class="marquee"><ul class="marquee-track" role="list">{tiles_html(False)}{tiles_html(True)}</ul></div>
  </div>
 </div>
</section>

<div class="value-line"><div class="container"><p>{e(L['value_line'][0])} <span class="eq">{e(L['value_line'][1])}</span> {e(L['value_line'][2])}</p></div></div>

<!-- Eddekhar offer band -->
<section class="edd-band-wrap" aria-labelledby="edd-band-h">
 <div class="container">
  <div class="edd-band">
   <a class="edd-band-logo" href="https://eddekhar.com" rel="noopener"><img src="{edd_logo}" alt="{e(L['edd_alt'])}" width="138" height="44" loading="lazy"></a>
   <div class="edd-band-copy"><span class="edd-band-tag">{e(L['edd_band_tag'])}</span><h2 id="edd-band-h">{e(L['edd_band_h'])}</h2><p>{e(L['edd_band_p'])}</p></div>
   <div class="edd-band-offer"><span class="edd-band-big">{e(L['offer_big'])}</span>{cta(L['cta_primary'], 'edd_band', 'btn btn-edd', focus='hr')}</div>
  </div>
 </div>
</section>

<!-- Stats: the profile's "Numbers that speak for themselves" slide, using the slide artwork itself -->
<section class="stats-slide" aria-labelledby="stats-h">
 <div class="slide slide-{lang}">
  <img class="slide-art" src="{A}img/stats-{lang}.webp" alt="" width="1600" height="900" loading="lazy">
  <img class="slide-cubes" src="{A}img/cubes.svg" alt="" width="460" height="470" loading="lazy">
  <h2 id="stats-h" class="slide-h">{e(L['stats_h'])}</h2>
  <ul class="slide-stats" aria-label="{e(L['stats_label'])}">{stat_cards}</ul>
 </div>
 <div class="container stats-foot">
  <p class="stats-note">{pending(L, 'الأرقام من ملف الشركة 2026، بانتظار تأكيد لارا' if rtl else 'Figures from the 2026 company profile, awaiting Lara’s confirmation')}</p>
 </div>
</section>

<!-- How we help: the profile's core-services tiles -->
<section id="help" class="alt sweep" aria-labelledby="help-h">
 <div class="container">
  {head(L['help_eyebrow'], L['help_h'], L['help_answer'], 'help-h')}
  <div class="tiles">{services}</div>
 </div>
</section>

<!-- Offer: the profile's cream "We deliver / Ideal for" cards -->
<section id="offer" class="waves" aria-labelledby="offer-h">
 <div class="container">
  {head(L['checks_eyebrow'], L['checks_h'], L['checks_answer'], 'offer-h', center=True)}
  <div class="cream-grid">{cream('rocket', L['check1_h'], L['check1'], L['check1_ideal'], L['check1_cta'], 'hr', 'offer_hr')}{cream('check', L['check2_h'], L['check2'], L['check2_ideal'], L['check2_cta'], 'team', 'offer_team')}</div>
  <p class="unsure">{e(L['unsure'])}</p>
 </div>
</section>

<!-- How it works: the profile's values arc -->
<section id="how" class="alt" aria-labelledby="how-h">
 <div class="container">
  {head(L['how_eyebrow'], L['how_h'], L['how_answer'], 'how-h', center=True)}
  <div class="arc-wrap">{ARC}<ol class="steps">{steps}</ol></div>
  <p class="mock-note">{e(L['mock_note'])}</p>
 </div>
</section>

<!-- Inline booking -->
<section id="book" class="waves" aria-labelledby="book-h">
 <div class="container">
  {head(L['book_eyebrow'], L['book_h'], L['book_answer'], 'book-h')}
  <div class="booking-grid">
   <div class="booker" id="booker">
    <form id="booking-form" novalidate>
     <div class="bk-col bk-when">
     <fieldset class="bk-step"><legend><h3><span class="step-n">1</span>{e(L['step1'])}</h3></legend><div class="chips">{chips}</div></fieldset>
     <fieldset class="bk-step"><legend><h3><span class="step-n">2</span>{e(L['step2'])}</h3></legend>
      <div class="tz-row"><strong id="bk-tz-label">{e(L['tz_riyadh'])}</strong><button type="button" id="bk-tz">{e(L['show_local'])}</button></div>
      <div class="cal">
       <div class="cal-head"><button type="button" class="cal-nav cal-prev" id="bk-prev" aria-label="{e(L['js']['prevWeek'])}"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button><strong class="cal-month" id="bk-month" aria-live="polite"></strong><button type="button" class="cal-nav cal-next" id="bk-next" aria-label="{e(L['js']['nextWeek'])}"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button></div>
       <div class="days" id="bk-days" role="group" aria-label="{e(L['days_label'])}"></div>
      </div>
      <p class="slots-title" id="bk-slots-title"></p>
      <div class="slots" id="bk-slots" role="group" aria-label="{e(L['slots_label'])}" aria-live="polite"></div>
     </fieldset>
     </div>
     <div class="bk-col bk-who">
     <fieldset class="bk-step"><legend><h3><span class="step-n">3</span>{e(L['step3'])}</h3></legend>
      <p class="summary-line" id="bk-summary" hidden aria-live="polite"></p>
      <div class="fields">
       <div class="field"><label for="bk-name">{e(L['f_name'])}</label><input id="bk-name" name="name" autocomplete="name" required></div>
       <div class="field"><label for="bk-email">{e(L['f_email'])}</label><input id="bk-email" name="email" type="email" autocomplete="email" inputmode="email" dir="ltr" required></div>
       <div class="field"><label for="bk-company">{e(L['f_company'])}</label><input id="bk-company" name="company" autocomplete="organization" required></div>
      </div>
      <div class="hp" aria-hidden="true"><label for="bk-website">Website</label><input id="bk-website" name="website" tabindex="-1" autocomplete="off"></div>
      <label class="consent"><input type="checkbox" name="consent" required><span>{re.sub(r'<a href="\{privacy\}">(.*?)</a>', r'<button type="button" class="link-btn" popovertarget="pdpl-pop">\1</button>', L['consent'])}</span></label>
     </fieldset>
     <button class="btn btn-primary btn-block" id="bk-submit" type="submit" disabled>{e(L['submit'])}</button>
     <p class="bk-hint" id="bk-hint">{e(L['js']['pickTime'])}</p>
     <p class="form-error" id="bk-error" role="alert"></p>
     </div>
    </form>
   </div>
   <aside class="booking-aside">
    <div class="aside-edd"><img src="{edd_logo}" alt="{e(L['edd_alt'])}" width="81" height="26" loading="lazy"><span>{e(L['edd_band_tag'])}</span></div>
    {offer}
   </aside>
  </div>
 </div>
</section>

<!-- Ecosystem (government platforms): hidden while SHOW_ECOSYSTEM is False -->
{eco_section}

<!-- Elite: the profile's HCM pillars layout -->
<section id="elite" class="sweep" aria-labelledby="elite-h">
 <div class="container case-grid">
  <div>
   <div class="case-logo"><img src="{A}img/clients/elite.webp" alt="Elite" width="104" height="120"></div>
   <span class="label">{e(L['elite_eyebrow'])}</span>
   <h2 id="elite-h">{e(L['elite_h'])} {pending(L, 'إذن Elite الكتابي' if rtl else 'Elite written permission')}</h2>
   <hr class="rule" aria-hidden="true">
   <p class="answer">{e(L['elite_answer'])}</p>
   <div class="case-metric" role="img" aria-label="{e(L['elite_from'])} → {e(L['elite_to'])} {e(L['elite_unit'])}"><span class="from">{e(L['elite_from'])}</span>{ARROW.replace('width="18" height="18"', 'width="42" height="42"')}<span class="to">{e(L['elite_to'])}</span><span class="unit">{e(L['elite_unit'])}</span></div>
  </div>
  <div>
   <ul class="pills">{pills}</ul>
   <p class="quote-ph pending placeholder">{e(L['elite_quote_ph'])}</p>
   <div class="cta-row" style="justify-content:flex-start">{cta(L['elite_cta'], 'elite', focus='team')}<button class="btn btn-secondary" type="button" data-tool="elite_case_pdf" data-title="{e(L['elite_pdf_t'])}">{e(L['elite_pdf'])}</button></div>
  </div>
 </div>
</section>

<!-- Credibility: the profile's "Why choose Talent 360" slide -->
<section id="trust" aria-labelledby="trust-h">
 <div class="container">
  {head(L['cred_eyebrow'], L['cred_h'], L['cred_answer'], 'trust-h')}
  <div class="why">
   <div class="why-photo"><img src="{A}img/consultants-1200.webp" srcset="{A}img/consultants-640.webp 640w, {A}img/consultants-1200.webp 1200w" sizes="(min-width: 960px) 50vw, 100vw" alt="" width="1200" height="675" loading="lazy">
    <div class="why-cap"><h3>{e(L['why_h'])}</h3><p>{e(L['why_sub'])}</p><hr class="rule" aria-hidden="true"></div></div>
   <div class="why-panel">
    <h3 class="teal-h">{e(L['why_panel_h'])}</h3>
    <p class="expect-h">{e(L['expert_back_h'])}</p><ul class="promise expect-list">{''.join('<li>%s<span>%s</span></li>' % (TICK, e(i)) for i in L['expert_back_items'])}</ul>
   </div>
  </div>
  <div class="partner-approval"><a class="edd-chip" href="https://eddekhar.com" rel="noopener"><img src="{edd_logo}" alt="{e(L['edd_alt'])}" width="138" height="44" loading="lazy"></a><p>{e(L['partner_approval'])}</p></div>
  <div class="cta-row trust-cta">{cta(L['cta_primary'], 'trust', 'btn btn-primary btn-lg', focus='hr')}</div>
 </div>
</section>

<!-- Free tools (Eddekhar's blog slot) -->
<section id="tools" class="waves" aria-labelledby="tools-h">
 <div class="container">
  {head(L['tools_eyebrow'], L['tools_h'], L['tools_answer'], 'tools-h')}
  <div class="tool-grid">{tools}</div>
 </div>
</section>

<!-- Comparison -->
<section id="compare" class="alt" aria-labelledby="compare-h">
 <div class="container">
  {head(L['cmp_eyebrow'], L['cmp_h'], L['cmp_answer'], 'compare-h')}
  <div class="cmp-wrap" role="region" aria-labelledby="compare-h"><table class="cmp"><thead><tr>{cmp_head}</tr></thead><tbody>{cmp_body}</tbody></table>
   <div class="cmp-locked"><table class="cmp cmp-blur" aria-hidden="true"><tbody>{cmp_locked}</tbody></table>
   <div class="cmp-gate"><p class="cmp-gate-h">{e(L['cmp_gate_h'])}</p><p class="cmp-gate-p">{e(L['cmp_gate_p'])}</p><button class="btn btn-primary" type="button" data-tool="compare_pdf" data-title="{e(L['tools'][0][2])}">{e(L['cmp_gate_btn'])}</button></div></div>
  </div>
  <div class="cta-row">{cta(L['cmp_cta2'], 'compare', focus='team')}</div>
 </div>
</section>

<!-- Egypt salary calculator -->
<section id="salcalc-sec" class="waves" aria-labelledby="salcalc-h">
 <div class="container">
  <div class="salcalc" id="salcalc">
   <div class="sc-intro">
    <span class="sc-kicker">{e(L['sc_kicker'])}</span>
    <h3 id="salcalc-h">{e(L['sc_h'])} <span dir="ltr">{e(L['sc_h2'])}</span></h3>
    <p>{e(L['sc_sub'])}</p>
   </div>
   <div class="sc-pick" role="group" aria-label="{e(L['sc_pick_label'])}">
    <button type="button" class="sc-pick-card" data-scpick="one" aria-expanded="false" aria-controls="sc-one"><span class="sc-pick-ico"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg></span><span class="sc-pick-txt"><b>{e(L['sc_pick_one_t'])}</b><small>{e(L['sc_pick_one_d'])}</small></span></button>
    <button type="button" class="sc-pick-card" data-scpick="team" aria-expanded="false" aria-controls="sc-bulk"><span class="sc-pick-ico"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.9 3.1-7 7-7s7 3.1 7 7"/><circle cx="17.5" cy="7.5" r="2.8"/><path d="M17 12.6c2.9.3 5 2.7 5 5.6"/></svg></span><span class="sc-pick-txt"><b>{e(L['sc_pick_team_t'])}</b><small>{e(L['sc_pick_team_d'])}</small></span></button>
   </div>
   <div class="sc-body" id="sc-one" hidden>
    <div class="sc-form">
     <div class="sc-seg" role="group" aria-label="{e(L['sc_h'])}"><button type="button" data-scmode="g2n" aria-pressed="true" dir="ltr">{e(L['sc_g2n'])}</button><button type="button" data-scmode="n2g" aria-pressed="false" dir="ltr">{e(L['sc_n2g'])}</button></div>
     <label class="sc-label" for="sc-amount" id="sc-amount-label" data-g="{e(L['sc_in_gross'])}" data-n="{e(L['sc_in_net'])}">{e(L['sc_in_gross'])}</label>
     <input class="sc-input" id="sc-amount" type="number" inputmode="decimal" min="0" placeholder="0" value="20000" dir="ltr">
     <span class="sc-label">{e(L['sc_ins'])}</span>
     <div class="sc-chips" role="group" aria-label="{e(L['sc_ins'])}"><button type="button" data-scins="auto" aria-pressed="true">{e(L['sc_ins_auto'])}</button><button type="button" data-scins="manual" aria-pressed="false">{e(L['sc_ins_manual'])}</button></div>
     <input class="sc-input sc-manual" id="sc-manual" type="number" inputmode="decimal" min="0" placeholder="0" dir="ltr" hidden aria-label="{e(L['sc_ins'])}">
     <p class="sc-note" id="sc-note">{e(L['sc_ins_note'])}</p>
    </div>
    <div class="sc-result" aria-live="polite">
     <p class="sc-empty" id="sc-empty">{e(L['sc_empty'])}</p>
     <p class="sc-err" id="sc-err" hidden>{e(L['sc_err'])}</p>
     <div id="sc-out" hidden>
      <div class="sc-head">
      <small id="sc-out-label" data-g="{e(L['sc_out_gross'])}" data-n="{e(L['sc_out_net'])}">{e(L['sc_out_net'])}</small>
      <div class="sc-big" dir="ltr"><span id="sc-big">0</span> <span class="cur">{e(L['js']['cur'])}</span></div>
      <div class="sc-bar" dir="ltr" aria-hidden="true"><i class="b-net" id="sc-b-net"></i><i class="b-ins" id="sc-b-ins"></i><i class="b-tax" id="sc-b-tax"></i></div>
      </div>
      <dl class="sc-rows">
       <div><dt>{e(L['sc_gross'])}</dt><dd dir="ltr" id="sc-r-gross"></dd></div>
       <div class="sc-muted" id="sc-wage-row"><dt>{e(L['sc_wage'])}</dt><dd dir="ltr" id="sc-r-wage"></dd></div>
       <div><dt><i class="dot d-ins"></i>{e(L['sc_insurance'])} <span id="sc-ins-pct">(11%)</span></dt><dd dir="ltr" id="sc-r-ins"></dd></div>
       <div><dt><i class="dot d-tax"></i>{e(L['sc_tax'])}</dt><dd dir="ltr" id="sc-r-tax"></dd></div>
       <div class="sc-total"><dt><i class="dot d-net"></i>{e(L['sc_net'])}</dt><dd dir="ltr" id="sc-r-net"></dd></div>
      </dl>
      <div class="sc-annual"><span>{e(L['sc_annual'])}</span><b dir="ltr" id="sc-r-annual"></b></div>
      <div class="sc-rates"><span>{e(L['sc_eff'])} <b dir="ltr" id="sc-r-eff"></b></span><span>{e(L['sc_marg'])} <b dir="ltr" id="sc-r-marg"></b></span></div>
      <div class="sc-er" id="sc-er">
       <p class="sc-er-h">{e(L['sc_er_h'])}</p>
       <dl class="sc-rows">
        <div class="sc-muted"><dt>{e(L['sc_er_ins'])} (18.75%)</dt><dd dir="ltr" id="sc-r-erins"></dd></div>
        <div class="sc-total"><dt>{e(L['sc_er_total'])}</dt><dd dir="ltr" id="sc-r-ercost"></dd></div>
       </dl>
       <div class="sc-annual"><span>{e(L['sc_er_annual'])}</span><b dir="ltr" id="sc-r-erannual"></b></div>
      </div>
      <details class="sc-br">
       <summary>{e(L['sc_br_h'])}</summary>
       <table class="sc-br-t"><thead><tr><th scope="col">{e(L['sc_br_slice'])}</th><th scope="col">{e(L['sc_br_rate'])}</th><th scope="col">{e(L['sc_br_tax'])}</th></tr></thead><tbody id="sc-br-body"></tbody></table>
       <p class="sc-br-none" id="sc-br-none" hidden>{e(L['sc_br_none'])}</p>
      </details>
      <button class="sc-copy" type="button" id="sc-copy" data-done="{e(L['sc_copied'])}" data-l="{e(json.dumps([L['sc_gross'], L['sc_insurance'], L['sc_tax'], L['sc_net'], L['sc_er_ins'], L['sc_er_total']], ensure_ascii=False))}">{e(L['sc_copy'])}</button>
     </div>
    </div>
   </div>
   <div class="sc-bulk" id="sc-bulk" hidden>
    <div class="sc-bulk-head"><span class="sc-kicker">{e(L['sc_bulk_kicker'])}</span><h4 id="scbulk-h">{e(L['sc_bulk_h'])}</h4><p>{e(L['sc_bulk_p'])}</p></div>
    <div class="sc-bulk-body">
     <div class="sc-bulk-in">
      <textarea class="sc-input sc-ta" id="sc-bulk-ta" rows="7" dir="auto" aria-labelledby="scbulk-h" placeholder="{e(L['sc_bulk_ph'].replace(chr(92)+'n', chr(10)))}"></textarea>
      <label class="sc-file"><input type="file" id="sc-bulk-file" accept=".csv,.txt,text/csv,text/plain">{e(L['sc_bulk_file'])}</label>
     </div>
     <div class="sc-result sc-bulk-out" aria-live="polite">
      <p class="sc-empty" id="sc-bulk-empty">{e(L['sc_bulk_empty'])}</p>
      <div id="sc-bulk-res" hidden>
       <div class="sc-tot">
        <div><small>{e(L['sc_bulk_count'])}</small><b dir="ltr" id="sc-t-n"></b></div>
        <div><small>{e(L['sc_bulk_tg'])}</small><b dir="ltr" id="sc-t-g"></b></div>
        <div><small>{e(L['sc_bulk_tn'])}</small><b dir="ltr" id="sc-t-net"></b></div>
        <div><small>{e(L['sc_bulk_tc'])}</small><b dir="ltr" id="sc-t-c"></b></div>
       </div>
       <div class="sc-tw"><table class="sc-br-t sc-prev"><thead><tr><th scope="col">{e(L['sc_bulk_name'])}</th><th scope="col">{e(L['sc_gross'])}</th><th scope="col">{e(L['sc_net'])}</th><th scope="col">{e(L['sc_bulk_tc'])}</th></tr></thead><tbody id="sc-prev-body"></tbody></table></div>
       <p class="sc-bulk-more" id="sc-bulk-more" data-t="{e(L['sc_bulk_more'])}" hidden></p>
       <p class="sc-bulk-more" id="sc-bulk-skip" data-t="{e(L['sc_bulk_skip'])}" hidden></p>
       <button class="btn btn-primary btn-block" type="button" id="sc-bulk-dl" data-tool="bulk_payroll_eg" data-title="{e(L['sc_bulk_gate_t'])}" data-head="{e(json.dumps(L['sc_csv_head'], ensure_ascii=False))}">{e(L['sc_bulk_dl'])}</button>
      </div>
     </div>
    </div>
   </div>
   <p class="sc-basis">{e(L['sc_basis'])}</p>
   <div class="sc-cta">{cta(L['sc_cta'], 'salary_calc', focus='team')}</div>
  </div>
 </div>
</section>


<!-- Testimonials: omitted until real, approved quotes exist -->

<!-- FAQ -->
<section id="faq" class="waves" aria-labelledby="faq-h">
 <div class="container">
  {head(L['faq_eyebrow'], L['faq_h'], L['faq_answer'], 'faq-h', center=True)}
  <div class="faq-list">{faqs}</div>
 </div>
</section>

<!-- Final CTA: the profile's "Let's partner for growth" slide -->
<section class="final alt sweep" aria-labelledby="final-h">
 <div class="container final-grid">
  <div>
   <h2 id="final-h">{e(L['final_title'])}</h2>
   <span class="kicker">{e(L['final_kicker'])}</span><hr class="rule" aria-hidden="true">
   <p class="sub">{e(L['final_h'])}. {e(L['final_sub'])}</p>
   <div class="hero-ctas" style="justify-content:flex-start">{cta(L['cta_primary'], 'final', focus='hr')}</div>
   {offer}
  </div>
  <div class="puzzle"><img class="puzzle-art" src="{A}img/puzzle.webp" alt="" width="389" height="893" loading="lazy"><ul class="bars">{''.join('<li>%s</li>' % e(i) for i in L['final_list'])}</ul></div>
 </div>
</section>
</main>

<!-- Footer: the profile's "Connect with us" slide -->
<footer class="site-footer">
 <div class="container">
  <div class="foot-main">
  <div class="foot-brand">
   <div class="fb-logos"><a class="fb-logo" href="https://talent-360.me" target="_blank" rel="noopener"><img src="{t360}" alt="{e(L['t360_alt'])}" width="381" height="195" loading="lazy"></a><span class="fb-x" aria-hidden="true">×</span><a class="fb-logo fb-edd" href="https://eddekhar.com" rel="noopener"><img src="{edd_logo}" alt="{e(L['edd_alt'])}" width="138" height="44" loading="lazy"></a></div>
   <p class="fb-line">{e(L['foot_line'])}</p>
   <div class="socials">{socials}</div>
  </div>
  <div class="foot-grid">
   <div class="foot-col">
    <h3>{e(L['foot_contact'])}</h3>
    <ul class="contact-list">
     <li><span class="cdot">{ICO['phone']}</span><a href="tel:+966592060727" dir="ltr">+966 592060727</a></li>
     <li><span class="cdot">{ICO['mail']}</span><a href="mailto:info@talent-360.me">info@talent-360.me</a></li>
     <li><span class="cdot">{ICO['globe']}</span><a href="https://talent-360.me" target="_blank" rel="noopener">www.talent-360.me</a></li>
    </ul>
   </div>
   <div class="foot-col">
    <h3>{e(L['foot_offices_h'])}</h3>
    <ul class="contact-list offices">{''.join('<li><span class="cdot">%s</span><span><strong>%s</strong><span class="addr">%s</span><a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=%s" target="_blank" rel="noopener">%s</a></span></li>' % (ICO['pin'], e(t), e(a), q.replace(' ', '+').replace(',', '%2C'), e(L['foot_map'])) for t, a, q in L['offices'])}</ul>
   </div>
  </div>
  </div>
  <div id="pdpl-pop" class="pdpl-pop" popover role="dialog" aria-label="{e(L['privacy'])}"><p class="pp-h">{e(L['privacy'])}</p><p>{e(L['pdpl'])}</p><button type="button" class="pp-close" popovertarget="pdpl-pop" popovertargetaction="hide" aria-label="{'إغلاق' if rtl else 'Close'}">×</button></div>
  <div class="legal">
   <span>{e(L['copyright'])}</span>
   <a href="https://eddekhar.com" rel="noopener">{e(L['partnership'])}</a>
   <button type="button" class="link-btn" popovertarget="pdpl-pop">{e(L['privacy'])}</button>
  </div>
 </div>
</footer>

<div class="sticky-cta" aria-hidden="true"><span class="mini-offer">10%</span>{cta(L['sticky_cta'], 'sticky_mobile', focus='hr', arrow=False)}</div>

<dialog class="gate-modal" id="gate-modal" aria-labelledby="gate-title">
 <form class="gate-inner" id="gate-form" method="dialog" novalidate>
  <button class="icon-btn gate-close" type="button" id="gate-close" aria-label="{e(L['gate_close'])}">✕</button>
  <h3 id="gate-title"></h3>
  <input type="hidden" name="tool">
  <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
  <div class="field"><label for="gate-email">{e(L['gate_email'])}</label><input id="gate-email" name="email" type="email" autocomplete="email" dir="ltr" required></div>
  <button class="btn btn-primary btn-block" type="submit">{e(L['gate_send'])}</button>
  <p class="form-error" id="gate-msg" role="status"></p>
  <p style="font-size:.8125rem;color:var(--text-muted);margin:0">{e(L['gate_note'])}</p>
 </form>
</dialog>

<script type="application/json" id="i18n">{json.dumps(L['js'], ensure_ascii=False)}</script>
<script>window.T360_CONFIG = {{ apiBase: "/api", formEndpoint: "https://formsubmit.co/ajax/{TEAM_INBOX}", debug: false }};</script>
<script src="{A}js/main.js?v={_ver('js/main.js')}" defer></script>
</body>
</html>
"""


def page_links(lang, mode):
    """Home and case-study URLs for each language, relative to the page being built."""
    if mode == "preview":
        return {"home": {"ar": "index.html", "en": "en.html"}, "cases": {"ar": "cases.html", "en": "cases-en.html"}}
    return {"home": {"ar": "../ar/", "en": "../en/"}, "cases": {"ar": "../ar/case-studies/", "en": "../en/case-studies/"}}


def render(lang, mode, page="home"):
    L = C[lang]
    links = page_links(lang, mode)
    html = _render(lang, mode)
    cases_label = L["cases_nav"]
    # the case study lives on its own page; the landing page links to it from the nav
    elite_start = html.index("<!-- Elite:")
    elite_end = html.index("</section>", elite_start) + len("</section>")
    elite = html[elite_start:elite_end]
    if page == "home":
        html = html[:elite_start] + html[elite_end:]
        return html.replace('href="#elite"', 'href="%s"' % (links["cases"][lang] if mode == "preview" else "case-studies/"))
    # case-study page: same header and footer, its own intro, the case, and the closing CTA
    final_start = html.index("<!-- Final CTA:")
    final_end = html.index("</section>", final_start) + len("</section>")
    intro = ('<section class="page-intro" aria-labelledby="cases-h"><div class="container">'
             '<a class="back-link" href="#top-home">%s</a><span class="label">%s</span><h1 id="cases-h">%s</h1><hr class="rule" aria-hidden="true"><p class="answer">%s</p></div></section>'
             % (e(L["cases_back"]), e(L["cases_label"]), e(L["cases_h1"]), e(L["cases_intro"])))
    main_start = html.index('<main id="main">') + len('<main id="main">')
    main_end = html.index("</main>")
    html = html[:main_start] + "\n" + intro + "\n" + elite.replace("<h2 id=\"elite-h\"", "<h2 id=\"elite-h\"") + "\n" + html[final_start:final_end] + "\n" + html[main_end:]
    home = links["home"][lang] if mode == "preview" else "../"
    html = html.replace('href="#elite"', 'href="#elite" aria-current="page"')
    html = html.replace('href="#top-home"', 'href="%s"' % home)
    for frag in ("#help", "#compare", "#tools", "#faq", "#book", "#offer", "#how"):
        html = html.replace('href="%s"' % frag, 'href="%s%s"' % (home, frag))
    # head: own title, canonical and language link; no landing-page structured data
    url = BASE + lang + "/case-studies/"
    html = html.replace("<title>%s</title>" % e(L["title"]), "<title>%s</title>" % e(L["cases_title"]))
    html = html.replace('<link rel="canonical" href="%s%s/">' % (BASE, lang), '<link rel="canonical" href="%s">' % url)
    html = html.replace('content="%s%s/"' % (BASE, lang), 'content="%s"' % url)
    s = html.index('<script type="application/ld+json">')
    html = html[:s] + html[html.index("</script>", s) + len("</script>"):]
    other = "en" if lang == "ar" else "ar"
    other_now = 'href="%s" hreflang' % (("en.html" if lang == "ar" else "index.html") if mode == "preview" else "../%s/" % other)
    other_new = 'href="%s" hreflang' % (links["cases"][other] if mode == "preview" else "../../%s/case-studies/" % other)
    html = html.replace(other_now, other_new, 1)
    if mode != "preview":
        html = html.replace('"../assets/', '"../../assets/')
    return html
