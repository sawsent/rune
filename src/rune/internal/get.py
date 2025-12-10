from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Result, Success, Failure
from rune.storage import factory as StorageManagerFactory
from rune.encryption import factory as EncrypterFactory

def get_secret(name: str, key: str) -> Result[str]:
    """
    Retreives the encrypted secret via the configured storage manager.
    Decrypts the ciphertext with the provided key.

    Returns the decrypted secret, if it exists.
    Returns None if not successful.
    """
    encrypter = EncrypterFactory.get_configured_encrypter()
    storage = StorageManagerFactory.get_configured_storage_manager()

    try:
        secret = storage.retreive_ciphertext(name)
        if secret is not None:
            try:
                decrypted = encrypter.decrypt(secret.data, key)
                return Success(decrypted)
            except WrongEncryptionMode as err:
                return Failure(err.message)
            except WrongKeyUsed as err:
                return Failure(err.message)
        else:
            return Failure(f"Secret '{name}' does not exist.")

    except NotFoundError as err:
        return Failure(err.message)


