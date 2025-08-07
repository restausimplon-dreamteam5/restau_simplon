from typing import Annotated
import uuid
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
from app.schemas.schemas import UserCreate, UserOut
from app.models.models import User
from app.deps import SessionDep

router = APIRouter(prefix="/users", tags=["User"])


# TODO: droits admin
@router.get("/")
def get_all_users(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[UserOut]:
    users = session.exec(select(User).offset(offset).limit(limit))
    return users

@router.get("/{id}")
def get_user_by_id(id: uuid.UUID, session: SessionDep) -> UserOut:
    return session.exec(select(User).where(User.id==id)).one()

@router.post("/")
def insert_user(new_user: UserCreate, session: SessionDep) -> UserOut:
    user_db = User(
        first_name=new_user.first_name,
        surname=new_user.surname,
        phone=new_user.phone,
        address=new_user.address,
        email=new_user.email,
        password=new_user.password,  # TODO: hash and salt password
    )
    session.add(user_db)
    session.commit()
    print(user_db)
    return user_db

