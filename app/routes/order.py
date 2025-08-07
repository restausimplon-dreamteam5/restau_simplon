from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from app.models.models import Order, OrderDetail, MenuItem
from app.schemas.schemas import OrderCreate, OrderOut, OrderDetailCreate
from app.deps import SessionDep
from decimal import Decimal
import uuid


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

    