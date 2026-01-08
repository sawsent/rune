import time
from typing import Optional
import socket
import json
import subprocess
import sys

from rune.models.session.protocol.command import EndSessionCmd, GetSessionKeyCmd, HandshakeCmd, SessionCmd, SessionStatusCmd, StartSessionCmd
from rune.models.session.protocol.response import FailureResponse, GetKeyResponse, HandshakeResp, SessionResp, StatusResponse, SuccessResponse
from rune.models.session.status import SessionStatus
from rune.session.base import SessionManager
from rune.utils.environment import sanitized_env
from rune.exception.session import NoSessionError, WrongUserError


class DaemonSessionManager(SessionManager):
    def __init__(self, daemon_host: str, daemon_port: int) -> None:
        self.daemon_host = daemon_host
        self.daemon_port = daemon_port

    def start_session(self, user: str, session_key: str, ttl_seconds: int) -> None:
        """
        Starts a session.
        Session exists for the provided ttl.
        """
        if not self._is_daemon_started():
            self._spawn_daemon()

        self.make_request(StartSessionCmd(session_key, ttl_seconds, user))


    def end_session(self) -> None:
        """
        Ends the current session.

        raises NoSessionError if the session does not exist.
        """
        if not self._is_daemon_started():
            raise NoSessionError("No session in progress.")

        resp = self.make_request(EndSessionCmd())
        if isinstance(resp, SuccessResponse):
            return

        raise RuntimeError(str(resp.to_dict()))

    def is_session_in_progress(self) -> bool:
        """
        Returns true if there is an ongoing session

        False otherwise.
        """
        if not self._is_daemon_started():
            return False

        resp = self.make_request(SessionStatusCmd())
        if isinstance(resp, StatusResponse):
            return resp.remaining_ttl != -1

        return False


    def get_default_key(self, user: str) -> Optional[str]:
        """
        Retrieves the default key for this session.
        Returns None if the key is not set.

        Raises NoSessionError if the session does not exist.
        Raises WrongUserError if the user is not the same as the one that started the session.
        """
        if not self._is_daemon_started():
            raise NoSessionError("No session in progress.")

        resp = self.make_request(GetSessionKeyCmd(user))
        if isinstance(resp, FailureResponse):
            raise WrongUserError(resp.message)

        if isinstance(resp, GetKeyResponse):
            return resp.session_key

        return None

    def get_session_status(self) -> SessionStatus:
        """
        Retrieves the session status.

        Raises NoSessionError if the session does not exist.
        """
        try:
            resp = self.make_request(SessionStatusCmd())
            if isinstance(resp, StatusResponse):
                return SessionStatus(True, resp.remaining_ttl, resp.user)
            return SessionStatus.STARTED_UNKNOWN()
        except:
            return SessionStatus.NOT_STARTED()

    def _is_daemon_started(self, timeout: float = 1) -> bool:
        try:
            resp = self.make_request(HandshakeCmd(), timeout)
            return isinstance(resp, HandshakeResp) and resp.all_good
        except:
            return False

    def _spawn_daemon(self) -> bool:
        env = sanitized_env({
            "HOST": self.daemon_host,
            "PORT": str(self.daemon_port),
        })

        subprocess.Popen(
            [sys.executable, "-m", "rune.session.daemon"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=env,
            close_fds=True,
            start_new_session=True,
        )

        time.sleep(0.5)

        return self._is_daemon_started()

    def make_request(self, request: SessionCmd, timeout: float = 1) -> SessionResp:
        with socket.create_connection((self.daemon_host, self.daemon_port)) as s:
            s.sendall((json.dumps(request.to_dict()) + "\n").encode("utf-8"))

            s.settimeout(timeout)
            response = s.recv(4096)
            return SessionResp.from_dict(json.loads(response.decode("utf-8")))




