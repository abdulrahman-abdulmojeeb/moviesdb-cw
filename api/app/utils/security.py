from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings
from app.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "username": username, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if "sub" not in payload or "username" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme)):
    """Dependency: returns the current user dict or raises 401."""
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    user_id = int(payload["sub"])
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, display_name FROM app_users WHERE user_id = %s",
                (user_id,),
            )
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return {"user_id": row[0], "username": row[1], "display_name": row[2]}


def get_optional_user(credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme)):
    """Dependency: returns current user dict or None if not authenticated."""
    if credentials is None:
        return None
    try:
        payload = decode_token(credentials.credentials)
        return {"user_id": int(payload["sub"]), "username": payload["username"]}
    except Exception:
        return None
