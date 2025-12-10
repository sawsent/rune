from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Result, Success, Failure
from rune.storage import factory as StorageManagerFactory
from rune.encryption import factory as EncrypterFactory

from typing import Dict

def get_secret(name: str, key: str, namespace: str = "") -> Result[Dict[str, str]]:
    """
    Retreives the encrypted secret via the configured storage manager.
    Decrypts the ciphertext with the provided key.

    Returns the decrypted secret, if it exists.
    Returns None if not successful.
    """
    storage = StorageManagerFactory.get_configured_storage_manager()

    try:
        secret = storage.retreive_ciphertext(name, namespace)
        if secret is not None:
            try:
                decrypted_fields = {}
                for field_name, field in secret.fields.items():
                    encrypter = EncrypterFactory.get_encrypter(field.algorithm)
                    decrypted_fields[field_name] = encrypter.decrypt(field, key)
            except WrongEncryptionMode as err:
                return Failure(err.message)
            except WrongKeyUsed as err:
                return Failure(err.message)

            return Success(decrypted_fields)
        else:
            return Failure(f"Secret '{name}' does not exist.")

    except NotFoundError as err:
        return Failure(err.message)


