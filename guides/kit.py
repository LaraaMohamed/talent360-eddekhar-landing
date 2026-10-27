"""Shared layout for the Talent360 employer guides (lead magnets).

A guide is a dict with a title page, numbered sections made of blocks, and a closing page.
Every text is a pair (ar, en). Block types:
  ("p", text)                       paragraph
  ("ul", [text, ...])               bullet list
  ("h", text)                       sub-heading
  ("table", [head, ...], [[cell, ...], ...])
  ("kv", [(label, value), ...])     two-column fact list
  ("tip", text)                     employer tip (teal box)
  ("warn", text)                    watch-out (amber box)
  ("ex", title, [line, ...], result)  worked example
  ("check", [text, ...])            checklist with tick boxes
  ("cols", [block, block])          two blocks side by side
"""
import base64, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets", "img")
BOOK = {"ar": "https://talent360-eddekhar.onrender.com/ar/#book", "en": "https://talent360-eddekhar.onrender.com/en/#book"}
E = html.escape


def img64(rel):
    path = os.path.join(ASSETS, rel)
    ext = rel.rsplit(".", 1)[1]
    with open(path, "rb") as f:
        return "data:image/%s;base64,%s" % ({"png": "png", "webp": "webp", "svg": "svg+xml"}[ext], base64.b64encode(f.read()).decode())


def t(x, lang):
    """Pick the language from an (ar, en) pair; plain strings pass through."""
    return x[0 if lang == "ar" else 1] if isinstance(x, tuple) else x


CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; }
@page :first { margin: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: %(font)s; color: #26324D; font-size: 10.2pt; line-height: 1.7; }
.cover { height: 297mm; position: relative; overflow: hidden; color: #fff; background: #0E183C; page-break-after: always; }
.cover .art { position: absolute; inset: 0; background: url(%(cover)s) center / cover no-repeat; opacity: .42; }
.cover .shade { position: absolute; inset: 0; background: linear-gradient(160deg, rgba(14,24,60,.96) 0%%, rgba(14,24,60,.82) 55%%, rgba(22,140,124,.75) 120%%); }
.cover .in { position: relative; height: 100%%; padding: 22mm 20mm 18mm; display: flex; flex-direction: column; }
.cover .logos { display: flex; align-items: center; gap: 14px; }
.cover .logos img.mm { height: 54px; }
.cover .logos .x { color: #5FE3CF; font-size: 14pt; }
.cover .logos img.ed { height: 34px; background: #fff; border-radius: 8px; padding: 5px 8px; }
.cover .by { display: flex; align-items: center; gap: 6px; font: 600 9pt Montserrat, sans-serif; color: #CFE3F0; margin-top: 6px; }
.cover .by img { height: 11px; }
.cover .kicker { margin-top: auto; color: #5FE3CF; font-weight: 700; font-size: 12pt; letter-spacing: .02em; }
.cover h1 { font-size: 30pt; line-height: 1.25; margin: 8px 0 14px; color: #fff; max-width: 150mm; }
.cover .sub { font-size: 13pt; color: #D5E2EE; max-width: 140mm; margin: 0 0 22px; }
.cover .pills { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 26px; }
.cover .pills span { border: 1px solid rgba(95,227,207,.55); color: #5FE3CF; border-radius: 99px; padding: 4px 12px; font-size: 9pt; font-weight: 700; }
.cover .foot { display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid rgba(255,255,255,.2); padding-top: 12px; font-size: 9pt; color: #C9D6E6; }
.toc { page-break-after: always; }
.toc h2 { font-size: 18pt; color: #0E183C; margin: 0 0 4px; }
.toc .rule { width: 60px; height: 4px; background: #1FC9B1; border-radius: 4px; margin: 0 0 18px; }
.toc ol { list-style: none; padding: 0; margin: 0; counter-reset: s; }
.toc li { counter-increment: s; display: flex; gap: 14px; align-items: baseline; padding: 9px 0; border-bottom: 1px solid #DCE7EE; font-size: 11.5pt; color: #0E183C; font-weight: 700; }
.toc li::before { content: counter(s, decimal-leading-zero); color: #168C7C; font-weight: 800; min-width: 28px; }
.toc li small { display: block; font-weight: 400; color: #5A6785; font-size: 9pt; }
.toc .intro { background: #F1FAF8; border-radius: 14px; padding: 14px 18px; margin: 0 0 20px; color: #26324D; }
section.s { margin: 0 0 6mm; }
.keep { break-inside: avoid; }
section.s + section.s { page-break-before: auto; }
.sh { display: flex; align-items: center; gap: 12px; margin: 0 0 10px; padding: 10px 14px; background: linear-gradient(120deg, #0E183C, #13285A); color: #fff; border-radius: 12px; break-after: avoid; }
.sh .n { background: #1FC9B1; color: #0E183C; font-weight: 800; border-radius: 8px; min-width: 30px; height: 30px; display: grid; place-items: center; font-size: 11pt; }
.sh h2 { margin: 0; font-size: 13.5pt; color: #fff; }
.sh small { display: block; color: #9FE9DD; font-size: 8.6pt; font-weight: 400; }
h3 { font-size: 11.2pt; color: #0E183C; margin: 12px 0 5px; padding-inline-start: 10px; border-inline-start: 3px solid #1FC9B1; break-after: avoid; }
p { margin: 0 0 7px; }
ul { margin: 0 0 8px; padding-inline-start: 18px; }
li { margin: 2px 0; }
li::marker { color: #168C7C; }
table { width: 100%%; border-collapse: separate; border-spacing: 0; margin: 4px 0 10px; font-size: 9.2pt; border: 1px solid #DCE7EE; border-radius: 10px; overflow: hidden; break-inside: avoid; }
th { background: #E3F6F3; color: #0E183C; text-align: start; padding: 7px 9px; font-weight: 800; border-bottom: 1px solid #C8E9E3; }
td { padding: 6px 9px; border-bottom: 1px solid #EDF2F6; vertical-align: top; }
tr:last-child td { border-bottom: 0; }
td:first-child { font-weight: 700; color: #0E183C; }
.kv { display: grid; grid-template-columns: 34%% 1fr; border: 1px solid #DCE7EE; border-radius: 10px; overflow: hidden; margin: 4px 0 10px; break-inside: avoid; font-size: 9.4pt; }
.kv div { padding: 6px 10px; border-bottom: 1px solid #EDF2F6; }
.kv div:nth-child(odd) { background: #F6FAFC; font-weight: 700; color: #0E183C; }
.box { border-radius: 12px; padding: 10px 14px; margin: 6px 0 10px; break-inside: avoid; font-size: 9.6pt; }
.box b.l { display: block; font-size: 8.6pt; letter-spacing: .03em; margin-bottom: 2px; }
.tip { background: #E3F6F3; border-inline-start: 4px solid #1FC9B1; }
.tip b.l { color: #168C7C; }
.warn { background: #FFF7E6; border-inline-start: 4px solid #E0A526; }
.warn b.l { color: #8A5A00; }
.ex { border: 1px dashed #9FD8CF; background: #FBFEFD; }
.ex b.l { color: #0E183C; font-size: 10pt; }
.ex ol { margin: 4px 0 6px; padding-inline-start: 18px; }
.ex .res { background: #0E183C; color: #fff; border-radius: 8px; padding: 6px 10px; font-weight: 700; display: inline-block; }
.logos-grid { background: #fff; border: 1px solid #DCE7EE; border-radius: 12px; padding: 12px 14px; margin: 8px 0 10px; break-inside: avoid; }
.logos-grid b { display: block; text-align: center; color: #0E183C; font-size: 10pt; margin-bottom: 10px; }
.logos-grid div { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px 14px; align-items: center; justify-items: center; }
.dl { list-style: none; padding: 0; margin: 6px 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; }
.dl li { background: #fff; border: 1px solid #DCE7EE; border-radius: 10px; padding: 9px 12px; font-size: 9pt; line-height: 1.5; break-inside: avoid; }
.dl li b { display: block; color: #0E183C; font-size: 9.5pt; margin-bottom: 3px; }
.logos-grid img { max-width: 100%%; max-height: 30px; object-fit: contain; }
.check { background: #F1FAF8; border-radius: 12px; padding: 10px 14px; margin: 6px 0 10px; break-inside: avoid; }
.check ul { list-style: none; padding: 0; margin: 0; }
.check li { position: relative; padding-inline-start: 24px; margin: 5px 0; }
.check li::before { content: ""; position: absolute; inset-inline-start: 0; top: 3px; width: 13px; height: 13px; border: 2px solid #168C7C; border-radius: 3px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.cols > div { min-width: 0; }
.bdi { unicode-bidi: isolate; direction: ltr; display: inline-block; }
.close { page-break-before: always; min-height: 250mm; display: flex; flex-direction: column; }
.close .cta { background: linear-gradient(150deg, #0E183C 0%%, #13285A 65%%, #168C7C 130%%); color: #fff; border-radius: 22px; padding: 26px 26px 24px; margin-top: 8px; }
.close .cta h2 { color: #fff; font-size: 18pt; margin: 0 0 8px; }
.close .cta p { color: #D5E2EE; font-size: 11pt; }
.close .cta .offer { display: inline-flex; gap: 12px; align-items: center; background: linear-gradient(140deg, #6E9E59, #4E7A3D); border-radius: 14px; padding: 10px 16px; margin: 6px 0 16px; }
.close .cta .offer b { font: 800 22pt Montserrat, sans-serif; }
.close .cta a.btn { display: inline-block; background: #1FC9B1; color: #0E183C; font-weight: 800; text-decoration: none; padding: 11px 22px; border-radius: 99px; font-size: 11pt; }
.close .svc { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 16px 0; }
.close .svc div { background: #F1FAF8; border-radius: 12px; padding: 10px 14px; }
.close .svc b { color: #0E183C; display: block; }
.close .contact { margin-top: auto; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 9.2pt; border-top: 1px solid #DCE7EE; padding-top: 12px; }
.close .contact b { color: #0E183C; display: block; }
.close .note { font-size: 8.4pt; color: #6B7894; margin-top: 10px; }
"""


def block(b, lang):
    k = b[0]
    if k == "p":
        return "<p>%s</p>" % E(t(b[1], lang))
    if k == "h":
        return "<h3>%s</h3>" % E(t(b[1], lang))
    if k == "ul":
        return "<ul>%s</ul>" % "".join("<li>%s</li>" % E(t(x, lang)) for x in b[1])
    if k == "table":
        head = "".join("<th>%s</th>" % E(t(h, lang)) for h in b[1])
        rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % E(t(c, lang)) for c in r) for r in b[2])
        return "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, rows)
    if k == "kv":
        return '<div class="kv">%s</div>' % "".join("<div>%s</div><div>%s</div>" % (E(t(a, lang)), E(t(v, lang))) for a, v in b[1])
    if k in ("tip", "warn"):
        label = {"tip": ("نصيحة لصاحب العمل", "Employer tip"), "warn": ("انتبه", "Watch out")}[k]
        return '<div class="box %s"><b class="l">%s</b>%s</div>' % (k, E(t(label, lang)), E(t(b[1], lang)))
    if k == "ex":
        lines = "".join("<li>%s</li>" % E(t(x, lang)) for x in b[2])
        return '<div class="box ex"><b class="l">%s · %s</b><ol>%s</ol><span class="res">%s</span></div>' % (
            E(t(("مثال محسوب", "Worked example"), lang)), E(t(b[1], lang)), lines, E(t(b[3], lang)))
    if k == "check":
        return '<div class="check"><ul>%s</ul></div>' % "".join("<li>%s</li>" % E(t(x, lang)) for x in b[1])
    if k == "dl":
        return '<ul class="dl">%s</ul>' % "".join("<li><b>%s</b>%s</li>" % (E(t(h, lang)), E(t(d, lang))) for h, d in b[1])
    if k == "logos":
        return '<div class="logos-grid"><b>%s</b><div>%s</div></div>' % (E(t(b[1], lang)), "".join('<img src="%s" alt="">' % img64(f) for f in b[2]))
    if k == "cols":
        return '<div class="cols">%s</div>' % "".join("<div>%s</div>" % block(x, lang) for x in b[1])
    raise ValueError(k)


def render(g, lang):
    rtl = lang == "ar"
    font = "'Almarai', 'Noto Sans Arabic', sans-serif" if rtl else "Montserrat, 'Noto Sans', sans-serif"
    fonts = "family=Almarai:wght@400;700;800" if rtl else "family=Montserrat:wght@400;600;700;800"
    css = CSS % {"font": font, "cover": img64("cover-1600.webp")}
    secs = g["sections"]
    toc = "".join("<li><span>%s<small>%s</small></span></li>" % (E(t(s["title"], lang)), E(t(s.get("sub", ("", "")), lang))) for s in secs)
    body = "".join(
        # the heading travels with the section's first block so it never sits alone at the foot of a page
        '<section class="s"><div class="keep"><div class="sh"><span class="n">%02d</span><h2>%s<small>%s</small></h2></div>%s</div>%s</section>'
        % (i + 1, E(t(s["title"], lang)), E(t(s.get("sub", ("", "")), lang)),
           block(s["blocks"][0], lang), "".join(block(b, lang) for b in s["blocks"][1:]))
        for i, s in enumerate(secs))
    pills = "".join("<span>%s</span>" % E(t(p, lang)) for p in g["pills"])
    svc = "".join("<div><b>%s</b>%s</div>" % (E(t(a, lang)), E(t(d, lang))) for a, d in SERVICES)
    return """<!doctype html><html lang="%(lang)s" dir="%(dir)s"><head><meta charset="utf-8"><title>%(title)s</title>
<link href="https://fonts.googleapis.com/css2?%(fonts)s&display=swap" rel="stylesheet"><style>%(css)s</style></head><body>
<div class="cover"><div class="art"></div><div class="shade"></div><div class="in">
 <div class="logos"><img class="mm" src="%(mm)s" alt=""><span class="x">×</span><img class="ed" src="%(ed)s" alt=""></div>
 <div class="by" dir="ltr">by <img src="%(t360)s" alt="Talent360"></div>
 <div class="kicker">%(kicker)s</div><h1>%(title)s</h1><p class="sub">%(sub)s</p><div class="pills">%(pills)s</div>
 <div class="foot"><span>%(upd)s</span><span dir="ltr">talent-360.me · business-growth@talent-360.me</span></div>
</div></div>
<div class="toc"><h2>%(toc_h)s</h2><div class="rule"></div><div class="intro">%(intro)s</div><ol>%(toc)s</ol></div>
%(body)s
<div class="close">
 <div class="cta"><h2>%(cta_h)s</h2><p>%(cta_p)s</p><div class="offer"><b>10%%</b><span>%(offer)s</span></div><br><a class="btn" href="%(book)s">%(cta_btn)s</a></div>
 <div class="svc">%(svc)s</div>
 <div class="contact"><div><b>%(ksa_h)s</b>%(ksa)s</div><div><b>%(eg_h)s</b>%(eg)s</div><div><b>%(ct_h)s</b><span dir="ltr">+966 592060727<br>business-growth@talent-360.me<br>talent-360.me</span></div></div>
 <p class="note">%(note)s</p>
</div></body></html>""" % {
        "lang": lang, "dir": "rtl" if rtl else "ltr", "fonts": fonts, "css": css,
        "mm": img64("brand/mawared-mark-white.png"), "ed": img64("brand/eddekhar-%s.svg" % lang), "t360": img64("brand/talent360-wordmark-white.png"),
        "kicker": E(t(g["kicker"], lang)), "title": E(t(g["title"], lang)), "sub": E(t(g["sub"], lang)), "pills": pills,
        "upd": E(t(("محدّث 2026 · موارد ومهارات × إدخار", "Updated 2026 · Talent360 × Eddekhar"), lang)),
        "toc_h": E(t(("المحتويات", "Contents"), lang)), "intro": E(t(g["intro"], lang)), "toc": toc, "body": body,
        "cta_h": E(t(g["cta_h"], lang)), "cta_p": E(t(g["cta_p"], lang)),
        "offer": E(t(("خصم على كل خدمات موارد ومهارات لعملاء إدخار", "off every Talent360 service for Eddekhar clients"), lang)),
        "book": BOOK[lang], "cta_btn": E(t(("احجز فحصك المجاني", "Book your free HR check"), lang)), "svc": svc,
        "ksa_h": E(t(("مكتب السعودية", "Saudi office"), lang)), "ksa": E(t(("7750 طريق الملك عبدالعزيز، الرياض", "7750 King Abdelaziz Rd, Riyadh"), lang)),
        "eg_h": E(t(("مكتب مصر", "Egypt office"), lang)), "eg": E(t(("مدينة نصر، القاهرة", "Nasr City, Cairo"), lang)),
        "ct_h": E(t(("تواصل معنا", "Contact us"), lang)),
        "note": E(t(g["note"], lang)),
    }


SERVICES = [
    (("إدارة رأس المال البشري (HCM)", "Human capital management (HCM)"), ("نكون إدارة الموارد البشرية لشركتك: الرواتب والعقود والامتثال.", "We act as your HR department: payroll, contracts and compliance.")),
    (("فريقك في مصر", "Your team in Egypt"), ("فريق كامل في مصر دون تأسيس شركة، والعقود والتأمينات علينا.", "A full team in Egypt without a local company; contracts and insurance on us.")),
    (("التوظيف", "Recruitment"), ("من تحديد الدور حتى أول يوم عمل.", "From defining the role to day one.")),
    (("اللوائح والسياسات", "Policies and bylaws"), ("لائحة تنظيم العمل والجزاءات، ونماذج العقود المحدّثة.", "Work and disciplinary bylaws, and updated contract templates.")),
]
