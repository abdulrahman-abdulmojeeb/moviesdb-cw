from fastapi import APIRouter

router = APIRouter()


@router.get("/genre-popularity")
def genre_popularity():
    return []


@router.get("/genre-polarisation")
def genre_polarisation():
    return []
