import random
import datetime
from src.database.connection import init_database, get_db_cursor

TICKERS = {
    "AAPL": 170.0,
    "NVDA": 900.0,
    "MSFT": 415.0,
    "GOOGL": 170.0,
    "AMZN": 200.0,
    "TSLA": 240.0,
    "META": 500.0,
}
TRADING_DAYS = 60
START_DATE = datetime.date.today() - datetime.timedelta(days=90)

def _trading_dates(start, count):
    dates = []
    current = start
    while len(dates) < count:
        if current.weekday() < 5:
            dates.append(current)
        current += datetime.timedelta(days=1)
    return dates

def _generate_ohlcv(base_price, dates):
    random.seed(hash(base_price * 1000 + dates[0].toordinal()))
    rows = []
    price = base_price
    for d in dates:
        daily_return = random.gauss(0.0008, 0.018)
        close = round(price * (1.0 + daily_return), 2)
        open_p = round(close * random.uniform(0.998, 1.002), 2)
        high = round(max(open_p, close) * random.uniform(1.001, 1.018), 2)
        low = round(min(open_p, close) * random.uniform(0.982, 0.999), 2)
        volume = int(10 ** random.uniform(6.5, 8.0))
        rows.append((d.isoformat(), open_p, high, low, close, volume))
        price = close
    return rows

def main():
    print("Initializing database schema...")
    init_database()

    dates = _trading_dates(START_DATE, TRADING_DAYS)

    with get_db_cursor() as cursor:
        for ticker, base_price in TICKERS.items():
            print(f"  Generating {TRADING_DAYS} candles for {ticker}...")
            rows = _generate_ohlcv(base_price, dates)
            for d_iso, open_p, high, low, close, volume in rows:
                cursor.execute(
                    """INSERT OR IGNORE INTO market_candles
                       (ticker, timestamp, open, high, low, close, volume)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (ticker, d_iso, open_p, high, low, close, volume),
                )
        
        print("  Initializing account balance...")
        cursor.execute("SELECT COUNT(*) FROM account_balance")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO account_balance (cash, equity) VALUES (100000.00, 0.00)")
    
    print(f"Seed complete. Database: 7 tickers x {TRADING_DAYS} candles each.")

if __name__ == "__main__":
    main()