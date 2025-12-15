from abc import ABC, abstractmethod

from rune.models.crypto.secretfield import SecretField


class Encrypter(ABC):
    def __init__(self) -> None:
        self._encryption_algorithm: str

    @abstractmethod
    def encrypt(self, secret: str, key: str, **kwargs) -> SecretField:
        """
        Encrypts the provided secret with the provided key.
        """
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, secret: SecretField, key: str, **kwargs) -> str:
        """
        Decrypts the provided secret with the provided key
        """
        raise NotImplementedError()
