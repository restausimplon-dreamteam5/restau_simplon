import requests
import os


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
    assert [response[i]["name"] for i in range(40)] == [
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


# def test_create_menu_item():
#     # Act: Exécution de la fonction testée
#     req = requests.post(
#         "http://localhost:8000/menu_items/",
#         data={
#             "name": "Pizza",
#             "price": 16.99,
#             "category": "main course",
#             "description": "Pure happiness",
#             "stock": 10,
#         },
#         auth=('admin@restau-simplon.com', 'admin')
#     )

#     # Assert: Évaluation de la conformité du résultat
#     assert req.status_code == 200
