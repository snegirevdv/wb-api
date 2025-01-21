import asyncio
import uvicorn
from fastapi import FastAPI

from app.bot.main import start_bot
from app.core.config import settings
from app.api.endpoints import products
from app.services.scheduler import start_scheduler


async def startup_event():
    """Запускает scheduler"""
    await start_scheduler()


def get_application() -> FastAPI:
    """Создает и возвращает объект FastAPI."""
    app = FastAPI(title=settings.app_title, description=settings.app_description)
    app.include_router(products.router, prefix="/api/v1", tags=["products"])
    app.router.on_startup.append(startup_event)
    return app


async def start_api():
    """Создает и запускает приложение FastAPI."""
    config = uvicorn.Config(
        "app.main:get_application",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """Входная точка приложения."""
    api_task = asyncio.create_task(start_api())
    bot_task = asyncio.create_task(start_bot())
    await asyncio.gather(api_task, bot_task)


if __name__ == "__main__":
    asyncio.run(main())
