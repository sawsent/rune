from rune.encryption.base import Encrypter

class NoEncryption(Encrypter):
    def encrypt(self, secret: str, key: str) -> str:
        """
        Encrypts the provided secret with the provided key.
        """
        return secret

    def decrypt(self, secret: str, key: str) -> str:
        """
        Decrypts the provided secret with the provided key
        """
        return secret
