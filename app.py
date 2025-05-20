import streamlit as st

st.set_page_config(
    page_title="Stock Forecast App",
    page_icon="📈",
    layout="wide",
)

st.title("💼 Welcome to the Stock Forecast App")
st.markdown("""
This app provides **stock price forecasts** using a GRU neural network and Monte Carlo simulations.  
Navigate to the **Forecasts** page from the sidebar to begin forecasting.

**Theme**: Professional • Confident • Minimal • Financial
""")
