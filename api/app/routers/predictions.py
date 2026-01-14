from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
def predict():
    return {"prediction": None}


@router.get("/similar-films/{movie_id}")
def similar_films(movie_id: int):
    return []
