from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from app.models.models import Order, OrderDetail, MenuItem
from app.schemas.schemas import OrderCreate, OrderOut, OrderDetailCreate, OrderDetailOut, OrderWithDetailsOut
from app.deps import SessionDep
from decimal import Decimal
from sqlalchemy import func
from datetime import date
from uuid import UUID


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, session: SessionDep) -> OrderOut:
    """Création d'une commande avec plusieurs articles"""

    # Création de la commande
    order_db = Order(user_id=order.user_id)
    session.add(order_db)
    session.commit()
    session.refresh(order_db)

    total_amount = Decimal("0.00")

    # Création des détails de la commande
    for item in order.items:
        # Vérification du produit
        item_db = session.get(MenuItem, item.item_id)
        if not item_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article ID {item.item_id} non trouvé."
            )
        # Création d'un détail
        detail = OrderDetail(
            order_id=order_db.id,
            item_id=item.item_id,
            quantity=item.quantity,
            unit_price=item_db.price
        )
        total_amount += item.quantity * item_db.price
        session.add(detail)

    session.commit()

    # On renvoie l'Order + total_amount
    return OrderOut(
        id=order_db.id,
        status=order_db.status,
        order_date=order_db.order_date,
        user_id=order_db.user_id,
        total_amount=total_amount
    )


@router.get("/by_client/{user_id}", response_model=list[OrderOut])
def get_orders_by_user(user_id: UUID, session: SessionDep) -> list[OrderOut]:
    """
    Récupérer toutes les commandes d'un utilisateur spécifique.

    - Cette route retourne la liste des commandes associées à un user_id.
    - Utile pour afficher l’historique des commandes d’un client.

    Args:
        user_id (UUID): L'identifiant du client.
        session (SessionDep): Session de base de données.

    Raises:
        HTTPException: Si aucune commande n'est trouvée.

    Returns:
        list[OrderOut]: Liste des commandes du client.
    """
    orders = session.exec(select(Order).where(Order.user_id == user_id)).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour ce client.")

    result = []
    for order in orders:
        # Récupérer les détails de cette commande
        details = session.exec(
            select(OrderDetail).where(OrderDetail.order_id == order.id)
        ).all()

        # Calcul du total
        total_amount = sum(detail.quantity * detail.unit_price for detail in details)

        # Création de l'objet OrderOut
        result.append(
            OrderOut(
                id=order.id,
                user_id=order.user_id,
                order_date=order.order_date,
                status=order.status,
                total_amount=total_amount
            )
        )

    return result

@router.get("/{order_id}", response_model=OrderWithDetailsOut)
def get_order_by_id(order_id: UUID, session: SessionDep) -> OrderWithDetailsOut:
    """
    Récupérer une commande avec ses détails à partir de son ID.
    """
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée.")

    # Récupérer les détails associés
    details = session.exec(
        select(OrderDetail).where(OrderDetail.order_id == order_id)
    ).all()

    total_amount = sum(d.quantity * d.unit_price for d in details)

    items_out = [
        OrderDetailOut(
            item_id=d.item_id,
            quantity=d.quantity,
            unit_price=d.unit_price
        )
        for d in details
    ]

    return OrderWithDetailsOut(
        id=order.id,
        user_id=order.user_id,
        order_date=order.order_date,
        status=order.status,
        total_amount=total_amount,
        items=items_out
    )

@router.get("/by_date/{query_date}", response_model=list[OrderOut])
def get_orders_by_date(query_date: date, session: SessionDep) -> list[OrderOut]:
    """
    Récupérer les commandes créées à une date précise (ex: 2025-08-07)
    """
    orders = session.exec(
        select(Order).where(func.date(Order.order_date) == query_date)
    ).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée pour cette date.")

    results = []
    for order in orders:
        # Récupération des détails de commande
        details = session.exec(
            select(OrderDetail).where(OrderDetail.order_id == order.id)
        ).all()

        # Calcul du montant total
        total_amount = sum(detail.unit_price * detail.quantity for detail in details)

        # Construction de l'objet OrderOut
        results.append(OrderOut(
            id=order.id,
            user_id=order.user_id,
            order_date=order.order_date,
            status=order.status,
            total_amount=total_amount
        ))

    return results

    