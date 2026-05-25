from src.agent.prompts import SYSTEM_PROMPT
from src.agent.parser import parse_agent_action
from src.agent.llm_api import generate_agent_reasoning
from src.tools.base import TOOL_ROUTER
from src.utils.helpers import log_agent_step, log_tool_action, log_tool_success, log_error

def run_wang_street_loop(user_objective: str, max_turns: int = 6):
    """Orchestrates the ReAct simulation engine loop."""
    
    # Initialize stateful conversation history arrays
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_objective}
    ]
    
    for turn in range(1, max_turns + 1):
        try:
            thought_output = generate_agent_reasoning(messages)
            log_agent_step(turn, thought_output)
            
            # Track memory trail
            messages.append({"role": "assistant", "content": thought_output})
            
            # Intercept custom execution commands via the regex compiler
            tool_name, tool_args = parse_agent_action(thought_output)
            
            # Action block intercepted
            if tool_name:
                log_tool_action(tool_name, tool_args)
                
                if tool_name in TOOL_ROUTER:
                    # Native look-up map route execution call
                    execution_result = TOOL_ROUTER[tool_name](**tool_args)
                    log_tool_success(execution_result)
                    
                    # Inject sandbox data directly back into the conversational trail
                    messages.append({
                        "role": "user",
                        "content": f"[TOOL EXECUTION RESULT FOR {tool_name}]: {execution_result}"
                    })
                else:
                    err = f"Requested tool '{tool_name}' does not exist in local registry definitions."
                    log_error(err)
                    messages.append({"role": "user", "content": f"[SYSTEM ERROR]: {err}"})
            
            # No action block found means the agent has completed its analytics loop cleanly
            else:
                print("\n[SUMMARY]: Analysis finalized cleanly.")
                return thought_output
                
        except Exception as e:
            error_boundary_msg = f"Failed loop verification step. Trace: {str(e)}"
            log_error(error_boundary_msg)
            messages.append({"role": "user", "content": f"[RUNTIME BOUNDARY EXCEPTION]: {error_boundary_msg}"})
            
    print(f"\n[AGENT HALTED]: Hard cutoff triggered at max iterations ({max_turns}).")
    return None