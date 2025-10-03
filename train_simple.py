# Simple training script using scikit-learn instead of TensorFlow
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
import pickle
import os

def create_synthetic_data():
    """Create synthetic exoplanet data for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'koi_disposition': np.random.choice(['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'], 
                                           n_samples, p=[0.3, 0.2, 0.5]),
        'koi_period': np.abs(np.random.normal(50, 100, n_samples)),
        'koi_period_err1': np.abs(np.random.normal(0.1, 0.05, n_samples)),
        'koi_time0bk': np.random.uniform(120, 140, n_samples),
        'koi_time0bk_err1': np.abs(np.random.normal(0.01, 0.005, n_samples)),
        'koi_impact': np.random.uniform(0, 1, n_samples),
        'koi_duration': np.abs(np.random.normal(5, 3, n_samples)),
        'koi_depth': np.abs(np.random.normal(200, 150, n_samples)),
        'koi_prad': np.abs(np.random.normal(3, 2, n_samples)),
        'koi_teq': np.random.uniform(200, 400, n_samples),
        'koi_insol': np.abs(np.random.normal(1.5, 1, n_samples)),
        'koi_model_snr': np.abs(np.random.normal(30, 15, n_samples)),
        'koi_steff': np.random.uniform(4000, 7000, n_samples),
        'koi_slogg': np.random.uniform(3.5, 5, n_samples),
        'koi_srad': np.abs(np.random.normal(1.2, 0.5, n_samples))
    }
    
    return pd.DataFrame(data)

def train_simple_model():
    """Train a simple model using scikit-learn"""
    print("Starting model training with scikit-learn...")
    
    # Create synthetic data
    df = create_synthetic_data()
    
    # Select features
    feature_columns = [
        'koi_period', 'koi_period_err1', 'koi_time0bk', 'koi_time0bk_err1',
        'koi_impact', 'koi_duration', 'koi_depth', 'koi_prad', 'koi_teq',
        'koi_insol', 'koi_model_snr', 'koi_steff', 'koi_slogg', 'koi_srad'
    ]
    
    X = df[feature_columns].values
    y = df['koi_disposition'].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.4f}")
    
    # Save model, scaler, and label encoder
    print("Saving model components...")
    
    with open('simple_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    print("Model, scaler, and label encoder saved successfully!")
    
    # Generate classification report
    y_pred = model.predict(X_test)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    print("\nTraining process complete!")
    
    return model, scaler, label_encoder, feature_columns

if __name__ == "__main__":
    train_simple_model()