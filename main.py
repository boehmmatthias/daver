import json
import yaml
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

    #table_list = ['person', 'games', 'games_competitor', 'competitor_event', 'medal', 'city', 'competitor_event',
    #              'event', 'games_city', 'noc_region', 'person_region', 'sport']
    table_list = [
        'person',
        'games',
        #'city',
        'games_competitor',
        'competitor_event',
        'medal',
        #'event',
        'games_city',
        #'noc_region',
        #'person_region',
        #'sport'
    ]
    table_list_small = ['person']
    reanalyze_schema = False
    if reanalyze_schema:
        # If reanalyzing schema, we need to query the database for the schema
        analyzed_schema = get_analyzed_schema(db_config=db_config, table_list=table_list)
        print('Schema analyzed successfully.')
        # save the analyzed schema to a file for debugging
        with open('analyzed_schema.yaml', 'w') as f:
            f.write(analyzed_schema)
    else:
        # If not reanalyzing, we can load the schema from a file
        analyzed_schema = yaml.load('analyzed_schema.yaml', Loader=yaml.FullLoader)
        print('Schema loaded from file.')

    generated_query = get_database_query(processed_query, analyzed_schema, model='deepseek-coder:6.7b')
    print(generated_query)
