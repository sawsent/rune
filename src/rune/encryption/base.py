from abc import ABC, abstractmethod
from typing import Dict, Self


class Encrypter(ABC):
    def set_encription_mode(self, mode: str) -> Self:
        self.encryption_mode = mode
        return self

    @abstractmethod
    def encrypt(self, secret: str, key: str) -> Dict:
        """
        Encrypts the provided secret with the provided key.
        """
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, secret: Dict, key: str) -> str:
        """
        Decrypts the provided secret with the provided key
        """
        raise NotImplementedError()
