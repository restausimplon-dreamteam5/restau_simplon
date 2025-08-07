from sqlmodel import Session
from app.models.models import Order, OrderDetail


def create_order_detail_in_db(session: Session, order_detail_db: OrderDetail) -> bool:
    """Création d'un détail de commande dans la base de données.

    Args:
        session (Session): La session communicante avec la BDD
        order_detail (OrderDetail): Le détail de commande à insérer en base.

    Returns:
        bool: Vrai si l'article a été mis en base
    """
    session.add(order_detail_db)
    session.commit()
    session.refresh(order_detail_db)
    return True


def create_order_in_db(session: Session, order_db: Order) -> bool:
    """Création d'une commande dans la base de données.

    Args:
        session (Session): La session communicante avec la BDD
        order (Order): La commande à insérer en base.

    Returns:
        bool: Vrai si l'article a été mis en base
    """
    session.add(order_db)
    session.commit()
    session.refresh(order_db)
    return True
