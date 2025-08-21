from fastapi import APIRouter
from sqlmodel import select

from app.deps import SessionDep
from app.models.models import Role

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
def get_all_users(session: SessionDep) -> list[Role]:
    """Renvoie tous les rôles

    Args:
    * session (SessionDep): (interne) connexion à la base de données

    Returns:
    * list[Role]: la liste des roles
    """
    roles = session.exec(select(Role)).all()
    return list(roles)
