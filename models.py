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
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

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

    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(username='admin', name='Admin', is_admin=True)
        admin.password = 'admin'
        db.session.add(admin)
        db.session.commit()