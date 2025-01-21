from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float

from app.models.base import Base


class Product(Base):
    """Модель товара."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    artikul: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    total_in_stock: Mapped[int] = mapped_column(Integer)
