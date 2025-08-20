import os
import urllib.request


def test_site_available():
    status_code = urllib.request.urlopen(os.environ["API_URL"]).getcode()
    assert status_code == 200
