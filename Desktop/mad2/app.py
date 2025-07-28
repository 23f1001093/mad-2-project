from flask import Flask
from models import db, login_manager
from routes import routes

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
login_manager.init_app(app)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
