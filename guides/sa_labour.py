"""Saudi Labour Law (Royal Decree M/51, as amended from 19 February 2025): employer guide.
Sources: HRSD official English text of the Labour Law; amended articles per Royal Decree M/44 and
Cabinet Decision 117 (Teamed article-by-article review, Roedl); GOSI; SPA announcements on Qiwa
documentation and engineering Saudization; HRSD on Mudad."""

GUIDE = {
    "kicker": ("دليل صاحب العمل", "Employer guide"),
    "title": ("نظام العمل السعودي بعد تعديلات 2025", "Saudi Labour Law after the 2025 amendments"),
    "sub": ("العقود والتجربة، وساعات العمل، والإجازات، والتأمينات، والإنهاء ومكافأة نهاية الخدمة، والتوطين، بأرقام المواد وأمثلة محسوبة.",
            "Contracts and probation, working hours, leave, GOSI, termination and end of service, and Saudization, with article numbers and worked examples."),
    "pills": [("تعديلات فبراير 2025", "February 2025 amendments"), ("قوى ومدد والتأمينات", "Qiwa, Mudad, GOSI"), ("مكافأة نهاية الخدمة", "End-of-service award"), ("التوطين 2026", "Saudization 2026")],
    "intro": ("نظام العمل الصادر بالمرسوم الملكي م/51، بعد تعديلات دخلت حيز التنفيذ في 19 فبراير 2025 بالمرسوم الملكي م/44 وقرار مجلس الوزراء 117: عُدّلت 38 مادة وأُلغيت 7 وأُضيفت مادتان. "
              "يجمع هذا الدليل ما يحتاجه صاحب العمل في القطاع الخاص، مع أرقام المواد، وأمثلة محسوبة، ومتطلبات المنصات الحكومية لعام 2026.",
              "The Labour Law issued by Royal Decree M/51, as amended from 19 February 2025 by Royal Decree M/44 and Cabinet Decision 117: 38 articles changed, 7 removed and 2 added. "
              "This guide brings together what a private-sector employer needs, with article numbers, worked examples and the 2026 government-platform requirements."),
    "cta_h": ("نتولى امتثالك لنظام العمل والمنصات الحكومية", "We keep you compliant with the Labour Law and the platforms"),
    "cta_p": ("موارد ومهارات تدير الموارد البشرية والرواتب وقوى ومدد والتأمينات والتوطين. احجز فحصًا مجانيًا مدته 30 دقيقة.",
              "Talent360 runs HR, payroll, Qiwa, Mudad, GOSI and Saudization for you. Book a free 30-minute check."),
    "note": ("الأحكام كما نُشرت حتى 2026.", "Rules as published up to 2026."),
    "sections": [
        {
            "title": ("نظرة عامة وأهم التعديلات", "Overview and key amendments"),
            "sub": ("ما تغيّر في 19 فبراير 2025", "What changed on 19 February 2025"),
            "blocks": [
                ("table", [("الموضوع", "Topic"), ("قبل التعديل", "Before"), ("بعد التعديل", "After")], [
                    [("فترة التجربة (م 53)", "Probation (Art 53)"), ("90 يومًا، تمدد كتابة إلى 180", "90 days, extendable in writing to 180"), ("حتى 180 يومًا إجمالًا، تُذكر صراحة في العقد", "Up to 180 days in total, stated in the contract")],
                    [("عقد غير السعودي (م 37)", "Non-Saudi contract (Art 37)"), ("مرتبط بمدة رخصة العمل", "Tied to the work permit"), ("سنة إذا لم تُحدد المدة، ويتجدد لمدة مماثلة", "One year if no term is stated, renewing for the same period")],
                    [("إشعار الموظف (م 75)", "Employee notice (Art 75)"), ("60 يومًا", "60 days"), ("30 يومًا (وصاحب العمل 60)", "30 days (employer still 60)")],
                    [("الاستقالة (م 79 مكرر)", "Resignation (Art 79 bis)"), ("لا تنظيم صريح", "Not expressly regulated"), ("رد خلال 30 يومًا، وتأجيل حتى 60 بمبرر، وعدول خلال 7 أيام", "Reply within 30 days, defer up to 60 with reason, withdraw within 7 days")],
                    [("إجازة الوضع (م 151)", "Maternity (Art 151)"), ("10 أسابيع", "10 weeks"), ("12 أسبوعًا، 6 منها إلزامية بعد الولادة", "12 weeks, 6 mandatory after birth")],
                    [("الإجازات الخاصة (م 113)", "Special leave (Art 113)"), ("دون وفاة الأخ أو الأخت", "No sibling bereavement"), ("الزواج 5، والوفاة 5، والأخ أو الأخت 3، والمولود 3", "Marriage 5, bereavement 5, sibling 3, new child 3")],
                    [("العمل الإضافي (م 107)", "Overtime (Art 107)"), ("أجر فقط", "Pay only"), ("أجر، أو إجازة مدفوعة بموافقة العامل", "Pay, or paid time off with consent")],
                    [("المساواة", "Equal treatment"), ("—", "—"), ("حظر التمييز بسبب الجنس أو العمر أو الجنسية أو الحالة الاجتماعية أو الإعاقة", "No discrimination by gender, age, nationality, marital status or disability")],
                ]),
                ("tip", ("لم تتغير مواد مكافأة نهاية الخدمة (84 إلى 88) في تعديلات 2025.", "The end-of-service articles (84 to 88) were not changed by the 2025 amendments.")),
            ],
        },
        {
            "title": ("العقود والتجربة وتوثيق قوى", "Contracts, probation and Qiwa"),
            "sub": ("المواد 9 و37 و53 و80", "Articles 9, 37, 53 and 80"),
            "blocks": [
                ("ul", [
                    ("العقد مكتوب من نسختين ووفق النموذج الموحد للوزارة، ويشمل الأجر والبدلات والمزايا ونوع العمل ومكانه وتاريخ البدء والمدة إن كان محددًا.", "A written contract in two copies on the Ministry's unified model, covering pay, allowances, benefits, the work, its place, the start date and any fixed term."),
                    ("العربية لغة العقد، وعند وجود لغة أخرى يُعمل بالنص العربي (م 9).", "Arabic is the contract language; where another language is used, the Arabic prevails (Art 9)."),
                    ("عقد غير السعودي مكتوب ومحدد المدة، وإذا لم تُذكر المدة فهو سنة من تاريخ المباشرة ويتجدد لمدة مماثلة (م 37).", "A non-Saudi's contract is written and fixed-term; with no term stated it runs one year from the start and renews for the same period (Art 37)."),
                    ("فترة التجربة حتى 180 يومًا إجمالًا وتُذكر صراحة في العقد (م 53)، ولأي طرف الإنهاء خلالها دون مكافأة أو إشعار أو تعويض (م 80).", "Probation up to 180 days in total, stated in the contract (Art 53); either side may end the contract during it with no award, notice or compensation (Art 80)."),
                ]),
                ("h", ("توثيق العقود في قوى 2026", "Qiwa contract documentation in 2026")),
                ("kv", [
                    (("نسبة الالتزام المطلوبة", "Required compliance rate"), ("85% من 30 أبريل 2026، ثم 90% من 30 يونيو 2026", "85% from 30 April 2026, then 90% from 30 June 2026")),
                    (("طريقة الحساب", "How it is measured"), ("العقود الموثقة إلى إجمالي عقود المنشأة", "Documented contracts over all the establishment's contracts")),
                    (("أثرها على نطاقات", "Effect on Nitaqat"), ("منذ 15 أبريل 2026 لا يُحتسب في التوطين إلا السعوديون ذوو العقود الموثقة", "Since 15 April 2026 only Saudis with documented contracts count")),
                    (("عدم الالتزام", "Falling short"), ("قد يقيّد خدمات الوزارة للمنشأة", "Can restrict the establishment's Ministry services")),
                ]),
                ("warn", ("الموظف السعودي غير الموثق عقده في قوى لا يُحسب في نسبة التوطين، حتى لو كان مسجلًا في التأمينات.", "A Saudi employee whose contract is not documented on Qiwa does not count towards Saudization, even if registered with GOSI.")),
            ],
        },
        {
            "title": ("ساعات العمل والعمل الإضافي", "Working hours and overtime"),
            "sub": ("المواد 98 و101 و104 و107", "Articles 98, 101, 104 and 107"),
            "blocks": [
                ("kv", [
                    (("الحد الأقصى", "Maximum"), ("9 ساعات يوميًا بالمعيار اليومي، أو 45 ساعة أسبوعيًا بالمعيار الأسبوعي (م 98)", "9 hours a day on a daily standard, or 45 a week on a weekly standard (Art 98)")),
                    (("رمضان", "Ramadan"), ("7 ساعات يوميًا أو 35 أسبوعيًا للمسلمين (م 98)", "7 hours a day or 35 a week for Muslim employees (Art 98)")),
                    (("الراحة", "Breaks"), ("لا يعمل أكثر من 5 ساعات متصلة دون راحة 30 دقيقة، ولا يبقى في مكان العمل أكثر من 12 ساعة (م 101)", "No more than 5 hours in a row without a 30-minute break, and no more than 12 hours on site (Art 101)")),
                    (("الراحة الأسبوعية", "Weekly rest"), ("يوما راحة في الأسبوع بأجر كامل أحدهما الجمعة، ويجوز استبدال الجمعة بإخطار مكتب العمل (م 104)", "Two fully paid rest days a week, one of them Friday, which may be swapped by notifying the labour office (Art 104)")),
                    (("أجر الساعة الإضافية", "Overtime hour"), ("أجر الساعة + 50% من الأجر الأساسي، أو إجازة مدفوعة بموافقة العامل (م 107)", "Hourly wage + 50% of the basic wage, or paid time off with consent (Art 107)")),
                ]),
                ("ex", ("أجر الساعة الإضافية", "An overtime hour"), [
                    ("أجر الساعة الفعلي للموظف: 50 ريالًا، وأجر الساعة الأساسي: 30 ريالًا.", "The employee's hourly wage: SAR 50; basic hourly wage: SAR 30."),
                    ("الساعة الإضافية: 50 + (30 × 50%) = 65 ريالًا.", "Overtime hour: 50 + (30 × 50%) = SAR 65."),
                    ("10 ساعات إضافية في الشهر: 10 × 65 = 650 ريالًا.", "10 overtime hours in a month: 10 × 65 = SAR 650."),
                ], ("المستحق: 650 ريالًا، أو إجازة مدفوعة باتفاق كتابي", "Due: SAR 650, or paid time off by written agreement")),
            ],
        },
        {
            "title": ("الإجازات", "Leave"),
            "sub": ("المواد 109 إلى 117 و151", "Articles 109 to 117 and 151"),
            "blocks": [
                ("table", [("الإجازة", "Leave"), ("المدة", "Entitlement"), ("ملاحظات", "Notes")], [
                    [("سنوية (م 109)", "Annual (Art 109)"), ("21 يومًا، و30 بعد 5 سنوات متصلة", "21 days; 30 after 5 continuous years"), ("لا تُستبدل نقدًا أثناء الخدمة، وإشعار بالموعد قبل 30 يومًا", "Not cashed in during employment; 30 days' notice of dates")],
                    [("الأعياد والمناسبات (م 112)", "Eids and occasions (Art 112)"), ("بأجر كامل", "Full pay"), ("حسب اللائحة التنفيذية", "As set by the regulations")],
                    [("الزواج (م 113)", "Marriage (Art 113)"), ("5 أيام بأجر", "5 paid days"), ("", "")],
                    [("وفاة الزوج أو أحد الأصول أو الفروع", "Death of spouse, parent or child"), ("5 أيام بأجر", "5 paid days"), ("", "")],
                    [("وفاة الأخ أو الأخت", "Death of a sibling"), ("3 أيام بأجر", "3 paid days"), ("جديدة في 2025", "New in 2025")],
                    [("مولود جديد", "Birth of a child"), ("3 أيام بأجر", "3 paid days"), ("تُؤخذ خلال 7 أيام من الولادة", "Taken within 7 days of the birth")],
                    [("الحج (م 114)", "Hajj (Art 114)"), ("10 إلى 15 يومًا بأجر شاملة عيد الأضحى", "10 to 15 paid days including Eid al-Adha"), ("مرة واحدة، بعد سنتين متصلتين", "Once, after 2 continuous years")],
                    [("الامتحانات (م 115)", "Exams (Art 115)"), ("أيام الامتحان الفعلية بأجر", "Actual exam days, paid"), ("بدون أجر إذا كان العام معادًا", "Unpaid for a repeat year")],
                    [("مرضية (م 117)", "Sick (Art 117)"), ("30 يومًا بأجر كامل، ثم 60 بثلاثة أرباع الأجر، ثم 30 بدون أجر", "30 days full pay, 60 at three quarters, then 30 unpaid"), ("في السنة الواحدة، متصلة أو متقطعة", "In one year, continuous or not")],
                    [("الوضع (م 151)", "Maternity (Art 151)"), ("12 أسبوعًا بأجر كامل", "12 weeks on full pay"), ("6 أسابيع إلزامية بعد الولادة، ويجوز البدء قبل 4 أسابيع من الموعد المتوقع", "6 weeks mandatory after birth; may start up to 4 weeks before the due date")],
                    [("بدون أجر (م 116)", "Unpaid (Art 116)"), ("باتفاق الطرفين", "By agreement"), ("يُعلّق العقد فيما زاد على 20 يومًا ما لم يُتفق على غير ذلك", "Contract suspended beyond 20 days unless agreed otherwise")],
                ]),
                ("p", ("إذا انتهت الخدمة قبل استخدام الإجازة، يستحق الموظف أجر الأيام المتراكمة، وأجر الإجازة عن جزء السنة الذي عمله (م 111).", "If employment ends before leave is used, the employee is paid for the accrued days and for leave on the part-year worked (Art 111).")),
            ],
        },
        {
            "title": ("الأجور وحماية الأجور والتأمينات", "Pay, wage protection and GOSI"),
            "sub": ("المواد 90 و94، ومدد، ونظام التأمينات", "Articles 90 and 94, Mudad, and GOSI"),
            "blocks": [
                ("ul", [
                    ("الأجر الشهري يُدفع مرة في الشهر، ويُودع في حساب الموظف في بنك معتمد داخل المملكة (م 90).", "Monthly pay is paid once a month into the employee's account at an approved bank in the Kingdom (Art 90)."),
                    ("ملف الأجور يُرفع شهريًا على منصة مدد، ومنذ 1 مارس 2025 لا يغطي إلا الشهر السابق (30 يومًا بدل 60).", "The wage file goes up monthly on Mudad; since 1 March 2025 it may only cover the previous month (30 days, down from 60)."),
                    ("الخصم أو التأخير دون مبرر قد يُلزم صاحب العمل بغرامة حتى ضعف المبلغ (م 94).", "Unjustified deductions or delays can bring a fine of up to twice the amount (Art 94)."),
                ]),
                ("table", [("الفئة", "Group"), ("صاحب العمل", "Employer"), ("الموظف", "Employee")], [
                    [("سعودي مسجل قبل 3 يوليو 2024: المعاشات", "Saudi insured before 3 July 2024: pension"), ("9%", "9%"), ("9%", "9%")],
                    [("ساند (التعطل عن العمل)", "SANED (unemployment)"), ("0.75%", "0.75%"), ("0.75%", "0.75%")],
                    [("الأخطار المهنية", "Occupational hazards"), ("2%", "2%"), ("—", "—")],
                    [("سعودي مسجل من 3 يوليو 2024: المعاشات", "Saudi insured from 3 July 2024: pension"), ("يبدأ 9% ويرتفع 0.5 نقطة سنويًا من يوليو 2025 حتى 11%", "Starts at 9%, rising 0.5 points a year from July 2025 to 11%"), ("مثل صاحب العمل", "Same as employer")],
                    [("غير السعودي", "Non-Saudi"), ("2% أخطار مهنية فقط", "2% occupational hazards only"), ("لا شيء", "None")],
                ]),
                ("p", ("الأجر الخاضع للاشتراك هو الأجر الأساسي وبدل السكن، بحد أعلى 45,000 ريال شهريًا.", "The contributory wage is basic pay plus housing allowance, capped at SAR 45,000 a month.")),
            ],
        },
        {
            "title": ("الإنهاء والاستقالة", "Termination and resignation"),
            "sub": ("المواد 64 و75 إلى 81", "Articles 64 and 75 to 81"),
            "blocks": [
                ("table", [("الحالة", "Situation"), ("القاعدة", "Rule")], [
                    [("إشعار العقد غير محدد المدة (م 75)", "Notice, indefinite contract (Art 75)"), ("أجر شهري: 60 يومًا من صاحب العمل و30 من الموظف. غير شهري: 30 يومًا من أي طرف. ولسبب مشروع.", "Monthly pay: 60 days from the employer, 30 from the employee. Otherwise 30 days either way. For a legitimate reason.")],
                    [("عدم مراعاة الإشعار (م 76)", "Notice not observed (Art 76)"), ("يدفع الطرف المخالف أجر مدة الإشعار", "The party at fault pays wages for the notice period")],
                    [("الإنهاء لسبب غير مشروع (م 77)", "Termination for an invalid reason (Art 77)"), ("ما لم يحدده العقد: أجر 15 يومًا عن كل سنة في غير محدد المدة، وباقي المدة في محدد المدة، وبحد أدنى أجر شهرين", "Unless the contract sets it: 15 days' wage per year (indefinite) or the rest of the term (fixed), minimum two months' wage")],
                    [("الاستقالة (م 79 مكرر)", "Resignation (Art 79 bis)"), ("تُعتبر مقبولة إذا لم يرد صاحب العمل خلال 30 يومًا، وله تأجيلها حتى 60 يومًا بمبرر مكتوب، وللموظف العدول خلال 7 أيام ما لم تُقبل", "Deemed accepted if no reply within 30 days; the employer may defer up to 60 days with a written reason; the employee may withdraw within 7 days unless accepted")],
                    [("الفصل دون مكافأة (م 80)", "Dismissal without award (Art 80)"), ("في حالات محددة كالاعتداء، أو الإخلال الجوهري بالالتزامات، أو سوء السلوك، بعد إعطاء الموظف فرصة لإبداء أسباب اعتراضه", "Only in listed cases such as assault, serious breach of duties or misconduct, after giving the employee a chance to object")],
                    [("ترك العمل دون إشعار (م 81)", "Leaving without notice (Art 81)"), ("للموظف ذلك إذا أخل صاحب العمل بالتزاماته الجوهرية، أو غشّه، أو أساء معاملته، أو عرّضه لخطر جسيم", "Allowed if the employer breaches essential duties, misleads, mistreats or exposes the employee to serious danger")],
                    [("شهادة الخبرة (م 64)", "Experience certificate (Art 64)"), ("مجانًا عند الطلب، دون أي ملاحظة تسيء للموظف، مع إعادة شهاداته ووثائقه", "Free on request, with no remark that harms the employee, plus return of their documents")],
                ]),
                ("ex", ("إنهاء عقد غير محدد المدة لسبب غير مشروع", "Ending an indefinite contract for an invalid reason"), [
                    ("موظف أمضى 6 سنوات، وأجره الشهري 9,000 ريال (أجر اليوم 300).", "An employee with 6 years' service on SAR 9,000 a month (SAR 300 a day)."),
                    ("التعويض: 15 يومًا × 6 سنوات × 300 = 27,000 ريال (أكثر من الحد الأدنى: شهران = 18,000).", "Compensation: 15 days × 6 years × 300 = SAR 27,000 (above the two-month minimum of 18,000)."),
                    ("إضافة لمكافأة نهاية الخدمة وأجر الإشعار إن لم يُراعَ.", "On top of the end-of-service award, and notice pay if notice was not given."),
                ], ("التعويض: 27,000 ريال", "Compensation: SAR 27,000")),
            ],
        },
        {
            "title": ("مكافأة نهاية الخدمة", "End-of-service award"),
            "sub": ("المواد 84 إلى 88", "Articles 84 to 88"),
            "blocks": [
                ("kv", [
                    (("الحساب (م 84)", "Formula (Art 84)"), ("نصف شهر عن كل سنة من السنوات الخمس الأولى، وشهر عن كل سنة بعدها، على آخر أجر، وأجزاء السنة بنسبتها", "Half a month per year for the first five years, a month per year after, on the last wage, with part-years pro rata")),
                    (("الاستقالة (م 85)", "Resignation (Art 85)"), ("أقل من سنتين: لا شيء. من 2 إلى 5: الثلث. أكثر من 5 وأقل من 10: الثلثان. 10 فأكثر: كاملة", "Under 2 years: nothing. 2 to 5: one third. Over 5 and under 10: two thirds. 10 or more: full")),
                    (("استثناءات (م 87)", "Exceptions (Art 87)"), ("كاملة عند القوة القاهرة، وللموظفة خلال 6 أشهر من الزواج أو 3 أشهر من الولادة", "Full award for force majeure, and for a woman leaving within 6 months of marriage or 3 months of giving birth")),
                    (("موعد الصرف (م 88)", "Payment (Art 88)"), ("خلال أسبوع من انتهاء العلاقة، أو أسبوعين إذا أنهاها الموظف", "Within a week of the end, or two weeks if the employee ended it")),
                ]),
                ("table", [("مدة الخدمة", "Service"), ("إنهاء من صاحب العمل أو انتهاء المدة", "Employer ends it / term expires"), ("استقالة", "Resignation")], [
                    [("سنة واحدة", "1 year"), ("0.5 شهر", "0.5 month"), ("لا شيء", "Nothing")],
                    [("3 سنوات", "3 years"), ("1.5 شهر", "1.5 months"), ("0.5 شهر", "0.5 month")],
                    [("5 سنوات", "5 years"), ("2.5 شهر", "2.5 months"), ("0.83 شهر", "0.83 month")],
                    [("8 سنوات", "8 years"), ("5.5 أشهر", "5.5 months"), ("3.67 أشهر", "3.67 months")],
                    [("10 سنوات", "10 years"), ("7.5 أشهر", "7.5 months"), ("7.5 أشهر", "7.5 months")],
                ]),
                ("ex", ("8 سنوات خدمة بأجر 10,000 ريال", "8 years' service on SAR 10,000"), [
                    ("السنوات الخمس الأولى: 5 × 0.5 = 2.5 شهر.", "First five years: 5 × 0.5 = 2.5 months."),
                    ("السنوات الثلاث التالية: 3 × 1 = 3 أشهر. المجموع 5.5 أشهر = 55,000 ريال.", "Next three years: 3 × 1 = 3 months. Total 5.5 months = SAR 55,000."),
                    ("عند الاستقالة (أكثر من 5 وأقل من 10): الثلثان = 36,667 ريالًا تقريبًا.", "On resignation (over 5, under 10): two thirds = about SAR 36,667."),
                ], ("55,000 ريال، أو 36,667 عند الاستقالة", "SAR 55,000, or about 36,667 on resignation")),
            ],
        },
        {
            "title": ("التوطين ونطاقات 2026", "Saudization and Nitaqat in 2026"),
            "sub": ("النطاقات، ونسب المهن، والقرارات الجديدة", "Bands, profession quotas and new decisions"),
            "blocks": [
                ("p", ("يصنّف برنامج نطاقات المطور المنشآت في خمسة نطاقات: البلاتيني، والأخضر المرتفع، والأخضر المتوسط، والأخضر المنخفض، والأحمر، حسب نسبة التوطين مقارنة بنشاطها وحجمها. وتفقد المنشآت في الأخضر المنخفض والأحمر الوصول لتأشيرات جديدة وخدمات أخرى.",
                       "Nitaqat Mutawar places each establishment in one of five bands: Platinum, High Green, Medium Green, Low Green and Red, by its Saudization rate against its activity and size. Low Green and Red establishments lose access to new visas and other services.")),
                ("table", [("القرار", "Decision"), ("النسبة", "Rate"), ("منذ", "From")], [
                    [("توطين 46 مهنة هندسية للمنشآت التي لديها 5 مهندسين فأكثر، مع اعتماد الهيئة السعودية للمهندسين", "46 engineering professions, establishments with 5+ engineers, with Saudi Council of Engineers accreditation"), ("30%", "30%"), ("30 يونيو 2026", "30 June 2026")],
                    [("69 مهنة دعم إداري", "69 administrative support professions"), ("100% للسعوديين", "100% Saudi"), ("دخل حيز التنفيذ 4 أكتوبر 2026 مع بدء التفتيش", "In force 4 October 2026, with inspections")],
                    [("احتساب التوطين", "Saudization count"), ("السعوديون ذوو العقود الموثقة في قوى فقط", "Only Saudis with Qiwa-documented contracts"), ("15 أبريل 2026", "15 April 2026")],
                ]),
                ("warn", ("مخالفة نظام العمل عمومًا، وليس التوطين فقط، قد تمنع تجديد أو إصدار رخص العمل لغير السعوديين بعد تعديلات 2025.",
                          "Since the 2025 amendments, breaching the Labour Law generally, not only Saudization quotas, can block new or renewed work permits for non-Saudis.")),
            ],
        },
        {
            "title": ("قائمة التحقق والتقويم", "Checklist and calendar"),
            "sub": ("ما تراجعه الآن، ومتى", "What to review now, and when"),
            "blocks": [
                ("check", [
                    ("نماذج العقود: مدة التجربة صريحة (حتى 180 يومًا)، ومدة عقد غير السعودي، ومهل الإشعار الجديدة.", "Contract templates: explicit probation (up to 180 days), non-Saudi term, new notice periods."),
                    ("كل العقود موثقة في قوى، والنسبة 90% أو أكثر.", "Every contract documented on Qiwa, rate at 90% or above."),
                    ("سياسة الإجازات: الوضع 12 أسبوعًا، والمولود 3 أيام، ووفاة الأخ أو الأخت 3 أيام، والزواج والوفاة 5 أيام.", "Leave policy: maternity 12 weeks, birth 3 days, sibling bereavement 3 days, marriage and bereavement 5 days."),
                    ("إجراء الاستقالة: رد خلال 30 يومًا، والتأجيل حتى 60 بمبرر مكتوب.", "Resignation process: reply within 30 days, defer up to 60 with a written reason."),
                    ("ملف مدد يُرفع شهريًا ويغطي الشهر السابق فقط.", "Mudad file uploaded monthly, covering only the previous month."),
                    ("اشتراكات التأمينات بالنسب الصحيحة لكل فئة، والسقف 45,000 ريال.", "GOSI at the right rate for each group, capped at SAR 45,000."),
                    ("حساب مكافأة نهاية الخدمة والعمل الإضافي مطابق للمواد 84 و85 و107.", "End-of-service and overtime calculations match Arts 84, 85 and 107."),
                    ("نسب التوطين في المهن المستهدفة (الهندسة، الدعم الإداري).", "Saudization in targeted professions (engineering, administrative support)."),
                ]),
                ("table", [("الموعد", "When"), ("ما يجب فعله", "What to do")], [
                    [("شهريًا", "Monthly"), ("صرف الأجور، ورفع ملف مدد، وسداد اشتراكات التأمينات", "Pay wages, upload the Mudad file, pay GOSI")],
                    [("عند كل تعيين", "Every hire"), ("توثيق العقد في قوى وتسجيل الموظف في التأمينات", "Document the contract on Qiwa and register with GOSI")],
                    [("قبل الإجازة السنوية بـ 30 يومًا", "30 days before annual leave"), ("إشعار الموظف بموعد إجازته", "Notify the employee of their leave dates")],
                    [("يوليو من كل عام", "Every July"), ("رفع نسبة المعاش 0.5 نقطة للمسجلين الجدد حتى 11%", "Raise the pension rate 0.5 points for new-system members, up to 11%")],
                    [("خلال أسبوع أو أسبوعين من الانتهاء", "1 or 2 weeks after exit"), ("صرف المستحقات ومكافأة نهاية الخدمة (م 88)", "Pay final dues and the end-of-service award (Art 88)")],
                ]),
            ],
        },
    ],
}
