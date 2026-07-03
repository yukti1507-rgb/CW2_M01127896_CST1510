import pandas as pd

# CSV → SQLite migration using pandas
def migrate_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('metadata', conn)

# Querying SQLite into a DataFrame
def get_all_metadata(conn):
    sql = 'SELECT * FROM metadata'
    return pd.read_sql(sql, conn)