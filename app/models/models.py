# Import
import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


# User
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    phone: str
    address: str | None
    email: str = Field(index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)


# Article


# Order