from rune.encryption.base import Encrypter
from rune.utils.settings import get_configured_encryption_identifier
from rune.encryption.aesgcm import AESGCMEncrypter
from rune.encryption.noencryption import NoEncryption

def get_configured_encrypter() -> Encrypter:
    return get_encrypter(algorithm=get_configured_encryption_identifier())

def get_encrypter(algorithm: str | None) -> Encrypter:
    if algorithm == NoEncryption.encryption_algorithm():
        return NoEncryption()
    if algorithm == AESGCMEncrypter.encryption_algorithm():
        return AESGCMEncrypter()

    raise ValueError(f"Algorithm '{algorithm}' is not supported.")

