from fastapi import APIRouter, HTTPException, Query, status
from psycopg2.extras import RealDictCursor
from app.db import get_db
from app.queries.movies import (
    GET_MOVIE_DETAIL,
    GET_MOVIE_GENRES,
    GET_MOVIE_CAST,
    GET_MOVIE_CREW,
    GET_MOVIE_TAGS,
    LIST_GENRES,
)

router = APIRouter()

ALLOWED_SORT_COLUMNS = {"title": "m.title", "year": "m.release_year", "rating": "avg_rating"}
ALLOWED_ORDERS = {"asc", "desc"}


@router.get("/movies")
def list_movies(
    q: str = Query(None, description="Search term for movie title"),
    genre_id: int = Query(None),
    year_min: int = Query(None),
    year_max: int = Query(None),
    sort_by: str = Query("title", description="Sort column: title, year, rating"),
    order: str = Query("asc", description="Sort order: asc, desc"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    sort_col = ALLOWED_SORT_COLUMNS.get(sort_by, "m.title")
    sort_order = order.lower() if order.lower() in ALLOWED_ORDERS else "asc"

    conditions = []
    params = []

    if q:
        conditions.append("m.title ILIKE %s")
        params.append(f"%{q}%")
    if genre_id is not None:
        conditions.append("mg.genre_id = %s")
        params.append(genre_id)
    if year_min is not None:
        conditions.append("m.release_year >= %s")
        params.append(year_min)
    if year_max is not None:
        conditions.append("m.release_year <= %s")
        params.append(year_max)

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    genre_join = "LEFT JOIN movie_genres mg ON mg.movie_id = m.movie_id"

    count_query = f"""
        SELECT COUNT(DISTINCT m.movie_id)
        FROM movies m
        {genre_join}
        {where_clause}
    """

    data_query = f"""
        SELECT
            m.movie_id, m.title, m.release_year, m.poster_path,
            ROUND(AVG(r.rating), 2) AS avg_rating,
            COUNT(r.rating_id) AS rating_count
        FROM movies m
        {genre_join}
        LEFT JOIN ratings r ON r.movie_id = m.movie_id
        {where_clause}
        GROUP BY m.movie_id, m.title, m.release_year, m.poster_path
        ORDER BY {sort_col} {sort_order} NULLS LAST
        LIMIT %s OFFSET %s
    """

    offset = (page - 1) * per_page
    data_params = params + [per_page, offset]

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(count_query, params)
            total = cur.fetchone()[0]

            cur.execute(data_query, data_params)
            rows = cur.fetchall()

    movies = [
        {
            "movie_id": row[0],
            "title": row[1],
            "release_year": row[2],
            "poster_path": row[3],
            "avg_rating": float(row[4]) if row[4] else None,
            "rating_count": row[5],
        }
        for row in rows
    ]

    return {
        "movies": movies,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page if total else 0,
    }


@router.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(GET_MOVIE_DETAIL, (movie_id,))
            movie = cur.fetchone()
            if not movie:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

            cur.execute(GET_MOVIE_GENRES, (movie_id,))
            genres = cur.fetchall()

            cur.execute(GET_MOVIE_CAST, (movie_id,))
            cast = cur.fetchall()

            cur.execute(GET_MOVIE_CREW, (movie_id,))
            crew = cur.fetchall()

            cur.execute(GET_MOVIE_TAGS, (movie_id,))
            tags = cur.fetchall()

    movie["genres"] = genres
    movie["cast"] = cast
    movie["crew"] = crew
    movie["tags"] = tags
    return movie


@router.get("/genres")
def list_genres():
    with get_db() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(LIST_GENRES)
            return cur.fetchall()
