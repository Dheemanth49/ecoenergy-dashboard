#!/usr/bin/env python3
"""
Generate synthetic training data for ML models
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_data(num_samples=5000):
    """Generate synthetic energy consumption data"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate timestamps
    start_date = datetime(2023, 1, 1)
    timestamps = [start_date + timedelta(hours=i) for i in range(num_samples)]
    
    # Generate realistic energy consumption patterns
    data = []
    for i, ts in enumerate(timestamps):
        hour = ts.hour
        day_of_week = ts.weekday()
        
        # Base consumption with daily and weekly patterns
        base_consumption = 3.0
        
        # Higher consumption during peak hours
        if 6 <= hour <= 10 or 18 <= hour <= 22:
            base_consumption += np.random.uniform(1.0, 3.0)
        elif 23 <= hour or hour <= 5:
            base_consumption += np.random.uniform(-1.0, 0.5)
        
        # Weekend patterns
        if day_of_week >= 5:  # Weekend
            base_consumption += np.random.uniform(-0.5, 1.0)
        
        # Add seasonal variation
        month = ts.month
        if month in [6, 7, 8]:  # Summer - higher AC usage
            base_consumption += np.random.uniform(0.5, 2.0)
        elif month in [12, 1, 2]:  # Winter - higher heating
            base_consumption += np.random.uniform(0.3, 1.5)
        
        # Add random noise
        consumption = max(0.1, base_consumption + np.random.normal(0, 0.5))
        
        # Generate correlated electrical parameters
        voltage = np.random.normal(230, 10)  # 230V ± 10V
        current = consumption / voltage * 1000 + np.random.normal(0, 0.5)  # Approximate current
        frequency = np.random.normal(50, 0.2)  # 50Hz ± 0.2Hz
        
        data.append({
            'x_Timestamp': ts,
            'meter': f'METER{(i % 10) + 1:03d}',  # 10 different meters
            't_kWh': round(consumption, 3),
            'z_Avg Voltage (Volt)': round(voltage, 2),
            'z_Avg Current (Amp)': round(max(0.1, current), 2),
            'y_Freq (Hz)': round(frequency, 2)
        })
    
    return pd.DataFrame(data)

def main():
    print("Generating synthetic training data...")
    
    # Generate data
    df = generate_synthetic_data(5000)
    
    # Save to CSV
    df.to_csv('data/sample_dataset.csv', index=False)
    
    print(f"Generated {len(df)} samples")
    print(f"Date range: {df['x_Timestamp'].min()} to {df['x_Timestamp'].max()}")
    print(f"Consumption range: {df['t_kWh'].min():.2f} - {df['t_kWh'].max():.2f} kWh")
    print("Data saved to data/sample_dataset.csv")

if __name__ == "__main__":
    main()