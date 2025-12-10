from typing import Dict
from rune.encryption.base import Encrypter
from rune.exception.wrongencryption import WrongEncryptionMode

class NoEncryption(Encrypter):
    def encrypt(self, secret: str, key: str) -> Dict:
        """
        Encrypts the provided secret with the provided key.
        """
        return {
            "ciphertext": secret,
            "mode": self.encryption_mode
        }

    def decrypt(self, secret: Dict, key: str) -> str:
        """
        Decrypts the provided secret with the provided key
        """
        if self.encryption_mode != secret["mode"]:
            raise WrongEncryptionMode(f"Secret was encrypted with mode {secret["mode"]}. Please use it to decrypt.")
        return secret["ciphertext"]
