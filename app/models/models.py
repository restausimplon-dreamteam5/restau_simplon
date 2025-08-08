# Import
import uuid
from sqlmodel import Field, SQLModel, Relationship, Column, Enum as smEnum
from typing import Optional, List
from decimal import Decimal
from enum import Enum
from datetime import datetime
from pydantic import EmailStr


# User
class User(SQLModel, table=True):
    __tablename__ = "user_info"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    # On a choisi de prendre en charges les numéro de type "0677889910". 
    # Pas d'espaces, pas prefix comme +33
    # Que des numeros français de 10 caractères
    # TODO: on pourrait verifier les prefix valables 06, 07, 01, 02, 03, 04,05 ...
    # TODO: regarder du côté de pydantic
    # THINK: Est ce que le pattern à besoin d'être la ? 
    # Il devrait être dans le schema d'entré. mais dans la db peut être pas
    phone: str = Field(
        min_length=10, max_length=10, schema_extra={"pattern": r"^[0-9]*$"}
    )
    # Adresse complète comme (46 rue des michels 44000 Nantes)
    address: str | None = Field(max_length=200)
    email: EmailStr = Field(index=True, unique=True, max_length=320)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)


# Article
class MenuCategory(str, Enum):
    "Énumération des catégories dans le menu"

    starter = "starter"
    main_course = "main course"
    dessert = "dessert"


class MenuItem(SQLModel, table=True):
    """Modèle d'article de menu pour la base de données"""

    __tablename__ = "menu_item"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(..., unique=True, index=True, max_length=100)
    price: Decimal = Field(..., max_digits=8, decimal_places=2)
    category: MenuCategory = Field(...)
    # category: MenuCategory = Field(
    #     sa_column=Column(
    #         smEnum(MenuCategory, name="category", create_type=True),
    #         nullable=False,
    #     ),
    # )
    description: str | None = Field(None)
    stock: int = Field(default=0, ge=0)


# Commande
class OrderStatus(str, Enum):
    "Énumération des statuts de commande"

    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

# Modele commande
class Order(SQLModel, table=True):
    """Modèle de commande pour la base de données"""

    __tablename__ = "order"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: OrderStatus = Field(default=OrderStatus.pending)
    order_date: datetime = Field(default_factory=datetime.now)

    user_id: uuid.UUID = Field(foreign_key="user_info.id")
    details: List["OrderDetail"] = Relationship(back_populates="order")

# Modele detail commande
class OrderDetail(SQLModel, table=True):
    """Modèle de détail de commande pour la base de données"""

    __tablename__ = "order_detail"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
   
    order_id: uuid.UUID = Field(foreign_key="order.id")
    item_id: uuid.UUID = Field(foreign_key="menu_item.id")
    
    quantity: int = Field(gt=0, default=1)
    unit_price: Decimal = Field(..., max_digits=8, decimal_places=2) 

    # Relation inverse avec Order
    order: Optional[Order] = Relationship(back_populates="details")
