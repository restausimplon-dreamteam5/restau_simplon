# Import
from datetime import datetime
import uuid
from decimal import Decimal

from pydantic import EmailStr
from app.models.models import MenuCategory
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime
from typing import List
from app.models.models import OrderStatus



# User
# TODO: find out about doc
class UserCreate(SQLModel):
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone: str = Field(
        min_length=10, max_length=10, schema_extra={"pattern": r"^[0-9]*$"}
    )
    # Adresse complète comme (46 rue des michels 44000 Nantes)
    address: str | None = Field(default=None, max_length=200)
    email: EmailStr = Field(max_length=320)
    password: str


class UserPatch(SQLModel):
    first_name: str | None = Field(default=None, max_length=50)
    surname: str | None = Field(default=None, max_length=50)
    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        schema_extra={"pattern": r"^[0-9]*$"},
    )
    # Adresse complète comme (46 rue des michels 44000 Nantes)
    address: str | None = Field(default=None, max_length=200)
    email: EmailStr | None = Field(default=None, max_length=320)
    password: str | None = None


class UserPost(SQLModel):
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

# Detail commande
class OrderDetailCreate(SQLModel):
    """Schéma d’entrée pour un article dans une commande"""

    item_id: UUID
    quantity: int = Field(default=1, gt=0)

# Commande
class OrderCreate(SQLModel):
    """Schéma pour créer une commande"""

    user_id: UUID
    order_date: datetime = Field(default_factory=datetime.now)
    items: List[OrderDetailCreate]

class OrderOut(SQLModel):
    """Schéma de sortie pour une commande
       Contient les informations de la commande une fois créée ou consultée
    """

    id: UUID
    user_id: UUID
    order_date: datetime
    status: OrderStatus
    total_amount: Decimal 

class OrderStatusUpdate(SQLModel):
    """Schéma pour mettre à jour le statut d'une commande
       Permet de changer le statut d'une commande existante
    """

    new_status: OrderStatus
    
    
    




