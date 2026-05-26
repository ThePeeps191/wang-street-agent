import json
from src.database.connection import get_db_cursor
from src.database.sync import sync_ticker

def get_historical_closes(ticker: str) -> str:
    """Queries the market_candles table for chronological closing prices.
    Falls back to yfinance sync if no local data exists."""
    ticker_upper = ticker.upper()
    
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT close FROM market_candles WHERE ticker = ? ORDER BY timestamp ASC",
            (ticker_upper,),
        )
        rows = cursor.fetchall()
    
    if not rows:
        sync_ticker(ticker_upper)
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT close FROM market_candles WHERE ticker = ? ORDER BY timestamp ASC",
                (ticker_upper,),
            )
            rows = cursor.fetchall()
    
    if not rows:
        return json.dumps(
            {"error": f"Ticker '{ticker_upper}' not found in database and could not be synced from yfinance."}
        )
    
    closes = [row["close"] for row in rows]
    return json.dumps({"ticker": ticker_upper, "closes": closes})