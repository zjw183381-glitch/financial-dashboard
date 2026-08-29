import os
from dotenv import load_dotenv
from fredapi import Fred

load_dotenv()


FRED_SERIES = {
    "GDP": "GDP",
    "Inflation (CPI)": "CPIAUCSL",
    "Unemployment Rate": "UNRATE",
    "Federal Funds Rate": "FEDFUNDS"
}


def get_fred_client():
    """
    Create and return a FRED API client.
    """
    api_key = os.getenv("FRED_API_KEY")

    if not api_key:
        raise ValueError(
            "FRED_API_KEY is missing. Please add it to your .env file."
        )

    return Fred(api_key=api_key)


def get_economic_indicator(indicator_name, start_date, end_date):
    """
    Retrieve one economic indicator from FRED.
    """
    if indicator_name not in FRED_SERIES:
        raise ValueError("Invalid economic indicator selected.")

    fred = get_fred_client()
    series_id = FRED_SERIES[indicator_name]

    data = fred.get_series(
        series_id,
        observation_start=start_date,
        observation_end=end_date
    )

    if data.empty:
        raise ValueError(
            f"No FRED data found for {indicator_name}."
        )

    return data.dropna()