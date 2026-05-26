import json
import numpy as np

def calculate_volatility(price_vector: list) -> str:
    """Computes historical standard deviation over a price array."""
    try:
        if not price_vector or not isinstance(price_vector, list):
            return json.dumps({"error": "price_vector must be a non-empty list of floats."})
        arr = np.array(price_vector, dtype=np.float64)
        std = float(np.std(arr))
        return json.dumps({
            "metric": "volatility",
            "sample_size": len(arr),
            "value": round(std, 4)
        })
    except Exception as e:
        return json.dumps({"error": f"Volatility calculation failed: {str(e)}"})

def compute_rsi(price_vector: list, periods: int) -> str:
    """Computes the Relative Strength Index (RSI) using Wilder's smoothing."""
    try:
        if not price_vector or not isinstance(price_vector, list):
            return json.dumps({"error": "price_vector must be a non-empty list of floats."})
        if periods < 2:
            return json.dumps({"error": "periods must be at least 2."})
        if len(price_vector) < periods + 1:
            return json.dumps({"error": f"Need at least {periods + 1} price points, got {len(price_vector)}."})
        
        arr = np.array(price_vector, dtype=np.float64)
        deltas = np.diff(arr)
        
        gains = np.where(deltas > 0, deltas, 0.0)
        losses = np.where(deltas < 0, -deltas, 0.0)
        
        avg_gain = np.mean(gains[:periods])
        avg_loss = np.mean(losses[:periods])
        
        if avg_loss == 0:
            return json.dumps({"metric": "rsi", "periods": periods, "value": 100.0})
        
        for i in range(periods, len(deltas)):
            avg_gain = (avg_gain * (periods - 1) + gains[i]) / periods
            avg_loss = (avg_loss * (periods - 1) + losses[i]) / periods
        
        rs = avg_gain / avg_loss if avg_loss != 0 else float("inf")
        rsi = 100.0 - (100.0 / (1.0 + rs))
        
        return json.dumps({
            "metric": "rsi",
            "periods": periods,
            "value": round(rsi, 2)
        })
    except Exception as e:
        return json.dumps({"error": f"RSI calculation failed: {str(e)}"})

def run_linear_regression(independent_vector: list, dependent_vector: list) -> str:
    """Fits an OLS linear trend line and returns slope, intercept, R-squared, and predicted velocity."""
    try:
        if not independent_vector or not dependent_vector:
            return json.dumps({"error": "Both vectors must be non-empty lists."})
        if len(independent_vector) != len(dependent_vector):
            return json.dumps({"error": f"Vector length mismatch: {len(independent_vector)} vs {len(dependent_vector)}."})
        
        x = np.array(independent_vector, dtype=np.float64)
        y = np.array(dependent_vector, dtype=np.float64)
        
        A = np.vstack([x, np.ones_like(x)]).T
        (slope, intercept), residuals, rank, singular = np.linalg.lstsq(A, y, rcond=None)
        
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
        
        predicted_velocity = float(slope * x[-1] * (1 + slope / intercept)) if intercept != 0 else float(slope * x[-1])
        
        return json.dumps({
            "slope": round(float(slope), 6),
            "intercept": round(float(intercept), 4),
            "r_squared": round(float(r_squared), 4),
            "predicted_velocity": round(predicted_velocity, 4)
        })
    except Exception as e:
        return json.dumps({"error": f"Linear regression failed: {str(e)}"})

def calculate_expected_value(probability_win: float, win_size: float, loss_size: float) -> str:
    """Computes EV = (P_win * W) - ((1 - P_win) * L) and returns a risk verdict."""
    try:
        p_win = float(probability_win)
        w = float(win_size)
        l = float(loss_size)

        if p_win < 0 or p_win > 1:
            return json.dumps({"error": "probability_win must be between 0 and 1."})
        if w < 0:
            return json.dumps({"error": "win_size must be non-negative."})
        if l < 0:
            return json.dumps({"error": "loss_size must be non-negative."})
        
        ev = p_win * w - (1.0 - p_win) * l
        risk_ratio = w / l if l != 0 else float("inf")
        
        if ev > 0:
            verdict = "positive"
        elif ev == 0:
            verdict = "neutral"
        else:
            verdict = "negative"
        
        return json.dumps({
            "expected_value": round(ev, 4),
            "risk_ratio": round(risk_ratio, 4),
            "verdict": verdict
        })
    except Exception as e:
        return json.dumps({"error": f"EV calculation failed: {str(e)}"})

