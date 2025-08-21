import dotenv
from fastapi import FastAPI

from app.routes import login, menu_item, order, roles, user

dotenv.load_dotenv()

# TODO: vérifier la présence de toutes les clés

app = FastAPI()

app.include_router(login.router)
app.include_router(menu_item.router)
app.include_router(user.router)
app.include_router(order.router)
app.include_router(roles.router)
