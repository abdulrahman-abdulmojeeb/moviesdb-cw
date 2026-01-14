from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://moviesdb:moviesdb@db:5432/moviesdb"
    jwt_secret: str  # Required — no default; must be set via env var
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours
    tmdb_api_key: str = ""
    omdb_api_key: str = ""
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
