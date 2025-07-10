def load_creds(creds_path: str) -> tuple[str, str] | None:
    try:
        with open(creds_path, 'r') as creds_file:
            lines = creds_file.readlines()
            if len(lines) != 2:
                print(f"Error: {creds_path} should contain exactly 2 lines (username and password).")
                return None

            username = lines[0].strip()
            password = lines[1].strip()
            return username, password

    except FileNotFoundError:
        print(f"Error: {creds_path} not found.")
        return None


def check_config(config_path) -> bool:
    try:
        with open(config_path, 'r'):
            return True

    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return False



def write_vpn_auth(auth_path: str, credentials: tuple[str, str], code: str) -> None:
    with open(auth_path, 'w') as auth_file:
        username, password = credentials
        auth_file.write(f"{username}\n")
        auth_file.write(f"{password}{code}\n")
