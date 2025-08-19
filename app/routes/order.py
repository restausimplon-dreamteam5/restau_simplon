from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from sqlmodel import select
from app.models.models import Order, OrderDetail, MenuItem, OrderStatus
from app.schemas.schemas import (
    OrderCreate,
    OrderOut,
    OrderDetailOut,
    OrderWithDetailsOut,
    OrderStatusUpdate,
    TokenData,
)
from app.deps import SessionDep
from app.routes.login import extract_token_data, insufficient_permissions_exception
from decimal import Decimal
from sqlalchemy import func
from datetime import date
from uuid import UUID


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/with_details")
def read_orders_with_details(
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
    skip: int = 0,
    limit: int = 20,
) -> list[OrderWithDetailsOut]:
    """
    Récupération paginée des commandes avec leurs détails.

    * Pagination avec skip et limit
    * Calcul automatique du montant total
    * Utilisation la relation Order.details (back_populates)

    Args:
        session (SessionDep): Session avec la base de données
        skip (int): Nombre d'éléments à ignorer (par défaut 0)
        limit (int): Nombre maximum de résultats à retourner (par défaut 20)

    Returns:
        list[OrderWithDetailsOut]: Liste des commandes avec leurs détails
    """

    # Vérifie que l'utilisateur a bien le rôle "admin"
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    orders = session.exec(select(Order).offset(skip).limit(limit)).all()

    results = []
    for order in orders:
        total_amount = sum(d.unit_price * d.quantity for d in order.details)

        items = [
            OrderDetailOut(
                item_id=d.item_id, quantity=d.quantity, unit_price=d.unit_price
            )
            for d in order.details
        ]

        results.append(
            OrderWithDetailsOut(
                id=order.id,
                user_id=order.user_id,
                order_date=order.order_date,
                status=order.status,
                total_amount=total_amount,
                items=items,
            )
        )

    return results


@router.post("/")
def create_order(
    order: OrderCreate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> OrderOut:
    """**Création d'une commande avec plusieurs articles**

    * Vérifie l'existence de chaque article
    * Calcule automatiquement le montant total
    * Enregistre la commande et ses détails

    Args:
        order (OrderCreate): Données de la commande (user_id + items)
        session (SessionDep): Session avec la base de données

    Returns:
        OrderOut: Commande enregistrée avec son montant total
    """

    # Si c’est un client, il ne peut commander que pour lui-même
    if token_data.has_role("client") and not token_data.is_user(order.user_id):
        raise insufficient_permissions_exception

    total_amount = Decimal("0.00")

    # Création de la commande
    order_db = Order(user_id=order.user_id)
    session.add(order_db)

    # Création des détails de commande
    for item in order.items:
        item_db = session.get(MenuItem, item.item_id)
        if not item_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article ID {item.item_id} non trouvé.",
            )

        detail = OrderDetail(
            order=order_db,
            item_id=item.item_id,
            quantity=item.quantity,
            unit_price=item_db.price,
        )

        total_amount += item.quantity * item_db.price
        session.add(detail)

    session.commit()
    session.refresh(order_db)

    return OrderOut(
        id=order_db.id,
        user_id=order_db.user_id,
        order_date=order_db.order_date,
        status=order_db.status,
        total_amount=total_amount,
    )


@router.get("/by_client/{user_id}")
def get_orders_by_user(
    user_id: UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> list[OrderOut]:
    """**Récupération des commandes d’un utilisateur**

    * Affiche l’historique des commandes associées à un user_id
    * Calcule automatiquement le montant total pour chaque commande

    Args:
        user_id (UUID): Identifiant unique du client
        session (SessionDep): Session de base de données

    Raises:
        HTTPException: Si aucune commande n'est trouvé

    Returns:
        list[OrderOut]: Liste des commandes du client
    """

    # Seul le client concerné OU le staff peuvent accéder
    if (
        not token_data.has_role("admin")
        and not token_data.has_role("employee")
        and not token_data.is_user(user_id)
    ):
        raise insufficient_permissions_exception

    orders = session.exec(select(Order).where(Order.user_id == user_id)).all()

    if not orders:
        raise HTTPException(
            status_code=404, detail="Aucune commande trouvée pour ce client."
        )

    results = []
    for order in orders:
        # Accès direct grâce à la relation back_populates
        total_amount = sum(
            detail.unit_price * detail.quantity for detail in order.details
        )

        results.append(
            OrderOut(
                id=order.id,
                user_id=order.user_id,
                order_date=order.order_date,
                status=order.status,
                total_amount=total_amount,
            )
        )

    return results


@router.get("/by_order/{order_id}")
def get_order_by_id(
    order_id: UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> OrderWithDetailsOut:
    """**Récupération d'une commande avec ses détails**

    * À partir de son ID unique
    * Calcule automatiquement le montant total de la commande

    Args:
        order_id (UUID): L'identifiant unique de la commande
        session (SessionDep): La session communicante avec la BDD

    Raises:
        HTTPException: Si la commande est introuvable

    Returns:
        OrderWithDetailsOut: Les informations complètes de la commande
    """

    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée.")

    # Vérification : seul le propriétaire de la commande OU le staff peut accéder
    if (
        not token_data.has_role("admin")
        and not token_data.has_role("employee")
        and not token_data.is_user(order.user_id)
    ):
        raise insufficient_permissions_exception

    total_amount = sum(d.quantity * d.unit_price for d in order.details)

    items_out = [
        OrderDetailOut(item_id=d.item_id, quantity=d.quantity, unit_price=d.unit_price)
        for d in order.details
    ]

    return OrderWithDetailsOut(
        id=order.id,
        user_id=order.user_id,
        order_date=order.order_date,
        status=order.status,
        total_amount=total_amount,
        items=items_out,
    )


@router.get("/by_date/{query_date}")
def get_orders_by_date(
    query_date: date,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> list[OrderOut]:
    """**Récupération des commandes par date**

    * Retourne toutes les commandes passées à une date précise (format : YYYY-MM-DD)
    * Calcule automatiquement le montant total de chaque commande

    Args:
        query_date (date): La date recherchée (ex: 2025-08-07)
        session (SessionDep): La session communicante avec la BDD

    Raises:
        HTTPException: Si aucune commande n'est trouvée pour cette date

    Returns:
        list[OrderOut]: Liste des commandes avec leurs montants totaux
    """

    # Restriction d'accès : seuls admin/employee peuvent voir toutes les commandes d'une date
    if not token_data.has_role("admin") and not token_data.has_role("employee"):
        raise insufficient_permissions_exception

    orders = session.exec(
        select(Order).where(func.date(Order.order_date) == query_date)
    ).all()

    if not orders:
        raise HTTPException(
            status_code=404, detail="Aucune commande trouvée pour cette date."
        )

    results = []
    for order in orders:
        # Calcul du montant total grace a la relation order.details
        total_amount = sum(
            detail.unit_price * detail.quantity for detail in order.details
        )

        # Construction de l'objet OrderOut
        results.append(
            OrderOut(
                id=order.id,
                user_id=order.user_id,
                order_date=order.order_date,
                status=order.status,
                total_amount=total_amount,
            )
        )

    return results


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: UUID,
    status_update: OrderStatusUpdate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> dict:
    """**Mise à jour du statut d'une commande avec transitions contrôlées**

    * Ne permet que certaines transitions entre les statuts :
        - `pending` → `confirmed` ou `cancelled`
        - `confirmed` → `completed` ou `cancelled`
        - `completed` ou `cancelled` → (aucune transition autorisée)
    * Empêche toute transition non autorisée via une exception

    Args:
        order_id (UUID): L'identifiant unique de la commande
        status_update (OrderStatusUpdate): Le nouveau statut souhaité
        session (SessionDep): La session communicante avec la BDD

    Raises:
        HTTPException: Si la commande n'est pas trouvée ou si la transition est interdite

    Returns:
        dict: Message de confirmation du changement de statut
    """

    # Vérification des rôles
    if not token_data.has_role("admin") and not token_data.has_role("employee"):
        raise insufficient_permissions_exception

    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée.")

    current_status = order.status
    new_status = status_update.new_status

    allowed_transitions = {
        OrderStatus.pending: [OrderStatus.confirmed, OrderStatus.cancelled],
        OrderStatus.confirmed: [OrderStatus.completed, OrderStatus.cancelled],
        OrderStatus.completed: [],
        OrderStatus.cancelled: [],
    }

    if new_status not in allowed_transitions[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Transition de '{current_status.value}' vers '{new_status.value}' non autorisée.",
        )

    order.status = new_status
    session.add(order)
    session.commit()
    session.refresh(order)

    return {"message": f"Statut mis à jour : {new_status.value}"}
