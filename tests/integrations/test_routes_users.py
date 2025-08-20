import os
import urllib.request


def test_site_available():
    print(os.environ["API_URL"])
    status_code = urllib.request.urlopen(f"{os.environ["API_URL"]}/docs").getcode()
    assert status_code == 200


def test_qui_echoue():
    assert 1 == 2
