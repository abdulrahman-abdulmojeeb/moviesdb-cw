"""
Enrich movies with OMDB data: IMDB rating, Rotten Tomatoes score, box office.
Uses imdb_id from the movies table.
Free tier: 1000 requests/day.
"""
import os
import sys
import time
import psycopg2
import httpx

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://moviesdb:moviesdb@db:5432/moviesdb"
)
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "")
OMDB_BASE = "https://www.omdbapi.com/"
RATE_LIMIT_DELAY = 0.1
DAILY_LIMIT = 990  # Stay under the 1000/day limit


def enrich_movie(cur, client, movie_id, imdb_id):
    """Fetch OMDB data for one movie."""
    params = {"apikey": OMDB_API_KEY, "i": imdb_id}
    resp = client.get(OMDB_BASE, params=params)
    resp.raise_for_status()
    data = resp.json()

    if data.get("Response") == "False":
        return False

    # Extract Rotten Tomatoes score
    rt_score = None
    for src in data.get("Ratings", []):
        if src.get("Source") == "Rotten Tomatoes":
            val = src["Value"].replace("%", "")
            try:
                rt_score = int(val)
            except ValueError:
                pass

    # Extract IMDB rating
    imdb_rating = None
    if data.get("imdbRating") and data["imdbRating"] != "N/A":
        try:
            imdb_rating = float(data["imdbRating"])
        except ValueError:
            pass

    box_office = data.get("BoxOffice") if data.get("BoxOffice") != "N/A" else None

    cur.execute(
        """UPDATE movies SET
            imdb_rating = %s, rotten_tomatoes_score = %s, box_office = %s
           WHERE movie_id = %s""",
        (imdb_rating, rt_score, box_office, movie_id),
    )
    return True


def main():
    if not OMDB_API_KEY:
        print("OMDB_API_KEY not set. Skipping OMDB enrichment.")
        return

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Get movies with imdb_id but no imdb_rating (not yet enriched)
    cur.execute(
        """SELECT movie_id, imdb_id FROM movies
           WHERE imdb_id IS NOT NULL AND imdb_rating IS NULL
           ORDER BY movie_id"""
    )
    movies = cur.fetchall()
    total = min(len(movies), DAILY_LIMIT)
    print(f"Enriching {total} movies from OMDB (of {len(movies)} pending)...")

    with httpx.Client(timeout=15) as client:
        for i, (movie_id, imdb_id) in enumerate(movies[:DAILY_LIMIT]):
            try:
                enrich_movie(cur, client, movie_id, imdb_id)
                conn.commit()
                if (i + 1) % 100 == 0:
                    print(f"  Progress: {i + 1}/{total}")
            except Exception as e:
                conn.rollback()
                print(f"  Error for movie {movie_id}: {e}")

            time.sleep(RATE_LIMIT_DELAY)

    cur.close()
    conn.close()
    print("OMDB enrichment complete.")


if __name__ == "__main__":
    main()
