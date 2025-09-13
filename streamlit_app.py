import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from werkzeug.security import generate_password_hash, check_password_hash
from models.data_processor import DataProcessor
from models.ml_models import MLModels
from models.gamification import GamificationEngine

# Page config
st.set_page_config(
    page_title="🌱 EcoEnergy Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem 0;
}
.badge-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
}
.leaderboard-header {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    data_processor = DataProcessor()
    ml_models = MLModels()
    gamification = GamificationEngine()
    return data_processor, ml_models, gamification

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

def authenticate_user(username, password):
    conn = sqlite3.connect('energy_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data and check_password_hash(user_data[3], password):
        return {"id": user_data[0], "username": user_data[1], "email": user_data[2], "meter_id": user_data[4]}
    return None

def register_user(username, email, password, meter_id):
    conn = sqlite3.connect('energy_app.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    if cursor.fetchone():
        conn.close()
        return False
    
    password_hash = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, email, password_hash, meter_id) VALUES (?, ?, ?, ?)',
                  (username, email, password_hash, meter_id))
    conn.commit()
    conn.close()
    return True

def login_page():
    st.title("🌱 EcoEnergy Dashboard")
    st.subheader("Login to your account")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = authenticate_user(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    st.markdown("---")
    if st.button("Don't have an account? Register here"):
        st.session_state.show_register = True
        st.rerun()

def register_page():
    st.title("🌱 Register New Account")
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        meter_id = st.text_input("Meter ID")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if register_user(username, email, password, meter_id):
                st.success("Registration successful! Please login.")
                st.session_state.show_register = False
                st.rerun()
            else:
                st.error("Username or email already exists")
    
    if st.button("Back to Login"):
        st.session_state.show_register = False
        st.rerun()

def dashboard_page():
    data_processor, ml_models, gamification = init_components()
    user = st.session_state.user
    
    st.title(f"🌱 Welcome, {user['username']}!")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox("Select Page", ["Dashboard", "Badges", "Leaderboard", "Suggestions", "About"])
        
        if st.button("Logout"):
            del st.session_state.user
            st.rerun()
    
    if page == "Dashboard":
        show_dashboard(data_processor, ml_models, gamification, user)
    elif page == "Badges":
        show_badges(gamification, user)
    elif page == "Leaderboard":
        show_leaderboard(gamification, user)
    elif page == "Suggestions":
        show_suggestions(ml_models, user)
    elif page == "About":
        show_about()

def show_dashboard(data_processor, ml_models, gamification, user):
    # Welcome Section
    st.markdown(f"""
    <div class="metric-card">
        <h2>🏠 Welcome back, {user['username']}!</h2>
        <p>Here's your energy consumption overview for today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics Cards
    today_usage = data_processor.get_today_usage(user['meter_id'])
    today_emissions = today_usage * 0.82 if today_usage else 0
    badge = gamification.get_user_badge(user['id'])
    est_cost = (today_usage or 0) * 8.5
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #007bff, #0056b3); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <h3>⚡</h3>
            <h5>Today's Usage</h5>
            <h3>{:.2f} kWh</h3>
        </div>
        """.format(today_usage or 0), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dc3545, #c82333); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <h3>💨</h3>
            <h5>CO₂ Emissions</h5>
            <h3>{:.2f} kg</h3>
        </div>
        """.format(today_emissions), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffc107, #e0a800); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <h3>🏅</h3>
            <h5>Current Badge</h5>
            <h3>{}</h3>
        </div>
        """.format(badge or "No Badge"), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #28a745, #1e7e34); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <h3>₹</h3>
            <h5>Est. Cost</h5>
            <h3>₹{:.2f}</h3>
        </div>
        """.format(est_cost), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Energy Consumption Trend")
        chart_data = data_processor.get_chart_data(user['meter_id'], 'daily')
        if chart_data:
            df = pd.DataFrame(chart_data)
            # Use correct column names from chart_data
            x_col = 'labels' if 'labels' in df.columns else 'date'
            fig = px.line(df, x=x_col, y='consumption', title='Daily Energy Consumption (Last 30 Days)')
            fig.update_traces(line_color='#007bff')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No consumption data available")
    
    with col2:
        st.subheader("🍃 Carbon Footprint")
        if chart_data:
            df = pd.DataFrame(chart_data)
            x_col = 'labels' if 'labels' in df.columns else 'date'
            if 'emissions' not in df.columns:
                df['emissions'] = df['consumption'] * 0.82
            fig = px.bar(df, x=x_col, y='emissions', title='Daily CO₂ Emissions')
            fig.update_traces(marker_color='#dc3545')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No emissions data available")
    
    # Forecast Section
    st.subheader("🔮 7-Day Forecast")
    forecast_data = ml_models.get_forecast(user['meter_id'])
    if forecast_data:
        df_forecast = pd.DataFrame(forecast_data)
        # Use correct column names from forecast_data
        x_col = 'dates' if 'dates' in df_forecast.columns else 'date'
        y_col = 'forecast' if 'forecast' in df_forecast.columns else 'predicted_consumption'
        fig = px.line(df_forecast, x=x_col, y=y_col, title='Energy Consumption Forecast')
        fig.update_traces(line=dict(color='#28a745', dash='dash'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No forecast data available")
    
    # Quick Actions
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #ffeaa7;">
            <h3>💡</h3>
            <h5>Get Suggestions</h5>
            <p>Discover personalized tips to reduce your energy consumption.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #d4edda; padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #c3e6cb;">
            <h3>🏆</h3>
            <h5>Check Leaderboard</h5>
            <p>See how you rank against other eco-conscious users.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #cce5ff; padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #b3d9ff;">
            <h3>🏅</h3>
            <h5>Badge Progress</h5>
            <p>Track your achievements and unlock new badges.</p>
        </div>
        """, unsafe_allow_html=True)

def show_badges(gamification, user):
    st.header("🏆 Your Badges")
    
    current_badge = gamification.get_user_badge(user['id'])
    progress = gamification.get_badge_progress(user['id'])
    
    # Current Badge Section
    st.markdown(f"""
    <div class="badge-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🏆</div>
        <h2>{current_badge or "No Badge"}</h2>
        <p>Your current achievement level</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress Section
    if progress:
        st.subheader("📊 Progress to Next Level")
        progress_val = progress.get('progress', 0)
        st.progress(progress_val)
        st.write(f"**Goal:** {progress.get('next_goal', 'Unknown')}")
        st.write(f"**Current 7-day average:** {progress.get('current_consumption', 0):.2f} kWh/day")
    
    # Badge Categories
    st.subheader("🏅 Badge Categories")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #d4edda; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
            <div style="font-size: 3rem;">🌱</div>
            <h5 style="color: #28a745;">Eco Saver</h5>
            <p>Using less than 2 kWh per day</p>
            <span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Excellent Efficiency</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #cce5ff; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #007bff;">
            <div style="font-size: 3rem;">🌍</div>
            <h5 style="color: #007bff;">Green User</h5>
            <p>Using 2-5 kWh per day efficiently</p>
            <span style="background: #007bff; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Good Balance</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #ffc107;">
            <div style="font-size: 3rem;">🔥</div>
            <h5 style="color: #ffc107;">Carbon Heavy</h5>
            <p>Using 5-8 kWh per day</p>
            <span style="background: #ffc107; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Room for Improvement</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #e2e3e5; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #6c757d;">
            <div style="font-size: 3rem;">🏆</div>
            <h5 style="color: #6c757d;">Efficient Hero</h5>
            <p>High usage but improving</p>
            <span style="background: #6c757d; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Making Progress</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Badge History
    st.subheader("📜 Badge History (Last 30 Days)")
    badges_history = gamification.get_user_badges_history(user['id'])
    if badges_history:
        df = pd.DataFrame(badges_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No badges earned yet. Start saving energy to earn your first badge!")
    
    # Tips Section
    st.subheader("💡 Tips to Improve Your Badge")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        - ✅ Use energy-efficient appliances
        - ✅ Unplug devices when not in use
        - ✅ Optimize heating and cooling settings
        """)
    
    with col2:
        st.markdown("""
        - ✅ Use natural light during the day
        - ✅ Run appliances during off-peak hours
        - ✅ Regular maintenance of electrical systems
        """)

def show_leaderboard(gamification, user):
    # Header Section
    st.markdown("""
    <div class="leaderboard-header">
        <h2>🏆 Weekly Leaderboard</h2>
        <p>Compete with other users for the most efficient energy consumption!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # User's Rank
    user_rank = gamification.get_user_rank(user['id'])
    if user_rank:
        rank_emoji = "🥇" if user_rank.get('rank') == 1 else "🥈" if user_rank.get('rank') == 2 else "🥉" if user_rank.get('rank') == 3 else f"#{user_rank.get('rank')}"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #007bff, #0056b3); padding: 1rem; border-radius: 10px; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h5>👤 Your Current Ranking</h5>
                    <p>You are currently ranked <strong>#{user_rank.get('rank')}</strong> with <strong>{user_rank.get('points')}</strong> points this week.</p>
                </div>
                <div style="font-size: 3rem;">{rank_emoji}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Leaderboard Table
    st.subheader("🏅 Top Performers This Week")
    rankings = gamification.get_leaderboard()
    
    if rankings:
        # Create enhanced dataframe
        df = pd.DataFrame(rankings)
        
        # Add badge column
        def get_badge_emoji(consumption):
            if consumption < 2:
                return "🌱 Eco Saver"
            elif consumption < 5:
                return "🌍 Green User"
            elif consumption < 8:
                return "🔥 Carbon Heavy"
            else:
                return "🏆 Efficient Hero"
        
        df['Badge'] = df['avg_consumption'].apply(get_badge_emoji)
        df['Rank'] = df.index + 1
        
        # Display with styling
        st.dataframe(
            df[['Rank', 'username', 'avg_consumption', 'avg_emissions', 'points', 'Badge']].rename(columns={
                'username': 'User',
                'avg_consumption': 'Avg Daily Consumption (kWh)',
                'avg_emissions': 'Avg Daily Emissions (kg CO₂)',
                'points': 'Points'
            }),
            use_container_width=True
        )
        
        # Leaderboard Chart
        st.subheader("📊 Top 10 Users - Weekly Performance")
        top_10 = df.head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Avg Daily Consumption (kWh)',
            x=top_10['username'],
            y=top_10['avg_consumption'],
            marker_color='#007bff'
        ))
        
        fig.add_trace(go.Bar(
            name='Points',
            x=top_10['username'],
            y=top_10['points'],
            yaxis='y2',
            marker_color='#28a745'
        ))
        
        fig.update_layout(
            title='Top 10 Users Performance',
            xaxis_title='Users',
            yaxis=dict(title='Consumption (kWh)', side='left'),
            yaxis2=dict(title='Points', side='right', overlaying='y'),
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No leaderboard data available yet")
    
    # Scoring System
    st.subheader("ℹ️ How Scoring Works")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Point Calculation:**
        - ⭐ Lower consumption = Higher points
        - ⭐ Points = (10 - avg_daily_consumption) × 10
        - ⭐ Minimum 0 points, maximum 100 points
        """)
    
    with col2:
        st.markdown("""
        **Weekly Reset:**
        - 📅 Leaderboard resets every Monday
        - 📅 Based on 7-day rolling average
        - 📅 Encourages consistent improvement
        """)

def show_suggestions(ml_models, user):
    st.header("💡 Energy Saving Suggestions")
    
    suggestions = ml_models.get_personalized_suggestions(user['meter_id'])
    savings = ml_models.calculate_potential_savings(user['meter_id'])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Personalized Recommendations")
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"**{i}.** {suggestion}")
        else:
            st.info("No suggestions available at the moment")
    
    with col2:
        st.subheader("💰 Potential Savings")
        if savings:
            st.metric("Monthly Savings", f"${savings.get('monthly', 0):.2f}")
            st.metric("CO₂ Reduction", f"{savings.get('co2', 0):.2f} kg")
        else:
            st.info("No savings data available")

def show_about():
    st.header("ℹ️ About EcoEnergy Dashboard")
    
    st.markdown("""
    ## 🌱 Mission
    EcoEnergy Dashboard helps you monitor and reduce your energy consumption through:
    
    - **Real-time Monitoring**: Track your daily energy usage
    - **ML Predictions**: Forecast future consumption patterns
    - **Gamification**: Earn badges and compete with others
    - **Smart Suggestions**: Get personalized energy-saving tips
    
    ## 🛠️ Technology Stack
    - **Frontend**: Streamlit
    - **Backend**: Python, SQLite
    - **ML**: Scikit-learn, Pandas, NumPy
    - **Visualization**: Plotly
    
    ## 🏆 Badge System
    - **Energy Saver**: Consume less than 50 kWh daily
    - **Eco Warrior**: Maintain low consumption for a week
    - **Carbon Neutral**: Achieve minimal carbon footprint
    
    ---
    **Built with ❤️ for a sustainable future** 🌍
    """)

def main():
    init_db()
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    
    # Demo credentials info
    if not st.session_state.user:
        st.sidebar.info("Demo Credentials:\nUsername: demo_user\nPassword: password123")
    
    # Route to appropriate page
    if st.session_state.user:
        dashboard_page()
    elif st.session_state.get('show_register', False):
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()