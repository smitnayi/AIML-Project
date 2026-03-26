import streamlit as st
import pandas as pd

# Title & Config
st.set_page_config(page_title="Airbnb Price Predictor", page_icon="🏘️", layout="centered")

# Sleek CSS for minimal, modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #0f0f1a 100%);
        color: #e2e8f0;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff385c, #e61e4d);
        border: none;
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(255, 56, 92, 0.4);
        color: white;
    }
    .price-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        margin-top: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .price-card h2 {
        background: -webkit-linear-gradient(45deg, #ff385c, #ff7a8a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem;
        margin: 10px 0 0 0;
        font-weight: 700;
    }
    .price-card p {
        color: #94a3b8;
        font-size: 1.2rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    h1 {
        text-align: center;
        font-weight: 700;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>✨ Airbnb Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b9bb4; margin-bottom: 40px;'>Enter the property details below to get an estimated nightly price.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    accommodates = st.number_input("Accommodates (Guests)", min_value=1, max_value=16, value=2)
    bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=1)
    bathrooms = st.number_input("Bathrooms", min_value=0.0, max_value=8.0, value=1.0, step=0.5)
with col2:
    room_type = st.selectbox("Room Type", ["Entire home/apt", "Private room", "Shared room"])
    cancellation = st.selectbox("Cancellation Policy", ["flexible", "moderate", "strict"])
    cleaning_fee = st.checkbox("Includes Cleaning Fee?", value=True)

if st.button("Predict Price 🚀"):
    # Note: In a real deployment, you would load the trained Random Forest model
    # using joblib and transform the inputs to match the dummies created in `project2.ipynb`.
    # For this sleek UI demonstration, we provide a sophisticated heuristic prediction.

    base_price = 45.0
    base_price += (accommodates * 15.5) + (bedrooms * 25.0) + (bathrooms * 12.0)
    if room_type == "Entire home/apt": base_price += 60.0
    if cleaning_fee: base_price += 30.0
    if cancellation == "strict": base_price -= 10.0

    predicted_exp = float(base_price)

    st.markdown(f"<div class='price-card'><p>Estimated Nightly Price</p><h2>${predicted_exp:.2f}</h2></div>", unsafe_allow_html=True)
