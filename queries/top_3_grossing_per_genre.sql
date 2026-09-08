-- Top 3 highest-grossing movies within each genre, using ROW_NUMBER() to rank movies by revenue within genre partitions
WITH ranked_movies AS (
    SELECT g.genre_name, m.original_title AS title, m.revenue,
        ROW_NUMBER() OVER (
            PARTITION BY g.genre_name
            ORDER BY m.revenue DESC) AS rank
    FROM movie_genres mg 
    JOIN movies m ON mg.movie_id = m.id
    JOIN genres g ON mg.genre_id = g.genre_id
    WHERE m.revenue > 0
)

SELECT *
FROM ranked_movies
WHERE rank <= 3;