import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import plotly.graph_objs as go
import plotly.utils

class DataProcessor:
    def __init__(self):
        self.df = None
        self.load_data()
        self.preprocess_data()
    
    def load_data(self):
        """Load and initial preprocessing of the dataset"""
        try:
            # Use sample dataset for deployment
            print("Loading sample dataset...")
            self.df = pd.read_csv('data/sample_dataset.csv')
            print(f"Dataset loaded: {self.df.shape}")
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create minimal sample data if file not found
            self.df = pd.DataFrame({
                'x_Timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
                'meter': ['METER001'] * 100,
                't_kWh': np.random.uniform(1, 8, 100),
                'z_Avg Voltage (Volt)': np.random.uniform(220, 240, 100),
                'z_Avg Current (Amp)': np.random.uniform(5, 15, 100),
                'y_Freq (Hz)': np.random.uniform(49.5, 50.5, 100)
            })
            print("Using generated sample data")
    
    def preprocess_data(self):
        """Optimized data preprocessing for large datasets"""
        if self.df.empty:
            return
        
        print("Converting timestamps...")
        self.df['x_Timestamp'] = pd.to_datetime(self.df['x_Timestamp'])
        self.df.set_index('x_Timestamp', inplace=True)
        
        print("Handling missing values...")
        # Use faster fillna methods
        self.df['t_kWh'].fillna(method='ffill', inplace=True)
        if 'z_Avg Voltage (Volt)' in self.df.columns:
            self.df['z_Avg Voltage (Volt)'].fillna(method='ffill', inplace=True)
        if 'z_Avg Current (Amp)' in self.df.columns:
            self.df['z_Avg Current (Amp)'].fillna(method='ffill', inplace=True)
        if 'y_Freq (Hz)' in self.df.columns:
            self.df['y_Freq (Hz)'].fillna(method='ffill', inplace=True)
        
        print("Calculating carbon emissions...")
        self.df['carbon_emissions'] = self.df['t_kWh'] * 0.82
        
        print("Creating aggregated data...")
        # Create resampled versions
        agg_dict = {
            't_kWh': 'sum',
            'carbon_emissions': 'sum'
        }
        
        # Add optional columns if they exist
        if 'z_Avg Voltage (Volt)' in self.df.columns:
            agg_dict['z_Avg Voltage (Volt)'] = 'mean'
        if 'z_Avg Current (Amp)' in self.df.columns:
            agg_dict['z_Avg Current (Amp)'] = 'mean'
        if 'y_Freq (Hz)' in self.df.columns:
            agg_dict['y_Freq (Hz)'] = 'mean'
        
        if 'meter' in self.df.columns:
            self.hourly_data = self.df.groupby(['meter']).resample('H').agg(agg_dict).reset_index()
            self.daily_data = self.df.groupby(['meter']).resample('D').agg(agg_dict).reset_index()
        else:
            self.hourly_data = self.df.resample('H').agg(agg_dict).reset_index()
            self.daily_data = self.df.resample('D').agg(agg_dict).reset_index()
        
        print("Data preprocessing completed")
    
    def get_dataset_overview(self):
        """Generate comprehensive dataset overview"""
        if self.df.empty:
            return {}
        
        overview = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'statistics': self.df.describe().to_dict(),
            'date_range': {
                'start': self.df.index.min().strftime('%Y-%m-%d'),
                'end': self.df.index.max().strftime('%Y-%m-%d')
            },
            'unique_meters': self.df['meter'].nunique(),
            'total_consumption': self.df['t_kWh'].sum(),
            'total_emissions': self.df['carbon_emissions'].sum()
        }
        return overview
    
    def get_correlation_matrix(self):
        """Calculate correlation matrix for numerical columns"""
        numeric_cols = ['t_kWh', 'carbon_emissions']
        
        # Add optional columns if they exist
        optional_cols = ['z_Avg Voltage (Volt)', 'z_Avg Current (Amp)', 'y_Freq (Hz)']
        for col in optional_cols:
            if col in self.df.columns:
                numeric_cols.append(col)
        
        corr_matrix = self.df[numeric_cols].corr()
        return corr_matrix.to_dict()
    
    def detect_anomalies(self):
        """Detect anomalies in energy consumption"""
        if self.df.empty:
            return []
        
        # Using Z-score method
        z_scores = np.abs((self.df['t_kWh'] - self.df['t_kWh'].mean()) / self.df['t_kWh'].std())
        anomalies = self.df[z_scores > 3]
        
        return [{
            'timestamp': idx.strftime('%Y-%m-%d %H:%M'),
            'consumption': row['t_kWh'],
            'meter': row['meter'],
            'z_score': z_scores.loc[idx]
        } for idx, row in anomalies.iterrows()]
    
    def get_user_data(self, meter_id):
        """Get data for specific user/meter"""
        if not meter_id:
            return pd.DataFrame()
        
        # Generate sample data for demo
        import random
        from datetime import timedelta
        
        random.seed(hash(meter_id) % 1000)
        dates = [datetime.now().date() - timedelta(days=i) for i in range(30)]
        data = []
        
        for date in dates:
            consumption = round(random.uniform(1.0, 9.0), 2)
            data.append({
                'x_Timestamp': date,
                't_kWh': consumption,
                'carbon_emissions': consumption * 0.82
            })
        
        return pd.DataFrame(data)
    
    def get_today_usage(self, meter_id):
        """Get today's energy usage for user"""
        if not meter_id:
            return 0
        
        # Generate sample data for demo
        import random
        random.seed(hash(meter_id) % 1000)
        return round(random.uniform(1.5, 8.0), 2)
    
    def get_chart_data(self, meter_id, chart_type='daily'):
        """Generate chart data for frontend"""
        user_data = self.get_user_data(meter_id)
        
        if user_data.empty:
            return {'labels': [], 'consumption': [], 'emissions': []}
        
        data = user_data.tail(30) if chart_type == 'daily' else user_data.tail(7)
        
        return {
            'labels': [d.strftime('%Y-%m-%d') for d in data['x_Timestamp']],
            'consumption': data['t_kWh'].tolist(),
            'emissions': data['carbon_emissions'].tolist()
        }
    
    def get_insights(self):
        """Generate automated insights from the data"""
        if self.df.empty:
            return []
        
        insights = []
        
        # Peak usage time
        hourly_avg = self.df.groupby(self.df.index.hour)['t_kWh'].mean()
        peak_hour = hourly_avg.idxmax()
        insights.append(f"Peak energy usage occurs at {peak_hour}:00 with average {hourly_avg.max():.2f} kWh")
        
        # Weekly patterns
        daily_avg = self.df.groupby(self.df.index.dayofweek)['t_kWh'].mean()
        peak_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][daily_avg.idxmax()]
        insights.append(f"Highest consumption day is {peak_day} with {daily_avg.max():.2f} kWh average")
        
        # Efficiency insights
        avg_voltage = self.df['z_Avg Voltage (Volt)'].mean()
        if avg_voltage < 220:
            insights.append("Voltage levels are below optimal (220V), which may indicate inefficiency")
        
        # Carbon footprint
        total_emissions = self.df['carbon_emissions'].sum()
        insights.append(f"Total carbon footprint: {total_emissions:.2f} kg CO₂")
        
        return insights