import os
import sys
from dotenv import load_dotenv
from src.agent.engine import run_wang_street_loop
from src.utils.helpers import log_error

def main():
    load_dotenv()
    if not os.getenv("DEEPSEEK_API_KEY"):
        log_error("Missing DEEPSEEK_API_KEY in environment variables. Please set it before running the agent.")
        sys.exit(1)
    
    target_objective = (
        "Extract Apple's (AAPL) historical dataset. "
        "Calculate both its volatility and overall momentum profile across those closes, "
        "then output a compiled quantitative synthesis report."
    )
    
    run_wang_street_loop(target_objective)

if __name__ == "__main__":
    main()