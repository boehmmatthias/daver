import json
import yaml
import os
import pickle
import nlparser.natural_language_parser as nlparser
from querygenerator.query_generator import get_database_query
from queryjudge.query_judge import judge_sql_responses
from schemaanalyzer.schema_analyzer import get_analyzed_schema

if __name__ == "__main__":
    user_prompt = 'Find all athletes from the United States'
    print('User prompt: 🗣️ ', user_prompt)
    
    
    processed_query = nlparser.get_processed_query(user_prompt, model='phi4-mini:3.8b')
    print('Processed query: 🔍 ', processed_query)

    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'daver',
        'password': 'pizzatime',
        'database': 'daver_db'
    }
    reanalyze_schema = False
    if reanalyze_schema:
        # If reanalyzing schema, we need to query the database for the schema
        analyzed_schema = get_analyzed_schema(db_config=db_config, model='gemma3:4b')
        print('Schema analyzed successfully.')
        # save the analyzed schema to a file for debugging
        with open('analyzed_schema.yaml', 'w') as f:
            f.write(analyzed_schema)
    else:
        # If not reanalyzing, we can load the schema from a file
        yaml_schema = yaml.load(open('analyzed_schema.yaml'), Loader=yaml.FullLoader)
        analyzed_schema = yaml.dump(yaml_schema)
        print('Schema loaded from file.')

    n = 10
    sql_responses = [get_database_query(processed_query, analyzed_schema, model='deepseek-coder:6.7b') for _ in range(n)]
    
    for i, sql in enumerate(sql_responses):
        print(f'Response {i}: \n{sql}')
    
    resp = judge_sql_responses(sql_responses, user_prompt, processed_query, analyzed_schema, model='deepseek-coder:6.7b')
    # check if thinking field is present
    resp_json = json.loads(resp)
    if 'thinking' in resp_json:
        print(f'Thinking: {resp_json["thinking"]}')

    resp = json.loads(resp)['choice']
    print(f'Judged Response: {resp}')
    
    # int from string
    idx = int(resp.lower().removeprefix('response '))
    
    print(f'Response {idx}: \n{sql_responses[idx]}')
    
    # print(generated_query)
