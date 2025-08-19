import pytest

from app.schemas.schemas import UserCreate


@pytest.fixture
def valid_UserCreate():
    return {
        "first_name": "Jeremy",
        "surname": "Michel",
        "phone": "0102030405",
        "address": "46 rue des michels 44000 Nantes",
        "email": "jeremy.michel@nantes.com",
        "password": "$2b$12$eJ/wRnWJb0URoOFkllBD1eKGD.SMTy.Vo57XTyJzTP2mkig8MvoEW",  # admin hash
        "roles": ["admin"],
    }


def test_UserCreate_firstname_should_not_exceed_50_characters(valid_UserCreate):

    valid_UserCreate["first_name"] = "a" * 51
    with pytest.raises(ValueError):
        _ = UserCreate(**valid_UserCreate)

    valid_UserCreate["first_name"] = "a" * 50
    user = UserCreate(**valid_UserCreate)
    assert user.first_name == "a" * 50
