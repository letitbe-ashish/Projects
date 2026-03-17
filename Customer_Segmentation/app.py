import streamlit as st
import pandas as pd
import numpy as np
import pickle
st.set_page_config(layout="wide")

@st.cache_resource
def load_model():
    with open('kmeans_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

@st.cache_data
def load_data():
    return pd.read_csv('cluster_insights.csv')

kmeans, scaler = load_model()
clusters = load_data()
st.title("Customer Segmentation Prediction")

st.subheader("Enter Customer Details")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 18, 100, 30)
with col2:
    income = st.number_input("Annual Income (k$)", 1, 200, 50)
with col3:
    spending = st.number_input("Spending Score (1-100)", 1, 100, 50)

if st.button("Predict Segment", type="primary"):
 
    input_data = scaler.transform([[age, income, spending]])
    cluster = kmeans.predict(input_data)[0]
    segment = clusters[clusters['Cluster'] == cluster].iloc[0]
   
    st.success(f"**Predicted Segment: {segment['Segment_Name']}**")
st.markdown("---")
st.subheader("All Customer Segments")
st.dataframe(clusters, use_container_width=True, hide_index=True)
