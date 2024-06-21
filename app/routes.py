from flask import render_template, redirect, url_for, request, session, flash
from . import create_app

app = create_app()

users = {'user@example.com': 'password'}  # مستخدم افتراضي

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' in session:
        return render_template('profile.html')
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user' in session:
        if request.method == 'POST':
            new_password = request.form['new_password']
            users[session['user']] = new_password
            flash('Password changed successfully', 'success')
            return redirect(url_for('profile'))
        return render_template('change_password.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
