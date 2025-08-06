# Import
import uuid
from sqlmodel import Field, SQLModel, Column, Enum as smEnum
from decimal import Decimal
from enum import Enum
from datetime import datetime


# User
class User(SQLModel, table=True):
    __tablename__ = "user_info"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone: str
    address: str | None
    email: str = Field(index=True)
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


# Order
