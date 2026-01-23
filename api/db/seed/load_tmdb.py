"""
Enrich movies with TMDB data: overview, poster, backdrop, runtime, budget, revenue, cast, crew.
Uses tmdb_id from the movies table (populated by load_movielens via links.csv).
Rate limited to respect TMDB API limits.
"""
import os
import sys
import time
import psycopg2
import httpx

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://moviesdb:moviesdb@db:5432/moviesdb"
)
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_BASE = "https://api.themoviedb.org/3"
RATE_LIMIT_DELAY = 0.26  # ~4 requests/sec to stay under TMDB limits


def enrich_movie(cur, client, movie_id, tmdb_id):
    """Fetch TMDB data for one movie and update the database."""
    url = f"{TMDB_BASE}/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY, "append_to_response": "credits"}
    resp = client.get(url, params=params)

    if resp.status_code == 404:
        return False
    resp.raise_for_status()
    data = resp.json()

    # Update movie metadata
    cur.execute(
        """UPDATE movies SET
            overview = %s, poster_path = %s, backdrop_path = %s,
            runtime_minutes = %s, budget = %s, revenue = %s,
            tmdb_vote_avg = %s, tmdb_vote_count = %s
           WHERE movie_id = %s""",
        (
            data.get("overview"),
            data.get("poster_path"),
            data.get("backdrop_path"),
            data.get("runtime"),
            data.get("budget"),
            data.get("revenue"),
            data.get("vote_average"),
            data.get("vote_count"),
            movie_id,
        ),
    )

    # Load cast (top 20)
    credits = data.get("credits", {})
    for member in credits.get("cast", [])[:20]:
        person_id = _upsert_person(cur, member["id"], member["name"], member.get("profile_path"))
        cur.execute(
            """INSERT INTO movie_cast (movie_id, person_id, "character", cast_order)
               VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING""",
            (movie_id, person_id, member.get("character"), member.get("order")),
        )

    # Load key crew (director, writer, producer)
    key_jobs = {"Director", "Writer", "Screenplay", "Producer", "Executive Producer"}
    for member in credits.get("crew", []):
        if member.get("job") not in key_jobs:
            continue
        person_id = _upsert_person(cur, member["id"], member["name"], member.get("profile_path"))
        cur.execute(
            """INSERT INTO movie_crew (movie_id, person_id, job, department)
               VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING""",
            (movie_id, person_id, member["job"], member.get("department")),
        )

    return True


def _upsert_person(cur, tmdb_id, name, profile_path):
    """Insert or get a person by TMDB ID."""
    cur.execute("SELECT person_id FROM people WHERE tmdb_id = %s", (tmdb_id,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        """INSERT INTO people (name, tmdb_id, profile_path)
           VALUES (%s, %s, %s) RETURNING person_id""",
        (name, tmdb_id, profile_path),
    )
    return cur.fetchone()[0]


def main():
    if not TMDB_API_KEY:
        print("TMDB_API_KEY not set. Skipping TMDB enrichment.")
        return

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Get movies with tmdb_id but no overview (not yet enriched)
    cur.execute(
        """SELECT movie_id, tmdb_id FROM movies
           WHERE tmdb_id IS NOT NULL AND overview IS NULL
           ORDER BY movie_id"""
    )
    movies = cur.fetchall()
    print(f"Enriching {len(movies)} movies from TMDB...")

    with httpx.Client(timeout=15) as client:
        for i, (movie_id, tmdb_id) in enumerate(movies):
            try:
                enrich_movie(cur, client, movie_id, tmdb_id)
                conn.commit()
                if (i + 1) % 100 == 0:
                    print(f"  Progress: {i + 1}/{len(movies)}")
            except httpx.HTTPStatusError as e:
                conn.rollback()
                if e.response.status_code == 429:
                    print("  Rate limited, sleeping 10s...")
                    time.sleep(10)
                else:
                    print(f"  Error for movie {movie_id}: {e}")
            except Exception as e:
                conn.rollback()
                print(f"  Error for movie {movie_id}: {e}")

            time.sleep(RATE_LIMIT_DELAY)

    cur.close()
    conn.close()
    print("TMDB enrichment complete.")


if __name__ == "__main__":
    main()
