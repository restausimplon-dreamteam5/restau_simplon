from fastapi import APIRouter
from sqlmodel import select

from app.deps import SessionDep
from app.models.models import Role

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
def get_all_users(session: SessionDep) -> list[Role]:
    roles = session.exec(select(Role)).all()
    return list(roles)
