"""Genre report queries -- popularity and polarisation."""

# ---------------------------------------------------------------------------
# Genre popularity: average user rating and number of ratings per genre
# ---------------------------------------------------------------------------

GENRE_POPULARITY = """
    SELECT g.genre_id,
           g.name,
           COUNT(r.rating_id)       AS rating_count,
           ROUND(AVG(r.rating), 2)  AS avg_rating,
           COUNT(DISTINCT r.movie_id) AS movie_count
      FROM genres g
      JOIN movie_genres mg USING (genre_id)
      JOIN ratings r       USING (movie_id)
     GROUP BY g.genre_id, g.name
     ORDER BY avg_rating DESC
"""


# ---------------------------------------------------------------------------
# Genre polarisation: how divisive each genre is (high stddev = polarising)
# ---------------------------------------------------------------------------

GENRE_POLARISATION = """
    SELECT g.genre_id,
           g.name,
           COUNT(r.rating_id)          AS rating_count,
           ROUND(AVG(r.rating), 2)     AS avg_rating,
           ROUND(STDDEV(r.rating), 2)  AS stddev_rating
      FROM genres g
      JOIN movie_genres mg USING (genre_id)
      JOIN ratings r       USING (movie_id)
     GROUP BY g.genre_id, g.name
    HAVING COUNT(r.rating_id) >= 10
     ORDER BY stddev_rating DESC
"""
