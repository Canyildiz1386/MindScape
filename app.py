from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib

matplotlib.use("Agg")

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "home"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)



class AkhenbachQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    score_no = db.Column(db.Integer, default=0)
    score_sometimes = db.Column(db.Integer, default=1)
    score_yes = db.Column(db.Integer, default=2)


class CattellQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    score_no = db.Column(db.Integer, default=0)
    score_maybe = db.Column(db.Integer, default=1)
    score_yes = db.Column(db.Integer, default=2)


class ExamResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    score_data = db.Column(db.String(1000), nullable=False)
    date_taken = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship("User", backref="exam_results")

    def __repr__(self):
        return f"<ExamResult {self.exam_type} by User {self.user_id}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("Home Page/homepage.html")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("❌ رمزهای عبور مطابقت ندارند! لطفاً دوباره تلاش کنید. ❌", "danger")
        return redirect(url_for("home", open_modal=True))

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed_password, is_admin=False)
    db.session.add(user)
    db.session.commit()
    flash("✅ حساب کاربری شما با موفقیت ایجاد شد! 🎉", "success")
    return redirect(url_for("user_panel"))


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        flash("🎉 ورود موفقیت‌آمیز بود! خوش آمدید. 😊", "success")
        if user.is_admin:
            return redirect(url_for("admin_panel"))
        else:
            return redirect(url_for("user_panel"))
    else:
        flash("❌ ورود ناموفق. لطفاً نام کاربری و رمز عبور را بررسی کنید. ❌", "danger")
        return redirect(url_for("home", open_modal=True))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("👋 شما با موفقیت خارج شدید. تا دیدار بعدی! 😊", "info")
    return redirect(url_for("home", open_modal=True))


@app.route("/admin_panel")
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("🚫 شما اجازه دسترسی به این بخش را ندارید! 🚫", "danger")
        return redirect(url_for("home"))
    return render_template("Admin Panel Page/adminhome.html")


import json


@app.route("/user_panel")
@login_required
def user_panel():
    if current_user.is_admin:
        flash("🚫 شما اجازه دسترسی به این بخش را ندارید! 🚫", "danger")
        return redirect(url_for("admin_panel"))

    exam_results = ExamResult.query.filter_by(user_id=current_user.id).all()

    for result in exam_results:
        result.score_data = json.loads(result.score_data)

        if result.exam_type == "Akhenbach":
            result.interpretation = calculate_results(
                result.gender, result.age, result.score_data
            )
        elif result.exam_type == "Cattell":
            result.interpretation = calculate_result(
                result.gender, result.age, result.score_data
            )

    exam_count = len(exam_results)

    return render_template(
        "User Panel Page/index.html", exam_results=exam_results, exam_count=exam_count
    )

@app.route("/update_user_info", methods=["POST"])
@login_required
def update_user_info():
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("phone")
    address = request.form.get("address")

    current_user.email = email
    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.phone = phone
    current_user.address = address
    db.session.commit()

    flash("✅ اطلاعات شما با موفقیت به‌روزرسانی شد! 🔄", "success")
    return redirect(url_for("user_panel"))


@app.route("/admin-quiz")
@login_required
def admin_quiz():
    if not current_user.is_admin:
        flash("🚫 شما اجازه دسترسی به این بخش را ندارید! 🚫", "danger")
        return redirect(url_for("home"))
    return render_template("Admin Quiz Page/adminquiz.html")


@app.route("/take_akhenbach", methods=["GET", "POST"])
@login_required
def take_akhenbach():
    if request.method == "POST":
        gender = request.form.get("gender")
        birthdate = request.form.get("birthdate")

        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        return redirect(url_for("akhenbach_questions", gender=gender, age=age))

    return render_template("User Panel Page/akhenbach_info.html")



import json


@app.route("/akhenbach_questions/<gender>/<age>", methods=["GET", "POST"])
@login_required
def akhenbach_questions(gender, age):
    if request.method == "POST":
        score = {
            "اضطراب/افسردگی": 0,
            "گوشه گیری/افسردگی": 0,
            "شکایات جسمانی": 0,
            "مشکلات اجتماعی": 0,
            "مشکلات تفکر": 0,
            "مشکلات توجه": 0,
            "رفتار قانون شکنی": 0,
            "رفتار پرخاشگرانه": 0,
            "سایر مشکلات": 0,
        }

        for question_id, answer in request.form.items():
            if question_id.isdigit():
                question = AkhenbachQuestion.query.get(int(question_id))
                if answer == "no":
                    score[question.category] += question.score_no
                elif answer == "sometimes":
                    score[question.category] += question.score_sometimes
                elif answer == "yes":
                    score[question.category] += question.score_yes

        score_data = json.dumps(score)

        exam_result = ExamResult(
            user_id=current_user.id,
            exam_type="Akhenbach",
            gender=gender,
            age=age,
            score_data=score_data,
        )
        db.session.add(exam_result)
        db.session.commit()

        return redirect(url_for("akhenbach_results", gender=gender, age=age, **score))

    questions = AkhenbachQuestion.query.all()
    return render_template(
        "User Panel Page/akhenbach_questions.html",
        questions=questions,
        gender=gender,
        age=age,
    )


@app.route("/akhenbach_results")
@login_required
def akhenbach_results():
    gender = request.args.get("gender")
    age = int(request.args.get("age"))
    score = {
        "اضطراب/افسردگی": request.args.get("اضطراب/افسردگی", type=int, default=0),
        "گوشه گیری/افسردگی": request.args.get("گوشه گیری/افسردگی", type=int, default=0),
        "شکایات جسمانی": request.args.get("شکایات جسمانی", type=int, default=0),
        "مشکلات اجتماعی": request.args.get("مشکلات اجتماعی", type=int, default=0),
        "مشکلات تفکر": request.args.get("مشکلات تفکر", type=int, default=0),
        "مشکلات توجه": request.args.get("مشکلات توجه", type=int, default=0),
        "رفتار قانون شکنی": request.args.get("رفتار قانون شکنی", type=int, default=0),
        "رفتار پرخاشگرانه": request.args.get("رفتار پرخاشگرانه", type=int, default=0),
        "سایر مشکلات": request.args.get("سایر مشکلات", type=int, default=0),
    }

    results = calculate_results(gender, age, score)
    return render_template(
        "User Panel Page/akhenbach_results.html", result_message=results
    )


def calculate_results(gender, age, score):
    interpretation = ""
    t_scores = []
    t_score_mapping = {
        "اضطراب/افسردگی": get_t_score(
            "اضطراب/افسردگی", score["اضطراب/افسردگی"], gender, age
        ),
        "گوشه گیری/افسردگی": get_t_score(
            "گوشه گیری/افسردگی", score["گوشه گیری/افسردگی"], gender, age
        ),
        "شکایات جسمانی": get_t_score(
            "شکایات جسمانی", score["شکایات جسمانی"], gender, age
        ),
        "مشکلات اجتماعی": get_t_score(
            "مشکلات اجتماعی", score["مشکلات اجتماعی"], gender, age
        ),
        "مشکلات تفکر": get_t_score("مشکلات تفکر", score["مشکلات تفکر"], gender, age),
        "مشکلات توجه": get_t_score("مشکلات توجه", score["مشکلات توجه"], gender, age),
        "رفتار قانون شکنی": get_t_score(
            "رفتار قانون شکنی", score["رفتار قانون شکنی"], gender, age
        ),
        "رفتار پرخاشگرانه": get_t_score(
            "رفتار پرخاشگرانه", score["رفتار پرخاشگرانه"], gender, age
        ),
        "سایر مشکلات": "مقیاس سفارشی است",
    }

    for category, t_score in t_score_mapping.items():
        t_scores.append(t_score)
        if t_score == "نرمال":
            interpretation += (
                f"😊 نمره {category} فرزند شما در محدوده نرمال قرار دارد. 👌 وضعیت او طبیعی است و نیازی به نگرانی نیست.<br>"
            )
        elif t_score == "مرزی":
            interpretation += (
                f"🤔 نمره {category} فرزند شما در محدوده مرزی قرار دارد. 📊 توصیه می‌شود کمی دقت بیشتری به این موضوع داشته باشید.<br>"
            )
        elif t_score == "بالینی":
            interpretation += (
                f"⚠️ نمره {category} فرزند شما در محدوده بالینی قرار دارد. 🚨 حتماً با یک متخصص مشورت کنید.<br>"
            )

    return interpretation



def get_t_score(category, raw_score, gender, age):
    if category == "اضطراب/افسردگی":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 7:
                    return "نرمال"
                elif 8 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 8:
                    return "نرمال"
                elif 9 <= raw_score <= 12:
                    return "مرزی"
                elif raw_score >= 13:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 9:
                    return "نرمال"
                elif 10 <= raw_score <= 13:
                    return "مرزی"
                elif raw_score >= 14:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 11:
                    return "نرمال"
                elif 12 <= raw_score <= 15:
                    return "مرزی"
                elif raw_score >= 16:
                    return "بالینی"

    if category == "گوشه گیری/افسردگی":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 5:
                    return "نرمال"
                elif 6 <= raw_score <= 9:
                    return "مرزی"
                elif raw_score >= 10:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 7:
                    return "نرمال"
                elif 8 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 6:
                    return "نرمال"
                elif 7 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 8:
                    return "نرمال"
                elif 9 <= raw_score <= 12:
                    return "مرزی"
                elif raw_score >= 13:
                    return "بالینی"

    if category == "شکایات جسمانی":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 3:
                    return "نرمال"
                elif 4 <= raw_score <= 5:
                    return "مرزی"
                elif raw_score >= 6:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 5:
                    return "نرمال"
                elif 6 <= raw_score <= 7:
                    return "مرزی"
                elif raw_score >= 8:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 4:
                    return "نرمال"
                elif 5 <= raw_score <= 6:
                    return "مرزی"
                elif raw_score >= 7:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 6:
                    return "نرمال"
                elif 7 <= raw_score <= 8:
                    return "مرزی"
                elif raw_score >= 9:
                    return "بالینی"

    if category == "مشکلات اجتماعی":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 6:
                    return "نرمال"
                elif 7 <= raw_score <= 9:
                    return "مرزی"
                elif raw_score >= 10:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 8:
                    return "نرمال"
                elif 9 <= raw_score <= 11:
                    return "مرزی"
                elif raw_score >= 12:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 7:
                    return "نرمال"
                elif 8 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 9:
                    return "نرمال"
                elif 10 <= raw_score <= 12:
                    return "مرزی"
                elif raw_score >= 13:
                    return "بالینی"

    if category == "مشکلات تفکر":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 4:
                    return "نرمال"
                elif 5 <= raw_score <= 6:
                    return "مرزی"
                elif raw_score >= 7:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 6:
                    return "نرمال"
                elif 7 <= raw_score <= 9:
                    return "مرزی"
                elif raw_score >= 10:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 5:
                    return "نرمال"
                elif 6 <= raw_score <= 8:
                    return "مرزی"
                elif raw_score >= 9:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 7:
                    return "نرمال"
                elif 8 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"

    if category == "مشکلات توجه":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 7:
                    return "نرمال"
                elif 8 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 9:
                    return "نرمال"
                elif 10 <= raw_score <= 12:
                    return "مرزی"
                elif raw_score >= 13:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 8:
                    return "نرمال"
                elif 9 <= raw_score <= 11:
                    return "مرزی"
                elif raw_score >= 12:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 10:
                    return "نرمال"
                elif 11 <= raw_score <= 13:
                    return "مرزی"
                elif raw_score >= 14:
                    return "بالینی"

    if category == "رفتار قانون شکنی":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 5:
                    return "نرمال"
                elif 6 <= raw_score <= 8:
                    return "مرزی"
                elif raw_score >= 9:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 7:
                    return "نرمال"
                elif 8 <= raw_score <= 10:
                    return "مرزی"
                elif raw_score >= 11:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 6:
                    return "نرمال"
                elif 7 <= raw_score <= 9:
                    return "مرزی"
                elif raw_score >= 10:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 8:
                    return "نرمال"
                elif 9 <= raw_score <= 11:
                    return "مرزی"
                elif raw_score >= 12:
                    return "بالینی"

    if category == "رفتار پرخاشگرانه":
        if gender == "male":
            if 6 <= age <= 11:
                if raw_score <= 9:
                    return "نرمال"
                elif 10 <= raw_score <= 12:
                    return "مرزی"
                elif raw_score >= 13:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 11:
                    return "نرمال"
                elif 12 <= raw_score <= 14:
                    return "مرزی"
                elif raw_score >= 15:
                    return "بالینی"
        elif gender == "female":
            if 6 <= age <= 11:
                if raw_score <= 10:
                    return "نرمال"
                elif 11 <= raw_score <= 13:
                    return "مرزی"
                elif raw_score >= 14:
                    return "بالینی"
            elif 12 <= age <= 18:
                if raw_score <= 12:
                    return "نرمال"
                elif 13 <= raw_score <= 15:
                    return "مرزی"
                elif raw_score >= 16:
                    return "بالینی"
    return "مقیاس سفارشی است"


@app.route("/take_cattell", methods=["GET", "POST"])
@login_required
def take_cattell():
    if request.method == "POST":
        gender = request.form.get("gender")
        birthdate = request.form.get("birthdate")

        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = (
            today.year
            - birthdate.year
            - ((today.month, today.day) < (birthdate.month, birthdate.day))
        )

        return redirect(url_for("cattell_questions", gender=gender, age=age))

    return render_template("User Panel Page/cattell_info.html")


@app.route("/cattell_questions/<gender>/<age>", methods=["GET", "POST"])
@login_required
def cattell_questions(gender, age):
    if request.method == "POST":
        score = {
            "A": 0,
            "B": 0,
            "C": 0,
            "E": 0,
            "F": 0,
            "G": 0,
            "H": 0,
            "I": 0,
            "L": 0,
            "M": 0,
            "N": 0,
            "O": 0,
            "Q1": 0,
            "Q2": 0,
            "Q3": 0,
            "Q4": 0,
        }

        for question_id, answer in request.form.items():
            if question_id.isdigit():
                question = CattellQuestion.query.get(int(question_id))
                if answer == "no":
                    score[question.category] += question.score_no
                elif answer == "maybe":
                    score[question.category] += question.score_maybe
                elif answer == "yes":
                    score[question.category] += question.score_yes

        score_data = json.dumps(score)

        exam_result = ExamResult(
            user_id=current_user.id,
            exam_type="Cattell",
            gender=gender,
            age=age,
            score_data=score_data,
        )
        db.session.add(exam_result)
        db.session.commit()

        return redirect(url_for("cattell_results", gender=gender, age=age, **score))

    questions = CattellQuestion.query.all()
    return render_template(
        "User Panel Page/cattell_questions.html",
        questions=questions,
        gender=gender,
        age=age,
    )


@app.route("/cattell_results")
@login_required
def cattell_results():
    gender = request.args.get("gender")
    age = int(request.args.get("age"))
    score = {
        "A": request.args.get("A", type=int, default=0),
        "B": request.args.get("B", type=int, default=0),
        "C": request.args.get("C", type=int, default=0),
        "E": request.args.get("E", type=int, default=0),
        "F": request.args.get("F", type=int, default=0),
        "G": request.args.get("G", type=int, default=0),
        "H": request.args.get("H", type=int, default=0),
        "I": request.args.get("I", type=int, default=0),
        "L": request.args.get("L", type=int, default=0),
        "M": request.args.get("M", type=int, default=0),
        "N": request.args.get("N", type=int, default=0),
        "O": request.args.get("O", type=int, default=0),
        "Q1": request.args.get("Q1", type=int, default=0),
        "Q2": request.args.get("Q2", type=int, default=0),
        "Q3": request.args.get("Q3", type=int, default=0),
        "Q4": request.args.get("Q4", type=int, default=0),
    }

    results = calculate_result(gender, age, score)
    return render_template(
        "User Panel Page/cattell_results.html", result_message=results
    )


def calculate_result(gender, age, score):
    interpretation = ""
    t_scores = []

    for factor, raw_score in score.items():
        interpretation += interpret_cattell(factor, raw_score)

    return interpretation


def interpret_cattell(factor, raw_score):
    result = ""

    if factor == "A":
        if raw_score <= 3:
            result = "🧍‍♂️ نمره پایین در عامل A: شما فردی اجتماعی نیستید و ترجیح می‌دهید تنها باشید. 😶‍🌫️<br>"
        elif 4 <= raw_score <= 7:
            result = (
                "😀 نمره متوسط در عامل A: شما در تعاملات اجتماعی متعادل هستید. 😊<br>"
            )
        else:
            result = "🎉 نمره بالا در عامل A: شما خیلی اجتماعی هستید و دوست دارید با دیگران ارتباط برقرار کنید. 💬<br>"

    elif factor == "B":  # هوش عمومی
        if raw_score <= 3:
            result = (
                "🧠 نمره پایین در عامل B: توانایی تفکر انتزاعی شما پایین است. 🤔<br>"
            )
        elif 4 <= raw_score <= 7:
            result = "🔍 نمره متوسط در عامل B: شما دارای هوش طبیعی هستید. 🧑‍🎓<br>"
        else:
            result = "💡 نمره بالا در عامل B: شما دارای توانایی‌های یادگیری سریع و تفکر انتزاعی هستید. 👨‍🏫<br>"

    elif factor == "C":  # پایداری هیجانی
        if raw_score <= 3:
            result = "😰 نمره پایین در عامل C: شما به راحتی دچار ناپایداری هیجانی می‌شوید. 😢<br>"
        elif 4 <= raw_score <= 7:
            result = (
                "😊 نمره متوسط در عامل C: شما از پایداری هیجانی خوبی برخوردارید. 😊<br>"
            )
        else:
            result = "😎 نمره بالا در عامل C: شما خیلی پایدار و آرام هستید. 😌<br>"

    elif factor == "E":  # سلطه‌گری در برابر سلطه‌پذیری
        if raw_score <= 3:
            result = "🧑‍🤝‍🧑 نمره پایین در عامل E: شما فردی مطیع هستید و از درگیری‌ها اجتناب می‌کنید. 🫱<br>"
        elif 4 <= raw_score <= 7:
            result = "⚖️ نمره متوسط در عامل E: شما بین همکاری و assertiveness تعادل دارید. ⚖️<br>"
        else:
            result = "🗣️ نمره بالا در عامل E: شما خیلی assertive هستید و دوست دارید مدیریت کنید. 👩‍💼<br>"

    elif factor == "F":  # سرزندگی در برابر جدیت
        if raw_score <= 3:
            result = "😐 نمره پایین در عامل F: شما فردی جدی و اهل برنامه هستید. 📝<br>"
        elif 4 <= raw_score <= 7:
            result = "😊 نمره متوسط در عامل F: شما تعادل خوبی بین جدیت و سرزندگی دارید. 😃<br>"
        else:
            result = "😄 نمره بالا در عامل F: شما سرزنده و شاداب هستید و دوست دارید زندگی را به سبک خود بگذرانید. 🎉<br>"

    elif factor == "G":  # خودکنترلی و رعایت قواعد در برابر نافرمانی
        if raw_score <= 3:
            result = "🤷‍♂️ نمره پایین در عامل G: شما زیاد به قوانین توجه نمی‌کنید و انعطاف‌پذیری بالایی دارید. 😌<br>"
        elif 4 <= raw_score <= 7:
            result = "⚖️ نمره متوسط در عامل G: شما تعادل خوبی در رعایت قواعد و انعطاف‌پذیری دارید. ⚖️<br>"
        else:
            result = "👮‍♂️ نمره بالا در عامل G: شما فردی با مسئولیت هستید و قوانین را به شدت رعایت می‌کنید. 👨‍⚖️<br>"

    elif factor == "H":  # جسارت اجتماعی در برابر خجالتی بودن
        if raw_score <= 3:
            result = "😶 نمره پایین در عامل H: شما خجالتی و محتاط هستید و از برخوردهای اجتماعی اجتناب می‌کنید. 🤐<br>"
        elif 4 <= raw_score <= 7:
            result = "😊 نمره متوسط در عامل H: شما در موقعیت‌های اجتماعی رفتار متعادلی دارید. 😎<br>"
        else:
            result = "🎤 نمره بالا در عامل H: شما خیلی جسور و اجتماعی هستید و از حضور در مرکز توجه لذت می‌برید. 🕺<br>"

    elif factor == "I":  # حساسیت و احساسات‌گرایی در برابر واقع‌گرایی
        if raw_score <= 3:
            result = "🛠 نمره پایین در عامل I: شما فردی واقع‌گرا و عمل‌گرا هستید و به احساسات کمتر توجه دارید. 🧑‍🔧<br>"
        elif 4 <= raw_score <= 7:
            result = "🤔 نمره متوسط در عامل I: شما تعادل خوبی بین حساسیت و واقع‌گرایی دارید. 🧑‍🎓<br>"
        else:
            result = "🌸 نمره بالا در عامل I: شما فردی حساس، لطیف و احساساتی هستید و به جزئیات احساسی اهمیت می‌دهید. 💕<br>"

    elif factor == "L":  # شکاکیت در برابر اعتماد
        if raw_score <= 3:
            result = "🤗 نمره پایین در عامل L: شما به دیگران اعتماد دارید و راحت با آن‌ها کنار می‌آیید. 🤝<br>"
        elif 4 <= raw_score <= 7:
            result = "🤔 نمره متوسط در عامل L: شما تعادل خوبی بین اعتماد و شکاکیت دارید. 🤷‍♂️<br>"
        else:
            result = "🧐 نمره بالا در عامل L: شما نسبت به دیگران شکاک و منتقد هستید و به راحتی اعتماد نمی‌کنید. 😠<br>"

    elif factor == "M":  # تخیل در برابر واقع‌گرایی
        if raw_score <= 3:
            result = "🛠 نمره پایین در عامل M: شما واقع‌گرا و منطقی هستید و تخیل زیادی ندارید. 🔧<br>"
        elif 4 <= raw_score <= 7:
            result = "⚖️ نمره متوسط در عامل M: شما تعادل خوبی بین تخیل و واقع‌گرایی دارید. 🧑‍🎨<br>"
        else:
            result = "🌈 نمره بالا در عامل M: شما فردی خیال‌پرداز هستید و بیشتر در دنیای تخیلات خود زندگی می‌کنید. 🌠<br>"

    elif factor == "N":  # هوشیاری و زرنگی در برابر سادگی
        if raw_score <= 3:
            result = "😇 نمره پایین در عامل N: شما فردی ساده، صادق و بدون پیچیدگی هستید. 🥰<br>"
        elif 4 <= raw_score <= 7:
            result = "🧐 نمره متوسط در عامل N: شما تعادل خوبی بین هوشیاری و سادگی دارید. 😊<br>"
        else:
            result = "🤨 نمره بالا در عامل N: شما فردی هوشیار، زرنگ و پیچیده هستید و روابطتان را حساب‌شده مدیریت می‌کنید. 🧠<br>"

    elif factor == "O":  # احساس گناه و نگرانی در برابر اعتماد به نفس
        if raw_score <= 3:
            result = "😌 نمره پایین در عامل O: شما به خود اعتماد دارید و به راحتی نگران نمی‌شوید. 😊<br>"
        elif 4 <= raw_score <= 7:
            result = "😐 نمره متوسط در عامل O: شما تعادل خوبی بین اعتماد به نفس و نگرانی دارید. 😇<br>"
        else:
            result = "😟 نمره بالا در عامل O: شما نگرانی زیادی دارید و خود را به شدت قضاوت می‌کنید. 😔<br>"

    elif factor == "Q1":  # محافظه‌کاری در برابر باز بودن به تغییر
        if raw_score <= 3:
            result = "🛑 نمره پایین در عامل Q1: شما فردی محافظه‌کار هستید و تغییرات را دوست ندارید. 🧳<br>"
        elif 4 <= raw_score <= 7:
            result = "⚖️ نمره متوسط در عامل Q1: شما تعادل خوبی بین سنت‌گرایی و تغییرپذیری دارید. 🔄<br>"
        else:
            result = "🌍 نمره بالا در عامل Q1: شما خیلی باز به تغییرات و نوآوری هستید و از ایده‌های جدید استقبال می‌کنید. 🚀<br>"

    elif factor == "Q2":  # اتکا به خود در برابر اتکا به گروه
        if raw_score <= 3:
            result = "🤝 نمره پایین در عامل Q2: شما بیشتر به گروه و حمایت دیگران تکیه می‌کنید. 👥<br>"
        elif 4 <= raw_score <= 7:
            result = "⚖️ نمره متوسط در عامل Q2: شما تعادل خوبی بین اتکا به خود و دیگران دارید. 🔗<br>"
        else:
            result = "🤠 نمره بالا در عامل Q2: شما خیلی مستقل هستید و ترجیح می‌دهید کارها را به تنهایی انجام دهید. 🧍‍♂️<br>"

    elif factor == "Q3":
        if raw_score <= 3:
            result = "🙃 نمره پایین در عامل Q3: شما نظم زیادی ندارید و به راحتی قوانین را رعایت نمی‌کنید. 😵‍💫<br>"
        elif 4 <= raw_score <= 7:
            result = "🙂 نمره متوسط در عامل Q3: شما تعادل خوبی بین کمال‌گرایی و انعطاف‌پذیری دارید. 🧘‍♀️<br>"
        else:
            result = "👌 نمره بالا در عامل Q3: شما بسیار منظم، دقیق و کمال‌گرا هستید و به جزئیات توجه زیادی دارید. 📝<br>"

    elif factor == "Q4":
        if raw_score <= 3:
            result = "😌 نمره پایین در عامل Q4: شما آرام و ریلکس هستید و به ندرت دچار تنش می‌شوید. 🧘‍♂️<br>"
        elif 4 <= raw_score <= 7:
            result = (
                "🙂 نمره متوسط در عامل Q4: شما تعادل خوبی بین تنش و آرامش دارید. 😎<br>"
            )
        else:
            result = "😫 نمره بالا در عامل Q4: شما خیلی تنش‌زا و عصبی هستید و همیشه در فشار و اضطراب هستید. 😖<br>"

    return result


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=9003, host="0.0.0.0")
