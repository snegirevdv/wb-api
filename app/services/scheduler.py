from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy import create_engine

from app.core.config import settings
from app.core.db import session_maker
from app.services.products import create_or_update_product

engine = create_engine(settings.jobs_db_url)
jobstore = SQLAlchemyJobStore(url=settings.jobs_db_url, tablename="scheduler_jobs")
scheduler = AsyncIOScheduler(jobstores={"default": jobstore})


async def start_scheduler():
    """Запуск scheduler."""
    scheduler.start()


async def collect_product_data(artikul: str):
    """Обновление БД по артикулу."""
    async with session_maker() as session:
        await create_or_update_product(artikul, session)
