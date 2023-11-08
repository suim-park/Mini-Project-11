import pandas as pd
import sqlite3
from io import StringIO

def read_csv(file_path):
    """
    Fetch a CSV file from a Databricks repository and load it into a Pandas DataFrame.

    Parameters:
    file_path (str): The path of the CSV file in the Databricks repository.

    Returns:
    pd.DataFrame: DataFrame containing the data from the CSV file.
    """

    # DBFS file path
    dbfs_file_path = "/dbfs/" + file_path.strip("/")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(dbfs_file_path)

    return df

    # file_path = "Workspace/Repos/sp699@duke.edu/Mini-Project-11/baseball.csv"

def csv_to_sql(csv_file_path, sql_file_path, table_name):
    """
    Convert a CSV file to a SQL file.

    Parameters:
    csv_file_path (str): Path to the input CSV file.
    sql_file_path (str): Path to the output SQL file.
    table_name (str): Name of the SQL table to be used in INSERT statements.

    Returns:
    None: Creates a SQL file at the specified location.
    """

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a SQLite in-memory database and write the DataFrame to it
    conn = sqlite3.connect(":memory:")
    df.to_sql(table_name, conn, index=False, if_exists='replace')

    # Extract the SQL INSERT statements
    query = f"SELECT * FROM {table_name}"
    sql_data = StringIO()
    for row in conn.iterdump():
        if row.startswith('INSERT INTO'):
            sql_data.write(row + ';\n')

    # Write the SQL statements to a file
    with open(sql_file_path, 'w') as sql_file:
        sql_file.write(sql_data.getvalue())

    # Close the connection
    conn.close()

