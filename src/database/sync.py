import argparse
import yfinance as yf
from src.database.connection import get_db_cursor

TICKERS = ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN", "TSLA", "META"]

def sync_ticker(ticker: str, period: str = "2y") -> int:
    """Download real OHLCV from yfinance and insert into market_candles."""
    print(f"  Downloading {ticker} ({period}) from yfinance...")
    df = yf.download(ticker, period=period, progress=False)
    
    if df.empty:
        print(f"  WARNING: No data returned for {ticker}")
        return 0
    
    inserted = 0
    with get_db_cursor() as cursor:
        for idx, row in df.iterrows():
            timestamp = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
            cursor.execute(
                """INSERT OR IGNORE INTO market_candles
                   (ticker, timestamp, open, high, low, close, volume)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    ticker.upper(),
                    timestamp,
                    round(row["Open"].item(), 2),
                    round(row["High"].item(), 2),
                    round(row["Low"].item(), 2),
                    round(row["Close"].item(), 2),
                    int(row["Volume"].item()),
                ),
            )
            inserted += 1
    print(f"  {ticker}: {inserted} rows processed")
    return inserted

def sync_all_tickers():
    total = 0
    for t in TICKERS:
        total += sync_ticker(t)
    print(f"\nSync complete. {total} total rows across {len(TICKERS)} tickers.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync market data from yfinance to local database.")
    parser.add_argument("--ticker", type=str, help="Sync a single ticker")
    parser.add_argument("--all", action="store_true", help="Sync all default tickers")
    args = parser.parse_args()
    
    if args.ticker:
        sync_ticker(args.ticker)
    elif args.all:
        sync_all_tickers()
    else:
        print("Usage: python -m src.database.sync [--ticker AAPL | --all]")
