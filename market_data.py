import yfinance as yf
import pandas as pd


def get_stock_data(ticker, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.
    """
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        progress=False
    )

    if data.empty:
        raise ValueError("No stock data found. Please check the ticker symbol.")

    return data