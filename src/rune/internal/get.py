from rune.context import Context
from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongencryption import WrongEncryptionMode
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Result, Success, Failure
from rune.crypto import factory as EncrypterFactory

from typing import Dict, Tuple

def get_secret(user: str, full_name: str, key: str) -> Result[Dict[str, Tuple[str, bool]]]:
    """
    Retreives the encrypted secret via the configured storage manager.
    Decrypts the ciphertext with the provided key.

    Returns the decrypted secret, if it exists.
    Returns None if not successful.
    """
    storage = Context.get().storage_manager

    try:
        secret = storage.retreive_secret(user, full_name)
        if secret is not None:
            try:
                decrypted_fields = {}
                for field_name, field in secret.fields.items():
                    encrypter = EncrypterFactory.get_encrypter_by_algorithm(field.algorithm)
                    decrypted_fields[field_name] = (encrypter.decrypt(field, key), field.deleted)
            except WrongEncryptionMode as err:
                return Failure(err.message)
            except WrongKeyUsed as err:
                return Failure(err.message)

            return Success(decrypted_fields)
        else:
            return Failure(f"Secret '{full_name}' does not exist.")

    except NotFoundError as err:
        return Failure(err.message)


