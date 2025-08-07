import os, sys

sys.path.append(os.getcwd())
from app.models.models import MenuItem
from app.schemas.schemas import MenuItemCreate
from app.crud.menu_items import create_menu_item_in_db
from sqlmodel import create_engine, select, SQLModel, Session
import json

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def db_init():
    """Ajoute du contenu aléatoire dans la base de données pour les tests.

    **Attention**: la base de données doit être à jour des migrations alembiques"""

    # Récupération des données générées par chatGPT
    with open("app/menu_items.json", "r") as file:
        menu_items = json.load(file)

    with Session(engine) as session:
        # Nettoyage complet de la table menu_items
        all_menu_items = session.exec(select(MenuItem)).all()
        for menu_item in all_menu_items:
            session.delete(menu_item)
        session.commit()

        # Mise en base des informations de menu_items.json
        for menu_item in menu_items:
            menu_item_create = MenuItemCreate(**menu_item)
            menu_item_db = MenuItem(**menu_item_create.model_dump())
            if create_menu_item_in_db(session, menu_item_db):
                print(f"Added: {menu_item_db.name} in category {menu_item_db.category}")


if __name__ == "__main__":
    db_init()
