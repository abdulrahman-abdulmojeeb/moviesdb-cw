"""
Database migration runner.
Applies SQL migration files in order, tracking which have been applied.
"""
import os
import sys
import psycopg2

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://moviesdb:moviesdb@db:5432/moviesdb"
)
MIGRATIONS_DIR = os.path.join(os.path.dirname(__file__), "migrations")


def run_migrations():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()

    # Ensure schema_migrations table exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version    TEXT PRIMARY KEY,
            applied_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    conn.commit()

    # Get already applied migrations
    cur.execute("SELECT version FROM schema_migrations ORDER BY version")
    applied = {row[0] for row in cur.fetchall()}

    # Find and sort migration files
    files = sorted(
        f for f in os.listdir(MIGRATIONS_DIR)
        if f.endswith(".sql")
    )

    applied_count = 0
    for filename in files:
        version = filename.replace(".sql", "")
        if version in applied:
            print(f"  [skip] {filename} (already applied)")
            continue

        filepath = os.path.join(MIGRATIONS_DIR, filename)
        print(f"  [apply] {filename} ...", end=" ")
        with open(filepath) as f:
            sql = f.read()

        try:
            cur.execute(sql)
            cur.execute(
                "INSERT INTO schema_migrations (version) VALUES (%s)",
                (version,),
            )
            conn.commit()
            print("OK")
            applied_count += 1
        except Exception as e:
            conn.rollback()
            print(f"FAILED: {e}")
            cur.close()
            conn.close()
            sys.exit(1)

    cur.close()
    conn.close()
    print(f"\nMigrations complete. {applied_count} new migration(s) applied.")


if __name__ == "__main__":
    print("Running database migrations...")
    run_migrations()
