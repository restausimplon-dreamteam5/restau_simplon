from fastapi import APIRouter, HTTPException, Query, status
from typing import Annotated
from decimal import Decimal
from sqlmodel import select
from app.schemas.schemas import MenuItemCreate, MenuItemOut, MenuItemUpdate
from app.models.models import MenuItem, MenuCategory
from app.deps import SessionDep

router = APIRouter(prefix="/menu_items", tags=["Menu items"])


@router.post("/")
def create_menu_item(menu_item: MenuItemCreate, session: SessionDep) -> MenuItemOut:
    """**Ajout d'un article de menu dans la base de donnée.**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemCreate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    Args:
        menu_item (MenuItemCreate): Les informations entrantes
        session (SessionDep): La session communicante avec la BDD

    Returns:
        MenuItemOut: Les informations sortantes
    """

    # Conversion
    menu_item_db = MenuItem(
        name=menu_item.name,
        price=menu_item.price,
        category=menu_item.category,
        description=menu_item.description,
        stock=menu_item.stock,
    )

    # Mise en base
    session.add(menu_item_db)
    session.commit()
    session.refresh(menu_item_db)

    # Récupération
    menu_item_out = MenuItemOut(
        id=menu_item_db.id,
        name=menu_item_db.name,
        price=menu_item_db.price,
        category=menu_item_db.category,
        description=menu_item_db.description,
        stock=menu_item_db.stock,
    )
    return menu_item_out


@router.get("/")
def read_menu_items(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[MenuItemOut]:
    """**Lecture (possiblement partiel) du menu**:
    récupération des articles de menus, à partir de **offset**
    jusqu'à une limite de **limit** articles.

    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    Args:
        session (SessionDep): La session communicante avec la BDD
        offset (int, optional): Décalage pour le premier article à lire. Par défaut: 0.
        limit (int <= 100, optional): Limite du nombre d'articles retournées. Par défaut: 100.

    Returns:
        list[MenuItemOut]: Liste des informations sortantes
    """

    menu_items_db = session.exec(select(MenuItem).offset(offset).limit(limit)).all()
    menu_items_out = [
        MenuItemOut(
            id=menu_item_db.id,
            name=menu_item_db.name,
            price=menu_item_db.price,
            category=menu_item_db.category,
            description=menu_item_db.description,
            stock=menu_item_db.stock,
        )
        for menu_item_db in menu_items_db
    ]
    return menu_items_out


@router.get("/{menu_item_name}")
def read_menu_item(menu_item_name: str, session: SessionDep) -> MenuItemOut:
    """**Récupération de l'article de menu**, dont le nom est **menu_item_name**

    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """

    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    menu_item_out = MenuItemOut(
        id=menu_item_db.id,
        name=menu_item_db.name,
        price=menu_item_db.price,
        category=menu_item_db.category,
        description=menu_item_db.description,
        stock=menu_item_db.stock,
    )
    return menu_item_out


@router.patch("/{menu_item_name}")
def partial_update_menu_item(
    menu_item_name: str, new_menu_item: MenuItemUpdate, session: SessionDep
) -> MenuItemOut:
    """**Mise à jour partielle de l'article de menu**, dont le nom est **menu_item_name**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemUpdate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **new_menu_item** (*MenuItemUpdate*): Les informations entrantes
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """

    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    if new_menu_item.name:
        menu_item_db.name = new_menu_item.name
    if new_menu_item.price:
        menu_item_db.price = new_menu_item.price
    if new_menu_item.category:
        menu_item_db.category = new_menu_item.category
    if new_menu_item.description:
        menu_item_db.description = new_menu_item.description
    if new_menu_item.stock:
        menu_item_db.stock = new_menu_item.stock

    session.add(menu_item_db)
    session.commit()
    session.refresh(menu_item_db)

    menu_item_out = MenuItemOut(
        id=menu_item_db.id,
        name=menu_item_db.name,
        price=menu_item_db.price,
        category=menu_item_db.category,
        description=menu_item_db.description,
        stock=menu_item_db.stock,
    )
    return menu_item_out


@router.put("/{menu_item_name}")
def update_menu_item(
    menu_item_name: str, new_menu_item: MenuItemCreate, session: SessionDep
) -> MenuItemOut:
    """**Mise à jour complète de l'article de menu**, dont le nom est **menu_item_name**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemCreate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **new_menu_item** (*MenuItemCreate*): Les informations entrantes
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """

    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    menu_item_db.name = new_menu_item.name
    menu_item_db.price = new_menu_item.price
    menu_item_db.category = new_menu_item.category
    menu_item_db.description = new_menu_item.description
    menu_item_db.stock = new_menu_item.stock

    session.add(menu_item_db)
    session.commit()
    session.refresh(menu_item_db)

    menu_item_out = MenuItemOut(
        id=menu_item_db.id,
        name=menu_item_db.name,
        price=menu_item_db.price,
        category=menu_item_db.category,
        description=menu_item_db.description,
        stock=menu_item_db.stock,
    )
    return menu_item_out


@router.delete("/{menu_item_name}")
def delete_menu_item(menu_item_name: str, session: SessionDep) -> bool:
    """**Suppression de l'article de menu**, dont le nom est **menu_item_name**

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*bool*): Vrai si l'article a été supprimé
    """

    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    session.delete(menu_item_db)
    session.commit()
    return True
