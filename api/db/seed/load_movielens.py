"""
Load MovieLens small dataset into the database.
Expects CSV files in /app/data/ (mounted from infra/data/).
"""
import csv
import os
import sys
from datetime import datetime, timezone
import psycopg2

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://moviesdb:moviesdb@db:5432/moviesdb"
)
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")


def load_movies(cur):
    """Load movies.csv - extract genres into normalised tables."""
    filepath = os.path.join(DATA_DIR, "movies.csv")
    if not os.path.exists(filepath):
        print(f"  [skip] {filepath} not found")
        return

    genre_cache = {}

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        movie_count = 0
        for row in reader:
            movie_id = int(row["movieId"])
            raw_title = row["title"].strip()

            # Extract year from title like "Toy Story (1995)"
            release_year = None
            title = raw_title
            if raw_title.endswith(")") and "(" in raw_title:
                idx = raw_title.rfind("(")
                year_str = raw_title[idx + 1 : -1].strip()
                if year_str.isdigit() and len(year_str) == 4:
                    release_year = int(year_str)
                    title = raw_title[:idx].strip()

            cur.execute(
                """INSERT INTO movies (movie_id, title, release_year)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (movie_id) DO UPDATE
                   SET title = EXCLUDED.title, release_year = EXCLUDED.release_year""",
                (movie_id, title, release_year),
            )

            # Genres
            genres = [g.strip() for g in row["genres"].split("|") if g.strip() and g.strip() != "(no genres listed)"]
            for genre_name in genres:
                if genre_name not in genre_cache:
                    cur.execute(
                        """INSERT INTO genres (name) VALUES (%s)
                           ON CONFLICT (name) DO NOTHING
                           RETURNING genre_id""",
                        (genre_name,),
                    )
                    result = cur.fetchone()
                    if result:
                        genre_cache[genre_name] = result[0]
                    else:
                        cur.execute("SELECT genre_id FROM genres WHERE name = %s", (genre_name,))
                        genre_cache[genre_name] = cur.fetchone()[0]

                cur.execute(
                    """INSERT INTO movie_genres (movie_id, genre_id)
                       VALUES (%s, %s)
                       ON CONFLICT DO NOTHING""",
                    (movie_id, genre_cache[genre_name]),
                )
            movie_count += 1

    print(f"  Loaded {movie_count} movies, {len(genre_cache)} genres.")


def load_ratings(cur):
    """Load ratings.csv."""
    filepath = os.path.join(DATA_DIR, "ratings.csv")
    if not os.path.exists(filepath):
        print(f"  [skip] {filepath} not found")
        return

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        batch = []
        for row in reader:
            ts = datetime.fromtimestamp(int(row["timestamp"]), tz=timezone.utc)
            batch.append((int(row["userId"]), int(row["movieId"]), float(row["rating"]), ts))
            if len(batch) >= 5000:
                _insert_ratings_batch(cur, batch)
                count += len(batch)
                batch = []
        if batch:
            _insert_ratings_batch(cur, batch)
            count += len(batch)

    print(f"  Loaded {count} ratings.")


def _insert_ratings_batch(cur, batch):
    args = ",".join(
        cur.mogrify("(%s, %s, %s, %s)", row).decode() for row in batch
    )
    cur.execute(
        f"INSERT INTO ratings (user_id, movie_id, rating, rated_at) VALUES {args} ON CONFLICT DO NOTHING"
    )


def load_tags(cur):
    """Load tags.csv."""
    filepath = os.path.join(DATA_DIR, "tags.csv")
    if not os.path.exists(filepath):
        print(f"  [skip] {filepath} not found")
        return

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            ts = datetime.fromtimestamp(int(row["timestamp"]), tz=timezone.utc)
            cur.execute(
                """INSERT INTO tags (user_id, movie_id, tag, created_at)
                   VALUES (%s, %s, %s, %s)""",
                (int(row["userId"]), int(row["movieId"]), row["tag"], ts),
            )
            count += 1

    print(f"  Loaded {count} tags.")


def load_links(cur):
    """Load links.csv to set tmdb_id and imdb_id on movies."""
    filepath = os.path.join(DATA_DIR, "links.csv")
    if not os.path.exists(filepath):
        print(f"  [skip] {filepath} not found")
        return

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            movie_id = int(row["movieId"])
            imdb_id = f"tt{row['imdbId'].zfill(7)}" if row.get("imdbId") else None
            tmdb_id = int(row["tmdbId"]) if row.get("tmdbId") else None
            cur.execute(
                """UPDATE movies SET imdb_id = %s, tmdb_id = %s
                   WHERE movie_id = %s""",
                (imdb_id, tmdb_id, movie_id),
            )
            count += 1

    print(f"  Updated {count} movie links.")


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    try:
        print("Loading MovieLens data...")
        load_movies(cur)
        conn.commit()

        load_ratings(cur)
        conn.commit()

        load_tags(cur)
        conn.commit()

        load_links(cur)
        conn.commit()

        print("MovieLens data loaded successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error loading data: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
