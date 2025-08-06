# Import
import uuid
from pydantic import BaseModel, Field
from decimal import Decimal
from app.models.models import MenuCategory


# User


# Article
class MenuItemCreate(BaseModel):
    """Modèle de création d'article de menu"""

    name: str = Field(max_length=100)
    price: Decimal = Field(..., max_digits=8, decimal_places=2)
    category: MenuCategory = Field(...)
    description: str | None = None
    stock: int = Field(default=0, ge=0)


class MenuItemOut(BaseModel):
    """Modèle de création d'article de menu"""

    id: uuid.UUID
    name: str
    price: Decimal = Field(..., max_digits=8, decimal_places=2)
    category: MenuCategory
    description: str | None = None
    stock: int


# Order
