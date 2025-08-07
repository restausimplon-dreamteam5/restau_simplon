# Import
from datetime import datetime
import uuid
from decimal import Decimal

from pydantic import EmailStr
from app.models.models import MenuCategory
from sqlmodel import SQLModel, Field


# User
# TODO: find out about doc
class UserCreate(SQLModel):
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone: str = Field(
        min_length=10, max_length=10, schema_extra={"pattern": r"^[0-9]*$"}
    )
    # Adresse complète comme (46 rue des michels 44000 Nantes)
    address: str | None = Field(max_length=200)
    email: EmailStr = Field(max_length=320)
    password: str

class UserOut(SQLModel):
    """
    Téléphone: numéro de type "0677889910". Pas d'espaces, pas prefix national (+33). Juste 10 numero. 
    Adresse: Adresse complète (ex: 46 rue des michels 44000 Nantes) 
    """
    id: uuid.UUID
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone: str = Field(
        min_length=10, max_length=10, schema_extra={"pattern": r"^[0-9]*$"}
    )
    address: str | None = Field(max_length=200)
    email: EmailStr = Field(max_length=320)
    created_at: datetime
    

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
