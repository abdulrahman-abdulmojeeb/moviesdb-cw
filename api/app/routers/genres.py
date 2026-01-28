from fastapi import APIRouter
from app.db import get_db
from app.queries.genres import GENRE_POPULARITY, GENRE_POLARISATION

router = APIRouter()


@router.get("/genre-popularity")
def genre_popularity():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(GENRE_POPULARITY)
            rows = cur.fetchall()

    return [
        {
            "genre_id": row[0],
            "genre_name": row[1],
            "rating_count": row[2],
            "avg_rating": float(row[3]) if row[3] else None,
            "movie_count": row[4],
        }
        for row in rows
    ]


@router.get("/genre-polarisation")
def genre_polarisation():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(GENRE_POLARISATION)
            rows = cur.fetchall()

    return [
        {
            "genre_id": row[0],
            "genre_name": row[1],
            "total_ratings": row[2],
            "avg_rating": float(row[3]) if row[3] else None,
            "rating_stddev": float(row[4]) if row[4] else None,
        }
        for row in rows
    ]
