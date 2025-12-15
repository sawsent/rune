from rune.context import Context
from rune.crypto import factory as EncryptionFactory
from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Failure, Result, Success

from typing import Dict

def update_secret(user: str, full_name: str, fields: Dict[str, str], key: str) -> Result[None]:
    """
    Encrypts a secret with the configured encrypter.
    Updates the encrypted secret (if it exists) with the configured storage manager.

    Returns the result.
    """
    storage = Context.get().storage_manager

    try:
        original_secret = storage.retreive_secret(user, full_name)
        decrypted_fields = {}
        if original_secret is not None:
            for full_name, field in original_secret.fields.items():
                encrypter = EncryptionFactory.get_encrypter_by_algorithm(field.algorithm)
                decrypted_fields[full_name] = encrypter.decrypt(field, key)
        else:
            return Failure(f"Secret '{full_name}' does not exist. You can create it with `rune add -n {full_name}`.")
    except WrongKeyUsed as err:
        return Failure(f"You have to use the same key to update a secret.")

    encrypter = Context.get().configured_encrypter
    provided_encrypted_fields = {name: encrypter.encrypt(secret, key) for name, secret in fields.items()}

    encrypted_fields = {}
    for full_name, f in original_secret.fields.items():
        encrypted_fields[full_name] = provided_encrypted_fields.get(full_name) or f

    for full_name, f in provided_encrypted_fields.items():
        if full_name not in original_secret.fields:
            encrypted_fields[full_name] = f

    model = original_secret.update(
        algorithm = encrypter._encryption_algorithm,
        fields = encrypted_fields
    )
    try:
        if storage.store_secret(model):
            return Success()
        else:
            return Failure(f"Storage manager could not store the secret {full_name}.")

    except NotFoundError as err:
        return Failure(err.message)

