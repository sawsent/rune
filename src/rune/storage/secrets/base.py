from abc import ABC, abstractmethod
from typing import List, Optional

from rune.models.crypto.secret import Secret

class StorageManager(ABC):
    @abstractmethod
    def store_secret(self, secret: Secret) -> bool:
        """
        Stores the provided secret.

        Returns True if storage is successful, False otherwise.
        Raises NotFoundError if it fails to find a secrets file.
        """
        raise NotImplementedError()

    @abstractmethod
    def retreive_secret(self, user: str, name: str)-> Optional[Secret]:
        """
        Retreives the provided ciphertext under the provided secret name under the provided user.

        Raises NotFoundError if it fails to find a secrets file.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_secret(self, user: str, name: str) -> bool:
        """
        Deletes the entry with the provided name for the provided user.

        Returns True if successful, False if it fails.
        Raises NotFoundError if it fails to find a secrets file.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all_secrets(self, user: str) -> List[Secret]:
        """
        Retrieves all entry names for a specific user.

        Raises NotFoundError if it fails to retreive entries.
        """
        raise NotImplementedError()


