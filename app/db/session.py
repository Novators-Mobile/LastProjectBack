from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

database_url = os.getenv("DATABASE_URL", settings.database_url)
if database_url.startswith("sqlite"):
    kwargs = {"connect_args": {"check_same_thread": False}}
    if database_url.endswith(":memory:"):
        kwargs["poolclass"] = StaticPool
    engine = create_engine(database_url, **kwargs)
else:
    engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
