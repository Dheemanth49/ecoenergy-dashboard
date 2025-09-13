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
    initial_sidebar_state="collapsed"
)

# App title
st.markdown("""
<div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
    <h1 style="font-size: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0;">🌱 EcoEnergy Dashboard</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 1.2rem; margin: 0.5rem 0 0 0;">Smart Energy Management & Carbon Footprint Tracking</p>
</div>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 50%, #0c0c0c 100%);
    background-attachment: fixed;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1d391kg {display: none;}
.css-1lcbmhc {margin-left: 0 !important;}

/* Enhanced metric cards */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin: 0.8rem 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2), 0 5px 15px rgba(0,0,0,0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.15);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
}

.metric-card:hover::before {
    left: 100%;
}

.metric-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0,0,0,0.3), 0 10px 25px rgba(0,0,0,0.15);
}

/* Navbar styling */
.navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.15);
}

.nav-item {
    display: inline-block;
    margin: 0 1rem;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    color: white;
    text-decoration: none;
    transition: all 0.3s ease;
    cursor: pointer;
    font-weight: 500;
}

.nav-item:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-2px);
}

.nav-item.active {
    background: rgba(255,255,255,0.3);
    font-weight: 600;
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin-right: 2rem;
}

.nav-logout {
    float: right;
    background: rgba(220,53,69,0.8);
    border: none;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.nav-logout:hover {
    background: rgba(220,53,69,1);
    transform: translateY(-2px);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* Form styling */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    color: white;
    backdrop-filter: blur(10px);
}

.stSelectbox > div > div > div {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

/* Enhanced glass cards */
.glass-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.glass-card:hover {
    background: rgba(255,255,255,0.12);
    transform: translateY(-5px);
}

/* Progress bars */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
    border-radius: 15px;
    height: 15px;
    box-shadow: 0 2px 10px rgba(79, 172, 254, 0.3);
}

/* Enhanced headers */
h1, h2, h3 {
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Dataframe styling */
.stDataFrame {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Chart containers */
.js-plotly-plot {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Metric containers */
.stMetric {
    background: rgba(255,255,255,0.08);
    padding: 1.5rem;
    border-radius: 15px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease;
}

.stMetric:hover {
    background: rgba(255,255,255,0.12);
    transform: translateY(-3px);
}

/* Animation keyframes */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeInUp 0.6s ease-out;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🌱</h1>
            <h1 style="color: white; font-weight: 700; margin-bottom: 0.5rem;">EcoEnergy Dashboard</h1>
            <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">Monitor your energy consumption sustainably</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: white; margin-bottom: 1.5rem;'>Welcome Back</h3>", unsafe_allow_html=True)
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submitted:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("⚠️ Invalid credentials")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🆕 Don't have an account? Register here", use_container_width=True):
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
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Dashboard'
    
    # Navbar with integrated navigation buttons
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
    
    with col1:
        if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'Dashboard'
            st.rerun()
    with col2:
        if st.button("🏆 Badges", key="nav_badges", use_container_width=True):
            st.session_state.current_page = 'Badges'
            st.rerun()
    with col3:
        if st.button("🏅 Leaderboard", key="nav_leaderboard", use_container_width=True):
            st.session_state.current_page = 'Leaderboard'
            st.rerun()
    with col4:
        if st.button("💡 Suggestions", key="nav_suggestions", use_container_width=True):
            st.session_state.current_page = 'Suggestions'
            st.rerun()
    with col5:
        if st.button("ℹ️ About", key="nav_about", use_container_width=True):
            st.session_state.current_page = 'About'
            st.rerun()
    with col6:
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            del st.session_state.user
            st.rerun()
    
    page = st.session_state.current_page
    
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
    st.title(f"🏠 Welcome back, {user['username']}!")
    st.write("Here's your energy consumption overview for today.")
    
    st.markdown("---")
    
    # Metrics Cards
    today_usage = data_processor.get_today_usage(user['meter_id']) or 5.69
    today_emissions = today_usage * 0.82 if today_usage else 0
    badge = gamification.get_user_badge(user['id'])
    est_cost = today_usage * 8.5
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #007bff, #0056b3); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚡</div>
            <h5 style="margin: 0.5rem 0; opacity: 0.9;">Today's Usage</h5>
            <h2 style="margin: 0; font-weight: 700;">{today_usage:.2f} kWh</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Daily Consumption</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #28a745, #20c997); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💨</div>
            <h5 style="margin: 0.5rem 0; opacity: 0.9;">CO₂ Emissions</h5>
            <h2 style="margin: 0; font-weight: 700;">{today_emissions:.2f} kg</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Carbon Footprint</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        badge_name = badge['name'] if isinstance(badge, dict) else (badge or "No Badge")
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #dc3545, #c82333); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔥</div>
            <h5 style="margin: 0.5rem 0; opacity: 0.9;">Current Badge</h5>
            <h2 style="margin: 0; font-weight: 700; white-space: nowrap;">{badge_name}</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Achievement Level</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ffc107, #e0a800); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">₹</div>
            <h5 style="margin: 0.5rem 0; opacity: 0.9;">Est. Cost</h5>
            <h2 style="margin: 0; font-weight: 700;">₹{est_cost:.2f}</h2>
            <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">Daily Expense</p>
        </div>
        """, unsafe_allow_html=True)
    
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
        <div style="background: #fff3cd; padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid #ffeaa7; color: black; height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0 0 0.5rem 0;">💡</h3>
            <h5 style="margin: 0 0 0.5rem 0;">Get Suggestions</h5>
            <p style="margin: 0; font-size: 0.9rem;">Discover personalized tips to reduce your energy consumption.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #d4edda; padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid #c3e6cb; color: black; height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0 0 0.5rem 0;">🏆</h3>
            <h5 style="margin: 0 0 0.5rem 0;">Check Leaderboard</h5>
            <p style="margin: 0; font-size: 0.9rem;">See how you rank against other eco-conscious users.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #cce5ff; padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid #b3d9ff; color: black; height: 150px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="margin: 0 0 0.5rem 0;">🏅</h3>
            <h5 style="margin: 0 0 0.5rem 0;">Badge Progress</h5>
            <p style="margin: 0; font-size: 0.9rem;">Track your achievements and unlock new badges.</p>
        </div>
        """, unsafe_allow_html=True)

def show_badges(gamification, user):
    st.header("🏆 Your Badges")
    
    current_badge = gamification.get_user_badge(user['id'])
    progress = gamification.get_badge_progress(user['id'])
    
    # Current Badge Section
    if isinstance(current_badge, dict):
        badge_name = current_badge['name']
        badge_emoji = current_badge['emoji']
        badge_desc = current_badge['description']
        badge_color = current_badge['color']
    else:
        badge_name = current_badge or "No Badge"
        badge_emoji = "🏆"
        badge_desc = "Your current achievement level"
        badge_color = "#667eea"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {badge_color}22, {badge_color}44); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{badge_emoji}</div>
        <h2 style="color: {badge_color};">{badge_name}</h2>
        <p>{badge_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress Section
    st.subheader("📊 Progress to Next Level")
    
    # Get current usage for progress calculation
    data_processor, _, _ = init_components()
    current_usage = data_processor.get_today_usage(user['meter_id']) or 5.0
    
    # Calculate progress based on current badge and usage
    if isinstance(current_badge, dict):
        badge_name = current_badge['name']
        
        if badge_name == 'Efficient Hero':  # >8 kWh
            next_goal = "Reduce to under 8 kWh/day for Carbon Heavy badge"
            progress_val = max(0, min(1, (12 - current_usage) / 4))  # Progress from 12 to 8
        elif badge_name == 'Carbon Heavy':  # 5-8 kWh
            next_goal = "Reduce to under 5 kWh/day for Green User badge"
            progress_val = max(0, min(1, (8 - current_usage) / 3))  # Progress from 8 to 5
        elif badge_name == 'Green User':  # 2-5 kWh
            next_goal = "Reduce to under 2 kWh/day for Eco Saver badge"
            progress_val = max(0, min(1, (5 - current_usage) / 3))  # Progress from 5 to 2
        else:  # Eco Saver or No Badge
            next_goal = "Maintain excellent efficiency under 2 kWh/day"
            progress_val = 0.9  # Almost complete
    else:
        next_goal = "Start tracking to earn your first badge"
        progress_val = 0.1
    
    st.progress(progress_val)
    st.write(f"**Goal:** {next_goal}")
    st.write(f"**Current usage:** {current_usage:.2f} kWh/day")
    st.write(f"**Progress:** {progress_val*100:.0f}% to next level")
    
    # Badge Categories
    st.subheader("🏅 Badge Categories")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #d4edda; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
            <div style="font-size: 3rem;">🌱</div>
            <h5 style="color: #28a745;">Eco Saver</h5>
            <p style="color: black;">Using less than 2 kWh per day</p>
            <span style="background: #28a745; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Excellent Efficiency</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #cce5ff; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #007bff;">
            <div style="font-size: 3rem;">🌍</div>
            <h5 style="color: #007bff;">Green User</h5>
            <p style="color: black;">Using 2-5 kWh per day efficiently</p>
            <span style="background: #007bff; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Good Balance</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #ffc107;">
            <div style="font-size: 3rem;">🔥</div>
            <h5 style="color: #ffc107;">Carbon Heavy</h5>
            <p style="color: black;">Using 5-8 kWh per day</p>
            <span style="background: #ffc107; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Room for Improvement</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #e2e3e5; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid #6c757d;">
            <div style="font-size: 3rem;">🏆</div>
            <h5 style="color: #6c757d;">Efficient Hero</h5>
            <p style="color: black;">High usage but improving</p>
            <span style="background: #6c757d; color: white; padding: 0.2rem 0.5rem; border-radius: 5px;">Making Progress</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Badge History
    st.subheader("📜 Badge History (Last 30 Days)")
    badges_history = gamification.get_user_badges_history(user['id'])
    if badges_history:
        import json
        import re
        
        # Create clean data for display
        clean_data = []
        for entry in badges_history:
            clean_entry = {}
            
            # Handle date
            if 'date' in entry:
                clean_entry['Date'] = entry['date']
            elif 'earned_date' in entry:
                clean_entry['Date'] = entry['earned_date']
            
            # Handle consumption
            consumption = entry.get('consumption') or entry.get('daily_consumption', 0)
            clean_entry['Daily Consumption (kWh)'] = f"{consumption:.2f}"
            clean_entry['CO₂ Emissions (kg)'] = f"{consumption * 0.82:.2f}"
            
            # Handle badge parsing
            badge_str = entry.get('badge', '')
            if isinstance(badge_str, str) and badge_str:
                try:
                    # Try regex extraction first
                    emoji_match = re.search(r'"emoji":"([^"]+)"', badge_str)
                    name_match = re.search(r'"name":"([^"]+)"', badge_str)
                    if emoji_match and name_match:
                        clean_entry['Badge'] = f"{emoji_match.group(1)} {name_match.group(1)}"
                    else:
                        # Try JSON parsing as fallback
                        clean_str = badge_str.replace('""', '"')
                        badge_data = json.loads(clean_str)
                        clean_entry['Badge'] = f"{badge_data['emoji']} {badge_data['name']}"
                except:
                    clean_entry['Badge'] = "Unknown Badge"
            else:
                clean_entry['Badge'] = "No Badge"
            
            clean_data.append(clean_entry)
        
        if clean_data:
            df = pd.DataFrame(clean_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No badge history data available")
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

def get_dynamic_suggestions(data_processor, user):
    """Generate dynamic suggestions based on user's consumption patterns"""
    current_usage = data_processor.get_today_usage(user['meter_id']) or 5.0
    
    suggestions = []
    
    if current_usage > 8:
        suggestions.extend([
            {'title': 'High Usage Alert', 'description': 'Your consumption is very high. Consider reducing AC/heating usage during peak hours.', 'potential_saving': '20-25%', 'difficulty': 'Medium', 'co2_reduction': '2.5 kg/month'},
            {'title': 'Energy Audit', 'description': 'Schedule a professional energy audit to identify major inefficiencies.', 'potential_saving': '15-30%', 'difficulty': 'Easy', 'co2_reduction': '3.0 kg/month'}
        ])
    elif current_usage > 5:
        suggestions.extend([
            {'title': 'Optimize Peak Hours', 'description': 'Shift high-energy activities to off-peak hours (11 PM - 6 AM)', 'potential_saving': '15-20%', 'difficulty': 'Easy', 'co2_reduction': '1.2 kg/month'},
            {'title': 'Smart Thermostat', 'description': 'Install a programmable thermostat to optimize heating/cooling', 'potential_saving': '10-15%', 'difficulty': 'Medium', 'co2_reduction': '1.0 kg/month'}
        ])
    else:
        suggestions.extend([
            {'title': 'LED Lighting', 'description': 'Replace remaining incandescent bulbs with LED alternatives', 'potential_saving': '5-10%', 'difficulty': 'Easy', 'co2_reduction': '0.8 kg/month'},
            {'title': 'Smart Power Strips', 'description': 'Use smart power strips to eliminate phantom loads', 'potential_saving': '5-8%', 'difficulty': 'Easy', 'co2_reduction': '0.5 kg/month'}
        ])
    
    # Add seasonal suggestions
    current_month = datetime.now().month
    if current_month in [6, 7, 8]:  # Summer
        suggestions.append({'title': 'Summer Cooling Tips', 'description': 'Use fans with AC, close blinds during day, set AC to 78°F', 'potential_saving': '12-18%', 'difficulty': 'Easy', 'co2_reduction': '1.5 kg/month'})
    elif current_month in [12, 1, 2]:  # Winter
        suggestions.append({'title': 'Winter Heating Tips', 'description': 'Lower thermostat by 2°F, use draft stoppers, wear warmer clothes', 'potential_saving': '10-15%', 'difficulty': 'Easy', 'co2_reduction': '1.3 kg/month'})
    
    return suggestions

def show_suggestions(ml_models, user):
    st.header("💡 Energy Saving Suggestions")
    
    data_processor, _, _ = init_components()
    current_usage = data_processor.get_today_usage(user['meter_id']) or 5.0
    monthly_usage = current_usage * 30
    
    # Potential Savings Overview
    st.subheader("💰 Your Potential Savings")
    col1, col2, col3, col4 = st.columns(4)
    
    potential_reduction = monthly_usage * 0.2  # 20% reduction
    co2_reduction = potential_reduction * 0.82
    monthly_savings = potential_reduction * 5.67  # ₹5.67 per kWh
    
    with col1:
        st.metric("Current Monthly Usage", f"{monthly_usage:.0f} kWh")
    with col2:
        st.metric("Potential Reduction", f"{potential_reduction:.1f} kWh")
    with col3:
        st.metric("CO₂ Reduction", f"{co2_reduction:.1f} kg")
    with col4:
        st.metric("Monthly Savings", f"₹{monthly_savings:.2f}")
    
    st.markdown("---")
    
    # Personalized Recommendations
    st.subheader("🎯 Your Personalized Recommendations")
    
    recommendations = [
        {"title": "LED Lighting", "desc": "Replace incandescent bulbs with LED alternatives", "saving": "5-10%", "difficulty": "Easy", "co2": "0.8 kg/month"},
        {"title": "Unplug Devices", "desc": "Unplug electronics when not in use to eliminate phantom loads", "saving": "5-8%", "difficulty": "Easy", "co2": "0.3 kg/month"},
        {"title": "Optimize Peak Hours", "desc": "Shift high-energy activities to off-peak hours (11 PM - 6 AM)", "saving": "15-20%", "difficulty": "Easy", "co2": "0.5 kg/month"}
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border-left: 4px solid #4facfe; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
            <h4 style="color: white; margin-bottom: 1rem;">💡 {rec['title']}</h4>
            <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">{rec['desc']}</p>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <span style="background: rgba(40, 167, 69, 0.2); color: #28a745; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(40, 167, 69, 0.3);"><strong>Potential Saving</strong><br>{rec['saving']}</span>
                <span style="background: rgba(0, 123, 255, 0.2); color: #007bff; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(0, 123, 255, 0.3);"><strong>Difficulty</strong><br>{rec['difficulty']}</span>
                <span style="background: rgba(255, 152, 0, 0.2); color: #ff9800; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(255, 152, 0, 0.3);"><strong>CO₂ Reduction Potential</strong><br>{rec['co2']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # General Tips
    st.subheader("💡 General Energy Saving Tips")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏠 Home Efficiency**
        - Seal air leaks around windows and doors
        - Use programmable thermostats
        - Insulate your home properly
        - Clean or replace HVAC filters regularly
        """)
    
    with col2:
        st.markdown("""
        **🔌 Appliance Usage**
        - Unplug electronics when not in use
        - Use cold water for washing clothes
        - Air dry clothes instead of using dryer
        - Use energy-efficient appliances
        """)
    
    with col3:
        st.markdown("""
        **⏰ Peak Hours Optimization**
        
        Shift high-energy activities to off-peak hours to save money and reduce grid strain:
        
        **Peak Hours:** 6 AM - 10 AM, 6 PM - 10 PM (Higher rates)
        **Off-Peak Hours:** 11 PM - 6 AM (Lower rates)
        **Best Times:** Run dishwasher, laundry, and charge devices during off-peak
        """)
    
    st.markdown("---")
    
    # Action Plan
    st.subheader("📅 Your Action Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(40, 167, 69, 0.1); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #28a745; backdrop-filter: blur(10px); border: 1px solid rgba(40, 167, 69, 0.2);">
            <h4 style="color: #28a745; margin-bottom: 1rem;">This Week</h4>
            <p style="color: rgba(255,255,255,0.8);">Implement 1-2 easy suggestions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255, 152, 0, 0.1); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #ff9800; backdrop-filter: blur(10px); border: 1px solid rgba(255, 152, 0, 0.2);">
            <h4 style="color: #ff9800; margin-bottom: 1rem;">This Month</h4>
            <p style="color: rgba(255,255,255,0.8);">Focus on medium difficulty changes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(33, 150, 243, 0.1); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #2196f3; backdrop-filter: blur(10px); border: 1px solid rgba(33, 150, 243, 0.2);">
            <h4 style="color: #2196f3; margin-bottom: 1rem;">Long Term</h4>
            <p style="color: rgba(255,255,255,0.8);">Plan major efficiency upgrades</p>
        </div>
        """, unsafe_allow_html=True)

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
        st.info("Demo Credentials: Username: demo_user | Password: password123")
    
    # Route to appropriate page
    if st.session_state.user:
        dashboard_page()
    elif st.session_state.get('show_register', False):
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()