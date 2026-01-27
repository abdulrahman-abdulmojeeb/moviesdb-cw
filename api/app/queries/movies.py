"""Movie search, detail, and genre listing queries."""

# ---------------------------------------------------------------------------
# Search / list movies
# ---------------------------------------------------------------------------
# Dynamic filters are injected by the router via optional WHERE clauses.
# The router must build the WHERE / ORDER BY parts and flatten the params
# list accordingly.  The base query below uses placeholders that the router
# appends to.
#
# Mandatory params: search_term (twice, for title and overview), limit, offset
# Optional WHERE fragments the router can append before ORDER BY:
#   AND g.name = %s          -- genre filter
#   AND m.release_year = %s  -- year filter
# ---------------------------------------------------------------------------

SEARCH_MOVIES = """
    SELECT m.movie_id,
           m.title,
           m.release_year,
           m.runtime_minutes,
           m.overview,
           m.poster_path,
           m.imdb_rating,
           m.tmdb_vote_avg,
           COALESCE(mar.avg_rating, 0) AS avg_user_rating,
           COALESCE(mar.rating_count, 0) AS rating_count
      FROM movies m
      LEFT JOIN movie_avg_ratings mar USING (movie_id)
      LEFT JOIN movie_genres mg USING (movie_id)
      LEFT JOIN genres g USING (genre_id)
     WHERE (m.title ILIKE '%%' || %s || '%%'
            OR m.overview ILIKE '%%' || %s || '%%')
"""

# Appended by the router when a genre filter is provided.
SEARCH_MOVIES_GENRE_FILTER = " AND g.name = %s"

# Appended by the router when a year filter is provided.
SEARCH_MOVIES_YEAR_FILTER = " AND m.release_year = %s"

# The GROUP BY is always required because of the LEFT JOIN on genres.
SEARCH_MOVIES_GROUP_BY = """
     GROUP BY m.movie_id, mar.avg_rating, mar.rating_count
"""

# Sort options the router can pick from (no user-supplied values).
SEARCH_MOVIES_ORDER_TITLE = " ORDER BY m.title ASC"
SEARCH_MOVIES_ORDER_YEAR = " ORDER BY m.release_year DESC"
SEARCH_MOVIES_ORDER_RATING = " ORDER BY avg_user_rating DESC"
SEARCH_MOVIES_ORDER_POPULARITY = " ORDER BY rating_count DESC"
SEARCH_MOVIES_ORDER_DEFAULT = " ORDER BY m.title ASC"

# Pagination (always appended last).
SEARCH_MOVIES_PAGINATION = " LIMIT %s OFFSET %s"


# ---------------------------------------------------------------------------
# Single movie detail
# ---------------------------------------------------------------------------

GET_MOVIE_DETAIL = """
    SELECT m.movie_id,
           m.title,
           m.release_year,
           m.runtime_minutes,
           m.overview,
           m.poster_path,
           m.backdrop_path,
           m.budget,
           m.revenue,
           m.imdb_id,
           m.tmdb_id,
           m.tmdb_vote_avg,
           m.tmdb_vote_count,
           m.imdb_rating,
           m.rotten_tomatoes_score,
           m.box_office,
           COALESCE(mar.avg_rating, 0) AS avg_user_rating,
           COALESCE(mar.rating_count, 0) AS rating_count
      FROM movies m
      LEFT JOIN movie_avg_ratings mar USING (movie_id)
     WHERE m.movie_id = %s
"""

GET_MOVIE_GENRES = """
    SELECT g.genre_id, g.name
      FROM genres g
      JOIN movie_genres mg USING (genre_id)
     WHERE mg.movie_id = %s
     ORDER BY g.name
"""

GET_MOVIE_CAST = """
    SELECT p.person_id,
           p.name,
           p.profile_path,
           mc.character,
           mc.cast_order
      FROM movie_cast mc
      JOIN people p USING (person_id)
     WHERE mc.movie_id = %s
     ORDER BY mc.cast_order
"""

GET_MOVIE_CREW = """
    SELECT p.person_id,
           p.name,
           p.profile_path,
           mc.job,
           mc.department
      FROM movie_crew mc
      JOIN people p USING (person_id)
     WHERE mc.movie_id = %s
     ORDER BY mc.department, mc.job
"""

GET_MOVIE_TAGS = """
    SELECT t.tag,
           COUNT(*) AS count
      FROM tags t
     WHERE t.movie_id = %s
     GROUP BY t.tag
     ORDER BY count DESC
"""

GET_MOVIE_RATING_STATS = """
    SELECT COUNT(*) AS total_ratings,
           ROUND(AVG(r.rating), 2) AS avg_rating,
           MIN(r.rating) AS min_rating,
           MAX(r.rating) AS max_rating,
           ROUND(STDDEV(r.rating), 2) AS stddev_rating,
           PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY r.rating) AS median_rating
      FROM ratings r
     WHERE r.movie_id = %s
"""


# ---------------------------------------------------------------------------
# Genre listing (for filters / dropdowns)
# ---------------------------------------------------------------------------

LIST_GENRES = """
    SELECT g.genre_id, g.name
      FROM genres g
     ORDER BY g.name
"""
