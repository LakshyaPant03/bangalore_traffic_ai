import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib  # Used to save the model to a file
import os

# 1. ENGINEERING: Define constants at the top
MODEL_PATH = "model.pkl"
LOCATIONS = {
    0: "Silk Board",
    1: "Marathahalli Bridge",
    2: "Tin Factory",
    3: "Sony World Signal"
}

def generate_mock_data(n_samples=1000):
    """
    Generates synthetic traffic data simulating Bangalore patterns.
    High traffic during peak hours (8-10 AM, 5-8 PM).
    """
    np.random.seed(42) # Ensure we get same numbers every time
   
    # Randomly pick locations and hours
    location_ids = np.random.choice(list(LOCATIONS.keys()), n_samples)
    hours = np.random.randint(0, 24, n_samples)
    is_weekend = np.random.choice([0, 1], n_samples, p=[0.7, 0.3]) # 70% weekdays
   
    # Simulate Traffic Volume (The "Target" Variable)
    # Base traffic + Peak Hour Logic + Random Noise
    traffic_volume = np.random.normal(30, 10, n_samples) # Base flow
   
    for i in range(n_samples):
        # Add rush hour spikes
        if (8 <= hours[i] <= 10) or (17 <= hours[i] <= 20):
            traffic_volume[i] += 50  # Huge spike
       
        # Reduce traffic on weekends
        if is_weekend[i] == 1:
            traffic_volume[i] *= 0.6
           
    # Ensure no negative traffic
    traffic_volume = np.maximum(traffic_volume, 0)
   
    # Create DataFrame
    df = pd.DataFrame({
        'location_id': location_ids,
        'hour_of_day': hours,
        'is_weekend': is_weekend,
        'traffic_volume': traffic_volume
    })
   
    return df

def train_and_save():
    print("Step 1: Generating synthetic Bangalore traffic data...")
    df = generate_mock_data(5000)
   
    # Features (Inputs) vs Target (Output)
    X = df[['location_id', 'hour_of_day', 'is_weekend']]
    y = df['traffic_volume']
   
    print(f"Step 2: Training Random Forest on {len(df)} samples...")
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
   
    # Simple Evaluation
    y_pred = model.predict(X)
    mae = mean_absolute_error(y, y_pred)
    print(f"   Model Performance: Average Error is +/- {mae:.2f} vehicles")
   
    print("Step 3: Saving the model artifact...")
    joblib.dump(model, MODEL_PATH)
    print(f"   Success! Model saved to {os.getcwd()}\{MODEL_PATH}")

if __name__ == "__main__":
    train_and_save()