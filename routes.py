from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Subject, Chapter, Quiz, Question, Score
from functools import wraps
from datetime import datetime
import os
import csv
api = Blueprint('api', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- Authentication Routes ---
@api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({'message': 'Login successful', 'user_id': user.id, 'role': user.role}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

@api.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'message': 'Unauthorized'}), 401
    return jsonify(user.serialize()), 200

@api.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    qualification = data.get('qualification')
    dob = data.get('dob')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User with this email already exists'}), 409

    hashed_password = generate_password_hash(password, method='scrypt')

    new_user = User(
        email=email,
        password=hashed_password,
        full_name=full_name,
        qualification=qualification,
        dob=datetime.strptime(dob, '%Y-%m-%d').date() if dob else None,
        role='user'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

# --- Admin API Routes
@api.route('/admin/quizzes', methods=['GET'])
@admin_required
def get_admin_quizzes():
    quizzes = Quiz.query.all()
    return jsonify({'quizzes': [q.serialize() for q in quizzes]}), 200

@api.route('/admin/subjects', methods=['GET'])
@admin_required
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([s.serialize() for s in subjects])

@api.route('/admin/subjects', methods=['POST'])
@admin_required
def add_subject():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Subject name is required'}), 400
    if Subject.query.filter_by(name=name).first():
        return jsonify({'message': 'Subject with this name already exists'}), 409
    subject = Subject(name=name, description=data.get('description'))
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.serialize()), 201

@api.route('/admin/subjects/<int:id>', methods=['PUT'])
@admin_required
def edit_subject(id):
    data = request.json
    subject = Subject.query.get_or_404(id)
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    db.session.commit()
    return jsonify(subject.serialize())

@api.route('/admin/subjects/<int:id>', methods=['DELETE'])
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.chapters:
        return jsonify({'message': 'Cannot delete subject with existing chapters'}), 400
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted'})

@api.route('/admin/chapters', methods=['GET'])
@admin_required
def get_chapters():
    chapters = Chapter.query.all()
    return jsonify([c.serialize() for c in chapters])

@api.route('/admin/subjects/<int:subject_id>/chapters', methods=['GET'])
@admin_required
def get_chapters_by_subject(subject_id):
    """Fetches all chapters for a given subject ID."""
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([c.serialize() for c in chapters])

@api.route('/admin/chapters', methods=['POST'])
@admin_required
def add_chapter():
    data = request.json
    name = data.get('name')
    subject_id = data.get('subject_id')
    description = data.get('description', '')
    if not name or not subject_id:
        return jsonify({'message': 'Chapter name and subject ID are required'}), 400
    if Chapter.query.filter_by(name=name, subject_id=subject_id).first():
        return jsonify({'message': 'Chapter with this name already exists under this subject'}), 409
    chapter = Chapter(name=name, subject_id=subject_id, description=description)
    db.session.add(chapter)
    db.session.commit()
    return jsonify(chapter.serialize()), 201

@api.route('/admin/chapters/<int:id>', methods=['PUT'])
@admin_required
def edit_chapter(id):
    data = request.json
    chapter = Chapter.query.get_or_404(id)
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    chapter.subject_id = data.get('subject_id', chapter.subject_id)
    db.session.commit()
    return jsonify(chapter.serialize())

@api.route('/admin/chapters/<int:id>', methods=['DELETE'])
@admin_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    if chapter.quizzes:
        return jsonify({'message': 'Cannot delete chapter with existing quizzes'}), 400
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({'message': 'Chapter deleted'})


# --- Quiz Management
@api.route('/admin/quizzes', methods=['POST'])
@admin_required
def add_quiz():
    data = request.json
    name = data.get('name')
    chapter_id = data.get('chapter_id')
    time_duration_str = data.get('time_duration')
    remarks = data.get('remarks')

    if not name or not chapter_id or not time_duration_str:
        return jsonify({'message': 'Quiz name, chapter ID, and duration are required'}), 400

    quiz = Quiz(
        name=name,
        chapter_id=chapter_id,
        date_of_quiz=datetime.utcnow(),
        time_duration=time_duration_str,
        remarks=remarks
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify(quiz.serialize()), 201

@api.route('/admin/quizzes/<int:id>', methods=['PUT'])
@admin_required
def edit_quiz(id):
    data = request.json
    quiz = Quiz.query.get_or_404(id)
    quiz.name = data.get('name', quiz.name)
    quiz.chapter_id = data.get('chapter_id', quiz.chapter_id)
    quiz.time_duration = data.get('time_duration', quiz.time_duration)
    quiz.remarks = data.get('remarks', quiz.remarks)
    db.session.commit()
    return jsonify(quiz.serialize())

@api.route('/admin/quizzes/<int:id>', methods=['DELETE'])
@admin_required
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    if quiz.questions:
        return jsonify({'message': 'Cannot delete quiz with existing questions'}), 400
    if quiz.scores:
        return jsonify({'message': 'Cannot delete quiz with existing scores'}), 400
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz deleted'})

@api.route('/admin/quizzes/<int:quiz_id>', methods=['GET'])
@admin_required
def get_quiz_details(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return jsonify(quiz.serialize()), 200

# --- Question Management---
@api.route('/admin/quizzes/<int:quiz_id>/questions', methods=['GET'])
@admin_required
def get_quiz_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([q.serialize() for q in questions]), 200

@api.route('/admin/quizzes/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def add_question(quiz_id):
    data = request.json
    question_statement = data.get('question_statement')
    options = data.get('options', [])
    correct_option = data.get('correct_option')

    if not all([question_statement, len(options) == 4, correct_option]):
        return jsonify({'message': 'Missing data for question'}), 400

    if correct_option not in options:
        return jsonify({'message': 'Correct option must be one of the provided options'}), 400

    question = Question(
        quiz_id=quiz_id,
        question_statement=question_statement,
        option1=options[0],
        option2=options[1],
        option3=options[2],
        option4=options[3],
        correct_option=correct_option
    )
    db.session.add(question)
    db.session.commit()
    return jsonify(question.serialize()), 201

@api.route('/admin/questions/<int:question_id>', methods=['PUT'])
@admin_required
def edit_question(question_id):
    data = request.json
    question = Question.query.get_or_404(question_id)

    question.question_statement = data.get('question_statement', question.question_statement)
    options = data.get('options', [])
    if len(options) == 4:
        question.option1 = options[0]
        question.option2 = options[1]
        question.option3 = options[2]
        question.option4 = options[3]
    question.correct_option = data.get('correct_option', question.correct_option)

    if question.correct_option not in [question.option1, question.option2, question.option3, question.option4]:
         return jsonify({'message': 'Correct option must be one of the provided options'}), 400

    db.session.commit()
    return jsonify(question.serialize()), 200

@api.route('/admin/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted'}), 200


@api.route('/quizzes', methods=['GET'])
def get_user_quizzes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    quizzes = Quiz.query.all()
    quizzes_data = []
    for quiz in quizzes:
        
        subject_name = quiz.chapter.subject.name if quiz.chapter and quiz.chapter.subject else "Unknown Subject"
        chapter_name = quiz.chapter.name if quiz.chapter else "Unknown Chapter"
        quizzes_data.append({
            'id': quiz.id,
            'name': quiz.name,
            'subject_name': subject_name,
            'chapter_name': chapter_name,
            'time_duration': quiz.time_duration,
            'remarks': quiz.remarks,
            'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d %H:%M:%S') if quiz.date_of_quiz else None
        })
    return jsonify({'quizzes': quizzes_data}), 200


@api.route('/quizzes/<int:quiz_id>/attempt', methods=['GET'])
def get_quiz_for_attempt(quiz_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    questions_for_user = []
    for q in questions:
        q_data = q.serialize()
        q_data.pop('correct_option', None)
        questions_for_user.append(q_data)

    return jsonify({
        'quiz_id': quiz.id,
        'quiz_name': quiz.name,
        'time_duration': quiz.time_duration,
        'questions': questions_for_user
    }), 200

@api.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    user_answers = data.get('answers', {})

    quiz = Quiz.query.get_or_404(quiz_id)
    questions = {q.id: q for q in Question.query.filter_by(quiz_id=quiz_id).all()}

    total_correct = 0
    total_questions = len(questions)

    for q_id_str, submitted_answer in user_answers.items():
        q_id = int(q_id_str)
        if q_id in questions:
            correct_answer = questions[q_id].correct_option
            if submitted_answer == correct_answer:
                total_correct += 1

    new_score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        time_stamp_of_attempt=datetime.utcnow(),
        total_scored=total_correct,
        total_possible=total_questions
    )
    db.session.add(new_score)
    db.session.commit()

    return jsonify({
        'message': 'Quiz submitted successfully',
        'score': total_correct,
        'total_questions': total_questions,
        'score_id': new_score.id
    }), 200

# --- User Score History ---
@api.route('/user/scores', methods=['GET'])
def get_user_scores():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Unauthorized'}), 401

    scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.desc()).all()
    results = []
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        results.append({
            'score_id': score.id,
            'quiz_name': quiz.name if quiz else 'Unknown Quiz',
            'scored': score.total_scored,
            'total_possible': score.total_possible,
            'attempt_date': score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(results), 200


# --- View Quiz--
@api.route('/admin/quizzes/<int:quiz_id>/results', methods=['GET'])
@admin_required
def get_quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    scores = Score.query.filter_by(quiz_id=quiz_id).all()
    results = []
    for score in scores:
        user = User.query.get(score.user_id)
        results.append({
            'user_name': user.full_name if user else 'Unknown User',
            'user_email': user.email if user else 'N/A',
            'scored': score.total_scored,
            'total_possible': score.total_possible,
            'attempt_date': score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({
        'quiz_name': quiz.name,
        'results': results
    }), 200



@api.route('/admin/search', methods=['GET'])
@admin_required
def admin_search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'message': 'Search query is required'}), 400

    results = {}
    users = User.query.filter(
        (User.full_name.ilike(f'%{query}%')) |
        (User.email.ilike(f'%{query}%'))
    ).all()
    results['users'] = [u.serialize() for u in users]
    subjects = Subject.query.filter(
        (Subject.name.ilike(f'%{query}%')) |
        (Subject.description.ilike(f'%{query}%'))
    ).all()
    results['subjects'] = [s.serialize() for s in subjects]
    quizzes = Quiz.query.filter(
        (Quiz.name.ilike(f'%{query}%')) |
        (Quiz.remarks.ilike(f'%{query}%'))
    ).all()
    results['quizzes'] = [q.serialize() for q in quizzes]

    return jsonify(results), 200


# --- Score Export--
@api.route('/admin/export-scores', methods=['POST'])
@admin_required
def export_scores():
    try:
        scores = Score.query.all()
        users = {u.id: u for u in User.query.all()}
        quizzes = {q.id: q for q in Quiz.query.all()}
        chapters = {c.id: c for c in Chapter.query.all()}
        subjects = {s.id: s for s in Subject.query.all()}

        static_folder = os.path.join(current_app.root_path, 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f'all_quiz_scores_{timestamp}.csv'
        filepath = os.path.join(static_folder, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Score ID', 'User Email', 'User Full Name', 'Quiz Name',
                'Subject Name', 'Chapter Name', 'Score', 'Total Possible', 'Attempt Date'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for score in scores:
                user = users.get(score.user_id)
                quiz = quizzes.get(score.quiz_id)

                user_email = user.email if user else 'N/A'
                user_full_name = user.full_name if user else 'N/A'
                quiz_name = quiz.name if quiz else 'N/A'
                time_duration = quiz.time_duration if quiz else 'N/A'
                remarks = quiz.remarks if quiz else 'N/A'

                subject_name = 'N/A'
                chapter_name = 'N/A'

                if quiz and quiz.chapter_id:
                    chapter = chapters.get(quiz.chapter_id)
                    chapter_name = chapter.name if chapter else 'N/A'
                    if chapter and chapter.subject_id:
                        subject = subjects.get(chapter.subject_id)
                        subject_name = subject.name if subject else 'N/A'

                writer.writerow({
                    'Score ID': score.id,
                    'User Email': user_email,
                    'User Full Name': user_full_name,
                    'Quiz Name': quiz_name,
                    'Subject Name': subject_name,
                    'Chapter Name': chapter_name,
                    'Score': score.total_scored,
                    'Total Possible': score.total_possible,
                    'Attempt Date': score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M:%S')
                })
        return jsonify({'message': 'Scores exported successfully!', 'filepath': f'/static/{filename}'}), 200

    except Exception as e:
        current_app.logger.error(f"Error exporting scores: {e}")
        return jsonify({'error':'An internal server error occurred during export.'}, 500)