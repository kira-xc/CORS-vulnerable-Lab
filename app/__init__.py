from flask import Flask
from flask_cors import CORS
from flask import render_template, redirect, url_for, request, session, flash
import random
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    CORS(app, resources={r"/*": {"origins": "http://atachrak.com"}}, supports_credentials=True)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    app.config['SESSION_COOKIE_SECURE'] = True  # يُفضل تفعيلها في الإنتاج
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # تعيين SameSite=None

    Session(app)
    users = {'user@example.com': 'password'}  # مستخدم افتراضي
    sample_posts = [
        {"title": "خالد الكويت ", "content": "خالد الكويت يخرج عن السيطرة"},
        {"title": "خالد الكويت ", "content": "خالد الكويت يحذف يحذف الملفات المهمة"},
        {"title": "خالد الكويت ", "content": "خالد الكويت ما يتوب "},
        {"title": "خالد الكويت ", "content": "خالد الكويت يفجرها "},
        {"title": "خالد الكويت ", "content": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Tenetur labore praesentium non ab qui eligendi dicta omnis soluta perspiciatis, libero quam quaerat nihil vitae. Aperiam veniam dolores laborum magni possimus!"},
        {"title": "Aperiam veniam dolores", "content": "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iure, architecto, saepe molestiae voluptatem tempore magni harum error doloribus unde quis corporis dicta illo accusamus rem impedit aliquam iste! Deleniti commodi magni nulla, aspernatur exercitationem voluptas sint magnam dignissimos adipisci perspiciatis repellat quibusdam corrupti minus beatae labore quae non culpa autem cupiditate pariatur dolorem voluptatum cumque quam! Molestiae alias ex eum."}
    ]

    @app.route('/')
    def index():
        if 'user' in session:
            posts = random.sample(sample_posts, k=len(sample_posts))  # منشورات عشوائية
            return render_template('index.html', posts=posts)
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
    
    return app

