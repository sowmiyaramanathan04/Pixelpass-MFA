PixelPass: Multi-Factor Authentication using Image Steganography
----------------------------------------------------
Overview
PixelPass is a secure multi-factor authentication (MFA) system combining traditional credentials, biometric verification, and image-based OTP validation. It embeds an encrypted one-time password (OTP) into an image via steganography, providing a hidden layer of protection against interception.

First Prize Winner at TechHacks Hackathon (₹5000 cash prize)

Key Features
-------------------------------------------------------
Secure username/password authentication with bcrypt hashing

Fingerprint verification via Arduino Uno and R307 sensor

Time-based OTP generation and Fernet encryption

LSB steganography for embedding OTP in images

Metadata validation (user ID, timestamp) to prevent tampering

3-minute OTP expiration to mitigate replay attacks

Tech Stack
------------------------------------------
Backend
Python (Flask)

Flask-Login, Flask-Bcrypt, Flask-SQLAlchemy

Frontend
-----------------------------------------------
HTML, CSS, JavaScript

Security & Processing
------------------------------------------------
Stegano (LSB steganography)

Cryptography (Fernet symmetric encryption)

Pillow (image processing)

piexif (metadata handling)

Hardware
--------------------------------------------------
Arduino Uno

R307 Fingerprint Sensor

System Workflow
-------------------------------------------------------
Login: User enters credentials, verified via bcrypt hash comparison.

Biometrics: Fingerprint scanned and matched via Arduino/R307.

OTP Generation: Random OTP encrypted with Fernet, embedded in image via steganography, tagged with user ID and timestamp.

Validation: User uploads image; system extracts, decrypts, and verifies OTP + metadata within 3 minutes.

All factors must pass for successful authentication.

Project Structure
----------------------------------------------------
PixelPass/
│
├── app.py
├── users.db
├── requirements.txt
│
├── templates/
├── static/
│ ├── otp_images/
│ ├── dataset_images/
│ └── screenshots/
│
└── Arduino/
└── fingerprint_code.ino

Hardware Setup
---------------------------------------------------
Connect R307 Fingerprint Sensor to Arduino Uno:

R307 Pin	Arduino Pin
VCC	5V
GND	GND
TX	Pin 2
RX	Pin 3

Installation & Setup
-----------------------------------------------------------
Clone the repository:

bash
git clone <repository-link>
cd PixelPass
Create virtual environment:

bash
python -m venv venv
 Windows: venv\Scripts\activate
 macOS/Linux: source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Generate Fernet key and create .env:

text
SECRET_KEY=your_generated_fernet_key_here
Run in Python: from cryptography.fernet import Fernet; print(Fernet.generate_key())

Initialize database:

bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
Run application:

bash
python app.py

Use Cases
---------------------------------------------------------------
Secure enterprise login systems

Banking and financial authentication

Confidential data access

Multi-layer identity verification

My Contributions
-----------------------------------------------------------------
Designed MFA workflow integrating biometrics and steganography

Implemented OTP encryption (Fernet) and LSB steganography

Developed Flask backend logic and security validation

Integrated metadata tampering detection

Note: Team project—code reflects my primary contributions to authentication and OTP mechanisms.
