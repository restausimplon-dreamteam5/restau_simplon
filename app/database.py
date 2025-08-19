import os
import sys

sys.path.append(os.getcwd())
import json
import random

import bcrypt
import dotenv
from sqlmodel import Session, SQLModel, create_engine, select

from app.crud.menu_items import create_menu_item_in_db
from app.crud.order import create_order_detail_in_db, create_order_in_db
from app.crud.user_info import create_user_info_in_db
from app.models.models import MenuItem, Order, OrderDetail, OrderStatus, Role, User
from app.schemas.schemas import MenuItemCreate, UserCreate

dotenv.load_dotenv()
DB_URI = os.getenv("DB_URI")
if DB_URI == None:
    print("DB_URI manquante")
    sys.exit()

engine = create_engine(DB_URI, echo=True)


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

    # Nettoyage complet de la table user_info
    with Session(engine) as session:
        all_users_info = session.exec(select(User)).all()
        for user_info in all_users_info:
            session.delete(user_info)
        session.commit()

    # Mise en base des comptes de contrôles
    create_base_data()

    # Récupération des données générées par chatGPT
    with open("app/users_info.json", "r") as file:
        users_info = json.load(file)

    with Session(engine) as session:
        # Mise en base des informations de users_info.json
        for user_info in users_info:
            user_salt = bcrypt.gensalt()
            user_hashed_password = bcrypt.hashpw(
                user_info["password"].encode("utf-8"), user_salt
            )
            user_info["password"] = user_hashed_password.decode("utf-8")
            user_info_create = UserCreate(**user_info)

            admin_role = session.exec(select(Role).where(Role.role == "admin")).first()
            staff_role = session.exec(select(Role).where(Role.role == "staff")).first()
            client_role = session.exec(
                select(Role).where(Role.role == "client")
            ).first()

            user_info_create_roles = []
            for user_role in user_info_create.roles:
                if user_role == "admin":
                    user_info_create_roles.append(admin_role)
                elif user_role == "staff":
                    user_info_create_roles.append(staff_role)
                elif user_role == "client":
                    user_info_create_roles.append(client_role)

            user_info_db = User(
                first_name=user_info_create.first_name,
                surname=user_info_create.surname,
                email=user_info_create.email,
                password=user_info_create.password,
                phone=user_info_create.phone,
                address=user_info_create.address,
                roles=user_info_create_roles,
                salt=user_salt.decode("utf-8"),
            )
            if create_user_info_in_db(session, user_info_db):
                print(f"Added: {user_info_db.first_name} {user_info_db.surname}")


def create_base_data():
    with Session(engine) as session:
        # Nettoyage complet de la table role
        all_roles = session.exec(select(Role)).all()
        for role in all_roles:
            session.delete(role)
        session.commit()

        admin_db = session.exec(select(User).where(User.surname == "admin")).first()
        if admin_db:
            session.delete(admin_db)
        staff_db = session.exec(select(User).where(User.surname == "staff")).first()
        if staff_db:
            session.delete(staff_db)
        client_db = session.exec(select(User).where(User.surname == "client")).first()
        if client_db:
            session.delete(client_db)
        session.commit()

    # # Création des nouveaux user
    admin = create_default_admin()
    staff = create_a_staff()
    client = create_a_client()

    with Session(engine) as session:
        session.add(admin)
        session.add(staff)
        session.add(client)
        session.commit()


def create_default_admin() -> User:
    admin_role = Role(role="admin")
    admin_password = os.environ["ADMIN_PASSWORD"]
    admin_salt = bcrypt.gensalt()
    admin_hashed_password = bcrypt.hashpw(admin_password.encode("utf-8"), admin_salt)

    admin = User(
        first_name="to_modify",
        surname="to_modify",
        email=os.environ["ADMIN_EMAIL"],
        password=admin_hashed_password.decode("utf-8"),
        salt=admin_salt.decode("utf-8"),
        phone="0600000000",
        address=None,
        roles=[admin_role],
    )
    return admin


def create_a_staff() -> User:
    staff_role = Role(role="staff")
    staff_password = "staff"
    staff_salt = bcrypt.gensalt()
    staff_hashed_password = bcrypt.hashpw(staff_password.encode("utf-8"), staff_salt)

    staff = User(
        first_name="henri",
        surname="staff",
        email="staff@restau-simplon.com",
        password=staff_hashed_password.decode("utf-8"),
        salt=staff_salt.decode("utf-8"),
        phone="0701020304",
        address=None,
        roles=[staff_role],
    )
    return staff


def create_a_client() -> User:
    client_role = Role(role="client")
    client_password = "client"
    client_salt = bcrypt.gensalt()
    client_hashed_password = bcrypt.hashpw(client_password.encode("utf-8"), client_salt)

    client = User(
        first_name="Jean-Phi",
        surname="client",
        email="client@restau-simplon.com",
        password=client_hashed_password.decode("utf-8"),
        salt=client_salt.decode("utf-8"),
        phone="0601020304",
        address=None,
        roles=[client_role],
    )
    return client


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

            details = []
            for _ in range(random.randint(1, 10)):
                menu_item = random.choice(all_menu_items)
                order_detail_db = OrderDetail(
                    item_id=menu_item.id,
                    quantity=random.randint(1, 2),
                    unit_price=menu_item.price,
                )
                details.append(order_detail_db)

            order_db = Order(
                user_id=user_id,
                status=random.choice([status for status in OrderStatus]),
                details=details,
            )

            if create_order_in_db(session, order_db):
                print(f"Added: Commande {order_db.id}")


if __name__ == "__main__":
    db_init()
