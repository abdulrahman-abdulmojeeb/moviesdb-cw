from fastapi import APIRouter, Body, HTTPException, status, Depends
from app.db import get_db
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post("/register")
def register(
    username: str = Body(min_length=3, max_length=50),
    password: str = Body(min_length=8, max_length=128),
    display_name: str = Body(None),
):
    display_name = display_name.strip() if display_name else None
    hashed = hash_password(password)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id FROM app_users WHERE username = %s",
                (username,),
            )
            if cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken",
                )
            cur.execute(
                """INSERT INTO app_users (username, password_hash, display_name)
                   VALUES (%s, %s, %s)
                   RETURNING user_id, username, display_name, created_at""",
                (username, hashed, display_name),
            )
            row = cur.fetchone()

    user = {
        "user_id": row[0],
        "username": row[1],
        "display_name": row[2],
        "created_at": row[3].isoformat(),
    }
    token = create_access_token(user["user_id"], user["username"])
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/login")
def login(
    username: str = Body(min_length=3, max_length=50),
    password: str = Body(min_length=8, max_length=128),
):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, password_hash, display_name FROM app_users WHERE username = %s",
                (username,),
            )
            row = cur.fetchone()

    if not row or not verify_password(password, row[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    user = {"user_id": row[0], "username": row[1], "display_name": row[3]}
    token = create_access_token(user["user_id"], user["username"])
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user
