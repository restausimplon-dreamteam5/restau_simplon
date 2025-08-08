from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
import bcrypt
from sqlmodel import select
from app.routes.login import extract_token_data, insufficient_permissions_exception
from app.schemas.schemas import TokenData, UserCreate, UserOut, UserPatch, UserPost
from app.models.models import Role, User
from app.deps import SessionDep

router = APIRouter(prefix="/users", tags=["User"])


def find_corresponding_roles(roles: list[str], session: SessionDep):
    res = []
    for role in roles:
        try:
            res.append(session.exec(select(Role).where(Role.role == role)).one())
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role '{role}' n'existe pas",
            )
    return res


@router.get("/")
def get_all_users(
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserOut]:

    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    users = session.exec(select(User).offset(offset).limit(limit))
    return users


@router.get("/{id}")
def get_user_by_id(
    id: uuid.UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    if not token_data.has_role("admin") and not token_data.is_user(id):
        raise insufficient_permissions_exception

    return session.exec(select(User).where(User.id == id)).one()


# TODO: roles
@router.post("/")
def insert_user(
    new_user: UserCreate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    roles_db = find_corresponding_roles(new_user.roles, session)
    # Sécurisation du mot de passe
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_user.password.encode("utf-8"), salt)

    user_db = User(
        first_name=new_user.first_name,
        surname=new_user.surname,
        phone=new_user.phone,
        address=new_user.address,
        email=new_user.email,
        password=hashed_password.decode("utf-8"),
        salt=salt.decode("utf-8"),
        roles=roles_db,
    )
    session.add(user_db)
    session.commit()
    print(user_db)
    return user_db


@router.patch("/{id}")
def partial_update_user(
    id: uuid.UUID,
    new_user: UserPatch,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:

    if not token_data.has_role("admin") and not token_data.is_user(id):
        raise insufficient_permissions_exception

    # Seulement les amdins peuvent modifier les roles
    if new_user.roles and not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    user_db = session.exec(select(User).where(User.id == id)).one()
    user_salt = user_db.salt.encode("utf-8")

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
        # Sécurisation du mot de passe
        hashed_password = bcrypt.hashpw(new_user.password.encode("utf-8"), user_salt)
        user_db.password = hashed_password.decode("utf-8")
    if new_user.roles:
        roles_db = find_corresponding_roles(new_user.roles, session)
        user_db.roles = roles_db

    session.add(user_db)  # TODO: email unique exception
    session.commit()
    return user_db


@router.put("/{id}")
def update_user(
    id: uuid.UUID,
    new_user: UserPost,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    user_db = session.exec(select(User).where(User.id == id)).one()
    # Sécurisation du mot de passe
    user_salt = user_db.salt.encode("utf-8")
    hashed_password = bcrypt.hashpw(new_user.password.encode("utf-8"), user_salt)

    user_db.first_name = new_user.first_name
    user_db.surname = new_user.surname
    user_db.email = new_user.email
    user_db.phone = new_user.phone
    user_db.password = hashed_password.decode("utf-8")
    if new_user.address:
        user_db.address = new_user.address

    roles_db = find_corresponding_roles(new_user.roles, session)
    user_db.roles = roles_db

    session.add(user_db)  # TODO: email unique exception
    session.commit()
    return user_db


@router.delete("/{id}")
def delete_user(
    id: uuid.UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> bool:
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    user_to_delete = session.exec(select(User).where(User.id == id)).one()
    session.delete(user_to_delete)
    session.commit()
    return True  # TODO: meilleur retour
