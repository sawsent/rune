from abc import ABC, abstractmethod
from typing import Optional


class SessionManager(ABC):
    @abstractmethod
    def start_session(self, username: str, ttl_seconds: int = -1) -> None:
        """
        Starts a session for the provided username.

        Session exists for the provided ttl. (-1 means it will not close unless the shell is restarted)
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
    def set_default_key(self, key: str) -> None:
        """
        Sets the default key for this session.

        raises NoSessionError if the session does not exist.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_default_key(self) -> Optional[str]:
        """
        Retrieves the default key for this session.
        Returns None if the key is not set.

        Raises NoSessionError if the session does not exist.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_default_key_defined(self) -> bool:
        """
        Raises NoSessionError if the session does not exist
        """
        raise NotImplementedError()

    

