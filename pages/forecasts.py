import streamlit as st
import matplotlib.pyplot as plt
from forecasting_backend import run_forecasting_pipeline

st.title("📈 Forecast Stock Prices")

ticker = st.text_input("Enter Stock Ticker", value="AAPL")
forecast_days = st.number_input("Days to Forecast", min_value=1, max_value=60, value=10, step=1)

if st.button("Run Forecast"):
    st.subheader(f"Running Forecast for {ticker}...")

    historical, all_simulations, avg_forecast = run_forecasting_pipeline(ticker, forecast_days)

    st.subheader("📊 Historical and Forecasted Prices")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(historical, label="Historical Close", color="white")

    for sim in all_simulations:
        ax.plot(range(len(historical), len(historical) + len(sim)), sim, color='gray', alpha=0.2)

    ax.plot(range(len(historical), len(historical) + len(avg_forecast)), avg_forecast, label="Forecast (MC Avg)", color="cyan", linewidth=2)

    ax.set_facecolor("black")
    fig.patch.set_facecolor('black')
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig)

    st.markdown("### 📉 Forecasted Values")
    st.write(avg_forecast)
