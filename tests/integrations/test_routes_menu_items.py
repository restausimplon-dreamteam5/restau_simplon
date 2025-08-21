import os

import pytest
import requests


# Récupếration du token
@pytest.fixture
def admin_access_token() -> str:
    """Retourne le token associé à l'admin

    Returns:
        str: le token
    """
    req = requests.post(
        f"{os.environ["API_URL"]}/login",
        data={
            "grant_type": "password",
            "username": "admin@restau-simplon.com",
            "password": "admin",
            "client_id": "string",
        },
    )
    response = req.json()
    return response["access_token"]


def test_read_menu_item_by_name():
    # Act: Exécution de la route testée
    req = requests.get(f"{os.environ["API_URL"]}/menu_items/name/Bruschetta")

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46


def test_read_menu_category():
    # Act: Exécution de la fonction testée
    req = requests.get(f"{os.environ["API_URL"]}/menu_items/category/starter")

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert len(response) == 40
    for i in range(40):
        assert response[i]["name"] in [
            "Bruschetta",
            "Caesar Salad",
            "French Onion Soup",
            "Spring Rolls",
            "Garlic Bread",
            "Caprese Salad",
            "Stuffed Mushrooms",
            "Deviled Eggs",
            "Mini Quiches",
            "Shrimp Cocktail",
            "Spring Rolls 2",
            "Deviled Eggs 2",
            "Caprese Salad 2",
            "Caesar Salad 2",
            "Deviled Eggs 3",
            "Bruschetta 2",
            "Mini Quiches 2",
            "Caesar Salad 3",
            "Mini Quiches 3",
            "Spring Rolls 3",
            "French Onion Soup 2",
            "French Onion Soup 3",
            "Spring Rolls 4",
            "Spring Rolls 5",
            "Caesar Salad 4",
            "Bruschetta 3",
            "Stuffed Mushrooms 2",
            "Spring Rolls 6",
            "Bruschetta 4",
            "Caprese Salad 3",
            "Caesar Salad 5",
            "Deviled Eggs 4",
            "Garlic Bread 2",
            "French Onion Soup 4",
            "Stuffed Mushrooms 3",
            "Shrimp Cocktail 2",
            "Spring Rolls 7",
            "French Onion Soup 5",
            "Caprese Salad 4",
            "Stuffed Mushrooms 4",
        ]


def test_read_menu_items():
    # Act: Exécution de la route testée
    req = requests.get(f"{os.environ["API_URL"]}/menu_items")

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert len(response) == 100


def test_create_delete_menu_item(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.post(
        f"{os.environ["API_URL"]}/menu_items/",
        json={
            "name": "Pizza",
            "price": 16.99,
            "category": "main course",
            "description": "Good !",
            "stock": 10,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Pizza"
    assert response["price"] == "16.99"
    assert response["category"] == "main course"
    assert response["description"] == "Good !"
    assert response["stock"] == 10

    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
    }

    # Act: Exécution de la fonction delete
    req = requests.delete(
        f"{os.environ["API_URL"]}/menu_items/name/Pizza",
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200
    response = req.json()
    assert response is True


def test_partial_update_menu_item_by_name_1(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "price": 100.00,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "100.00"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46

    # Reverse
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "price": 7.23,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46


def test_partial_update_menu_item_by_name_2(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "category": "main course",
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "main course"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46

    # Reverse
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "category": "starter",
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46


def test_partial_update_menu_item_by_name_3(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "description": "Good !",
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Good !"
    assert response["stock"] == 46

    # Reverse
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "description": "Toasted bread with tomato and basil",
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46


def test_partial_update_menu_item_by_name_4(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "stock": 100,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 100

    # Reverse
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "stock": 46,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46


def test_partial_update_menu_item_by_name_5(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "name": "Tartine",
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Tartine"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46

    # Reverse
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Tartine",
        json={
            "name": "Bruschetta",
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46


def test_update_menu_item_by_name(admin_access_token: str):
    # Arrange: préparation du header pour la requête
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + admin_access_token,
        "Content-Type": "application/json",
    }

    # Act: Exécution de la fonction create
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Bruschetta",
        json={
            "name": "Tartine",
            "price": 100.00,
            "category": "main course",
            "description": "Good !",
            "stock": 100,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Tartine"
    assert response["price"] == "100.00"
    assert response["category"] == "main course"
    assert response["description"] == "Good !"
    assert response["stock"] == 100

    # Reverse
    req = requests.patch(
        f"{os.environ["API_URL"]}/menu_items/name/Tartine",
        json={
            "name": "Bruschetta",
            "price": "7.23",
            "category": "starter",
            "description": "Toasted bread with tomato and basil",
            "stock": 46,
        },
        headers=headers,
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200

    response = req.json()
    assert response["name"] == "Bruschetta"
    assert response["price"] == "7.23"
    assert response["category"] == "starter"
    assert response["description"] == "Toasted bread with tomato and basil"
    assert response["stock"] == 46
