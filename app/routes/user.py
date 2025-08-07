from typing import Annotated
import uuid
import bcrypt
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select
from app.schemas.schemas import UserCreate, UserOut, UserPatch, UserPost
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
    return session.exec(select(User).where(User.id == id)).one()


# TODO: roles
@router.post("/")
def insert_user(new_user: UserCreate, session: SessionDep) -> UserOut:

    hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

    user_db = User(
        first_name=new_user.first_name,
        surname=new_user.surname,
        phone=new_user.phone,
        address=new_user.address,
        email=new_user.email,
        password=hashed_password.decode("utf-8"),
    )
    session.add(user_db)
    session.commit()
    print(user_db)
    return user_db


@router.patch("/{id}")
def partial_update_user(
    id: uuid.UUID, new_user: UserPatch, session: SessionDep
) -> UserOut:
    user_db = session.exec(select(User).where(User.id == id)).one()

    if new_user.first_name:
        user_db.first_name = new_user.first_name
    if new_user.surname:
        user_db.surname = new_user.surname
    if new_user.email:
        user_db.email = new_user.email
    if new_user.phone:
        user_db.phone = new_user.phone
    if new_user.address:
        user_db.address = new_user.address
    if new_user.password:
        hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())
        user_db.password = hashed_password.decode("utf-8")

    session.add(user_db)  # TODO: email unique exception
    session.commit()
    return user_db


@router.put("/{id}")
def update_user(id: uuid.UUID, new_user: UserPost, session: SessionDep) -> UserOut:
    user_db = session.exec(select(User).where(User.id == id)).one()

    hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

    user_db.first_name = new_user.first_name
    user_db.surname = new_user.surname
    user_db.email = new_user.email
    user_db.phone = new_user.phone
    user_db.password = hashed_password.decode("utf-8")
    if new_user.address:
        user_db.address = new_user.address

    session.add(user_db)  # TODO: email unique exception
    session.commit()
    return user_db


@router.delete("/{id}")
def delete_user(id: uuid.UUID, session: SessionDep) -> bool:
    user_to_delete = session.exec(select(User).where(User.id == id)).one()
    session.delete(user_to_delete)
    session.commit()
    return True # TODO: meilleur retour
