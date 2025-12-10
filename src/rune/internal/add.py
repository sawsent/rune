from rune.encryption.factory import get_configured_encrypter
from rune.storage.factory import get_configured_storage_manager

def add_secret(name: str, secret: str, key: str) -> None:
    encrypter = get_configured_encrypter()
    storage = get_configured_storage_manager()
    ciphertext = encrypter.encrypt(secret, key)
    storage.store_ciphertext(name, ciphertext)

