from rune.crypto.base import Encrypter
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.crypto.secretfield import SecretField

import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AESGCMEncrypter(Encrypter):

    @classmethod
    def encryption_algorithm(cls) -> str:
        return "aesgcm"

    def __init__(self) -> None:
        self._encryption_algorithm = self.encryption_algorithm()

    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000
        )
        return kdf.derive(password.encode())


    def encrypt(self, secret: str, key: str, **kwargs) -> SecretField:
        """
        Encrypt a secret using a password-based key.
        Returns a dictionary suitable for JSON storage.
        """
        salt = os.urandom(16)
        nonce = os.urandom(12)

        aes_key = self.derive_key(key, salt)
        aesgcm = AESGCM(aes_key)

        ciphertext = aesgcm.encrypt(nonce, secret.encode(), None)

        return SecretField(
            ciphertext=base64.b64encode(ciphertext).decode("utf-8"),
            salt=base64.b64encode(salt).decode("utf-8"),
            nonce=base64.b64encode(nonce).decode("utf-8"),
            algorithm=self._encryption_algorithm
        )

    def decrypt(self, secret: SecretField, key: str, **kwargs) -> str:
        """
        Decrypt a secret previously encrypted by encrypt().
        """
        if self._encryption_algorithm != secret.algorithm:
            raise WrongEncryptionMode(f"Secret was encrypted with mode {secret.algorithm}. Please use it to decrypt.")

        salt = base64.b64decode(secret.salt or "")
        nonce = base64.b64decode(secret.nonce or "")
        ciphertext = base64.b64decode(secret.ciphertext)

        aes_key = self.derive_key(key, salt)
        aesgcm = AESGCM(aes_key)

        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode()
        except:
            raise WrongKeyUsed("Invalid key or corrupted secret")

