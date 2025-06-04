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
            'role': 'asssistant',
            'content': few_shot_examples
        },
        {
            'role': 'user',
            'content': user_prompt
        }
    ]


#client = Client(
#    host='http://localhost:11434',
#    headers={'Content-Type': 'application/json'},
#)

# response: ChatResponse = client.chat(model='gemma3:4b', messages=[
#  {
#    'role': 'user',
#    'content': 'Hello World',
#  },
# ])
#
# print(response.message.content)

if __name__ == "__main__":

    system_prompt = read_txt_file('system_prompt.txt')
    few_shot_examples = read_txt_file('few_shot_examples.txt')
    user_prompt = 'Find all the persons that won a gold medal in Paris.'
    messages = build_messages(system_prompt, few_shot_examples, user_prompt)
    client = Client(
        host='http://localhost:11434',
        headers={'Content-Type': 'application/json'},
    )
    response: ChatResponse = client.chat(
        model='gemma3:4b',
        messages=messages,
        stream=False,
        options={
            'temperature': 0.2
        }
    )
    print(response.message.content)



