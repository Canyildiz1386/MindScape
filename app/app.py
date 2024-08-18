from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    province = db.Column(db.String(150), nullable=True)
    education = db.Column(db.String(150), nullable=True)
    age = db.Column(db.String(10), nullable=True)
    gender = db.Column(db.String(50), nullable=True)

# Quiz model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)  # Time limit in minutes
    categories = db.relationship('Category', backref='quiz', lazy=True)

# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    questions = db.relationship('Question', backref='category', lazy=True)

# Question model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True)

# Option model
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    grade = db.Column(db.Float, nullable=False)  # Grade for this option
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

@app.route('/')
def index():
    username = session.get('username')
    is_admin = session.get('is_admin', False)
    quizzes = Quiz.query.all()  # Fetch all quizzes from the database
    return render_template('index.html', username=username, is_admin=is_admin, quizzes=quizzes)

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    verify_password = request.form.get('verify_password')

    if password != verify_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('index'))

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists!', 'error')
        return redirect(url_for('index'))

    is_admin = not User.query.first()  # First user to sign up becomes the admin

    new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    flash('Signup successful! Please log in.', 'success')
    
    session['user_id'] = new_user.id
    session['username'] = new_user.username
    session['is_admin'] = new_user.is_admin
    
    return redirect(url_for('user_panel'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Invalid username or password!', 'error')
        return redirect(url_for('index'))

    session['user_id'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    flash('Login successful!', 'success')
    
    return redirect(url_for('user_panel'))

@app.route('/user_panel')
def user_panel():
    if 'username' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('index'))

    if session.get('is_admin'):
        return redirect(url_for('admin_panel'))

    user = User.query.get(session['user_id'])
    return render_template('user_panel.html', 
                           username=session['username'], 
                           is_admin=session['is_admin'], 
                           province=user.province, 
                           education=user.education, 
                           age=user.age, 
                           gender=user.gender)

@app.route('/admin_panel')
def admin_panel():
    if 'username' not in session or not session.get('is_admin'):
        flash('Admin access required.', 'error')
        return redirect(url_for('index'))
    
    # Fetch counts
    user_count = User.query.count()
    quiz_count = Quiz.query.count()
    question_count = Question.query.count()

    # Fetch all quizzes
    quizzes = Quiz.query.all()

    return render_template('admin_panel.html', 
                           user_count=user_count, 
                           quiz_count=quiz_count, 
                           question_count=question_count, 
                           quizzes=quizzes)

@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if 'username' not in session or not session.get('is_admin'):
        flash('Admin access required.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get quiz details
        title = request.form.get('quiz_title')
        description = request.form.get('quiz_description')
        time_limit = request.form.get('quiz_time')
        
        # Create quiz
        quiz = Quiz(title=title, description=description, time_limit=int(time_limit))
        db.session.add(quiz)
        db.session.flush()  # Flush to get the quiz ID

        # Add categories
        category_names = request.form.getlist('category_name[]')
        for cat_name in category_names:
            category = Category(name=cat_name, quiz_id=quiz.id)
            db.session.add(category)
            db.session.flush()  # Flush to get the category ID
            
            # Add questions
            questions = request.form.getlist(f'question_text_{cat_name}[]')
            for q_text in questions:
                question = Question(text=q_text, category_id=category.id)
                db.session.add(question)
                db.session.flush()  # Flush to get the question ID
                
                # Add options
                options = request.form.getlist(f'options_{q_text}[]')
                for option_text in options:
                    grade = 0 if 'no' in option_text.lower() else 1 if 'sometimes' in option_text.lower() else 2
                    option = Option(text=option_text, grade=grade, question_id=question.id)
                    db.session.add(option)
        
        db.session.commit()
        flash('Quiz added successfully!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('add_quiz.html')

@app.route('/update_user_info', methods=['POST'])
def update_user_info():
    if 'user_id' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('index'))

    user = User.query.get(session['user_id'])

    user.province = request.form.get('province')
    user.education = request.form.get('education')
    user.age = request.form.get('age')
    user.gender = request.form.get('gender')

    db.session.commit()

    flash('User information updated successfully!', 'success')
    return redirect(url_for('user_panel'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))
@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    # Logic to handle quiz submission and grading

    flash('Quiz submitted successfully!', 'success')
    return redirect(url_for('user_panel'))
@app.route('/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'username' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('index'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    categories = Category.query.filter_by(quiz_id=quiz_id).all()
    
    return render_template('start_quiz.html', quiz=quiz, categories=categories)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True,port=8080)
