from fastapi import APIRouter

router = APIRouter()


@router.get("/rating-bias")
def rating_bias():
    return []


@router.get("/cross-genre-preferences")
def cross_genre_preferences():
    return []
