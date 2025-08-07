import os, sys

sys.path.append(os.getcwd())

from sqlmodel import Session
from app.models.models import Role, User
from database import engine

def create_base_data():
    admin_role = Role(role="admin")
    staff_role = Role(role="staff")
    client_role = Role(role="client")
    
    admin = User(
        first_name="michelle",
        surname="admin",
        email="admin@restau-simplon.com",
        password="admin", #TODO: salé et hashé le mdp
        phone="0801020304",
        roles= [admin_role]
    )
    
    with Session(engine) as session:
        session.add(staff_role)
        session.add(client_role)
        session.add(admin)
        session.commit()
        
if __name__ == "__main__":
    create_base_data()