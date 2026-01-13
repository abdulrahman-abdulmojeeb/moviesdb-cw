-- 001_initial_schema.sql
-- Core database schema for Movies DB

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Movies
CREATE TABLE IF NOT EXISTS movies (
    movie_id    INTEGER PRIMARY KEY,
    title       TEXT NOT NULL,
    release_year INTEGER,
    runtime_minutes INTEGER,
    overview    TEXT,
    poster_path TEXT,
    backdrop_path TEXT,
    budget      BIGINT,
    revenue     BIGINT,
    imdb_id     TEXT,
    tmdb_id     INTEGER,
    tmdb_vote_avg   NUMERIC(3,1),
    tmdb_vote_count INTEGER,
    imdb_rating     NUMERIC(3,1),
    rotten_tomatoes_score INTEGER CHECK (rotten_tomatoes_score >= 0 AND rotten_tomatoes_score <= 100),
    box_office  TEXT
);

-- Genres
CREATE TABLE IF NOT EXISTS genres (
    genre_id SERIAL PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE
);

-- Movie-Genre junction
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    genre_id INTEGER NOT NULL REFERENCES genres(genre_id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

-- Ratings (from MovieLens dataset)
CREATE TABLE IF NOT EXISTS ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id   INTEGER NOT NULL,
    movie_id  INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    rating    NUMERIC(2,1) NOT NULL CHECK (rating >= 0.5 AND rating <= 5.0),
    rated_at  TIMESTAMP NOT NULL
);

-- Tags (from MovieLens dataset)
CREATE TABLE IF NOT EXISTS tags (
    tag_id     SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL,
    movie_id   INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    tag        TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

-- People (actors, directors, crew)
CREATE TABLE IF NOT EXISTS people (
    person_id    SERIAL PRIMARY KEY,
    name         TEXT NOT NULL,
    tmdb_id      INTEGER,
    profile_path TEXT
);

-- Movie cast
CREATE TABLE IF NOT EXISTS movie_cast (
    movie_id   INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    person_id  INTEGER NOT NULL REFERENCES people(person_id) ON DELETE CASCADE,
    "character" TEXT,
    cast_order INTEGER,
    PRIMARY KEY (movie_id, person_id)
);

-- Movie crew
CREATE TABLE IF NOT EXISTS movie_crew (
    movie_id   INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    person_id  INTEGER NOT NULL REFERENCES people(person_id) ON DELETE CASCADE,
    job        TEXT NOT NULL,
    department TEXT,
    PRIMARY KEY (movie_id, person_id, job)
);

-- Personality profiles (Big Five traits)
CREATE TABLE IF NOT EXISTS personality_profiles (
    user_id              INTEGER PRIMARY KEY,
    openness             NUMERIC(6,4),
    agreeableness        NUMERIC(6,4),
    emotional_stability  NUMERIC(6,4),
    conscientiousness    NUMERIC(6,4),
    extraversion         NUMERIC(6,4),
    assigned_metric      TEXT,
    assigned_condition   TEXT
);

-- Personality ratings (separate from MovieLens ratings)
CREATE TABLE IF NOT EXISTS personality_ratings (
    user_id  INTEGER NOT NULL REFERENCES personality_profiles(user_id) ON DELETE CASCADE,
    movie_id INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    rating   NUMERIC(2,1) NOT NULL CHECK (rating >= 0.5 AND rating <= 5.0),
    rated_at TIMESTAMP,
    PRIMARY KEY (user_id, movie_id)
);

-- Application users (for auth / collections)
CREATE TABLE IF NOT EXISTS app_users (
    user_id       SERIAL PRIMARY KEY,
    username      TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name  TEXT,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Collections
CREATE TABLE IF NOT EXISTS collections (
    collection_id SERIAL PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES app_users(user_id) ON DELETE CASCADE,
    title         TEXT NOT NULL,
    description   TEXT,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Collection items
CREATE TABLE IF NOT EXISTS collection_items (
    collection_id INTEGER NOT NULL REFERENCES collections(collection_id) ON DELETE CASCADE,
    movie_id      INTEGER NOT NULL REFERENCES movies(movie_id) ON DELETE CASCADE,
    added_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    note          TEXT,
    display_order INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (collection_id, movie_id)
);

-- Migration tracking
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    TEXT PRIMARY KEY,
    applied_at TIMESTAMP NOT NULL DEFAULT NOW()
);
