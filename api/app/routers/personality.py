from fastapi import APIRouter

router = APIRouter()


@router.get("/personality-genre-correlation")
def personality_genre_correlation():
    return []


@router.get("/personality-clusters")
def personality_clusters():
    return []
