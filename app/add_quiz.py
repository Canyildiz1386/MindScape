from app import db, Quiz, Category, Question, Option, app

# Ensure this code runs within the application context
with app.app_context():
    # Create a new quiz
    new_quiz = Quiz(title='Sample Quiz', description='This is a sample quiz.', time_limit=10)
    db.session.add(new_quiz)
    db.session.flush()  # Get the quiz ID after flushing

    # Create categories
    category_1 = Category(name='Sample Category 1', quiz_id=new_quiz.id)
    category_2 = Category(name='Sample Category 2', quiz_id=new_quiz.id)
    db.session.add(category_1)
    db.session.add(category_2)
    db.session.flush()

    # Create questions for category 1
    question_1 = Question(text='What is 2 + 2?', category_id=category_1.id)
    question_2 = Question(text='What is the capital of France?', category_id=category_1.id)
    db.session.add(question_1)
    db.session.add(question_2)
    db.session.flush()

    # Add options for question 1
    option_1_1 = Option(text='3', grade=0, question_id=question_1.id)
    option_1_2 = Option(text='4', grade=2, question_id=question_1.id)
    option_1_3 = Option(text='5', grade=0, question_id=question_1.id)
    db.session.add(option_1_1)
    db.session.add(option_1_2)
    db.session.add(option_1_3)

    # Add options for question 2
    option_2_1 = Option(text='Paris', grade=2, question_id=question_2.id)
    option_2_2 = Option(text='London', grade=0, question_id=question_2.id)
    option_2_3 = Option(text='Berlin', grade=0, question_id=question_2.id)
    db.session.add(option_2_1)
    db.session.add(option_2_2)
    db.session.add(option_2_3)

    # Commit the changes to the database
    db.session.commit()

    print("Quiz added successfully!")
