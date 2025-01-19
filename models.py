from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

# User model
class User(db.Model):
    __tablename__ = "user"  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    first_last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)


# Hike model
class Hike(db.Model):
    __tablename__ = "hike"  
    id = db.Column(db.Integer, primary_key=True)
    hike_name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.String(128), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
