from app import db, app

# Create the database tables
with app.app_context():
    db.create_all()