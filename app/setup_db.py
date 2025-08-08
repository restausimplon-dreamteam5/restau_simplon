import os, sys

sys.path.append(os.getcwd())
import bcrypt
from sqlmodel import Session, select
from app.models.models import Role, User
from database import engine


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
    admin = create_an_admin()
    staff = create_a_staff()
    client = create_a_client()

    with Session(engine) as session:
        session.add(admin)
        session.add(staff)
        session.add(client)
        session.commit()


def create_an_admin() -> User:
    admin_role = Role(role="admin")
    admin_password = "admin"
    admin_salt = bcrypt.gensalt()
    admin_hashed_password = bcrypt.hashpw(admin_password.encode("utf-8"), admin_salt)

    admin = User(
        first_name="michelle",
        surname="admin",
        email="admin@restau-simplon.com",
        password=admin_hashed_password.decode("utf-8"),
        salt=admin_salt.decode("utf-8"),
        phone="0801020304",
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


if __name__ == "__main__":
    create_base_data()
