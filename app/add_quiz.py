from app import db, Quiz, Category, Question, Option, Factor, app

# Ensure this code runs within the application context
with app.app_context():
    # Create a new quiz
    new_quiz = Quiz(title='آزمون تشخیص مشکلات رفتاری کودکان', description='این آزمون به بررسی مشکلات رفتاری کودکان می‌پردازد.', time_limit=60)
    db.session.add(new_quiz)
    db.session.flush()  # Get the quiz ID after flushing

    # Define factors
    factors = [
        'اضطراب/افسردگی',
        'گوشه گیری/افسردگی',
        'شکایات جسمانی',
        'مشکلات اجتماعی',
        'مشکلات تفکر',
        'مشکلات توجه',
        'رفتار قانون شکنی',
        'رفتار پرخاشگرانه',
        'سایر مشکلات'
    ]

    # Add factors to the database
    factor_objects = []
    for factor_name in factors:
        factor = Factor(name=factor_name)
        db.session.add(factor)
        factor_objects.append(factor)
    db.session.flush()

    # Define categories
    categories = [
        'Demographic Information',  # New category for demographic questions
    ] + factors  # Add factors as categories too

    # Add categories to the database
    category_objects = []
    for category_name in categories:
        category = Category(name=category_name, quiz_id=new_quiz.id)
        db.session.add(category)
        category_objects.append(category)
    db.session.flush()

    # Add demographic questions (Age and Gender) to the "Demographic Information" category
    demographic_category = category_objects[0]  # Assuming the first category is "Demographic Information"

    # Age Question
    age_question = Question(text='فرزند شما در سن چه بازه‌ای قرار دارد؟', category_id=demographic_category.id)
    db.session.add(age_question)
    db.session.flush()
    age_options = [
        ('6-8 سال', 2),
        ('9-11 سال', 1),
        ('12-14 سال', 0),
        ('15-16 سال', 0)
    ]
    for option_text, grade in age_options:
        option = Option(text=option_text, grade=grade, question_id=age_question.id)
        db.session.add(option)

    # Gender Question
    gender_question = Question(text='جنسیت فرزند خود را انتخاب کنید.', category_id=demographic_category.id)
    db.session.add(gender_question)
    db.session.flush()
    gender_options = [
        ('پسر', 2),
        ('دختر', 1)
    ]
    for option_text, grade in gender_options:
        option = Option(text=option_text, grade=grade, question_id=gender_question.id)
        db.session.add(option)

    # Add questions and options for each category and factor
    questions_data = [
        # اضطراب/افسردگی
        ('زیاد گریه می کند', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('ترس از حیوانات دارد', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('ترس از مدرسه دارد', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('می‌ترسد که کار بدی انجام دهد', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('فکر می‌کند باید بی نقص باشد', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('احساس طردشدن دارد', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('احساس بی ارزشی می‌کند', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('عصبی و پرتنش است', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('ترسو و مضطرب است', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('احساس گناه می‌کند', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('کمرو و خجالتی است', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('به فکر خودکشی افتاده است', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('نگران است', category_objects[1], factor_objects[0], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # گوشه گیری/افسردگی
        ('لذت کمی از چیزها می‌برد', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('تنهایی را ترجیح می‌دهد', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('از صحبت کردن امتناع می‌کند', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('تودار و مرموز است', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خجالتی یا ترسو است', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('کم فعالیت و کم انرژی است', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('ناراحت و غمگین است', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('گوشه گیر است', category_objects[2], factor_objects[1], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # شکایات جسمانی
        ('کابوس می‌بیند', category_objects[3], factor_objects[2], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('یبوست دارد', category_objects[3], factor_objects[2], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('احساس گیجی و منگی می‌کند', category_objects[3], factor_objects[2], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('احساس خستگی شدید می‌کند', category_objects[3], factor_objects[2], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('از دردهای جسمانی شکایت دارد', category_objects[3], factor_objects[2], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # مشکلات اجتماعی
        ('وابستگی زیادی به بزرگترها دارد', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('از تنهایی شکایت می‌کند', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('با دیگران کنار نمی‌آید', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('حسادت می‌کند', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('احساس می‌کند دیگران دنبالش هستند', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیاد صدمه می‌بیند', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('مورد تمسخر قرار می‌گیرد', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بچه‌های دیگر او را دوست ندارند', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('دست و پا چلفتی است', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('میل به بودن با بچه‌های کوچکتر دارد', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('مشکلات گفتاری دارد', category_objects[4], factor_objects[3], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # مشکلات تفکر
        ('ناتوانی در اجتناب از افکار خاص دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('به خود آسیب می‌رساند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('صداهایی می‌شنود که وجود ندارند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('حرکات عصبی و انقباض عضلات دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('پوست خود را فشار می‌دهد و زخمی می‌کند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بازی با اعضای تناسلی در ملا عام دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بازی کردن زیاد با اعضای تناسلی دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('اعمال خاصی را بارها و بارها تکرار می‌کند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('چیزهایی می‌بیند که وجود ندارند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('کم‌خوابی دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('چیزهایی که به دردش نمی‌خورند را جمع می‌کند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('رفتارهای عجیب و غریب دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('افکار عجیب و غریب دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در خواب راه می‌رود یا صحبت می‌کند', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('مشکل در خوابیدن دارد', category_objects[5], factor_objects[4], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # مشکلات توجه
        ('بچه گانه تر از سن خود رفتار می کند', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('کارهایی که شروع می کند، تمام نمی کند', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('نمی تواند حواسش را جمع کند، نمی تواند توجه اش را برای مدت طولانی نگه دارد', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('نمی تواند آرام بنشیند، بی قرار و بیش فعال است', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('گیج یا سردرگم به نظر می رسد', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خیال پردازی می کند یا در افکار خودش غرق می شود', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بدون فکر عمل می کند', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خود تکالیف درسی را خوب انجام نمی دهد', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بی توجه است یا به راحتی حواسش پرت می شود', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('مات و مبهوت به جایی خیره می شود', category_objects[6], factor_objects[5], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # رفتار قانون شکنی
        ('مصرف مشروبات الکلی دارد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('فقدان احساس گناه دارد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیرپا گذاشتن مقررات دارد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('گشتن با دوستان بد دارد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('دروغ می گوید یا تقلب می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('میل به بودن با بچه های بزرگ تر از خودش دارد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('از خانه فرار می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('آتش روشن می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('مشکلات جنسی دارد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در منزل بدون اجازه وسایل را برمی دارد (دزدی می کند)', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خارج از منزل بدون اجازه وسایل را برمی دارد (دزدی می کند)', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('دشنام می دهد یا کلمات رکیک به کار می برد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیاد به مسائل جنسی فکر می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('سیگار یا قلیان می کشد', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('از مدرسه گریزان است و فرار می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('برای مقاصد غیردارویی مواد مخدر مصرف می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('اموال عمومی را تخریب می کند', category_objects[7], factor_objects[6], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # رفتار پرخاشگرانه
        ('زیاد جر و بحث می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('نسبت به دیگران بی رحم است، زورگو است و دیگران را آزار می دهد', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('دلش می خواهد به او زیاد توجه کنند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('وسایل خودش را خراب می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('وسایل متعلق به خانواده یا دیگران را خراب می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در خانه نافرمانی می کند (حرف گوش نمی دهد)', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در مدرسه نافرمانی می کند (حرف گوش نمی دهد)', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیاد جنگ و دعوا می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بدون دلیل با دیگران کتک کاری می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیاد جیغ و داد می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('کله شق و یک دنده، عبوس و زودرنج است', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خلق یا احساساتش سریع تغییر می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیاد قهر می کند و اخمو است', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بدگمان و شکاک است', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('دیگران را مسخره و اذیت می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('قشقرق راه می اندازد یا تند خو است', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('دیگران را تهدید می کند', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بیش از حد پر سر و صدا است', category_objects[8], factor_objects[7], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # سایر مشکلات
        ('کم خوابی دارد', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('بیش از حد غذا می خورد (پرخور است)', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('اضافه وزن دارد', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خودنمایی یا دلقک بازی می کند', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('خیلی خجالتی یا ترسو است', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در طول روز و یا شب از اکثر بچه ها کمتر می خوابد', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در طول روز و یا شب از اکثر بچه ها بیشتر می خوابد', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('زیاد صحبت می کند', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('انگشت شست خود را می مکد', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('در طول روز خودش را خیس می کند', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('شب ادراری دارد', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('غر و نق می زند', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('اگر کودک یا نوجوان پسر است «آرزو می‌کند دختر باشد» یا اگر کودک یا نوجوان دختر است «آرزو می‌کند پسر باشد»', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('با دیگران ارتباط برقرار نمی‌کند و گوشه‌گیر است', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),
        ('نگران است', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)]),

        # Question 113
        ('چنانچه کودک یا نوجوان مشکلات دیگری دارد که در فهرست بالا نیامده آنها را بنویسید', category_objects[9], factor_objects[8], [('خیر', 2), ('بعضی مواقع', 1), ('بلی', 0)])
    ]

    # Loop through questions and add them with their options
    for question_text, category, factor, options in questions_data:
        question = Question(text=question_text, category_id=category.id, factor_id=factor.id)
        db.session.add(question)
        db.session.flush()  # Ensure question ID is available

        # Add options for this question
        for option_text, grade in options:
            option = Option(text=option_text, grade=grade, question_id=question.id)
            db.session.add(option)

    # Commit all changes to the database
    db.session.commit()

    print("Quiz and related data, including age and gender questions, added successfully!")
