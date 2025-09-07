#!/usr/bin/env python3
"""
Setup script for EcoEnergy Dashboard
This script initializes the database, trains ML models, and prepares the application
"""

import os
import sys
import sqlite3
from models.data_processor import DataProcessor
from models.ml_models import MLModels
from models.gamification import GamificationEngine

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/images',
        'static/css',
        'static/js',
        'templates',
        'models',
        'data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def initialize_database():
    """Initialize the SQLite database"""
    print("\nInitializing database...")
    
    conn = sqlite3.connect('energy_app.db')
    cursor = conn.cursor()
    
    # Create users table
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
    
    # Create user_badges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            badge_type INTEGER,
            earned_date DATE,
            daily_consumption REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create leaderboard table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            week_start DATE,
            avg_daily_consumption REAL,
            avg_daily_emissions REAL,
            total_points INTEGER,
            rank_position INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def check_dataset():
    """Check if dataset exists"""
    dataset_path = 'data/total_dataset.csv'
    if os.path.exists(dataset_path):
        print(f"Dataset found: {dataset_path}")
        return True
    else:
        print(f"Dataset not found: {dataset_path}")
        print("Please ensure your dataset is placed in the data/ directory")
        return False

def train_models():
    """Train ML models if dataset is available"""
    print("\nTraining ML models...")
    
    try:
        # Initialize data processor
        data_processor = DataProcessor()
        
        if data_processor.df.empty:
            print("No data available for training models")
            return False
        
        # Initialize and train ML models
        ml_models = MLModels()
        success = ml_models.train_models(data_processor.df)
        
        if success:
            print("ML models trained successfully")
            return True
        else:
            print("Failed to train ML models")
            return False
            
    except Exception as e:
        print(f"Error training models: {e}")
        return False

def create_sample_users():
    """Create sample users for testing"""
    print("\nCreating sample users...")
    
    from werkzeug.security import generate_password_hash
    
    conn = sqlite3.connect('energy_app.db')
    cursor = conn.cursor()
    
    sample_users = [
        ('demo_user', 'demo@example.com', 'password123', 'METER_001'),
        ('eco_saver', 'eco@example.com', 'password123', 'METER_002'),
        ('green_user', 'green@example.com', 'password123', 'METER_003')
    ]
    
    for username, email, password, meter_id in sample_users:
        try:
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, email, password_hash, meter_id) 
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, meter_id))
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error creating user {username}: {e}")
    
    conn.commit()
    conn.close()

def run_eda():
    """Run EDA analysis if dataset is available"""
    print("\nRunning EDA analysis...")
    
    try:
        from eda_analysis import EDAAnalysis
        eda = EDAAnalysis()
        eda.run_complete_analysis()
        print("EDA analysis completed")
        return True
    except Exception as e:
        print(f"Error running EDA: {e}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'plotly', 'matplotlib', 'seaborn', 'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"OK {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"MISSING {package}")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main setup function"""
    print("="*60)
    print("EcoEnergy Dashboard Setup")
    print("="*60)
    
    # Check dependencies
    # if not check_dependencies():
    #     sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Initialize database
    initialize_database()
    
    # Check dataset
    dataset_available = check_dataset()
    
    # Create sample users
    create_sample_users()
    
    # Train models if dataset is available
    if dataset_available:
        train_models()
        run_eda()
    else:
        print("\nSkipping model training and EDA due to missing dataset")
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nTo start the application:")
    print("1. Ensure your dataset is in data/total_dataset.csv")
    print("2. Run: python app.py")
    print("3. Open your browser to: http://localhost:5000")
    print("\nSample login credentials:")
    print("Username: demo_user")
    print("Password: password123")
    print("="*60)

if __name__ == "__main__":
    main()