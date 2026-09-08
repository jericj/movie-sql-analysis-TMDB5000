-- Cumulative box office revenue from 1992 to 2016
WITH revenue_by_year AS (
    SELECT CAST(strftime('%Y', release_date) AS INT) AS year, SUM(revenue) AS yearly_revenue
    FROM movies
    WHERE revenue > 0
    GROUP BY year
)

SELECT year, yearly_revenue,
    SUM(yearly_revenue) OVER (ORDER BY year) as cumulative_revenue
FROM revenue_by_year
WHERE year > (SELECT MAX(year) FROM revenue_by_year) - 25
ORDER BY year;