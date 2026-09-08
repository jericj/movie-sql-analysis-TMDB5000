import pandas as pd
import os
from sqlalchemy import create_engine

engine = create_engine("sqlite:///project.db")

def run_query(filename):
    with open(f"queries/{filename}") as f:
        sql = f.read()
    return pd.read_sql(sql, engine)

def export_query(filename, output_name):
    result = run_query(filename)
    os.makedirs("exports", exist_ok=True)
    result.to_csv(f"exports/{output_name}", index=False)
    print(f"Exported {output_name} — {len(result)} rows")

if __name__ == "__main__":
    export_query("revenue_by_genre.sql", "revenue_by_genre.csv")
    export_query("top_3_grossing_per_genre.sql", "top_3_grossing_per_genre.csv")
    export_query("cumulative_revenue_1992_to_2016.sql", "cumulative_revenue_1992_to_2016.csv")
    export_query("top_roi_min_budget_20k.sql", "top_roi_min_budget_20k.csv")
    export_query("director_performance.sql", "director_performance.csv")