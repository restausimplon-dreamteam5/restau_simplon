import os

import requests


def test_login():
    # Act: Exécution de la route testée
    req = requests.post(
        f"{os.environ["API_URL"]}/login",
        data={
            "grant_type": "password",
            "username": "admin@restau-simplon.com",
            "password": "admin",
            "client_id": "string",
        },
    )

    # Assert: Évaluation de la conformité du résultat
    assert req.status_code == 200
