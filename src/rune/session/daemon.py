from typing import Optional
import socket
import json

from rune.models.session.protocol.command import SessionCmd, StartSessionCmd
from rune.models.session.protocol.response import SessionResp
from rune.session.base import SessionManager


class DaemonSessionManager(SessionManager):
    def __init__(self, daemon_host: str, daemon_port: int) -> None:
        self.daemon_host = daemon_host
        self.daemon_port = daemon_port

    def start_session(self, user: str, session_key: str, ttl_seconds: int) -> None:
        """
        Starts a session.
        Session exists for the provided ttl. (-1 means it will not close)
        """
        command = StartSessionCmd(session_key, ttl_seconds, user)
        try:
            response = self.make_request(command)
            print(response.RESP)
            
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

    def make_request(self, request: SessionCmd, timeout: float = 1) -> SessionResp:
        with socket.create_connection((self.daemon_host, self.daemon_port)) as s:
            s.sendall((json.dumps(request.to_dict()) + "\n").encode("utf-8"))

            s.settimeout(timeout)
            response = s.recv(4096)
            return SessionResp.from_dict(json.loads(response.decode("utf-8")))




