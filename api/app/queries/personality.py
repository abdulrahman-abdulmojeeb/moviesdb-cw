"""Personality trait queries -- Big Five correlations with genre preferences."""

# ---------------------------------------------------------------------------
# Personality-genre correlation
#
# For each Big Five trait, compute the Pearson correlation between the trait
# score and users' average rating per genre. Only includes users who have
# both a personality profile and enough ratings in that genre.
# ---------------------------------------------------------------------------

PERSONALITY_GENRE_CORRELATION = """
    WITH user_genre_avg AS (
        SELECT pr.user_id,
               g.name AS genre,
               AVG(pr.rating) AS avg_rating
          FROM personality_ratings pr
          JOIN movie_genres mg USING (movie_id)
          JOIN genres g        USING (genre_id)
         GROUP BY pr.user_id, g.name
        HAVING COUNT(*) >= 5
    )
    SELECT uga.genre,
           ROUND(CORR(pp.openness, uga.avg_rating)::numeric, 3)
               AS openness_corr,
           ROUND(CORR(pp.agreeableness, uga.avg_rating)::numeric, 3)
               AS agreeableness_corr,
           ROUND(CORR(pp.emotional_stability, uga.avg_rating)::numeric, 3)
               AS emotional_stability_corr,
           ROUND(CORR(pp.conscientiousness, uga.avg_rating)::numeric, 3)
               AS conscientiousness_corr,
           ROUND(CORR(pp.extraversion, uga.avg_rating)::numeric, 3)
               AS extraversion_corr,
           COUNT(*) AS sample_size
      FROM user_genre_avg uga
      JOIN personality_profiles pp USING (user_id)
     GROUP BY uga.genre
    HAVING COUNT(*) >= 20
     ORDER BY uga.genre
"""


# ---------------------------------------------------------------------------
# Personality clusters
#
# Group users by their assigned_metric / assigned_condition and compute
# aggregate rating behaviour per cluster.
# ---------------------------------------------------------------------------

PERSONALITY_CLUSTERS = """
    SELECT pp.assigned_metric,
           pp.assigned_condition,
           COUNT(DISTINCT pp.user_id) AS user_count,
           ROUND(AVG(pr.rating), 2) AS avg_rating,
           ROUND(STDDEV(pr.rating), 2) AS stddev_rating,
           COUNT(pr.rating) AS total_ratings,
           ROUND(AVG(pp.openness), 3) AS avg_openness,
           ROUND(AVG(pp.agreeableness), 3) AS avg_agreeableness,
           ROUND(AVG(pp.emotional_stability), 3) AS avg_emotional_stability,
           ROUND(AVG(pp.conscientiousness), 3) AS avg_conscientiousness,
           ROUND(AVG(pp.extraversion), 3) AS avg_extraversion
      FROM personality_profiles pp
      LEFT JOIN personality_ratings pr USING (user_id)
     GROUP BY pp.assigned_metric, pp.assigned_condition
     ORDER BY pp.assigned_metric, pp.assigned_condition
"""
