import pytest
from app.schemas.schemas import OrderCreate


# Test fixture pour un ordre valide
@pytest.fixture
def valid_order() -> dict:
    return {
        "user_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "items": [{"item_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", "quantity": 3}],
    }


# Test pour vérifier la création d'une commande avec des données valides
def test_order_create_minimal(valid_order: dict):
    order = OrderCreate(**valid_order)
    assert order.user_id
    assert len(order.items) == 1
    assert order.items[0].quantity == 3
