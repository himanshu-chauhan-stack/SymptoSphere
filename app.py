import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

# Load model
model, encoder = load("trained_models/best_model.joblib")

st.title("🩺 AI Disease Predictor")

# ✅ Load ALL features from dataset (ensures 132 features)
df = pd.read_csv("dataset/training_data.csv")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

all_symptoms = df.drop("prognosis", axis=1).columns.tolist()

st.write(f"Total Symptoms Loaded: {len(all_symptoms)}")  # DEBUG

st.write("Select your symptoms:")

# Create checkboxes
selected_symptoms = []
cols = st.columns(4)

for i, symptom in enumerate(all_symptoms):
    with cols[i % 4]:
        if st.checkbox(symptom):
            selected_symptoms.append(symptom)

# ✅ Build FULL 132-length input vector
input_data = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]

input_array = np.array(input_data).reshape(1, -1)

# DEBUG (important)
st.write("Input shape:", input_array.shape)

# Predict
if st.button("Predict Disease"):

    probs = model.predict_proba(input_array)[0]
    classes = encoder.inverse_transform(range(len(probs)))

    top3_idx = probs.argsort()[-3:][::-1]

    st.subheader("🔮 Top 3 Predictions:")
    for i in top3_idx:
        st.write(f"{classes[i]} : {probs[i]*100:.2f}%")