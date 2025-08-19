from sqlmodel import Session

from app.models.models import MenuItem


def create_menu_item_in_db(session: Session, menu_item_db: MenuItem) -> bool:
    """Création d'un article de menu dans la base de données.

    Args:
        session (Session): La session communicante avec la BDD
        menu_item (MenuItem): L'article de menu aà insérer en base.

    Returns:
        bool: Vrai si l'article a été mis en base
    """
    session.add(menu_item_db)
    session.commit()
    session.refresh(menu_item_db)
    return True
