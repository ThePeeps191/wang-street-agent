import os
import openai

def get_llm_client() -> openai.OpenAI:
    """Initializes and returns an OpenAI-compatible DeepSeek API client."""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("Missing DEEPSEEK_API_KEY in environment variables. Please set it before running the agent.")
        
    return openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

def generate_agent_reasoning(messages: list) -> str:
    """Executes a text completion turn against DeepSeek using a deterministic layout."""
    model = os.getenv("DEEPSEEK_MODEL")
    if not model:
        raise ValueError("Missing DEEPSEEK_MODEL in environment variables. Please set it before running the agent.")
    
    client = get_llm_client()
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1         # Maintained low variance for consistent syntax tool routing
    )
    
    return response.choices[0].message.content