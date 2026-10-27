"""Labour-law lead magnets: employer guides to Egypt's Labour Law 14/2025 (with employee
benefits) and Saudi Arabia's Labour Law after the 2025 amendments, in Arabic and English.

python3 guides/guides.py  -> guides/out/<tool>-<lang>.html, then render.js prints the PDFs.
Facts come only from the sources listed in each guide; re-check them before each edition.
"""
import html, os, base64

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
BRAND = os.path.join(HERE, "..", "assets", "img", "brand")
BOOK = {"ar": "https://talent-360.me/eddekhar/ar/#book", "en": "https://talent-360.me/eddekhar/en/#book"}
EDITION = {"ar": "إصدار أكتوبر 2026", "en": "October 2026 edition"}


def img64(name):
    with open(os.path.join(BRAND, name), "rb") as f:
        ext = name.rsplit(".", 1)[1]
        return "data:image/%s;base64,%s" % ("png" if ext == "png" else ext, base64.b64encode(f.read()).decode())


E = html.escape

EG = {
    "ar": dict(
        title="دليل صاحب العمل لقانون العمل المصري الجديد 14 لسنة 2025",
        sub="أهم ما تغيّر لأصحاب العمل، ومزايا الموظفين في مصر لعام 2026",
        intro="صدر قانون العمل رقم 14 لسنة 2025 في 3 مايو 2025، وبدأ العمل به في 1 سبتمبر 2025، وألغى القانون 12 لسنة 2003. وبدأت المحاكم العمالية المتخصصة في 1 أكتوبر 2025. يلخّص هذا الدليل ما يحتاج صاحب العمل لمعرفته، ومعه مزايا الموظفين القانونية والمعتادة في السوق المصري.",
        sections=[
            ("العقود والتوثيق", [
                "يُحرَّر عقد العمل باللغة العربية من أربع نسخ، ويجوز للعامل الأجنبي نسخة بلغته إلى جانب العربية. ويجوز التوقيع الورقي أو الإلكتروني.",
                "يقدّم صاحب العمل بيانًا بالعاملين وأجورهم لوزارة العمل، ويحدّثه في يناير من كل عام.",
                "يُحفظ ملف كل عامل، ورقيًا أو إلكترونيًا، لمدة خمس سنوات بعد انتهاء الخدمة.",
                "يعترف القانون بالعمل عن بُعد، والعمل الجزئي، والساعات المرنة، وتقاسم الوظيفة.",
                "لا يجوز تشغيل غير المصريين إلا بترخيص عمل من الوزارة المختصة.",
            ]),
            ("فترة الاختبار والإنهاء والاستقالة", [
                "فترة الاختبار بحد أقصى ثلاثة أشهر، ولا تتكرر مع نفس صاحب العمل.",
                "مهلة الإخطار ثلاثة أشهر في العقد غير محدد المدة، أيًا كانت مدة الخدمة.",
                "الاستقالة تُعتمد من الجهة الإدارية المختصة، ويرد صاحب العمل عليها خلال 10 أيام. واستمارات الاستقالة الموقعة مسبقًا دون تاريخ باطلة.",
                "العقد محدد المدة إذا أنهاه صاحب العمل: تعويض بأجر شهر عن كل سنة خدمة.",
                "الفصل التأديبي يحتاج حكمًا من المحكمة العمالية.",
            ]),
            ("ساعات العمل والإضافي", [
                "8 ساعات يوميًا و48 ساعة أسبوعًا بحد أقصى، و12 ساعة تواجد كحد أقصى في اليوم.",
                "يكفي إخطار الوزارة بالعمل الإضافي خلال 7 أيام بدلًا من الحصول على إذن مسبق.",
                "أجر الإضافي: الأجر + 35% نهارًا، و+ 70% ليلًا.",
            ]),
            ("الأجور والزيادة السنوية", [
                "علاوة دورية سنوية لا تقل عن 3% من الأجر التأميني (المادة 12)، ولا يُعفى منها إلا بموافقة المجلس القومي للأجور.",
                "الحد الأدنى للأجور في القطاع الخاص 7,000 جنيه شهريًا منذ 1 مارس 2025 (آخر قرار منشور للمجلس القومي للأجور).",
                "صندوق التدريب والتأهيل: 0.25% من الحد الأدنى للأجر التأميني عن كل عامل، بحد أدنى 10 وأقصى 30 جنيهًا، بدلًا من 1% من صافي الأرباح.",
                "يمكن إثبات صرف الأجر بالتحويل البنكي.",
            ]),
            ("حماية بيئة العمل والعقوبات", [
                "تجريم التحرش والتنمر والعنف اللفظي والجسدي والنفسي، بالطرق التقليدية أو التقنية.",
                "الغرامات من 1,000 إلى 100,000 جنيه، ويُسأل المدير المسؤول مع صاحب العمل.",
            ]),
        ],
        benefits_h="مزايا الموظفين في مصر 2026",
        benefits=[
            ("التأمينات الاجتماعية (قانون 148/2019)", "صاحب العمل 18.75% والموظف 11% من أجر الاشتراك. حدود الأجر التأميني من يناير 2026: 2,700 إلى 16,700 جنيه شهريًا.", "قانوني"),
            ("الإجازة السنوية", "15 يومًا في السنة الأولى، 21 يومًا من السنة الثانية، 30 يومًا بعد 10 سنوات أو سن الخمسين، و45 يومًا لذوي الإعاقة.", "قانوني"),
            ("الإجازة المرضية", "مدفوعة عبر منظومة التأمينات الاجتماعية بشهادة طبية من الجهة المختصة.", "قانوني"),
            ("إجازة الوضع", "أربعة أشهر مدفوعة، منها 45 يومًا على الأقل بعد الولادة، حتى ثلاث مرات طوال الخدمة ودون اشتراط مدة خدمة.", "قانوني"),
            ("إجازة رعاية الطفل", "حتى سنتين بدون أجر، ثلاث مرات، بعد سنة خدمة، في المنشآت التي تضم 50 عاملًا فأكثر.", "قانوني"),
            ("إجازة الأب", "يوم مدفوع يوم الولادة، حتى ثلاث مرات، ولا يُخصم من الإجازة السنوية.", "قانوني"),
            ("الزيادة السنوية", "3% على الأقل من الأجر التأميني سنويًا.", "قانوني"),
            ("التأمين الطبي الخاص", "معتاد في الشركات: تقريبًا 15,000 إلى 45,000 جنيه للموظف سنويًا لتغطية فردية.", "سوقي"),
            ("مكافأة نهاية العام", "غير إلزامية. المعتاد نصف شهر إلى شهر من الأساسي، وقد تصل إلى 1 إلى 3 أشهر حسب الأداء والقطاع.", "سوقي"),
            ("العمل المرن", "معترف به قانونًا، والمعتاد يوم إلى ثلاثة أيام من المنزل للوظائف المكتبية.", "سوقي"),
            ("ميزانية التعلّم", "تقريبًا 5,000 إلى 25,000 جنيه للموظف سنويًا.", "سوقي"),
        ],
        col_benefit="الميزة", col_detail="التفاصيل", col_type="النوع",
        checklist_h="ما الذي تفعله الآن",
        checklist=[
            "راجع عقودك: عربية، أربع نسخ، ومهلة إخطار ثلاثة أشهر.",
            "حدّث سياسة الإجازات (15/21/30/45 يومًا) وإجازة الوضع وإجازة الأب.",
            "أدرج العلاوة السنوية 3% في دورة الرواتب.",
            "أعدّ بيان العاملين السنوي، واحفظ الملفات خمس سنوات.",
            "حدّث إجراءات الاستقالة والتأديب لتتوافق مع الاعتماد الإداري والمحاكم العمالية.",
        ],
        cta_h="نبني فريقك في مصر وندير موارده البشرية بالكامل",
        cta_p="موارد ومهارات تتولى التوظيف والرواتب والتأمينات والامتثال لقانون العمل الجديد، برسوم ثابتة لكل موظف. احجز HR Health Check مجانًا.",
        cta_btn="احجز فحصك المجاني",
        sources_h="المصادر",
        disclaimer="هذا الدليل للتوعية العامة وليس استشارة قانونية. الأرقام كما نُشرت حتى أكتوبر 2026، وقد تتغير بالقرارات التنفيذية. راجع النص الرسمي في الجريدة الرسمية أو استشر محاميًا مرخصًا قبل اتخاذ أي قرار.",
        stat_type={"قانوني": "قانوني", "سوقي": "ممارسة سوقية"},
    ),
    "en": dict(
        title="Employer guide to Egypt's new Labour Law No. 14 of 2025",
        sub="What changed for employers, plus employee benefits in Egypt for 2026",
        intro="Labour Law No. 14 of 2025 was issued on 3 May 2025, took effect on 1 September 2025 and repealed Law No. 12 of 2003. The new specialised labour courts started on 1 October 2025. This guide sums up what an employer needs to know, together with the statutory and market-standard employee benefits in Egypt.",
        sections=[
            ("Contracts and records", [
                "Employment contracts are written in Arabic in four copies; a non-Egyptian employee may also have a copy in their own language. Paper or electronic signature is allowed.",
                "Employers file a statement of employees and salaries with the Ministry of Labour and update it every January.",
                "Each employee's file, paper or electronic, is kept for five years after employment ends.",
                "The law recognises remote work, part-time work, flexible hours and job sharing.",
                "Non-Egyptians may only be employed with a work licence from the competent ministry.",
            ]),
            ("Probation, termination and resignation", [
                "Probation is capped at three months, once per employee with the same employer.",
                "Notice on an indefinite contract is three months, regardless of length of service.",
                "Resignations are ratified by the competent administrative authority and the employer responds within 10 days. Pre-signed, undated resignations are void.",
                "Fixed-term contract ended by the employer: one month's salary per year of service.",
                "Disciplinary dismissal requires a ruling from the labour court.",
            ]),
            ("Working hours and overtime", [
                "8 hours a day and 48 hours a week, with at most 12 hours of presence a day.",
                "Overtime now needs notification to the Ministry within 7 days instead of prior approval.",
                "Overtime pay: wage + 35% by day and + 70% at night.",
            ]),
            ("Pay and the annual raise", [
                "Annual periodic raise of at least 3% of the insured wage (Article 12); waivers need National Wages Council approval.",
                "Private-sector minimum wage: EGP 7,000 a month since 1 March 2025 (latest published National Wages Council decision).",
                "Training and Qualification Fund: 0.25% of the minimum insured wage per employee, minimum EGP 10 and maximum EGP 30, replacing 1% of net profits.",
                "Salary payment can be evidenced by bank transfer.",
            ]),
            ("Workplace protection and penalties", [
                "Harassment, bullying and verbal, physical or psychological violence are criminalised, offline or online.",
                "Fines range from EGP 1,000 to EGP 100,000, and the responsible manager is liable alongside the employer.",
            ]),
        ],
        benefits_h="Employee benefits in Egypt, 2026",
        benefits=[
            ("Social insurance (Law 148/2019)", "Employer 18.75% and employee 11% of the insured wage. Insured wage from January 2026: EGP 2,700 to 16,700 a month.", "law"),
            ("Annual leave", "15 days in year one, 21 days from year two, 30 days after 10 years or at age 50, and 45 days for employees with disabilities.", "law"),
            ("Sick leave", "Paid through the social insurance system, on a certificate from the competent medical authority.", "law"),
            ("Maternity leave", "Four months paid, at least 45 days of it after birth, up to three times in service, with no minimum service.", "law"),
            ("Childcare leave", "Up to two years unpaid, three times, after one year of service, in establishments with 50+ employees.", "law"),
            ("Paternity leave", "One paid day on the day of birth, up to three times, not deducted from annual leave.", "law"),
            ("Annual raise", "At least 3% of the insured wage every year.", "law"),
            ("Private medical insurance", "Common practice: about EGP 15,000 to 45,000 per employee a year for individual cover.", "market"),
            ("Year-end bonus", "Not mandatory. Typically half a month to one month of base pay; 1 to 3 months for strong performers or sectors.", "market"),
            ("Flexible work", "Recognised in law; typically 1 to 3 days a week from home for office roles.", "market"),
            ("Learning budget", "About EGP 5,000 to 25,000 per employee a year.", "market"),
        ],
        col_benefit="Benefit", col_detail="Detail", col_type="Type",
        checklist_h="What to do now",
        checklist=[
            "Review contracts: Arabic, four copies, three-month notice.",
            "Update the leave policy (15/21/30/45 days), maternity and paternity leave.",
            "Build the 3% annual raise into your payroll cycle.",
            "Prepare the annual employee statement and keep files for five years.",
            "Align resignation and disciplinary procedures with administrative ratification and the labour courts.",
        ],
        cta_h="We build your team in Egypt and run its HR end to end",
        cta_p="Talent360 handles hiring, payroll, social insurance and compliance with the new labour law, for a fixed fee per employee. Book a free HR Health Check.",
        cta_btn="Book your free check",
        sources_h="Sources",
        disclaimer="This guide is general information, not legal advice. Figures are as published up to October 2026 and may change with executive regulations. Check the official text in the Official Gazette or consult a licensed lawyer before acting.",
        stat_type={"law": "Statutory", "market": "Market practice"},
    ),
    "sources": [
        ("Law No. 14 of 2025, Labour Code (Arabic text, Art. 1–50)", "https://www.manshurat.org/content/qnwn-lml-ljdyd-2025"),
        ("EY: Egypt enacts new labor law (1 September 2025)", "https://www.ey.com/en_gl/technical/tax-alerts/egypt-enacts-new-labor-law-with-changes-affecting-employers-beginning-1-september-2025"),
        ("Amereller: Egypt New Labor Law No. 14 of 2025", "https://amereller.com/publication/egypt-new-labor-law-no-14-of-2025/"),
        ("ZenHR: Egypt Labor Law at a glance", "https://www.zenhr.com/en/egypt-labor-law"),
        ("Atlas HXM: Employee benefits in Egypt, 2026", "https://www.atlashxm.com/resources/employee-benefits-in-egypt"),
        ("Ministry of Investment: private-sector minimum wage EGP 7,000", "https://moic.gov.eg/news/1998"),
    ],
}

SA = {
    "ar": dict(
        title="دليل صاحب العمل لنظام العمل السعودي بعد تعديلات 2025",
        sub="أهم الأحكام التي يحتاجها صاحب العمل في المملكة",
        intro="دخلت تعديلات نظام العمل السعودي حيز التنفيذ في فبراير 2025، وغيّرت فترة التجربة ومهل الإشعار والإجازات والعقود محددة المدة لغير السعوديين. يلخّص هذا الدليل الأحكام الأساسية بأرقام المواد.",
        sections=[
            ("فترة التجربة والعقود", [
                "فترة التجربة حتى 180 يومًا، وتُذكر صراحة في العقد (المادة 53 المعدّلة). ويجوز لأي طرف الإنهاء خلالها دون مكافأة أو تعويض (المادة 80).",
                "عقد غير السعودي الذي لا تُحدد مدته يُعد عقدًا لمدة سنة، ويتجدد لمدة مماثلة إذا استمر الطرفان.",
                "حظر التمييز في الأجر وفرص العمل بسبب الجنس أو السن أو الجنسية أو الحالة الاجتماعية أو الإعاقة.",
            ]),
            ("الإشعار والاستقالة والإنهاء", [
                "العقد غير محدد المدة: إشعار 30 يومًا من العامل و60 يومًا من صاحب العمل لمن يتقاضى أجرًا شهريًا (المادة 75 المعدّلة).",
                "الاستقالة: يرد صاحب العمل خلال 30 يومًا، ويجوز تأجيلها حتى 60 يومًا بمبرر مكتوب.",
                "الإنهاء لسبب غير مشروع في العقد غير محدد المدة: أجر 15 يومًا عن كل سنة خدمة، وبحد أدنى أجر شهرين (المادة 77).",
            ]),
            ("مكافأة نهاية الخدمة", [
                "نصف شهر عن كل سنة من السنوات الخمس الأولى، وشهر عن كل سنة بعدها، على أساس آخر أجر (المادة 84).",
                "عند الاستقالة: لا شيء قبل سنتين، ثلث المكافأة من 2 إلى 5 سنوات، ثلثاها من 5 إلى 10، وكاملة بعد 10 سنوات (المادة 85).",
                "تُصرف خلال أسبوع من انتهاء العلاقة، أو أسبوعين عند الاستقالة (المادة 88).",
            ]),
            ("الوقت الإضافي والإجازات", [
                "أجر الإضافي: أجر الساعة + 50% من الأجر الأساسي، ويجوز التعويض بإجازة مدفوعة بموافقة العامل (المادة 107 المعدّلة).",
                "الإجازة السنوية 21 يومًا، و30 يومًا بعد خمس سنوات متصلة (المادة 109).",
                "المرضية: 30 يومًا بأجر كامل، ثم 60 يومًا بثلاثة أرباع الأجر، ثم 30 يومًا بدون أجر في السنة (المادة 117).",
                "الوضع 12 أسبوعًا بأجر كامل، منها 6 أسابيع إلزامية بعد الولادة (المادة 151 المعدّلة).",
                "الزواج 5 أيام، المولود 3 أيام خلال 7 أيام من الولادة، الوفاة 5 أيام للزوج أو الوالدين أو الأبناء و3 أيام للأخ أو الأخت (المادة 113 المعدّلة).",
            ]),
            ("التأمينات والأجور", [
                "غير السعوديين: أخطار مهنية 2% على صاحب العمل.",
                "السعوديون المشتركون قبل 3 يوليو 2024: معاشات 9% + 9%، ساند 0.75% + 0.75%، وأخطار مهنية 2% على صاحب العمل.",
                "المشتركون الجدد من 3 يوليو 2024: المعاش يبدأ 9% لكل طرف ويرتفع 0.5 نقطة سنويًا من يوليو 2025 حتى 11%. الحد الأعلى للأجر الخاضع 45,000 ريال.",
                "حماية الأجور (مدد): رفع ملف الأجور شهريًا، ويغطي الشهر السابق فقط منذ مارس 2025.",
            ]),
        ],
        checklist_h="ما الذي تفعله الآن",
        checklist=[
            "حدّث نماذج العقود: فترة التجربة، ومدة العقد لغير السعوديين، ومهل الإشعار الجديدة.",
            "عدّل سياسة الإجازات: الوضع 12 أسبوعًا، والمولود 3 أيام، ووفاة الأخ أو الأخت.",
            "راجع احتساب مكافأة نهاية الخدمة وجداول الإضافي.",
            "تأكد من رفع ملف مدد شهريًا ومطابقة اشتراكات التأمينات.",
        ],
        cta_h="نتولى امتثالك لنظام العمل في السعودية",
        cta_p="موارد ومهارات تدير الموارد البشرية والتوظيف والرواتب ومنصات قوى ومدد والتأمينات. احجز HR Health Check مجانًا.",
        cta_btn="احجز فحصك المجاني",
        sources_h="المصادر",
        disclaimer="هذا الدليل للتوعية العامة وليس استشارة قانونية. الأحكام كما نُشرت حتى أكتوبر 2026. راجع النص الرسمي على موقع هيئة الخبراء أو وزارة الموارد البشرية أو استشر محاميًا مرخصًا قبل اتخاذ أي قرار.",
    ),
    "en": dict(
        title="Employer guide to Saudi Labour Law after the 2025 amendments",
        sub="The rules an employer in the Kingdom needs to know",
        intro="The Saudi Labour Law amendments came into force in February 2025, changing probation, notice periods, leave and fixed-term contracts for non-Saudi employees. This guide sums up the core rules with their article numbers.",
        sections=[
            ("Probation and contracts", [
                "Probation of up to 180 days, stated expressly in the contract (amended Art. 53). Either party may end the contract during it without award or compensation (Art. 80).",
                "A non-Saudi's contract without a stated term is deemed a one-year contract and renews for the same period if both parties continue.",
                "No discrimination in pay or opportunity by gender, age, nationality, marital status or disability.",
            ]),
            ("Notice, resignation and termination", [
                "Indefinite contract, monthly pay: 30 days' notice from the employee, 60 days from the employer (amended Art. 75).",
                "Resignation: the employer responds within 30 days and may defer it by up to 60 days with a written reason.",
                "Termination for an invalid reason on an indefinite contract: 15 days' wage per year of service, minimum two months' wage (Art. 77).",
            ]),
            ("End-of-service award", [
                "Half a month's wage for each of the first five years and one month for each year after, on the last wage (Art. 84).",
                "On resignation: nothing under 2 years, one third from 2 to 5 years, two thirds from 5 to 10, the full award after 10 (Art. 85).",
                "Paid within one week of the end of employment, or two weeks on resignation (Art. 88).",
            ]),
            ("Overtime and leave", [
                "Overtime: hourly wage + 50% of the basic wage, or paid time off with the employee's consent (amended Art. 107).",
                "Annual leave of 21 days, 30 days after five continuous years (Art. 109).",
                "Sick leave: 30 days on full pay, 60 days at three quarters, then 30 days unpaid in a year (Art. 117).",
                "Maternity: 12 weeks on full pay, 6 of them mandatory after birth (amended Art. 151).",
                "Marriage 5 days; birth of a child 3 days within 7 days; bereavement 5 days for a spouse, parent or child and 3 days for a sibling (amended Art. 113).",
            ]),
            ("Social insurance and wages", [
                "Non-Saudis: occupational hazards at 2%, paid by the employer.",
                "Saudis insured before 3 July 2024: pension 9% + 9%, SANED 0.75% + 0.75%, occupational hazards 2% by the employer.",
                "Saudis insured from 3 July 2024: pension starts at 9% each side and rises 0.5 points a year from July 2025 to 11%. Contributory wage cap SAR 45,000.",
                "Wage Protection (Mudad): monthly wage file, covering only the previous month since March 2025.",
            ]),
        ],
        checklist_h="What to do now",
        checklist=[
            "Update contract templates: probation, term for non-Saudis and the new notice periods.",
            "Revise the leave policy: 12-week maternity, 3-day birth leave, sibling bereavement.",
            "Check end-of-service and overtime calculations.",
            "Make sure the Mudad file goes up monthly and GOSI contributions reconcile.",
        ],
        cta_h="We keep you compliant with Saudi Labour Law",
        cta_p="Talent360 runs HR, hiring, payroll, Qiwa, Mudad and GOSI for you. Book a free HR Health Check.",
        cta_btn="Book your free check",
        sources_h="Sources",
        disclaimer="This guide is general information, not legal advice. Rules are as published up to October 2026. Check the official text on the Bureau of Experts or HRSD websites, or consult a licensed lawyer, before acting.",
    ),
    "sources": [
        ("Rödl & Partner: Saudi labour law 2025, the most important amendments", "https://www.roedl.com/en/insights/saudi-arabia-labor-law-amendments-impact/"),
        ("Teamed: Employment law in Saudi Arabia, 2026 guide for employers", "https://www.teamed.global/gulf-employment-law/saudi-arabia"),
        ("Saudipedia: نظام العمل في السعودية", "https://saudipedia.com/نظام-العمل-في-السعودية"),
    ],
}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: %s; color: #26324D; font-size: 10.5pt; line-height: 1.75; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.cover { background: linear-gradient(150deg, #0E183C 0%%, #13285A 70%%, #168C7C 140%%); color: #fff; padding: 34px 44px 36px; }
.brand { display: flex; align-items: center; justify-content: space-between; gap: 16px; }
.brand .mm { display: flex; align-items: center; gap: 10px; }
.brand img.mark { height: 46px; }
.brand .by { display: flex; align-items: center; gap: 6px; font: 600 9pt Montserrat, sans-serif; color: #CFE3F0; }
.brand .by img { height: 11px; }
.edition { font-size: 9pt; color: #5FE3CF; border: 1px solid rgba(95,227,207,.5); border-radius: 99px; padding: 3px 12px; }
h1 { font-size: 21pt; line-height: 1.35; margin: 26px 0 8px; color: #fff; }
.sub { color: #5FE3CF; font-weight: 700; margin: 0 0 14px; font-size: 12pt; }
.intro { color: #D5E2EE; margin: 0; max-width: 620px; }
main { padding: 26px 44px 10px; }
h2 { font-size: 13pt; color: #0E183C; margin: 20px 0 8px; padding-inline-start: 12px; border-inline-start: 4px solid #1FC9B1; line-height: 1.4; }
ul { margin: 0; padding-inline-start: 20px; }
li { margin: 3px 0; }
li::marker { color: #168C7C; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 26px; }
.sec { break-inside: avoid; }
table { width: 100%%; border-collapse: collapse; margin-top: 6px; font-size: 9.6pt; }
th { background: #0E183C; color: #fff; text-align: start; padding: 7px 10px; font-weight: 700; }
td { padding: 7px 10px; border-bottom: 1px solid #DCE7EE; vertical-align: top; }
tr { break-inside: avoid; }
td.k { font-weight: 700; color: #0E183C; width: 28%%; }
.tag { display: inline-block; font-size: 8pt; font-weight: 700; padding: 1px 8px; border-radius: 99px; white-space: nowrap; }
.tag.law { background: #E3F6F3; color: #168C7C; }
.tag.market { background: #EEF1F7; color: #46536F; }
.check { background: #E3F6F3; border-radius: 14px; padding: 12px 18px 12px; margin-top: 18px; break-inside: avoid; }
.check h2 { margin-top: 4px; border: 0; padding: 0; }
.check li::marker { content: "✓  "; color: #168C7C; font-weight: 800; }
.cta { margin: 18px 0 0; background: #0E183C; color: #fff; border-radius: 14px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; gap: 18px; break-inside: avoid; }
.cta h3 { margin: 0 0 4px; font-size: 12.5pt; color: #fff; }
.cta p { margin: 0; color: #C9D6E6; font-size: 9.5pt; }
.cta a { background: #1FC9B1; color: #0E183C; font-weight: 800; text-decoration: none; padding: 9px 16px; border-radius: 99px; white-space: nowrap; }
.src { margin-top: 16px; font-size: 8.4pt; color: #5A6785; break-inside: avoid; }
.src h2 { font-size: 10pt; margin: 0 0 4px; border: 0; padding: 0; }
.src a { color: #168C7C; word-break: break-all; }
.disc { font-size: 8.2pt; color: #6B7894; border-top: 1px solid #DCE7EE; margin-top: 10px; padding-top: 8px; }
"""


def render(data, lang, benefits=False):
    L = data[lang]
    rtl = lang == "ar"
    font = "'Almarai', 'Noto Sans Arabic', sans-serif" if rtl else "Montserrat, 'Noto Sans', sans-serif"
    fonts = "Almarai:wght@400;700;800" if rtl else "Montserrat:wght@400;600;700;800"
    secs = "".join('<div class="sec"><h2>%s</h2><ul>%s</ul></div>' % (E(h), "".join("<li>%s</li>" % E(i) for i in items)) for h, items in L["sections"])
    ben = ""
    if benefits:
        rows = "".join('<tr><td class="k">%s</td><td>%s</td><td><span class="tag %s">%s</span></td></tr>'
                       % (E(k), E(d), "law" if t in ("قانوني", "law") else "market", E(L["stat_type"][t])) for k, d, t in L["benefits"])
        ben = '<h2>%s</h2><table><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table>' % (
            E(L["benefits_h"]), E(L["col_benefit"]), E(L["col_detail"]), E(L["col_type"]), rows)
    src = "".join('<li>%s: <a href="%s">%s</a></li>' % (E(t), E(u), E(u)) for t, u in data["sources"])
    return """<!doctype html><html lang="%s" dir="%s"><head><meta charset="utf-8"><title>%s</title>
<link href="https://fonts.googleapis.com/css2?family=%s&display=swap" rel="stylesheet"><style>%s</style></head><body>
<header class="cover"><div class="brand"><div class="mm"><img class="mark" src="%s" alt="موارد ومهارات"><span class="by" dir="ltr">by <img src="%s" alt="Talent360"></span></div><span class="edition">%s</span></div>
<h1>%s</h1><p class="sub">%s</p><p class="intro">%s</p></header>
<main><div class="cols">%s</div>%s
<div class="check"><h2>%s</h2><ul>%s</ul></div>
<div class="cta"><div><h3>%s</h3><p>%s</p></div><a href="%s">%s</a></div>
<div class="src"><h2>%s</h2><ul>%s</ul><p class="disc">%s</p></div></main></body></html>""" % (
        lang, "rtl" if rtl else "ltr", E(L["title"]), fonts, CSS % font,
        img64("mawared-mark-white.png"), img64("talent360-wordmark-white.png"), E(EDITION[lang]),
        E(L["title"]), E(L["sub"]), E(L["intro"]), secs, ben,
        E(L["checklist_h"]), "".join("<li>%s</li>" % E(i) for i in L["checklist"]),
        E(L["cta_h"]), E(L["cta_p"]), BOOK[lang], E(L["cta_btn"]),
        E(L["sources_h"]), src, E(L["disclaimer"]))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for tool, data, ben in (("labour_law_eg", EG, True), ("labour_law_sa", SA, False)):
        for lang in ("ar", "en"):
            with open(os.path.join(OUT, "%s-%s.html" % (tool, lang)), "w", encoding="utf-8") as f:
                f.write(render(data, lang, ben))
    print("ok")
