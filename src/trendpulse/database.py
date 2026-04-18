from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from trendpulse.config import settings

Base = declarative_base()

engine = None
async_session_maker = None


def init_database():
    global engine, async_session_maker
    if settings.database_url:
        engine = create_async_engine(
            settings.database_url,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            echo=settings.app_env == "dev",
        )
        async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    if async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    async with async_session_maker() as session:
        yield session


async def close_database():
    global engine
    if engine:
        await engine.dispose()


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trace_id = Column(String(64), nullable=False, index=True)
    theme = Column(String(500), nullable=False)
    platform = Column(String(100), nullable=False)
    region = Column(String(50), nullable=True)
    provider = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    latency_ms = Column(Float, nullable=True)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
