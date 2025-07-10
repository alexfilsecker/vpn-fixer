import time

import pyotp

from .smart_logger import SmartLogger


def generate_totp_code(secret, logger: SmartLogger) -> str:
    totp = pyotp.TOTP(secret)
    time_remaining = totp.interval - (int(time.time()) % totp.interval)
    if time_remaining < 3:
        logger.waiting()
        time.sleep(time_remaining + 1)

    return totp.now()

