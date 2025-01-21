from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Создает и отдает асинхронную сессию."""
    async with session_maker() as session:
        yield session
