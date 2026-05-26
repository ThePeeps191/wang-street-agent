from src.tools.finance import get_historical_closes
from src.tools.market_data import get_full_ohlcv, fetch_realtime_quote
from src.tools.indicators import (
    calculate_volatility,
    compute_rsi,
    run_linear_regression,
    calculate_expected_value,
)

TOOL_ROUTER = {
    "get_historical_closes":    get_historical_closes,
    "get_full_ohlcv":           get_full_ohlcv,
    "fetch_realtime_quote":     fetch_realtime_quote,
    "calculate_volatility":     calculate_volatility,
    "compute_rsi":              compute_rsi,
    "run_linear_regression":    run_linear_regression,
    "calculate_expected_value": calculate_expected_value,
}