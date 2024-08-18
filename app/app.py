from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for matplotlib
import matplotlib.pyplot as plt
import io
import base64

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

# Factor model
class Factor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='factor', lazy=True)

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
    factor_id = db.Column(db.Integer, db.ForeignKey('factor.id'), nullable=True)
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

@app.route('/start_quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'username' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('index'))
    
    quiz = db.session.get(Quiz, quiz_id)
    categories = Category.query.filter_by(quiz_id=quiz_id).all()
    
    return render_template('start_quiz.html', quiz=quiz, categories=categories)

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    session = db.session  # Access SQLAlchemy session
    quiz = session.get(Quiz, quiz_id)
    user_answers = request.form
    
    # Initialize a dictionary to hold the sum of grades for each factor
    factor_scores = {factor.name: 0 for factor in session.query(Factor).all()}
    
    # Loop through the user's answers and calculate the scores
    for key, selected_option_id in user_answers.items():
        if key.startswith('question_'):
            question_id_str = key.split('_')[1]
            try:
                question_id = int(question_id_str)
            except ValueError:
                continue
            
            question = session.get(Question, question_id)
            if question is None:
                continue
            
            selected_option = session.get(Option, int(selected_option_id))
            if selected_option is None:
                continue

            if question.factor is not None:
                factor_scores[question.factor.name] += selected_option.grade
            else:
                print(f"Question ID {question_id} has no associated factor.")
    
    # Plotting the results
    fig, ax = plt.subplots(figsize=(10, 6))
    t_scores = []
    factors = []
    results = {}
    for factor_name, raw_score in factor_scores.items():
        t_score, interpretation = determine_t_score_and_interpretation(factor_name, raw_score, quiz)
        results[factor_name] = {'raw_score': raw_score, 't_score': t_score, 'interpretation': interpretation}
        t_scores.append(t_score)
        factors.append(factor_name)

    ax.barh(factors, t_scores, color='skyblue')
    ax.set_xlabel('T-Score')
    ax.set_title('Quiz Results by Factor')
    ax.axvline(x=65, color='orange', linestyle='--', label='Borderline (65)')
    ax.axvline(x=70, color='red', linestyle='--', label='Clinical (70)')
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')

    return render_template('quiz_results.html', results=results, image_base64=image_base64)


def determine_t_score_and_interpretation(factor_name, raw_score, quiz):
    # Example mapping based on typical psychological assessment T-scores.
    t_score_mapping = {
        'Anxiety/Depression': [
            (30, 50),  # raw_score <= 30 -> T-score 50
            (60, 65),  # raw_score <= 60 -> T-score 65
            (80, 70),  # raw_score <= 80 -> T-score 70
            (100, 75), # raw_score <= 100 -> T-score 75
        ],
        'Withdrawn/Depressed': [
            (10, 50),
            (20, 60),
            (30, 70),
            (40, 80),
        ],
        'Somatic Complaints': [
            (5, 50),
            (15, 60),
            (25, 70),
            (35, 80),
        ],
        'Social Problems': [
            (8, 50),
            (16, 60),
            (24, 70),
            (32, 80),
        ],
        'Thought Problems': [
            (10, 50),
            (20, 60),
            (30, 70),
            (40, 80),
        ],
        'Attention Problems': [
            (12, 50),
            (24, 60),
            (36, 70),
            (48, 80),
        ],
        'Rule-Breaking Behavior': [
            (15, 50),
            (30, 60),
            (45, 70),
            (60, 80),
        ],
        'Aggressive Behavior': [
            (20, 50),
            (40, 60),
            (60, 70),
            (80, 80),
        ],
        'Other Problems': [
            (25, 50),
            (50, 60),
            (75, 70),
            (100, 80),
        ],
    }
    
    t_score_ranges = t_score_mapping.get(factor_name, [])
    
    for cutoff, t_score in t_score_ranges:
        if raw_score <= cutoff:
            if t_score < 65:
                interpretation = 'Normal'
            elif 65 <= t_score < 70:
                interpretation = 'Borderline'
            else:
                interpretation = 'Clinical'
            return t_score, interpretation
    
    # Default to a high T-score and "Clinical" interpretation if no range is matched
    return 90, 'Clinical'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8080)
