from sqlmodel import Session

from app.models.models import Order, OrderDetail


def create_order_detail_in_db(session: Session, order_detail_db: OrderDetail) -> bool:
    """Créer une **commande** en base.

    Effectue **add → commit → refresh** sur l'objet fourni.

    Args:
        session (Session): Session de base de données.
        order_db (Order): Commande à persister.

    Returns:
        bool: **True** si l'enregistrement a été **persisté et rafraîchi**.

    Raises:
        Exception: Toute erreur de persistance SQL/connexion (propagée telle quelle).
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
