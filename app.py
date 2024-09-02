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
    is_admin = db.Column(db.Boolean, default=False)  # Admin status


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


@app.route("/admin-quiz")
@login_required
def admin_quiz():
    if not current_user.is_admin:
        flash("🚫 شما اجازه دسترسی به این بخش را ندارید! 🚫", "danger")
        return redirect(url_for("home"))
    return render_template("Admin Quiz Page/adminquiz.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

