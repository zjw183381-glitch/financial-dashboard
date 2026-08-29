import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from calculations import (
    calculate_daily_returns,
    calculate_total_return,
    calculate_average_return,
    calculate_volatility,
    calculate_moving_average,
)


def create_test_data():
    return pd.DataFrame({
        "Close": [100, 105, 110, 108, 115]
    })


def test_daily_returns():
    data = create_test_data()
    result = calculate_daily_returns(data)

    assert len(result) == 4
    assert round(result.iloc[0], 2) == 0.05


def test_total_return():
    data = create_test_data()
    result = calculate_total_return(data)

    assert round(result, 2) == 0.15


def test_average_return():
    data = create_test_data()
    result = calculate_average_return(data)

    assert result > 0


def test_volatility():
    data = create_test_data()
    result = calculate_volatility(data)

    assert result >= 0


def test_moving_average():
    data = create_test_data()
    result = calculate_moving_average(data, window=3)

    assert result.iloc[-1] == (110 + 108 + 115) / 3