import os, sys
import pytest

sys.path.append(os.getcwd())
from app.schemas.schemas import MenuItemCreate, MenuCategory
from decimal import Decimal


# Définition d'un article de menu correct et complet
@pytest.fixture
def correct_menu_item_example() -> dict:
    """Retourne un article de menu type sous forme de dictionnaire.

    Returns:
        dict: Les données d'un article de menu type
    """
    return {
        "name": "Tomatoe soup",
        "price": Decimal("18.99"),
        "category": "starter",
        "description": "A warm soup made with tomatoes.",
        "stock": 10,
    }


def test_MenuItemCreate_init_correct(correct_menu_item_example):
    # Act: Éxecution de la fonction testée
    menu_item = MenuItemCreate(**correct_menu_item_example)

    # Assert: Évaluation de la conformité du résultat
    assert menu_item.name == correct_menu_item_example["name"]
    assert menu_item.price == correct_menu_item_example["price"]
    assert menu_item.category == correct_menu_item_example["category"]
    assert menu_item.description == correct_menu_item_example["description"]
    assert menu_item.stock == correct_menu_item_example["stock"]