import json
import yfinance as yf

def get_full_ohlcv(ticker: str) -> str:
    """Fetches full OHLCV bars from yfinance for the given ticker."""
    try:
        t = yf.Ticker(ticker.upper())
        df = t.history(period="2y")
        if df.empty:
            return json.dumps({"error": f"No data returned from yfinance for {ticker.upper()}"})
        
        opens = [round(float(v), 2) for v in df["Open"].tolist()]
        highs = [round(float(v), 2) for v in df["High"].tolist()]
        lows = [round(float(v), 2) for v in df["Low"].tolist()]
        closes = [round(float(v), 2) for v in df["Close"].tolist()]
        volumes = [int(v) for v in df["Volume"].tolist()]
        
        return json.dumps({
            "ticker": ticker.upper(),
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "count": len(closes),
        })
    except Exception as e:
        return json.dumps({"error": f"yfinance OHLCV fetch failed: {str(e)}"})

def fetch_realtime_quote(ticker: str) -> str:
    """Fetches a real-time bid/ask/last quote from yfinance."""
    try:
        t = yf.Ticker(ticker.upper())
        info = t.info
        
        bid = info.get("bid")
        ask = info.get("ask")
        last = info.get("regularMarketPrice") or info.get("currentPrice") or info.get("previousClose")
        
        if not last:
            df = t.history(period="1d")
            if not df.empty:
                last = round(float(df["Close"].iloc[-1]), 2)
        
        if not bid:
            bid = round(float(last or 0) * 0.999, 2) if last else None
        if not ask:
            ask = round(float(last or 0) * 1.001, 2) if last else None
        
        spread = round(float((ask or 0) - (bid or 0)), 4) if bid and ask else None
        
        return json.dumps({
            "ticker": ticker.upper(),
            "bid": bid,
            "ask": ask,
            "last": last,
            "spread": spread,
        })
    except Exception as e:
        return json.dumps({"error": f"yfinance quote fetch failed: {str(e)}"})