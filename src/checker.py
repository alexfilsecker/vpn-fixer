from threading import Lock

import requests


def health_checker(shared, locky: Lock, health_url: str):
    while True:
        kill = False
        try:
            response = requests.get(health_url)
            if response.status_code != 200:
                kill = True

        except requests.exceptions.ConnectionError:
            kill = True

        with locky:
            shared["kill"] = kill
