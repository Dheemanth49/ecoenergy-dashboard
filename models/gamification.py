import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class GamificationEngine:
    def __init__(self):
        self.badges = {
            0: {'name': 'Eco Saver', 'emoji': '🌱', 'description': 'Using less than 2 kWh/day', 'color': '#4CAF50'},
            1: {'name': 'Green User', 'emoji': '🌍', 'description': 'Using 2-5 kWh/day efficiently', 'color': '#2196F3'},
            2: {'name': 'Carbon Heavy', 'emoji': '🔥', 'description': 'Using 5-8 kWh/day', 'color': '#FF9800'},
            3: {'name': 'Efficient Hero', 'emoji': '🏆', 'description': 'High usage but improving', 'color': '#9C27B0'}
        }
        self.init_gamification_db()
    
    def init_gamification_db(self):
        """Initialize gamification database tables"""
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        # User badges table
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
        
        # Leaderboard table
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
    
    def calculate_daily_consumption(self, user_id, date=None):
        """Calculate daily consumption for a user"""
        if date is None:
            date = datetime.now().date()
        
        # In a real implementation, this would query the actual energy data
        # For demo purposes, we'll simulate realistic consumption patterns
        np.random.seed(user_id + date.day)
        base_consumption = np.random.uniform(1.5, 8.0)
        
        # Add some weekly patterns
        if date.weekday() in [5, 6]:  # Weekend
            base_consumption *= 1.2
        
        return round(base_consumption, 2)
    
    def determine_badge(self, daily_consumption):
        """Determine badge based on daily consumption"""
        if daily_consumption < 2:
            return 0  # Eco Saver
        elif daily_consumption < 5:
            return 1  # Green User
        elif daily_consumption < 8:
            return 2  # Carbon Heavy
        else:
            return 3  # Efficient Hero
    
    def update_user_badge(self, user_id, date=None):
        """Update user's badge for a given date"""
        if date is None:
            date = datetime.now().date()
        
        daily_consumption = self.calculate_daily_consumption(user_id, date)
        badge_type = self.determine_badge(daily_consumption)
        
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        cursor.execute('''INSERT OR REPLACE INTO user_badges 
                        (user_id, badge_type, earned_date, daily_consumption) 
                        VALUES (?, ?, ?, ?)''',
                      (user_id, badge_type, date, daily_consumption))
        
        conn.commit()
        conn.close()
        
        return badge_type
    
    def get_user_badge(self, user_id, date=None):
        """Get user's current badge"""
        if date is None:
            date = datetime.now().date()
        
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT badge_type FROM user_badges 
                         WHERE user_id = ? AND earned_date = ?''', 
                      (user_id, date))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            badge_type = result[0]
        else:
            # Create badge for today if it doesn't exist
            badge_type = self.update_user_badge(user_id, date)
        
        return {
            'type': badge_type,
            'name': self.badges[badge_type]['name'],
            'emoji': self.badges[badge_type]['emoji'],
            'description': self.badges[badge_type]['description'],
            'color': self.badges[badge_type]['color']
        }
    
    def get_user_badges_history(self, user_id, days=30):
        """Get user's badge history"""
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        cursor.execute('''SELECT earned_date, badge_type, daily_consumption 
                         FROM user_badges 
                         WHERE user_id = ? AND earned_date BETWEEN ? AND ?
                         ORDER BY earned_date DESC''', 
                      (user_id, start_date, end_date))
        
        results = cursor.fetchall()
        conn.close()
        
        badges_history = []
        for date, badge_type, consumption in results:
            badges_history.append({
                'date': date,
                'badge': self.badges[badge_type],
                'consumption': consumption
            })
        
        return badges_history
    
    def get_badge_progress(self, user_id):
        """Calculate progress towards next badge level"""
        current_badge = self.get_user_badge(user_id)
        
        # Get last 7 days consumption
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        cursor.execute('''SELECT AVG(daily_consumption) 
                         FROM user_badges 
                         WHERE user_id = ? AND earned_date BETWEEN ? AND ?''', 
                      (user_id, start_date, end_date))
        
        result = cursor.fetchone()
        conn.close()
        
        avg_consumption = result[0] if result[0] else 5.0
        
        # Calculate progress based on current badge type
        current_type = current_badge['type']
        
        if current_type == 0:  # Eco Saver - maintain low consumption
            progress = max(0, (2 - avg_consumption) / 2 * 100)
            next_goal = "Maintain under 2 kWh/day"
        elif current_type == 1:  # Green User - try to become Eco Saver
            progress = max(0, (5 - avg_consumption) / 3 * 100)
            next_goal = "Reduce to under 2 kWh/day for Eco Saver"
        elif current_type == 2:  # Carbon Heavy - become Green User
            progress = max(0, (8 - avg_consumption) / 3 * 100)
            next_goal = "Reduce to under 5 kWh/day for Green User"
        else:  # Efficient Hero - improve efficiency
            progress = 75  # Always show some progress for motivation
            next_goal = "Continue improving efficiency"
        
        return {
            'current_consumption': avg_consumption,
            'progress_percentage': min(100, progress),
            'next_goal': next_goal
        }
    
    def update_leaderboard(self):
        """Update weekly leaderboard"""
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        # Get current week start (Monday)
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        # Get all users
        cursor.execute('SELECT id FROM users')
        users = cursor.fetchall()
        
        leaderboard_data = []
        
        for user_id, in users:
            # Calculate weekly average
            cursor.execute('''SELECT AVG(daily_consumption) 
                            FROM user_badges 
                            WHERE user_id = ? AND earned_date >= ?''', 
                          (user_id, week_start))
            
            result = cursor.fetchone()
            avg_consumption = result[0] if result[0] else self.calculate_daily_consumption(user_id)
            avg_emissions = avg_consumption * 0.82
            
            # Calculate points (lower consumption = higher points)
            points = max(0, int((10 - avg_consumption) * 10))
            
            leaderboard_data.append({
                'user_id': user_id,
                'avg_consumption': avg_consumption,
                'avg_emissions': avg_emissions,
                'points': points
            })
        
        # Sort by points (descending) and assign ranks
        leaderboard_data.sort(key=lambda x: x['points'], reverse=True)
        
        # Clear existing leaderboard for this week
        cursor.execute('DELETE FROM leaderboard WHERE week_start = ?', (week_start,))
        
        # Insert new leaderboard data
        for rank, data in enumerate(leaderboard_data, 1):
            cursor.execute('''INSERT INTO leaderboard 
                            (user_id, week_start, avg_daily_consumption, 
                             avg_daily_emissions, total_points, rank_position) 
                            VALUES (?, ?, ?, ?, ?, ?)''',
                          (data['user_id'], week_start, data['avg_consumption'],
                           data['avg_emissions'], data['points'], rank))
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self, limit=10):
        """Get current leaderboard"""
        self.update_leaderboard()  # Ensure it's up to date
        
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        cursor.execute('''SELECT u.username, l.avg_daily_consumption, 
                                l.avg_daily_emissions, l.total_points, l.rank_position
                         FROM leaderboard l
                         JOIN users u ON l.user_id = u.id
                         WHERE l.week_start = ?
                         ORDER BY l.rank_position
                         LIMIT ?''', (week_start, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        leaderboard = []
        for username, consumption, emissions, points, rank in results:
            leaderboard.append({
                'rank': rank,
                'username': username,
                'avg_consumption': round(consumption, 2),
                'avg_emissions': round(emissions, 2),
                'points': points
            })
        
        return leaderboard
    
    def get_user_rank(self, user_id):
        """Get user's current rank"""
        conn = sqlite3.connect('energy_app.db')
        cursor = conn.cursor()
        
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        
        cursor.execute('''SELECT rank_position, total_points 
                         FROM leaderboard 
                         WHERE user_id = ? AND week_start = ?''', 
                      (user_id, week_start))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'rank': result[0], 'points': result[1]}
        else:
            return {'rank': 'N/A', 'points': 0}