import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(ticker):
    df = yf.download(ticker, period="6mo")
    df.reset_index(inplace=True)
    return df[["Date", "Close"]]

def forecast_prices(ticker, days):
    # Dummy forecast for example
    last_date = pd.Timestamp.today()
    future_dates = pd.date_range(start=last_date, periods=days)
    forecast = np.random.normal(200, 5, days)
    df = pd.DataFrame({"Date": future_dates, "Forecast": forecast})
    return df
