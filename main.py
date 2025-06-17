import json
import os
import pickle
import nlparser.natural_language_parser as nlparser
from querygenerator.query_generator import get_database_query
from schemaanalyzer.schema_analyzer import get_analyzed_schema

if __name__ == "__main__":
    user_prompt = 'Find all the persons with a gold medal'
    processed_query = nlparser.get_processed_query(user_prompt)
    
    print('Processed query: ', processed_query)

    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'daver',
        'password': 'pizzatime',
        'database': 'daver_db'
    }

    table_list = ['person', 'games', 'games_competitor', 'competitor_event', 'medal']
    #table_list = ['person', 'medal']
    
    # check if the json file exists
    if os.path.exists('analyzed_schema.json'):
        print('Loading analyzed schema from json file')
        with open('analyzed_schema.json', 'r') as f:
            js = json.load(f)
            analyzed_schema = json.dumps(js)
    else:
        print('Analyzing schema')
        analyzed_schema = get_analyzed_schema(db_config=db_config, table_list=table_list)
        with open('analyzed_schema.json', 'w') as f:
            # parse the analyzed schema that is already a json string
            s = json.loads(analyzed_schema)
            json.dump(s, f)

    generated_query = get_database_query(processed_query, analyzed_schema, model='deepseek-coder:6.7b')
    print(generated_query)