from abc import ABC, abstractmethod
from typing import Optional

from rune.models.session.status import SessionStatus


class SessionManager(ABC):
    @abstractmethod
    def start_session(self, user: str, session_key: str, ttl_seconds: int) -> None:
        """
        Starts a session.
        Session exists for the provided ttl. (-1 means it will not close)
        """
        raise NotImplementedError()

    @abstractmethod
    def end_session(self) -> None:
        """
        Ends the current session.

        raises NoSessionError if the session does not exist.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_session_in_progress(self) -> bool:
        """
        Returns true if there is an ongoing session

        False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_default_key(self, user: str) -> Optional[str]:
        """
        Retrieves the default key for this session.
        Returns None if the key is not set.

        Raises NoSessionError if the session does not exist.
        Raises WrongUserError if the user is not the same as the one that started the session.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_session_status(self) -> SessionStatus:
        """
        Retrieves the session status.

        Raises NoSessionError if the session does not exist.
        """
        raise NotImplementedError()


