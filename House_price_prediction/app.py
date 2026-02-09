import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="House Price Predictor",
    layout="wide"
)

# Title and description
st.title("House Price Prediction App")
st.markdown("### Predict house prices using LightGBM model")

# Load the trained model and encoder
@st.cache_resource
def load_model():
    try:
        with open('best_lgbm_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('ordinal_encoder.pkl', 'rb') as f:
            encoder = pickle.load(f)
        return model, encoder
    except FileNotFoundError:
        st.error("Model files not found! Please ensure 'best_lgbm_model.pkl' and 'ordinal_encoder.pkl' are in the same directory.")
        return None, None

model, encoder = load_model()

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Property Details")

    col_left, col_right = st.columns(2)

    with col_left:
        size = st.number_input(
            "Size (sq ft)",
            min_value=1,
            value=2000,
            step=100,
           
        )

        bedrooms = st.number_input(
            "Number of Bedrooms",
            min_value=0,
            value=3,
            step=1
        )

       
        location = st.selectbox(
            "Location",
            options=['CityA', 'CityB', 'CityC', 'CityD'],
       
        )

    with col_right:
        condition = st.selectbox(
            "Property Condition",
            options=['New', 'Good', 'Fair', 'Poor'],
       
        )
        
        property_type = st.selectbox(
            "Property Type",
            options=['Single Family', 'Townhouse', 'Condominium'],
     
        )

        

        date_sold = st.date_input(
            "Date Sold",
            value=datetime.now(),
            max_value=datetime.now(),
       
        )

        

if st.button("Predict Price", type="primary"):
    if model is not None and encoder is not None:
        sale_year = date_sold.year
        sale_month = date_sold.month
        
        # Prepare input data
        input_data = pd.DataFrame({
            'Size': [size],
            'Bedrooms': [bedrooms],
            'Sale_Year': [sale_year],
            'Sale_Month': [sale_month],
            'Location': [location],
            'Condition': [condition],
            'Type': [property_type]
            
        })
        
        # Separate numerical and categorical
        numerical_cols = ['Size', 'Bedrooms', 'Sale_Year','Sale_Month']
        categorical_cols = ['Location', 'Condition','Type']
        
        # Encode categorical variables
        encoded_cats = encoder.transform(input_data[categorical_cols])
        encoded_df = pd.DataFrame(encoded_cats, columns=categorical_cols)
        
        # Combine numerical and encoded categorical
        final_input = pd.concat([
            input_data[numerical_cols].reset_index(drop=True),
            encoded_df.reset_index(drop=True)
        ], axis=1)
        
        # Apply scaling (IMPORTANT!)
      
        
        # Make prediction (log-transformed)
        prediction = model.predict(final_input)[0]
        
        # Inverse log transformation
        
        
        # Display results
        msg_col, _ = st.columns([1, 5])
        with msg_col:
         st.success("Prediction Completed")

        
        # Create three columns for results
        result_col1= st.columns(1)[0]
        
        with result_col1:
            st.metric(
                label="Predicted Price",
                value=f"₨ {prediction:,.2f}"
            )
        
                
       
    else:
        st.error("Model not loaded. Please check if model files exist.")

