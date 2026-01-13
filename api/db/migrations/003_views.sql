-- 003_views.sql
-- Materialized views for common aggregations

-- Average ratings per movie
CREATE OR REPLACE VIEW movie_avg_ratings AS
SELECT
    m.movie_id,
    m.title,
    COUNT(r.rating_id)   AS rating_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM movies m
LEFT JOIN ratings r ON r.movie_id = m.movie_id
GROUP BY m.movie_id, m.title;

-- Genre popularity overview
CREATE OR REPLACE VIEW genre_popularity AS
SELECT
    g.genre_id,
    g.name AS genre_name,
    COUNT(DISTINCT mg.movie_id) AS movie_count,
    COUNT(r.rating_id)          AS total_ratings,
    ROUND(AVG(r.rating), 2)     AS avg_rating
FROM genres g
JOIN movie_genres mg ON mg.genre_id = g.genre_id
LEFT JOIN ratings r  ON r.movie_id = mg.movie_id
GROUP BY g.genre_id, g.name;
