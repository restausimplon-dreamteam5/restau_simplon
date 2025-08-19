"""
Test d’intégration de la route /orders.

Étapes :
1) Authentification via /login (form username/password) -> on récupère un token.
2) On extrait l'identifiant utilisateur (user_id) depuis le token.
3) On lit la liste des menu items et on prend le premier id.
4) On crée une commande avec POST /orders et on vérifie la réponse.
"""

import os
import json
import base64
import requests


# Configuration variables
BASE_URL       = f"http://localhost:{os.getenv('LOCAL_API_PORT', '8000')}"
ADMIN_EMAIL    = os.getenv("ADMIN_EMAIL", "admin@restau-simplon.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")

LOGIN_PATH     = "/login"
MENU_LIST_PATH = "/menu_items"
ORDERS_PATH    = "/orders"


def login_and_get_bearer() -> str:
    """
    Appelle POST /login avec un formulaire (username/password)
    et renvoie l'en-tête Authorization au format 'Bearer <token>'.
    """
    resp = requests.post(
        f"{BASE_URL}{LOGIN_PATH}",
        data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        timeout=10,
    )
    assert resp.status_code in (200, 201), f"Login échoué: {resp.status_code} -> {resp.text}"
    data = resp.json()
    token = data.get("access_token") or data.get("token")
    assert token, f"Le login n'a pas renvoyé de token: {data}"
    return f"Bearer {token}"


def extract_user_id_from_token(bearer: str) -> str:
    """
    Récupère l'identifiant utilisateur (champ 'sub') contenu dans le token.
    Le token est au format JWT : header.payload.signature (base64url).
    """
    token = bearer.split()[1]            # 'Bearer <token>'
    payload_part = token.split(".")[1]   # on prend la partie payload
    payload_part += "=" * (-len(payload_part) % 4)  # padding base64
    payload = json.loads(base64.urlsafe_b64decode(payload_part).decode())
    user_id = payload.get("sub")
    assert user_id, f"Impossible de trouver 'sub' (user_id) dans le token: {payload}"
    return str(user_id)


def get_first_menu_item_id() -> str:
    """
    Retourne l'id du premier menu item disponible (GET /menu_items).
    """
    resp = requests.get(f"{BASE_URL}{MENU_LIST_PATH}", timeout=10)
    assert resp.status_code == 200, f"Echec GET /menu_items: {resp.status_code} -> {resp.text}"
    items = resp.json()
    assert isinstance(items, list) and items, "Aucun menu item disponible pour le test."
    return str(items[0]["id"])


def test_create_order_basic():
    """
    Test : création d'une commande minimale avec un seul article.
    Vérifie un statut 200/201 et la présence d'un id de commande.
    """
    # 1) Authentification
    bearer = login_and_get_bearer()
    headers = {"Authorization": bearer}

    # 2) Extraction du user_id depuis le token
    user_id = extract_user_id_from_token(bearer)

    # 3) Récupération d'un item existant
    item_id = get_first_menu_item_id()

    # 4) Création de la commande
    payload = {
        "user_id": user_id,
        "items": [{"item_id": item_id, "quantity": 1}],
    }
    resp = requests.post(f"{BASE_URL}{ORDERS_PATH}", json=payload, headers=headers, timeout=15)
    if resp.status_code == 404:  # au cas où la route exige un slash final
        resp = requests.post(f"{BASE_URL}{ORDERS_PATH}/", json=payload, headers=headers, timeout=15)

    # 5) Asserts 
    assert resp.status_code in (200, 201), f"Echec POST /orders: {resp.status_code} -> {resp.text}"
    data = resp.json()
    assert isinstance(data, dict) and "id" in data, f"Réponse inattendue: {data}"
    if "user_id" in data:
        assert str(data["user_id"]) == user_id






