from rune.crypto.base import Encrypter
from rune.crypto.aesgcm import AESGCMEncrypter
from rune.models.settings.encryptionsettings import AES_GCMEncryptionSettings
from rune.models.settings.settings import Settings

def get_encrypter(settings: Settings) -> Encrypter:
    match settings.encryption:
        case AES_GCMEncryptionSettings():
            return AESGCMEncrypter()
        case _:
            raise ValueError(f"Algorithm '{settings.encryption.mode}' is not supported.")

def get_encrypter_by_algorithm(algorithm: str | None) -> Encrypter:
    if algorithm == AESGCMEncrypter.encryption_algorithm():
        return AESGCMEncrypter()

    raise ValueError(f"Algorithm '{algorithm}' is not supported.")


