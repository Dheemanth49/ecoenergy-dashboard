from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from models.data_processor import DataProcessor
from models.ml_models import MLModels
from models.gamification import GamificationEngine

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, email, meter_id):
        self.id = id
        self.username = username
        self.email = email
        self.meter_id = meter_id

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('energy_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    return None

def init_db():
    conn = sqlite3.connect('energy_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            meter_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize components
data_processor = DataProcessor()
ml_models = MLModels()
gamification = GamificationEngine()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        meter_id = request.form['meter_id']
        
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            flash('Username or email already exists')
            conn.close()
            return render_template('register.html')
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password_hash, meter_id) VALUES (?, ?, ?, ?)',
                      (username, email, password_hash, meter_id))
        conn.commit()
        conn.close()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2], user_data[4])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's energy data
    user_data = data_processor.get_user_data(current_user.meter_id)
    today_usage = data_processor.get_today_usage(current_user.meter_id)
    today_emissions = today_usage * 0.82 if today_usage else 0
    
    # Get user's badge
    badge = gamification.get_user_badge(current_user.id)
    
    return render_template('dashboard.html', 
                         today_usage=today_usage,
                         today_emissions=today_emissions,
                         badge=badge)

@app.route('/badges')
@login_required
def badges():
    user_badges = gamification.get_user_badges_history(current_user.id)
    current_badge = gamification.get_user_badge(current_user.id)
    progress = gamification.get_badge_progress(current_user.id)
    
    return render_template('badges.html', 
                         badges=user_badges,
                         current_badge=current_badge,
                         progress=progress)

@app.route('/leaderboard')
@login_required
def leaderboard():
    rankings = gamification.get_leaderboard()
    user_rank = gamification.get_user_rank(current_user.id)
    
    return render_template('leaderboard.html', 
                         rankings=rankings,
                         user_rank=user_rank)

@app.route('/suggestions')
@login_required
def suggestions():
    user_suggestions = ml_models.get_personalized_suggestions(current_user.meter_id)
    potential_savings = ml_models.calculate_potential_savings(current_user.meter_id)
    
    return render_template('suggestions.html', 
                         suggestions=user_suggestions,
                         savings=potential_savings)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/chart_data')
@login_required
def chart_data():
    chart_type = request.args.get('type', 'daily')
    data = data_processor.get_chart_data(current_user.meter_id, chart_type)
    return jsonify(data)

@app.route('/api/forecast')
@login_required
def forecast():
    forecast_data = ml_models.get_forecast(current_user.meter_id)
    return jsonify(forecast_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)