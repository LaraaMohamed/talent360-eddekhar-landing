"""Offshoring team vs your own Egypt entity vs an EOR: the 12-pillar comparison (lead magnet compare_pdf).
The pillar table is the landing page's comparison (content.py cmp_rows). Employment-cost figures are the
2026 rules used in eg_benefits.py: Social Insurance Law 148/2019 and NOSI 2026 limits, Income Tax Law 91/2005
as amended, the NWC minimum wage, Labour Law 14/2025. No entity set-up prices are quoted: they vary by case."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from content import C

AR, EN = C["ar"], C["en"]
COLS = [(a, b) for a, b in zip(AR["cmp_cols"], EN["cmp_cols"])]
ROWS = [[(a, b) for a, b in zip(ra, re)] for ra, re in zip(AR["cmp_rows"], EN["cmp_rows"])]

GUIDE = {
    "kicker": ("دليل المقارنة", "Comparison guide"),
    "title": ("فريق Offshoring في مصر أم كيان قانوني خاص بك؟", "An offshoring team in Egypt, or your own entity?"),
    "sub": ("12 محورًا تقارن بين ثلاثة طرق لبناء فريق في مصر، مع تكاليف التوظيف الإلزامية في 2026 ومثال محسوب.",
            "12 pillars comparing three ways to build a team in Egypt, with the 2026 statutory employment costs and a worked example."),
    "pills": [("12 محورًا", "12 pillars"), ("تكلفة التوظيف 2026", "2026 employment cost"), ("مثال محسوب", "Worked example"), ("قائمة قرار", "Decision checklist")],
    "intro": ("هناك ثلاث طرق شائعة لتوظيف فريق في مصر: أن تبني الفريق عبر موارد ومهارات دون تأسيس شركة، أو أن تؤسس كيانًا قانونيًا خاصًا بك، أو أن تتعاقد مع مزود صاحب عمل مسجل (EOR). "
              "يقارن هذا الدليل بينها في 12 محورًا، ثم يعرض التكاليف التي يفرضها القانون على أي صاحب عمل في مصر أيًا كان الخيار.",
              "There are three common ways to employ a team in Egypt: build it through Talent360 without incorporating, set up your own legal entity, or contract an employer-of-record (EOR) provider. "
              "This guide compares them across 12 pillars, then sets out the costs Egyptian law places on any employer, whichever route you take."),
    "cta_h": ("اعرف أي خيار يناسب شركتك", "Find out which route fits your company"),
    "cta_p": ("في فحص مجاني مدته 30 دقيقة، نراجع خطة التوظيف في مصر ونحسب تكلفة الفريق الفعلية لكل خيار.",
              "In a free 30-minute check we review your hiring plan for Egypt and cost the team under each option."),
    "note": ("مقارنة نوعية مع أرقام 2026 المعمول بها. تكاليف التأسيس ورسوم المزودين تختلف حسب الحالة، فلا نذكر لها أرقامًا عامة.",
             "A qualitative comparison with the 2026 figures in force. Set-up costs and provider fees vary case by case, so no general figures are quoted for them."),
    "sections": [
        {
            "title": ("المقارنة في 12 محورًا", "The comparison in 12 pillars"),
            "sub": ("موارد ومهارات، والكيان الخاص، وصاحب العمل المسجل", "Talent360, your own entity, and an EOR"),
            "blocks": [
                ("table", COLS, ROWS),
                ("tip", ("الفرق الأكبر في البداية والخروج: مع موارد ومهارات تبدأ خلال أيام دون تأسيس، وتنهي الخدمة وفق العقد دون تصفية كيان.",
                         "The biggest differences are at the start and the exit: with Talent360 you start within days without incorporating, and end the service under the contract with no entity to liquidate.")),
            ],
        },
        {
            "title": ("ما يفرضه القانون على أي صاحب عمل في مصر", "What the law requires of any employer in Egypt"),
            "sub": ("هذه التكاليف ثابتة في كل الخيارات الثلاثة", "These costs apply under all three options"),
            "blocks": [
                ("kv", [
                    (("الحد الأدنى للأجر، القطاع الخاص", "Minimum wage, private sector"), ("7,000 جنيه شهريًا منذ 1 مارس 2025", "EGP 7,000 a month since 1 March 2025")),
                    (("تأمينات صاحب العمل", "Employer social insurance"), ("18.75% من الأجر التأميني", "18.75% of the insured wage")),
                    (("تأمينات الموظف", "Employee social insurance"), ("11% من الأجر التأميني", "11% of the insured wage")),
                    (("الأجر التأميني 2026", "Insured wage, 2026"), ("من 2,700 إلى 16,700 جنيه شهريًا", "EGP 2,700 to 16,700 a month")),
                    (("العلاوة الدورية", "Periodic raise"), ("3% على الأقل من الأجر التأميني سنويًا (م 12 من قانون العمل 14/2025)", "At least 3% of the insured wage a year (Labour Law 14/2025 Art 12)")),
                    (("الموظفون الأجانب", "Foreign employees"), ("ترخيص عمل وإقامة بقصد العمل (م 71)", "Work permit and residence for work (Art 71)")),
                ]),
                ("p", ("الفرق بين الخيارات ليس في هذه التكاليف، بل في من يسجّل الموظفين ويدير الرواتب والضرائب ويتحمل مسؤولية صاحب العمل، وفي التكاليف الثابتة حولها.",
                       "The options don't differ on these costs. They differ on who registers employees, runs payroll and tax, carries the employer's liability, and on the fixed costs around them.")),
            ],
        },
        {
            "title": ("مثال محسوب: تكلفة موظف واحد", "Worked example: the cost of one employee"),
            "sub": ("راتب إجمالي 10,000 جنيه شهريًا، قواعد 2026", "Gross salary EGP 10,000 a month, 2026 rules"),
            "blocks": [
                ("ex", ("راتب إجمالي 10,000 جنيه", "Gross salary EGP 10,000"), [
                    ("تأمينات الموظف: 10,000 × 11% = 1,100.", "Employee insurance: 10,000 × 11% = 1,100."),
                    ("ضريبة كسب العمل: 592.50 شهريًا، وصندوق الشهداء: 5.", "Payroll tax: 592.50 a month; Martyrs Fund: 5."),
                    ("صافي الراتب: 8,302.50.", "Net pay: 8,302.50."),
                    ("تأمينات صاحب العمل: 10,000 × 18.75% = 1,875.", "Employer insurance: 10,000 × 18.75% = 1,875."),
                ], ("تكلفة الشركة: 11,875 جنيهًا شهريًا قبل أي رسوم إدارة", "Company cost: EGP 11,875 a month before any management fee")),
                ("p", ("مع موارد ومهارات تضاف رسوم ثابتة لكل موظف فوق هذه التكلفة، وتغطي التوظيف والعقود والرواتب والتأمينات. ومع الكيان الخاص تضاف تكاليف التأسيس والمكتب والمحاسبة والإدارة المحلية.",
                       "With Talent360 a fixed fee per employee is added on top, covering recruitment, contracts, payroll and insurance. With your own entity you add set-up, office, accounting and local management costs.")),
                ("tip", ("استخدم حاسبة الراتب على صفحتنا لأي راتب آخر، أو لكشف رواتب الفريق كله مرة واحدة.",
                         "Use the salary calculator on our page for any other salary, or for your whole team's payroll at once.")),
            ],
        },
        {
            "title": ("متى يناسبك كل خيار؟", "When does each option fit?"),
            "sub": ("ثلاثة سيناريوهات شائعة", "Three common scenarios"),
            "blocks": [
                ("table", [("الخيار", "Option"), ("يناسبك إذا", "Fits when")], [
                    [("فريق عبر موارد ومهارات", "Team via Talent360"), ("تريد البدء بسرعة، أو اختبار السوق قبل الالتزام، أو تكبير الفريق وتصغيره بمرونة دون إدارة محلية.", "You want to start fast, test the market before committing, or scale the team up and down without local management.")],
                    [("كيان خاص في مصر", "Own Egypt entity"), ("تخطط لوجود طويل وكبير، وتريد سيطرة كاملة، ومستعد لوقت التأسيس ورأس المال والإدارة المحلية.", "You plan a long, large presence, want full control, and can take on set-up time, capital and local management.")],
                    [("صاحب عمل مسجل (EOR)", "Employer of record (EOR)"), ("تحتاج عقود توظيف وامتثالًا فقط، وتدير التوظيف والتشغيل اليومي بنفسك.", "You only need employment contracts and compliance, and handle recruitment and day-to-day operations yourself.")],
                ]),
            ],
        },
        {
            "title": ("قائمة قرار سريعة", "Quick decision checklist"),
            "sub": ("أجب عنها قبل أن تختار", "Answer these before you choose"),
            "blocks": [
                ("check", [
                    ("كم موظفًا تحتاج في أول 12 شهرًا؟", "How many people do you need in the first 12 months?"),
                    ("متى يجب أن يبدأ أول موظف؟", "When must the first hire start?"),
                    ("هل تريد اختبار السوق قبل التزام طويل؟", "Do you want to test the market before a long commitment?"),
                    ("من سيدير الرواتب والتأمينات والضرائب يوميًا؟", "Who will run payroll, insurance and tax day to day?"),
                    ("هل لديك فريق إدارة محلي في مصر؟", "Do you have local management in Egypt?"),
                    ("كيف ستخرج من السوق إذا تغيرت خطتك؟", "How would you exit if your plans change?"),
                ]),
            ],
        },
    ],
}
