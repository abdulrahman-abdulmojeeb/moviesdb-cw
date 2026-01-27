"""Prediction queries -- rating prediction and similar film discovery."""

# ---------------------------------------------------------------------------
# Predict rating: genre-overlap weighted average
#
# For a given user (%s) and movie (%s), find other movies the user has rated
# that share genres with the target movie. Weight each rated movie's score by
# the number of shared genres and return the weighted average as the
# predicted rating.
# ---------------------------------------------------------------------------

PREDICT_RATING = """
    WITH target_genres AS (
        SELECT genre_id
          FROM movie_genres
         WHERE movie_id = %s
    ),
    user_rated AS (
        SELECT r.movie_id,
               r.rating,
               COUNT(tg.genre_id) AS shared_genres
          FROM ratings r
          JOIN movie_genres mg ON mg.movie_id = r.movie_id
          JOIN target_genres tg ON tg.genre_id = mg.genre_id
         WHERE r.user_id = %s
           AND r.movie_id != %s
         GROUP BY r.movie_id, r.rating
    )
    SELECT ROUND(
               SUM(rating * shared_genres)::numeric
               / NULLIF(SUM(shared_genres), 0),
               2
           ) AS predicted_rating,
           COUNT(*) AS based_on_movies,
           SUM(shared_genres) AS total_genre_overlap
      FROM user_rated
"""


# ---------------------------------------------------------------------------
# Similar films: movies that share the most genres with a target movie and
# also have similar community ratings.
#
# Params: movie_id (%s), movie_id again (%s for exclusion), limit (%s)
# ---------------------------------------------------------------------------

SIMILAR_FILMS = """
    WITH target_genres AS (
        SELECT genre_id
          FROM movie_genres
         WHERE movie_id = %s
    ),
    target_rating AS (
        SELECT COALESCE(avg_rating, 0) AS avg_rating
          FROM movie_avg_ratings
         WHERE movie_id = %s
    ),
    candidates AS (
        SELECT m.movie_id,
               m.title,
               m.release_year,
               m.poster_path,
               COALESCE(mar.avg_rating, 0) AS avg_rating,
               COUNT(tg.genre_id) AS shared_genres,
               (SELECT COUNT(*) FROM target_genres) AS target_genre_count
          FROM movies m
          JOIN movie_genres mg ON mg.movie_id = m.movie_id
          JOIN target_genres tg ON tg.genre_id = mg.genre_id
          LEFT JOIN movie_avg_ratings mar ON mar.movie_id = m.movie_id
         WHERE m.movie_id != %s
         GROUP BY m.movie_id, m.title, m.release_year,
                  m.poster_path, mar.avg_rating
    )
    SELECT c.movie_id,
           c.title,
           c.release_year,
           c.poster_path,
           c.avg_rating,
           c.shared_genres,
           ROUND(
               c.shared_genres::numeric / NULLIF(c.target_genre_count, 0),
               2
           ) AS genre_similarity,
           ROUND(
               1.0 / (1.0 + ABS(c.avg_rating - tr.avg_rating)),
               3
           ) AS rating_similarity
      FROM candidates c
     CROSS JOIN target_rating tr
     ORDER BY genre_similarity DESC,
              rating_similarity DESC
     LIMIT %s
"""
