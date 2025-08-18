import os, sys

sys.path.append(os.getcwd())
from app.schemas.schemas import MenuItemCreate, MenuCategory
from decimal import Decimal


def test_MenuItemCreate_init_correct():
    # Act: Éxecution de la fonction testée
    menu_item = MenuItemCreate(
        name="Tomatoe soup",
        price=Decimal("18.99"),
        category=MenuCategory.starter,
        description="A warm soup made with tomatoes.",
        stock=10,
    )

    # Assert: Évaluation de la conformité du résultat
    assert menu_item.name == "Tomatoe soup"
    assert menu_item.price == Decimal("18.99")
    assert menu_item.category == MenuCategory.starter
    assert menu_item.description == "A warm soup made with tomatoes."
    assert menu_item.stock == 10
