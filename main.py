import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # Your service account JSON
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Load ML model and scaler
model = joblib.load('svm_stress_99.joblib')  # Your trained model
scaler = joblib.load('scaler.joblib')         # Your scaler

# Stress detection function
def predict_stress(features):
    features = np.array(features).reshape(1, -1)
    features = scaler.transform(features)
    prediction = model.predict(features)
    stress_level = int(prediction[0])
    return stress_level

# Mapping for stress level
stress_mapping = {
    0: "Relaxed",
    1: "Moderate Stress",
    2: "High Stress"
}

# Main stress detection app
def stress_detection_app(user_email):
    st.title("🔮 Stress Prediction")

    st.write("Please input your EEG frequency band powers:")

    # Input fields
    delta_power = st.number_input("Delta Power", format="%.5f")
    theta_power = st.number_input("Theta Power", format="%.5f")
    alpha_power = st.number_input("Alpha Power", format="%.5f")
    beta_power = st.number_input("Beta Power", format="%.5f")
    gamma_power = st.number_input("Gamma Power", format="%.5f")

    if st.button("🔮 Predict"):
        with st.spinner("Predicting..."):
            input_features = [delta_power, theta_power, alpha_power, beta_power, gamma_power]  # Correct order!
            prediction = predict_stress(input_features)
            stress_label = stress_mapping[prediction]

            st.success(f"🔎 Predicted: **{stress_label}**")

            # Save prediction to Firestore
            now = datetime.datetime.now()
            data = {
                'user_email': user_email,
                'delta_power': delta_power,
                'theta_power': theta_power,
                'alpha_power': alpha_power,
                'beta_power': beta_power,
                'gamma_power': gamma_power,
                'prediction': stress_label,
                'timestamp': now
            }
            try:
                db.collection("stress_predictions").add(data)
                st.info("Prediction saved successfully!")
            except Exception as e:
                st.error("⚠️ Failed to save prediction. Please try again.")
                st.error(f"Error: {e}")


# History page
def prediction_history(user_email):
    st.title("🕓 Prediction History")

    try:
        query = db.collection("stress_predictions").where("user_email", "==", user_email).order_by("timestamp", direction=firestore.Query.DESCENDING)
        results = query.stream()

        history = []
        for doc in results:
            record = doc.to_dict()
            history.append(record)

        if history:
            df = pd.DataFrame(history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(by='timestamp', ascending=False)
            st.dataframe(df[['timestamp', 'prediction']])
        else:
            st.info("No predictions found yet. Make your first prediction!")
    
    except Exception as e:
        st.error("⚠️ Failed to load history.")
        st.error(f"Error: {e}")
