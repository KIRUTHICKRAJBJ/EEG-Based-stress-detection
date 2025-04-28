# main.py
import streamlit as st
import joblib
import numpy as np
from firebase_config import db

def stress_detection_app(user_email):
    st.markdown("<h1>🧠 EEG Stress Detection</h1>", unsafe_allow_html=True)

    tabs = st.tabs(["🔮 Predict Stress", "🕓 Prediction History"])

    with tabs[0]:  # First Tab - Stress Prediction
        model = joblib.load("svm_stress_99.joblib")
        scaler = joblib.load("scaler.joblib")

        feature_names = ["Delta Power", "Theta Power", "Alpha Power", "Beta Power", "Gamma Power"]
        inputs = [st.number_input(f"{name}", value=0.0, format="%.3f") for name in feature_names]

        if st.button("🚀 Predict Stress Level"):
            features = np.array(inputs).reshape(1, -1)
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]

            stress_labels = {
                0: "🟢 **Low Stress** – Stay relaxed!",
                1: "🟡 **Moderate Stress** – Keep calm!",
                2: "🔴 **High Stress** – Take a break!"
            }

            st.markdown(f"### 🔎 Predicted: {stress_labels[prediction]}")

            # Save into Firestore
            data = {
                "email": user_email,
                "inputs": inputs,
                "predicted_stress_level": int(prediction)
            }
            db.collection("stress_predictions").add(data)
            st.success("✅ Result saved to your history!")

    with tabs[1]:  # Second Tab - View Prediction History
        st.subheader("📜 Your Past Predictions")

        # Fetch from Firestore
        predictions = db.collection("stress_predictions").where("email", "==", user_email).stream()

        results = []
        for pred in predictions:
            data = pred.to_dict()
            results.append(data)

        if results:
            for idx, record in enumerate(results[::-1], 1):  # reverse to show latest first
                stress_levels = {
                    0: "Low Stress",
                    1: "Moderate Stress",
                    2: "High Stress"
                }
                st.write(f"**{idx}. Stress Level:** {stress_levels[record['predicted_stress_level']]}")
                st.write(f"Inputs: {record['inputs']}")
                st.markdown("---")
        else:
            st.info("No predictions found. Make your first prediction!")

