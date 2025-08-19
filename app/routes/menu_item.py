from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select

from app.crud.menu_items import create_menu_item_in_db
from app.deps import SessionDep
from app.models.models import MenuCategory, MenuItem
from app.routes.login import extract_token_data, insufficient_permissions_exception
from app.schemas.schemas import MenuItemCreate, MenuItemOut, MenuItemUpdate, TokenData

router = APIRouter(prefix="/menu_items", tags=["Menu items"])


@router.post("/")
def create_menu_item(
    menu_item: MenuItemCreate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> MenuItemOut:
    """**Ajout d'un article de menu dans la base de donnée.**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemCreate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: admin, staff

    **Args**:
    * menu_item (*MenuItemCreate*): Les informations entrantes
    * session (*SessionDep*): La session communicante avec la BDD

    **Returns**:
    * *MenuItemOut*: Les informations sortantes
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    menu_item_db = MenuItem(**menu_item.model_dump())
    create_menu_item_in_db(session, menu_item_db)
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())

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

    **Permissions**: sans condition

    **Args**:
    * **session** (*SessionDep*): La session communicante avec la BDD
    * **offset** (*int*, optional): Décalage pour le premier article à lire. Par défaut: 0.
    * **limit** (*int* <= 100, optional): Limite du nombre d'articles retournées. Par défaut: 100.

    *Returns*:
    * *list[MenuItemOut]*: Liste des informations sortantes
    """

    menu_items_db = session.exec(select(MenuItem).offset(offset).limit(limit)).all()
    menu_items_out = [
        MenuItemOut(**menu_item_db.model_dump()) for menu_item_db in menu_items_db
    ]
    return menu_items_out


@router.get("/category/{menu_category}")
def read_menu_category(menu_category: str, session: SessionDep) -> list[MenuItemOut]:
    """**Récupération des articles de menu**, dont la catégorie est **menu_category**

    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: sans condition

    **Args**:
    * **menu_category** (*str*): La catégorie d'articles de menu
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Catégorie de menu inexistante

    **Returns**:
    * (*list[MenuItemOut]*): Liste des informations sortantes
    """

    if menu_category in MenuCategory:
        menu_items_db = session.exec(
            select(MenuItem).where(MenuItem.category == menu_category)
        ).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"La catégorie {menu_category} n'existe pas dans l'énumération de catégorie",
        )

    if not menu_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No menu items found"
        )

    menu_items_out = [
        MenuItemOut(**menu_item_db.model_dump()) for menu_item_db in menu_items_db
    ]

    return menu_items_out


@router.get("/name/{menu_item_name}")
def read_menu_item_by_name(menu_item_name: str, session: SessionDep) -> MenuItemOut:
    """**Récupération de l'article de menu**, dont le nom est **menu_item_name**

    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: sans condition

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
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())
    return menu_item_out


@router.get("/id/{menu_item_id}")
def read_menu_item_by_id(menu_item_id: UUID, session: SessionDep) -> MenuItemOut:
    """**Récupération de l'article de menu**, dont l'ID est **menu_item_id**

    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: sans condition

    **Args**:
    * **menu_item_id** (*UUID*): L'ID unique de l'article de menu
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """

    menu_item_db = session.get(MenuItem, menu_item_id)
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())
    return menu_item_out


@router.patch("/name/{menu_item_name}")
def partial_update_menu_item_by_name(
    menu_item_name: str,
    new_menu_item: MenuItemUpdate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> MenuItemOut:
    """**Mise à jour partielle de l'article de menu**, dont le nom est **menu_item_name**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemUpdate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: admin, staff

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **new_menu_item** (*MenuItemUpdate*): Les informations entrantes
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    # Recherche de l'article de menu dans la base
    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    # Préparation de la mise à jour partielle
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

    # Mise à jour
    create_menu_item_in_db(session, menu_item_db)
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())
    return menu_item_out


@router.patch("/id/{menu_item_id}")
def partial_update_menu_item_by_id(
    menu_item_id: UUID,
    new_menu_item: MenuItemUpdate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> MenuItemOut:
    """**Mise à jour partielle de l'article de menu**, dont l'ID est **menu_item_id**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemUpdate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: admin, staff

    **Args**:
    * **menu_item_id** (*UUID*): L'ID unique de l'article
    * **new_menu_item** (*MenuItemUpdate*): Les informations entrantes
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    # Recherche de l'article de menu dans la base de données
    menu_item_db = session.get(MenuItem, menu_item_id)
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    # Préparation de la mise à jour partielle
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

    # Mise à jour
    create_menu_item_in_db(session, menu_item_db)
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())
    return menu_item_out


@router.put("/name/{menu_item_name}")
def update_menu_item_by_name(
    menu_item_name: str,
    new_menu_item: MenuItemCreate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> MenuItemOut:
    """**Mise à jour complète de l'article de menu**, dont le nom est **menu_item_name**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemCreate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: admin, staff

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **new_menu_item** (*MenuItemCreate*): Les informations entrantes
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    # Recherche de l'article de menu dans la base de données
    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    # Préparation de la mise à jour
    for key, value in new_menu_item.model_dump().items():
        setattr(menu_item_db, key, value)

    create_menu_item_in_db(session, menu_item_db)
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())
    return menu_item_out


@router.put("/id/{menu_item_id}")
def update_menu_item_by_id(
    menu_item_id: UUID,
    new_menu_item: MenuItemCreate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> MenuItemOut:
    """**Mise à jour complète de l'article de menu**, dont l'ID est **menu_item_id**

    * Validation des données entrantes grâce au schéma Pydantic **MenuItemCreate**
    * Filtrage des données sortantes grâce au schéma Pydantic **MenuItemOut**

    **Permissions**: admin, staff

    **Args**:
    * **menu_item_id** (*UUID*): L'ID unique de l'article
    * **new_menu_item** (*MenuItemCreate*): Les informations entrantes
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*MenuItemOut*): Les informations sortantes
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    # Recherche de l'article de menu dans la base de données
    menu_item_db = session.get(MenuItem, menu_item_id)
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    # Préparation de la mise à jour
    for key, value in new_menu_item.model_dump().items():
        setattr(menu_item_db, key, value)

    create_menu_item_in_db(session, menu_item_db)
    menu_item_out = MenuItemOut(**menu_item_db.model_dump())
    return menu_item_out


@router.delete("/name/{menu_item_name}")
def delete_menu_item_by_name(
    menu_item_name: str,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> bool:
    """**Suppression de l'article de menu**, dont le nom est **menu_item_name**

    **Permissions**: admin, staff

    **Args**:
    * **menu_item_name** (*str*): Le nom de l'article
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*bool*): Vrai si l'article a été supprimé
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    # Recherche de l'article de menu
    menu_item_db = session.exec(
        select(MenuItem).where(MenuItem.name == menu_item_name)
    ).first()
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    # Suppression
    session.delete(menu_item_db)
    session.commit()
    return True


@router.delete("/id/{menu_item_id}")
def delete_menu_item_by_id(
    menu_item_id: UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> bool:
    """**Suppression de l'article de menu**, dont l'ID est **menu_item_id**

    **Permissions**: admin, staff

    **Args**:
    * **menu_item_id** (*UUID*): L'ID unique de l'article
    * **session** (*SessionDep*): La session communicante avec la BDD

    **Raises**:
    * *HTTPException*: Article de menu introuvable

    **Returns**:
    * (*bool*): Vrai si l'article a été supprimé
    """
    # Gestion permission
    if not token_data.has_role("admin") and not token_data.has_role("staff"):
        raise insufficient_permissions_exception

    # Recherche de l'article de menu
    menu_item_db = session.get(MenuItem, menu_item_id)
    if not menu_item_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
        )

    # Suppression
    session.delete(menu_item_db)
    session.commit()
    return True
