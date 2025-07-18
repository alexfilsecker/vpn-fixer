import json


class Paths:
    def __init__(self):
        with open("paths.json", "r") as f:
            obj = json.load(f)

        self.OPENVPN_BIN_PATH = obj["OPENVPN_BIN_PATH"]
        self.CONFIG_PATH = obj["CONFIG_PATH"]
        self.QR_PATH = obj["QR_PATH"]
        self.AUTH_PATH = obj["AUTH_PATH"]
        self.CREDENTIALS_PATH = obj["CREDENTIALS_PATH"]
        self.LOGS_DIR = obj["LOGS_DIR"]
        self.HEALTH_URL = obj["HEALTH_URL"]
