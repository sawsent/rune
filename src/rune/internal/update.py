from typing import Dict
from rune.encryption import factory as EncryptionFactory
from rune.exception.notfounderror import NotFoundError
from rune.exception.wrongkey import WrongKeyUsed
from rune.models.result import Failure, Result, Success
from rune.storage import factory as StorageManagerFactory

def update_secret(name: str, fields: Dict[str, str], key: str, namespace: str = "") -> Result[None]:
    """
    Encrypts a secret with the configured encrypter.
    Updates the encrypted secret (if it exists) with the configured storage manager.

    Returns the result.
    """
    storage = StorageManagerFactory.get_configured_storage_manager()

    try:
        original_secret = storage.retreive_ciphertext(name, namespace)
        decrypted_fields = {}
        if original_secret is not None:
            for name, field in original_secret.fields.items():
                encrypter = EncryptionFactory.get_encrypter(field.algorithm)
                decrypted_fields[name] = encrypter.decrypt(field, key)
        else:
            return Failure(f"Secret '{name}' does not exist. You can create it with `rune add -n {name}`.")
    except WrongKeyUsed as err:
        return Failure(f"You have to use the same key to update a secret.")

    encrypter = EncryptionFactory.get_configured_encrypter()
    provided_encrypted_fields = {name: encrypter.encrypt(secret, key) for name, secret in fields.items()}

    encrypted_fields = {}
    for name, f in original_secret.fields.items():
        encrypted_fields[name] = provided_encrypted_fields.get(name) or f

    for name, f in provided_encrypted_fields.items():
        if name not in original_secret.fields:
            encrypted_fields[name] = f

    model = original_secret.update(
        algorithm = encrypter._encryption_algorithm,
        fields = encrypted_fields
    )
    try:
        if storage.store_ciphertext(model):
            return Success()
        else:
            return Failure(f"Storage manager could not store the secret {name}.")

    except NotFoundError as err:
        return Failure(err.message)

