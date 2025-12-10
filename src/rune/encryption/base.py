from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    def encrypt(self, secret: str, key: str) -> str:
        """
        Encrypts the provided secret with the provided key.
        """
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, secret: str, key: str) -> str:
        """
        Decrypts the provided secret with the provided key
        """
        raise NotImplementedError()
