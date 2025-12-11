from abc import ABC, abstractmethod
from typing import List, Optional

from rune.models.secret import Secret

class StorageManager(ABC):
    @abstractmethod
    def store_secret(self, secret: Secret) -> bool:
        """
        Stores the provided ciphertext under the provided secret name.

        Returns True if storage is successful, False otherwise.
        Raises NotFoundError if it fails to find a secrets file.
        """
        raise NotImplementedError()

    @abstractmethod
    def retreive_secret(self, name: str, namespace: str)-> Optional[Secret]:
        """
        Retreives the provided ciphertext under the provided secret name.

        Raises NotFoundError if it fails to find a secrets file.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_secret(self, name: str, namespace: str) -> bool:
        """
        Deletes the entry with the provided name.

        Returns True if successful, False if it fails.
        Raises NotFoundError if it fails to find a secrets file.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_all_secrets(self) -> List[Secret]:
        """
        Retrieves all entry names.

        Raises NotFoundError if it fails to retreive entries.
        """
        raise NotImplementedError()


