import numpy as np
import pandas as pd
import re
from sqlalchemy import create_engine
from sqlalchemy import text

# Database connection
user = "postgres"
password = "vimaljue73"
host = "localhost"
port = 5432
database = "Grizzley_DB"

def get_connection():
    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )
    return engine

# Table profiling function
def table_profile(engine, table_name):

    # Row count
    row_count = pd.read_sql(
        f'SELECT COUNT(*) AS row_count FROM "{table_name}"',
        engine
    ).iloc[0, 0]

    # Only load 5 rows for pandas dtype detection
    sample = pd.read_sql(
        f'SELECT * FROM "{table_name}" LIMIT 5',
        engine
    )

    print(f"Table: {table_name}")
    print(f"Shape: ({row_count:,}, {len(sample.columns)})")

    print("\nColumns:")
    for column in sample.columns:
        print(f"  - {column}: {sample[column].dtype}")

# Header profiling function
def header_profile(engine, table_name, n=5):
    query = f'SELECT * FROM "{table_name}" LIMIT {n}'
    df = pd.read_sql(query, engine)
    return df

# Uniqueness profiling function
def uniqueness_profile(engine, table_name, column):
    query = text(f"""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT "{column}") AS unique_values,
            COUNT(*) - COUNT(DISTINCT "{column}") AS duplicate_count
        FROM "{table_name}";
    """)

    with engine.connect() as conn:
        result = conn.execute(query).mappings().one()

    return dict(result)

# Missing value profiling function
def missing_profile(engine, table_name):
    
    columns = pd.read_sql(
        f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = '{table_name}'
        ORDER BY ordinal_position;
        """,
        engine
    )

    results = []

    for column in columns["column_name"]:
        
        query = f"""
        SELECT
            '{table_name}' AS table_name,
            '{column}' AS column_name,
            COUNT(*) AS total_rows,
            COUNT(*) - COUNT("{column}") AS null_count,
            ROUND(
                (COUNT(*) - COUNT("{column}")) * 100.0 / COUNT(*),
                2
            ) AS null_percentage
        FROM "{table_name}";
        """

        results.append(pd.read_sql(query, engine))

    return pd.concat(results, ignore_index=True)

def convert_to_hours(duration):
    """
    Convert a duration string (e.g., '38h30m0s') to hours as a float.
    """
    # Extract hours, minutes, and seconds from the string, defaulting to 0 if not present.
    hours = int(re.search(r"(\d+)h", duration).group(1)) if "h" in duration else 0
    minutes = int(re.search(r"(\d+)m", duration).group(1)) if "m" in duration else 0
    seconds = int(re.search(r"(\d+)s", duration).group(1)) if "s" in duration else 0
    # Calculate total hours.
    return hours + minutes / 60 + seconds / 3600