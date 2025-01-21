from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings


engine = create_async_engine(settings.database_url)
session_maker = async_sessionmaker(engine, expire_on_commit=False)
