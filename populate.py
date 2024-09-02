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

    # مشکلات دیگر (Other Specified Problems)
    {"category": "سایر مشکلات", "question_text": "اگر کودک یا نوجوان مشکلات دیگری دارد که در فهرست بالا نیامده آنها را بنویسید"},
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

if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()
        populate_akhenbach_questions()
        print("Akhenbach questions populated successfully!")
