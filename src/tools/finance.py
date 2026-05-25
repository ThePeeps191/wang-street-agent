import json

def load_database() -> dict:
    """Load a database of historical time-series data."""
    return {
        "AAPL": [170.20, 171.55, 173.10, 172.85, 175.00, 174.20, 178.10, 179.50, 182.41],
        "MSFT": [415.20, 417.00, 412.50, 418.90, 420.10, 421.50],
        "NVDA": [850.10, 862.40, 875.00, 890.20, 882.10, 903.25]
    }

def get_historical_closes(ticker: str) -> str:
    """Mock database lookup for historical time-series data."""
    data_store = load_database()
    
    ticker_upper = ticker.upper()
    if ticker_upper in data_store:
        return json.dumps({"ticker": ticker_upper, "closes": data_store[ticker_upper]})
    return json.dumps({"error": f"Ticker '{ticker_upper}' not found in local datastore."})