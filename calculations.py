import pandas as pd


def get_close_prices(data):
    """
    Extract closing prices as a one-dimensional Series.
    """
    close_prices = data["Close"]

    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]

    return close_prices.dropna()


def calculate_daily_returns(data):
    """
    Calculate daily percentage returns from closing prices.
    """
    close_prices = get_close_prices(data)
    return close_prices.pct_change().dropna()


def calculate_total_return(data):
    """
    Calculate total return over the selected period.
    """
    close_prices = get_close_prices(data)

    if len(close_prices) < 2:
        return 0.0

    first_price = close_prices.iloc[0]
    last_price = close_prices.iloc[-1]

    return (last_price / first_price) - 1


def calculate_average_return(data):
    """
    Calculate average daily return.
    """
    daily_returns = calculate_daily_returns(data)

    if daily_returns.empty:
        return 0.0

    return daily_returns.mean()


def calculate_volatility(data):
    """
    Calculate annualized volatility from daily returns.
    """
    daily_returns = calculate_daily_returns(data)

    if daily_returns.empty:
        return 0.0

    return daily_returns.std() * (252 ** 0.5)


def calculate_moving_average(data, window=20):
    """
    Calculate moving average of closing prices.
    """
    close_prices = get_close_prices(data)
    return close_prices.rolling(window=window).mean()