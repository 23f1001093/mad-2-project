from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False) 
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)
    role = db.Column(db.String(20), default='user') 
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    scores = db.relationship('Score', backref='user', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'qualification': self.qualification,
            'dob': self.dob.strftime('%Y-%m-%d') if self.dob else None,
            'role': self.role
        }

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete-orphan") 

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Subject {self.name}>'


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan") 

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subject_id': self.subject_id,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Chapter {self.name} (Subject: {self.subject_id})>'


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=datetime.utcnow)
    time_duration = db.Column(db.String(10)) 
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan") 
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan") 

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name, 
            'chapter_id': self.chapter_id,
            'date_of_quiz': self.date_of_quiz.isoformat(),
            'time_duration': self.time_duration,
            'remarks': self.remarks,
            'created_at': self.created_at.isoformat(),
            'chapter_name': self.chapter.name if self.chapter else None, # Include chapter name
            'subject_name': self.chapter.subject.name if self.chapter and self.chapter.subject else None # Include subject name
        }

    def __repr__(self):
        return f'<Quiz {self.name} (Chapter: {self.chapter_id})>'



class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(255), nullable=False) 
   
    def serialize(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_statement': self.question_statement,
            'options': [self.option1, self.option2, self.option3, self.option4],
            'correct_option': self.correct_option 
        }

    def __repr__(self):
        return f'<Question {self.id} (Quiz: {self.quiz_id})>'



class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer)
    total_possible = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'time_stamp_of_attempt': self.time_stamp_of_attempt.isoformat(),
            'total_scored': self.total_scored,
            'total_possible': self.total_possible,
            'quiz_name': self.quiz.name if self.quiz else None, 
            'user_email': self.user.email if self.user else None 
        }

    def __repr__(self):
        return f'<Score {self.id} (User: {self.user_id}, Quiz: {self.quiz_id})>'