import streamlit as st
import pandas as pd
from forecasting_backend import get_numeric_data, forecast_prices

st.set_page_config(
    page_title="Market Forecast",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"
)

# ---- CUSTOM STYLING ----
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

st.title("💹 Financial Forecasting Dashboard")
st.subheader("Confident. Professional. Data-Driven.")

# ---- INPUTS ----
with st.sidebar:
    st.header("🔍 Forecast Parameters")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL")
    days = st.number_input("Days to Forecast", min_value=1, max_value=365, value=30)
    submitted = st.button("Run Forecast")

# ---- MAIN LOGIC ----
if submitted:
    with st.spinner("Fetching data and running forecast..."):

        numeric_df = get_numeric_data(ticker)
        forecast_df = forecast_prices(ticker, days)

        st.success("Forecast complete!")

        # ---- DISPLAY HISTORICAL ----
        st.subheader(f"📉 Historical Close Prices for {ticker}")
        st.line_chart(numeric_df.set_index("Date")["Close"])

        # ---- DISPLAY FORECAST ----
        st.subheader(f"🔮 {days}-Day Forecast for {ticker}")
        st.line_chart(forecast_df.set_index("Date")["Forecast"])

        # ---- DATA TABLES ----
        st.subheader("📊 Forecast Data Table")
        st.dataframe(forecast_df)

        st.subheader("📋 Technical Indicators Snapshot")
        st.dataframe(numeric_df.tail(10))
