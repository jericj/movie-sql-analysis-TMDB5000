SELECT g.genre_name, ROUND(AVG(m.revenue), 2) AS avg_revenue
FROM movies m 
JOIN movie_genres mg ON m.id = mg.movie_id
JOIN genres g ON mg.genre_id = g.genre_id
WHERE revenue > 0
GROUP BY g.genre_name
ORDER BY avg_revenue DESC;