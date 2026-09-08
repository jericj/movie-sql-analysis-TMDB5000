import pandas as pd
from sqlalchemy import create_engine
import kagglehub
import os

# This will use the cached copy if already downloaded — instant, no re-download
path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")

# TMDB gives you two files — load both
movies_df = pd.read_csv(os.path.join(path, "tmdb_5000_movies.csv"))
credits_df = pd.read_csv(os.path.join(path, "tmdb_5000_credits.csv"))

# Connect to your database (SQLite example — swap for your Postgres connection string if using that)
engine = create_engine("sqlite:///project.db")

movies_df.to_sql("movies", engine, index=False, if_exists="replace")
credits_df.to_sql("credits", engine, index=False, if_exists="replace")

print("Data loaded successfully!")