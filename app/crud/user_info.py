from sqlmodel import Session

from app.models.models import User


def create_user_info_in_db(session: Session, user_info_db: User) -> bool:
    """Création d'un utilisateur dans la base de données.

    Args:
        session (Session): La session communicante avec la BDD
        user_info (User): L'utilisateur à insérer en base.

    Returns:
        bool: Vrai si l'article a été mis en base
    """
    session.add(user_info_db)
    session.commit()
    session.refresh(user_info_db)
    return True
