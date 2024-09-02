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
matplotlib.use('Agg')  # Use the Agg backend for non-GUI, image-only rendering

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


class AkhenbachQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    score_no = db.Column(db.Integer, default=0)
    score_sometimes = db.Column(db.Integer, default=1)
    score_yes = db.Column(db.Integer, default=2)


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
    return redirect(url_for("home"))


@app.route("/admin_panel")
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("🚫 شما اجازه دسترسی به این بخش را ندارید! 🚫", "danger")
        return redirect(url_for("home"))
    return render_template("Admin Panel Page/adminhome.html")


@app.route("/user_panel")
@login_required
def user_panel():
    if current_user.is_admin:
        flash("🚫 شما اجازه دسترسی به این بخش را ندارید! 🚫", "danger")
        return redirect(url_for("admin_panel"))
    return render_template("User Panel Page/index.html")


from datetime import datetime

@app.route("/take_akhenbach", methods=["GET", "POST"])
@login_required
def take_akhenbach():
    if request.method == "POST":
        gender = request.form.get("gender")
        birthdate = request.form.get("birthdate")
        
        birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        return redirect(url_for("akhenbach_questions", gender=gender, age=age))
    
    return render_template("User Panel Page/akhenbach_info.html")


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
            if question_id.isdigit():  # Ensure it's a question ID
                question = AkhenbachQuestion.query.get(int(question_id))
                if answer == "no":
                    score[question.category] += question.score_no
                elif answer == "sometimes":
                    score[question.category] += question.score_sometimes
                elif answer == "yes":
                    score[question.category] += question.score_yes

        return redirect(url_for("akhenbach_results", gender=gender, age=age, **score))

    questions = AkhenbachQuestion.query.all()
    return render_template("User Panel Page/akhenbach_questions.html", questions=questions, gender=gender, age=age)



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
    return render_template("User Panel Page/akhenbach_results.html", result_message=results, plot_url="static/images/akhenbach_plot.png")

def calculate_results(gender, age, score):
    # T-score interpretation based on gender and age group as per the provided PDF
    interpretation = ""
    t_scores = []

    # Map each category to its raw score ranges and corresponding T-scores based on gender and age
    t_score_mapping = {
        "اضطراب/افسردگی": get_t_score("اضطراب/افسردگی", score["اضطراب/افسردگی"], gender, age),
        "گوشه گیری/افسردگی": get_t_score("گوشه گیری/افسردگی", score["گوشه گیری/افسردگی"], gender, age),
        "شکایات جسمانی": get_t_score("شکایات جسمانی", score["شکایات جسمانی"], gender, age),
        "مشکلات اجتماعی": get_t_score("مشکلات اجتماعی", score["مشکلات اجتماعی"], gender, age),
        "مشکلات تفکر": get_t_score("مشکلات تفکر", score["مشکلات تفکر"], gender, age),
        "مشکلات توجه": get_t_score("مشکلات توجه", score["مشکلات توجه"], gender, age),
        "رفتار قانون شکنی": get_t_score("رفتار قانون شکنی", score["رفتار قانون شکنی"], gender, age),
        "رفتار پرخاشگرانه": get_t_score("رفتار پرخاشگرانه", score["رفتار پرخاشگرانه"], gender, age),
        "سایر مشکلات": "مقیاس سفارشی است",  # Custom category, no T-score
    }

    for category, t_score in t_score_mapping.items():
        t_scores.append(t_score)
        if t_score == "نرمال":
            interpretation += f"نمره {category} فرزند شما در محدوده نرمال قرار دارد.<br>"
        elif t_score == "مرزی":
            interpretation += f"نمره {category} فرزند شما در محدوده مرزی قرار دارد. نیاز به توجه بیشتر دارد.<br>"
        elif t_score == "بالینی":
            interpretation += f"نمره {category} فرزند شما در محدوده بالینی قرار دارد. توصیه می‌شود با یک متخصص مشورت کنید.<br>"

    # Generate the plot
    generate_plot(t_scores)

    return interpretation

import matplotlib.pyplot as plt

def generate_plot(t_scores):
    categories = [
        "اضطراب/افسردگی", "گوشه گیری/افسردگی", "شکایات جسمانی", 
        "مشکلات اجتماعی", "مشکلات تفکر", "مشکلات توجه", 
        "رفتار قانون شکنی", "رفتار پرخاشگرانه"
    ]

    # Ensure the t_scores and categories are the same length
    if len(t_scores) > len(categories):
        t_scores = t_scores[:len(categories)]
    elif len(t_scores) < len(categories):
        categories = categories[:len(t_scores)]

    # Use Matplotlib's default sans-serif font
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['font.family'] = 'sans-serif'

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(categories, t_scores, marker='o', linestyle='-', color='r', linewidth=2, markersize=8)
    
    # Adding grid
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Setting the Y-axis limits to make the plot more readable
    plt.ylim(0, 100)  # T-Score typically ranges from 0 to 100

    # Apply font to labels and title
    plt.xlabel("دسته‌بندی‌ها", fontsize=14, labelpad=15)
    plt.ylabel("T-نمره", fontsize=14, labelpad=15)
    plt.title("CBCL پروفایل T-نمره", fontsize=16, pad=20)
    
    # Rotate category labels for better readability
    plt.xticks(rotation=45, ha="right", fontsize=12)
    
    # Save the plot to a file
    plt.savefig("static/images/akhenbach_plot.png", bbox_inches='tight')  # Save the plot as an image with tight layout
    plt.close()  # Close the figure to free up memory





def get_t_score(category, raw_score, gender, age):
    # Logic for "اضطراب/افسردگی" based on gender and age group
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

    # Logic for "گوشه گیری/افسردگی" based on gender and age group
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

    # Logic for "شکایات جسمانی" based on gender and age group
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

    # Logic for "مشکلات اجتماعی" based on gender and age group
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

    # Logic for "مشکلات تفکر" based on gender and age group
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

    # Logic for "مشکلات توجه" based on gender and age group
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

    # Logic for "رفتار قانون شکنی" based on gender and age group
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

    # Logic for "رفتار پرخاشگرانه" based on gender and age group
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

    return "مقیاس سفارشی است"  # Default return for unspecified categories


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=9001,host="0.0.0.0")
