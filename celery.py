from celery import Celery
from flask import current_app
from flask_mail import Mail, Message
from datetime import datetime
from io import StringIO
import csv
from models import db, User, Quiz, Score
from app import create_app

# Setup Flask context for Celery
flask_app = create_app()
celery = Celery(__name__, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

mail = Mail(flask_app)

@celery.task()
def send_score_email(user_id, quiz_id):
    with flask_app.app_context():
        user = User.query.get(user_id)
        quiz = Quiz.query.get(quiz_id)
        score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()

        if not user or not quiz or not score:
            return "User, quiz, or score not found"

        msg = Message('Quiz Score Notification',
                      sender=flask_app.config['MAIL_USERNAME'],
                      recipients=[user.email])
        msg.body = f"Hello {user.username},\n\nYou have completed the quiz '{quiz.title}' and your score is {score.score}.\n\nThanks,\nQuiz Master Team"

        try:
            mail.send(msg)
            return "Email sent successfully"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

@celery.task()
def export_scores():
    with flask_app.app_context():
        scores = Score.query.all()

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Username', 'Quiz Title', 'Score'])

        for score in scores:
            writer.writerow([
                score.user.username,
                score.quiz.title,
                score.score
            ])

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'scores_export_{timestamp}.csv'

        with open(filename, 'w', newline='') as f:
            f.write(output.getvalue())

        return filename
