from ollama import ChatResponse
from ollama import Client

def read_txt_file(file_path) -> str:
    """Read the content of a text file and return it as a string."""
    with open(file_path, 'r') as file:
        return file.read().strip()


def build_messages(system_prompt: str, few_shot_examples: str, user_prompt: str):
    """Build the prompt by combining the system prompt and few-shot examples."""
    return [
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'assistant',
            'content': few_shot_examples
        },
        {
            'role': 'user',
            'content': user_prompt
        }
    ]


def load_json_schema(file_path: str):
    """Load a JSON schema from a file."""
    import json
    with open(file_path, 'r') as file:
        return json.load(file)


def get_processed_query(natural_query: str, model: str = 'gemma3:4b', host: str = 'http://localhost:11434') -> str:
    """Process the natural language query to a structured format."""
    # build messages prompt
    system_prompt = read_txt_file('system_prompt.txt')
    few_shot_examples = read_txt_file('few_shot_examples.txt')
    messages = build_messages(system_prompt, few_shot_examples, natural_query)

    # load JSON schema for the response
    response_schema = load_json_schema('response_schema.json')
    client = Client(
        host=host,
        headers={'Content-Type': 'application/json'},
    )
    response: ChatResponse = client.chat(
        model=model,
        messages=messages,
        format=response_schema,
        stream=False,
        options={
            'temperature': 0.2
        }
    )
    return response.message.content


if __name__ == "__main__":
    user_prompt = 'Find all the persons that won a gold medal in Paris.'
    processed_query = get_processed_query(user_prompt)
    print(f"Processed Query for '{user_prompt}':\n{processed_query}\n")

