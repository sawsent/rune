from typing import Optional
import socket
import json
import subprocess
import sys

from rune.models.session.protocol.command import HandshakeCmd, SessionCmd, StartSessionCmd
from rune.models.session.protocol.response import HandshakeResp, SessionResp
from rune.session.base import SessionManager
from rune.utils.environment import sanitized_env


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

        command = StartSessionCmd(session_key, ttl_seconds, user)

        try:
            response = self.make_request(command)
            print(response.to_dict())
            
        except RuntimeError as e:
            print(e)


    def end_session(self) -> None:
        """
        Ends the current session.

        raises NoSessionError if the session does not exist.
        """
        raise NotImplementedError()

    def is_session_in_progress(self) -> bool:
        """
        Returns true if there is an ongoing session

        False otherwise.
        """
        raise NotImplementedError()

    def get_default_key(self) -> Optional[str]:
        """
        Retrieves the default key for this session.
        Returns None if the key is not set.

        Raises NoSessionError if the session does not exist.
        """
        raise NotImplementedError()

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

        return self._is_daemon_started()

    def make_request(self, request: SessionCmd, timeout: float = 1) -> SessionResp:
        with socket.create_connection((self.daemon_host, self.daemon_port)) as s:
            s.sendall((json.dumps(request.to_dict()) + "\n").encode("utf-8"))

            s.settimeout(timeout)
            response = s.recv(4096)
            return SessionResp.from_dict(json.loads(response.decode("utf-8")))




