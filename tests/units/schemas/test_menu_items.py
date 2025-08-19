import os
import sys
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.schemas import MenuItemCreate, MenuItemOut, MenuItemUpdate

sys.path.append(os.getcwd())


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


@pytest.mark.parametrize(
    "schema",
    [(MenuItemCreate), (MenuItemUpdate), (MenuItemOut)],
    ids=["MenuItemCreate", "MenuItemUpdate", "MenuItemOut"],
)
def test_MenuItemCreate_init_correct(correct_menu_item_example: dict, schema):
    # Arrange: État initial de l'environnement de test
    if schema is MenuItemOut:
        correct_menu_item_example["id"] = "46351949-8598-45c0-9fd5-2b0ec3ac3b3c"

    # Act: Exécution de la fonction testée
    menu_item = schema(**correct_menu_item_example)

    # Assert: Évaluation de la conformité du résultat
    if schema is MenuItemOut:
        assert str(menu_item.id) == correct_menu_item_example["id"]
    assert menu_item.name == correct_menu_item_example["name"]
    assert menu_item.price == correct_menu_item_example["price"]
    assert menu_item.category == correct_menu_item_example["category"]
    assert menu_item.description == correct_menu_item_example["description"]
    assert menu_item.stock == correct_menu_item_example["stock"]


@pytest.mark.parametrize(
    "schema",
    [(MenuItemCreate), (MenuItemUpdate)],
    ids=["MenuItemCreate", "MenuItemUpdate"],
)
def test_MenuItemCreate_init_too_long_name(correct_menu_item_example: dict, schema):
    # Arrange: État initial de l'environnement du test
    correct_menu_item_example["name"] = (
        "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890extra_characters"
    )

    # Act: Exécution de la fonction testée
    with pytest.raises(ValidationError) as excinfo:
        _ = schema(**correct_menu_item_example)

    # Assert: Évaluation de la conformité du résultat
    assert "String should have at most 100 characters" in str(excinfo.value)
