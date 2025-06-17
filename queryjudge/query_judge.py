import os

from ollama import ChatResponse
from ollama import Client

def read_txt_file(file_path) -> str:
    """Read the content of a text file and return it as a string."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, "r") as f:
        return f.read().strip()


def build_messages(system_prompt: str,  user_prompt: str):
    """Build the prompt by combining the system prompt and few-shot examples."""
    return [
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': user_prompt
        }
    ]

def judge_sql_responses(sql_responses: list[str], user_nl_query: str, processed_nl_query: str, database_schema: str, model: str = 'gemma3:4b', host: str = 'http://localhost:11434') -> str:
    """Process the natural language query to a structured database query."""
    system_prompt = read_txt_file('system_prompt.txt')
    user_prompt = read_txt_file('user_prompt.txt')
    response_template = read_txt_file('response_template.txt')
    
    user_prompt = user_prompt.replace('<SCHEMA>', database_schema)
    templates =  [
        response_template
        .replace('<RESPONSE_NUMBER>', str(i))
        .replace('<GENERATED_SQL>', sql)
        .replace('<USER_PROMPT>', user_nl_query)
        .replace('<PROCESSED_QUERY>', processed_nl_query)
        for i,sql in enumerate(sql_responses)
    ]
    
    templates_str = '\n\n'.join(templates)
    # replace user prompt placeholder with the actual processed query
    user_prompt = user_prompt.replace('<RESPONSES>', templates_str)
    messages = build_messages(system_prompt, user_prompt)
        
        
    client = Client(
        host=host,
        headers={'Content-Type': 'application/json'},
    )
    response: ChatResponse = client.chat(
        model=model,
        messages=messages,
        format={
            "type": "object",
            "properties": {
                "thinking": {"type": "string"},
                "choice": {"enum": [f"Response {i}" for i in range(len(sql_responses))]}
            },
            "required": ["choice"]
        },
        options={
            # 'temperature': 0.1
            'num_ctx': 40960
        }
    )
    
    
    return response.message.content

