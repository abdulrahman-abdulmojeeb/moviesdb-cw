"""
Load Personality ISF 2018 dataset.
Expects personality-data.csv and personality-ratings.csv in /app/data/.
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


def load_profiles(cur):
    """Load personality-data.csv into personality_profiles."""
    filepath = os.path.join(DATA_DIR, "personality-data.csv")
    if not os.path.exists(filepath):
        print(f"  [skip] {filepath} not found")
        return

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            cur.execute(
                """INSERT INTO personality_profiles
                   (user_id, openness, agreeableness, emotional_stability,
                    conscientiousness, extraversion, assigned_metric, assigned_condition)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                   ON CONFLICT (user_id) DO NOTHING""",
                (
                    int(row["userid"]),
                    float(row["openness"]) if row.get("openness") else None,
                    float(row["agreeableness"]) if row.get("agreeableness") else None,
                    float(row["emotional_stability"]) if row.get("emotional_stability") else None,
                    float(row["conscientiousness"]) if row.get("conscientiousness") else None,
                    float(row["extraversion"]) if row.get("extraversion") else None,
                    row.get("assigned metric"),
                    row.get("assigned condition"),
                ),
            )
            count += 1

    print(f"  Loaded {count} personality profiles.")


def load_personality_ratings(cur):
    """Load personality-ratings.csv."""
    filepath = os.path.join(DATA_DIR, "personality-ratings.csv")
    if not os.path.exists(filepath):
        print(f"  [skip] {filepath} not found")
        return

    # Get valid movie IDs so we skip ratings for unknown movies
    cur.execute("SELECT movie_id FROM movies")
    valid_movies = {row[0] for row in cur.fetchall()}

    # Get valid personality user IDs
    cur.execute("SELECT user_id FROM personality_profiles")
    valid_users = {row[0] for row in cur.fetchall()}

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        skipped = 0
        batch = []
        for row in reader:
            user_id = int(row["userid"]) if "userid" in row else int(row.get("userId", 0))
            movie_id = int(row["movie_id"]) if "movie_id" in row else int(row.get("movieId", 0))

            if user_id not in valid_users or movie_id not in valid_movies:
                skipped += 1
                continue

            rating = float(row["rating"])
            ts_str = row.get("timestamp")
            rated_at = None
            if ts_str:
                try:
                    rated_at = datetime.fromtimestamp(int(float(ts_str)), tz=timezone.utc)
                except (ValueError, OSError):
                    rated_at = None

            batch.append((user_id, movie_id, rating, rated_at))
            if len(batch) >= 5000:
                _insert_batch(cur, batch)
                count += len(batch)
                batch = []

        if batch:
            _insert_batch(cur, batch)
            count += len(batch)

    print(f"  Loaded {count} personality ratings (skipped {skipped} invalid refs).")


def _insert_batch(cur, batch):
    args = ",".join(
        cur.mogrify("(%s, %s, %s, %s)", row).decode() for row in batch
    )
    cur.execute(
        f"INSERT INTO personality_ratings (user_id, movie_id, rating, rated_at) "
        f"VALUES {args} ON CONFLICT DO NOTHING"
    )


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    try:
        print("Loading Personality ISF 2018 data...")
        load_profiles(cur)
        conn.commit()

        load_personality_ratings(cur)
        conn.commit()

        print("Personality data loaded successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error loading data: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
