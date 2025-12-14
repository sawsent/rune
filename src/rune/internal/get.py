from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Result, Success, Failure
from rune.storage.secrets import factory as StorageManagerFactory
from rune.encryption import factory as EncrypterFactory

from typing import Dict

from rune.utils.input import get_fqn

def get_secret(user: str, name: str, namespace: str, key: str) -> Result[Dict[str, str]]:
    """
    Retreives the encrypted secret via the configured storage manager.
    Decrypts the ciphertext with the provided key.

    Returns the decrypted secret, if it exists.
    Returns None if not successful.
    """
    storage = StorageManagerFactory.get_configured_storage_manager()

    fqn = get_fqn(name, namespace)

    try:
        secret = storage.retreive_secret(user, fqn)
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
            return Failure(f"Secret '{fqn}' does not exist.")

    except NotFoundError as err:
        return Failure(err.message)


