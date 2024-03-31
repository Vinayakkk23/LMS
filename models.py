from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app # from app means app.py import that variable app
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64), nullable=False)

    def check_password(self, password):
        return self.passhash == check_password_hash(self.passhash, password)

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String)
    books = db.relationship("Book", back_populates="section")

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(32), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False)
    date_returned = db.Column(db.DateTime, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    section = db.relationship("Section", back_populates="books")


#create database if doesn't exist
with app.app_context():    
    db.create_all()