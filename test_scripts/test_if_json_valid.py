import kagglehub
import os
import pandas as pd
import json

path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")
movies_df = pd.read_csv(os.path.join(path, "tmdb_5000_movies.csv"))

def is_valid_json(value):
    try:
        json.loads(value)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

valid_count = movies_df["genres"].apply(is_valid_json).sum()
total = len(movies_df)
print(f"{valid_count} out of {total} rows are valid strict JSON")