import sys

def log_agent_step(turn: int, thought: str):
    print(f"\n{'='*60}\n[WANG STREET AGENT] | TURN #{turn} REASONING:\n{'='*60}")
    print(thought)

def log_tool_action(name: str, args: dict):
    print(f"[INTERCEPTOR] Running Tool: '{name}'")
    print(f"              Arguments: {args}")

def log_tool_success(result: str):
    print(f"[SANDBOX RETURN]: {result}\n")

def log_error(msg: str):
    print(f"[SYSTEM ERROR]: {msg}", file=sys.stderr)
