import os, sys
import pytest

sys.path.append(os.getcwd())
from app.schemas.schemas import MenuItemCreate, MenuItemUpdate
from decimal import Decimal
from pydantic import ValidationError


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


testschemas = [(MenuItemCreate), (MenuItemUpdate)]


@pytest.mark.parametrize(
    "schema", testschemas, ids=["MenuItemCreate", "MenuItemUpdate"]
)
def test_MenuItemCreate_init_correct(correct_menu_item_example: dict, schema):
    # Act: Exécution de la fonction testée
    menu_item = schema(**correct_menu_item_example)

    # Assert: Évaluation de la conformité du résultat
    assert menu_item.name == correct_menu_item_example["name"]
    assert menu_item.price == correct_menu_item_example["price"]
    assert menu_item.category == correct_menu_item_example["category"]
    assert menu_item.description == correct_menu_item_example["description"]
    assert menu_item.stock == correct_menu_item_example["stock"]


@pytest.mark.parametrize(
    "schema", testschemas, ids=["MenuItemCreate", "MenuItemUpdate"]
)
def test_MenuItemCreate_init_too_long_name(correct_menu_item_example: dict, schema):
    # Arrange: État initial de l'environnement du test
    correct_menu_item_example["name"] = (
        "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890extra_characters"
    )

    # Act: Exécution de la fonction testée
    with pytest.raises(ValidationError) as excinfo:
        menu_item = schema(**correct_menu_item_example)

    # Assert: Évaluation de la conformité du résultat
    assert "String should have at most 100 characters" in str(excinfo.value)
