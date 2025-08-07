import os, sys

sys.path.append(os.getcwd())
from app.models.models import MenuItem, User, Order, OrderDetail, OrderStatus
from app.schemas.schemas import (
    MenuItemCreate,
    UserCreate
)
from app.crud.menu_items import create_menu_item_in_db
from app.crud.user_info import create_user_info_in_db
from app.crud.order import create_order_detail_in_db, create_order_in_db
from sqlmodel import create_engine, select, SQLModel, Session
import json
import random

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def db_init():
    """Ajoute du contenu aléatoire dans la base de données pour les tests.

    **Attention**: la base de données doit être à jour des migrations alembiques"""
    db_init_menu_item()
    db_init_user_info()
    db_init_order()


def db_init_menu_item():
    """Population de la table menu_item"""

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


def db_init_user_info():
    """Population de la table user_info"""

    # Récupération des données générées par chatGPT
    with open("app/users_info.json", "r") as file:
        users_info = json.load(file)

    with Session(engine) as session:
        # Nettoyage complet de la table menu_user_info
        all_users_info = session.exec(select(User)).all()
        for user_info in all_users_info:
            session.delete(user_info)
        session.commit()

        # Mise en base des informations de users_info.json
        for user_info in users_info:
            user_info_create = UserCreate(**user_info)
            user_info_db = User(**user_info_create.model_dump())
            if create_user_info_in_db(session, user_info_db):
                print(f"Added: {user_info_db.first_name} {user_info_db.surname}")


def db_init_order():
    """Population de la table order et order_detail"""

    with Session(engine) as session:
        # Nettoyage complet de la table menu_user_info
        all_orders = session.exec(select(Order)).all()
        for order in all_orders:
            session.delete(order)
        all_order_details = session.exec(select(OrderDetail)).all()
        for order_detail in all_order_details:
            session.delete(order_detail)
        session.commit()

        # Récupération de tous les utilisateurs et tous les articles de menu
        all_users_info = session.exec(select(User)).all()
        all_menu_items = session.exec(select(MenuItem)).all()

        for _ in range(30):
            user_id = random.choice(all_users_info).id

            order_db = Order(
                user_id=user_id,
                status=random.choice([status for status in OrderStatus]),
            )
            if create_order_in_db(session, order_db):
                print(f"Added: Commande {order_db.id}")
                order_id = order_db.id

                for _ in range(random.randint(1, 10)):
                    menu_item = random.choice(all_menu_items)
                    order_detail_db = OrderDetail(
                        order_id=order_id,
                        item_id=menu_item.id,
                        quantity=random.randint(1, 2),
                        unit_price=menu_item.price,
                    )
                    if create_order_detail_in_db(session, order_detail_db):
                        print(f"Complèment de commande pour {order_detail_db.item_id}")


if __name__ == "__main__":
    db_init()
