from fastapi import FastAPI
from .database import create_db_and_tables
from app.routes import menu_item

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(menu_item.router)