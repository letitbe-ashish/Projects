#  House Price Prediction App

A machine learning-powered web application built with Streamlit that predicts house prices using a LightGBM model. The app provides an intuitive interface for users to input property details and receive instant price predictions.

##  Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

##  Features

- **Interactive Web Interface**: Built with Streamlit for a smooth user experience
- **Real-time Predictions**: Instant house price predictions based on property features
- **Multiple Input Parameters**: 
  - Property size (sq ft)
  - Number of bedrooms
  - Location (CityA, CityB, CityC, CityD)
  - Property condition (New, Good, Fair, Poor)
  - Property type (Single Family, Townhouse, Condominium)
  - Sale date
- **LightGBM Model**: Trained machine learning model with high accuracy
- **Clean UI**: User-friendly interface with organized input sections



## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/house-price-prediction.git
cd house-price-prediction
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Ensure model files are present**
Make sure `best_lgbm_model.pkl` and `ordinal_encoder.pkl` are in the project directory.

##  Usage

1. **Run the Streamlit app**
```bash
streamlit run app.py
```

2. **Open your browser**
The app should automatically open at `http://localhost:8501`

3. **Input property details**
- Enter the property size and number of bedrooms
- Select the location, condition, and property type
- Choose the sale date
- Click "Predict Price" to get the estimated price

##  Model Details

### Training Process
The model was trained using the following approach:
- **Algorithm**: LightGBM (Light Gradient Boosting Machine)
- **Data**: Historical house sale data from multiple cities
- **Features**: Size, Bedrooms, Location, Condition, Type, Sale Year, Sale Month
- **Preprocessing**: 
  - Ordinal encoding for categorical variables
  - Feature engineering from date fields

### Model Performance
The model training and evaluation process is documented in `house_price(q1)v2.ipynb`.

##  Project Structure

```
House_price_prediction_v4/
│
├── app.py                      # Main Streamlit application
├── best_lgbm_model.pkl         # Trained LightGBM model
├── ordinal_encoder.pkl         # Fitted ordinal encoder
├── house_price(q1)v2.ipynb    # Model training notebook
├── data.xlsx                   # Training dataset
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Technologies Used

- **Python 3.x**: Core programming language
- **Streamlit**: Web application framework
- **LightGBM**: Gradient boosting framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning utilities
- **Pickle**: Model serialization

## Dataset

The dataset (`data.xlsx`) contains historical house sale records with the following features:
- Property size
- Number of bedrooms
- Location
- Property condition
- Property type
- Sale date
- Sale price

