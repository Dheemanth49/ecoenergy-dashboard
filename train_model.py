#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Train ML models and display accuracy metrics
"""

from models.data_processor import DataProcessor
from models.ml_models import MLModels

def main():
    print("Starting model training...")
    
    # Initialize components
    data_processor = DataProcessor()
    ml_models = MLModels()
    
    # Check if data is loaded
    if data_processor.df.empty:
        print("No data available for training")
        return
    
    print(f"Dataset shape: {data_processor.df.shape}")
    
    # Train models
    success = ml_models.train_models(data_processor.df)
    
    if success:
        print("Model training completed successfully!")
        
        # Get and display accuracy metrics
        metrics = ml_models.get_model_accuracy()
        print("\nFinal Model Performance:")
        print(f"   Forecasting MAE: {metrics['forecast_mae']:.4f} kWh")
        print(f"   Classification Accuracy: {metrics['classification_accuracy_percent']:.2f}%")
        
    else:
        print("Model training failed")

if __name__ == "__main__":
    main()