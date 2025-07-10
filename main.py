import subprocess

from src.file_utils import check_config, load_creds, write_vpn_auth
from src.read_qr import read_secret_in_qr
from src.smart_logger import SmartLogger
from src.totp import generate_totp_code

OPENVPN_BIN_PATH = "openvpn"
CONFIG_PATH = ".configs/client.ovpn"
QR_PATH = ".configs/qr.png"
AUTH_PATH = ".configs/.auth"
CREDENTIALS_PATH = ".configs/.creds"
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
        bufsize=1,  # Line-buffered
    )

    for line in process.stdout:
        error = logger.new_line(line)
        if error:
            process.kill()

    process.stdout.close()
    process.wait()
    logger.end(process.returncode)


def main():
    secret = read_secret_in_qr(QR_PATH)
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
