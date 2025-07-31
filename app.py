from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_cors import CORS
from config import Config
import os
from models import db

# Initialize extensions
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    print(f"DEBUG: db.init_app(app) called. app is {app}")
    # Note: Your routes.py uses a custom session-based auth, not Flask-Login.
    # The login_manager here is initialized but not actively used by your current routes.
    login_manager.init_app(app)
    mail.init_app(app)

    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    print("DEBUG: CORS extension initialized successfully with specific origins.")

    # Import and register routes (blueprints)
    from routes import api as api_blueprint
    
    # --- THIS LINE HAS BEEN CORRECTED ---
    # Register the blueprint with the correct URL prefix that the frontend is expecting.
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Serve static files from the 'exports' directory
    @app.route('/exports/<filename>')
    def download_export(filename):
        return send_from_directory(os.path.join(app.root_path, 'exports'), filename, as_attachment=True)

    return app
