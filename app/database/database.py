import os
import threading
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import NewConfig

# Module-level singletons (mirrors the Go package level variables)
_engine: Engine = None
_SessionLocal = None
_lock = threading.Lock()

def get_instance() -> Engine:
    """Returns a singleton instance of the database engine."""
    global _engine, _SessionLocal
    if _engine is None:
        with _lock:
            if _engine is None:
                config = NewConfig()
                env = config.GetEnvironment().lower()
                
                # Fetch credentials
                db_url = os.getenv("DATABASE_URL")
                if not db_url:
                    host = config.GetDBHost()
                    user = config.GetDBUser()
                    password = config.GetDBPassword()
                    dbname = config.GetDBName()
                    port = config.GetDBPort()
                    sslmode = config.GetDBSSLMode()
                    db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode={sslmode}"
                
                # Standardize Render/Heroku URLs
                if db_url.startswith("postgres://"):
                    db_url = db_url.replace("postgres://", "postgresql://", 1)
                
                schema = config.GetDBSchema()
                
                # Configure pool limits
                if env in ("prod", "production"):
                    max_open_conns = 20
                    max_idle_conns = 4
                else:
                    max_open_conns = 20
                    max_idle_conns = 10
                
                # Map Go pool configurations to SQLAlchemy Engine/QueuePool parameters
                _engine = create_engine(
                    db_url,
                    pool_size=max_idle_conns,
                    max_overflow=max_open_conns - max_idle_conns,
                    pool_recycle=1800,  # 30 minutes
                    pool_pre_ping=True,
                    connect_args={"options": f"-c search_path={schema}"}
                )
                _SessionLocal = sessionmaker(bind=_engine)
    return _engine

def GetInstance() -> Engine:
    """Go-style alias for get_instance."""
    return get_instance()

def close() -> None:
    """Closes all database connections."""
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None

def Close() -> None:
    """Go-style alias for close."""
    close()

def GetConnectionStats() -> dict:
    """Returns connection stats for the main database instance."""
    global _engine
    if _engine is None:
        return {"error": "database instance not initialized"}
    
    pool = _engine.pool
    # SQLAlchemy QueuePool statistics
    checked_in = pool.checkedin()
    checked_out = pool.checkedout()
    size = pool.size()
    
    return {
        "max_open_connections": size + (pool._max_overflow if hasattr(pool, "_max_overflow") else 0),
        "open_connections": checked_in + checked_out,
        "in_use": checked_out,
        "idle": checked_in,
        "wait_count": 0,
        "wait_duration": "0s",
        "max_idle_closed": 0,
        "max_idle_time_closed": 0,
        "max_lifetime_closed": 0,
    }

def get_connection_stats() -> dict:
    """Alias for GetConnectionStats."""
    return GetConnectionStats()

# Helper function to get database session for FastAPI dependencies
def get_db() -> Generator[Session, None, None]:
    """FastAPI database session dependency."""
    get_instance()  # Ensure initialization
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.close()
