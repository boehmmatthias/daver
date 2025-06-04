import json
import os
import mysql.connector
from ollama import Client, ChatResponse

from schemaanalyzer.mysql_utils import get_knowledge_base_schema_for_table, query_random_rows


def read_txt_file(file_path) -> str:
    """Read the content of a text file and return it as a string."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, "r") as f:
        return f.read().strip()


def load_json_schema(file_path: str):
    """Load a JSON schema from a file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, 'r') as file:
        return json.load(file)


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


def get_analyzed_schema(db_config, table_list, model: str = 'gemma3:4b',
                        ollama_host: str = 'http://localhost:11434'):
    """Analyze the database schema and return a structured description."""

    connection = None
    cursor = None
    result = None

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        result = {
            'database': 'mysql',
            'tables': [],
        }
        # Read system prompt and few-shot examples
        system_prompt = read_txt_file('system_prompt.txt')
        few_shot_examples = read_txt_file('few_shot_examples.txt')
        # load JSON schema for the response
        response_schema = load_json_schema('response_schema.json')
        client = Client(
            host=ollama_host,
            headers={'Content-Type': 'application/json'},
        )

        for table in table_list:
            table_schema = get_knowledge_base_schema_for_table(cursor=cursor, table_name=table,
                                                               db_connection_params=db_config)
            table_rows_df = query_random_rows(cursor=cursor, table_name=table, num_rows=100)
            max_rows = min(100, len(table_rows_df))
            rows = []

            for i in range(max_rows):
                row = table_rows_df.iloc[i].to_dict()
                rows.append(row)

            user_prompt = read_txt_file('user_prompt.txt')
            user_prompt = user_prompt.replace('<SCHEMA>', json.dumps(table_schema))
            user_prompt = user_prompt.replace('<ROWS>', json.dumps(rows))
            messages = build_messages(system_prompt, few_shot_examples, user_prompt)

            response: ChatResponse = client.chat(
                model=model,
                messages=messages,
                format=response_schema,
                stream=False,
                options={
                    'temperature': 0.1
                }
            )
            result['tables'].append(response.message.content)

    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return result


if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'daver',
        'password': 'pizzatime',
        'database': 'daver_db'
    }

    #table_list = ['person', 'games', 'games_competitor']
    table_list = ['games_competitor']
    analyzed_schema = get_analyzed_schema(db_config=db_config, table_list=table_list)
    print(analyzed_schema)
