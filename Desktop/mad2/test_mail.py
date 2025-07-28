from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '23f1001093@ds.study.iitm.ac.in'
app.config['MAIL_PASSWORD'] = 'jrbnfgdgpgwpjnlf'
app.config['MAIL_DEFAULT_SENDER'] = '23f1001093@ds.study.iitm.ac.in'

mail = Mail(app)

# Send a test email
with app.app_context():
    msg = Message(subject='Test Email from Flask',
                  recipients=['23f1001093@ds.study.iitm.ac.in'],  # 🔁 change to your email
                  body='This is a test email sent from Flask using Flask-Mail.')
    mail.send(msg)
    print("✅ Test email sent.")

