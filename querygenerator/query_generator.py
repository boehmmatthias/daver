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

def get_database_query(processed_nl_query: str, database_schema: str, model: str = 'gemma3:4b', host: str = 'http://localhost:11434') -> str:
    """Process the natural language query to a structured database query."""
    system_prompt = read_txt_file('system_prompt.txt')
    user_prompt = read_txt_file('user_prompt.txt')
    # replace user prompt placeholder with the actual processed query
    user_prompt = user_prompt.replace('<NLQUERY>', processed_nl_query)
    user_prompt = user_prompt.replace('<SCHEMA>', database_schema)
    messages = build_messages(system_prompt, user_prompt)
    client = Client(
        host=host,
        headers={'Content-Type': 'application/json'},
    )
    response: ChatResponse = client.chat(
        model=model,
        messages=messages,
        stream=False,
        options={
            'temperature': 0.2
        }
    )
    return response.message.content

