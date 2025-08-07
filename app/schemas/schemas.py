# Import
import uuid
from decimal import Decimal
from app.models.models import MenuCategory
from sqlmodel import SQLModel, Field


# User


# Article
class MenuItemCreate(SQLModel):
    """Modèle de création d'article de menu"""

    name: str = Field(max_length=100)
    price: Decimal = Field(..., max_digits=8, decimal_places=2)
    category: MenuCategory = Field(...)
    description: str | None = None
    stock: int = Field(default=0, ge=0)


class MenuItemUpdate(SQLModel):
    """Modèle de mise à jour d'article de menu"""

    name: str | None = Field(default=None, max_length=100)
    price: Decimal | None = Field(default=None, max_digits=8, decimal_places=2)
    category: MenuCategory | None = None
    description: str | None = None
    stock: int | None = Field(default=None, ge=0)


class MenuItemOut(SQLModel):
    """Modèle de création d'article de menu"""

    id: uuid.UUID
    name: str
    price: Decimal = Field(..., max_digits=8, decimal_places=2)
    category: MenuCategory
    description: str | None = None
    stock: int


# Order
