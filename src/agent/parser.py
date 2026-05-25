import re
import json

def parse_agent_action(text: str):
    """
    Evaluates raw assistant output via regular expressions to parse functional intents.
    Returns (tool_name, parsed_arguments_dict) or (None, None).
    """
    # Intercept tool tags across line breaks
    pattern = r'\[ACTION:\s*(\w+),\s*ARGUMENTS:\s*({.*?})\]'
    match = re.search(pattern, text, re.DOTALL)
    
    if not match:
        return None, None
        
    tool_name = match.group(1).strip()
    raw_arguments = match.group(2).strip()
    
    try:
        arguments_dict = json.loads(raw_arguments)
        return tool_name, arguments_dict
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to compile valid JSON from tool payload: {raw_arguments}. Error: {str(e)}")