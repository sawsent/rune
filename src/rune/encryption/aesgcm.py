import os
import base64
from typing import Dict
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from rune.encryption.base import Encrypter
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.exception.wrongkey import WrongKeyUsed

class AESGCMEncrypter(Encrypter):
    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=600000
        )
        return kdf.derive(password.encode())


    def encrypt(self, secret: str, key: str) -> Dict:
        """
        Encrypt a secret using a password-based key.
        Returns a dictionary suitable for JSON storage.
        """
        salt = os.urandom(16)
        nonce = os.urandom(12)

        aes_key = self.derive_key(key, salt)
        aesgcm = AESGCM(aes_key)

        ciphertext = aesgcm.encrypt(nonce, secret.encode(), None)

        return {
            "mode": self.encryption_mode,
            "salt": base64.b64encode(salt).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
        }


    def decrypt(self, secret: Dict, key: str) -> str:
        """
        Decrypt a secret previously encrypted by encrypt().
        """
        if self.encryption_mode != secret["mode"]:
            raise WrongEncryptionMode(f"Secret was encrypted with mode {secret["mode"]}. Please use it to decrypt.")

        salt = base64.b64decode(secret["salt"])
        nonce = base64.b64decode(secret["nonce"])
        ciphertext = base64.b64decode(secret["ciphertext"])

        aes_key = self.derive_key(key, salt)
        aesgcm = AESGCM(aes_key)

        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext.decode()
        except:
            raise WrongKeyUsed("Invalid key or corrupted secret")

