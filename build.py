# -*- coding: utf-8 -*-
"""Builds /ar/ and /en/ from content.py.

  python3 build.py            -> production files in ./dist (ar/, en/, assets/, robots, sitemap, llms.txt)
  python3 build.py preview    -> flat preview in ./preview (index.html = AR, en.html = EN)

Set REVIEW = False before launch to hide the yellow "pending approval" markers.
"""
import html, json, os, shutil, sys
from content import C

BASE = "https://talent-360.me/eddekhar/"   # PENDING: final hosting URL
REVIEW = False
UPDATED = "2026-10-26"
# Inbox that receives booking and download requests (FormSubmit relay). Change here, then rebuild.
TEAM_INBOX = "business-growth@talent-360.me"
PRIVACY_URL = "https://talent-360.me/privacy"  # PENDING: real privacy policy URL
SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/company/talent-360-me/", '<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9z" fill="currentColor"/>'),
    ("Instagram", "https://www.instagram.com/talent360me/", '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/>'),
    ("Facebook", "https://www.facebook.com/talent360me", '<path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.6-.6z" fill="currentColor"/>'),
]

e = html.escape

TICK = '<svg class="tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
ARROW = '<svg class="ico-dir" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICONS = {
    # simple line illustrations, Talent360 teal
    "hcm": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="16" cy="9" r="4"/><path d="M8 25c0-4.4 3.6-8 8-8s8 3.6 8 8"/><circle cx="6" cy="13" r="2.5"/><circle cx="26" cy="13" r="2.5"/><path d="M2 23c0-2.5 1.8-4.5 4-4.5M30 23c0-2.5-1.8-4.5-4-4.5"/></svg>',
    "recruit": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="13" cy="13" r="7"/><path d="M18 18l8 8"/><circle cx="13" cy="11" r="2.5"/><path d="M9 17c.8-1.8 2.2-2.6 4-2.6s3.2.8 4 2.6"/></svg>',
    "offshore": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="16" cy="16" r="12"/><path d="M4 16h24M16 4c3.5 3.5 5 7.5 5 12s-1.5 8.5-5 12M16 4c-3.5 3.5-5 7.5-5 12s1.5 8.5 5 12"/></svg>',
    "od": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="12" y="3" width="8" height="6" rx="1.5"/><rect x="3" y="23" width="8" height="6" rx="1.5"/><rect x="12" y="23" width="8" height="6" rx="1.5"/><rect x="21" y="23" width="8" height="6" rx="1.5"/><path d="M16 9v7M7 23v-4h18v4M16 16v7"/></svg>',
}
CLIENTS = [  # (file, name, needs naming approval)
    ("alinma", "Alinma Bank", False), ("holouly", "Holouly", False), ("techstrike", "TechStrike", False),
    ("sifi", "SIFI", False), ("mohasby", "Mohasby", False), ("amanah", "Amanah Al Riyadh", False),
    ("magnetic", "Magnetic", True), ("omq", "OMQ", True), ("elite", "Elite", False),
    ("kayangulf", "Kayan Gulf", False),
    ("impetus", "Impetus Strategy", False), ("probuilder", "Probuilder", False),
    ("ase", "ASE", False), ("walaplus", "WalaPlus", False), ("mrsool", "Mrsool", False),
    ("meexpo", "MEEXPO", False), ("wsad", "WSAD", False),
    ("madkhol", "Madkhol", False),
]
CLIENT_SIZES = {"alinma": (309, 120), "techstrike": (360, 62), "sifi": (387, 120), "magnetic": (252, 120), "mohasby": (308, 120), "holouly": (360, 80), "omq": (144, 120), "elite": (104, 120), "amanah": (126, 120), "kayangulf": (225, 120), "impetus": (183, 80), "probuilder": (111, 120), "ase": (375, 120), "walaplus": (310, 120), "mrsool": (597, 120), "madkhol": (585, 120), "meexpo": (299, 120), "wsad": (156, 120)}


def pending(L, label=None):
    if not REVIEW:
        return ""
    return '<span class="pending">%s</span>' % e(label or ("بانتظار الموافقة" if L["dir"] == "rtl" else "Pending approval"))


def jsonld(lang, L, url):
    org = {
        "@type": "Organization", "@id": "https://talent-360.me/#org",
        "name": "Talent 360" if lang == "en" else "موارد ومهارات", "alternateName": "Talent360",
        "url": "https://talent-360.me", "logo": BASE + "assets/img/brand/talent360-logo.png",
        "email": "info@talent-360.me", "telephone": "+966592060727",
        "address": {"@type": "PostalAddress", "addressLocality": "Riyadh" if lang == "en" else "الرياض", "addressCountry": "SA"},
        "sameAs": [s[1] for s in SOCIAL],
        "description": L["foot_line"],
    }
    service = {
        "@type": "Service", "@id": url + "#hr-health-check", "name": "فحص الموارد البشرية" if lang == "ar" else "Free HR check",
        "serviceType": "HR consulting" if lang == "en" else "استشارات الموارد البشرية",
        "provider": {"@id": "https://talent-360.me/#org"}, "areaServed": {"@type": "Country", "name": "Saudi Arabia" if lang == "en" else "المملكة العربية السعودية"},
        "description": L["checks_answer"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SAR", "description": L["description"]},
    }
    faq = {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in L["faqs"]]}
    howto = {"@type": "HowTo", "@id": url + "#how", "name": L["how_h"], "description": L["how_answer"], "totalTime": "PT30M",
             "step": [{"@type": "HowToStep", "position": i + 1, "name": s[0], "text": s[1]} for i, s in enumerate(L["steps"])]}
    page = {"@type": "WebPage", "@id": url, "url": url, "name": L["title"], "description": L["description"], "inLanguage": L["hreflang"],
            "dateModified": UPDATED, "about": {"@id": "https://talent-360.me/#org"}}
    return json.dumps({"@context": "https://schema.org", "@graph": [page, org, service, faq, howto]}, ensure_ascii=False, indent=1)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


ROBOTS = """# Talent360 × Eddekhar landing page
User-agent: *
Allow: /

# AI search and answer engines are welcome
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Disallow: /api/

Sitemap: {base}sitemap.xml
"""

LLMS = """# Talent360 × Eddekhar partner offer

> Talent360 (talent-360.me) is a people-management firm working across Saudi Arabia, Egypt and the GCC. Clients of Eddekhar (eddekhar.com) get a free 30-minute HR Health Check or Team & Workforce Check with a Talent360 consultant, three written priorities, and 10% off every Talent360 service, applied automatically.

Last updated: {updated}

## Pages
- [العربية (default)]({base}ar/): فحص مجاني للموارد البشرية وخصم 10% لعملاء إدخار
- [English]({base}en/): Free HR Health Check and 10% off for Eddekhar clients

## Key facts
- Offer: free 30-minute session (HR Health Check, or Team & Workforce Check), booked in-page, Sunday to Thursday, 10:00 to 16:00 Riyadh time (GMT+3). No commitment, no payment details.
- Discount: 10% off all Talent360 services for Eddekhar clients, applied automatically.
- Services: human capital management (HCM / outsourced HR), recruitment, offshore teams in Egypt without a legal entity, organisation development, strategy and performance consulting.
- Saudi platforms handled for clients: GOSI, Qiwa, Mudad, Nitaqat, Muqeem, Ajeer.
- Case study: Elite grew from 0 to a 25-person engineering team in Egypt via Talent360.
- Contact: info@talent-360.me, +966 592060727, Riyadh, Saudi Arabia.
- Data: handled under Saudi Arabia's Personal Data Protection Law (PDPL); never sold or shared.
"""

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{urls}
</urlset>
"""

ROOT_REDIRECT = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>موارد ومهارات × إدخار</title>
<link rel="canonical" href="{base}ar/">
<link rel="alternate" hreflang="ar-SA" href="{base}ar/"><link rel="alternate" hreflang="en-SA" href="{base}en/"><link rel="alternate" hreflang="x-default" href="{base}ar/">
<meta name="robots" content="noindex, follow">
<script>location.replace("ar/"+location.search);</script>
<meta http-equiv="refresh" content="0; url=ar/">
</head><body style="background:#FFFFFF"><p><a href="ar/">العربية</a> · <a href="en/">English</a></p></body></html>
"""


def main():
    from template import render
    here = os.path.dirname(os.path.abspath(__file__))
    mode = sys.argv[1] if len(sys.argv) > 1 else "dist"
    out = os.path.join(here, mode if mode == "preview" else "dist")
    if os.path.exists(out):
        shutil.rmtree(out)
    # Gated PDFs are served only by the booking server after email verification (backend/files), never as public files
    shutil.copytree(os.path.join(here, "assets"), os.path.join(out, "assets"), ignore=shutil.ignore_patterns("files"))
    if mode == "preview":
        write(os.path.join(out, "index.html"), render("ar", "preview"))
        write(os.path.join(out, "en.html"), render("en", "preview"))
        write(os.path.join(out, "cases.html"), render("ar", "preview", "cases"))
        write(os.path.join(out, "cases-en.html"), render("en", "preview", "cases"))
    else:
        for lang in ("ar", "en"):
            write(os.path.join(out, lang, "index.html"), render(lang, "dist"))
            write(os.path.join(out, lang, "case-studies", "index.html"), render(lang, "dist", "cases"))
        write(os.path.join(out, "index.html"), ROOT_REDIRECT.format(base=BASE))
        write(os.path.join(out, "robots.txt"), ROBOTS.format(base=BASE))
        write(os.path.join(out, "llms.txt"), LLMS.format(base=BASE, updated=UPDATED))
        alts = '<xhtml:link rel="alternate" hreflang="ar-SA" href="{b}ar/"/><xhtml:link rel="alternate" hreflang="en-SA" href="{b}en/"/><xhtml:link rel="alternate" hreflang="x-default" href="{b}ar/"/>'.format(b=BASE)
        urls = "\n".join(' <url><loc>%s%s/</loc><lastmod>%s</lastmod>%s</url>' % (BASE, l, UPDATED, alts) for l in ("ar", "en", "ar/case-studies", "en/case-studies"))
        write(os.path.join(out, "sitemap.xml"), SITEMAP.format(urls=urls))
    print("built", out)


if __name__ == "__main__":
    main()
