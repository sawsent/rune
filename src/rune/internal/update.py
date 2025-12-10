from rune.encryption import factory as EncryptionFactory
from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Failure, Result, Success
from rune.models.secret import Secret
from rune.storage import factory as StorageManagerFactory
from time import time_ns

def update_secret(name: str, secret: str, key: str) -> Result[None]:
    """
    Encrypts a secret with the configured encrypter.
    Updates the encrypted secret (if it exists) with the configured storage manager.

    Returns the result.
    """
    encrypter = EncryptionFactory.get_configured_encrypter()
    storage = StorageManagerFactory.get_configured_storage_manager()

    try:
        original_secret = storage.retreive_ciphertext(name)
        if original_secret is not None:
            encrypter.decrypt(original_secret.data, key)
        else:
            return Failure(f"Secret '{name}' does not exist. You can create it with `rune add -n {name}`.")
    except WrongKeyUsed as err:
        return Failure(f"You have to use the same key to update a secret.")

    model = Secret(name, encrypter.encrypt(secret, key), time_ns())

    try:
        if storage.store_ciphertext(model):
            return Success()
        else:
            return Failure(f"Storage manager could not store the secret {name}.")

    except NotFoundError as err:
        return Failure(err.message)

