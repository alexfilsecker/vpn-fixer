from pytimeparse.timeparse import timeparse
import os
from datetime import datetime, timedelta, timezone

def load_creds(creds_path: str) -> tuple[str, str] | None:
    try:
        with open(creds_path, "r") as creds_file:
            lines = creds_file.readlines()
            if len(lines) != 2:
                print(f"Error: {creds_path} should contain exactly 2 lines.")
                return None

            username = lines[0].strip()
            password = lines[1].strip()
            return username, password

    except FileNotFoundError:
        print(f"Error: {creds_path} not found.")
        return None


def check_config(config_path) -> bool:
    try:
        with open(config_path, "r"):
            return True

    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return False


def write_vpn_auth(auth_path: str, credentials: tuple[str, str], code: str) -> None:
    with open(auth_path, "w") as auth_file:
        username, password = credentials
        auth_file.write(f"{username}\n")
        auth_file.write(f"{password}{code}\n")


def clean_old_logs(log_dir: str, keep_time: str):
    seconds = timeparse(keep_time)
    logs = os.listdir(log_dir)
    to_delete = []
    for log in logs:
        time_str = log.split(".")[0]
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        now = datetime.now()
        if dt < now - timedelta(seconds=seconds):
            to_delete.append(log)

    for deleting in to_delete:
        file_path = f"{log_dir}/{deleting}"
        if os.path.exists(file_path):  # Check if file exists
            os.remove(file_path)
            print(f"Deleted {file_path}")

        



        
    

