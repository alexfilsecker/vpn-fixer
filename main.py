import subprocess
from threading import Lock, Thread

from src.checker import health_checker
from src.file_utils import check_config, load_creds, write_vpn_auth
from src.paths import Paths
from src.read_qr import read_secret_in_qr
from src.smart_logger import SmartLogger
from src.totp import generate_totp_code


def loop(secret: str, credentials: tuple[str, str], p: Paths):
    logger = SmartLogger(p.LOGS_DIR)
    code = generate_totp_code(secret, logger)
    write_vpn_auth(p.AUTH_PATH, credentials, code)

    process = subprocess.Popen(
        [p.OPENVPN_BIN_PATH, "--config", p.CONFIG_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Combine stdout + stderr
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line-buffered
    )

    shared = {"kill": False}
    locky = Lock()
    thread = Thread(
        target=health_checker, args=(shared, locky, p.HEALTH_URL), daemon=True
    )

    for line in process.stdout:
        with locky:
            if shared["kill"]:
                logger.killed()
                process.kill()
                break

        control = logger.new_line(line)
        if control is None:
            continue

        if control == "error":
            process.kill()
            break

        if control == "started":
            thread.start()

    process.stdout.close()
    process.wait()
    logger.end(process.returncode)


def main():
    p = Paths()
    secret = read_secret_in_qr(p.QR_PATH)
    if not secret:
        return

    credentials = load_creds(p.CREDENTIALS_PATH)
    if not credentials:
        return

    if not check_config(p.CONFIG_PATH):
        return

    while True:
        loop(secret, credentials, p)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
