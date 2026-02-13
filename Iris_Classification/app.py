import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the saved model, scaler, and label encoder
@st.cache_resource
def load_models():
    with open('knn_model.pkl', 'rb') as f:
        knn_model = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    return knn_model, scaler, label_encoder


knn, scaler, le = load_models()

# App title and description
st.title("Iris Flower Species Classifier")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sepal Measurements")
    sepal_length = st.number_input(
        "Sepal Length (cm)",
        min_value=4.0,
        max_value=8.0,
        value=5.8,
        step=0.01,
        format="%.2f"
    )
    
    sepal_width = st.number_input(
        "Sepal Width (cm)",
        min_value=0.1,
       
        value=3.0,
        step=0.01,
        format="%.2f"
    )

with col2:
    st.subheader("Petal Measurements")
    petal_length = st.number_input(
        "Petal Length (cm)",
        min_value=0.1,
        
        value=4.0,
        step=0.01,
        format="%.2f"
    )
    
    petal_width = st.number_input(
        "Petal Width (cm)",
        min_value=0.1,
        
        value=1.2,
        step=0.01,
        format="%.2f"
    )

st.write("---")

# Create a button for prediction
if st.button("Predict Species", type="primary"):
    # Prepare input data
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    
    # Scale the input
    input_scaled = scaler.transform(input_data)
    
    # Make prediction
    prediction = knn.predict(input_scaled)
    prediction_proba = knn.predict_proba(input_scaled)
    
    # Decode the prediction
    species = le.inverse_transform(prediction)[0]
    
    # Display results
    st.success(f"### Predicted Species: **{species}**")
    
   