from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import validate_token
from app.api.dependencies.db import get_session
from app.core.config import settings
from app.schemas.products import ProductCreate, ProductRead
from app.services.products import create_or_update_product
from app.services.scheduler import scheduler, collect_product_data

router = APIRouter()


@router.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token),
):
    """Обновляет либо добавляет информацию в БД по указанному артикулу."""
    try:
        product = await create_or_update_product(product_in.artikul, session)
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/subscribe/{artikul}", status_code=status.HTTP_200_OK)
async def subscribe(
    artikul: str,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token),
):
    """Обновляет информацию о товаре и добавляет его в список подписок."""
    try:
        await create_or_update_product(artikul, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    job_id = f"collect_{artikul}"

    if scheduler.get_job(job_id):
        return {
            "message": f"Артикул {artikul} уже добавлен в расписание.",
        }

    scheduler.add_job(
        collect_product_data,
        "interval",
        minutes=settings.schedule_interval_minutes,
        id=job_id,
        args=[artikul],
    )
    return {
        "message": f"Артикул {artikul} успешно добавлен в расписание.",
    }
