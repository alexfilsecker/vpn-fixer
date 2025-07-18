import time
from threading import Lock

import requests


def health_checker(shared, locky: Lock, health_url: str):
    time.sleep(3)
    while True:
        kill = False
        try:
            response = requests.get(health_url)
            if response.status_code != 200:
                print(health_url, "responded with status code", response.status_code)
                kill = True

        except requests.exceptions.ConnectionError as e:
            print("CONNECTION ERROR")
            print(e)
            kill = True

        with locky:
            shared["kill"] = kill
