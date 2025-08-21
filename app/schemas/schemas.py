# Import
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.models.models import MenuCategory, OrderStatus, Role


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
    roles: list[str]


class ClientCreate(SQLModel):
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone: str = Field(
        min_length=10, max_length=10, schema_extra={"pattern": r"^[0-9]*$"}
    )
    # Adresse complète comme (46 rue des michels 44000 Nantes)
    address: str | None = Field(default=None, max_length=200)
    email: EmailStr = Field(max_length=320)
    password: str


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
    roles: list[str]


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
    roles: list[str] | None = None


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
    roles: list[Role]


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    sub: str  # user id
    roles: list[str]
    exp: datetime

    def has_role(self, role: str) -> bool:
        return role in self.roles

    def is_user(self, user_id: uuid.UUID):
        return uuid.UUID(self.sub) == user_id


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
    """
    **Schéma d’entrée** pour une **ligne d’article** dans une commande.

    **Utilisation**
    - Inclus dans `OrderCreate.items`.

    **Contraintes**
    - `quantity` > **0** (par défaut **1**).

    Attributes:
        item_id (UUID): **Identifiant** de l’article (`MenuItem.id`).
        quantity (int): **Quantité** commandée (> 0).

    Example:
        {
          "item_id": "d5a6b3f1-8f4a-4c25-9c91-6a2e4ee9c1a2",
          "quantity": 2
        }
    """

    item_id: UUID
    quantity: int = Field(default=1, gt=0)


class OrderDetailOut(SQLModel):
    """
    **Schéma de sortie** pour une **ligne d’article** d’une commande.

    **Notes**
    - `unit_price` est le **prix unitaire au moment de la commande** (type `Decimal`).

    Attributes:
        item_id (UUID): **Identifiant** de l’article.
        quantity (int): **Quantité** commandée.
        unit_price (Decimal): **Prix unitaire** (devise du système, ex. EUR).

    Example:
        {
          "item_id": "d5a6b3f1-8f4a-4c25-9c91-6a2e4ee9c1a2",
          "quantity": 2,
          "unit_price": "12.90"
        }
    """

    item_id: UUID
    quantity: int
    unit_price: Decimal


class OrderOut(SQLModel):
    """
    **Schéma de sortie** pour une **commande** (sans les lignes).

    **Contenu**
    - Métadonnées de la commande (**id**, **user_id**, **order_date**, **status**).
    - Montant total **calculé**: `total_amount = Σ(quantity × unit_price)`.

    Attributes:
        id (UUID): **Identifiant** de la commande.
        user_id (UUID): **Identifiant** du client.
        order_date (datetime): **Date/heure** de création (ISO 8601).
        status (OrderStatus): **Statut** de la commande (`pending`, `confirmed`, `completed`, `cancelled`).
        total_amount (Decimal): **Montant total** de la commande.

    Example:
        {
          "id": "b1a9d0e7-0d73-4e76-b5e6-0f3b1c7a9c2f",
          "user_id": "c4e58f9c-0b2f-4a64-9f1e-8e3c1b2d8c11",
          "order_date": "2025-08-07T10:42:31.123Z",
          "status": "confirmed",
          "total_amount": "38.70"
        }
    """

    id: UUID
    user_id: UUID
    order_date: datetime
    status: OrderStatus
    total_amount: Decimal


class OrderWithDetailsOut(OrderOut):
    """
    **Schéma de sortie** pour une **commande complète** (commande **+** lignes).

    Hérite de **OrderOut** et ajoute:
    - `items`: liste des **détails** (`OrderDetailOut`).

    Attributes:
        items (list[OrderDetailOut]): **Lignes** de la commande.

    Example:
        {
          "id": "b1a9d0e7-0d73-4e76-b5e6-0f3b1c7a9c2f",
          "user_id": "c4e58f9c-0b2f-4a64-9f1e-8e3c1b2d8c11",
          "order_date": "2025-08-07T10:42:31.123Z",
          "status": "confirmed",
          "total_amount": "38.70",
          "items": [
            {"item_id": "d5a6b3f1-8f4a-4c25-9c91-6a2e4ee9c1a2", "quantity": 2, "unit_price": "12.90"},
            {"item_id": "a9b1c2d3-4e5f-6789-0123-456789abcdef", "quantity": 1, "unit_price": "12.90"}
          ]
        }
    """

    items: list[OrderDetailOut]


# Commande
class OrderCreate(SQLModel):
    """
    **Schéma d’entrée** pour **créer** une commande.

    **Règles**
    - Le rôle **`client`** ne peut créer une commande que **pour lui-même** (côté routes).
    - `items` doit être **non vide** (attendu fonctionnellement).

    Attributes:
        user_id (UUID): **Identifiant** du client.
        order_date (datetime): **Date/heure** de création (défaut: `datetime.now()`).
        items (List[OrderDetailCreate]): **Lignes** de commande.

    Example:
        {
          "user_id": "c4e58f9c-0b2f-4a64-9f1e-8e3c1b2d8c11",
          "order_date": "2025-08-07T10:40:00Z",
          "items": [
            {"item_id": "d5a6b3f1-8f4a-4c25-9c91-6a2e4ee9c1a2", "quantity": 2},
            {"item_id": "a9b1c2d3-4e5f-6789-0123-456789abcdef", "quantity": 1}
          ]
        }
    """

    user_id: UUID
    order_date: datetime = Field(default_factory=datetime.now)
    items: List[OrderDetailCreate]


class OrderStatusUpdate(SQLModel):
    """
    **Schéma d’entrée** pour **mettre à jour** le statut d’une commande.

    **Transitions autorisées** (voir logique des routes):
    - `pending` → `confirmed` **ou** `cancelled`
    - `confirmed` → `completed` **ou** `cancelled`
    - `completed` **ou** `cancelled` → *(aucune transition autorisée)*

    Attributes:
        new_status (OrderStatus): **Nouveau statut** souhaité.

    Example:
        {
          "new_status": "confirmed"
        }
    """

    new_status: OrderStatus
