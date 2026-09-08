-- Movies with the best ROI with a minumum budget of $20k
WITH movies_budget_min AS (
    SELECT original_title AS title, budget, revenue
    FROM movies
    WHERE budget > 20000 
)

SELECT title, budget, revenue, ROUND(revenue * 1.0/budget, 2) AS roi
FROM movies_budget_min
ORDER BY roi DESC;