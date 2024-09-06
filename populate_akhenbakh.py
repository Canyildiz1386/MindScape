from app import db, AkhenbachQuestion

questions = [
    # اضطراب/افسردگی (Anxiety/Depression)
    {"category": "اضطراب/افسردگی", "question_text": "زیاد گریه می کند"},
    {"category": "اضطراب/افسردگی", "question_text": "از حیوانات می ترسد"},
    {"category": "اضطراب/افسردگی", "question_text": "از مدرسه می ترسد"},
    {"category": "اضطراب/افسردگی", "question_text": "از فکر یا کار بد می ترسد"},
    {"category": "اضطراب/افسردگی", "question_text": "احساس می کند باید بی نقص و کامل باشد"},
    {"category": "اضطراب/افسردگی", "question_text": "احساس طرد شدن می کند"},
    {"category": "اضطراب/افسردگی", "question_text": "احساس بی ارزشی می کند"},
    {"category": "اضطراب/افسردگی", "question_text": "زیاد عصبی و پرتنش است"},
    {"category": "اضطراب/افسردگی", "question_text": "خیلی ترسو و مضطرب است"},
    {"category": "اضطراب/افسردگی", "question_text": "احساس گناه زیاد دارد"},
    {"category": "اضطراب/افسردگی", "question_text": "کمرو و خجالتی است"},
    {"category": "اضطراب/افسردگی", "question_text": "به خودکشی فکر می کند"},
    {"category": "اضطراب/افسردگی", "question_text": "نگران است"},

    # گوشه گیری/افسردگی (Withdrawal/Depression)
    {"category": "گوشه گیری/افسردگی", "question_text": "لذت کمی از چیزها می برد"},
    {"category": "گوشه گیری/افسردگی", "question_text": "تنهایی را ترجیح می دهد"},
    {"category": "گوشه گیری/افسردگی", "question_text": "امتناع از صحبت می کند"},
    {"category": "گوشه گیری/افسردگی", "question_text": "تودار و مرموز است"},
    {"category": "گوشه گیری/افسردگی", "question_text": "خیلی خجالتی یا ترسو است"},
    {"category": "گوشه گیری/افسردگی", "question_text": "کم حرکتی یا فقدان انرژی دارد"},
    {"category": "گوشه گیری/افسردگی", "question_text": "ناراحت یا غمگین است"},
    {"category": "گوشه گیری/افسردگی", "question_text": "گوشه گیر است"},

    # شکایات جسمانی (Somatic Complaints)
    {"category": "شکایات جسمانی", "question_text": "کابوس می بیند"},
    {"category": "شکایات جسمانی", "question_text": "یبوست دارد"},
    {"category": "شکایات جسمانی", "question_text": "احساس گیجی و منگی دارد"},
    {"category": "شکایات جسمانی", "question_text": "احساس خستگی شدید دارد"},
    {"category": "شکایات جسمانی", "question_text": "از دردهای جسمانی شکایت دارد"},

    # مشکلات اجتماعی (Social Problems)
    {"category": "مشکلات اجتماعی", "question_text": "وابستگی زیاد به دیگران دارد"},
    {"category": "مشکلات اجتماعی", "question_text": "شکایت از تنهایی می کند"},
    {"category": "مشکلات اجتماعی", "question_text": "با دیگران کنار نمی آید"},
    {"category": "مشکلات اجتماعی", "question_text": "حسادت می کند"},
    {"category": "مشکلات اجتماعی", "question_text": "احساس می کند دیگران دنبال او هستند"},
    {"category": "مشکلات اجتماعی", "question_text": "زیاد صدمه می بیند"},
    {"category": "مشکلات اجتماعی", "question_text": "مورد تمسخر دیگران قرار می گیرد"},
    {"category": "مشکلات اجتماعی", "question_text": "بچه های دیگر از او خوششان نمی آید"},
    {"category": "مشکلات اجتماعی", "question_text": "دست و پا چلفتی است"},
    {"category": "مشکلات اجتماعی", "question_text": "میل به بودن با بچه های کوچکتر دارد"},
    {"category": "مشکلات اجتماعی", "question_text": "مشکلات گفتاری دارد"},

    # مشکلات تفکر (Thought Problems)
    {"category": "مشکلات تفکر", "question_text": "نمی تواند از افکار خاصی اجتناب کند"},
    {"category": "مشکلات تفکر", "question_text": "به خود آسیب می زند"},
    {"category": "مشکلات تفکر", "question_text": "صداهایی می شنود که وجود ندارند"},
    {"category": "مشکلات تفکر", "question_text": "حرکات عصبی و انقباض عضلات دارد"},
    {"category": "مشکلات تفکر", "question_text": "پوست و بدن خود را فشار می دهد"},
    {"category": "مشکلات تفکر", "question_text": "در حضور دیگران با آلت تناسلی خود بازی می کند"},
    {"category": "مشکلات تفکر", "question_text": "بازی کردن زیاد با آلت تناسلی دارد"},
    {"category": "مشکلات تفکر", "question_text": "اعمال خاصی را بارها و بارها تکرار می کند"},
    {"category": "مشکلات تفکر", "question_text": "چیزهایی می بیند که وجود ندارند"},
    {"category": "مشکلات تفکر", "question_text": "کم خوابی دارد"},
    {"category": "مشکلات تفکر", "question_text": "چیزهایی را انبار می کند"},
    {"category": "مشکلات تفکر", "question_text": "رفتار عجیب و غریب دارد"},
    {"category": "مشکلات تفکر", "question_text": "افکار عجیب و غریب دارد"},
    {"category": "مشکلات تفکر", "question_text": "در خواب راه می رود یا صحبت می کند"},
    {"category": "مشکلات تفکر", "question_text": "مشکل در خوابیدن دارد"},

    # مشکلات توجه (Attention Problems)
    {"category": "مشکلات توجه", "question_text": "کوچکتر از سن خود عمل می کند"},
    {"category": "مشکلات توجه", "question_text": "کارهای خود را تمام نمی کند"},
    {"category": "مشکلات توجه", "question_text": "مشکل در تمرکز طولانی مدت دارد"},
    {"category": "مشکلات توجه", "question_text": "بی قرار و بیش فعال است"},
    {"category": "مشکلات توجه", "question_text": "گیج و سردرگم به نظر می رسد"},
    {"category": "مشکلات توجه", "question_text": "خیالبافی می کند"},
    {"category": "مشکلات توجه", "question_text": "تکانشی عمل می کند"},
    {"category": "مشکلات توجه", "question_text": "در انجام تکالیف درسی ضعف دارد"},
    {"category": "مشکلات توجه", "question_text": "بی توجه یا حواس پرت است"},
    {"category": "مشکلات توجه", "question_text": "مات و مبهوت به جایی خیره می شود"},

    # رفتار قانون شکنی (Rule-breaking Behavior)
    {"category": "رفتار قانون شکنی", "question_text": "مصرف مشروبات الکلی دارد"},
    {"category": "رفتار قانون شکنی", "question_text": "احساس گناه نمی کند"},
    {"category": "رفتار قانون شکنی", "question_text": "مقررات را زیر پا می گذارد"},
    {"category": "رفتار قانون شکنی", "question_text": "با دوستان بد می گردد"},
    {"category": "رفتار قانون شکنی", "question_text": "دروغ می گوید یا تقلب می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "میل به بودن با بچه های بزرگتر دارد"},
    {"category": "رفتار قانون شکنی", "question_text": "از خانه فرار می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "آتش روشن می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "مشکلات جنسی دارد"},
    {"category": "رفتار قانون شکنی", "question_text": "در خانه دزدی می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "خارج از خانه دزدی می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "دشنام می دهد"},
    {"category": "رفتار قانون شکنی", "question_text": "زیاد به مسائل جنسی فکر می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "سیگار یا قلیان می کشد"},
    {"category": "رفتار قانون شکنی", "question_text": "از مدرسه فرار می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "مواد مخدر مصرف می کند"},
    {"category": "رفتار قانون شکنی", "question_text": "اموال عمومی را تخریب می کند"},

    # رفتار پرخاشگرانه (Aggressive Behavior)
    {"category": "رفتار پرخاشگرانه", "question_text": "زیاد جر و بحث می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "با دیگران بی رحمانه رفتار می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "توجه طلبی می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "اموال شخصی خود را خراب می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "اموال دیگران را خراب می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "در خانه نافرمانی می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "در مدرسه نافرمانی می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "زیاد جنگ و دعوا می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "به دیگران حمله می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "زیاد جیغ و داد می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "لجباز است"},
    {"category": "رفتار پرخاشگرانه", "question_text": "خلقش به سرعت تغییر می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "اخمو است"},
    {"category": "رفتار پرخاشگرانه", "question_text": "بدگمان است"},
    {"category": "رفتار پرخاشگرانه", "question_text": "دیگران را اذیت می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "قشقرق راه می اندازد"},
    {"category": "رفتار پرخاشگرانه", "question_text": "دیگران را تهدید می کند"},
    {"category": "رفتار پرخاشگرانه", "question_text": "بیش از حد پر سر و صدا است"},

    # سایر مشکلات (Other Problems)
    {"category": "سایر مشکلات", "question_text": "حساسیت (آلرژی) دارد"},
    {"category": "سایر مشکلات", "question_text": "بیرون از توالت مدفوع می کند"},
    {"category": "سایر مشکلات", "question_text": "از چیزی لذت نمی برد"},
    {"category": "سایر مشکلات", "question_text": "آب دهان را در هر مکانی می اندازد (تف می کند)"},
    {"category": "سایر مشکلات", "question_text": "مغرور است و از خودش تعریف می کند"},
    {"category": "سایر مشکلات", "question_text": "زیاد غذا می خورد (پرخور است)"},
    {"category": "سایر مشکلات", "question_text": "اضافه وزن دارد"},
    {"category": "سایر مشکلات", "question_text": "خودنمایی یا دلقک بازی می کند"},
    {"category": "سایر مشکلات", "question_text": "خیلی کم می خوابد"},
    {"category": "سایر مشکلات", "question_text": "خیلی زیاد می خوابد"},
    {"category": "سایر مشکلات", "question_text": "زیاد صحبت می کند"},
    {"category": "سایر مشکلات", "question_text": "انگشت شست خود را می مکد"},
    {"category": "سایر مشکلات", "question_text": "خودش را در طول روز خیس می کند"},
    {"category": "سایر مشکلات", "question_text": "شب ادراری دارد"},
    {"category": "سایر مشکلات", "question_text": "زیاد غر می زند"},
    {"category": "سایر مشکلات", "question_text": "آرزو می کند جنسیت دیگری داشت"},

]

def populate_akhenbach_questions():
    for question in questions:
        q = AkhenbachQuestion(
            category=question["category"],
            question_text=question["question_text"],
            score_no=0,
            score_sometimes=1,
            score_yes=2,
        )
        db.session.add(q)
    db.session.commit()

from app import db, CattellQuestion

questions = [
    # Factor A (Warmth) - 10 Questions
    {"category": "A - گرمی", "question_text": "آیا احساس می‌کنید به دیگران کمک کردن برایتان لذت‌بخش است؟"},
    {"category": "A - گرمی", "question_text": "آیا به راحتی با دیگران دوست می‌شوید؟"},
    {"category": "A - گرمی", "question_text": "آیا شما به آسانی با دیگران ارتباط برقرار می‌کنید؟"},
    {"category": "A - گرمی", "question_text": "آیا از وقت گذراندن با دیگران لذت می‌برید؟"},
    {"category": "A - گرمی", "question_text": "آیا اغلب وقت خود را با دوستان و خانواده می‌گذرانید؟"},
    {"category": "A - گرمی", "question_text": "آیا شما فردی اجتماعی هستید؟"},
    {"category": "A - گرمی", "question_text": "آیا ارتباطات اجتماعی برای شما اهمیت دارد؟"},
    {"category": "A - گرمی", "question_text": "آیا شما به راحتی با افراد جدید ارتباط برقرار می‌کنید؟"},
    {"category": "A - گرمی", "question_text": "آیا به روابط انسانی اهمیت می‌دهید؟"},
    {"category": "A - گرمی", "question_text": "آیا اغلب از تعامل با افراد لذت می‌برید؟"},

    # Factor B (Reasoning) - 13 Questions
    {"category": "B - استدلال", "question_text": "آیا به حل مسائل پیچیده علاقه دارید؟"},
    {"category": "B - استدلال", "question_text": "آیا از تفکر انتقادی لذت می‌برید؟"},
    {"category": "B - استدلال", "question_text": "آیا معمولاً به تحلیل مسائل از جنبه‌های مختلف فکر می‌کنید؟"},
    {"category": "B - استدلال", "question_text": "آیا در حل معماها و چالش‌ها مهارت دارید؟"},
    {"category": "B - استدلال", "question_text": "آیا به مباحث علمی و فلسفی علاقه‌مند هستید؟"},
    {"category": "B - استدلال", "question_text": "آیا اغلب دوست دارید مسائل را منطقی بررسی کنید؟"},
    {"category": "B - استدلال", "question_text": "آیا از مباحثه‌های منطقی و استدلالی لذت می‌برید؟"},
    {"category": "B - استدلال", "question_text": "آیا توانایی تمرکز بالا در حل مسائل دارید؟"},
    {"category": "B - استدلال", "question_text": "آیا به دنبال یافتن دلایل و شواهد منطقی هستید؟"},
    {"category": "B - استدلال", "question_text": "آیا از تفکر در مورد مسائل انتزاعی لذت می‌برید؟"},
    {"category": "B - استدلال", "question_text": "آیا به دنبال پیدا کردن راه حل‌های جدید برای مسائل هستید؟"},
    {"category": "B - استدلال", "question_text": "آیا تصمیمات خود را بر اساس استدلال‌های منطقی می‌گیرید؟"},
    {"category": "B - استدلال", "question_text": "آیا به کارهای فکری و تحلیلی علاقه‌مند هستید؟"},

    # Factor C (Emotional Stability) - 13 Questions
    {"category": "C - پایداری هیجانی", "question_text": "آیا به راحتی احساسات خود را کنترل می‌کنید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در مواجهه با مشکلات آرامش خود را حفظ می‌کنید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا احساسات خود را به خوبی مدیریت می‌کنید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا به ندرت اجازه می‌دهید احساسات شما بر تصمیمات شما تأثیر بگذارد؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در شرایط بحرانی آرام می‌مانید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در شرایط استرس‌زا کنترل خود را حفظ می‌کنید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا شما فردی متعادل و منطقی هستید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در مواقعی که تحت فشار هستید به راحتی واکنش نشان نمی‌دهید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در مواجهه با استرس به خوبی عمل می‌کنید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در برابر احساسات شدید مقاوم هستید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا شما فردی پایدار و ثابت‌قدم هستید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا در مواجهه با چالش‌ها به راحتی تحت تأثیر قرار نمی‌گیرید؟"},
    {"category": "C - پایداری هیجانی", "question_text": "آیا شما فردی خونسرد هستید؟"},

    # Factor E (Dominance) - 13 Questions
    {"category": "E - سلطه‌گری", "question_text": "آیا دوست دارید در یک گروه تصمیم‌گیرنده باشید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا تمایل به رهبری دارید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا در گروه‌ها نظرات خود را به راحتی بیان می‌کنید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا دوست دارید دیگران را راهنمایی کنید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا احساس می‌کنید که باید همیشه کنترل را در دست داشته باشید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا از تصمیم‌گیری برای دیگران لذت می‌برید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا تمایل دارید همیشه رهبری را بر عهده بگیرید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا دوست دارید در تصمیم‌گیری‌ها نفوذ داشته باشید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا شما فردی قاطع و مقتدر هستید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا در موقعیت‌های اجتماعی به راحتی رهبری را در دست می‌گیرید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا از اینکه دیگران شما را به عنوان رهبر انتخاب کنند لذت می‌برید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا شما فردی هستید که دوست دارید بر دیگران تأثیر بگذارید؟"},
    {"category": "E - سلطه‌گری", "question_text": "آیا شما اغلب به عنوان رهبر گروه انتخاب می‌شوید؟"},

    # Factor F (Liveliness) - 13 Questions
    {"category": "F - سرزندگی", "question_text": "آیا در جمع‌ها پرانرژی و شاد هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا از فعالیت‌های گروهی لذت می‌برید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما فردی فعال و پرتحرک هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما همیشه آماده انجام کارهای هیجان‌انگیز هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا به راحتی با افراد جدید ارتباط برقرار می‌کنید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما فردی شاداب و پرانرژی هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا از بودن در جمع‌های شاد و پرجنب‌وجوش لذت می‌برید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا اغلب در جمع‌ها فعال و پرجنب‌وجوش هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما فردی اجتماعی و پرشور هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما همیشه برای فعالیت‌های گروهی آماده هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا از انجام کارهای پرانرژی و هیجان‌انگیز لذت می‌برید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما فردی سرزنده و پرهیجان هستید؟"},
    {"category": "F - سرزندگی", "question_text": "آیا شما اغلب در موقعیت‌های اجتماعی پرجنب و جوش عمل می‌کنید؟"},

    # Factor G (Rule-Consciousness) - 10 Questions
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا به قوانین و مقررات پایبند هستید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا همیشه سعی می‌کنید وظایف خود را به بهترین شکل انجام دهید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا به اصول اخلاقی اهمیت می‌دهید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا به دنبال نظم و انضباط در کارها هستید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا همیشه به انجام کارها طبق برنامه پایبند هستید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا به رعایت قوانین و اصول در کارهایتان اهمیت می‌دهید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا از اینکه دیگران وظایف خود را درست انجام ندهند ناراحت می‌شوید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا همیشه سعی دارید در کارها دقیق و منظم باشید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا به مسئولیت‌های خود پایبند هستید؟"},
    {"category": "G - وظیفه‌شناسی", "question_text": "آیا همیشه وظایف خود را به موقع انجام می‌دهید؟"},

    # Factor H (Social Boldness) - 13 Questions
    {"category": "H - جسارت اجتماعی", "question_text": "آیا از صحبت کردن در جمع‌های بزرگ احساس راحتی می‌کنید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا در موقعیت‌های اجتماعی جسور هستید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا از بیان نظرات خود در مقابل دیگران لذت می‌برید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا در مواجهه با جمعیت‌های بزرگ احساس آرامش می‌کنید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا از شروع مکالمه با غریبه‌ها ابایی ندارید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا در موقعیت‌های جدید احساس جسارت و اطمینان می‌کنید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا به راحتی در محیط‌های اجتماعی جدید قرار می‌گیرید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا از رهبری جمع‌های اجتماعی لذت می‌برید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا تمایل دارید در جمع‌های اجتماعی نظرات خود را بیان کنید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا در شرایط اجتماعی پرتنش آرام و جسور می‌مانید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا از اینکه نظر شما مورد توجه قرار بگیرد لذت می‌برید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا به راحتی نظر خود را در جمع‌های بزرگ مطرح می‌کنید؟"},
    {"category": "H - جسارت اجتماعی", "question_text": "آیا تمایل دارید در بحث‌های گروهی شرکت فعال داشته باشید؟"},

    # Factor I (Sensitivity) - 10 Questions
    {"category": "I - حساسیت", "question_text": "آیا به احساسات دیگران توجه زیادی دارید؟"},
    {"category": "I - حساسیت", "question_text": "آیا شما فردی همدل و حساس هستید؟"},
    {"category": "I - حساسیت", "question_text": "آیا به راحتی تحت تأثیر احساسات دیگران قرار می‌گیرید؟"},
    {"category": "I - حساسیت", "question_text": "آیا معمولاً احساسات خود را به دیگران نشان می‌دهید؟"},
    {"category": "I - حساسیت", "question_text": "آیا در برخورد با دیگران سعی می‌کنید آنها را درک کنید؟"},
    {"category": "I - حساسیت", "question_text": "آیا شما فردی لطیف و حساس به احساسات هستید؟"},
    {"category": "I - حساسیت", "question_text": "آیا اغلب احساسات خود را با دیگران به اشتراک می‌گذارید؟"},
    {"category": "I - حساسیت", "question_text": "آیا به احساسات دیگران حساسیت زیادی نشان می‌دهید؟"},
    {"category": "I - حساسیت", "question_text": "آیا شما فردی دلسوز هستید؟"},
    {"category": "I - حساسیت", "question_text": "آیا در مواجهه با افراد دیگر به احساسات آنها توجه زیادی دارید؟"},

    # Factor L (Vigilance) - 10 Questions
    {"category": "L - شکاکیت", "question_text": "آیا معمولاً به انگیزه‌های دیگران مشکوک هستید؟"},
    {"category": "L - شکاکیت", "question_text": "آیا فکر می‌کنید دیگران قصد سوءاستفاده از شما دارند؟"},
    {"category": "L - شکاکیت", "question_text": "آیا سخت می‌توانید به دیگران اعتماد کنید؟"},
    {"category": "L - شکاکیت", "question_text": "آیا اغلب به قصد و نیت دیگران شک دارید؟"},
    {"category": "L - شکاکیت", "question_text": "آیا فکر می‌کنید دیگران اغلب سعی دارند شما را فریب دهند؟"},
    {"category": "L - شکاکیت", "question_text": "آیا به سختی می‌توانید به افراد جدید اعتماد کنید؟"},
    {"category": "L - شکاکیت", "question_text": "آیا به راحتی به مردم اعتماد نمی‌کنید؟"},
    {"category": "L - شکاکیت", "question_text": "آیا فکر می‌کنید که دیگران اغلب شما را از نظر دور می‌کنند؟"},
    {"category": "L - شکاکیت", "question_text": "آیا به ندرت به دیگران اعتماد می‌کنید؟"},
    {"category": "L - شکاکیت", "question_text": "آیا شما همیشه نیت‌های دیگران را زیر سوال می‌برید؟"},

    # Factor M (Abstractedness) - 13 Questions
    {"category": "M - خیالبافی", "question_text": "آیا شما فردی خیالباف هستید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا تمایل دارید بیشتر در دنیای درونی خود زندگی کنید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا اغلب در خیال و فکر عمیق هستید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما از واقعیت به دنیای خیالات پناه می‌برید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا از تفکرات و خیالات ذهنی لذت می‌برید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما به خیالات و افکار خود بیشتر از واقعیت توجه دارید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما فردی عمیق و خیال‌پرداز هستید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا اغلب خود را در دنیای خیالات گم می‌کنید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما فردی خیالی و خیال‌پرداز هستید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما اغلب به موضوعات انتزاعی فکر می‌کنید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما اغلب به مسائل انتزاعی و ناملموس توجه می‌کنید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما از خیال‌پردازی برای فرار از واقعیت لذت می‌برید؟"},
    {"category": "M - خیالبافی", "question_text": "آیا شما از تفکرات عمیق و خیالی لذت می‌برید؟"},

    # Factor N (Privateness) - 10 Questions
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما معمولاً اطلاعات شخصی خود را با دیگران به اشتراک نمی‌گذارید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما به سختی احساسات خود را بیان می‌کنید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا اغلب ترجیح می‌دهید احساسات خود را نزد خود نگه دارید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما فردی محتاط هستید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما از به اشتراک گذاشتن اطلاعات شخصی خود با دیگران اجتناب می‌کنید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما فردی خوددار و محفوظ هستید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما اغلب احساسات خود را مخفی می‌کنید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا ترجیح می‌دهید دیگران از افکار و احساسات شما مطلع نشوند؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما از بیان احساسات خود اجتناب می‌کنید؟"},
    {"category": "N - حفظ حریم شخصی", "question_text": "آیا شما به ندرت درباره خودتان با دیگران صحبت می‌کنید؟"},

    # Factor O (Apprehension) - 13 Questions
    {"category": "O - اضطراب", "question_text": "آیا شما معمولاً در موقعیت‌های جدید احساس نگرانی می‌کنید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما فردی مضطرب و نگران هستید؟"},
    {"category": "O - اضطراب", "question_text": "آیا از اینکه به اشتباه عمل کنید، می‌ترسید؟"},
    {"category": "O - اضطراب", "question_text": "آیا اغلب نگران هستید که چیزی اشتباه پیش برود؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما معمولاً در مواجهه با مسائل احساس اضطراب می‌کنید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما به راحتی مضطرب می‌شوید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما اغلب خود را سرزنش می‌کنید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما اغلب نگران هستید که از پس وظایف خود برنیایید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما به راحتی دچار استرس می‌شوید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما فردی هستید که به مسائل کوچک هم اهمیت زیادی می‌دهید و نگران می‌شوید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما به راحتی دچار نگرانی‌های بی‌مورد می‌شوید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما معمولاً خود را تحت فشار قرار می‌دهید؟"},
    {"category": "O - اضطراب", "question_text": "آیا شما فردی هستید که به‌راحتی تحت فشارهای روانی قرار می‌گیرید؟"},

    # Factor Q1 (Openness to Change) - 10 Questions
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا از امتحان کردن راه‌های جدید لذت می‌برید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما اغلب از پذیرش تغییرات خوشحال می‌شوید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما مایل هستید چیزهای جدید را تجربه کنید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما فردی منعطف هستید و به تغییرات به راحتی پاسخ می‌دهید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما همیشه آماده پذیرش چیزهای جدید هستید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما از تغییرات استقبال می‌کنید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا از امتحان راه‌های جدید برای حل مسائل لذت می‌برید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما به راحتی خود را با تغییرات تطبیق می‌دهید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا از کشف و تجربه راه‌های جدید در زندگی لذت می‌برید؟"},
    {"category": "Q1 - باز بودن نسبت به تغییر", "question_text": "آیا شما از مواجهه با چالش‌های جدید استقبال می‌کنید؟"},

    # Factor Q2 (Self-Reliance) - 10 Questions
    {"category": "Q2 - اتکا به خود", "question_text": "آیا ترجیح می‌دهید تصمیمات را به تنهایی بگیرید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما به خودتان اعتماد دارید که از پس وظایف خود برآیید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما اغلب به جای کمک گرفتن از دیگران، سعی می‌کنید مشکلات را خودتان حل کنید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما معمولاً به تصمیمات خود اطمینان دارید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما به ندرت از دیگران کمک می‌خواهید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما در کارهای خود به دیگران متکی نیستید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما اغلب به خودتان اتکا می‌کنید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما در تصمیم‌گیری‌های خود مستقل عمل می‌کنید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما معمولاً به توانایی‌های خود در حل مسائل اعتماد دارید؟"},
    {"category": "Q2 - اتکا به خود", "question_text": "آیا شما به ندرت برای انجام کارها از دیگران کمک می‌خواهید؟"},

    # Factor Q3 (Perfectionism) - 10 Questions
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا همیشه سعی می‌کنید کارها را به بهترین نحو ممکن انجام دهید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا تمایل دارید که همه چیز بی‌نقص و کامل باشد؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا به دقت و نظم در کارها اهمیت می‌دهید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا همیشه به دنبال دستیابی به بالاترین استانداردها هستید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا شما اغلب به دنبال بی‌نقص بودن در کارها هستید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا شما اغلب خود را برای رسیدن به کمال تحت فشار قرار می‌دهید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا شما همیشه به دنبال انجام کارها به بهترین شکل ممکن هستید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا شما فردی دقیق و منظم هستید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا شما به کوچک‌ترین جزئیات در کارهای خود توجه می‌کنید؟"},
    {"category": "Q3 - کمال‌گرایی", "question_text": "آیا شما از خود انتظار دارید که همیشه به بهترین نحو عمل کنید؟"},

    # Factor Q4 (Tension) - 13 Questions
    {"category": "Q4 - تنش", "question_text": "آیا شما در موقعیت‌های استرس‌زا به سرعت دچار اضطراب می‌شوید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما معمولاً تحت فشار و استرس احساس تنش می‌کنید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا در مواجهه با مسائل دشوار احساس تنش می‌کنید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما در زمان انجام کارهای مهم دچار استرس می‌شوید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما اغلب تحت فشارهای روحی و روانی قرار می‌گیرید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما در شرایط استرس‌زا آرامش خود را از دست می‌دهید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما به سرعت تحت تأثیر فشارهای محیطی قرار می‌گیرید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما اغلب تحت تأثیر استرس و فشار قرار دارید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا در زمان‌های استرس‌زا دچار تنش‌های فیزیکی می‌شوید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا در شرایط اضطراب‌زا به سرعت آرامش خود را از دست می‌دهید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما به راحتی دچار تنش و اضطراب می‌شوید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما به سرعت تحت تأثیر موقعیت‌های استرس‌زا قرار می‌گیرید؟"},
    {"category": "Q4 - تنش", "question_text": "آیا شما اغلب از اضطراب و تنش رنج می‌برید؟"}
]

def populate_ketel_questions():
    for question in questions:
        q = CattellQuestion(
            category=question["category"],
            question_text=question["question_text"],
            score_no=0,
            score_maybe=1,
            score_yes=2,
        )
        db.session.add(q)
    db.session.commit()



if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
        populate_akhenbach_questions()
        print("Akhenbach questions populated successfully!")

        populate_ketel_questions()
        print("Ketel questions populated successfully!")

        from app import db, User, bcrypt  
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')

        admin_user = User(username='admin', password=hashed_password, is_admin=True)

        db.session.add(admin_user)
        db.session.commit()

        print('Admin user created!')



