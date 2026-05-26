CREATE TABLE IF NOT EXISTS market_candles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL,
    UNIQUE(ticker, timestamp)
);

CREATE INDEX IF NOT EXISTS idx_market_candles_ticker ON market_candles(ticker);
CREATE INDEX IF NOT EXISTS idx_market_candles_timestamp ON market_candles(timestamp);

CREATE TABLE IF NOT EXISTS portfolio_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    transaction_id TEXT NOT NULL UNIQUE,
    ticker TEXT NOT NULL,
    action TEXT NOT NULL CHECK(action IN ('BUY', 'SELL')),
    shares REAL NOT NULL,
    price REAL NOT NULL,
    total_cost REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS account_balance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    cash REAL NOT NULL DEFAULT 100000.00,
    equity REAL NOT NULL DEFAULT 0.00
);