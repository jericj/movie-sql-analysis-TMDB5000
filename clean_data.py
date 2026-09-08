import pandas as pd
import ast
import kagglehub
import os
from sqlalchemy import create_engine

# --- Load raw data ---
path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")
movies_df = pd.read_csv(os.path.join(path, "tmdb_5000_movies.csv"))
credits_df = pd.read_csv(os.path.join(path, "tmdb_5000_credits.csv"))

# Rename so both dataframes share a common id column name for merging
credits_df = credits_df.rename(columns={"movie_id": "id"})

# --- Helper to safely parse the JSON-like strings ---
def parse_json_column(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []

# ============================================================
# 1. GENRES
# ============================================================
genre_rows = []
movie_genre_rows = []

for _, row in movies_df.iterrows():
    genres = parse_json_column(row["genres"])
    for g in genres:
        genre_rows.append({"genre_id": g["id"], "genre_name": g["name"]})
        movie_genre_rows.append({"movie_id": row["id"], "genre_id": g["id"]})

genres_table = pd.DataFrame(genre_rows).drop_duplicates()
movie_genres_table = pd.DataFrame(movie_genre_rows).drop_duplicates()

# ============================================================
# 2. CAST
# ============================================================
cast_member_rows = []
movie_cast_rows = []

for _, row in credits_df.iterrows():
    cast_list = parse_json_column(row["cast"])
    for c in cast_list:
        cast_member_rows.append({"person_id": c["id"], "name": c["name"]})
        movie_cast_rows.append({
            "movie_id": row["id"],
            "person_id": c["id"],
            "character": c.get("character", ""),
            "cast_order": c.get("order", None)
        })

cast_members_table = pd.DataFrame(cast_member_rows).drop_duplicates()
movie_cast_table = pd.DataFrame(movie_cast_rows).drop_duplicates()

# ============================================================
# 3. CREW
# ============================================================
crew_member_rows = []
movie_crew_rows = []

for _, row in credits_df.iterrows():
    crew_list = parse_json_column(row["crew"])
    for c in crew_list:
        crew_member_rows.append({"person_id": c["id"], "name": c["name"]})
        movie_crew_rows.append({
            "movie_id": row["id"],
            "person_id": c["id"],
            "job": c.get("job", ""),
            "department": c.get("department", "")
        })

crew_members_table = pd.DataFrame(crew_member_rows).drop_duplicates()
movie_crew_table = pd.DataFrame(movie_crew_rows).drop_duplicates()

# ============================================================
# 4. CORE MOVIES TABLE (drop the raw JSON columns now that they're normalized)
# ============================================================
core_movies_table = movies_df.drop(columns=["genres", "keywords", "production_companies",
                                              "production_countries", "spoken_languages"])

# ============================================================
# LOAD EVERYTHING INTO THE DATABASE
# ============================================================
engine = create_engine("sqlite:///project.db")
# engine = create_engine("postgresql://postgres:YOUR_PASSWORD@localhost:5432/movies_project")

core_movies_table.to_sql("movies", engine, index=False, if_exists="replace")
genres_table.to_sql("genres", engine, index=False, if_exists="replace")
movie_genres_table.to_sql("movie_genres", engine, index=False, if_exists="replace")
cast_members_table.to_sql("cast_members", engine, index=False, if_exists="replace")
movie_cast_table.to_sql("movie_cast", engine, index=False, if_exists="replace")
crew_members_table.to_sql("crew_members", engine, index=False, if_exists="replace")
movie_crew_table.to_sql("movie_crew", engine, index=False, if_exists="replace")

print("Cleaned and loaded relational tables successfully!")
print(f"Movies: {len(core_movies_table)}")
print(f"Genres: {len(genres_table)}")
print(f"Cast entries: {len(movie_cast_table)}")
print(f"Crew entries: {len(movie_crew_table)}")