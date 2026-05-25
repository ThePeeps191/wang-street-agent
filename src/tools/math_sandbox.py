import json
import math

def execute_math_analysis(prices_json: str, metric: str) -> str:
    """Computes deterministic quantitative analytics over raw data vectors."""
    try:
        data = json.loads(prices_json)
        # Handle cases where the tool receives the full dictionary wrapper or a direct list
        prices = data.get("closes", []) if isinstance(data, dict) else data
        
        if not prices or not isinstance(prices, list):
            return json.dumps({"error": "Invalid price vector data array layout."})
            
        if metric == "volatility":
            mean = sum(prices) / len(prices)
            variance = sum((x - mean) ** 2 for x in prices) / len(prices)
            std_dev = math.sqrt(variance)
            return json.dumps({"metric": "volatility", "value": round(std_dev, 4)})
            
        elif metric == "momentum":
            delta = prices[-1] - prices[0]
            pct_change = (delta / prices[0]) * 100
            return json.dumps({"metric": "momentum_pct", "value": round(pct_change, 2)})
            
        return json.dumps({"error": f"Analytical metric algorithm '{metric}' is unsupported."})
    except Exception as e:
        return json.dumps({"error": f"Math execution failed: {str(e)}"})