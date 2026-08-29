import streamlit as st
from datetime import date, timedelta
from market_data import get_stock_data
from economic_data import get_economic_indicator
from calculations import (
    calculate_daily_returns,
    calculate_total_return,
    calculate_average_return,
    calculate_volatility,
    calculate_moving_average
)
st.title("Financial Market & Economic Dashboard")

st.success("Dashboard is working!")

st.subheader("Stock Selection")

ticker = st.text_input(
    "Enter a stock ticker:",
    value="AAPL"
)

st.write("Selected stock:", ticker.upper())

st.subheader("Date Range")

default_end = date.today()
default_start = default_end - timedelta(days=365)

start_date = st.date_input(
    "Start date",
    value=default_start
)

end_date = st.date_input(
    "End date",
    value=default_end
)

if start_date >= end_date:
    st.error("Start date must be earlier than end date.")
else:
    st.write("Selected period:", start_date, "to", end_date)

    st.subheader("Economic Indicators")

fred_options = [
    "GDP",
    "Inflation (CPI)",
    "Unemployment Rate",
    "Federal Funds Rate"
]

selected_indicators = st.multiselect(
    "Select at least three economic indicators:",
    fred_options,
    default=[
        "GDP",
        "Inflation (CPI)",
        "Unemployment Rate"
    ]
)

for indicator in selected_indicators:
    try:
        economic_data = get_economic_indicator(
            indicator,
            start_date,
            end_date
        )

        st.subheader(indicator)

        latest_value = economic_data.iloc[-1]

        st.metric(
            f"Latest {indicator}",
            f"{latest_value:.2f}"
        )

        st.line_chart(economic_data)
        first_value = economic_data.iloc[0]
        change = latest_value - first_value

        if indicator == "GDP":
            if change > 0:
                st.success(
                    "GDP increased during the selected period, "
                    "indicating overall economic growth."
                )
            else:
                st.warning(
                    "GDP decreased during the selected period, "
                    "which may indicate weaker economic activity."
                )

        elif indicator == "Inflation (CPI)":
            if change > 0:
                st.info(
                    "The CPI increased during the selected period, "
                    "indicating continued upward pressure on consumer prices."
                )
            else:
                st.info(
                    "The CPI decreased during the selected period, "
                    "indicating easing price pressures."
                )

        elif indicator == "Unemployment Rate":
            if change > 0:
                st.warning(
                    "The unemployment rate increased during the selected period, "
                    "suggesting some weakening in the labor market."
                )
            else:
                st.success(
                    "The unemployment rate decreased during the selected period, "
                    "suggesting improvement in the labor market."
                )

    except Exception as e:
        st.warning(f"Could not load {indicator}: {e}")

if len(selected_indicators) < 3:
    st.warning("Please select at least three economic indicators.")
else:
    st.write("Selected indicators:", selected_indicators)

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

st.subheader("Stock Data")

if start_date < end_date and ticker.strip():
    try:
        stock_data = get_stock_data(
            ticker.strip().upper(),
            start_date,
            end_date
        )

        st.success("Stock data loaded successfully!")

        total_return = calculate_total_return(stock_data)
        average_return = calculate_average_return(stock_data)
        volatility = calculate_volatility(stock_data)

        if hasattr(total_return, "iloc"):
            total_return = total_return.iloc[0]

        if hasattr(average_return, "iloc"):
            average_return = average_return.iloc[0]

        if hasattr(volatility, "iloc"):
            volatility = volatility.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Return",
            f"{float(total_return) * 100:.2f}%"
        )

        col2.metric(
            "Average Daily Return",
            f"{float(average_return) * 100:.2f}%"
        )

        col3.metric(
            "Annualized Volatility",
            f"{float(volatility) * 100:.2f}%"
        )

        high_data = stock_data["High"]
        low_data = stock_data["Low"]

        if hasattr(high_data, "iloc") and len(high_data.shape) > 1:
            high_data = high_data.iloc[:, 0]

        if hasattr(low_data, "iloc") and len(low_data.shape) > 1:
            low_data = low_data.iloc[:, 0]

        highest_price = high_data.max()
        lowest_price = low_data.min()

        close_data = stock_data["Close"]

        if hasattr(close_data, "iloc") and len(close_data.shape) > 1:
            close_data = close_data.iloc[:, 0]
        current_price = close_data.dropna().iloc[-1]
        previous_price = close_data.dropna().iloc[-2]
        price_change = current_price - previous_price
        price_change_pct = (price_change / previous_price) * 100
        col_current, col_change = st.columns(2)

        col_current.metric(
            "Current Price",
            f"${float(current_price):.2f}"
        )

        col_change.metric(
            "Price Change",
            f"${float(price_change):.2f}",
            f"{float(price_change_pct):.2f}%"
        )
        col4, col5 = st.columns(2)

        col4.metric(
            "Highest Price",
            f"${float(highest_price):.2f}"
        )

        col5.metric(
            "Lowest Price",
            f"${float(lowest_price):.2f}"
        )

        st.subheader("Historical Price Chart")

        close_data = stock_data["Close"]

        if hasattr(close_data, "iloc") and len(close_data.shape) > 1:
            close_data = close_data.iloc[:, 0]

        st.line_chart(close_data)
        st.subheader("Moving Average Comparison")

        moving_average_data = close_data.to_frame(name="Close")
        moving_average_data["20-Day MA"] = close_data.rolling(window=20).mean()
        moving_average_data["50-Day MA"] = close_data.rolling(window=50).mean()

        st.line_chart(moving_average_data)
        st.subheader("Daily Returns Chart")

        daily_returns = close_data.pct_change().dropna() * 100

        st.line_chart(daily_returns)

        st.subheader("Trading Volume Chart")

        volume_data = stock_data["Volume"]

        if hasattr(volume_data, "iloc") and len(volume_data.shape) > 1:
            volume_data = volume_data.iloc[:, 0]

        st.bar_chart(volume_data)

        st.write(stock_data.tail())

        

    except ValueError as e:
        st.error(str(e))

    except Exception as e:
        st.error(f"Unable to load stock data: {e}")

        st.divider()
st.header("Stock Comparison")
comparison_tickers = st.text_input(
    "Enter stock symbols to compare (separated by commas):",
    "AAPL, MSFT, GOOGL"
)

tickers_list = [
    symbol.strip().upper()
    for symbol in comparison_tickers.split(",")
    if symbol.strip()
]

comparison_data = {}

for symbol in tickers_list:
    try:
        data = get_stock_data(symbol, start_date, end_date)
        close_prices = data["Close"]

        if hasattr(close_prices, "iloc") and len(close_prices.shape) > 1:
            close_prices = close_prices.iloc[:, 0]

        comparison_data[symbol] = close_prices

    except Exception:
        st.warning(f"Could not load data for {symbol}.")

if comparison_data:
    st.subheader("Normalized Stock Performance")

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df = comparison_df.dropna(how="all")

    normalized_df = comparison_df / comparison_df.ffill().bfill().iloc[0] * 100

    st.line_chart(normalized_df)

    st.subheader("Comparison Summary")

    summary_rows = []

    for symbol in comparison_df.columns:
        prices = comparison_df[symbol].dropna()

        if len(prices) >= 2:
            stock_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100

            summary_rows.append({
                "Ticker": symbol,
                "Total Return (%)": round(float(stock_return), 2)
            })

    if summary_rows:
        summary_df = pd.DataFrame(summary_rows)
        st.dataframe(summary_df, hide_index=True)  

        st.subheader("S&P 500 Benchmark Comparison")

    try:
        benchmark_data = get_stock_data("^GSPC", start_date, end_date)
        benchmark_close = benchmark_data["Close"]

        if hasattr(benchmark_close, "iloc") and len(benchmark_close.shape) > 1:
            benchmark_close = benchmark_close.iloc[:, 0]

        benchmark_close = benchmark_close.dropna()

        if len(benchmark_close) >= 2:
            benchmark_return = (
                benchmark_close.iloc[-1] / benchmark_close.iloc[0] - 1
            ) * 100

            best_stock = max(
                summary_rows,
                key=lambda x: x["Total Return (%)"]
            )

            col_benchmark1, col_benchmark2 = st.columns(2)

            col_benchmark1.metric(
                "S&P 500 Return",
                f"{float(benchmark_return):.2f}%"
            )

            col_benchmark2.metric(
                "Best Performing Stock",
                best_stock["Ticker"],
                f'{best_stock["Total Return (%)"]:.2f}%'
            )

            st.subheader("Investment Analysis")

        best_return = best_stock["Total Return (%)"]
        outperformance = best_return - float(benchmark_return)

        if outperformance > 0:
            st.success(
                f"{best_stock['Ticker']} was the best-performing stock "
                f"with a {best_return:.2f}% return. It outperformed the "
                f"S&P 500 by {outperformance:.2f} percentage points."
            )
        else:
            st.info(
                f"The S&P 500 outperformed the selected stocks. "
                f"The best selected stock was {best_stock['Ticker']} "
                f"with a {best_return:.2f}% return."
            )
        st.subheader("Risk & Performance Analysis")

        selected_return = float(total_return) * 100
        selected_volatility = float(volatility) * 100

        risk_adjusted_return = (
            selected_return / selected_volatility
            if selected_volatility != 0
            else 0
        )

        risk_col1, risk_col2 = st.columns(2)

        risk_col1.metric(
            "Return / Volatility Ratio",
            f"{risk_adjusted_return:.2f}"
        )

        if selected_volatility < 20:
            risk_level = "Low"
        elif selected_volatility < 35:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        risk_col2.metric(
            "Risk Level",
            risk_level
        )

        if selected_return > float(benchmark_return):
            st.info(
                f"The selected stock returned {selected_return:.2f}% "
                f"with {selected_volatility:.2f}% annualized volatility. "
                f"It outperformed the S&P 500 during the selected period."
            )
        else:
            st.info(
                f"The selected stock returned {selected_return:.2f}% "
                f"with {selected_volatility:.2f}% annualized volatility. "
                f"It underperformed the S&P 500 during the selected period."
            )
    except Exception as e:
        st.warning(f"Could not load S&P 500 benchmark: {e}")      