from rune.session.base import SessionManager
from typing import Optional


class MockSessionManager(SessionManager):
    def start_session(self, default_password: Optional[str] = None, ttl_seconds: int = -1) -> None:
        """
        Starts a session.
        Session exists for the provided ttl. (-1 means it will not close)
        """
        pass

    def end_session(self) -> None:
        """
        Ends the current session.

        raises NoSessionError if the session does not exist.
        """
        pass

    def is_session_in_progress(self) -> bool:
        """
        Returns true if there is an ongoing session

        False otherwise.
        """
        return True

    def set_default_key(self, key: str) -> None:
        """
        Sets the default key for this session.

        raises NoSessionError if the session does not exist.
        """
        pass

    def get_default_key(self) -> Optional[str]:
        """
        Retrieves the default key for this session.
        Returns None if the key is not set.

        Raises NoSessionError if the session does not exist.
        """
        return "default-key"

    def is_default_key_defined(self) -> bool:
        """
        Raises NoSessionError if the session does not exist
        """
        return True

