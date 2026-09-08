import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///project.db")

query = """
SELECT title, release_date, budget, revenue
FROM movies
ORDER BY revenue DESC
LIMIT 10
"""

result = pd.read_sql(query, engine)
print(result)