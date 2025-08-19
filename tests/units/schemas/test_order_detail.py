import os, sys

sys.path.append(os.getcwd())
from app.schemas.schemas import OrderDetailCreate

def test_OrderDetailCreate_init_correct():
    # Act: Éxecution de la fonction testée
    detail = OrderDetailCreate(
        item_id="11111111-1111-1111-1111-111111111111",
        quantity=2,
    )

    # Assert : Évaluation de la conformité du résultat
    assert str(detail.item_id) == "11111111-1111-1111-1111-111111111111"
    assert detail.quantity == 2