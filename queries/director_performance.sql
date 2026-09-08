-- Directors ranked by how many films they've headed and average revenue across their catalog
SELECT cm.name, COUNT(*) AS film_count, ROUND(AVG(m.revenue), 2) AS avg_revenue
FROM movie_crew mc
JOIN crew_members cm ON mc.person_id = cm.person_id
JOIN movies m ON mc.movie_id = m.id
WHERE mc.job = 'Director' AND revenue > 0
GROUP BY cm.name
HAVING COUNT(*) >= 3
ORDER BY film_count DESC;