import socket
import json
import time

from rune.models.session.protocol.response import FailureResponse, HandshakeResp, SessionResp, GetKeyResponse, StatusResponse, SuccessResponse
from rune.models.session.protocol.command import EndSessionCmd, GetSessionKeyCmd, HandshakeCmd, SessionCmd, SessionStatusCmd, StartSessionCmd

class State:
    def __init__(self) -> None:
        self.start_time: float
        self.user: str | None = None
        self.session_key: str | None = None
        self.started: bool = False
        self.end_time: float | None = None
        self.force_finish: bool = False
        self.no_ttl: bool = False

    @property
    def time_remaining(self) -> float:
        if self.no_ttl:
            return -1
        if self.end_time:
            return self.end_time - time.time()
        return -1

    @property
    def is_finished(self) -> bool:
        if not self.started:
            return False
        if self.force_finish:
            return True
        if self.no_ttl:
            return False
        if self.time_remaining:
            return self.time_remaining < 0
        return False

    def start(self, user: str, session_key: str, ttl_seconds: int) -> None:
        if ttl_seconds == -1:
            self.no_ttl = True

        self.start_time = time.time()
        self.end_time = self.start_time + ttl_seconds

        self.user = user
        self.started = True
        self.session_key = session_key

    def end(self) -> None:
        self.force_finish = True

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
                    response = FailureResponse("Error decoding request.")


                conn.sendall((json.dumps(response.to_dict()) + "\n").encode("utf-8"))


def process_request(request: SessionCmd, state: State) -> SessionResp:
    cmd = request.CMD

    match cmd:
        case SessionCmd.GET_SESSION_KEY if isinstance(request, GetSessionKeyCmd):
            if state.user != request.user:
                return FailureResponse("Stored Session Key was provided by a different user.")
            if state.session_key:
                return GetKeyResponse(state.session_key)
            else:
                return FailureResponse("Session key is not set")
        case SessionCmd.START_SESSION if isinstance(request, StartSessionCmd):
            if not state.started:
                state.start(request.user, request.session_key, request.ttl)
                return SuccessResponse("Session started")
            else:
                return FailureResponse("Session already in progress")
        case SessionCmd.END_SESSION if isinstance(request, EndSessionCmd):
            if state.started:
                state.end()
                return SuccessResponse("Session ended")
            else:
                return FailureResponse("No session in progress")
        case SessionCmd.SESSION_STATUS if isinstance(request, SessionStatusCmd):
            if state.time_remaining:
                return StatusResponse(int(state.time_remaining), state.user or "")
            else:
                return StatusResponse(-1, state.user or "")
        case SessionCmd.HANDSHAKE if isinstance(request, HandshakeCmd):
            return HandshakeResp(all_good=True)

    return FailureResponse(f"Unknown command type {cmd} or session format {str(type(request))}.")


def main(host: str, port: int):
    state = State()
    print(state)
    print(state.is_finished)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        s.bind((host, port))
        s.listen()

        while not state.is_finished:
            try:
                conn, addr = s.accept()
                handle_client(conn, addr, state)
            except TimeoutError:
                continue

