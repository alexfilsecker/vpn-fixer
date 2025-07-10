from urllib.parse import parse_qs, urlparse

from PIL import Image
from pyzbar.pyzbar import decode


def read_secret_in_qr(qr_path: str) -> str | None:
    try:
        image = Image.open(qr_path)
    except FileNotFoundError:
        print(f"QR not found in {qr_path}")
        return None
    decoded_objects = decode(image)

    if len(decoded_objects) != 1:
        print("Probably not the correct qr")
        return None

    obj = decoded_objects[0]
    if obj.type != "QRCODE":
        print("Not a qr code (?)")
        return None

    url = obj.data.decode("utf-8")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    try:
        secret = query_params["secret"][0]
    except KeyError:
        print("Your qr does not contain a secret")
        return None

    return secret


if __name__ == "__main__":
    secret = read_secret_in_qr(".configs/qr.png")
    print(secret)
