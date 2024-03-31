from flask import Flask, render_template, redirect, url_for, request, flash

from models import db, User, Section, Book

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first() #after we got detail now its time to check whether its correct or not
        if not user:
            flash('Username does not exist!')
            return redirect(url_for('login'))
        if not user.check_password(password):
            flash('Incorrect password!')
            return redirect(url_for('login'))
        flash('Login successful!')
        return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!')
        else:
            new_user = User(username=username, name=name, passhash=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
    return render_template('register.html')


