from abc import ABC, abstractmethod
from typing import List, Optional

class StorageManager(ABC):
    @abstractmethod
    def store_ciphertext(self, name: str, ciphertext: str) -> None:
        """
        Stores the provided ciphertext under the provided secret name.
        """
        raise NotImplementedError()

    @abstractmethod
    def retreive_ciphertext(self, name: str) -> Optional[str]:
        """
        Retreives the provided ciphertext under the provided secret name.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_entries(self) -> List[str]:
        """
        Retrieves all entry names.
        """
        raise NotImplementedError()


