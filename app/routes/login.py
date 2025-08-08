from datetime import datetime, timedelta, timezone
from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.deps import SessionDep
from app.models.models import User
from app.schemas.schemas import Token, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import bcrypt

router = APIRouter(prefix="/login", tags=["Login"])

# to get a string like this run:
# openssl rand -hex 32
# TODO: gen 1 and put in env
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

        # TODO: vérifier que le token ne soit pas expirer
    except jwt.InvalidTokenError:
        raise credentials_exception
    return TokenData(sub=sub, roles=user_roles, exp=exp)


@router.get("/test")
def get_token_data(
    token_data: Annotated[TokenData, Depends(extract_token_data)],
) -> TokenData:
    if not token_data.has_role("admin"):
        raise insufficient_permissions_exception
    return token_data


@router.post("/")
def login(
    logins: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:

    try:
        user = session.exec(select(User).where(User.email == logins.username)).one()
    except:
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
