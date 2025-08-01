import time
from typing import Callable, Dict, List, Tuple, Union


class SmartLogger:
    def __init__(self, logs_dir):
        self.mute_add = (
            "/sbin/route add -net",
            "add net ",
        )
        self.mute_delete = ("/sbin/route delete -net", "delete net ")

        self.line_controls = [
            ("SENT CONTROL", self.handle_sent_control),
            ("AUTH: Received control message: AUTH_FAILED", "Login Failed"),
            ("PUSH: Received control message: ", self.handle_recieve_control),
            ("/sbin/route add -net", self.handle_add_route),
            ("/sbin/route delete -net", self.handle_del_route),
            ("AEAD Decrypt error: cipher final failed", self.decrypt_error),
            ("OPTIONS IMPORT: --ifconfig/up options modified", self.handle_options),
            ("Initialization Sequence Completed", self.handle_success),
        ]
        local_now_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        self.log_path = f"{logs_dir}/{local_now_iso}.log"
        self.route_counter = 0
        self.add_counter = 0
        self.del_counter = 0
        print("\n-------- OPENVPN LOGS --------")
        print(f"Full vpn logs in {self.log_path}")

    def waiting(self) -> None:
        print("Waiting for next totp code...")

    def killed(self) -> None:
        print("KILLED BY THREAD")

    def end(self, return_code) -> None:
        print("OpenVPN process exited with code:", return_code)
        print("-------- END OF OPENVPN LOGS --------")

    def new_line(self, line: str) -> str | None:
        self.ovpn_log(line)

        for line_control in self.line_controls:
            key = line_control[0]
            if key not in line:
                continue

            control = line_control[1]
            if isinstance(control, str):
                print(control)
            elif callable(control):
                return_control = control(line)
                if return_control is not None:
                    return return_control

            break

        return None

    def general_check_if_log(self, line: str, mute: Tuple[str, str]) -> bool:
        for unwanted in mute:
            if unwanted in line:
                return False

        return True

    def ovpn_log(self, line: str) -> None:
        def log(line: str):
            with open(self.log_path, "a") as log_file:
                log_file.write(line)

        if not self.general_check_if_log(line, self.mute_add):
            if self.add_counter == 0:
                log("\n--- ADD LINES MUTED ---\n\n")
            return

        if not self.general_check_if_log(line, self.mute_delete):
            if self.del_counter == 0:
                log("\n--- DELETE LINES MUTED ---\n\n")
            return

        log(line)

    # Handlers
    def handle_sent_control(self, _):
        self.logging_in = True
        print("Logging in...")

    def handle_options(self, _) -> None:
        print()

    def handle_success(self, _) -> str:
        print("VPN STARTED!")
        return "started"

    def handle_recieve_control(self, line: str):
        if self.logging_in:
            print("Logged in succesfully")
            print("Recieving routes...")
            self.logging_in = False

        splited = line.split("'")
        body = splited[1]
        controls = body.split(",")
        for control in controls:
            if control.startswith("route "):
                self.route_counter += 1

        print("\rroutes:", self.route_counter, end="", flush=True)

    def handle_add_route(self, _) -> None:
        self.add_counter += 1
        print(
            f"\rAdded route {self.add_counter}/{self.route_counter}", end="", flush=True
        )
        if self.add_counter == self.route_counter:
            print()

    def handle_del_route(self, _) -> None:
        self.del_counter += 1
        print(
            f"\rDeleted route {self.add_counter}/{self.route_counter}",
            end="",
            flush=True,
        )
        if self.del_counter == self.route_counter:
            print()

    def decrypt_error(self, _) -> str:
        print("Decript Error")
        return "error"
