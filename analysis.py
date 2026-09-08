import pandas as pd
import sys
from sqlalchemy import create_engine

engine = create_engine("sqlite:///project.db")
# engine = create_engine("postgresql://postgres:YOUR_PASSWORD@localhost:5432/movies_project")

def run_query(filename):
    with open(f"queries/{filename}") as f:
        sql = f.read()
    return pd.read_sql(sql, engine)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analysis.py <query_filename>.sql")
        sys.exit(1)

    filename = sys.argv[1]
    result = run_query(filename)
    print(result)