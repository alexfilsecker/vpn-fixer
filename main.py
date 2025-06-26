import subprocess
import pyotp
import time

from file_utils import load_secret, check_config, check_auth_file, write_vpn_auth, load_creds

OPENVPN_BIN_PATH = "openvpn"
CONFIG_PATH = ".configs/client.ovpn"
SECRET_PATH = ".configs/secret.txt"
AUTH_PATH = ".configs/vpn-auth.txt"
CREDENTIALS_PATH = ".configs/credentials.txt"
LOGS_DIR = "logs"


def loop(secret: str, credentials: tuple[str, str]):
    totp = pyotp.TOTP(secret)
    time_remaining = totp.interval - (int(time.time()) % totp.interval)
    if time_remaining < 3:
        print("Waiting for the next TOTP code...")
        time.sleep(time_remaining + 1)
    
    code = totp.now()
    write_vpn_auth(AUTH_PATH, credentials, code)

    process = subprocess.Popen(
        [OPENVPN_BIN_PATH, "--config", CONFIG_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Combine stdout + stderr
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1  # Line-buffered
    )

    local_now_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    log_path = f"{LOGS_DIR}/{local_now_iso}.log"

    print("\n\n-------- OPENVPN LOGS --------")
    print("Starting OpenVPN process...")
    print(f"Muting logs till connection. Full logs can be found in {log_path}")
    print("Connecting to OpenVPN...")

    print_enable = False
    for line in process.stdout:
        with open(log_path, 'a') as log_file:
            log_file.write(line)
        
        if "Initialization Sequence Completed" in line:
            print("\nOpenVPN connection established successfully.")
            print("Unmuting logs...\n")
            print_enable = True
        
        if print_enable:
            print(line.strip())
    
    process.stdout.close()
    process.wait()
    print("OpenVPN process finished.")
    

def main():
    secret = load_secret(SECRET_PATH)
    if not secret:
        return
    
    credentials = load_creds(CREDENTIALS_PATH)
    if not credentials:
        return
    
    if not check_config(CONFIG_PATH):
        return

    if not check_auth_file(AUTH_PATH):
        return
    
    while True:
        loop(secret, credentials)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted by user.")
 