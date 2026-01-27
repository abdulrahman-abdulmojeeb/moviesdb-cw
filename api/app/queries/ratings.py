"""Rating pattern queries -- bias analysis and cross-genre preferences."""

# ---------------------------------------------------------------------------
# Rating bias: how a user's average compares to the global average
# ---------------------------------------------------------------------------

RATING_BIAS = """
    WITH global AS (
        SELECT ROUND(AVG(rating), 2) AS global_avg
          FROM ratings
    ),
    user_stats AS (
        SELECT r.user_id,
               COUNT(*)              AS rating_count,
               ROUND(AVG(r.rating), 2) AS user_avg
          FROM ratings r
         GROUP BY r.user_id
        HAVING COUNT(*) >= 10
    )
    SELECT us.user_id,
           us.rating_count,
           us.user_avg,
           g.global_avg,
           ROUND(us.user_avg - g.global_avg, 2) AS bias
      FROM user_stats us
     CROSS JOIN global g
     ORDER BY bias DESC
"""

# Single-user variant: pass user_id as %s.
RATING_BIAS_USER = """
    WITH global AS (
        SELECT ROUND(AVG(rating), 2) AS global_avg
          FROM ratings
    ),
    user_stats AS (
        SELECT COUNT(*)              AS rating_count,
               ROUND(AVG(rating), 2) AS user_avg
          FROM ratings
         WHERE user_id = %s
    )
    SELECT us.rating_count,
           us.user_avg,
           g.global_avg,
           ROUND(us.user_avg - g.global_avg, 2) AS bias
      FROM user_stats us
     CROSS JOIN global g
"""


# ---------------------------------------------------------------------------
# Cross-genre preference correlation matrix
#
# For each pair of genres, compute the Pearson correlation of user average
# ratings across users who have rated films in both genres.
# ---------------------------------------------------------------------------

CROSS_GENRE_PREFERENCES = """
    WITH user_genre_avg AS (
        SELECT r.user_id,
               g.name AS genre,
               AVG(r.rating) AS avg_rating
          FROM ratings r
          JOIN movie_genres mg USING (movie_id)
          JOIN genres g        USING (genre_id)
         GROUP BY r.user_id, g.name
        HAVING COUNT(*) >= 5
    )
    SELECT a.genre AS genre_a,
           b.genre AS genre_b,
           ROUND(CORR(a.avg_rating, b.avg_rating)::numeric, 3) AS correlation,
           COUNT(*) AS shared_users
      FROM user_genre_avg a
      JOIN user_genre_avg b ON a.user_id = b.user_id
                           AND a.genre < b.genre
     GROUP BY a.genre, b.genre
    HAVING COUNT(*) >= 20
     ORDER BY correlation DESC
"""
