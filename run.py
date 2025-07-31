from app import create_app, db
from models import db, User
from werkzeug.security import generate_password_hash
import os
from flask import current_app # Import current_app
from datetime import datetime
# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Explicitly push the application context
    with app.app_context():
        # Add a print to explicitly check current_app within context
        print(f"DEBUG: Inside app.app_context(). Current app is {current_app}") # Added this
        
        # Create database tables if they don't exist
        db.create_all()
        print("Database tables created/checked.")

        # Check for and create admin user if not exists
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@quizmaster.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'adminpass') # !!! Change this in production !!!

        admin_user = User.query.filter_by(email=admin_email, role='admin').first()
        if not admin_user:
            hashed_password = generate_password_hash(admin_password, method='scrypt') # Use scrypt, it's more secure
            admin_user = User(
                email=admin_email,
                password=hashed_password,
                full_name='Quiz Master Admin',
                qualification='Administrator',
                dob=datetime(2000, 1, 1),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user '{admin_email}' created with default password. PLEASE CHANGE IT!")
        else:
            print(f"Admin user '{admin_email}' already exists.")

    # Run the Flask app
    app.run(debug=True, port=5001)