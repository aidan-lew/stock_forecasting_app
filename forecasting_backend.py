import yfinance as yf
import pandas as pd
import numpy as np

def get_numeric_data(ticker):
    period = '3mo'
    interval = "1h"
    data = yf.download(tickers=ticker, period=period, interval=interval, group_by='ticker')
    data = data.stack(level=0).reset_index()
    data.rename(columns={'level_1': 'Ticker'}, inplace=True)

    # Moving Averages
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    data['MA_200'] = data['Close'].rolling(window=200).mean()

    # RSI
    delta = data['Close'].diff(1)
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.rolling(window=14).mean()
    roll_down = down.rolling(window=14).mean().abs()
    RS = roll_up / roll_down
    data['RSI'] = 100.0 - (100.0 / (1.0 + RS))

    # MACD
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    numeric_df = data.select_dtypes(include=['number'])
    numeric_df['Date'] = data['Datetime']
    numeric_df['Ticker'] = data['Ticker']

    return numeric_df

def forecast_prices(ticker, days):
    # Dummy forecast for demonstration
    last_date = pd.Timestamp.today()
    future_dates = pd.date_range(start=last_date, periods=days)
    forecast = np.random.normal(loc=200, scale=5, size=days)
    df = pd.DataFrame({"Date": future_dates, "Forecast": forecast})
    return df
