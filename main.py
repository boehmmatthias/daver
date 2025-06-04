import nlparser.natural_language_parser as nlparser
from querygenerator.query_generator import get_database_query
from schemaanalyzer.schema_analyzer import get_analyzed_schema

if __name__ == "__main__":
    user_prompt = 'Find all the persons with a gold medal'
    processed_query = nlparser.get_processed_query(user_prompt)

    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'daver',
        'password': 'pizzatime',
        'database': 'daver_db'
    }

    table_list = ['person', 'games', 'games_competitor', 'competitor_event', 'medal']
    #table_list = ['person', 'medal']
    analyzed_schema = get_analyzed_schema(db_config=db_config, table_list=table_list)

    generated_query = get_database_query(processed_query, analyzed_schema)
    print(generated_query)