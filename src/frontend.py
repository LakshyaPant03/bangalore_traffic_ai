import streamlit as st
import requests

# 1. Setup the Page
st.set_page_config(page_title="Bangalore Traffic AI", page_icon="🚦")

st.title("🚦 Bangalore Traffic Predictor")
st.markdown("### Powered by Random Forest & FastAPI")

# 2. Input Form (The User Interface)
col1, col2 = st.columns(2)

with col1:
    location = st.selectbox(
        "Select Junction",
        ["Silk Board", "Marathahalli Bridge", "Tin Factory", "Sony World Signal"]
    )

with col2:
    hour = st.slider("Hour of Day (0-23)", 0, 23, 18)

is_weekend = st.checkbox("Is it a Weekend?")

# Map location name to ID (Must match model.py!)
LOC_MAP = {
    "Silk Board": 0,
    "Marathahalli Bridge": 1,
    "Tin Factory": 2,
    "Sony World Signal": 3
}

# 3. The Logic (Sending data to the Backend)
if st.button("Predict Congestion"):
    # Create the payload (JSON)
    payload = {
        "location_id": LOC_MAP[location],
        "hour_of_day": hour,
        "is_weekend": 1 if is_weekend else 0
    }
   
    # Call the API
    try:
        # Note: We assume the API is running on localhost:8000
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
       
        if response.status_code == 200:
            result = response.json()
            volume = result['predicted_volume']
            message = result['message']
           
            # Display Results
            st.metric(label="Predicted Traffic Volume", value=f"{volume} cars/min")
           
            if "High" in message:
                st.error(f"⚠️ {message}")
            else:
                st.success(f"✅ {message}")
        else:
            st.error("Error: Could not connect to the Brain.")
           
    except Exception as e:
        st.error(f"Connection Error. Is the API running? \n\nDetails: {e}")