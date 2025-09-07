# EcoEnergy Dashboard 🌱

A comprehensive full-stack ML application for sustainable energy consumption monitoring with gamification features.

## 🚀 Features

### 📊 Data Analytics & ML
- **Real-time Energy Monitoring**: Track consumption patterns with 3-minute granularity
- **Carbon Footprint Calculation**: Automatic CO₂ emission tracking (0.82 kg CO₂/kWh)
- **ML Forecasting**: Prophet/LSTM models for consumption prediction
- **Anomaly Detection**: Identify unusual consumption patterns
- **Professional EDA**: Comprehensive exploratory data analysis with visualizations

### 🎮 Gamification System
- **Badge System**: 
  - 🌱 Eco Saver (< 2 kWh/day)
  - 🌍 Green User (2-5 kWh/day)
  - 🔥 Carbon Heavy (5-8 kWh/day)
  - 🏆 Efficient Hero (> 8 kWh but improving)
- **Leaderboard**: Weekly rankings based on efficiency
- **Progress Tracking**: Visual progress bars and achievement history

### 💡 Smart Recommendations
- **Personalized Suggestions**: AI-powered energy-saving tips
- **Potential Savings Calculator**: CO₂ and cost reduction estimates
- **Peak Hour Optimization**: Time-based usage recommendations

### 🔐 User Management
- **Secure Authentication**: Flask-Login with bcrypt password hashing
- **Multi-user Support**: Individual dashboards per meter/user
- **Session Management**: Secure login/logout functionality

### 📱 Modern Frontend
- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Interactive Charts**: Plotly.js visualizations
- **Professional UI**: Clean, modern interface with intuitive navigation

<<<<<<< HEAD
## 🛠 Technology Stack

### Backend
- **Framework**: Flask (Python)
- **ML Libraries**: Scikit-learn, TensorFlow, Prophet
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite (default)
- **Authentication**: Flask-Login, Werkzeug Security

### Frontend
- **HTML5 & CSS3**: Semantic markup with modern styling
- **Bootstrap 5**: Responsive component library
- **JavaScript**: Interactive features and AJAX
- **Plotly.js**: Dynamic data visualizations

## 📁 Project Structure

```
sus-energy/
├── app.py                 # Main Flask application
├── setup.py              # Setup and initialization script
├── eda_analysis.py        # Comprehensive EDA analysis
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── energy_app.db         # SQLite database (created on setup)
│
├── data/
│   └── total_dataset.csv  # Energy consumption dataset
│
├── models/
│   ├── __init__.py
│   ├── data_processor.py  # Data preprocessing and EDA
│   ├── ml_models.py       # ML forecasting and classification
│   └── gamification.py    # Badge system and leaderboard
│
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Landing page
│   ├── login.html         # User login
│   ├── register.html      # User registration
│   ├── dashboard.html     # Main dashboard
│   ├── badges.html        # Badge system page
│   ├── leaderboard.html   # Rankings and competition
│   ├── suggestions.html   # Energy-saving recommendations
│   └── about.html         # Project information
│
└── static/
    ├── css/
    │   └── style.css      # Custom styles
    ├── js/
    │   └── main.js        # JavaScript functionality
    └── images/            # Generated EDA visualizations
```
=======
>>>>>>> 8c55bc9113d43998dcc4078c182cbc6fe8629a25

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Installation

```bash
# Clone or download the project
<<<<<<< HEAD
cd sus-energy
=======
cd carbon-emission
>>>>>>> 8c55bc9113d43998dcc4078c182cbc6fe8629a25

# Install dependencies
pip install -r requirements.txt

<<<<<<< HEAD
# Run setup script
python setup.py
=======
>>>>>>> 8c55bc9113d43998dcc4078c182cbc6fe8629a25
```

### 3. Dataset Setup
Ensure your dataset (`total_dataset.csv`) is in the `data/` directory with columns:
- `x_Timestamp`: DateTime (every 3 minutes)
- `t_kWh`: Energy consumed in kWh
- `z_Avg Voltage (V)`: Average voltage
- `z_Avg Current (A)`: Average current
- `y_Freq (Hz)`: Frequency
- `meter`: Meter ID

<<<<<<< HEAD
### 4. Run Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### 5. Login
Use sample credentials:
- **Username**: `demo_user`
- **Password**: `password123`

## 📊 Data Processing Pipeline

### 1. Data Preprocessing
- **Timestamp Conversion**: Convert to datetime and set as index
- **Resampling**: Aggregate to hourly and daily totals
- **Missing Values**: Median/mean imputation
- **Outlier Handling**: IQR-based outlier removal
- **Feature Engineering**: Carbon emissions calculation

### 2. EDA Analysis
- **Dataset Overview**: Shape, types, missing values, statistics
- **Correlation Analysis**: Heatmap and correlation matrix
- **Distribution Analysis**: Histograms and KDE plots
- **Time Series Analysis**: Trends, seasonality, rolling statistics
- **Anomaly Detection**: Z-score and IQR methods
- **Meter Comparison**: Cross-meter efficiency analysis

### 3. ML Models
- **Forecasting Model**: Random Forest for consumption prediction
- **Classification Model**: Badge category prediction
- **Feature Engineering**: Time-based features, lag variables, rolling statistics

## 🎮 Gamification Features

### Badge System
Users earn badges based on daily consumption:
- **Eco Saver** 🌱: < 2 kWh/day (Excellent efficiency)
- **Green User** 🌍: 2-5 kWh/day (Good balance)
- **Carbon Heavy** 🔥: 5-8 kWh/day (Room for improvement)
- **Efficient Hero** 🏆: > 8 kWh/day but improving

### Leaderboard
- **Weekly Rankings**: Based on average daily consumption
- **Point System**: Lower consumption = Higher points
- **Progress Tracking**: 7-day rolling averages

### Achievements
- **Badge History**: Track daily badge progression
- **Progress Bars**: Visual progress toward next badge level
- **Personalized Goals**: Custom targets based on usage patterns

## 💡 Smart Suggestions Engine

### Recommendation Categories
1. **Peak Hour Optimization**: Shift usage to off-peak times
2. **Appliance Efficiency**: Upgrade to energy-efficient devices
3. **Behavioral Changes**: Simple habit modifications
4. **Home Improvements**: Insulation and weatherization
5. **Smart Technology**: Programmable thermostats and smart plugs

### Savings Calculator
- **Energy Reduction**: Potential kWh savings
- **Cost Savings**: Monthly dollar savings
- **CO₂ Reduction**: Environmental impact reduction
- **Implementation Difficulty**: Easy/Medium/Hard categorization

## 🔧 Configuration


### Database Configuration
- **Default**: SQLite (energy_app.db)
- **Production**: PostgreSQL (update connection string in app.py)

## 📈 API Endpoints

### Authentication
- `POST /register`: User registration
- `POST /login`: User login
- `GET /logout`: User logout

### Dashboard
- `GET /dashboard`: Main dashboard
- `GET /api/chart_data`: Chart data for visualizations
- `GET /api/forecast`: ML forecast data

### Gamification
- `GET /badges`: Badge system page
- `GET /leaderboard`: Rankings and competition
- `GET /suggestions`: Personalized recommendations

## 🧪 Testing

### Sample Data Generation
The application includes sample data generation for testing:
```python
# Generate sample consumption data
python -c "from models.gamification import GamificationEngine; g = GamificationEngine(); print('Sample data generated')"
```

### User Testing
1. Register new users with different meter IDs
2. Simulate different consumption patterns
3. Test badge progression and leaderboard updates

## 🚀 Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
1. **Update Configuration**: Set production database and secret key
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Initialize Database**: `python setup.py`
4. **Run with WSGI**: Use Gunicorn or similar WSGI server



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## 🆘 Support

### Common Issues
1. **Dataset Not Found**: Ensure `total_dataset.csv` is in the `data/` directory
2. **Database Errors**: Run `python setup.py` to reinitialize
3. **Missing Dependencies**: Install with `pip install -r requirements.txt`

### Getting Help
- Check the console output for error messages
- Ensure all dependencies are installed
- Verify dataset format and column names
- Check file permissions for database creation

## 🌟 Future Enhancements

- **Real-time Data Integration**: Connect to actual smart meters
- **Mobile App**: React Native companion app
- **Advanced ML**: Deep learning models for better forecasting
- **Social Features**: Friend connections and challenges
- **IoT Integration**: Smart home device control
- **Renewable Energy**: Solar panel and battery tracking

---

**Made with ❤️ for a sustainable future** 🌍
=======

**Made with ❤️ for a sustainable future** 🌍

>>>>>>> 8c55bc9113d43998dcc4078c182cbc6fe8629a25
