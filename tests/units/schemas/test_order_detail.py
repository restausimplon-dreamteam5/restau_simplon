import pytest
from pydantic import ValidationError
from app.schemas.schemas import OrderDetailCreate


# Test fixture pour un détail de commande valide
@pytest.fixture
def valid_order_detail() -> dict:
    return {
        "item_id": "11111111-1111-1111-1111-111111111111",
        "quantity": 2,
    }


def test_OrderDetailCreate_init_correct(valid_order_detail: dict):
    # Act
    detail = OrderDetailCreate(**valid_order_detail)

    # Assert
    assert str(detail.item_id) == valid_order_detail["item_id"]
    assert detail.quantity == valid_order_detail["quantity"]


def test_OrderDetailCreate_rejects_quantity_lt_1(valid_order_detail: dict):
    # Arrange
    valid_order_detail["quantity"] = 0

    # Act + Assert
    with pytest.raises(ValidationError):
        _ = OrderDetailCreate(**valid_order_detail)