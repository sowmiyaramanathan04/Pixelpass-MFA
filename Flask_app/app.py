import random
import os
import io
import json
import uuid
import time
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from stegano import lsb
from PIL import Image
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import serial

# Setup Serial Communication with Arduino
ser = serial.Serial('COM9', 9600, timeout=1)  # Update with correct COM port

time.sleep(2)  # Give Arduino time to reset

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY found in .env file!")

fernet = Fernet(SECRET_KEY)
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Ensure required directories exist
os.makedirs("static/otp_images", exist_ok=True)
os.makedirs("static/dataset_images", exist_ok=True)

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fingerprint_id = db.Column(db.Integer, nullable=True)  # Fingerprint ID stored during registration

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register User (with fingerprint enrollment)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Ask Arduino to enroll fingerprint
        ser.write(b'1\n')  # Command for enrollment
        time.sleep(2)
        response = ser.readline().decode().strip()
        
        if "ID:" in response:
            fingerprint_id = int(response.split("ID:")[1].strip())
        else:
            flash("Fingerprint enrollment failed. Try again.", "danger")
            return redirect(url_for('register'))
        
        new_user = User(username=username, password=hashed_pw, fingerprint_id=fingerprint_id)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login User (Fingerprint verification required)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('fingerprint'))  # Redirect to fingerprint authentication
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

# Fingerprint Authentication
@app.route('/verify_fingerprint')
def verify_fingerprint():
    if not ser.is_open:
        ser.open()
    ser.write(b'2\n')  # Send command to Arduino to scan
    time.sleep(2)
    response = ser.readline().decode().strip()
    print(f"Fingerprint response from Arduino: {response}")  # Debugging output

    if "verified" in response.lower():
        return jsonify({'status': 'MATCHED'})
    elif "not matched" in response.lower():
        return jsonify({'status': 'NOT_MATCHED'})
    else:
        return jsonify({'status': 'WAITING', 'message': response})

# Logout User
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Steganography Page
@app.route('/steganography')
@login_required
def steganography():
    return render_template('index.html')

# Run Application
if __name__ == "__main__":  # ✅ Fixed entry point
    with app.app_context():
        db.create_all()  # Ensure database tables exist
    app.run(debug=True)
