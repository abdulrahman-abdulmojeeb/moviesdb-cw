from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import get_pool, close_pool, get_db
from app.routers import movies, genres, auth, ratings, predictions, personality


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_pool()
    yield
    close_pool()


app = FastAPI(
    title="Movies DB API",
    description="COMP0022 Movie Information Application",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.allowed_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(movies.router, prefix="/api", tags=["Movies"])
app.include_router(genres.router, prefix="/api", tags=["Genres"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(ratings.router, prefix="/api/reports", tags=["Rating Reports"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["Predictions"])
app.include_router(personality.router, prefix="/api/reports", tags=["Personality Reports"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=503, content={"status": "unhealthy"})
