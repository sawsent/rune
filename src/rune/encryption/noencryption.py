from rune.encryption.base import Encrypter
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.models.secret import SecretField

class NoEncryption(Encrypter):
    @classmethod
    def encryption_algorithm(cls) -> str:
        return "no-encryption"

    def __init__(self) -> None:
        self._encryption_algorithm = "no-encryption"

    def encrypt(self, secret: str, key: str, **kwargs) -> SecretField:
        """
        Encrypts the provided secret with the provided key.
        """
        return SecretField(
            ciphertext=secret,
            algorithm=self._encryption_algorithm
        )

    def decrypt(self, secret: SecretField, key: str, **kwargs) -> str:
        """
        Decrypts the provided secret with the provided key
        """
        if self._encryption_algorithm != secret.algorithm:
            raise WrongEncryptionMode(f"Secret was encrypted with mode {secret.algorithm}. Please use it to decrypt.")
        return secret.ciphertext
