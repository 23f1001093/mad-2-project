from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Quiz, Question, Score
from werkzeug.security import check_password_hash
from tasks import send_daily_reminder, generate_monthly_report, export_csv

routes = Blueprint('routes', __name__)

# ---------- Home & Auth ----------

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

# ---------- Dashboard ----------

@routes.route('/dashboard')
@login_required
def dashboard():
    scores = Score.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, scores=scores)

# ---------- Quiz Routes ----------

@routes.route('/quizzes')
@login_required
def quizzes():
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)

@routes.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions:
            selected = request.form.get(str(question.id))
            if selected == question.correct_option:
                score += 1
        new_score = Score(user_id=current_user.id, quiz_id=quiz.id, score=score)
        db.session.add(new_score)
        db.session.commit()
        flash(f'You scored {score}/{len(quiz.questions)}', 'success')
        return redirect(url_for('routes.dashboard'))
    return render_template('attempt_quiz.html', quiz=quiz)

# ---------- Celery Task Routes (Optional for manual trigger/testing) ----------

@routes.route('/send_reminders')
@login_required
def trigger_send_reminders():
    send_daily_reminder.delay()
    flash("Reminder task triggered.", "info")
    return redirect(url_for('routes.dashboard'))

@routes.route('/generate_reports')
@login_required
def trigger_generate_reports():
    generate_monthly_report.delay()
    flash("Monthly report task triggered.", "info")
    return redirect(url_for('routes.dashboard'))

@routes.route('/export_scores')
@login_required
def trigger_export_csv():
    export_csv.delay()
    flash("CSV export task triggered.", "info")
    return redirect(url_for('routes.dashboard'))
