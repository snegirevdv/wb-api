from http import HTTPStatus

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.product import Product


async def get_data_from_wb(artikul: str) -> dict:
    """Запрашивает данные о товаре с Wildberries."""
    url = settings.wb_url + artikul

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != HTTPStatus.OK:
        raise ValueError("Ошибка при запросе к WB.")

    data = response.json()

    try:
        product_data: dict = data["data"]["products"][0]
        name = product_data["name"]
        price = product_data["salePriceU"] // 100
        rating = float(product_data.get("rating", 0))
        total_in_stock = sum(
            stock["qty"] for size in product_data["sizes"] for stock in size["stocks"]
        )

        return {
            "artikul": artikul,
            "name": name,
            "price": price,
            "rating": rating,
            "total_in_stock": total_in_stock,
        }

    except IndexError:
        raise ValueError(f"Товар с артикулом {artikul} не найден.")

    except KeyError:
        raise ValueError("Структура ответа WB не соответствует ожидаемой.")


async def create_or_update_product(artikul: str, session: AsyncSession) -> Product:
    """Проверяет наличие товара в БД и обновляет либо создаёт его."""
    data = await get_data_from_wb(artikul)
    query = select(Product).where(Product.artikul == artikul)
    product = await session.scalar(query)

    if product:
        product.name = data["name"]
        product.price = data["price"]
        product.rating = data["rating"]
        product.total_in_stock = data["total_in_stock"]
    else:
        product = Product(**data)
        session.add(product)

    await session.commit()
    await session.refresh(product)

    return product
