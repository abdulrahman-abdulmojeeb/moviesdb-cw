from fastapi import APIRouter

router = APIRouter()


@router.get("/movies")
def list_movies():
    return {"movies": [], "total": 0, "page": 1, "per_page": 20, "total_pages": 0}


@router.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    return {"detail": "Not implemented"}


@router.get("/genres")
def list_genres():
    return []
