import os, sys

sys.path.append(os.getcwd())
from app.schemas.schemas import OrderCreate, OrderDetailCreate
from decimal import Decimal 

def test_OrderCreate_init_correct():
    # Act : on instancie avec un user_id et 1 item
    order = OrderCreate(
        user_id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        items=[
            OrderDetailCreate(
                item_id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                quantity=3,
            )
        ],
    )

    # Assert : vérifications très simples
    assert str(order.user_id) == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    assert len(order.items) == 1
    assert str(order.items[0].item_id) == "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    assert order.items[0].quantity == 3