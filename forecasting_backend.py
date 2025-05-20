from data.data_fetcher import get_numeric_data
from model.forecast_model import gru_forecast

def run_forecasting_pipeline(ticker: str, forecast_days: int):
    df = get_numeric_data(ticker)
    historical, mc_simulations, mc_average = gru_forecast("Close", df, forecast_days)
    return historical, mc_simulations, mc_average
