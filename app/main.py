from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.schemas.schemas import MenuItemCreate, MenuItemOut
from app.models.models import MenuItem
from .database import engine
from .deps import SessionDep
from app.routes import menu_item


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(menu_item.router)