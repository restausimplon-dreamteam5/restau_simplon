import uuid
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.deps import SessionDep
from app.models.models import Role, User
from app.routes.login import extract_token_data, insufficient_permissions_exception
from app.schemas.schemas import (
    ClientCreate,
    TokenData,
    UserCreate,
    UserOut,
    UserPatch,
    UserPost,
)

router = APIRouter(prefix="/users", tags=["User"])


def find_corresponding_roles(roles: list[str], session: SessionDep) -> list[Role]:
    """Renvoie les entrés en base de données des roles passé en paramètres.

    Args:
    * roles (list[str]): list des roles (ex: ["admin", "staff"])
    * session (SessionDep): connexion à la base de données

    Raises:
    * HTTPException: si le role n'existe pas

    Returns:
    * list[Role]: les roles de la base de données
    """
    res = []
    for role in roles:
        try:
            res.append(session.exec(select(Role).where(Role.role == role)).one())
        except Exception:
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
    """Renvoie tous les utilisateurs selon la pagination.

    Args:
    * token_data (TokenData): Le token de l'utilisateur effectuant la requête.
    * offset (int, optional): L'offest pour la pagination. Par défaut 0.
    * limit (int, optional): Le nombre d'utilisateur maximal retourné. Ne peut pas être supérieur à 100.   Par défaut 100.
    * session (SessionDep): (interne) connexion à la base de données.

    Raises:
    * HTTPException: 403 si l'utilisateur n'a pas les permissions nécessaires

    Returns:
    * list[UserOut]: liste des utilisateurs
    """
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    users = session.exec(select(User).offset(offset).limit(limit)).all()

    users_out = [UserOut(**user.model_dump(), roles=user.roles) for user in users]
    return users_out


@router.get("/{id}")
def get_user_by_id(
    id: uuid.UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    """Renvoie l'utilisateur correspondant à l'id.

    Args:
    * id (uuid.UUID): l'id de l'utilisateur recherché
    * session (SessionDep): (interne) connexion à la base de données
    * token_data (TokenData): le token de l'utilisateur effectuant la requête

    Raises:
    * HTTPException: 403 si l'utilisateur n'a pas les permissions nécessaires. L'utilisateur doit être admin ou l'utilisateur concerné.
    * HTTPException: 404 si l'id n'a pas de correspondance.

    Returns:
    * UserOut: L'utilisateur concerné.
    """
    if not token_data.has_role("admin") and not token_data.is_user(id):
        raise insufficient_permissions_exception

    try:
        user_db = session.exec(select(User).where(User.id == id)).one()
        return UserOut(**user_db.model_dump(), roles=user_db.roles)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def insert_user(new_user: UserCreate, session: SessionDep) -> UserOut:
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

    try:
        session.add(user_db)
        # practice: gestion des doublons/unicité, erreur 500 ??? ou 400
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return UserOut(**user_db.model_dump(), roles=user_db.roles)


@router.post("/")
def new_user(
    new_user: UserCreate,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    """Créer un nouvel utilisateur

    Args:
    * new_user (UserCreate): l'utilisateur à créer
    * session (SessionDep): (interne) connexion à la base de données
    * token_data (TokenData): le token de l'utilisateur effectuant la requête

    Raises:
    * HTTPException: 403 si l'utilisateur n'a pas les permissions nécessaires. L'utilisateur doit être admin.

    Returns:
    * UserOut: L'utilisateur qui vient d'être créé.
    """
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception
    return insert_user(new_user, session)


@router.post("/client")
def new_client_account(new_client: ClientCreate, session: SessionDep) -> UserOut:
    """Créer un nouveau compte client.

    Args:
    * new_client (ClientCreate): Le nouveau client.
    * session (SessionDep): (interne) connexion à la base de données.

    Returns:
    * UserOut: L'utilisateur qui vient d'être créé.
    """
    new_user = UserCreate(**new_client.model_dump(), roles=["client"])
    return insert_user(new_user, session)


@router.patch("/{id}")
def partial_update_user(
    id: uuid.UUID,
    new_user: UserPatch,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    """Mets à jour certains champs d'un utilsateur.

    Args:
    * id (uuid.UUID): Id de l'utilisateur concerné.
    * new_user (UserPatch): Les champs utilisateur à modifier.
    * session (SessionDep): (interne) connexion à la base de données.
    * token_data (TokenData): le token de l'utilisateur effectuant la requête.

    Raises:
    * HTTPException: 403 si l'utilisateur n'a pas les permissions nécessaires. L'utilisateur doit être admin ou être l'utilisateur concerné. Un utilisateur non admin ne peut pas modifier ses rôles.
    * HTTPException: 404 si l'id n'a pas de correspondance.

    Returns:
        UserOut: L'utilisateur mis à jour
    """

    if not token_data.has_role("admin") and not token_data.is_user(id):
        raise insufficient_permissions_exception

    # Seulement les amdins peuvent modifier les roles
    if new_user.roles and not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    user_db = None
    try:
        user_db = session.exec(select(User).where(User.id == id)).one()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

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

    try:
        session.add(user_db)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return UserOut(**user_db.model_dump(), roles=user_db.roles)


@router.put("/{id}")
def update_user(
    id: uuid.UUID,
    new_user: UserPost,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> UserOut:
    """Écrase un utilisateur

    Args:
    * id (uuid.UUID): Id de l'utilisateur concerné.
    * new_user (UserPost): Le nouvel utilisateur
    * session (SessionDep): (interne) connexion à la base de données.
    * token_data (TokenData): le token de l'utilisateur effectuant la requête.

    Raises:
    * HTTPException: 403 si l'utilisateur n'a pas les permissions nécessaires. L'utilisateur doit être admin.
    * HTTPException: 404 si l'id n'a pas de correspondance.

    Returns:
    * UserOut: L'utilisateur mis à jour
    """
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    user_db = None
    try:
        user_db = session.exec(select(User).where(User.id == id)).one()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

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

    try:
        session.add(user_db)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return UserOut(**user_db.model_dump(), roles=user_db.roles)


@router.delete("/{id}")
def delete_user(
    id: uuid.UUID,
    session: SessionDep,
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> bool:
    """Supprime un utilisateur

    Args:
    * id (uuid.UUID): Id de l'utilisateur concerné.
    * session (SessionDep): (interne) connexion à la base de données.
    * token_data (TokenData): le token de l'utilisateur effectuant la requête.

    Raises:
    * HTTPException: 403 si l'utilisateur n'a pas les permissions nécessaires. L'utilisateur doit être admin.
    * HTTPException: 404 si l'id n'a pas de correspondance.

    Returns:
    * bool: True si l'utilisateur à été supprimer avec succès
    """
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception

    try:
        user_to_delete = session.exec(select(User).where(User.id == id)).one()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(user_to_delete)
    session.commit()
    return True  # TODO: meilleur retour
