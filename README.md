# Financial Market & Economic Dashboard

## Project Overview

This project is an interactive financial market and economic dashboard built with Python and Streamlit.

It allows users to analyze stock performance, compare multiple stocks, compare investments with the S&P 500, and examine important U.S. economic indicators using FRED data.

## Main Features

- Stock price analysis
- Total return calculation
- Average daily return calculation
- Annualized volatility analysis
- Historical price charts
- Moving average comparison
- Daily returns and trading volume charts
- Multiple stock comparison
- S&P 500 benchmark comparison
- Investment and risk analysis
- FRED economic indicator analysis

## Economic Indicators

The dashboard uses Federal Reserve Economic Data (FRED) to analyze important U.S. economic indicators.

The indicators include:

- GDP
- Inflation (CPI)
- Unemployment Rate
- Federal Funds Rate

## Data Sources

This project uses the following data sources:

- Yahoo Finance for stock market data
- Federal Reserve Economic Data (FRED) for economic indicators
- S&P 500 data for market benchmark comparison

## Technologies Used

- Python
- Streamlit
- Pandas
- yfinance
- fredapi
- python-dotenv
- Git
- GitHub

## Project Structure

financial-dashboard/

- app.py - Main Streamlit dashboard
- market_data.py - Retrieves stock market data
- calculations.py - Performs financial calculations
- economic_data.py - Retrieves FRED economic data
- requirements.txt - Required Python packages
- .gitignore - Protects private files from GitHub
- README.md - Project documentation

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## FRED API Configuration

Create a `.env` file inside the project folder.

Add your FRED API key:

```text
FRED_API_KEY=your_fred_api_key
```

The `.env` file is excluded from GitHub to protect the API key.