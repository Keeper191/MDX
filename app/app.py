from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
import os
import subprocess
import threading
from queue import Queue

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    socketio = SocketIO(app)

    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), unique=True, nullable=False)
        password = db.Column(db.String(150), nullable=False)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    download_queue = Queue()
    progress_tracker = {}

    def download_manga(manga_url, download_folder, job_id):
        command = f'mangadex-downloader {manga_url} -d {download_folder} --save-as cbz'
        progress_tracker[job_id] = "Downloading"
        try:
            subprocess.run(command, shell=True, check=True)
            progress_tracker[job_id] = "Completed"
        except subprocess.CalledProcessError as e:
            progress_tracker[job_id] = f"Failed: {str(e)}"
        finally:
            socketio.emit('update_status', {'job_id': job_id, 'status': progress_tracker[job_id]})

    def process_queue():
        while True:
            manga_url, download_folder, job_id = download_queue.get()
            try:
                download_manga(manga_url, download_folder, job_id)
            finally:
                download_queue.task_done()

    threading.Thread(target=process_queue, daemon=True).start()

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists', 'danger')
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/', methods=['GET', 'POST'])
    @login_required
    def index():
        if request.method == 'POST':
            manga_url = request.form['manga_url']
            download_folder = '/downloads'
            
            if not os.path.exists(download_folder):
                try:
                    os.makedirs(download_folder)
                except PermissionError:
                    flash("Permission denied: unable to create download folder.", "danger")
                    return render_template('index.html')

            job_id = str(len(progress_tracker) + 1)
            download_queue.put((manga_url, download_folder, job_id))
            flash(f'Manga added to download queue. Job ID: {job_id}', 'success')
            socketio.emit('new_job', {'job_id': job_id, 'status': 'Pending'})
        
        return render_template('index.html')

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)