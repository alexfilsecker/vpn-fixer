import subprocess
import pyotp
import time

from file_utils import load_secret, check_config, write_vpn_auth, load_creds
from smart_logger import SmartLogger
from totp import generate_totp_code

OPENVPN_BIN_PATH = "openvpn"
CONFIG_PATH = ".configs/client.ovpn"
SECRET_PATH = ".configs/secret.txt"
AUTH_PATH = ".configs/vpn-auth.txt"
CREDENTIALS_PATH = ".configs/credentials.txt"
LOGS_DIR = "logs"



def loop(secret: str, credentials: tuple[str, str]):
    logger = SmartLogger(LOGS_DIR)
    code = generate_totp_code(secret, logger)
    write_vpn_auth(AUTH_PATH, credentials, code)

    process = subprocess.Popen(
        [OPENVPN_BIN_PATH, "--config", CONFIG_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Combine stdout + stderr
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1  # Line-buffered
    )

    for line in process.stdout:
        logger.new_line(line)

    process.stdout.close()
    process.wait()
    logger.end(process.returncode)
    

def main():
    secret = load_secret(SECRET_PATH)
    if not secret:
        return
    
    credentials = load_creds(CREDENTIALS_PATH)
    if not credentials:
        return
    
    if not check_config(CONFIG_PATH):
        return
    
    while True:
        loop(secret, credentials)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted by user.")
 