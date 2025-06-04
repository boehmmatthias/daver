import nlparser.natural_language_parser as nlparser

if __name__ == "__main__":
    user_prompt = 'Find all the persons with a gold medal'
    processed_query = nlparser.get_processed_query(user_prompt)
    print(processed_query)