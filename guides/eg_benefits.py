"""Employee benefits in Egypt, 2026: what the law requires, what it costs, and what the market adds.
Sources: Labour Law 14/2025 (article text), Social Insurance Law 148/2019 and the NOSI 2026 wage limits,
Income Tax Law 91/2005 as amended by Law 7/2024, NWC minimum-wage decision (MOIC), Companies Law 159/1981.
Payroll examples use the same rules as the landing-page calculator."""

GUIDE = {
    "kicker": ("دليل صاحب العمل", "Employer guide"),
    "title": ("مزايا الموظفين في مصر 2026", "Employee benefits in Egypt, 2026"),
    "sub": ("ما يفرضه القانون، وتكلفته الحقيقية على الشركة، والمزايا التي يقدّمها السوق، وكيف تبني باقة مزايا تناسب ميزانيتك.",
            "What the law requires, what it really costs, what the market adds, and how to build a benefits package that fits your budget."),
    "pills": [("التأمينات والضريبة 2026", "2026 insurance and tax"), ("أمثلة رواتب محسوبة", "Worked payslips"), ("تكلفة صاحب العمل", "Employer cost"), ("خطوات بناء الباقة", "Package design steps")],
    "intro": ("المزايا في مصر نوعان: مزايا يفرضها القانون على كل صاحب عمل، ومزايا إضافية تقدّمها الشركات لتجذب الكفاءات وتحتفظ بها. "
              "يعرض هذا الدليل الأرقام المعمول بها في 2026، ويحسب لك تكلفة الموظف الفعلية، ثم يقترح طريقة عملية لبناء باقة مزايا.",
              "Benefits in Egypt come in two kinds: those the law requires of every employer, and extras companies add to attract and keep people. "
              "This guide gives the figures in force in 2026, works out the real cost of an employee, and sets out a practical way to build a package."),
    "cta_h": ("صمّم باقة مزايا تنافسية دون مفاجآت في التكلفة", "Design a competitive package with no cost surprises"),
    "cta_p": ("في فحص مجاني مدته 30 دقيقة، نراجع هيكل الرواتب والمزايا والتأمينات لديك، ونحسب لك تكلفة كل خيار.",
              "In a free 30-minute check we review your pay structure, benefits and social insurance, and cost each option for you."),
    "note": ("الأرقام كما نُشرت في 2026. الأمثلة تقديرية لأغراض التخطيط.", "Figures as published in 2026. Examples are estimates for planning."),
    "sections": [
        {
            "title": ("المزايا الإلزامية والإضافية", "Statutory and supplementary benefits"),
            "sub": ("الفرق بينهما، ولماذا يهمّك", "The difference, and why it matters"),
            "blocks": [
                ("cols", [
                    ("kv", [
                        (("إلزامية", "Statutory"), ("يفرضها القانون: الحد الأدنى للأجر، والعلاوة السنوية، والتأمينات، والإجازات، ومكافآت نهاية الخدمة في حالاتها", "Required by law: minimum wage, annual raise, social insurance, leave, and end-of-service payments where due")),
                    ]),
                    ("kv", [
                        (("إضافية", "Supplementary"), ("تختارها الشركة: التأمين الطبي الخاص، والمكافآت، والبدلات، والتدريب، وغيرها", "Chosen by the company: private medical cover, bonuses, allowances, training and more")),
                    ]),
                ]),
                ("p", ("أي ميزة نقدية أو عينية تذكرها في العقد تصبح حقًا للموظف، ويجب أن يذكر العقد الأجر وسائر المزايا النقدية والعينية المتفق عليها (المادة 89 من قانون العمل). ولا ينتقص القانون الجديد من أي مزايا حصل عليها العاملون قبل العمل به.",
                       "Any cash or in-kind benefit written into the contract becomes the employee's right; the contract must list the wage and every agreed cash and in-kind benefit (Labour Law Art 89). The new law does not reduce any benefits employees already had.")),
                ("tip", ("فرّق في العرض الوظيفي بين الأجر الأساسي والبدلات والمزايا. هذا يوضّح للموظف القيمة الكاملة، ويسهّل عليك حساب التأمينات والعلاوة.",
                         "In the offer letter, separate base pay, allowances and benefits. It shows the employee the full value and makes insurance and raise calculations easier.")),
            ],
        },
        {
            "title": ("الحد الأدنى للأجر والعلاوة السنوية", "Minimum wage and the annual raise"),
            "sub": ("قانون العمل 14 لسنة 2025 وقرارات المجلس القومي للأجور", "Labour Law 14/2025 and National Wages Council decisions"),
            "blocks": [
                ("kv", [
                    (("الحد الأدنى للأجر، القطاع الخاص", "Minimum wage, private sector"), ("7,000 جنيه شهريًا منذ 1 مارس 2025", "EGP 7,000 a month since 1 March 2025")),
                    (("المراجعة", "Review"), ("مرة في السنة على الأقل بقرار رئيس الوزراء 3165 لسنة 2026", "At least once a year under PM Decision 3165/2026")),
                    (("العلاوة الدورية", "Periodic raise"), ("3% على الأقل من الأجر التأميني بعد سنة من التعيين أو من آخر علاوة (م 12)", "At least 3% of the insured wage a year after hiring or the last raise (Art 12)")),
                    (("المساواة في الأجر", "Equal pay"), ("أجر متساوٍ عن العمل ذي القيمة المتساوية، بكل عناصره (م 53)", "Equal pay for work of equal value, in every element (Art 53)")),
                ]),
                ("p", ("لا يُعفى صاحب العمل من العلاوة إلا بقرار من المجلس القومي للأجور لظروف اقتصادية، ويبت المجلس خلال 30 يومًا.",
                       "Only the National Wages Council can exempt an employer from the raise, for economic hardship, deciding within 30 days.")),
            ],
        },
        {
            "title": ("التأمينات الاجتماعية 2026", "Social insurance in 2026"),
            "sub": ("قانون التأمينات الاجتماعية والمعاشات 148 لسنة 2019", "Social Insurance and Pensions Law 148/2019"),
            "blocks": [
                ("kv", [
                    (("الأجر التأميني", "Insured wage"), ("من 2,700 إلى 16,700 جنيه شهريًا اعتبارًا من 1 يناير 2026", "EGP 2,700 to 16,700 a month from 1 January 2026")),
                    (("حصة صاحب العمل", "Employer share"), ("18.75% من الأجر التأميني", "18.75% of the insured wage")),
                    (("حصة الموظف", "Employee share"), ("11% من الأجر التأميني", "11% of the insured wage")),
                    (("صندوق الشهداء", "Martyrs Fund"), ("0.05% من إجمالي الراتب يُخصم من الموظف", "0.05% of gross pay, deducted from the employee")),
                ]),
                ("table", [("فرع التأمين", "Insurance branch"), ("صاحب العمل", "Employer"), ("الموظف", "Employee")], [
                    [("الشيخوخة والعجز والوفاة", "Old age, disability and death"), ("12%", "12%"), ("9%", "9%")],
                    [("نظام المكافأة", "Lump-sum benefit scheme"), ("1%", "1%"), ("1%", "1%")],
                    [("إصابات العمل", "Work injury"), ("1.5%", "1.5%"), ("—", "—")],
                    [("المرض", "Sickness"), ("3.25%", "3.25%"), ("1%", "1%")],
                    [("البطالة", "Unemployment"), ("1%", "1%"), ("—", "—")],
                    [("الإجمالي", "Total"), ("18.75%", "18.75%"), ("11%", "11%")],
                ]),
                ("p", ("إذا زاد الراتب على 16,700 جنيه تُحسب الاشتراكات على 16,700 فقط، وإذا قلّ عن 2,700 تُحسب على 2,700. وترتفع نسبة اشتراك الشيخوخة والعجز والوفاة 1% كل 7 سنوات مناصفة بين الطرفين، وأول زيادة في يناير 2027.",
                       "Above EGP 16,700 contributions are calculated on 16,700 only; below 2,700 they are calculated on 2,700. The old-age, disability and death rate rises by 1% every 7 years, split equally, with the first rise in January 2027.")),
                ("warn", ("سجّل كل موظف في الهيئة القومية للتأمين الاجتماعي من أول يوم عمل، وسدّد الاشتراكات شهريًا. وتسلّم نسخة من عقد العمل لمكتب التأمينات (م 89 من قانون العمل).",
                          "Register every employee with the National Organization for Social Insurance from day one and pay contributions monthly. A copy of the contract goes to the insurance office (Labour Law Art 89).")),
            ],
        },
        {
            "title": ("ضريبة كسب العمل 2026", "Payroll tax in 2026"),
            "sub": ("القانون 91 لسنة 2005 وتعديلاته بالقانون 7 لسنة 2024", "Law 91/2005 as amended by Law 7/2024"),
            "blocks": [
                ("p", ("تُحسب الضريبة سنويًا على صافي الدخل: الراتب الإجمالي ناقص حصة الموظف في التأمينات، ثم يُخصم الإعفاء الشخصي 20,000 جنيه، وتُطبّق الشرائح على الباقي.",
                       "Tax is worked out annually on net income: gross pay minus the employee's insurance share, then the EGP 20,000 personal exemption, with the brackets applied to the rest.")),
                ("table", [("الدخل السنوي الخاضع", "Annual taxable income"), ("السعر", "Rate")], [
                    [("حتى 40,000 جنيه", "Up to EGP 40,000"), ("0%", "0%")],
                    [("40,000 إلى 55,000", "40,000 to 55,000"), ("10%", "10%")],
                    [("55,000 إلى 70,000", "55,000 to 70,000"), ("15%", "15%")],
                    [("70,000 إلى 200,000", "70,000 to 200,000"), ("20%", "20%")],
                    [("200,000 إلى 400,000", "200,000 to 400,000"), ("22.5%", "22.5%")],
                    [("400,000 إلى 1,200,000", "400,000 to 1,200,000"), ("25%", "25%")],
                    [("أكثر من 1,200,000", "Above 1,200,000"), ("27.5%", "27.5%")],
                ]),
                ("ul", [
                    ("فوق 600,000 جنيه سنويًا تسقط الشرائح الأدنى تدريجيًا وفق جدول المادة 8.", "Above EGP 600,000 a year the lower brackets fall away gradually under the Article 8 schedule."),
                    ("أقساط التأمين على الحياة والتأمين الصحي الخاص للموظف وزوجه وأولاده القُصّر تُخصم من الوعاء حتى 10,000 جنيه سنويًا أو 15% من صافي الدخل، أيهما أقل (م 13).", "Life and private health insurance premiums for the employee, spouse and minor children are deductible up to EGP 10,000 a year or 15% of net income, whichever is lower (Art 13)."),
                    ("البدلات النقدية جزء من الدخل الخاضع للضريبة كالراتب.", "Cash allowances are taxable income, like salary."),
                ]),
            ],
        },
        {
            "title": ("أمثلة رواتب محسوبة وتكلفة صاحب العمل", "Worked payslips and employer cost"),
            "sub": ("ثلاثة مستويات رواتب شهرية", "Three monthly salary levels"),
            "blocks": [
                ("table", [("البند (جنيه شهريًا)", "Item (EGP a month)"), ("7,000", "7,000"), ("10,000", "10,000"), ("25,000", "25,000")], [
                    [("الأجر التأميني", "Insured wage"), ("7,000", "7,000"), ("10,000", "10,000"), ("16,700", "16,700")],
                    [("تأمينات الموظف 11%", "Employee insurance 11%"), ("770", "770"), ("1,100", "1,100"), ("1,837", "1,837")],
                    [("ضريبة كسب العمل", "Payroll tax"), ("123", "123"), ("592.50", "592.50"), ("3,565.84", "3,565.84")],
                    [("صندوق الشهداء 0.05%", "Martyrs Fund 0.05%"), ("3.50", "3.50"), ("5", "5"), ("12.50", "12.50")],
                    [("صافي الراتب", "Net pay"), ("6,103.50", "6,103.50"), ("8,302.50", "8,302.50"), ("19,584.66", "19,584.66")],
                    [("تأمينات صاحب العمل 18.75%", "Employer insurance 18.75%"), ("1,312.50", "1,312.50"), ("1,875", "1,875"), ("3,131.25", "3,131.25")],
                    [("التكلفة الشهرية على الشركة", "Monthly cost to the company"), ("8,312.50", "8,312.50"), ("11,875", "11,875"), ("28,131.25", "28,131.25")],
                ]),
                ("ex", ("راتب إجمالي 10,000 جنيه", "Gross salary EGP 10,000"), [
                    ("التأمينات: 10,000 × 11% = 1,100.", "Insurance: 10,000 × 11% = 1,100."),
                    ("الوعاء السنوي: (10,000 − 1,100) × 12 − 20,000 = 86,800.", "Annual base: (10,000 − 1,100) × 12 − 20,000 = 86,800."),
                    ("الضريبة: 15,000 × 10% + 15,000 × 15% + 16,800 × 20% = 7,110 سنويًا = 592.50 شهريًا.", "Tax: 15,000 × 10% + 15,000 × 15% + 16,800 × 20% = 7,110 a year = 592.50 a month."),
                    ("صندوق الشهداء: 5. الصافي: 10,000 − 1,100 − 592.50 − 5 = 8,302.50.", "Martyrs Fund: 5. Net: 10,000 − 1,100 − 592.50 − 5 = 8,302.50."),
                ], ("تكلفة الشركة: 10,000 + 1,875 = 11,875 جنيهًا", "Company cost: 10,000 + 1,875 = EGP 11,875")),
                ("tip", ("بعد 16,700 جنيه تتوقف اشتراكات التأمين عن الزيادة، فتنخفض نسبة التكلفة الإضافية كلما ارتفع الراتب. استخدم حاسبة الراتب على موقعنا لأي رقم آخر.",
                         "Above EGP 16,700 insurance stops rising, so the on-cost percentage falls as pay rises. Use the salary calculator on our site for any other figure.")),
            ],
        },
        {
            "title": ("الإجازات المدفوعة كميزة", "Paid leave as a benefit"),
            "sub": ("ما يفرضه قانون العمل 14 لسنة 2025", "What Labour Law 14/2025 requires"),
            "blocks": [
                ("table", [("الإجازة", "Leave"), ("المدة", "Entitlement")], [
                    [("سنوية", "Annual"), ("15 يومًا في السنة الأولى، 21 من الثانية، 30 بعد 10 سنوات أو سن 50، و45 لذوي الإعاقة (م 124)", "15 days in year one, 21 from year two, 30 after 10 years or age 50, 45 for employees with disabilities (Art 124)")],
                    [("عارضة", "Casual"), ("7 أيام، يومان في المرة، من رصيد السنوية (م 128)", "7 days, 2 at a time, from the annual balance (Art 128)")],
                    [("الأب عند الولادة", "Father at birth"), ("يوم بأجر، 3 مرات (م 128)", "1 paid day, 3 times (Art 128)")],
                    [("الوضع", "Maternity"), ("4 أشهر بأجر، 3 مرات (م 54)", "4 paid months, 3 times (Art 54)")],
                    [("رعاية طفل", "Childcare"), ("حتى سنتين بدون أجر، للمنشآت 50 عاملًا فأكثر (م 57)", "Up to 2 years unpaid, establishments of 50+ (Art 57)")],
                    [("الحج", "Hajj"), ("شهر بأجر مرة واحدة بعد 5 سنوات (م 130)", "1 paid month once, after 5 years (Art 130)")],
                    [("الامتحانات", "Exams"), ("أيام الامتحان الفعلية بأجر (م 126)", "Actual exam days, paid (Art 126)")],
                    [("مرضية", "Sick"), ("تعويض الأجر وفق قانون التأمينات (م 131)", "Pay replacement under the Social Insurance Law (Art 131)")],
                    [("العطلات الرسمية", "Public holidays"), ("بأجر، وتحددها قرارات وزارية كل عام (م 129)", "Paid, set each year by ministerial decision (Art 129)")],
                ]),
                ("p", ("العمل في عطلة رسمية يُدفع بأجر اليوم ومثليه، أو يوم بديل بطلب كتابي من الموظف (م 129).", "Work on a public holiday is paid at the day's wage plus twice that wage, or a substitute day at the employee's written request (Art 129).")),
            ],
        },
        {
            "title": ("مزايا قانونية أخرى", "Other statutory benefits"),
            "sub": ("الوفاة، وما بعد الستين، والأرباح، والتدريب", "Death, after 60, profit share and training"),
            "blocks": [
                ("table", [("الميزة", "Benefit"), ("القاعدة", "Rule")], [
                    [("نفقات الجنازة", "Funeral costs"), ("أجر شهرين بحد أدنى 1,000 جنيه، ومنحة أجر شهر الوفاة والشهرين التاليين (م 169)", "Two months' pay, min EGP 1,000, plus a grant of the month of death and the next two (Art 169)")],
                    [("مكافأة ما بعد الستين", "Post-60 award"), ("نصف شهر عن كل سنة من أول 5 سنوات وشهر عن كل سنة بعدها، إذا لم تكن له حقوق تأمينية عنها (م 172)", "Half a month per year for the first 5 years, a month per year after, if no insurance rights cover the period (Art 172)")],
                    [("إنهاء غير مشروع", "Unlawful termination"), ("تعويض لا يقل عن أجر شهرين عن كل سنة (م 165)", "At least two months' pay per year of service (Art 165)")],
                    [("حصة العاملين في الأرباح", "Employees' profit share"), ("في الشركات الخاضعة لقانون الشركات 159 لسنة 1981: لا تقل عن 10% من الأرباح الموزعة ولا تزيد على مجموع الأجور السنوية", "In companies under Companies Law 159/1981: at least 10% of distributed profit, capped at total annual wages")],
                    [("صندوق التدريب والتأهيل", "Training and qualification fund"), ("0.25% من الحد الأدنى للأجر التأميني عن كل عامل سنويًا، بين 10 و30 جنيهًا، للمنشآت 30 عاملًا فأكثر (م 21)", "0.25% of the minimum insured wage per worker per year, EGP 10 to 30, for establishments of 30+ (Art 21)")],
                ]),
            ],
        },
        {
            "title": ("المزايا الإضافية الشائعة في السوق", "Common supplementary benefits"),
            "sub": ("ليست إلزامية، لكنها تصنع الفرق في جذب الكفاءات", "Not required by law, but they win candidates"),
            "blocks": [
                ("table", [("الميزة", "Benefit"), ("لماذا تهم", "Why it matters"), ("ملاحظة ضريبية", "Tax note")], [
                    [("تأمين طبي خاص", "Private medical cover"), ("أكثر ميزة يسأل عنها المرشحون، خاصة لمن لديهم أسر", "The benefit candidates ask about most, especially with families"), ("أقساط التأمين الصحي للموظف وأسرته تُخصم من وعائه حتى الحد القانوني", "Premiums for the employee and family are deductible up to the legal cap")],
                    [("تأمين على الحياة", "Life insurance"), ("أمان لأسرة الموظف بتكلفة منخفضة للشركة", "Security for the family at low cost"), ("ضمن نفس حد الخصم", "Within the same deduction cap")],
                    [("مكافأة سنوية أو راتب شهر إضافي", "Annual bonus or extra month"), ("ربط الأجر بالأداء ونتائج الشركة", "Ties pay to performance and results"), ("خاضعة للضريبة", "Taxable")],
                    [("بدل مواصلات أو وجبات", "Transport or meal allowance"), ("يخفف عبء التنقل والأسعار", "Eases commuting and living costs"), ("خاضع للضريبة كجزء من الدخل", "Taxable as income")],
                    [("العمل المرن أو عن بُعد", "Flexible or remote work"), ("ميزة يقدّرها الموظفون ويعترف بها القانون الجديد (م 96)", "Valued by employees and recognised by the new law (Art 96)"), ("لا تكلفة ضريبية", "No tax cost")],
                    [("تدريب وشهادات مهنية", "Training and certifications"), ("يرفع المهارات ويقوّي الولاء", "Builds skills and loyalty"), ("التزام بالبقاء مدة متفق عليها جائز (م 95)", "A tie-in period is allowed (Art 95)")],
                    [("هاتف وإنترنت", "Phone and internet"), ("ضروري لفرق العمل عن بعد والمبيعات", "Essential for remote and sales teams"), ("حسب طبيعته كميزة أو أداة عمل", "Depends on whether it is a perk or a work tool")],
                ]),
                ("warn", ("إذا موّلت تدريب موظف واتفقتما على مدة بقاء، يلتزم بسداد نفقات التدريب إذا ترك العمل قبلها، ما لم ينص العقد على خلاف ذلك (م 95). اكتب هذا الشرط بوضوح.",
                          "If you fund an employee's training and agree a tie-in period, they repay the training cost if they leave early, unless the contract says otherwise (Art 95). Write the clause clearly.")),
            ],
        },
        {
            "title": ("الموظفون الأجانب", "Foreign employees"),
            "sub": ("نفس الحقوق، وشروط إضافية للتشغيل", "Same rights, extra conditions to employ"),
            "blocks": [
                ("ul", [
                    ("يتمتع الموظف الأجنبي بالحقوق نفسها في قانون العمل فيما لم يرد بشأنه نص خاص في عقده.", "A foreign employee has the same Labour Law rights wherever their contract is silent."),
                    ("لا يعمل إلا بترخيص عمل من الوزارة المختصة وإقامة بقصد العمل (م 71).", "They may only work with a Ministry work permit and residence for work (Art 71)."),
                    ("يحدد الوزير النسبة القصوى للأجانب في المنشأة والمهن المحظورة عليهم (م 70).", "The Minister sets the maximum share of foreign staff and the closed professions (Art 70)."),
                    ("مزايا شائعة: السكن أو بدل سكن، وتذاكر سفر سنوية، وتأمين طبي دولي، ودعم الانتقال.", "Common extras: housing or a housing allowance, annual flights, international medical cover, relocation support."),
                ]),
            ],
        },
        {
            "title": ("كيف تبني باقة مزايا في 5 خطوات", "How to build a benefits package in 5 steps"),
            "sub": ("طريقة عملية تناسب الشركات الصغيرة والمتوسطة", "A practical method for SMEs"),
            "blocks": [
                ("table", [("الخطوة", "Step"), ("ماذا تفعل", "What to do")], [
                    [("1. الميزانية والأهداف", "1. Budget and goals"), ("ابدأ بالتكلفة الإلزامية (التأمينات والعلاوة والإجازات) ثم حدّد ما يتبقى للمزايا الإضافية، وما الذي تريد تحقيقه: جذب، أو احتفاظ، أو أداء.", "Start from the statutory cost (insurance, raise, leave), then set what remains for extras and what you want: hiring, retention or performance.")],
                    [("2. السوق والموظفون", "2. Market and people"), ("قارن بما يقدّمه منافسوك في قطاعك، واسأل موظفيك في استبيان قصير عما يهمهم فعلًا.", "Compare with competitors in your sector, and ask your people in a short survey what they actually value.")],
                    [("3. باقة مرنة", "3. A flexible package"), ("ثبّت أساسيات للجميع (مثل التأمين الطبي)، واترك خيارات حسب المستوى أو الاحتياج.", "Fix a core for everyone (such as medical cover) and offer options by level or need.")],
                    [("4. التواصل", "4. Communicate"), ("اشرح الباقة كتابة، واذكر المزايا في العقود والعروض الوظيفية، واجمع الملاحظات.", "Explain the package in writing, list benefits in contracts and offers, and collect feedback.")],
                    [("5. المراجعة السنوية", "5. Review yearly"), ("راجع الاستخدام والتكلفة سنويًا، ومع كل تغيير في الحد الأدنى للأجر أو حدود التأمينات.", "Review use and cost every year, and whenever the minimum wage or insurance limits change.")],
                ]),
                ("check", [
                    ("كل الأجور 7,000 جنيه على الأقل.", "Every wage is at least EGP 7,000."),
                    ("العلاوة الدورية 3% مجدولة لكل موظف.", "The 3% periodic raise is scheduled for each employee."),
                    ("التأمينات محسوبة على الأجر التأميني الصحيح (2,700 إلى 16,700).", "Insurance is calculated on the right insured wage (2,700 to 16,700)."),
                    ("المزايا مكتوبة في العقد ومحددة كنقدية أو عينية.", "Benefits are written into contracts as cash or in kind."),
                    ("سياسة الإجازات مطابقة للقانون الجديد.", "The leave policy matches the new law."),
                    ("أقساط التأمين الطبي والحياة مخصومة من الوعاء الضريبي في حدودها.", "Medical and life premiums are deducted from the tax base within the cap."),
                ]),
            ],
        },
    ],
}
