"""Elite case study (lead magnet elite_case_pdf).
Built only from the facts already published on the landing page (content.py elite_*) and the Offshoring service
description in the Talent360 Company Profile 2026. Replace with Elite's approved full case study when it arrives."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from content import C

AR, EN = C["ar"], C["en"]
FACTS = [(a, b) for a, b in zip(AR["elite_facts"], EN["elite_facts"])]

GUIDE = {
    "kicker": ("دراسة حالة", "Case study"),
    "title": (AR["elite_h"], EN["elite_h"]),
    "sub": ("كيف بنت Elite فريقها الهندسي في مصر عبر موارد ومهارات، دون تأسيس كيان قانوني هناك.",
            "How Elite built its engineering team in Egypt through Talent360, without setting up a legal entity there."),
    "pills": [("من 0 إلى 25 مهندسًا", "0 to 25 engineers"), ("دون كيان قانوني", "No legal entity"), ("مصر والسعودية", "Egypt and Saudi Arabia"), ("رسوم ثابتة لكل موظف", "Fixed fee per person")],
    "intro": (AR["elite_answer"], EN["elite_answer"]),
    "cta_h": ("ابنِ فريقك في مصر بالطريقة نفسها", "Build your team in Egypt the same way"),
    "cta_p": ("في فحص مجاني مدته 30 دقيقة، نراجع خطة فريقك ونحسب تكلفته الفعلية في مصر.",
              "In a free 30-minute check we review your team plan and cost it in Egypt."),
    "note": ("ملخص دراسة الحالة كما نُشر على صفحتنا. النسخة الكاملة المعتمدة من Elite تُضاف عند صدورها.",
             "Case-study summary as published on our page. Elite's approved full version will be added when it is released."),
    "sections": [
        {
            "title": ("الهدف", "The goal"),
            "sub": ("فريق هندسي في مصر، دون كيان قانوني", "An engineering team in Egypt, with no legal entity"),
            "blocks": [
                ("p", ("أرادت Elite بناء فريق هندسي في مصر بسرعة، دون أن تؤسس شركة هناك أو تتحمل مسؤوليات صاحب العمل المحلية، مع إبقاء إدارة الموارد البشرية في مصر والسعودية تحت سقف واحد.",
                       "Elite wanted to build an engineering team in Egypt quickly, without setting up a company there or carrying the local employer's obligations, and with HR for Egypt and Saudi Arabia under one roof.")),
                ("kv", [
                    (("نقطة البداية", "Starting point"), ("%s %s" % (AR["elite_from"], AR["elite_unit"]), "%s %s" % (EN["elite_from"], EN["elite_unit"]))),
                    (("النتيجة", "Result"), ("%s %s" % (AR["elite_to"], AR["elite_unit"]), "%s %s" % (EN["elite_to"], EN["elite_unit"]))),
                    (("الكيان القانوني في مصر", "Legal entity in Egypt"), ("لم يكن مطلوبًا", "Not needed")),
                ]),
            ],
        },
        {
            "title": ("ما تولّته موارد ومهارات", "What Talent360 handled"),
            "sub": ("نموذج فريق الـ Offshoring", "The offshoring-team model"),
            "blocks": [
                ("ul", FACTS),
                ("p", ("تولينا التوظيف والتهيئة الوظيفية، وإدارة العقود، والرواتب والامتثال القانوني، وشؤون الموظفين، والضرائب والتأمينات الاجتماعية، والتواصل المستمر مع الموظفين.",
                       "We ran hiring and onboarding, contracts, payroll and legal compliance, personnel administration, tax and social insurance, and ongoing employee engagement.")),
            ],
        },
        {
            "title": ("لماذا نجح النموذج", "Why the model worked"),
            "sub": ("ثلاثة عناصر", "Three elements"),
            "blocks": [
                ("table", [("العنصر", "Element"), ("الأثر", "Effect")], [
                    [("رسوم ثابتة لكل موظف", "Fixed fee per person"), ("تكلفة متوقعة تكبر مع الفريق دون مفاجآت", "A predictable cost that grows with the team, with no surprises")],
                    [("شفافية كاملة في الرواتب", "Full salary transparency"), ("تعرف Elite ما يتقاضاه كل موظف بالضبط", "Elite sees exactly what each person is paid")],
                    [("السرية والملكية الفكرية", "Confidentiality and IP"), ("اتفاقية سرية، والملكية الفكرية تبقى لـ Elite", "An NDA, and the IP stays with Elite")],
                ]),
                ("tip", ("الفريق يعمل لـ Elite يوميًا، بينما نتحمل نحن مسؤوليات صاحب العمل في مصر.", "The team works for Elite every day, while we carry the employer's obligations in Egypt.")),
            ],
        },
        {
            "title": ("هل يناسب هذا النموذج شركتك؟", "Does this model fit your company?"),
            "sub": ("إذا انطبق عليك أكثر من بند", "If more than one applies"),
            "blocks": [
                ("check", [
                    ("تريد فريقًا في مصر دون تأسيس شركة.", "You want a team in Egypt without setting up a company."),
                    ("تحتاج البدء خلال أيام، لا أشهر.", "You need to start within days, not months."),
                    ("تريد تكلفة ثابتة ومعروفة لكل موظف.", "You want a fixed, known cost per person."),
                    ("تدير موظفين في مصر والسعودية معًا.", "You manage people in Egypt and Saudi Arabia together."),
                    ("تهمك حماية الملكية الفكرية.", "Protecting your IP matters to you."),
                ]),
            ],
        },
    ],
}
