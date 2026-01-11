from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# 1. Initialize the App
app = FastAPI(title="Bangalore Traffic Predictor")

# 2. Load the Model (The Brain)
# We check if model exists first
MODEL_PATH = "model.pkl"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model not found at {MODEL_PATH}. Did you run model.py?")

model = joblib.load(MODEL_PATH)

# 3. Define the Input Data Shape (The Contract)
class TrafficRequest(BaseModel):
    location_id: int  # 0: Silk Board, 1: Marathahalli, etc.
    hour_of_day: int  # 0-23
    is_weekend: int   # 0 or 1

# 4. Define the Prediction Endpoint
@app.post("/predict")
def predict_traffic(data: TrafficRequest):
    """
    Input: JSON with location_id, hour, is_weekend
    Output: Predicted traffic volume
    """
    try:
        # Convert JSON request to Pandas DataFrame (what the model expects)
        input_data = pd.DataFrame([data.dict()])
       
        # Ask the model for a prediction
        prediction = model.predict(input_data)
       
        # Return the result
        return {
            "location_id": data.location_id,
            "predicted_volume": int(prediction[0]),
            "message": "High Traffic Warning" if prediction[0] > 60 else "Traffic Normal"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Root Endpoint (Just to check if it's alive)
@app.get("/")
def home():
    return {"status": "System is healthy", "version": "1.0.0"}