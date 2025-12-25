import socket
import json
import threading
import time

from rune.models.session.protocol.response import FailureResponse, SessionResp, GetKeyResponse, StatusResponse, SuccessResponse
from rune.models.session.protocol.command import GetSessionKeyCmd, SessionCmd, StartSessionCmd

class State:
    def __init__(self) -> None:
        self.user: str | None = None
        self.session_key: str | None = None
        self.ttl_seconds: int | None = None
        self.start_time: float | None = None

    @property
    def time_remaining(self) -> float:
        if self.start_time and self.ttl_seconds:
            return self.start_time + self.ttl_seconds - time.time()
        raise ValueError("Session not started")

    @property
    def started(self) -> bool:
        if self.start_time:
            return True
        else:
            return False

    @property
    def is_finished(self) -> bool:
        if self.ttl_seconds == None:
            return False
        try:
            return self.time_remaining > 0
        except:
            return False

    def start(self, user: str, session_key: str, ttl_seconds: int) -> None:
        self.user = user
        self.start_time = time.time()
        self.session_key = session_key
        self.ttl_seconds = ttl_seconds

    def end(self) -> None:
        self.ttl_seconds = 0

def handle_client(conn, addr, state: State):
    with conn:
        buffer = ""
        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                try:
                    request = SessionCmd.from_dict(json.loads(line))
                    response = process_request(request, state)
                except json.JSONDecodeError:
                    response = FailureResponse("Error decoding requrest.")


                conn.sendall((json.dumps(response.to_dict()) + "\n").encode("utf-8"))


def process_request(request: SessionCmd, state: State) -> SessionResp:
    cmd = request.CMD

    match request.CMD:
        case SessionCmd.GET_SESSION_KEY:
            if not isinstance(request, GetSessionKeyCmd):
                return FailureResponse("Something is wrong with the protocol.")
            if state.user != request.user:
                return FailureResponse("Stored Session Key was provided by a different user.")
            if state.session_key:
                return GetKeyResponse(state.session_key)
            else:
                return FailureResponse("Session key is not set")
        case SessionCmd.START_SESSION:
            if not isinstance(request, StartSessionCmd):
                return FailureResponse("Something is wrong with the protocol.")
            if not state.started:
                state.start(request.user, request.session_key, request.ttl)
                return SuccessResponse("Session started")
            else:
                return FailureResponse("Session already in progress")
        case SessionCmd.END_SESSION:
            if state.started:
                state.end()
                return SuccessResponse("Session ended")
            else:
                return FailureResponse("No session in progress")
        case SessionCmd.SESSION_STATUS:
            try:
                return StatusResponse(int(state.time_remaining), str(state.user))
            except:
                return StatusResponse(-1, "None")

    return FailureResponse(f"Unknown command type {cmd}.")


def main():
    HOST = "localhost"
    PORT = 5000
    state = State()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(10)
        print(f"Daemon listening on {HOST}:{PORT}")

        while not state.is_finished:
            try:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr, state), daemon=True).start()
            except:
                continue

