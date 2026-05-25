from src.tools.finance import get_historical_closes
from src.tools.math_sandbox import execute_math_analysis

TOOL_ROUTER = {
    "get_historical_closes": get_historical_closes,
    "execute_math_analysis": execute_math_analysis
}