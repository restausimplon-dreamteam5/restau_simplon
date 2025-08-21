import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

from app.deps import SessionDep
from app.models.models import User
from app.schemas.schemas import Token, TokenData

router = APIRouter(prefix="/login", tags=["Login"])

SECRET_KEY = os.environ["JWT_SECRET"]
ALGORITHM = os.environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

insufficient_permissions_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permissions insuffisantes",
    headers={"WWW-Authenticate": "Bearer"},
)


def extract_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        user_roles = payload.get("roles")
        exp = payload.get("exp")
        if sub is None or user_roles is None or exp is None:
            raise credentials_exception

    except jwt.InvalidTokenError:
        raise credentials_exception
    return TokenData(sub=sub, roles=user_roles, exp=exp)


@router.post("/")
def login(
    logins: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    """Permet à un utilisateur de se connecter.

    Args:
    * logins (OAuth2PasswordRequestForm): username et password dans un format "application/x-www-form-urlencoded"
    * session (SessionDep): (interne) connexion à la base donnée

    Raises:
    * HTTPException: 401 UNAUTHORIZED si username ou password n'ont pas de correspondance

    Returns:
    * Token: Le token JWT et son type. L'id de l'utilisateur ainsi que ses roles sont stocker dans le payload de l'access token
    """
    try:
        user = session.exec(select(User).where(User.email == logins.username)).one()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_salt = user.salt.encode("utf-8")
    hashed_password = bcrypt.hashpw(logins.password.encode("utf-8"), user_salt)
    if hashed_password.decode("utf-8") != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expiration_date = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    user_roles = []
    for role in user.roles:
        user_roles.append(role.role)

    access_token = {"sub": str(user.id), "roles": user_roles, "exp": expiration_date}
    encoded_jwt = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)

    return Token(access_token=encoded_jwt, token_type="bearer")
