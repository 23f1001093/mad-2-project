from celery import Celery
from flask import current_app
from flask_mail import Mail, Message
from datetime import datetime
import csv
from io import StringIO
from models import db, User, Quiz, Score
from app import create_app

# Setup Flask context for Celery
flask_app = create_app()
celery = Celery(__name__, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

mail = Mail(flask_app)

@celery.task
def send_daily_reminder():
    with flask_app.app_context():
        users = User.query.all()
        for user in users:
            if user.email:
                msg = Message(
                    subject="Your Daily Quiz Reminder!",
                    sender="noreply@quizmaster.com",
                    recipients=[user.email],
                    body=f"Hello {user.username},\nDon't forget to attempt today's quiz!"
                )
                mail.send(msg)

@celery.task
def generate_monthly_report():
    with flask_app.app_context():
        users = User.query.all()
        for user in users:
            user_scores = Score.query.filter_by(user_id=user.id).all()
            total = sum([s.score for s in user_scores])
            msg = Message(
                subject="Your Monthly Report",
                sender="noreply@quizmaster.com",
                recipients=[user.email],
                body=f"Hello {user.username},\nYour total score this month is {total}."
            )
            mail.send(msg)

@celery.task
def export_csv():
    with flask_app.app_context():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['User', 'Quiz', 'Score', 'Timestamp'])

        all_scores = Score.query.all()
        for s in all_scores:
            user = User.query.get(s.user_id)
            quiz = Quiz.query.get(s.quiz_id)
            writer.writerow([user.username, quiz.title, s.score, s.timestamp])

        output.seek(0)
        with open('exported_scores.csv', 'w') as f:
            f.write(output.read())
