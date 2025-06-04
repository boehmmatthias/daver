import pandas as pd


def get_table_definition(cursor, table_name, connection_params, method="describe"):
    """
    Get table definition/schema information
    
    Args:
        cursor: database cursor object
        table_name (str): Name of the table
        connection_params (dict): Database connection parameters
        method (str): Method to use - "describe", "create", "columns", or "information_schema"
    
    Returns:
        pandas.DataFrame or str: Table definition information
    """
    result = None

    if method == "describe":
        # DESCRIBE shows: Field, Type, Null, Key, Default, Extra
        cursor.execute(f"DESCRIBE `{table_name}`")
        results = cursor.fetchall()
        result = pd.DataFrame(results)

    elif method == "create":
        # SHOW CREATE TABLE shows the full CREATE statement
        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
        results = cursor.fetchall()
        result = results[0]['Create Table'] if results else None

    elif method == "columns":
        # SHOW COLUMNS is similar to DESCRIBE but with slightly different output
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        results = cursor.fetchall()
        result = pd.DataFrame(results)

    elif method == "information_schema":
        # More detailed information from INFORMATION_SCHEMA
        query = """
                SELECT COLUMN_NAME,
                       ORDINAL_POSITION,
                       COLUMN_DEFAULT,
                       IS_NULLABLE,
                       DATA_TYPE,
                       CHARACTER_MAXIMUM_LENGTH,
                       NUMERIC_PRECISION,
                       NUMERIC_SCALE,
                       COLUMN_TYPE,
                       COLUMN_KEY,
                       EXTRA,
                       COLUMN_COMMENT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s
                  AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION \
                """
        cursor.execute(query, (connection_params['database'], table_name))
        results = cursor.fetchall()
        result = pd.DataFrame(results)

    return result


def get_all_table_names(connection_params):
    """
    Get all table names from the database
    
    Args:
        connection_params (dict): Database connection parameters
    
    Returns:
        list: List of table names
    """
    connection = None
    cursor = None
    table_names = []

    try:
        connection = mysql.connector.connect(**connection_params)
        cursor = connection.cursor()

        # Get all table names
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]

    except mysql.connector.Error as err:
        print(f"Error getting table names: {err}")
        raise err
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return table_names


def query_random_rows(cursor, table_name, num_rows):
    """
    Query X random rows from a specified table
    
    Args:
        table_name (str): Name of the table to query
        num_rows (int): Number of random rows to retrieve
        connection_params (dict): Database connection parameters
    
    Returns:
        pandas.DataFrame: DataFrame with results, all values as strings
    """

    df = pd.DataFrame()

    # First check if table exists and has data
    cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
    row_count = cursor.fetchone()['count']

    if row_count == 0:
        print(f"Table {table_name} is empty")
        return pd.DataFrame()

    # Limit num_rows to actual available rows
    actual_rows = min(num_rows, row_count)

    # Query random rows
    query = f"SELECT * FROM `{table_name}` ORDER BY RAND() LIMIT {actual_rows}"
    cursor.execute(query)

    # Fetch results
    results = cursor.fetchall()

    if results:
        # Create DataFrame
        df = pd.DataFrame(results)

        # Convert all values to strings
        df = df.astype(str)

        print(f"Retrieved {len(df)} rows from {table_name}")
    else:
        print(f"No data retrieved from {table_name}")

    return df


def get_knowledge_base_schema_for_table(cursor, table_name, db_connection_params):
    definition = get_table_definition(cursor, table_name, db_connection_params, method="describe")

    fields = []
    for row_t in definition.iterrows():
        row = row_t[1]
        fields.append({'name': row['Field'], 'type': row['Type'], 'nullable': row['Null'], 'key': row['Key'],
                       'default': row['Default'], 'extra': row['Extra'], 'context': ''})

    return {
        "name": table_name,
        "fields": fields
    }
