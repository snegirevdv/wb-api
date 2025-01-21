from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Схема для POST-запроса на создание товара."""

    artikul: str = Field(default=..., description="Артикул")


class ProductRead(BaseModel):
    """Схема для вывода информации о товаре."""

    id: int
    artikul: str
    name: str
    price: int
    rating: float
    total_in_stock: int

    model_config = ConfigDict(from_attributes=True)
