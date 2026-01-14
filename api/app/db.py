import logging
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from app.config import settings

logger = logging.getLogger(__name__)

_pool: pool.SimpleConnectionPool | None = None


def get_pool() -> pool.SimpleConnectionPool:
    global _pool
    if _pool is None or _pool.closed:
        _pool = pool.SimpleConnectionPool(
            minconn=2,
            maxconn=10,
            dsn=settings.database_url,
        )
    return _pool


def close_pool():
    global _pool
    if _pool and not _pool.closed:
        _pool.closeall()
        _pool = None


@contextmanager
def get_db():
    """Yield a connection from the pool, auto-commit on success, rollback on error."""
    p = get_pool()
    conn = p.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        logger.exception("Database operation failed")
        raise
    finally:
        p.putconn(conn)
