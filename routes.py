from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, flash, session


from models import db, User, Section, Book

from app import app

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner

@app.route('/')
@auth_required
def index():
    return render_template('index.html', user=User.query.get(session['user_id']))


@app.route('/profile')
@auth_required
def profile():
    return render_template('profile.html', user=User.query.get(session['user_id']))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('User does not exist!')
            return redirect(url_for('login'))
        if not user.check_password(password):
            flash('Incorrect password!')
            return redirect(url_for('login'))
        flash('Login successful!')
        session['user_id'] = user.id  # Indentation corrected here
        return redirect(url_for('index'))
    
    # Return something for GET requests
    return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        if username == '' or name == '' or password == '':
            flash('Please fill in all fields!')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!')
            return redirect(url_for('register'))
        else:
            # Instead of passing password directly to passhash, use the password setter method
            new_user = User(username=username, name=name)
            new_user.password = password  # This line will automatically hash the password
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  #this removes the login id
