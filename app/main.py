from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .database import create_db_and_tables
from app.routes import menu_item, user, order, login, roles

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(login.router)
app.include_router(menu_item.router)
app.include_router(user.router)
app.include_router(order.router)
app.include_router(roles.router)
