-- 002_indexes.sql
-- Performance indexes

-- Trigram index for fuzzy title search
CREATE INDEX IF NOT EXISTS idx_movies_title_trgm
    ON movies USING gin (title gin_trgm_ops);

-- Common lookups
CREATE INDEX IF NOT EXISTS idx_movies_release_year ON movies(release_year);
CREATE INDEX IF NOT EXISTS idx_movies_tmdb_id ON movies(tmdb_id);
CREATE INDEX IF NOT EXISTS idx_movies_imdb_id ON movies(imdb_id);

-- Ratings indexes
CREATE INDEX IF NOT EXISTS idx_ratings_movie_id ON ratings(movie_id);
CREATE INDEX IF NOT EXISTS idx_ratings_user_id ON ratings(user_id);
CREATE INDEX IF NOT EXISTS idx_ratings_movie_rating ON ratings(movie_id, rating);

-- Tags
CREATE INDEX IF NOT EXISTS idx_tags_movie_id ON tags(movie_id);

-- Movie genres
CREATE INDEX IF NOT EXISTS idx_movie_genres_genre_id ON movie_genres(genre_id);

-- Cast & crew
CREATE INDEX IF NOT EXISTS idx_movie_cast_person_id ON movie_cast(person_id);
CREATE INDEX IF NOT EXISTS idx_movie_crew_person_id ON movie_crew(person_id);

-- Personality
CREATE INDEX IF NOT EXISTS idx_personality_ratings_movie_id ON personality_ratings(movie_id);

-- App users
CREATE INDEX IF NOT EXISTS idx_app_users_username ON app_users(username);

-- Ratings composite (user + movie for unique lookups)
CREATE INDEX IF NOT EXISTS idx_ratings_user_movie ON ratings(user_id, movie_id);

-- Collections
CREATE INDEX IF NOT EXISTS idx_collections_user_id ON collections(user_id);
CREATE INDEX IF NOT EXISTS idx_collection_items_movie_id ON collection_items(movie_id);
