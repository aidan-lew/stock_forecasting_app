import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from forecasting_backend import get_stock_data, forecast_prices  # your existing functions

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Market Forecast",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"
)

# ---- CUSTOM THEME ----
st.markdown("""
    <style>
        body {
            background-color: #0f1117;
            color: #ffffff;
        }
        .stApp {
            background-color: #0f1117;
        }
        .css-18e3th9 {
            background-color: #0f1117;
        }
        .css-1d391kg, .css-1offfwp {
            color: #00ffb3;
        }
        h1, h2, h3, h4 {
            color: #00ffb3;
        }
        .stButton>button {
            background-color: #00ffb3;
            color: black;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---- TITLE ----
st.title("💹 Financial Forecasting Dashboard")
st.subheader("Confident. Professional. Data-Driven.")

# ---- SIDEBAR INPUTS ----
with st.sidebar:
    st.header("🔍 Forecast Parameters")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")
    days = st.number_input("Days to Forecast", min_value=1, max_value=365, value=30)
    submitted = st.button("Run Forecast")

# ---- MAIN LOGIC ----
if submitted:
    with st.spinner("Fetching data and running forecast..."):

        # Call your backend functions
        historical_data = get_stock_data(ticker)
        forecast_df = forecast_prices(ticker, days)

        st.success("Forecast complete!")

        # ---- HISTORICAL DATA DISPLAY ----
        st.subheader(f"📉 Historical Prices for {ticker}")
        st.line_chart(historical_data.set_index("Date")["Close"])

        # ---- FORECASTED PRICES ----
        st.subheader(f"🔮 {days}-Day Forecast for {ticker}")
        st.line_chart(forecast_df.set_index("Date")["Forecast"])

        # ---- NUMERIC RESULTS ----
        st.subheader("📊 Forecast Data")
        st.dataframe(forecast_df)

