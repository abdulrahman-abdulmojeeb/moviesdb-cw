from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
def register():
    return {"detail": "Not implemented"}


@router.post("/login")
def login():
    return {"detail": "Not implemented"}


@router.get("/me")
def me():
    return {"detail": "Not implemented"}
